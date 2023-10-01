import jwt
import datetime
import streamlit as st
import os

SECRET_KEY = st.secrets.get("SECRET_KEY", os.getenv("SECRET_KEY"))

class TokenManager:
    def __init__(self):
        self.token = None
        self.expiry_time = None

    def get_token(self):
        if self.token is None or datetime.datetime.utcnow() >= self.expiry_time:
            self.token = self.create_jwt()
        return self.token

    def create_jwt(self):
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0)
        self.expiry_time = expiry_time
        payload = {
            'exp': expiry_time,
            'iat': datetime.datetime.utcnow(),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
