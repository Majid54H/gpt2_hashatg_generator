import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load tokenizer and model from Hugging Face
MODEL_REPO = "majid54/gpt2_captions_generator"  # Replace with your Hugging Face repo
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_REPO)
model = GPT2LMHeadModel.from_pretrained(MODEL_REPO)

# Set device
device = torch.device("cpu")
model.to(device)
model.eval()

# Streamlit UI
st.set_page_config(page_title="Hashtag & Emoji Caption Generator", page_icon="✨")

st.title("✨ Social Media Caption Generator")
st.subheader("Generate catchy captions with emojis and hashtags!")

prompt = st.text_area("Enter your idea or topic (e.g. 'A peaceful sunset over the mountains')", height=150)

max_length = st.slider("Max Length", min_value=20, max_value=100, value=50)
temperature = st.slider("Temperature", min_value=0.5, max_value=1.5, value=1.0)

if st.button("Generate Caption"):
    if prompt.strip() == "":
        st.warning("Please enter a topic or idea first.")
    else:
        try:
            inputs = tokenizer(prompt, return_tensors="pt").to(device)

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    eos_token_id=tokenizer.eos_token_id,
                )

            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            generated_text = generated_text.replace(prompt, "").strip()

            st.success("Generated Caption 🎉")
            st.markdown(f"**{generated_text}**")

        except Exception as e:
            st.error(f"🚨 Error: {e}")
