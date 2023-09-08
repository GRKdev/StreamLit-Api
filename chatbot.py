import openai
import os
import streamlit as st
import requests
import re
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader
from chart_utils import render_pie_chart_marca, render_pie_chart_fam

last_assistant_response = None

def XatBot():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''

    DOMINIO = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))
    OPEN_AI_MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL"))

    def ask_gpt(prompt, placeholder, additional_context=None):
        global last_assistant_response
        messages_list = [
            {"role": "system", "content": "Ets un assistent de la empresa GRK que respon sempre en estil MarkDown, mostra les dades relevants en Negrita. No expliquis com realitzar calculs, dona la resposta directament. Rebràs pregunta de l'usuari juntament amb dades obtingudes d'una base de dades. Has d'utilitzar ambdós per proporcionar una resposta coherent, clara i útil. Assegura't d'estructurar la informació de manera amigable i fàcil de comprendre per a l'usuari, el nom de client, article o albarà al principi. Si el json conté múltiples elements, sintetitza la informació de manera concisa. Quan tractis amb números monetaris, afegeix el simbol €."},
            {"role": "user", "content": ""},
            {"role": "assistant", "content": ""},
        ]
        if last_assistant_response:
            messages_list.append({"role": "assistant", "content": last_assistant_response})

        if additional_context:
            messages_list.append({"role": "user", "content": additional_context})

        messages_list.append({"role": "user", "content": prompt})
        full_response = ""
        
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_list,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.2,
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        
        last_assistant_response = full_response.strip()
        return last_assistant_response

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
            sanitized_response = ""

        print(f"Sanitized Response: {sanitized_response}")

        return sanitized_response

    def generate_response_from_mongo_results(data):
        print(f"data: {data}") 
        if not data:
            return "No se encontraron resultados."
        else:
            return str(data)
    
    st.title('XatBot API NOSQL')

    if st.session_state.api_key:
        openai_api_key = st.session_state.api_key 
    else:
        openai_api_key = st.sidebar.text_input('🔑 OpenAI API Key', type='password')

        if openai_api_key:
            st.session_state.api_key = openai_api_key
            
    with st.sidebar.expander("🧩 Exemples", False):
        st.markdown("""
        *Dona'm info del client GRK*
                    
        *info article Apple*
                    
        *telefono de Maria Lopez*
                    
        *¿Cual es el albaran 1012?*
                    
        """)
    st.sidebar.markdown("---")  
    st.sidebar.markdown(
    '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://github.com/GRKdev">GRKdev</a></h6>',
    unsafe_allow_html=True,
)
    st.sidebar.write(
            """
            [![GitHub][github_badge]][github_link]

            [github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
            [github_link]: https://github.com/GRKdev/StreamLit-Api
            """
            )
        
    openai.api_key = openai_api_key

    @st.cache_resource(show_spinner=False)
    def load_data():
        with st.spinner(text="Cargando los archivos de datos – espere! Deberia tardar entre 1-2 minutos."):
            reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
            docs = reader.load_data()
            service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.3, system_prompt="Contestarás en sempre en el idioma català. Ets un assitent personal que respondràs les preguntes del usuari. Seràs servicial i educat, donaràs info que sapiguis de la empresa, del chatbot i dels documents."))
            index = VectorStoreIndex.from_documents(docs, service_context=service_context)
            return index

    index = load_data()

    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    if 'welcome_message_shown' not in st.session_state:
        st.session_state.welcome_message_shown = False

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if not st.session_state.welcome_message_shown:
        with st.chat_message("assistant"):
            st.markdown("""
                Bienvenido al chatbot de GRK 👋.  
                Deberás poner tu clave de API de OpenAI en el menú de la izquierda.  
                
                Puedes hacer preguntas del estilo:
                - ¿Quién es el cliente GRK?
                - Dame el teléfono de John Doe.
                - Dame toda la info del cliente Pepito Grillo.
                - Info del artículo 1009.
                - Dame toda la info del albarán 1014.
                - ¿Cuánto son los ingresos del cliente GRK?
            """)
        st.session_state.welcome_message_shown = True

    user_input = st.chat_input('Ingresa tu pregunta:')

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        if not openai_api_key.startswith('sk-'):
            st.warning('Porfavor introduce una clave válida de OpenAI!', icon='⚠')
        else:
            api_response_url = ask_fine_tuned_ada(user_input)
            full_url = DOMINIO + api_response_url
            response = requests.get(full_url)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
            
            if response.status_code == 200:
                data = response.json()
                
                if "/api/art_stat?stat=stat_marca" in api_response_url:
                    render_pie_chart_marca(data)

                if "/api/art_stat?stat=stat_fam" in api_response_url:
                    render_pie_chart_fam(data)
                                        
                else:
                    json_response = generate_response_from_mongo_results(data)
                    gpt_response = ask_gpt(json_response, message_placeholder,additional_context=user_input)
                    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
                    
            else:
                with st.chat_message("assistant"):
                    with st.spinner("Pensando..."):
                        response = chat_engine.chat(user_input)
                        st.write(response.response)
                        message = {"role": "assistant", "content": response.response}
                        st.session_state.chat_history.append(message)