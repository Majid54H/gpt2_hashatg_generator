import streamlit as st
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import random
import re

# -----------------------------
# Load Hugging Face Model
# -----------------------------
@st.cache_resource
def load_hf_model():
    model_name = "thicchamz/gpt2_finetune_instagram_caption_generator"  # Replace if needed
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_hf_model()

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.set_page_config(page_title="SunsetGram", layout="wide")
st.markdown("""
<style>
body {
    background-color: #FAF3E0;
}
h1 {
    color: #FF6F61;
}
.generated-text {
    font-size: 1.3rem;
    color: #333333;
    background-color: #FFF8F0;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 20px;
}
.caption-header {
    font-weight: bold;
    font-size: 1.5rem;
    color: #FF6F61;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helper: Detect Category
# -----------------------------
def detect_category_advanced(user_input):
    keywords = {
        "travel": ["beach", "trip", "adventure", "sunset", "mountains", "journey"],
        "fashion": ["outfit", "style", "clothes", "look", "OOTD"],
        "food": ["delicious", "tasty", "recipe", "food", "meal", "dinner", "lunch", "breakfast"],
        "fitness": ["gym", "workout", "fit", "exercise", "health"],
        "motivational": ["dream", "goal", "inspire", "motivation", "success"],
    }

    user_input_lower = user_input.lower()
    for category, words in keywords.items():
        if any(word in user_input_lower for word in words):
            return category
    return "general"

# -----------------------------
# Hugging Face Text Generation
# -----------------------------
def generate_clean_caption(user_input, style='casual'):
    prompt = f"Generate an Instagram caption with emojis and hashtags in a {style} style for: {user_input.strip()}"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device if torch.cuda.is_available() else "cpu")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=80,
            temperature=0.8,
            top_p=0.95,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )

    result = tokenizer.decode(output[0], skip_special_tokens=True)
    caption = result.split(prompt)[-1].strip()
    category = detect_category_advanced(user_input)
    return caption, category

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🌅 SunsetGram AI")
st.markdown("Generate engaging Instagram captions, hashtags & emojis powered by AI!")

user_input = st.text_input("What is your post about? (e.g., sunset at beach, morning coffee, gym selfie)")
style = st.radio("Choose Style", ["casual", "professional", "funny", "inspirational"])
temperature = st.slider("Creativity Level (Temperature)", 0.2, 1.2, 0.8)

generate_button = st.button("Generate Caption ✨")

if "history" not in st.session_state:
    st.session_state.history = []

if generate_button and user_input.strip() != "":
    with st.spinner("Crafting the perfect caption..."):
        try:
            caption, category = generate_clean_caption(user_input, style)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save to history
            st.session_state.history.insert(0, {
                "input": user_input,
                "caption": caption,
                "style": style,
                "category": category,
                "timestamp": timestamp
            })

            st.markdown("#### ✅ Here's your generated caption:")
            st.markdown(f"<div class='generated-text'>{caption}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

# -----------------------------
# History Section
# -----------------------------
if st.session_state.history:
    st.markdown("## 🕒 Your Recent Captions")
    for item in st.session_state.history[:5]:
        st.markdown(f"""
        <div class='generated-text'>
        <div class='caption-header'>{item["input"]}</div>
        <div><strong>Style:</strong> {item["style"]} | <strong>Category:</strong> {item["category"]}</div>
        <div style='margin-top: 10px;'>{item["caption"]}</div>
        <div style='font-size: 0.8rem; color: #888;'>Generated on {item["timestamp"]}</div>
        </div>
        """, unsafe_allow_html=True)
