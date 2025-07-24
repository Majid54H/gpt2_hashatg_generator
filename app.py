import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

st.set_page_config(page_title="Majid’s Caption Generator 🚀")

# Load model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("model/")
    model = AutoModelForCausalLM.from_pretrained("model/", trust_remote_code=True)
    return tokenizer, model

tokenizer, model = load_model()

# Title
st.title("📝 Caption Generator using your AI Model")

# User input
prompt = st.text_area("Enter your prompt to generate caption:", "")

if st.button("Generate Caption"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(**inputs, max_new_tokens=50)
        generated = tokenizer.decode(output[0], skip_special_tokens=True)
        st.success("Here's the generated caption:")
        st.write(generated)
