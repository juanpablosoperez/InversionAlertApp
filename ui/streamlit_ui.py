import streamlit as st
import pandas as pd


def run_app():
    # Configuración de la página
    st.set_page_config(
        page_title="Inversion Alert",
        layout="wide"
    )

    # Estado para el modal
    if 'show_modal' not in st.session_state:
        st.session_state.show_modal = False

    def open_modal():
        st.session_state.show_modal = True

    def close_modal():
        st.session_state.show_modal = False
    
    # --- CSS Personalizado ---
    st.markdown("""
        <style>
        /* Ajustes generales */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body, [class*="st"] {
            font-family: 'Poppins', sans-serif;
            background-color: #FFFFFF;
            color: black;
        }
        
        /* Contenedor de métricas */
        .metrics-container {
            display: flex;
            gap: 2rem;
            align-items: center;
            font-size: 1rem;
            color: black;
            margin-bottom: 1rem;
        }
        .metric-box {
            text-align: center;
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: black;
        }
        
        /* Tarjetas */
        .card {
            background-color: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            border: 1px solid #E9ECEF;
            text-align: center;
            color: black;
        }
        .card h3 {
            margin: 0;
            font-size: 1.4rem;
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
            font-size: 1.7rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        .details-btn {
            font-size: 1rem;
            padding: 0.6rem 1.2rem;
            background-color: #34A853;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
        }
        .details-btn:hover {
            background-color: #2C7A45;
        }
        .add-investment-btn {
            background-color: #0D6EFD;
            color: white;
            padding: 0.6rem 1.5rem;
            font-size: 1rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
        }
        .add-investment-btn:hover {
            background-color: #0B5ED7;
        }
        .modal-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.4);
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background: white;  /* Asegura que el fondo sea blanco */
            padding: 20px;
            border-radius: 10px;
            width: 400px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        }
        /* Corrección del color de los campos de entrada */
        input, select {
            background-color: white !important;
            color: black !important;
            border: 1px solid #ccc !important;
            padding: 8px;
            width: 100%;
            border-radius: 5px;
        }
        .modal-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
        }
        .modal-buttons button {
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
        }
        .cancel-btn {
            background-color: #ccc;
            color: black;
        }
        .add-btn {
            background-color: #34A853;
            color: white;
        }
                
        .details-btn, .add-investment-btn {
            font-size: 1rem;
            padding: 10px 20px;
            background-color: #34A853;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: background 0.3s ease;
            display: inline-block;
            text-align: center;
        }
        .details-btn:hover, .add-investment-btn:hover {
            background-color: #2C7A45;
        }
        .styled-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 1rem;
            font-weight: 600;
            color: white;
            background-color: #34A853;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            transition: background 0.3s ease;
        }
        .styled-button:hover {
            background-color: #2C7A45;
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
        button = st.button("+ Agregar Inversión", key="open_modal")
        st.markdown("""
            <script>
            var elements = window.parent.document.querySelectorAll('button[data-testid="stButton"]');
            elements.forEach(el => {
                el.classList.add('styled-button');
            });
            </script>
        """, unsafe_allow_html=True)
        if button:
            open_modal()




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

    # --- Modal para agregar inversión ---
    if st.session_state.show_modal:
        st.markdown("""
            <div class='modal-container'>
                <div class='modal-content'>
                    <h3>Agregar Nueva Inversión</h3>
                    <label>Ticker</label>
                    <input type='text' placeholder='Ej: AAPL'>
                    <label>Precio Objetivo</label>
                    <input type='number' placeholder='0.00'>
                    <label>Frecuencia de Revisión</label>
                    <select>
                        <option>Seleccionar frecuencia</option>
                        <option>1 min</option>
                        <option>5 min</option>
                        <option>15 min</option>
                    </select>
                    <div class='modal-buttons'>
                        <button class='cancel-btn' onclick="window.location.reload();">Cancelar</button>
                        <button class='add-btn' onclick="window.location.reload();">Agregar</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def main():
    run_app()

if __name__ == "__main__":
    main()
