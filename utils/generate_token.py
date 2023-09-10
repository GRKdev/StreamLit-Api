import jwt
import datetime
import streamlit as st
import os

SECRET_KEY = st.secrets.get("SECRET_KEY", os.getenv("SECRET_KEY"))

def create_jwt():
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
        'iat': datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

token = create_jwt()
