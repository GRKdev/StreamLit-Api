<p align="center">
<img src="https://img.shields.io/github/last-commit/GRKdev/StreamLit-Api" alt="GitHub last commit" />
<img src="https://img.shields.io/github/commit-activity/m/GRKdev/StreamLit-Api" alt="GitHub commit activity month" />
</p>

# ChatBot Streamlit API NOSQL

Desarrollé un Chatbot avanzado que promueve la interacción en tiempo real y en lenguaje natural con una base de datos MongoDB, facilitando el acceso a información crucial como datos de clientes, artículos, albaranes y métricas financieras. Este proyecto resalta la integración eficaz de modelos de lenguaje con datos tabulares, empleando un modelo afinado para ejecutar consultas API y proporcionar respuestas precisas mediante GPT-3.5-Turbo de OpenAI, abordando así desafíos significativos en el campo de la Inteligencia Artificial.

## Tecnologías

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Streamlit-Echarts](https://github.com/andfanilo/streamlit-echarts)
- [Helicone](https://helicone.ai/)
- [Lakera](https://lakera.ai/)


## Roadmap

- [x] [Script para la preparación de datos](https://github.com/GRKdev/Script-SQL-API): Script para la preparación del entrenamiento.
- [x] [Script para la conexión y fine-tuning automático (nuevo API de OpenAI)](https://github.com/GRKdev/Script-SQL-API): Script para la conexión a OpenAI y fine-tuning automático.
- [x] [Flask API](https://github.com/GRKdev/api-docker-ngrok): API para la conexión con la base de datos MongoDB.
- [x] [Chatbot StreamLit](https://github.com/GRKdev/StreamLit-Api): Chatbot para la interacción con el usuario.
- [x] Respuestas con gràficas: Gràficas de barras, líneas, radar, etc. Streamlit-Echarts.
- [x] Contexto última pregunta/respuesta, y errores de api.
- [x] Respuesta de GPT-3.5 Turbo Finetuned para respuestas sin resultados de la base de datos
- [x] Feedback de las respuestas del chatbot con Helicone.
- [x] Lakera Guard para mensajes de prompt injection y mensajes de odio/sexual.
- [ ] Datos con embeddings (Langchain/Llama-Index) para chatear con los documentos.
- [ ] Creación de Agentes y Functiones personalizadas.

## Contributors
<a href="https://github.com/GRKdev/StreamLit-Api/graphs/contributors">
<img src="https://contrib.rocks/image?repo=GRKdev/StreamLit-Api" />
</a>

## 📄 License

This project is licensed under the **MIT License** - see the [**MIT License**](https://github.com/GRKdev/StreamLit-Api/blob/main/LICENSE) file for details.

---

# ChatBot Streamlit API NOSQL

Creation of the chatbot using Streamlit. The user asks questions, and the chatbot with the fine-tuning model returns a response via a request to the API URL. Additionally, the chatbot has quick access to view statistics directly connected to the database through the API. Successful results will be returned to GPT-3.5 Turbo to generate a response. If there are no successful results, or it is a general question, a GPT-3.5 Finetuned model will be used to generate the response.

## Technologies

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Streamlit-Echarts](https://github.com/andfanilo/streamlit-echarts)
- [Helicone](https://helicone.ai/)
- [Lakera](https://lakera.ai/)

## Roadmap

- [x] [Script for data preparation](https://github.com/GRKdev/Script-SQL-API): Script for training preparation.
- [x] [Script for automatic connection and fine-tuning (new OpenAI API)](https://github.com/GRKdev/Script-SQL-API): Script for connection to OpenAI and automatic fine-tuning.
- [x] [Flask API](https://github.com/GRKdev/api-docker-ngrok): API for connection to MongoDB database.
- [x] [StreamLit Chatbot](https://github.com/GRKdev/StreamLit-Api): Chatbot for user interaction.
- [x] Responses with graphs: Bar, line, radar, etc. Streamlit-Echarts.
- [x] Last question/answer context, and API errors
- [x] GPT-3.5 Turbo Finetuned response for answers without database results
- [x] Feedback for chatbot responses (Helicone)
- [x] Lakera Guard for prompt injection messages and hate/sexual messages
- [ ] Data with embeddings (Langchain/Llama-Index) for chatting with documents
- [ ] Creation of Agents and Custom Functions
