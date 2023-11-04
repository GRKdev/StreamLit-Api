import streamlit as st
from chat_bot import chat_bot
from utils.sidebar_info import logo

st.set_page_config(
    page_title="Chatbot - GRK",
    page_icon="IMG/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "# **GRKdev** v1.1"},
)

logo()
chat_bot()
