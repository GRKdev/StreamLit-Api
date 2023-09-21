import streamlit as st
import openai

def run_key_check_loop():
    iteration = 0
    while True:
        api_key_status = check_for_openai_key(iteration)
        iteration += 1

        if api_key_status == "provided":
            try:
                openai.api_key = st.session_state.api_key
                openai.Completion.create(engine="text-davinci-003", prompt="test", max_tokens=5)
                with st.chat_message("Assistant"):
                    st.write("¡Empezemos a chatear!")
                return True
            except openai.error.AuthenticationError:
                with st.chat_message("Assistant"):
                    st.warning('Porfavor introduce una clave válida de OpenAI!', icon='⚠')
                del st.session_state.api_key
        else:
            continue

def check_for_openai_key(iteration):
    key = f"key_{iteration}"
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''

    if st.session_state.api_key and len(st.session_state.api_key) > 10:
        return "provided"
    
    with st.chat_message("Assistant"):
        mp = st.empty()
        sl = mp.container()
        sl.write(
            """Hola, es fantástico que quieras chatear conmigo. Sin embargo, necesito tu clave API de OpenAI para funcionar.
            Si no tienes una clave, puedes registrarte y crear una aquí https://platform.openai.com/account/api-keys.
            No te preocupes, tu clave no se almacenará de ninguna forma, excepto durante tu sesión actual.
            """
        )
        openai_api_key = sl.text_input('🔑 OpenAI API Key', type='password', key=key)

        if openai_api_key:
            st.session_state.api_key = openai_api_key
            return "provided"
    st.stop()
    return "invalid"