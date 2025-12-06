import pandas as pd

def get_top_bottom_countries(df, year, n=5):
    """
    Retorna los Top N y Bottom N países.
    """
    df_year = df[df['Year'] == year]
    
    # Seleccionar columnas existentes
    cols = ['Country', 'Happiness_Score', 'GDP_per_Capita', 'Social_Support']
    valid_cols = [c for c in cols if c in df.columns]
    
    top = df_year.nlargest(n, 'Happiness_Score')[valid_cols]
    top.index = range(1, n + 1)
    
    bottom = df_year.nsmallest(n, 'Happiness_Score')[valid_cols].sort_values('Happiness_Score')
    bottom.index = range(1, n + 1)
    
    return top, bottom


def get_country_best_traits(df, countries):
    """
    Identifica las 3 variables más fuertes de cada país seleccionado.
    (Normaliza los datos para comparar peras con manzanas).
    """
    # 1. Definir columnas a evaluar y sus nombres bonitos
    traits = {
        'GDP_per_Capita': 'Economía',
        'Social_Support': 'Apoyo Social',
        'Healthy_Life_Expectancy': 'Salud',
        'Freedom': 'Libertad',
        'Generosity': 'Generosidad',
        'Corruption_Perception': 'Baja Corrupción' # Nombre especial porque se invierte
    }
    
    results = []
    
    # 2. Calcular min y max globales para normalizar (Escala 0-1)
    global_min = df[list(traits.keys())].min()
    global_max = df[list(traits.keys())].max()
    
    for country in countries:
        # Filtrar datos del país (Promedio histórico)
        c_data = df[df['Country'] == country]
        if c_data.empty: continue
        
        means = c_data[list(traits.keys())].mean()
        
        # 3. Normalizar cada variable para ver cuál es su "Fuerte" relativo al mundo
        scores = {}
        for col, name in traits.items():
            val = means[col]
            mn, mx = global_min[col], global_max[col]
            
            if col == 'Corruption_Perception':
                # Invertir: Menos es mejor. (1 - normalizado)
                # Si tienes 0.1 de corrupción (bajo), tu score es alto.
                score = 1 - ((val - mn) / (mx - mn))
            else:
                # Normal: Más es mejor
                score = (val - mn) / (mx - mn)
            
            scores[name] = score
            
        # 4. Ordenar y tomar Top 3
        top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Formatear fila
        row = {"País": country}
        row["Pilar #1 (Más Fuerte)"] = f"{top_3[0][0]} ({top_3[0][1]*100:.0f}%)"
        row["Pilar #2"] = f"{top_3[1][0]} ({top_3[1][1]*100:.0f}%)"
        row["Pilar #3"] = f"{top_3[2][0]} ({top_3[2][1]*100:.0f}%)"
        
        results.append(row)
        
    return pd.DataFrame(results)