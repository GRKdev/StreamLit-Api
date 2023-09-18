import openai
import os
import streamlit as st
import requests
import re
from utils.generate_token import create_jwt
from utils.key_check import run_key_check_loop
from utils.chatbot_utils import handle_chat_message, ask_gpt, ask_gpt_ft

def XatBot():
    DOMINIO = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))
    OPEN_AI_MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL"))
    openai.api_key = st.secrets.get("OPENAI_API_KEY")
    token = create_jwt()
    
    def ask_fine_tuned_ada(prompt):
        response = openai.Completion.create(
            engine=OPEN_AI_MODEL,
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop="&&",
            temperature=0,
        )
        api_response = response.choices[0].text.strip()
        api_response = api_response.strip()

        match = re.search(r'(api/[^ ?]+)(\?.*)?', api_response)

        if match:
            sanitized_response = match.group(0)
        else:
            sanitized_response = api_response

        print(f"Sanitized Response: {sanitized_response}")

        return sanitized_response

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


    def clear_chat_history():
        st.session_state.chat_history = []
    st.sidebar.button('Borrar Historial', on_click=clear_chat_history)

    st.sidebar.divider()  
    st.sidebar.markdown(
    '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="12">&nbsp by <a href="https://github.com/GRKdev/StreamLit-Api">GRKdev</a></h6>',
    unsafe_allow_html=True,
)

    if run_key_check_loop():
        st.session_state.chat_history = st.session_state.get('chat_history', [])
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_input = st.chat_input('Ingresa tu pregunta:')
        if user_input:
            user_input = user_input.strip()

        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            api_response_url = ask_fine_tuned_ada(user_input)


            if 'api/' in api_response_url:
                full_url = DOMINIO + api_response_url
                print(full_url)
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(full_url, headers=headers)
                print(response)
            else:
                response = None

            with st.chat_message("assistant"):
                message_placeholder = st.empty()

                if response and response.status_code == 200:
                    data = response.json()
                    handle_chat_message(api_response_url, data, message_placeholder, user_input)
                else:
                    st.markdown("<span style='color:red; font-style:italic; font-size:small;'>⚠ chatbot general</span>", unsafe_allow_html=True)
                    
                    additional_context = {
                        "previous_response": user_input,
                        "fine_tuned_result": api_response_url if 'api/' not in api_response_url else None,
                        "api_error": response.json() if 'api/' in api_response_url else None,
                    }

                    print(additional_context)
                    gpt_response = ask_gpt_ft(user_input, message_placeholder, additional_context=additional_context)
                    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})

