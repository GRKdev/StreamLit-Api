import streamlit as st
import openai
import os
import re
from utils.chart_utils import (
    render_pie_chart_marca,
    render_pie_chart_family,
    render_grouped_bar_chart_fact,
    render_bar_chart_monthly_revenue_monthly_year,
    render_bar_chart_monthly_revenue_client,
    render_bar_chart_monthly_revenue_client_ing,
    render_grouped_bar_chart_ing,
    render_bar_chart_monthly_revenue_monthly_year_ing,
    render_grouped_bar_chart_fact_cli_3_years,
    render_grouped_bar_chart_ing_cli_3_years,
)
import pymongo
from streamlit_feedback import streamlit_feedback


MONGO_URI = st.secrets.get("MONGO_URI", os.getenv("MONGO_URI"))
client = pymongo.MongoClient(MONGO_URI)
db = client["feedback"]
feedback_collection = db["feedback"]


OPEN_AI_MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL"))
model_name_ft = st.secrets["OPENAI_MODEL"].split(":")[3].upper()

OPENAI_MODEL_35 = st.secrets.get("OPENAI_MODEL_35", os.getenv("OPENAI_MODEL_35"))
model_name = st.secrets["OPENAI_MODEL_35"].split(":")[3].upper()

openai.api_base = "https://oai.hconeai.com/v1"
HELICONE_AUTH = st.secrets.get("HELICONE_AUTH", os.getenv("HELICONE_AUTH"))
HELICONE_SESSION = st.secrets.get("HELICONE_SESSION", os.getenv("HELICONE_SESSION"))

last_assistant_response = None


def ask_fine_tuned_api(prompt):
    response = openai.Completion.create(
        engine=OPEN_AI_MODEL,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop="&&",
        temperature=0,
        headers={
            "Helicone-Auth": HELICONE_AUTH,
            "Helicone-Property-Session": HELICONE_SESSION,
        },
    )
    api_response = response.choices[0].text.strip()
    api_response = api_response.strip()

    match = re.search(r"(api/[^ ?]+)(\?.*)?", api_response)

    if match:
        sanitized_response = match.group(0)
    else:
        sanitized_response = api_response
    print(sanitized_response)
    return sanitized_response


def ask_gpt(prompt, placeholder, additional_context=None):
    global last_assistant_response

    messages_list = [
        {
            "role": "system",
            "content": "Eres un conector que proporciona información interna de una DB a los usuarios de la empresa. Eres directo y conciso.",
        },
        {
            "role": "system",
            "content": "Recibirás una pregunta del User junto con datos obtenidos de una base de datos. Debes usar ambas fuentes para ofrecer una respuesta en formato de lista. Proporciona una respuesta clara, coherente y útil. Precios en €",
        },
        {
            "role": "system",
            "content": "Separás los resultados por grupos. No harás una frase de introducción ni una despedida, darás los datos y ya. Nunca sugieras al usuario que realice una compra o venta.",
        },
    ]
    if additional_context:
        previous_response = additional_context.get("previous_response")
        if previous_response:
            messages_list.append(
                {"role": "user", "content": f"User: {previous_response}"}
            )

    messages_list.append({"role": "user", "content": prompt})

    full_response = ""

    for response in openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_list,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0,
        stream=True,
        headers={
            "Helicone-Auth": HELICONE_AUTH,
            "Helicone-Property-Session": HELICONE_SESSION,
        },
    ):
        full_response += response.choices[0].delta.get("content", "")
        placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)

    last_assistant_response = full_response.strip()
    feedback = streamlit_feedback(feedback_type="thumbs")
    feedback

    return last_assistant_response


def ask_gpt_ft(prompt, placeholder, additional_context=None):
    global last_assistant_response
    messages_list = [
        {
            "role": "system",
            "content": "Eres un asistente de la empresa IAND creado por GRKdev. Tienes acceso a datos de clientes y artículos. Recibirás tu respuesta anterior y una pregunta del usuario.",
        },
        {
            "role": "system",
            "content": "Recuerda leer el contexto, Tu respuesta anterior, la pregunta del user y si obtienes 'error' formula una respuesta en base al error y el promp del User. Si el resultado del error es None, ignóralo, si te piden más informació aporta lo que tú también sepas en tu conocimiento.",
        },
    ]
    if last_assistant_response:
        messages_list.append(
            {
                "role": "system",
                "content": f"Assistant last resp: {last_assistant_response}",
            }
        )

    if additional_context:
        api_error = additional_context.get("api_error")
        messages_list.append({"role": "system", "content": f"Error: {api_error}"})

    messages_list.append({"role": "user", "content": prompt})

    full_response = ""

    for response in openai.ChatCompletion.create(
        model=OPENAI_MODEL_35,
        messages=messages_list,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=1,
        stream=True,
        headers={
            "Helicone-Auth": HELICONE_AUTH,
            "Helicone-Property-Session": HELICONE_SESSION,
        },
    ):
        full_response += response.choices[0].delta.get("content", "")
        placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)

    last_assistant_response = full_response.strip()

    return last_assistant_response


def generate_response_from_mongo_results(data):
    if not data:
        return "No se encontraron resultados."
    else:
        return str(data)


def default_handler(data, message_placeholder, user_input):
    json_response = generate_response_from_mongo_results(data)
    additional_context = {
        "previous_response": user_input,
    }
    gpt_response = ask_gpt(
        json_response, message_placeholder, additional_context=additional_context
    )
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
    st.markdown(
        f"<div style='text-align:right; color:green; font-size:small;'>✅ Modelo API: {model_name_ft}. Respuesta elaborada con base de datos y GPT-3.5. Revisa el resultado.</div>",
        unsafe_allow_html=True,
    )


def handle_chat_message(api_response_url, data, message_placeholder, user_input):
    api_to_function_map = {
        "api/alb_stat?fact_total=true": render_grouped_bar_chart_fact,
        "api/alb_stat?fact_cy=true": render_bar_chart_monthly_revenue_monthly_year,
        "api/alb_stat?fact_sy=": render_bar_chart_monthly_revenue_monthly_year,
        "api/alb_stat?cli_fact_cy=": render_bar_chart_monthly_revenue_client,
        "api/alb_stat?cli_ing_cy=": render_bar_chart_monthly_revenue_client_ing,
        "api/alb_stat?ing_total=true": render_grouped_bar_chart_ing,
        "api/alb_stat?ing_cy=true": render_bar_chart_monthly_revenue_monthly_year_ing,
        "api/alb_stat?ing_sy=": render_bar_chart_monthly_revenue_monthly_year_ing,
        "api/art_stat?stat=stat_marca": render_pie_chart_marca,
        "api/art_stat?stat=stat_fam": render_pie_chart_family,
        "api/alb_stat?cli_fact_3=": render_grouped_bar_chart_fact_cli_3_years,
        "api/alb_stat?cli_ing_3=": render_grouped_bar_chart_ing_cli_3_years,
    }

    handler = None
    for pattern, func in api_to_function_map.items():
        if api_response_url.startswith(pattern):
            handler = func
            break

    if handler:
        handler(data)
    else:
        default_handler(data, message_placeholder, user_input)


def handle_gpt_ft_message(
    user_input, message_placeholder, api_response_url, response=None
):
    # json_api = str(response.json())
    additional_context = {
        "api_error": response.json()["error"] if "api/" in api_response_url else None,
    }
    gpt_response = ask_gpt_ft(
        user_input, message_placeholder, additional_context=additional_context
    )
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
    st.markdown(
        f"<div style='text-align:right; color:red; font-size:small;'>⚠️ Modelo: GPT-3.5-{model_name}. Los datos pueden ser erróneos.</div>",
        unsafe_allow_html=True,
    )
