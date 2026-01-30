import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat/"

st.title("SATHCHALO Travel Chat")

user_input = st.text_input("Ask about your trip:")

if st.button("Send"):
    if user_input:
        response = requests.post(API_URL, json={"user_input": user_input})
        if response.status_code == 200:
            st.success(response.json()["response"])
        else:
            st.error("API Error!")
