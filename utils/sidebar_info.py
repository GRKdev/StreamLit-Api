import streamlit as st

def clear_chat_history():
    st.session_state.chat_history = []

def display_sidebar_info():
    with st.sidebar.expander("🎯 Ejemplos", False):
        st.markdown("""
        <h4 style='font-size: smaller;'>Clientes</h4>
        <ul style='font-size: smaller;'>
            <li>Dona'm info del client GRK</li>
            <li>telefono de Maria Lopez</li>
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
        </ul>
        
        <h4 style='font-size: smaller;'>Albaranes</h4>
        <ul style='font-size: smaller;'>
            <li>¿Cual es el albaran 1012?</li>
            <li>Albarán 1014</li>
        </ul>
        
        <h4 style='font-size: smaller;'>Finanzas</h4>
        <ul style='font-size: smaller;'>
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
    st.sidebar.divider()  
    st.sidebar.markdown(
    '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="12">&nbsp by <a href="https://github.com/GRKdev/StreamLit-Api">GRKdev</a></h6>',
    unsafe_allow_html=True)
    

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