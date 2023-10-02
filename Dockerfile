FROM python:3.11-slim-buster

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "your_app.py"]
