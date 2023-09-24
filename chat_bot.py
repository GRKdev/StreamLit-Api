import os
import streamlit as st
import requests
from utils.sidebar_info import display_sidebar_info, display_main_info
from utils.generate_token import create_jwt
from utils.key_check import run_key_check_loop
from utils.chatbot_utils import handle_chat_message, handle_gpt_ft_message, ask_fine_tuned_ada

def chat_bot():
    DOMINIO = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))
    token = create_jwt()

    display_main_info()
    display_sidebar_info() 

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

            if (len(user_input) == 12 or len(user_input) == 13) and user_input.isdigit():
                api_response_url = f"/api/art?bar={user_input}"
            else:
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
                    handle_gpt_ft_message(user_input, message_placeholder, api_response_url, response)