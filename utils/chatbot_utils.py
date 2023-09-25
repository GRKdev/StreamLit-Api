import streamlit as st
import openai
import os
import re
from utils.chart_utils import (
    render_pie_chart_marca, render_pie_chart_family,render_grouped_bar_chart_fact,
    render_bar_chart_monthly_revenue_monthly_year, render_bar_chart_monthly_revenue_client,
    render_bar_chart_monthly_revenue_client_ing, render_grouped_bar_chart_ing,
    render_bar_chart_monthly_revenue_monthly_year_ing, render_grouped_bar_chart_fact_cli_3_years,
    render_grouped_bar_chart_ing_cli_3_years
    )

secret_key_ft = st.secrets["OPENAI_MODEL"]
model_name_ft = ":".join(secret_key_ft.split(":")[1:4])
secret_key = st.secrets["OPENAI_MODEL_35"]
model_name = ":".join(secret_key.split(":")[1:4])
OPEN_AI_MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL"))
OPENAI_MODEL_35 = st.secrets.get("OPENAI_MODEL_35", os.getenv("OPENAI_MODEL_35"))
openai.api_base = "https://oai.hconeai.com/v1"
HELICONE_AUTH = st.secrets.get("HELICONE_AUTH", os.getenv("HELICONE_AUTH"))
HELICONE_SESSION = st.secrets.get("HELICONE_SESSION", os.getenv("HELICONE_SESSION"))



last_assistant_response = None

def ask_fine_tuned_ada(prompt):
    response = openai.Completion.create(
        engine=OPEN_AI_MODEL,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop="&&",
        temperature=0,
        headers={
        "Helicone-Auth": HELICONE_AUTH,
        "Helicone-Property-Session": HELICONE_SESSION
      }
    )
    api_response = response.choices[0].text.strip()
    api_response = api_response.strip()

    match = re.search(r'(api/[^ ?]+)(\?.*)?', api_response)

    if match:
        sanitized_response = match.group(0)
    else:
        sanitized_response = api_response

    return sanitized_response

def ask_gpt(prompt, placeholder, additional_context=None):
    global last_assistant_response
    messages_list = [
            {
            "role": "system",
            "content": "Recibirás preguntas del usuario junto con datos obtenidos de una base de datos. Debes usar ambas fuentes para ofrecer una respuesta en formato de lista. Proporciona una respuesta clara, coherente y útil. Asegúrate de presentar la información de forma amena y fácil de entender para el usuario. Cuando manejes cifras monetarias, hazlo así 40 €. No ofrezcas vender o comprar los artículos."
            }
    ]
    if last_assistant_response:
        messages_list.append({"role": "assistant", "content": f"Assistant last response: {last_assistant_response}"})

    if additional_context:
        fine_tuned_result = additional_context.get("fine_tuned_result")
        if fine_tuned_result:
            messages_list.append({"role": "assistant", "content": f"Result fine_tuned: {fine_tuned_result}"})
            
        previous_response = additional_context.get("previous_response")
        if previous_response:
            messages_list.append({"role": "user", "content": f"User previous response: {previous_response}"})

        api_error = additional_context.get("api_error")
        if api_error:
            messages_list.append({"role": "system", "content": f"Error: {api_error}"})

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
        "Helicone-Property-Session": HELICONE_SESSION
      }        
    ):
        full_response += response.choices[0].delta.get("content", "")
        placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)
    
    last_assistant_response = full_response.strip()

    return last_assistant_response


def ask_gpt_ft(prompt, placeholder, additional_context=None):
    global last_assistant_response
    messages_list = [
            {
            "role": "system",
            "content": "Eres un asistente de la empresa GRK Tech. ¡NO INVENTES INFORMACIÓN QUE DESCONOCES! Recibirás preguntas del usuario junto con datos obtenidos de una base de datos y del contexto. Si no sabes los resultados, dirás que no tienes información"
            }
    ]
    if last_assistant_response:
        messages_list.append({"role": "assistant", "content": f"Assistant last response: {last_assistant_response}"})

    if additional_context:          
        previous_response = additional_context.get("previous_response")
        if previous_response:
            messages_list.append({"role": "user", "content": f"User previous response: {previous_response}"})

        api_error = additional_context.get("api_error")
        if api_error:
            messages_list.append({"role": "system", "content": f"Error: {api_error}"})

    messages_list.append({"role": "user", "content": prompt})

    full_response = ""
    
    for response in openai.ChatCompletion.create(
        model=OPENAI_MODEL_35,
        messages=messages_list,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.1,
        stream=True,
        headers={
        "Helicone-Auth": HELICONE_AUTH,
        "Helicone-Property-Session": HELICONE_SESSION
      }        
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
        "fine_tuned_result": None
    }
    gpt_response = ask_gpt(json_response, message_placeholder, additional_context=additional_context)
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
    st.markdown(f"<div style='text-align:right; color:green; font-style:italic; font-size:small;'>⚠ Has utilizado el modelo {model_name_ft}. Respuesta elaborada con datos DB y GPT-3.5. Revisa el resultado. ⚠</div>", unsafe_allow_html=True)

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
        "api/alb_stat?cli_ing_3=": render_grouped_bar_chart_ing_cli_3_years
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


def handle_gpt_ft_message(user_input, message_placeholder, api_response_url, response=None):
    additional_context = {
        "previous_response": user_input,
        "fine_tuned_result": api_response_url if 'api/' not in api_response_url else None,
        "api_error": response.json() if 'api/' in api_response_url else None,
    }

    print(additional_context)
    gpt_response = ask_gpt_ft(user_input, message_placeholder, additional_context=additional_context)
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
    st.markdown(f"<div style='text-align:right; color:red; font-style:italic; font-size:small;'>⚠ Has utilizado el modelo: {model_name}. Los datos pueden ser erróneos. ⚠</div>", unsafe_allow_html=True)
