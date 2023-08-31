# ChatBot Streamlit API NOSQL

## Descripción General

Este proyecto es un ChatBot implementado en varias fases con el objetivo de crear un sistema conversacional eficiente y funcional. Se utiliza el modelo GPT-3.5 Turbo de OpenAI para generar respuestas y está construido sobre una arquitectura de API NOSQL.

## Fases del Proyecto

### Fase 1: Preparación de Datos
Creación de un script para crear dos archivos JSNL (train y valid) con el objetivo de entrenar un modelo de fine-tuning con OpenAI que devuelva respuestas mediante una URL API.

### Fase 2: Entrenamiento del Modelo
Entrenamiento del modelo de fine-tuning con OpenAI.

### Fase 3: Creación de la API con Flask
Desarrollo de una API utilizando Flask. Configuraciones de las rutas y funciones de cada ruta personalizada. Se implementa una conexión a una base de datos NoSQL de MongoDB.

### **Fase 4: Implementación con Streamlit**
Creación del chatbot utilizando Streamlit. El chatbot hace preguntas, y el modelo de fine-tuning devuelve una respuesta mediante una petición a la URL API. Además, el chatbot tiene accesos rápidos para ver estadísticas directamente conectadas a la base de datos a través de la API.

## Roadmap

- [x] Script para la preparación de datos
- [ ] Script para la conexión y fine-tuning automático
- [x] Flask API
- [x] Chatbot StreamLit
- [ ] Añadir contexto
- [ ] Añadir datos de la empresa (procedimientos) para chatear con los conocimientos.
