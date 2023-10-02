import streamlit as st
from streamlit_echarts import st_echarts
import os


if "saved_charts" not in st.session_state:
    st.session_state.saved_charts = []

MONTHS = [
    "Ene",
    "Feb",
    "Mar",
    "Abr",
    "May",
    "Jun",
    "Jul",
    "Ago",
    "Sep",
    "Oct",
    "Nov",
    "Dic",
]

OPEN_AI_MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL"))
model_name_ft = st.secrets["OPENAI_MODEL"].split(":")[3].upper()


def display_chart_and_warning(
    options, key=None, height="500px", theme="dark", write_s=False
):
    s = (
        st_echarts(options=options, height=height, key=key, theme=theme)
        if key
        else st_echarts(options=options, height=height, theme=theme)
    )
    if write_s and s is not None:
        st.write(s)
    st.markdown(
        f"<div style='text-align:right; color:lightblue; font-size:small;'>📊 Petición API con modelo: {model_name_ft}. Resultados directos de la base de datos.</div>",
        unsafe_allow_html=True,
    )


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
    display_chart_and_warning(options, write_s=True)


def render_pie_chart_family(data):
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

    display_chart_and_warning(options, write_s=True)


def render_pie_chart_comunidad_autonoma(data):
    prepared_data = [
        {"value": d["Cantidad"], "name": d["ComunidadAutonoma"]} for d in data
    ]

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

    display_chart_and_warning(options, write_s=True)


def render_pie_chart_comunidad_autonoma_barra(data):
    prepared_data = [
        {"value": d["Cantidad"], "name": d["ComunidadAutonoma"]} for d in data
    ]

    x_data = [d["name"] for d in prepared_data]
    y_data = [d["value"] for d in prepared_data]

    options = {
        "backgroundColor": "#0E1117",
        "title": {"text": "Clientes por Comunidad Autonoma", "left": "center"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": x_data,
            "axisLabel": {"rotate": 0, "fontSize": 8},
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

    display_chart_and_warning(options, write_s=True)


def render_bar_chart_monthly_revenue_client(data, key=None):
    data_dict = data[0] if data else {}

    nombre_cliente = data_dict.get("NombreCliente", "Desconocido")
    current_year = data_dict.get("Año", "Desconocido")

    ingresos_mensuales = data_dict.get("IngresosMensuales", {})

    x_data = MONTHS
    y_data = [
        float(ingresos_mensuales.get(mes, "0 €").replace(" €", "")) for mes in MONTHS
    ]
    total_ingresos = round(sum(y_data), 2)

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": f"Facturación cliente {nombre_cliente}: {current_year} (Total: {total_ingresos} €)",
            "left": "center",
        },
        "tooltip": {"trigger": "axis"},
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ["line", "bar"]},
            },
        },
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
                    "fontSize": 12,
                    "formatter": "{c} €",
                    "color": "#FFFFFF",
                    "align": "middle",
                    "verticalAlign": "middle",
                    "backgroundColor": "#000000",
                    "borderRadius": 8,
                    "padding": [3, 4],
                },
                "markPoint": {
                    "symbol": "pin",
                    "symbolSize": 40,
                    "data": [
                        {"type": "max", "name": "Max"},
                        {"type": "min", "name": "Min"},
                    ],
                    "label": {"show": False},
                },
                "markLine": {
                    "data": [{"type": "average", "name": "Avg"}],
                    "precision": 2,
                },
            }
        ],
    }
    display_chart_and_warning(options, write_s=True)


def render_bar_chart_monthly_revenue_client_ing(data, key=None):
    data_dict = data[0] if data else {}

    nombre_cliente = data_dict.get("NombreCliente", "Desconocido")
    current_year = data_dict.get("Año", "Desconocido")

    ingresos_mensuales = data_dict.get("IngresosMensuales", {})

    x_data = MONTHS
    y_data = [
        float(ingresos_mensuales.get(mes, "0 €").replace(" €", "")) for mes in MONTHS
    ]
    total_ingresos = round(sum(y_data), 2)

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": f"Ganancias del cliente {nombre_cliente}: {current_year} (Total: {total_ingresos} €)",
            "left": "center",
        },
        "tooltip": {"trigger": "axis"},
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ["line", "bar"]},
            },
        },
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
                "label": {"show": True, "position": "inside", "formatter": "{c} €"},
                "itemStyle": {"color": "#90EE90"},
                "markPoint": {
                    "symbol": "pin",
                    "data": [
                        {"type": "max", "name": "Max"},
                        {"type": "min", "name": "Min"},
                    ],
                },
                "markLine": {
                    "data": [{"type": "average", "name": "Avg"}],
                    "precision": 2,
                },
            }
        ],
    }
    display_chart_and_warning(options, write_s=True)


def render_bar_chart_monthly_revenue_monthly_year(data, key=None):
    data_dict = data[0] if data else {}

    current_year = data_dict.get("Año", "Desconocido")

    ingresos_mensuales = data_dict.get("IngresosMensuales", {})

    x_data = MONTHS
    y_data = [
        float(ingresos_mensuales.get(mes, "0 €").replace(" €", "")) for mes in MONTHS
    ]
    total_ingresos = round(sum(y_data), 2)

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": f"Facturación {current_year} (Total: {total_ingresos} €)",
            "left": "center",
        },
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": x_data,
        },
        "yAxis": {"type": "value"},
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ["line", "bar"]},
            },
        },
        "series": [
            {
                "name": "Ingresos Mensuales",
                "type": "bar",
                "data": y_data,
                "label": {"show": True, "position": "inside", "formatter": "{c} €"},
                "markPoint": {
                    "symbol": "pin",
                    "data": [
                        {"type": "max", "name": "Max"},
                        {"type": "min", "name": "Min"},
                    ],
                },
                "markLine": {
                    "data": [{"type": "average", "name": "Avg"}],
                    "precision": 2,
                },
            }
        ],
    }
    display_chart_and_warning(options, key=key, write_s=True)


def render_bar_chart_monthly_revenue_monthly_year_ing(data, key=None):
    data_dict = data[0] if data else {}

    current_year = data_dict.get("Año", "Desconocido")

    ingresos_mensuales = data_dict.get("IngresosMensuales", {})

    x_data = MONTHS
    y_data = [
        float(ingresos_mensuales.get(mes, "0 €").replace(" €", "")) for mes in MONTHS
    ]
    total_ingresos = round(sum(y_data), 2)

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": f"Ganancias {current_year} (Total: {total_ingresos} €)",
            "left": "center",
        },
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": x_data,
        },
        "yAxis": {"type": "value"},
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ["line", "bar"]},
            },
        },
        "series": [
            {
                "name": "Ingresos Mensuales",
                "type": "bar",
                "data": y_data,
                "label": {"show": True, "position": "inside", "formatter": "{c} €"},
                "itemStyle": {"color": "#90EE90"},
                "markPoint": {
                    "symbol": "pin",
                    "data": [
                        {"type": "max", "name": "Max"},
                        {"type": "min", "name": "Min"},
                    ],
                },
                "markLine": {
                    "data": [{"type": "average", "name": "Avg"}],
                    "precision": 2,
                },
            }
        ],
    }
    display_chart_and_warning(options, write_s=True)


def render_grouped_bar_chart_fact(data, key=None):
    years = [str(d["Año"]) for d in data]

    series_data = []
    yearly_sums = {}

    for year_data in data:
        year = str(year_data["Año"])
        monthly_data = year_data["IngresosMensuales"]

        monthly_values = [
            float(monthly_data.get(mes, "0 €").split(" ")[0].replace(",", "."))
            for mes in MONTHS
        ]
        yearly_sums[year] = round(sum(monthly_values), 2)

    legend_names = [
        f"{year} ({yearly_sums[year]:.2f} €)" for year in years if year in yearly_sums
    ]

    for year in years:
        if year in yearly_sums:
            monthly_values = [
                float(
                    data[int(year) - int(years[0])]["IngresosMensuales"]
                    .get(mes, "0 €")
                    .split(" ")[0]
                    .replace(",", ".")
                )
                for mes in MONTHS
            ]
            series_data.append(
                {
                    "name": f"{year} ({yearly_sums[year]:.2f} €)",
                    "type": "bar",
                    "data": monthly_values,
                    "markPoint": {
                        "symbol": "pin",
                        "data": [
                            {"type": "max", "name": "Max"},
                            {"type": "min", "name": "Min"},
                        ],
                    },
                    "markLine": {
                        "data": [{"type": "average", "name": "Avg"}],
                        "precision": 2,
                    },
                }
            )

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": "Facturaciones Anuales",
        },
        "tooltip": {"trigger": "axis"},
        "legend": {"data": legend_names},
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ["line", "bar"]},
            },
        },
        "xAxis": [{"type": "category", "data": MONTHS}],
        "yAxis": [{"type": "value"}],
        "series": series_data,
    }

    display_chart_and_warning(options, key=key)


def render_grouped_bar_chart_fact_cli_3_years(data, key=None):
    years = [str(d["Año"]) for d in data]
    data_dict = data[0] if data else {}
    nombre_cliente = data_dict.get("NombreCliente", "Desconocido")
    series_data = []
    yearly_sums = {}

    for year_data in data:
        year = str(year_data["Año"])
        monthly_data = year_data["IngresosMensuales"]

        monthly_values = [
            float(monthly_data.get(mes, "0 €").split(" ")[0].replace(",", "."))
            for mes in MONTHS
        ]
        yearly_sums[year] = round(sum(monthly_values), 2)

    legend_names = [
        f"{year} ({yearly_sums[year]:.2f} €)" for year in years if year in yearly_sums
    ]

    for year in years:
        if year in yearly_sums:
            monthly_values = [
                float(
                    next(y for y in data if str(y["Año"]) == year)["IngresosMensuales"]
                    .get(mes, "0 €")
                    .split(" ")[0]
                    .replace(",", ".")
                )
                for mes in MONTHS
            ]
            series_data.append(
                {
                    "name": f"{year} ({yearly_sums[year]:.2f} €)",
                    "type": "bar",
                    "data": monthly_values,
                    "markPoint": {
                        "symbol": "pin",
                        "data": [
                            {"type": "max", "name": "Max"},
                            {"type": "min", "name": "Min"},
                        ],
                    },
                    "markLine": {
                        "data": [{"type": "average", "name": "Avg"}],
                        "precision": 2,
                    },
                }
            )

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": f"Facturación Cliente: {nombre_cliente}",
        },
        "tooltip": {"trigger": "axis"},
        "legend": {"data": legend_names},
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ["line", "bar"]},
            },
        },
        "xAxis": [{"type": "category", "data": MONTHS}],
        "yAxis": [{"type": "value"}],
        "series": series_data,
    }

    display_chart_and_warning(options, key=key)


def render_grouped_bar_chart_ing(data, key=None):
    years = [str(d["Año"]) for d in data]

    series_data = []
    yearly_sums = {}

    for year_data in data:
        year = str(year_data["Año"])
        monthly_data = year_data["IngresosMensuales"]

        monthly_values = [
            float(monthly_data.get(mes, "0 €").split(" ")[0].replace(",", "."))
            for mes in MONTHS
        ]
        yearly_sums[year] = round(sum(monthly_values), 2)

    legend_names = [
        f"{year} ({yearly_sums[year]:.2f} €)" for year in years if year in yearly_sums
    ]

    for year in years:
        if year in yearly_sums:
            monthly_values = [
                float(
                    data[int(year) - int(years[0])]["IngresosMensuales"]
                    .get(mes, "0 €")
                    .split(" ")[0]
                    .replace(",", ".")
                )
                for mes in MONTHS
            ]
            series_data.append(
                {
                    "name": f"{year} ({yearly_sums[year]:.2f} €)",
                    "type": "bar",
                    "data": monthly_values,
                    "markPoint": {
                        "symbol": "pin",
                        "data": [
                            {"type": "max", "name": "Max"},
                            {"type": "min", "name": "Min"},
                        ],
                    },
                    "markLine": {
                        "data": [{"type": "average", "name": "Avg"}],
                        "precision": 2,
                    },
                }
            )

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": "Ganancias Anuales",
        },
        "tooltip": {"trigger": "axis"},
        "legend": {"data": legend_names},
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ["line", "bar"]},
            },
        },
        "xAxis": [{"type": "category", "data": MONTHS}],
        "yAxis": [{"type": "value"}],
        "series": series_data,
    }

    display_chart_and_warning(options, key=key)


def render_grouped_bar_chart_ing_cli_3_years(data, key=None):
    years = [str(d["Año"]) for d in data]
    data_dict = data[0] if data else {}
    nombre_cliente = data_dict.get("NombreCliente", "Desconocido")
    series_data = []
    yearly_sums = {}

    for year_data in data:
        year = str(year_data["Año"])
        monthly_data = year_data["IngresosMensuales"]

        monthly_values = [
            float(monthly_data.get(mes, "0 €").split(" ")[0].replace(",", "."))
            for mes in MONTHS
        ]
        yearly_sums[year] = round(sum(monthly_values), 2)

    legend_names = [
        f"{year} ({yearly_sums[year]:.2f} €)" for year in years if year in yearly_sums
    ]

    for year in years:
        if year in yearly_sums:
            monthly_values = [
                float(
                    next(y for y in data if str(y["Año"]) == year)["IngresosMensuales"]
                    .get(mes, "0 €")
                    .split(" ")[0]
                    .replace(",", ".")
                )
                for mes in MONTHS
            ]
            series_data.append(
                {
                    "name": f"{year} ({yearly_sums[year]:.2f} €)",
                    "type": "bar",
                    "data": monthly_values,
                    "markPoint": {
                        "symbol": "pin",
                        "data": [
                            {"type": "max", "name": "Max"},
                            {"type": "min", "name": "Min"},
                        ],
                    },
                    "markLine": {
                        "data": [{"type": "average", "name": "Avg"}],
                        "precision": 2,
                    },
                }
            )

    options = {
        "backgroundColor": "#0E1117",
        "title": {
            "text": f"Ganancias Cliente: {nombre_cliente}",
        },
        "tooltip": {"trigger": "axis"},
        "legend": {"data": legend_names},
        "toolbox": {
            "show": True,
            "feature": {
                "dataView": {"show": True, "readOnly": False},
                "magicType": {"show": True, "type": ["line", "bar"]},
            },
        },
        "xAxis": [{"type": "category", "data": MONTHS}],
        "yAxis": [{"type": "value"}],
        "series": series_data,
    }

    display_chart_and_warning(options, key=key)
