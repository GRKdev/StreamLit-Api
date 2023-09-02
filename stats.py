import streamlit as st
import requests
import os
from chart_utils import render_pie_chart_marca, render_pie_chart_fam, render_pie_chart_comunidad_autonoma, render_pie_chart_comunidad_autonoma_barra,render_bar_chart_monthly_revenue_echarts

def show_stats_page():
    dominio = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))
    
def show_stats_page():
    if 'show_chart' not in st.session_state:
        st.session_state.show_chart = []
    
    dominio = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))

    if st.button("Limpiar gráficos"):
        st.session_state.show_chart = []

    with st.sidebar.expander("🔍 Artículos"):
        if st.button("Marca Producto", key='button_marca_producto'):
            api_response_url = "/api/art_stat?stat=stat_marca"
            full_url = dominio + api_response_url
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                st.session_state.show_chart.insert(0, ("marca", data))
        
        if st.button("Familia Producto", key='button_familia_producto'):
            api_response_url = "/api/art_stat?stat=stat_fam"
            full_url = dominio + api_response_url
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                st.session_state.show_chart.insert(0, ("fam", data))

    with st.sidebar.expander("👥 Clientes"):

        if st.button("Domicili Client", key='button_domicili_client'):
            api_response_url = "/api/cli_stat?stat=comu" 
            full_url = dominio + api_response_url
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                st.session_state.show_chart.insert(0, ("cli", data))
            
        if st.button("Client barres", key='button_client_barres'):
            api_response_url = "/api/cli_stat?stat=comu" 
            full_url = dominio + api_response_url
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                st.session_state.show_chart.insert(0, ("cli_barras", data))
                  
    with st.sidebar.expander("📄 Albaranes"):

        if st.button("Ejemplo: Ingresos Cliente GRK", key='button_key'):
            api_response_url = "/api/alb_stat?cli_mes=grk"
            full_url = dominio + api_response_url
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                st.session_state.show_chart.insert(0, ("ingr", data))


    for i, (chart_type, data) in enumerate(st.session_state.show_chart):
        with st.container():
            if chart_type == "marca":
                render_pie_chart_marca(data)
            elif chart_type == "fam":
                render_pie_chart_fam(data)
            elif chart_type == "cli":
                render_pie_chart_comunidad_autonoma(data)                
            elif chart_type == "cli_barras":
                render_pie_chart_comunidad_autonoma_barra(data)     
            elif chart_type == "ingr":
                render_bar_chart_monthly_revenue_echarts(data, key=f'render_chart_client_{i}')                                     