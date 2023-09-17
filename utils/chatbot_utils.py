import streamlit as st
import openai
import os


from utils.chart_utils import (
    render_pie_chart_marca, render_pie_chart_family,render_grouped_bar_chart_fact,
    render_bar_chart_monthly_revenue_monthly_year, render_bar_chart_monthly_revenue_client,
    render_bar_chart_monthly_revenue_client_ing, render_grouped_bar_chart_ing,
    render_bar_chart_monthly_revenue_monthly_year_ing, render_grouped_bar_chart_fact_cli_3_years,
    render_grouped_bar_chart_ing_cli_3_years
    )

last_assistant_response = None

def ask_gpt(prompt, placeholder, additional_context=None):
    global last_assistant_response
    messages_list = [
            {
            "role": "system",
            "content": "Recibirás preguntas del usuario junto con datos obtenidos de una base de datos. Debes usar ambas fuentes para ofrecer una respuesta clara, coherente y útil en formato lista. Si no conoces la respuesta, indícalo. Asegúrate de presentar la información de forma amena y fácil de entender para el usuario. Si el JSON contiene múltiples elementos, resume la información de forma concisa. Cuando manejes cifras monetarias, añade el símbolo €."
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
    ):
        full_response += response.choices[0].delta.get("content", "")
        placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)
    
    last_assistant_response = full_response.strip()

    return last_assistant_response


def ask_gpt_ft(prompt, placeholder, additional_context=None):
    OPENAI_MODEL_35 = st.secrets.get("OPENAI_MODEL_35", os.getenv("OPENAI_MODEL_35"))
    global last_assistant_response
    messages_list = [
            {
            "role": "system",
            "content": "Eres un asistente de la empresa GRK Tech. ¡NO INVENTES INFORMACIÓN QUE DESCONOCES! Recibirás preguntas del usuario junto con datos obtenidos de una base de datos, o del contexto. Si no sabes los resultados, dirás que no tienes información"
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
        temperature=0.5,
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
        placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)
    
    last_assistant_response = full_response.strip()

    return last_assistant_response




def default_handler(data, message_placeholder, user_input):
    st.markdown("<span style='color:green; font-style:italic; font-size:small;'>⚠ chatbot Fine-Tuned</span>", unsafe_allow_html=True)
    json_response = generate_response_from_mongo_results(data)
    additional_context = {
        "previous_response": user_input,
        "fine_tuned_result": None
    }
    gpt_response = ask_gpt(json_response, message_placeholder, additional_context=additional_context)
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})


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
        
def generate_response_from_mongo_results(data):
    print(f"data: {data}") 
    if not data:
        return "No se encontraron resultados."
    else:
        return str(data)