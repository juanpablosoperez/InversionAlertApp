import streamlit as st
import pandas as pd

def run_app():
    # Configuración de la página
    st.set_page_config(
        page_title="Inversion Alert",
        layout="wide"
    )
    
    # --- CSS Personalizado ---
    st.markdown("""
        <style>
        /* Ajustes generales */
        html, body, [class*="st"] {
            font-family: Arial, sans-serif;
            background-color: #FFFFFF;
            color: black;
        }
        
        /* Contenedor de métricas */
        .metrics-container {
            display: flex;
            gap: 2rem;
            align-items: center;
            font-size: 0.9rem;
            color: black;
            margin-bottom: 1rem;
        }
        .metric-box {
            text-align: center;
        }
        .metric-value {
            font-size: 1.2rem;
            font-weight: 600;
            color: black;
        }
        
        /* Tarjetas */
        .card {
            background-color: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
            border: 1px solid #E9ECEF;
            text-align: center;
            color: black;
        }
        .card h3 {
            margin: 0;
            font-size: 1.2rem;
            font-weight: 600;
        }
        .badge {
            display: inline-block;
            padding: 0.25em 0.6em;
            font-size: 0.85rem;
            font-weight: 600;
            border-radius: 0.25rem;
            margin-bottom: 0.5rem;
        }
        .badge-green {
            background-color: #E6F4EA;
            color: #34A853;
        }
        .badge-red {
            background-color: #FCE8E6;
            color: #EA4335;
        }
        .price {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        .details-btn {
            font-size: 0.9rem;
            padding: 0.4rem 0.8rem;
            background-color: #f8f9fa;
            color: black;
            border: 1px solid #ced4da;
            border-radius: 0.25rem;
            cursor: pointer;
            text-decoration: none;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # --- Encabezado y Métricas ---
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("### Inversion Alert")
    with col2:
        st.markdown("<div class='metrics-container'>" +
                    "<div class='metric-box'><p>Inversiones monitoreadas</p><p class='metric-value'>3</p></div>" +
                    "<div class='metric-box'><p>Alcanzaron objetivo</p><p class='metric-value'>0</p></div>" +
                    "</div>", unsafe_allow_html=True)
    with col3:
        st.button("+ Agregar Inversión")
    
    # --- Barra de búsqueda y filtros ---
    col_search, col_sort = st.columns([3, 1])
    with col_search:
        st.text_input("Buscar por ticker...")
    with col_sort:
        st.selectbox("Ordenar por", ["Ticker [A->Z]", "Precio Actual", "Precio Objetivo"])
    
    # --- Datos de Ejemplo ---
    acciones_data = [
        {"ticker": "AAPL", "pct": "1.23%", "pct_class": "badge-green", "precio_actual": "$185.92", "precio_objetivo": "$200", "distancia": "-7.04%", "ultima_actualizacion": "Hace 3 min"},
        {"ticker": "GOOGL", "pct": "0.78%", "pct_class": "badge-green", "precio_actual": "$142.89", "precio_objetivo": "$150", "distancia": "-4.74%", "ultima_actualizacion": "Hace 12 min"},
        {"ticker": "MELI", "pct": "-0.45%", "pct_class": "badge-red", "precio_actual": "$1456.78", "precio_objetivo": "$1500", "distancia": "-2.88%", "ultima_actualizacion": "Hace 3 min"}
    ]
    
    # --- Tarjetas ---
    cols = st.columns(len(acciones_data))
    for i, accion in enumerate(acciones_data):
        with cols[i]:
            st.markdown(f"""
                <div class='card'>
                    <h3>{accion['ticker']} <span class='badge {accion['pct_class']}'>{accion['pct']}</span></h3>
                    <p class='price'>{accion['precio_actual']}</p>
                    <p>Precio objetivo: {accion['precio_objetivo']}</p>
                    <p>Distancia al objetivo: {accion['distancia']}</p>
                    <p>Última actualización: {accion['ultima_actualizacion']}</p>
                    <button class='details-btn'>Ver detalles</button>
                </div>
            """, unsafe_allow_html=True)

def main():
    run_app()

if __name__ == "__main__":
    main()
