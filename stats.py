import streamlit as st
from utils.sidebar_info import display_sidebar_info_stats
from utils.chart_utils import (
    render_pie_chart_marca, render_pie_chart_family, render_pie_chart_comunidad_autonoma, render_pie_chart_comunidad_autonoma_barra,
    render_bar_chart_monthly_revenue_client, render_bar_chart_monthly_revenue_monthly_year, render_bar_chart_monthly_revenue_client_ing,
    render_grouped_bar_chart_fact, render_grouped_bar_chart_ing, render_bar_chart_monthly_revenue_monthly_year_ing
)
def show_stats_page():
    if 'show_chart' not in st.session_state:
        st.session_state.show_chart = []

    if st.button("Limpiar gráficos"):
        st.session_state.show_chart = []

    display_sidebar_info_stats()

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

