import streamlit as st
import requests
import os
from utils.generate_token import create_jwt
from PIL import Image
import base64
from io import BytesIO


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def logo():
    logo = Image.open("IMG/logo.png")
    st.sidebar.markdown(
        f'<div style="text-align: center"><img src="data:image/png;base64,{image_to_base64(logo)}" style="width:200px;"></div>',
        unsafe_allow_html=True,
    )

def footer():
    logo_grk = Image.open("IMG/grk_logo.png")
    st.sidebar.divider()  
    st.sidebar.markdown(
    f'<h6 style="text-align: center">Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="12">&nbsp by &nbsp<a href="https://github.com/GRKdev/StreamLit-Api"><img src="data:image/png;base64,{image_to_base64(logo_grk)}" alt="GRK" height="16"&nbsp</a></h6>',
    unsafe_allow_html=True)

def clear_chat_history():
    st.session_state.chat_history = []

def display_sidebar_info():
    with st.sidebar.expander("🎯 Ejemplos", False):
        st.markdown("""
        <h4 style='font-size: smaller;'>Clientes</h4>
        <ul style='font-size: smaller;'>
            <li>Dona'm info del client GRK</li>
            <li>telefono Maria Lopez</li>
            <li>tlf de clientes GRK y Pepito</li>
            <li>Toda info cliente John Doe</li>   
            <li> ¿De quién es el tlf 955555555?</li>
            <li> Email de Global Data</li>                 
        </ul>
        
        <h4 style='font-size: smaller;'>Artículos</h4>
        <ul style='font-size: smaller;'>
            <li>info article Apple</li>
            <li>toda info articulo Razer Blackwidow</li>
            <li>Precio Venta articulo MacBook Air</li>
            <li>Info del artículo 1014</li>
            <li>991670248910</li>
        </ul>
        
        <h4 style='font-size: smaller;'>Albaranes</h4>
        <ul style='font-size: smaller;'>
            <li>¿Cual es el albaran 1012?</li>
            <li>Albarán 1014</li>
        </ul>
        
        <h4 style='font-size: smaller;'>Finanzas</h4>
        <ul style='font-size: smaller;'>
            <li>Facturacion de la empresa</li>
            <li>Facturacion total</li>
            <li>Facturacion año 2021</li>
            <li>Ganancias totales</li>
            <li>Facturación cliente Pepito grillo</li>
            <li>ingresos totales cliente Ultra Tech</li>
        </ul>
        
        <h4 style='font-size: smaller;'>Otros</h4>
        <ul style='font-size: smaller;'>
            <li>Quien ha creado el chatbot?</li>
            <li>¿Cómo funciona este chat?</li>
            <li>Los datos son inventados?</li>
        </ul>
        """, unsafe_allow_html=True)
    st.sidebar.button('Borrar Historial', on_click=clear_chat_history)

    footer()

def display_main_info():
    st.info(
        """
        #### **Bienvenido al chatbot de GRK Tech**

        Este chatbot inteligente te permite hacer consultas directas con lenguaje natural a nuestra base de datos de MongoDB.

        Utiliza un modelo de lenguaje Fine-Tuned (Entrenado con ADA) para enviar peticiones url a nuestra API y las respuestas son generadas por el modelo ChatGPT 3.5 Turbo de OpenAI a partir de los resultados obtenidos.
        Si no hay resultados o tenemos un error, el modelo GPT-3.5 FineTuned dará la respuesta.

        ##### ¿Qué puedes hacer?
        - 👤 **Clientes**: Buscar información detallada de clientes, como contacto y facturación.
        - 🛒 **Artículos**: Consultar detalles de artículos, incluyendo precios y stock.
        - 🧾 **Albaranes**: Obtener información sobre albaranes específicos.
        - 📊 **Finanzas**: Para consultas financieras, el sistema envía la petición directamente al servidor y muestra los datos en forma de gráfico, sin pasar por GPT 3.5.

        ⬅️ **Ejemplos de preguntas** que puedes hacer se encuentran en el menú de la izquierda.

        """
    )
    
## Sidebar Stats Page

DOMINIO = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))

def make_authenticated_request(url):
    token = create_jwt()
    headers = {'Authorization': f'Bearer {token}'}
    full_url = DOMINIO + url
    try:
        response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición: {e}")
    return None

def display_sidebar_info_stats():
    with st.sidebar.expander("🔍 Artículos"):
        if st.button("Marca Producto", key='button_marca_producto'):
            data = make_authenticated_request("/api/art_stat?stat=stat_marca")
            if data:
                st.session_state.show_chart.insert(0, ("marca", data))
        
        if st.button("Familia Producto", key='button_familia_producto'):
            data = make_authenticated_request("/api/art_stat?stat=stat_fam")
            if data:
                st.session_state.show_chart.insert(0, ("fam", data))

    with st.sidebar.expander("👥 Clientes"):
        if st.button("Domicili Client", key='button_domicili_client'):
            data = make_authenticated_request("/api/cli_stat?stat=comu")
            if data:
                st.session_state.show_chart.insert(0, ("cli", data))
                
        if st.button("Client barres", key='button_client_barres'):
            data = make_authenticated_request("/api/cli_stat?stat=comu")
            if data:
                st.session_state.show_chart.insert(0, ("cli_barras", data))

    with st.sidebar.expander("💶 Facturación"):
        if st.button("Anuales agrupadas", key='button_ingresos_anuales_group'):
            data = make_authenticated_request("/api/alb_stat?fact_total=true")
            if data:
                st.session_state.show_chart.insert(0, ("total_group_fact", data))

        if st.button("2023", key='button_ingresos_current_year'):
            data = make_authenticated_request("/api/alb_stat?fact_cy=true")
            if data:
                st.session_state.show_chart.insert(0, ("cy", data))
                
        if st.button("2022", key='button_ingresos_selected_year'):
            data = make_authenticated_request("/api/alb_stat?fact_sy=2022")
            if data:
                st.session_state.show_chart.insert(0, ("selectedyear", data))
                
        if st.button("Cliente GRK", key='button_key'):
            data = make_authenticated_request("/api/alb_stat?cli_fact_cy=grk")
            if data:
                st.session_state.show_chart.insert(0, ("facturacio_client", data))

    with st.sidebar.expander("💰 Ingresos"):
        if st.button("Anuales agrupadas", key='button_ganancias_anuales_group'):
            data = make_authenticated_request("/api/alb_stat?ing_total=true")
            if data:
                st.session_state.show_chart.insert(0, ("total_group_ing", data))

        if st.button("2023", key='button_ganacias_current_year'):
            data = make_authenticated_request("/api/alb_stat?ing_cy=true")
            if data:
                st.session_state.show_chart.insert(0, ("ing_cy", data))

        if st.button("2022", key='button_ganacias_selected_year'):
            data = make_authenticated_request("/api/alb_stat?ing_sy=2022")
            if data:
                st.session_state.show_chart.insert(0, ("selectedyear_ing", data))

        if st.button("Cliente GRK", key='button_ing_key'):
            data = make_authenticated_request("/api/alb_stat?cli_ing_cy=grk")
            if data:
                st.session_state.show_chart.insert(0, ("ganancia_client", data))
    footer()