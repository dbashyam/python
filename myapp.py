import os
import streamlit as st
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="nebius",
    api_key="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",
)

prompt = st.chat_input("Enter your chat input:")

if prompt is not None:
    # output is a PIL.Image object
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev",
    )

    st.image(image)