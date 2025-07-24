import streamlit as st
import requests
import os
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_FILE = "model.safetensors"
MODEL_NAME = "gpt2"  # Replace if you're using a different base model

# Google Drive direct download link
model_url = "https://drive.google.com/uc?export=download&id=1c3NtubWnel9Vw7GJB4vygR758I3jb2CW"

# Download the model if not present
def download_model(url):
    if not os.path.exists(MODEL_FILE):
        st.write("📥 Downloading model (~464MB)...")
        response = requests.get(url, stream=True)
        with open(MODEL_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        st.success("✅ Model downloaded!")
    else:
        st.write("✅ Model already exists.")

# UI
st.title("🧠 AI Text Generator")
prompt = st.text_input("Enter a prompt:")

# Download the model file
download_model(model_url)

# Load tokenizer and model
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    return tokenizer, model

tokenizer, model = load_model()

# Generate text
if st.button("🚀 Generate"):
    if prompt:
        st.write("Generating...")
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(**inputs, max_new_tokens=100)
        result = tokenizer.decode(output[0], skip_special_tokens=True)
        st.success("✅ Done!")
        st.write(result)
    else:
        st.warning("⚠️ Please enter a prompt.")
