import plotly.express as px
import pandas as pd
import streamlit as st

def plot_world_map(df, year):
    """Mapa de un año específico."""
    df_year = df[df['Year'] == year]
    if df_year.empty: return None
    
    fig = px.choropleth(
        df_year, locations="Country", locationmode="country names",
        color="Happiness_Score", hover_name="Country",
        color_continuous_scale="Viridis", title=f"Mapa Mundial ({year})",
        range_color=[2, 8]
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, geo=dict(showframe=False))
    return fig

def plot_global_average_map(df):
    """Mapa del promedio histórico."""
    df_avg = df.groupby('Country')['Happiness_Score'].mean().reset_index()
    
    fig = px.choropleth(
        df_avg, locations="Country", locationmode="country names",
        color="Happiness_Score", hover_name="Country",
        color_continuous_scale="Viridis", title="Mapa Promedio Histórico (2005-2022)",
        range_color=[2, 8]
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, geo=dict(showframe=False))
    return fig

def plot_multi_country_line(df, countries, y_col):
    """Gráfica de líneas para evolución."""
    mask = df['Country'].isin(countries)
    df_filtered = df[mask].sort_values('Year')
    if df_filtered.empty: return None
    
    fig = px.line(
        df_filtered, x="Year", y=y_col, color="Country", markers=True,
        title=f"Evolución Histórica: {y_col}", template="plotly_white"
    )
    fig.update_traces(line=dict(width=3))
    return fig

def plot_filtered_animation(df, selected_countries):
    """
    Animación robusta: Rellena huecos (interpolación) para que las burbujas no desaparezcan.
    """
    # 1. Filtramos países seleccionados
    mask = df['Country'].isin(selected_countries)
    df_filtered = df[mask].copy()
    
    if df_filtered.empty: return None

    # 2. PROCESO DE RELLENO DE HUECOS (INTERPOLACIÓN)
    # Creamos una cuadrícula completa de Años x Países
    years = sorted(df['Year'].unique())
    full_index = pd.MultiIndex.from_product([selected_countries, years], names=['Country', 'Year'])
    
    # Reindexamos para forzar que existan todas las filas
    df_filtered = df_filtered.set_index(['Country', 'Year']).reindex(full_index).reset_index()
    
    # Rellenar metadatos fijos (Region) que se pierden al reindexar
    # Hacemos un diccionario país -> región
    country_regions = df.groupby('Country')['Region'].first().to_dict()
    df_filtered['Region'] = df_filtered['Country'].map(country_regions)
    
    # Interpolamos los valores numéricos por grupo (País)
    # Esto llena los huecos (NaN) con el promedio de sus vecinos
    numeric_cols = ['Happiness_Score', 'GDP_per_Capita', 'Social_Support']
    df_filtered[numeric_cols] = df_filtered.groupby('Country')[numeric_cols].transform(lambda x: x.interpolate(method='linear', limit_direction='both'))
    
    # Limpiamos remanentes (si un país no tiene datos del todo, lo tiramos)
    df_filtered = df_filtered.dropna(subset=['Happiness_Score'])
    
    # 3. Calcular rangos globales fijos
    min_x = df['GDP_per_Capita'].min() * 0.95
    max_x = df['GDP_per_Capita'].max() * 1.05
    min_y = df['Happiness_Score'].min() * 0.95
    max_y = df['Happiness_Score'].max() * 1.05

    # 4. Crear Animación
    fig = px.scatter(
        df_filtered.sort_values('Year'),
        x="GDP_per_Capita",
        y="Happiness_Score",
        animation_frame="Year",
        animation_group="Country",
        size="Social_Support", 
        color="Country",
        hover_name="Country",
        range_x=[min_x, max_x],
        range_y=[min_y, max_y],
        title="Carrera de la Felicidad (Datos Interpolados)",
        labels={"GDP_per_Capita": "Economía (Log PIB)", "Happiness_Score": "Felicidad", "Social_Support": "Apoyo Social"}
    )
    
    # Configuración estética
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    # Hacemos que la animación sea un poco más lenta para apreciarla
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700 
    
    return fig


def plot_year_snapshot(df, selected_countries, current_year):
    """
    Muestra la posición de los países en un año específico (Controlado por Slider).
    Dibuja un 'rastro' gris para ver la historia.
    """
    # 1. Datos históricos (Rastro)
    mask_hist = (df['Country'].isin(selected_countries)) & (df['Year'] <= current_year)
    df_hist = df[mask_hist].sort_values('Year')
    
    # 2. Datos actuales (Punto grande)
    df_current = df_hist[df_hist['Year'] == current_year]
    
    if df_hist.empty: return None

    # Creamos la gráfica base con el rastro (línea gris)
    fig = px.line(
        df_hist, 
        x="GDP_per_Capita", 
        y="Happiness_Score", 
        color="Country",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title=f"Trayectoria hasta {current_year}",
        labels={"GDP_per_Capita": "Economía (Log PIB)", "Happiness_Score": "Felicidad"}
    )
    
    # Hacemos las líneas delgadas y grises (historia)
    fig.update_traces(line=dict(color="lightgrey", width=1), showlegend=False)
    
    # Añadimos los puntos del año actual (Burbujas grandes)
    if not df_current.empty:
        fig.add_scatter(
            x=df_current['GDP_per_Capita'],
            y=df_current['Happiness_Score'],
            mode='markers+text',
            text=df_current['Country'],
            textposition='top center',
            marker=dict(size=20, color=df_current['Social_Support'], colorscale='Viridis', showscale=True),
            name=f"Año {current_year}",
            customdata=df_current[['Country', 'Social_Support', 'Freedom']] # Datos extra para tooltip
        )
        
        # Ajustamos tooltip
        fig.update_traces(
            hovertemplate="<b>%{text}</b><br>PIB: %{x:.2f}<br>Felicidad: %{y:.2f}<br>Apoyo Social: %{marker.color:.2f}"
        )

    # Fijar rangos para que no salte la cámara
    fig.update_layout(
        xaxis_range=[df['GDP_per_Capita'].min()*0.95, df['GDP_per_Capita'].max()*1.05],
        yaxis_range=[df['Happiness_Score'].min()*0.95, df['Happiness_Score'].max()*1.05],
        showlegend=False
    )
    
    return fig