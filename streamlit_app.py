import streamlit as st
from chatbot import XatBot
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

page = st.sidebar.radio("Menú", ["ChatBot", "Estadísticas"])

if page == "ChatBot":
    XatBot()
# Página de estadísticas
elif page == "Estadísticas":
    show_stats_page()