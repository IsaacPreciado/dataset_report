import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
import streamlit as st

# Estilo profesional para reportes
sns.set_theme(style="whitegrid")

def plot_distributions_grid(df):
    """
    EDA UNIVARIADO: Muestra la distribución de las 6 variables clave.
    Ayuda a detectar sesgos (skewness) y normalidad.
    """
    vars_to_plot = ['Happiness_Score', 'GDP_per_Capita', 'Social_Support', 
                    'Healthy_Life_Expectancy', 'Freedom', 'Corruption_Perception']
    
    # Filtramos solo las que existen
    vars_exist = [v for v in vars_to_plot if v in df.columns]
    
    fig, axs = plt.subplots(2, 3, figsize=(18, 10))
    axs = axs.flatten()
    
    for i, col in enumerate(vars_exist):
        sns.histplot(df[col], kde=True, ax=axs[i], color='#34495e', edgecolor='white')
        axs[i].set_title(f'Distribución: {col}', fontsize=11, fontweight='bold')
        axs[i].set_xlabel('')
        axs[i].set_ylabel('')
    
    plt.tight_layout()
    return fig

def plot_global_factors_6(df):
    """
    EDA BIVARIADO: Panel de 3x2 scatter plots.
    Cruza Felicidad vs Las 6 Variables principales para ver linealidad.
    """
    fig, axs = plt.subplots(2, 3, figsize=(20, 12))
    axs = axs.flatten()
    
    # Lista de configuraciones (Variable, Color, Título)
    configs = [
        ('GDP_per_Capita', '#2980b9', 'Economía (Log PIB)'),
        ('Social_Support', '#27ae60', 'Apoyo Social'),
        ('Healthy_Life_Expectancy', '#d35400', 'Esperanza de Vida'),
        ('Freedom', '#f1c40f', 'Libertad'),
        ('Generosity', '#8e44ad', 'Generosidad'),
        ('Corruption_Perception', '#c0392b', 'Corrupción')
    ]

    for i, (col, color, title) in enumerate(configs):
        if col in df.columns:
            # Scatter con regresión
            sns.regplot(data=df, x=col, y='Happiness_Score', ax=axs[i], 
                        scatter_kws={'alpha':0.2, 's':10, 'color':color}, 
                        line_kws={'color':'black', 'linewidth':1})
            axs[i].set_title(f'{title} vs Felicidad', fontsize=12, fontweight='bold')
            axs[i].set_xlabel(title)
            axs[i].set_ylabel('Felicidad' if i % 3 == 0 else '')
    
    plt.tight_layout()
    return fig


def plot_variable_importance(df):
    """
    Gráfica de Barras Dinámica:
    Muestra solo las TOP 5 variables con mayor correlación (positiva o negativa).
    """
    target = 'Happiness_Score'
    if target not in df.columns:
        return None
    
    # 1. Selección Dinámica
    numeric_df = df.select_dtypes(include=['number'])
    features = [col for col in numeric_df.columns if col not in [target, 'Year']]
    
    if not features:
        return None
    
    # 2. Cálculo Real
    corrs = df[features].corrwith(df[target]).reset_index()
    corrs.columns = ['Factor', 'Correlación']
    
    # 3. Lógica Visual (Flip de Corrupción)
    corrs['Visual'] = corrs.apply(
        lambda row: row['Correlación'] * -1 if 'Corruption' in row['Factor'] else row['Correlación'], 
        axis=1
    )
    
    # 4. Diccionario de Nombres
    labels_map = {
        'GDP_per_Capita': 'Economía (Log PIB)',
        'Social_Support': 'Apoyo Social',
        'Healthy_Life_Expectancy': 'Esperanza de Vida',
        'Freedom': 'Libertad',
        'Generosity': 'Generosidad',
        'Corruption_Perception': 'Ausencia de Corrupción',
        'Positive Affect': 'Afecto Positivo',
        'Negative Affect': 'Afecto Negativo',
        'Confidence In National Government': 'Confianza en Gobierno'
    }
    corrs['Etiqueta'] = corrs['Factor'].map(lambda x: labels_map.get(x, x))
    
    # 5. Ordenar por Impacto Absoluto y FILTRAR TOP 5
    corrs['Fuerza'] = corrs['Visual'].abs()
    corrs = corrs.sort_values(by='Fuerza', ascending=True) # Ascendente para que el plot ponga el mejor arriba
    
    # --- FILTRO TOP 5 ---
    corrs_top5 = corrs.tail(5) # Tomamos los 5 últimos (que son los más altos por el sort)
    
    # 6. Graficar
    fig = px.bar(
        corrs_top5, 
        x='Visual', 
        y='Etiqueta', 
        orientation='h',
        title="Top 5 Determinantes de la Felicidad (Mayor Influencia)",
        color='Visual',
        color_continuous_scale='Bluered',
        labels={'Visual': 'Correlación (Impacto)', 'Etiqueta': 'Variable'}
    )
    
    # Línea central
    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="gray")
    
    return fig


def plot_global_correlation(df):
    df_num = df.select_dtypes(include=['number']).drop(columns=['Year'], errors='ignore')
    corr = df_num.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    return fig

def plot_historical_comparison(df, x_col, y_col, chart_type):
    try:
        title = f"{x_col} vs {y_col}"
        if "Scatter" in chart_type:
            fig = px.scatter(df, x=x_col, y=y_col, color="Region", hover_name="Country", opacity=0.6, title=title)
        elif "Box" in chart_type:
            fig = px.box(df, x=x_col, y=y_col, color=x_col, title=title)
        elif "Line" in chart_type:
            df_trend = df.groupby(x_col)[y_col].mean().reset_index()
            fig = px.line(df_trend, x=x_col, y=y_col, markers=True, title=f"Tendencia: {y_col} por {x_col}")
        else: return None
        return fig
    except: return None


def plot_rich_but_lonely(df):
    """
    Gráfica específica para demostrar la paradoja:
    Países ricos pero con bajo apoyo social vs. Países medios con alto apoyo.
    """
    # Filtramos el año más reciente para la "foto actual"
    latest_year = df['Year'].max()
    df_recent = df[df['Year'] == latest_year]
    
    fig = px.scatter(
        df_recent,
        x="GDP_per_Capita",
        y="Happiness_Score",
        color="Social_Support",
        size="Social_Support", # Las burbujas grandes tienen más apoyo social
        hover_name="Country",
        text="Country", # Muestra los nombres
        title=f"La Paradoja: Dinero vs Apoyo Social ({latest_year})",
        labels={
            "GDP_per_Capita": "Riqueza Económica (Log PIB)",
            "Happiness_Score": "Felicidad",
            "Social_Support": "Apoyo Social (Color)"
        },
        color_continuous_scale="Viridis"
    )
    
    # Configuramos para que solo muestre nombres de algunos países clave para no saturar
    # (Ocultamos el texto de la mayoría y solo dejamos los outliers interesantes si quieres)
    fig.update_traces(textposition='top center')
    
    # Líneas promedio para dividir cuadrantes
    avg_gdp = df_recent['GDP_per_Capita'].mean()
    avg_happy = df_recent['Happiness_Score'].mean()
    
    fig.add_vline(x=avg_gdp, line_width=1, line_dash="dash", line_color="red", annotation_text="PIB Promedio")
    fig.add_hline(y=avg_happy, line_width=1, line_dash="dash", line_color="red", annotation_text="Felicidad Promedio")
    
    return fig