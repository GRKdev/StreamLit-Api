import streamlit as st
from apps.chat_bot import chat_bot
from apps.chatbot_llama import XatBot_Llama
from apps.stats import show_stats_page
from utils.sidebar_info import logo

st.set_page_config(
    page_title="Chatbot - GRK",
    page_icon="IMG/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# **GRKdev** v1.1"
    }
)

logo()
chat_bot()
# page = st.sidebar.radio("Menú", ["ChatBot", "Chatbot Llama"])

# if page == "ChatBot":
#     chat_bot()
# # elif page == "Estadísticas":
# #     show_stats_page()
# elif page == "Chatbot Llama":
#     XatBot_Llama()
