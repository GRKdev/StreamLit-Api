<p align="center">
<img src="https://img.shields.io/github/last-commit/GRKdev/StreamLit-Api" alt="GitHub last commit" />
<img src="https://img.shields.io/github/commit-activity/m/GRKdev/StreamLit-Api" alt="GitHub commit activity month" />
</p>

# ChatBot Streamlit API NOSQL

## Descripción General

Este proyecto es un ChatBot implementado en varias fases con el objetivo de crear un sistema conversacional eficiente y funcional. Se utiliza el modelo GPT-3.5 Turbo de OpenAI para generar respuestas y está construido sobre una arquitectura de API NOSQL.

## Fases del Proyecto

### Fase 1: Preparación de Datos
Creación de un script para crear dos archivos JSONL (train y valid) con el objetivo de entrenar un modelo de fine-tuning con OpenAI que devuelva respuestas mediante una URL API.
El proyecto para esta fase se encuentra en [este repositorio de GitHub](https://github.com/GRKdev/Script-SQL-API).

### Fase 2: Entrenamiento del Modelo
Entrenamiento del modelo de fine-tuning con OpenAI.

### Fase 3: Creación de la API con Flask
Desarrollo de una API utilizando Flask. Configuraciones de las rutas y funciones de cada ruta personalizada. Se implementa una conexión a una base de datos NoSQL de MongoDB. Actualmente subido como contenedor Docker en un synology DS224+. Agregado tunel del puerto local a Ngrok. [URL API](https://github.com/GRKdev/api-docker-ngrok).

## **Fase 4: Implementación con Streamlit**
Creación del chatbot utilizando Streamlit. El usuario hace preguntas, y el chatbot con el modelo de fine-tuning devuelve una respuesta mediante una petición a la URL API. Además, el chatbot tiene accesos rápidos para ver estadísticas directamente conectadas a la base de datos a través de la API. Los resultados exitosos serán devueltos a GPT-3.5 Turbo para generar una respuesta. Si no hay resultados exitoso, o es una pregunta general, se utilizará un modelo GPT-3.5 Finetuneado para generar la respuesta.

## Roadmap

- [x] [Script para la preparación de datos](https://github.com/GRKdev/Script-SQL-API)
- [x] [Script para la conexión y fine-tuning automático (nuevo API de OpenAI)](https://github.com/GRKdev/Script-SQL-API)
- [x] [Flask API](https://github.com/GRKdev/api-docker-ngrok)
- [x] [Chatbot StreamLit](https://github.com/GRKdev/StreamLit-Api)
- [x] Añadido respuestas con gràficas
- [x] Añadido contexto última pregunta/respuesta, y errores de api
- [x] Añadadido Respuesta de GPT-3.5 Turbo Finetuned para respuestas sin resultados de la base de datos
- [ ] Añadir Feedback de las respuestas del chatbot
- [ ] Datos con embeddings (Langchain/Llama-Index) para chatear con los documentos
- [ ] Creación de Agentes y Functiones personalizadas

## Contributors
<a href="https://github.com/GRKdev/StreamLit-Api/graphs/contributors">
<img src="https://contrib.rocks/image?repo=GRKdev/StreamLit-Api" />
</a>

## 📄 License

This project is licensed under the **MIT License** - see the [**MIT License**](https://github.com/GRKdev/StreamLit-Api/blob/main/LICENSE) file for details.

---

# ChatBot Streamlit API NOSQL

## General Description

This project is a ChatBot implemented in various phases with the aim of creating an efficient and functional conversational system. It uses OpenAI's GPT-3.5 Turbo model to generate responses and is built on a NOSQL API architecture.

## Project Phases

### Phase 1: Data Preparation
Creation of a script to create two JSONL files (train and valid) with the aim of training a fine-tuning model with OpenAI that returns responses via a URL API.
The project for this phase can be found in [this GitHub repository](https://github.com/GRKdev/Script-SQL-API).

### Phase 2: Model Training
Training of the fine-tuning model with OpenAI.

### Phase 3: API Creation with Flask
Development of an API using Flask. Configuration of routes and functions for each custom route. A connection to a MongoDB NoSQL database is implemented. [API URL](https://github.com/GRKdev/api-docker-ngrok).

## **Phase 4: Implementation with Streamlit**
Creation of the chatbot using Streamlit. The user asks questions, and the chatbot with the fine-tuning model returns a response via a request to the API URL. Additionally, the chatbot has quick access to view statistics directly connected to the database through the API. Successful results will be returned to GPT-3.5 Turbo to generate a response. If there are no successful results, or it is a general question, a GPT-3.5 Finetuned model will be used to generate the response.

## Roadmap

- [x] [Script for data preparation](https://github.com/GRKdev/Script-SQL-API)
- [x] [Script for automatic connection and fine-tuning (new OpenAI API)](https://github.com/GRKdev/Script-SQL-API)
- [x] [Flask API](https://github.com/GRKdev/api-docker-ngrok)
- [x] [StreamLit Chatbot](https://github.com/GRKdev/StreamLit-Api)
- [x] Added responses with graphs
- [x] Added last question/answer context, and API errors
- [x] Added GPT-3.5 Turbo Finetuned response for answers without database results
- [x] Add Feedback for chatbot responses (Helicone)
- [ ] Data with embeddings (Langchain/Llama-Index) for chatting with documents
- [ ] Creation of Agents and Custom Functions
