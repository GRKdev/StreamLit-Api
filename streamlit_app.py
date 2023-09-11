import streamlit as st
from chatbot import XatBot
from chatbot_llama import XatBot_Llama
from stats import show_stats_page

st.set_page_config(
    page_title="Xabot API",
    page_icon="🎛",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# **GRKdev** v0.1.0"
    }
)

page = st.sidebar.radio("Menú", ["ChatBot", "Chatbot Llama", "Estadísticas"])

if page == "ChatBot":
    XatBot()
elif page == "Estadísticas":
    show_stats_page()
elif page == "Chatbot Llama":
    XatBot_Llama()