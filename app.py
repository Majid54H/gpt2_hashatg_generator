import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer
MODEL_NAME = "majid54/gpt2_captions_generator"  # Replace with your Hugging Face model repo
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Streamlit UI
st.set_page_config(page_title="Insta D-Bot", layout="centered")
st.title("📸 Insta D-Bot")
st.markdown("Create AI-generated Instagram posts with style and structure.")

# Input
user_prompt = st.text_area("📝 Enter your topic or idea:", height=150, placeholder="e.g. Self-love, birthday celebration, product launch...")

if st.button("🚀 Generate Post"):
    if not user_prompt.strip():
        st.warning("Please enter a topic or idea first.")
    else:
        # Add clear prompt instruction
        full_prompt = f"Write an Instagram post for the following idea with emojis, hashtags, and a clear post type (funny, informative, lifestyle, or celebration).\n\nIdea: {user_prompt.strip()}\n\nFormat:\nCaption: ...\nHashtags: ...\nEmojis: ...\nPost Type: ..."

        inputs = tokenizer(full_prompt, return_tensors="pt")
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.9,
            top_k=50,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Postprocess: extract only the generated response (remove input part)
        response_cleaned = response.split("Format:")[-1].strip()

        st.markdown("### 🎯 Generated Instagram Post")
        st.code(response_cleaned, language="markdown")
