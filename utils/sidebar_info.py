import streamlit as st
import requests
import os
from utils.generate_token import TokenManager
from PIL import Image
import base64
from io import BytesIO

token_manager = TokenManager()


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
    st.session_state.last_assistant_response = ""



import streamlit as st

def display_sidebar_info():

    option = st.sidebar.selectbox(
        ' ',
        ('Ejemplos','Clientes', 'Artículos', 'Albaranes', 'Finanzas', 'Otros')
    )

    if option == 'Clientes':
        lines = [
            "Dona'm info del client GRK",
            "telefono Maria Lopez",
            "tlf de clientes GRK y Pepito",
            "Toda info cliente John Doe",
            "¿De quién es el tlf 955555555?",
            "Email de Global Data",
            "Quién es el cliente Pedro Muñoz?",
            "Dame emails de GRK y de i-and",
            "¿Cómo puedo contactar con Ana Belen?",
            "Adreça de Andorra Telecom",
            "El teléfono 941123456 ¿De quién es?",
            "info de clientes Telecom y Ultra Tech"
        ]

        for line in lines:
            st.sidebar.markdown(f"```markdown\n{line}\n```")

    elif option == 'Artículos':
        lineas = [
            "info article Apple",
            "toda info articulo Razer Blackwidow",
            "Precio Venta articulo MacBook Air",
            "Info del artículo 1014",
            "991670248910",
            "art 2021",
            "Dame precio de compra de RTX 3080",
            "quiero toda la info del art 2023",
            "Tot info art 2017, en format llista",
            "Información completa artículo 2024",
            "Stock article Sony WH-1000XM4",
            "Dame la descripcion del articulo airpods"
        ]
        
        for line in lineas:
            st.sidebar.markdown(f"```markdown\n{line}\n```")


    elif option == 'Albaranes':
        lineas = [
            "¿Cuál es el albaran 1012?",
            "Albarán 1014",
            "Albara 1005, quin es el marge",
            "¿Puedo ver el albarán 2023?",
            "ver albaràn 2050",
            "Albaràn 1021, de que cliente es?",
            "Alb 1022 ¿Está facturado?",
            "Albarà 1023, dona'm el nº del pedido"
        ]
        
        for line in lineas:
            st.sidebar.markdown(f"```markdown\n{line}\n```")


    elif option == 'Finanzas':
        lineas = [
            "Facturacion de la empresa",
            "Facturación actual / facturación",
            "Facturacion total / fact total",
            "¿Cuál es la facturación en los últimos años?",
            "Facturacion año 2021",
            "¿Cuánto facturamos en 2022?",
            "Ganancias de la empresa",
            "¿Cuál es nuestra rentabilidad anual hasta la fecha?",
            "Ganancias totales",
            "¿Cuánto hemos ingresado en 2022?",
            "Facturación cliente Pepito grillo",
            "ingresos totales cliente Ultra Tech"
        ]

        for line in lineas:
            st.sidebar.markdown(f"```markdown\n{line}\n```")

    elif option == 'Otros':
        lineas = [
            "¿Qué es iand.dev?",
            "Quien ha creado el chatbot?",
            "¿Cómo funciona este chat?",
            "Los datos son inventados?",
            "¿Cómo te conectas a la DB?",
            "Hi ha algun tipus de revisió humana?",
            "Sobre qué puedo preguntarte?",
            "Quién está detrás de tu desarrollo?",
            "¿Cómo puedo reportar un error?",
            "¡Eres terrible!"
        ]

        for line in lineas:
            st.sidebar.markdown(f"```markdown\n{line}\n```")

    st.sidebar.button('Borrar Historial', on_click=clear_chat_history)

    footer()

def display_main_info():
    st.info(
        """
        #### **Bienvenido al chatbot de IAND**

        Este chatbot inteligente te permite hacer consultas directas con lenguaje natural a nuestra base de datos de MongoDB.

        Utilizamos un modelo de lenguaje afinado entrenado con Babbage-002, para gestionar las solicitudes URL hacia nuestra API que se integra con la base de datos. 
        Las respuestas son generadas por el modelo ChatGPT 3.5 Turbo de OpenAI, basadas en los datos recuperados. En caso de ausencia de resultados, errores o preguntas genéricas, un modelo 
        GPT-3.5 Fine-Tuned se encargará de proporcionar la respuesta adecuada.
        
        Datos de los entrenamientos: Nombres ficticios de clientes y nombres de empresas públicas reales. Los datos de los artículos son reales, del mundo de la tecnología.
        
        Datos en la MongoDB: Aunque la mayoría son ficticios, son completamente auténticos en su estructura. Adicionalmente, se han incorporado datos públicos relacionados con
        empresas tecnológicas de Andorra para enriquecer la información disponible.

        ##### ¿Qué puedes hacer?
        - 👤 **Clientes**: Buscar información detallada de clientes.
        - 🛒 **Artículos**: Consultar detalles de artículos, incluyendo precios y stock.
        - 🧾 **Albaranes**: Obtener información sobre albaranes específicos.
        - 📊 **Finanzas**: Consultas de facturación e ingresos de la empresa y cliente, este resultado se realiza sin pasar por GPT-3.5, directo de la API.

        ⬅️ **Ejemplos de preguntas** que puedes hacer se encuentran en el menú de la izquierda.

        Necesitarás una clave de acceso o tu clave API de OpenAI para funcionar.
        Si no tienes una clave, puedes registrarte y crear una aquí https://platform.openai.com/account/api-keys.
        No te preocupes, tu clave no se almacenará de ninguna forma en nuestros servidores, únicamente en tu sesión actual del navegador. 
        """
    )
    
    
## Sidebar Stats Page

DOMINIO = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))

def make_authenticated_request(url):
    token = token_manager.get_token()
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