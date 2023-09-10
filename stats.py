import streamlit as st
import requests
import os
from utils.generate_token import create_jwt
from utils.chart_utils import (
    render_pie_chart_marca, render_pie_chart_family, render_pie_chart_comunidad_autonoma, render_pie_chart_comunidad_autonoma_barra,
    render_bar_chart_monthly_revenue_client, render_bar_chart_monthly_revenue_monthly_year, render_bar_chart_anual_revenue,
    render_grouped_bar_chart_fact, render_grouped_bar_chart_ing, render_bar_chart_monthly_revenue_monthly_year_ing,
    render_bar_chart_monthly_revenue_client_ing
)

DOMINIO = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))
token = create_jwt()

def make_authenticated_request(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    full_url = DOMINIO + url
    response = requests.get(full_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def show_stats_page():
    if 'show_chart' not in st.session_state:
        st.session_state.show_chart = []

    if st.button("Limpiar gráficos"):
        st.session_state.show_chart = []

    with st.sidebar.expander("🔍 Artículos"):
        if st.button("Marca Producto", key='button_marca_producto'):
            data = make_authenticated_request("/api/art_stat?stat=stat_marca", token)
            if data:
                st.session_state.show_chart.insert(0, ("marca", data))
        
        if st.button("Familia Producto", key='button_familia_producto'):
            data = make_authenticated_request("/api/art_stat?stat=stat_fam", token)
            if data:
                st.session_state.show_chart.insert(0, ("fam", data))

    with st.sidebar.expander("👥 Clientes"):
        if st.button("Domicili Client", key='button_domicili_client'):
            data = make_authenticated_request("/api/cli_stat?stat=comu", token)
            if data:
                st.session_state.show_chart.insert(0, ("cli", data))
                
        if st.button("Client barres", key='button_client_barres'):
            data = make_authenticated_request("/api/cli_stat?stat=comu", token)
            if data:
                st.session_state.show_chart.insert(0, ("cli_barras", data))

    with st.sidebar.expander("💶 Facturación"):
        if st.button("Anuales agrupadas", key='button_ingresos_anuales_group'):
            data = make_authenticated_request("/api/alb_stat?fact_total=true", token)
            if data:
                st.session_state.show_chart.insert(0, ("total_group_fact", data))

        if st.button("2023", key='button_ingresos_current_year'):
            data = make_authenticated_request("/api/alb_stat?fact_cy=true", token)
            if data:
                st.session_state.show_chart.insert(0, ("cy", data))
                
        if st.button("2022", key='button_ingresos_selected_year'):
            data = make_authenticated_request("/api/alb_stat?fact_sy=2022", token)
            if data:
                st.session_state.show_chart.insert(0, ("selectedyear", data))
                
        if st.button("Cliente GRK", key='button_key'):
            data = make_authenticated_request("/api/alb_stat?cli_fact_cy=grk", token)
            if data:
                st.session_state.show_chart.insert(0, ("facturacio_client", data))

    with st.sidebar.expander("💰 Ingresos"):
        if st.button("Anuales agrupadas", key='button_ganancias_anuales_group'):
            data = make_authenticated_request("/api/alb_stat?ing_total=true", token)
            if data:
                st.session_state.show_chart.insert(0, ("total_group_ing", data))

        if st.button("2023", key='button_ganacias_current_year'):
            data = make_authenticated_request("/api/alb_stat?ing_cy=true", token)
            if data:
                st.session_state.show_chart.insert(0, ("ing_cy", data))

        if st.button("2022", key='button_ganacias_selected_year'):
            data = make_authenticated_request("/api/alb_stat?ing_sy=2022", token)
            if data:
                st.session_state.show_chart.insert(0, ("selectedyear_ing", data))

        if st.button("Cliente GRK", key='button_ing_key'):
            data = make_authenticated_request("/api/alb_stat?cli_ing_cy=grk", token)
            if data:
                st.session_state.show_chart.insert(0, ("ganancia_client", data))

    st.sidebar.markdown("---")  
    st.sidebar.markdown(
    '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="12">&nbsp by <a href="https://github.com/GRKdev">@GRKdev</a></h6>',
    unsafe_allow_html=True,
    )
   
    for i, (chart_type, data) in enumerate(st.session_state.show_chart):
        with st.container():
            if chart_type == "marca":
                render_pie_chart_marca(data)
            elif chart_type == "fam":
                render_pie_chart_family(data)
            elif chart_type == "cli":
                render_pie_chart_comunidad_autonoma(data)                
            elif chart_type == "cli_barras":
                render_pie_chart_comunidad_autonoma_barra(data)     
            elif chart_type == "facturacio_client":
                render_bar_chart_monthly_revenue_client(data, key=f'render_chart_fact_client_{i}')          
            elif chart_type == "ganancia_client":
                render_bar_chart_monthly_revenue_client_ing(data, key=f'render_chart_fact_client_{i}')                                                 
            elif chart_type == "cy":
                render_bar_chart_monthly_revenue_monthly_year(data, key=f'render_chart_cy_{i}')                                                     
            elif chart_type == "total":
                render_bar_chart_anual_revenue(data, key=f'render_chart_anual_{i}')                                                     
            elif chart_type == "selectedyear":
                render_bar_chart_monthly_revenue_monthly_year(data, key=f'render_chart_total_{i}')           
            elif chart_type == "total_group_fact":
                render_grouped_bar_chart_fact(data, key=f'render_chart_anual_group_{i}')    
            elif chart_type == "total_group_ing":
                render_grouped_bar_chart_ing(data, key=f'render_chart_anual_group_{i}')    
            elif chart_type == "ing_cy":
                render_bar_chart_monthly_revenue_monthly_year_ing(data, key=f'render_chart_gan_cy_{i}')   
            elif chart_type == "selectedyear_ing":
                render_bar_chart_monthly_revenue_monthly_year_ing(data, key=f'render_chart_gan_sy_{i}')                                   

