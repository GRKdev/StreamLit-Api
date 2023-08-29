import openai
import os
import streamlit as st
import requests
import re

dominio = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))
openai_model_ada = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL"))

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
openai.api_key = openai_api_key

def ask_gpt_streaming(prompt, placeholder):
    messages_list = [
        {"role": "system", "content": "Ets un assistent de la empresa GRK que respon sempre en estil MarkDown, mostra les dades relevants en Negrita. Rebràs pregunta de l'usuari juntament amb dades en format json obtingudes d'una base de dades. Has d'utilitzar ambdós per proporcionar una resposta coherent, clara i útil. Assegura't d'estructurar la informació de manera amigable i fàcil de comprendre per a l'usuari, el nom de client, article o albarà al principi. Si el json conté múltiples elements, sintetitza la informació de manera concisa. Quan tractis amb números monetaris, afegeix el simbol €."},
        {"role": "user", "content": ""},
        {"role": "assistant", "content": ""},
    ]
    
    messages_list.append({"role": "user", "content": prompt})
    full_response = ""
    
    for response in openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_list,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.2,
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
        placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)
    
    return full_response.strip()


def ask_fine_tuned_ada(prompt):
    response = openai.Completion.create(
        engine=openai_model_ada,
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
    
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    

st.title('XatBot API NOSQL')


for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input('Ingresa tu pregunta:')

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    if not openai_api_key.startswith('sk-'):
        st.warning('Porfavor introduce una clave válida de OpenAI!', icon='⚠')
    else:
        api_response_url = ask_fine_tuned_ada(user_input)
        full_url = dominio + api_response_url
        
        response = requests.get(full_url)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
        
        if response.status_code == 200:
            data = response.json()
            json_response = generate_response_from_mongo_results(data)
            gpt_response = ask_gpt_streaming(json_response, message_placeholder)
            st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
        else:
            gpt_response = ask_gpt_streaming(user_input, message_placeholder)
            st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
