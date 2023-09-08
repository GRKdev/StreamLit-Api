---
title: Chatbot por GRKdev
---

# Introducción
Este chatbot ha sido desarrollado por GRKdev para abordar las necesidades específicas de manejo de datos en tablas dentro de empresas. Dado que la tecnología de "semantic similarity" actual no aborda de manera efectiva la problemática de los datos tabulares y las casuísticas diversas de cada empresa, se han utilizado técnicas como "Fast-API" y "fine-tuning" específicos. En el futuro, se espera que se puedan desarrollar modelos más avanzados que puedan comprender múltiples tablas y columnas para ofrecer respuestas más precisas.

# Fase 4: Implementación con Streamlit

## Resumen
La Fase 4 del proyecto se centra en la implementación de la interfaz de usuario del chatbot utilizando Streamlit. Este chatbot está diseñado para ofrecer respuestas lo más precisas posible, abordando la falta de precisión en las tecnologías de búsqueda semántica actuales.

## Tecnologías Utilizadas
- **Streamlit**: Para la creación de la interfaz de usuario.
- **ChatGPT 3.5 Turbo**: Para la generación de respuestas en lenguaje natural.
- **Modelo Finetuneado**: Modelo Finetuned ADA de openAI, genera URLs a partir del input del usuario.
- **MongoDB**: Base de datos NoSQL.
- **E-charts**: Biblioteca para generar gráficos.

## Desarrollo del Chatbot

### Doble Motor de Lenguaje
- **Modelo Finetuneado**: Se encarga de generar URLs relevantes a partir del input del usuario, que posteriormente se utilizan para hacer peticiones al servidor API.
- **ChatGPT 3.5 Turbo**: Genera respuestas finales en lenguaje natural, basadas en la información obtenida desde la base de datos MongoDB.

### Peticiones y Respuestas
Una vez que el usuario envía una consulta:
1. El modelo finetuneado genera una URL.
2. Se realiza una petición al servidor API utilizando esta URL.
3. El servidor devuelve datos desde una tabla NoSQL de MongoDB.
4. ChatGPT 3.5 Turbo genera una respuesta en lenguaje natural basada en estos datos.

### Contexto de Conversación
- El chatbot guarda el contexto de la respuesta anterior para ofrecer una experiencia conversacional más fluida.

## Funciones Estadísticas
- Cuando el input del usuario activa funciones estadísticas, se utiliza la biblioteca E-charts para generar un gráfico que se muestra directamente en la interfaz del chatbot.

## Pestaña de Estadísticas
- En una segunda pestaña se presentan estadísticas con consultas más típicas a la base de datos.
- Se generan gráficos a partir de una petición a la base de datos a través de la API predeterminada, sin utilizar la respuesta de la IA.

## Roadmap

- Mejorar la precisión en la generación de respuestas
- Implementar una mejor comprensión de tablas y columnas para futuras versiones.
- Reducir los casos de "alucinaciones" en las respuestas del modelo.
