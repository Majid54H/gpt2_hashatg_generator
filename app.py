import streamlit as st
import requests
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_FILE = "model.safetensors"
MODEL_NAME = "gpt2"
model_url = "https://drive.google.com/uc?export=download&id=1c3NtubWnel9Vw7GJB4vygR758I3jb2CW"

# Page Configuration
st.set_page_config(
    page_title="Caption & Hashtag Generator 🤖",
    page_icon="💬",
    layout="centered",
)

# Header
st.markdown("<h1 style='text-align: center; color: #3D5A80;'>🧠 Smart Caption & Hashtag Bot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Generate Instagram-style captions, #hashtags, and emojis 🎯</p>", unsafe_allow_html=True)
st.markdown("---")

# Model Download
def download_model(url):
    if not os.path.exists(MODEL_FILE):
        with st.spinner("📥 Downloading model (approx 460MB)..."):
            response = requests.get(url, stream=True)
            with open(MODEL_FILE, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        st.success("✅ Model downloaded!")
    else:
        st.info("✅ Model already exists.")

download_model(model_url)

# Load the tokenizer and model
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    return tokenizer, model

tokenizer, model = load_model()

# Prompt Input
prompt = st.text_input("💬 Enter your image description, moment, or thought:")

# Generate Button
if st.button("🚀 Generate Caption + Hashtags"):
    if prompt.strip() == "":
        st.warning("⚠️ Please enter a prompt to generate from.")
    else:
        with st.spinner("🔍 Thinking..."):
            inputs = tokenizer(prompt, return_tensors="pt")
            output = model.generate(**inputs, max_new_tokens=100, do_sample=True, temperature=0.8)
            result = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Styling Output
        st.markdown("### 📝 Generated Post")
        st.success(result)
        st.markdown("---")
        st.info("🔄 You can refine your prompt to get better hashtags, emojis, or themes.")
