import streamlit as st
import requests
import os
from transformers import pipeline
from safetensors.torch import load_file

MODEL_FILE = "model.safetensors"

# Function to download the model from Google Drive
def download_model(url):
    if not os.path.exists(MODEL_FILE):
        st.write("📥 Downloading model...")
        response = requests.get(url)
        with open(MODEL_FILE, "wb") as f:
            f.write(response.content)
        st.success("✅ Model downloaded!")
    else:
        st.write("✅ Model already exists.")

# Streamlit UI
st.title("🧠 AI Text Generator App")
st.write("Enter a prompt to generate text using your finetuned model:")

# Input
prompt = st.text_input("🔤 Enter prompt here")

# Model download link (Google Drive direct download URL)
model_url = "YOUR_DIRECT_LINK_HERE"

# Download and load the model
download_model(model_url)

# Load pipeline (Assuming GPT-2 or similar architecture)
pipe = pipeline("text-generation", model=MODEL_FILE)

# Generate
if st.button("🚀 Generate"):
    if prompt:
        with st.spinner("Generating..."):
            result = pipe(prompt, max_new_tokens=100)
            st.success("✅ Done!")
            st.write(result[0]['generated_text'])
    else:
        st.warning("⚠️ Please enter a prompt!")
