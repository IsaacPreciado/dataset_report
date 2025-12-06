import streamlit as st
import pandas as pd
import plotly.express as px
from modules import data_loader, stats, visualizations, advanced_viz

# Configuración de página profesional
st.set_page_config(
    page_title="Informe de Felicidad Global", 
    layout="wide", 
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# --- CARGA DE DATOS ---
with st.spinner('Procesando dataset histórico (2005-2022)...'):
    df = data_loader.load_local_data()

if df is not None:
    
    # --- SIDEBAR DE NAVEGACIÓN ---
    with st.sidebar:
        st.header("📑 Estructura del Informe")
        section = st.radio(
            "Navegación:",
            ["1. Introducción y Contexto",
             "2. Metodología y Exploración",
             "3. Resultados y Hallazgos"]
        )
        st.markdown("---")
        st.markdown("### ⚙️ Ficha Técnica")
        st.info(f"**Fuente:** World Happiness Report")
        st.info(f"**Periodo:** {df['Year'].min()} - {df['Year'].max()}")
        st.info(f"**Países:** {df['Country'].nunique()}")

    # =========================================================================
    # SECCIÓN 1: INTRODUCCIÓN
    # =========================================================================
    if section == "1. Introducción y Contexto":
        
        st.title("🌍 Reporte sobre la felicidad global (2005-2022)")
        st.markdown("#### Reporte sobre los determinantes socioeconómicos y psicológicos de la felicidad humana en el mundo.")
        st.divider()

        # 1.1 PROPOSITO
        st.subheader("1.1. Alcance del Proyecto")
        st.markdown("""
        Este reporte presenta un análisis de los datos históricos del **World Happiness Report (WHR)**. 
        A diferencia de los reportes económicos tradicionales que solo miden el PIB, este estudio integra variables psicológicas (afecto positivo/negativo) y sociales (confianza, libertad) para construir una imagen holística del bienestar.
        
        **Objetivos Específicos:**
        * Evaluar la correlación histórica entre riqueza material y satisfacción de vida.
        * Analizar el impacto de los factores que envuelven a una sociedad y las emociones diarias en el puntaje final.
        """)
        
        # KPI Rápido
        avg_score_hist = df['Happiness_Score'].mean()
        historic_leader = df.groupby('Country')['Happiness_Score'].mean().idxmax()
        st.info(f"💡 **Dato Global:** El promedio histórico de felicidad en el mundo es de **{avg_score_hist:.2f} / 10**. El líder histórico consistente es **{historic_leader}**.")

        st.divider()

        # 1.2 DICCIONARIO DE VARIABLES (COMPLETO)
        st.subheader("1.2. Diccionario de Variables y Estadísticas Descriptivas")
        
        def get_stat_range(column):
            if column in df.columns:
                low = df[column].quantile(0.05)
                high = df[column].quantile(0.95)
                return f"{low:.2f} - {high:.2f}"
            return "N/A"

        # TABLA PROFESIONAL COMPLETA
        st.markdown(f"""
        | Categoría | Variable | Definición Técnica | Rango Típico (p5-p95) |
        | :--- | :--- | :--- | :--- |
        | **Objetivo** | **Happiness Score** | Promedio de la "Escalera de Cantril" (0=Peor vida posible, 10=Mejor vida posible). | **{get_stat_range('Happiness_Score')}** |
        | **Económico** | **GDP per Capita** | Logaritmo Natural del PIB per cápita ajustado por paridad de poder adquisitivo (PPA) en dólares internacionales de 2017. | **{get_stat_range('GDP_per_Capita')}** |
        | **Social** | **Social Support** | Promedio nacional de la respuesta binaria (0/1) a: *"¿Tiene familiares o amigos con quienes contar en momentos de necesidad?"* | **{get_stat_range('Social_Support')}** |
        | **Salud** | **Healthy Life Exp.** | Esperanza de vida saludable al nacer (HALE) basada en datos de la OMS. | **{get_stat_range('Healthy_Life_Expectancy')}** |
        | **Libertad** | **Freedom** | Promedio nacional de satisfacción con la libertad para elegir qué hacer con su vida. | **{get_stat_range('Freedom')}** |
        | **Ética** | **Generosity** | Residuo de regredir el promedio de "donaciones a caridad" sobre el PIB per cápita. | **{get_stat_range('Generosity')}** |
        | **Institucional** | **Corruption** | Promedio de percepción de corrupción en el gobierno y los negocios (0=Baja, 1=Alta). | **{get_stat_range('Corruption_Perception')}** |
        | **Institucional** | **Confidence in Gov** | Promedio de respuesta a: *"¿Tiene confianza en el gobierno nacional?"*. | **{get_stat_range('Confidence_in_Gov')}** |
        | **Emocional** | **Positive Affect** | Promedio de medidas de afecto positivo del día anterior (risa, disfrute, interés). | **{get_stat_range('Positive_Affect')}** |
        | **Emocional** | **Negative Affect** | Promedio de medidas de afecto negativo del día anterior (preocupación, tristeza, ira). | **{get_stat_range('Negative_Affect')}** |
        """)

        st.divider()

    # =========================================================================
    # SECCIÓN 2: METODOLOGÍA
    # =========================================================================
    elif section == "2. Metodología y Exploración":
        st.title("🔬 Metodología y Análisis Exploratorio (EDA)")
        
        st.subheader("2.1. Ingesta y Limpieza")
        st.markdown(f"El dataset consolidado abarca **{df['Year'].nunique()} años** de historia global.")
        st.dataframe(df.describe().style.format("{:.2f}"))

        st.subheader("2.2. Análisis de Correlación Multivariable")
        
        col_heat, col_text = st.columns([2, 1])
        with col_heat:
            fig_corr = visualizations.plot_global_correlation(df)
            st.pyplot(fig_corr)
        with col_text:
            st.info("""
            **Interpretación:**
            * **Correlación Fuerte:** GDP, Apoyo Social y Salud.
            * **Correlación Inversa:** Corrupción vs Felicidad.
            """)
            
        st.divider()
        st.subheader("2.3. Distribución Univariada por Variable")
        fig_dist = visualizations.plot_distributions_grid(df)
        st.pyplot(fig_dist)

        st.divider()
        st.subheader("2.4. Relaciones Bivariadas")
        fig_bivar = visualizations.plot_global_factors_6(df)
        st.pyplot(fig_bivar)

    # =========================================================================
    # SECCIÓN 3: RESULTADOS
    # =========================================================================
    elif section == "3. Resultados y Hallazgos":
        st.title("📊 Resultados y Conclusiones del Estudio")

        # 1. RANKING DINÁMICO
        st.header("1. Dinámica de Liderazgo Global")
        st.markdown("Comparativa de los líderes mundiales en bienestar.")
        
        years_list = sorted(df['Year'].unique())
        options = ["Promedio Histórico (Todos los Años)"] + list(years_list)
        sel_period = st.selectbox("Seleccionar Periodo de Análisis:", options, index=len(options)-1)
        
        if isinstance(sel_period, str) and "Todos" in sel_period:
            st.info("💡 Mostrando el ranking basado en el **promedio de felicidad acumulado**.")
            df_avg = df.groupby('Country')['Happiness_Score'].mean().reset_index()
            top10 = df_avg.nlargest(10, 'Happiness_Score')
            bottom10 = df_avg.nsmallest(10, 'Happiness_Score')
            top10.index = range(1, 11)
            bottom10.index = range(1, 11)
            current_map = advanced_viz.plot_global_average_map(df)
        else:
            st.success(f"📅 Visualizando datos del año **{sel_period}**.")
            top10, bottom10 = stats.get_top_bottom_countries(df, sel_period, n=10)
            current_map = advanced_viz.plot_world_map(df, sel_period)

        c1, c2 = st.columns(2)
        with c1: 
            st.subheader("🏆 Mejores 10")
            st.table(top10[['Country', 'Happiness_Score']].style.format({"Happiness_Score": "{:.2f}"}))
        with c2: 
            st.subheader("⚠️ Peores 10")
            st.table(bottom10[['Country', 'Happiness_Score']].style.format({"Happiness_Score": "{:.2f}"}))
        

        st.subheader("Distribución Geográfica del Periodo")
        if current_map: st.plotly_chart(current_map, use_container_width=True)

        # 2. DETERMINANTES
        st.divider()
        st.header("2. Determinantes Clave del Bienestar")
        fig_imp = visualizations.plot_variable_importance(df)
        st.plotly_chart(fig_imp, use_container_width=True)


        # 4. EVOLUCIÓN
        st.divider()
        st.header("4. Estudio Longitudinal Detallado")
        st.markdown("""
        Analiza la trayectoria individual de un país y observa cómo cambian sus variables clave año con año.
        """)
        
        # A. CONTROLES (Arriba)
        col_sel, col_time = st.columns([1, 2])
        
        with col_sel:
            all_c = sorted(df['Country'].unique())
            # Default: México si existe, si no el primero
            idx_def = all_c.index("Mexico") if "Mexico" in all_c else 0
            # CAMBIO: Selectbox para 1 solo país
            selected_country = st.selectbox("1. Selecciona País:", all_c, index=idx_def)
            
        with col_time:
            min_year = int(df['Year'].min())
            max_year = int(df['Year'].max())
            current_year = st.slider("2. Línea de Tiempo:", min_value=min_year, max_value=max_year, value=max_year)

        # B. VISUALIZACIÓN (Horizontal: Gráfica Izq | Tabla Der)
        col_graph, col_table = st.columns([2, 1]) # Proporción 2:1 para que la gráfica sea más ancha
        
        # Pasamos el país como lista [selected_country] porque las funciones esperan lista
        country_list = [selected_country]
        
        with col_graph:
            # Gráfica
            fig_snap = advanced_viz.plot_year_snapshot(df, country_list, current_year)
            if fig_snap:
                st.plotly_chart(fig_snap, use_container_width=True)
            else:
                st.warning("No hay datos gráficos disponibles.")

        with col_table:
            # Tabla de Datos Específicos
            st.subheader(f"📊 Datos {current_year}")
            
            cols_table = ['Social_Support', 'Healthy_Life_Expectancy', 'Freedom', "Positive_Affect"]
            
            # Filtramos dato exacto
            row_data = df[(df['Country'] == selected_country) & (df['Year'] == current_year)]
            
            if not row_data.empty:
                # Transponemos para que sea vertical (Mejor lectura en columna lateral)
                data_t = row_data[cols_table].T
                data_t.columns = ["Valor"]
                
                # Renombramos índice
                data_t.index = ['Apoyo Social', 'Salud (Años)', 'Libertad', 'Índice de Positividad']
                
                # Mostramos tabla limpia
                st.table(data_t.style.format("{:.2f}"))
                
                # Semáforo simple (Comparación con promedio global de ese año)
                avg_happy_yr = df[df['Year'] == current_year]['Happiness_Score'].mean()
                val_happy = row_data['Happiness_Score'].values[0]
                
            else:
                st.info(f"Sin datos para {selected_country} en {current_year}.")

        st.info("**Conclusión Final:** Al observar la historia individual, notamos que las caídas en felicidad no solamente se basan en el dinero, sino en muchísimos factores externos, sociales, culturas y que probablemente desconozcamos y sean imposibles de medir con exactitud.")

else:
    st.error("⚠️ Error crítico: Archivo 'World Happiness Report.csv' no encontrado en /data.")