import pandas as pd
import streamlit as st
import os

def load_local_data(folder_path='data'):
    """
    Carga el archivo 'World Happiness Report.csv' (2005-2022).
    Carga TODAS las variables disponibles.
    """
    if not os.path.exists(folder_path):
        st.error(f"⚠️ La carpeta '{folder_path}' no existe.")
        return None

    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not files:
        st.error(f"⚠️ No hay CSV en '{folder_path}'.")
        return None

    file_path = os.path.join(folder_path, files[0])
    print(file_path)
    
    try:
        df = pd.read_csv(file_path)
        df.columns = [c.strip() for c in df.columns]

        # Mapeo Completo de TODAS las variables
        rename_map = {
            'Country Name': 'Country',
            'Regional Indicator': 'Region',
            'Year': 'Year',
            'Life Ladder': 'Happiness_Score',
            'Log GDP Per Capita': 'GDP_per_Capita',
            'Social Support': 'Social_Support',
            'Healthy Life Expectancy At Birth': 'Healthy_Life_Expectancy',
            'Freedom To Make Life Choices': 'Freedom',
            'Generosity': 'Generosity',
            'Perceptions Of Corruption': 'Corruption_Perception',
            # Nuevas variables del dataset completo
            'Positive Affect': 'Positive_Affect',
            'Negative Affect': 'Negative_Affect',
            'Confidence In National Government': 'Confidence_in_Gov'
        }
        
        df = df.rename(columns=rename_map)
        
        # Rellenar Región
        if 'Region' in df.columns:
            df['Region'] = df['Region'].fillna('Unknown')
        else:
            df['Region'] = 'Unknown'

        # Lista completa de numéricos para limpiar
        numeric_cols = [
            'Happiness_Score', 'GDP_per_Capita', 'Social_Support', 
            'Healthy_Life_Expectancy', 'Freedom', 'Generosity', 
            'Corruption_Perception', 'Positive_Affect', 'Negative_Affect', 
            'Confidence_in_Gov'
        ]
        
        # Rellenar nulos con promedio (Imputación simple)
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].mean())
            else:
                # Si la columna no existe en el csv, la creamos con 0
                df[col] = 0

        return df.sort_values(by=['Year', 'Happiness_Score'], ascending=[True, False])

    except Exception as e:
        st.error(f"Error al cargar: {e}")
        return None