# chart_utils.py
import streamlit as st
from streamlit_echarts import st_echarts

def render_pie_chart_marca(data):
    prepared_data = [{"value": d["Cantidad"], "name": d["Marca"]} for d in data]
    
    options = {
        "backgroundColor": "#0E1117",
        "title": {"text": "Marques de Productes", "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "right": "right"},
        "series": [
            {
                "name": "Cantidad",
                "type": "pie",
                "radius": "50%",
                "data": prepared_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }

    s = st_echarts(options=options, height="800px", key="render_pie_events", theme="dark")
    if s is not None:
        st.write(s)

def render_pie_chart_fam(data):
    prepared_data = [{"value": d["Cantidad"], "name": d["Familia"]} for d in data]
    
    options = {
        "backgroundColor": "#0E1117",
        "title": {"text": "Familia - Productes", "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "right": "right"},
        "series": [
            {
                "name": "Cantidad",
                "type": "pie",
                "radius": "50%",
                "data": prepared_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }

    s = st_echarts(options=options, height="800px", key="render_pie_events", theme="dark")
    if s is not None:
        st.write(s)

def render_pie_chart_comunidad_autonoma(data):
    prepared_data = [{"value": d["Cantidad"], "name": d["ComunidadAutonoma"]} for d in data]
    
    options = {
        "backgroundColor": "#0E1117",
        "title": {"text": "Clientes por Comunidad Autonoma", "left": "center"},
        "tooltip": {"trigger": "item"},
        "legend": {"orient": "vertical", "right": "right"},
        "series": [
            {
                "name": "Cantidad",
                "type": "pie",
                "radius": "50%",
                "data": prepared_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }

    s = st_echarts(options=options, height="800px", key="render_pie_events", theme="dark")
    if s is not None:
        st.write(s)

def render_pie_chart_comunidad_autonoma_barra(data):
    prepared_data = [{"value": d["Cantidad"], "name": d["ComunidadAutonoma"]} for d in data]
    
    x_data = [d['name'] for d in prepared_data]
    y_data = [d['value'] for d in prepared_data]
    
    options = {
        "backgroundColor": "#0E1117",
        "title": {"text": "Clientes por Comunidad Autonoma", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "legend": {"orient": "vertical", "right": "right"},
        "xAxis": {
            "type": "category", 
            "data": x_data,
            "axisLabel": {
                "rotate": 0  # rota las etiquetas 90 grados
            }
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Cantidad",
                "type": "bar",
                "data": y_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }

    s = st_echarts(options=options, height="800px", theme="dark")
    if s is not None:
        st.write(s)
