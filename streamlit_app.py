import streamlit as st
from chat_bot import chat_bot
from chatbot_llama import XatBot_Llama
from stats import show_stats_page

st.set_page_config(
    page_title="Chabot - GRK",
    page_icon="🎛",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# **GRKdev** v1"
    }
)

page = st.sidebar.radio("Menú", ["ChatBot", "Chatbot Llama", "Estadísticas"])

if page == "ChatBot":
    chat_bot()
elif page == "Estadísticas":
    show_stats_page()
elif page == "Chatbot Llama":
    XatBot_Llama()
