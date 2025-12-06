# Happiness Analytics Pro 🌍

## Descripción
Plataforma interactiva para el análisis de datos del "World Happiness Report". Permite visualizar la correlación entre variables socioeconómicas y la percepción de felicidad a nivel global.

## Cumplimiento de Requisitos (Rúbrica)

### 1. Manejo de Datos (Pandas)
- Carga de datos robusta con estandarización de columnas (`modules/data_loader.py`).
- Uso de `groupby` para análisis regional y filtros por año (`modules/stats.py`).
- Cálculo de estadísticas descriptivas y correlaciones.

### 2. Visualización Estática (Matplotlib & Seaborn)
- **Dashboard 2x2:** Scatter plots, Histogramas y Boxplots integrados en una sola figura (`modules/visualizations.py`).
- **Heatmap:** Mapa de calor de correlación de Pearson con anotaciones.
- **Personalización:** Uso de paletas de colores ('viridis', 'coolwarm'), títulos, etiquetas de ejes y leyendas modificadas.

### 3. Visualización Avanzada
- **Mapa Interactivo:** Mapa Choropleth mundial generado con Plotly (`modules/advanced_viz.py`).
- **Animación:** Gráfico de dispersión animado a través del tiempo (Year) para observar la evolución de las naciones.

### 4. Estructura Modular
El código está separado en lógica de carga, estadística y visualización para mantener el orden y la escalabilidad.

## Ejecución
1. Instalar requerimientos: `pip install -r requirements.txt`
2. Ejecutar app: `streamlit run app.py`
3. Cargar el dataset `World Happiness Report`.