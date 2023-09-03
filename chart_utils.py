import streamlit as st
from streamlit_echarts import st_echarts

def render_pie_chart_marca(data):
    prepared_data = [{"value": d["Cantidad"], "name": d["Marca"]} for d in data]
    
    options = {
        "backgroundColor": "#0E1117",
        "title": {"text": "Marques de Productes", "left": "center"},
        "tooltip": {"trigger": "item"},
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

    s = st_echarts(options=options, height="550px", theme="dark")
    if s is not None:
        st.write(s)

def render_pie_chart_fam(data):
    prepared_data = [{"value": d["Cantidad"], "name": d["Familia"]} for d in data]
    
    options = {
        "backgroundColor": "#0E1117",
        "title": {"text": "Familia - Productes", "left": "center"},
        "tooltip": {"trigger": "item"},
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

    s = st_echarts(options=options, height="550px", theme="dark")
    if s is not None:
        st.write(s)

def render_pie_chart_comunidad_autonoma(data):
    prepared_data = [{"value": d["Cantidad"], "name": d["ComunidadAutonoma"]} for d in data]
    
    options = {
        "backgroundColor": "#0E1117",
        "title": {"text": "Clientes por Comunidad Autonoma", "left": "center"},
        "tooltip": {"trigger": "item"},
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

    s = st_echarts(options=options, height="550px", theme="dark")
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
        "xAxis": {
            "type": "category", 
            "data": x_data,
            "axisLabel": {
                "rotate": 0,
                "fontSize": 8

            }
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Comunidad Autonoma",
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

    s = st_echarts(options=options, height="550px", theme="dark")
    if s is not None:
        st.write(s)

def render_bar_chart_monthly_revenue_echarts(data, key=None):
    data_dict = data[0] if data else {}
    
    nombre_cliente = data_dict.get("NombreCliente", "Desconocido")
    current_year = data_dict.get("Año", "Desconocido")
    
    ingresos_mensuales = data_dict.get("IngresosMensuales", {})
    
    meses = [
        'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
    ]
    x_data = meses
    y_data = [float(ingresos_mensuales.get(mes, "0 €").replace(" €", "")) for mes in meses]
    total_ingresos = sum(y_data)

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": f"Facturación cliente {nombre_cliente}: {current_year} (Total: {total_ingresos} €)",
            "left": "center"
        },
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category", 
            "data": x_data,
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Ingresos Mensuales",
                "type": "bar",
                "data": y_data,
                "label": {
                    "show": True,
                    "position": "inside",
                    "formatter": "{c} €"
                },             
            }
        ],
    }
    s = st_echarts(options=options, height="550px", key=key ,theme="dark")
    if s is not None:
        st.write(s)

def render_bar_chart_monthly_revenue_currentyear(data, key=None):
    data_dict = data[0] if data else {}
    
    current_year = data_dict.get("Año", "Desconocido")
    
    ingresos_mensuales = data_dict.get("IngresosMensuales", {})
    
    meses = [
        'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
    ]
    x_data = meses
    y_data = [float(ingresos_mensuales.get(mes, "0 €").replace(" €", "")) for mes in meses]
    total_ingresos = sum(y_data)

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": f"Facturación {current_year} (Total: {total_ingresos} €)",
            "left": "center"
        },
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category", 
            "data": x_data,
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Ingresos Mensuales",
                "type": "bar",
                "data": y_data,
                "label": {
                    "show": True,
                    "position": "inside",
                    "formatter": "{c} €"
                },             
            }
        ],
    }
    s = st_echarts(options=options, height="550px", key=key ,theme="dark")
    if s is not None:
        st.write(s)

def render_bar_chart_anual_revenue(data, key=None):
    anuales_data = data[0]["IngresosAnuales"]
 
    prepared_data = [
        {"value": float(d["Cantidad"].split(" ")[0].replace(",", ".")), "year": str(d["Año"])}
        for d in anuales_data
    ]

    total_sum = sum(d["value"] for d in prepared_data)

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": f"Facturaciones Anuales (Total: {total_sum} €)",
            "left": "center"
        },
        "tooltip": {"trigger": "item"},
        "xAxis": {
            "type": "category",
            "data": [d["year"] for d in prepared_data],
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "year": "Cantidad",
                "type": "bar",
                "data": [d["value"] for d in prepared_data],
                "label": {
                    "show": True,
                    "position": "inside",
                    "formatter": "{c} €"
                },                
            }
        ],
    }

    st_echarts(options=options, height="550px", key=key,theme="dark")
