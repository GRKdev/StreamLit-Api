# import openai
# import os
import streamlit as st
from utils.sidebar_info import footer
from PIL import Image
import base64


# import requests
# import re
# from llama_index import VectorStoreIndex, ServiceContext
# from llama_index.llms import OpenAI
# from llama_index import SimpleDirectoryReader

last_assistant_response = None

def XatBot_Llama():
    image = Image.open('IMG/light-uc.png')
    st.image(image, use_column_width=False,  width=500)
#     DOMINIO = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))
#     OPEN_AI_MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL"))

#     def ask_gpt(prompt, placeholder, additional_context=None):
#         global last_assistant_response
#         messages_list = [
#             {"role": "system", "content": "Ets un assistent de la empresa GRK que respon sempre en estil MarkDown, mostra les dades relevants en Negrita. No expliquis com realitzar calculs, dona la resposta directament. Rebràs pregunta de l'usuari juntament amb dades obtingudes d'una base de dades. Has d'utilitzar ambdós per proporcionar una resposta coherent, clara i útil. Assegura't d'estructurar la informació de manera amigable i fàcil de comprendre per a l'usuari, el nom de client, article o albarà al principi. Si el json conté múltiples elements, sintetitza la informació de manera concisa. Quan tractis amb números monetaris, afegeix el simbol €."},
#             {"role": "user", "content": ""},
#             {"role": "assistant", "content": ""},
#         ]
#         if last_assistant_response:
#             messages_list.append({"role": "assistant", "content": last_assistant_response})

#         if additional_context:
#             messages_list.append({"role": "user", "content": additional_context})

#         messages_list.append({"role": "user", "content": prompt})
#         full_response = ""
        
#         for response in openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages_list,
#             max_tokens=1000,
#             n=1,
#             stop=None,
#             temperature=0.2,
#             stream=True,
#         ):
#             full_response += response.choices[0].delta.get("content", "")
#             placeholder.markdown(full_response + "▌")
#         placeholder.markdown(full_response)
        
#         last_assistant_response = full_response.strip()
#         return last_assistant_response

#     def ask_fine_tuned_ada(prompt):
#         response = openai.Completion.create(
#             engine=OPEN_AI_MODEL,
#             prompt=prompt,
#             max_tokens=100,
#             n=1,
#             stop="&&",
#             temperature=0,
#         )
#         api_response = response.choices[0].text.strip()

#         match = re.search(r'(api/[^ ?]+)(\?.*)?', api_response)

#         if match:
#             sanitized_response = match.group(0)
#         else:
#             sanitized_response = ""

#         print(f"Sanitized Response: {sanitized_response}")

#         return sanitized_response

#     def generate_response_from_mongo_results(data):
#         print(f"data: {data}") 
#         if not data:
#             return "No se encontraron resultados."
#         else:
#             return str(data)
    
#     st.title('XatBot API NOSQL - Llama version')

#     with st.sidebar.expander("🧩 Exemples", False):
#         st.markdown("""
#         *Dona'm info del client GRK*
                    
#         *info article Apple*
                    
#         *telefono de Maria Lopez*
                    
#         *¿Cual es el albaran 1012?*
                    
#         """)
    footer()

#     @st.cache_resource(show_spinner=False)
#     def load_data():
#         with st.spinner(text="Cargando los archivos de datos – espere! Deberia tardar entre 1-2 minutos."):
#             reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
#             docs = reader.load_data()
#             service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="Contestarás en sempre en el idioma català. Ets un assitent personal que respondràs les preguntes del usuari. Seràs servicial i educat, donaràs info que sapiguis de la empresa, del chatbot i dels documents."))
#             index = VectorStoreIndex.from_documents(docs, service_context=service_context)
#             return index

#     index = load_data()

#     chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

#     if 'chat_history' not in st.session_state:
#         st.session_state.chat_history = []
        
#     if 'welcome_message_shown' not in st.session_state:
#         st.session_state.welcome_message_shown = False

#     for message in st.session_state.chat_history:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if not st.session_state.welcome_message_shown:
#         with st.chat_message("assistant"):
#             st.markdown("""
#                 Bienvenido al chatbot de GRK 👋.  
#                 Deberás poner tu clave de API de OpenAI en el menú de la izquierda.  
                
#                 Puedes hacer preguntas del estilo:
#                 - ¿Quién es el cliente GRK?
#                 - Dame el teléfono de John Doe.
#                 - Dame toda la info del cliente Pepito Grillo.
#                 - Info del artículo 1009.
#                 - Dame toda la info del albarán 1014.
#                 - ¿Cuánto son los ingresos del cliente GRK?
#             """)
#         st.session_state.welcome_message_shown = True

#     user_input = st.chat_input('Ingresa tu pregunta:')

#     if user_input:
#         st.session_state.chat_history.append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.markdown(user_input)

#             api_response_url = ask_fine_tuned_ada(user_input)
#             full_url = DOMINIO + api_response_url
#             response = requests.get(full_url)
#             response_llama = chat_engine.stream_chat(user_input)

#             with st.chat_message("assistant"):
#                 message_placeholder = st.empty()

#             if response.status_code == 200:
#                 data = response.json()
#                 json_response = generate_response_from_mongo_results(data)
#                 gpt_response = ask_gpt(json_response, message_placeholder, additional_context=user_input)
#                 st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})

#             else:
#                 output = ""
#                 for token in response_llama.response_gen:
#                     output += token
#                     message_placeholder.markdown(output) 

#                 st.session_state.chat_history.append({"role": "assistant", "content": response_llama.response})
