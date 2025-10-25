from google import genai
import streamlit as st

client = genai.Client(api_key="AIzaSyBcI3rMgFb2ShRbCKiS2ypcPeF6jbYoiXs")
prompt = st.chat_input("enter your message:")
if prompt is not None:
    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=prompt
    )
    st.write(response. Text)
