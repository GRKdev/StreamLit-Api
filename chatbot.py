import openai
import os
import streamlit as st
import requests
import re
from key_check import run_key_check_loop
from chatbot_utils import handle_chat_message, ask_gpt

def XatBot():
    DOMINIO = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))
    OPEN_AI_MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL"))
    openai.api_key = st.secrets.get("OPENAI_API_KEY")

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

        match = re.search(r'(api/[^ ?]+)(\?.*)?', api_response)

        if match:
            sanitized_response = match.group(0)
        else:
            sanitized_response = api_response

        print(f"Sanitized Response: {sanitized_response}")

        return sanitized_response

    st.title('XatBot API NOSQL')

    st.info(
        """
        **Bienvenido al chatbot de GRK 👋**

        Puedes hacer preguntas del estilo:
        - ¿Quién es el cliente GRK?
        - Dame el teléfono de John Doe.
        - Dame toda la info del cliente Pepito Grillo.
        - Info del artículo 1009.
        - Cual es el albarán 1014.
        - ¿Cuánto son los ingresos del cliente GRK?
        - Dame los telefonos de los clientes GRK i Pepito
        - Info Articles MacBook Air i Razer Black
        """
    )
            
    with st.sidebar.expander("🧩 Ejemplos", False):
        st.markdown("""
        *Dona'm info del client GRK*
                    
        *info article Apple*
                    
        *telefono de Maria Lopez*
                    
        *¿Cual es el albaran 1012?*
        
        *Cual es el albarán 1014*
                    
        *tlf de clientes GRK y Pepito*
        
        *toda info articulo Razer Blackwidow*

        *Precio Venta articulo MacBook Air*
        
        *Facturacion total*

        *Ganancias totales*

        *Quien ha creado el chatbot?*            
        """)
    st.sidebar.markdown("---")  
    st.sidebar.markdown(
    '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="12">&nbsp by <a href="https://github.com/GRKdev">GRKdev</a></h6>',
    unsafe_allow_html=True,
)
   
    if run_key_check_loop():
        st.session_state.chat_history = st.session_state.get('chat_history', [])
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_input = st.chat_input('Ingresa tu pregunta:')

        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            api_response_url = ask_fine_tuned_ada(user_input)
            full_url = DOMINIO + api_response_url
            response = requests.get(full_url)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()

            if response.status_code == 200:
                data = response.json()
                handle_chat_message(api_response_url, data, message_placeholder, user_input)
            else:
                st.markdown("```⚠ chatbot general```")
                additional_context = {
                    "previous_response": user_input,
                    "fine_tuned_result": api_response_url if 'api/' not in api_response_url else None
                }
                gpt_response = ask_gpt(user_input, message_placeholder, additional_context=additional_context)
                st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
