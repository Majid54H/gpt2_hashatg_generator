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
    model_name = "majid54/gpt2_captions_generator"  # Replace if needed
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
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 20px;
    border-left: 5px solid #FF6F61;
}
.caption-section {
    background-color: #FFFFFF;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.caption-text {
    font-size: 1.2rem;
    color: #2C3E50;
    line-height: 1.6;
    margin-bottom: 10px;
}
.hashtags {
    color: #3498DB;
    font-weight: 500;
}
.emojis {
    font-size: 1.4rem;
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
        "travel": ["beach", "trip", "adventure", "sunset", "mountains", "journey", "vacation", "explore"],
        "fashion": ["outfit", "style", "clothes", "look", "OOTD", "fashion", "dress", "shoes"],
        "food": ["delicious", "tasty", "recipe", "food", "meal", "dinner", "lunch", "breakfast", "cooking"],
        "fitness": ["gym", "workout", "fit", "exercise", "health", "training", "muscle"],
        "motivational": ["dream", "goal", "inspire", "motivation", "success", "achieve", "believe"],
        "lifestyle": ["morning", "coffee", "relax", "home", "weekend", "selfie", "life"]
    }

    user_input_lower = user_input.lower()
    for category, words in keywords.items():
        if any(word in user_input_lower for word in words):
            return category
    return "general"

# -----------------------------
# Caption Enhancement Functions
# -----------------------------
def get_category_hashtags(category):
    hashtag_dict = {
        "travel": ["#travel", "#wanderlust", "#adventure", "#explore", "#vacation", "#journey", "#travelphotography"],
        "fashion": ["#fashion", "#style", "#OOTD", "#fashionista", "#outfit", "#trendy", "#styleinspo"],
        "food": ["#foodie", "#delicious", "#yummy", "#foodstagram", "#instafood", "#tasty", "#foodlover"],
        "fitness": ["#fitness", "#gym", "#workout", "#health", "#fitlife", "#exercise", "#strong"],
        "motivational": ["#motivation", "#inspiration", "#goals", "#success", "#mindset", "#positivity", "#believe"],
        "lifestyle": ["#lifestyle", "#life", "#mood", "#vibes", "#daily", "#moment", "#selfcare"],
        "general": ["#instagood", "#photooftheday", "#love", "#happy", "#beautiful", "#amazing", "#life"]
    }
    return hashtag_dict.get(category, hashtag_dict["general"])

def get_category_emojis(category):
    emoji_dict = {
        "travel": ["✈️", "🌍", "📸", "🗺️", "🏖️", "⛰️", "🌅"],
        "fashion": ["👗", "👠", "💄", "✨", "👜", "🕶️", "💫"],
        "food": ["🍽️", "😋", "🔥", "👨‍🍳", "🍴", "❤️", "🤤"],
        "fitness": ["💪", "🏋️‍♀️", "🔥", "💯", "⚡", "🏃‍♀️", "💦"],
        "motivational": ["💪", "🌟", "✨", "🔥", "💯", "🚀", "⭐"],
        "lifestyle": ["☕", "💕", "✨", "🌸", "😊", "🌞", "💫"],
        "general": ["❤️", "✨", "😊", "📸", "💕", "🌟", "😍"]
    }
    return emoji_dict.get(category, emoji_dict["general"])

def clean_and_format_caption(raw_caption, user_input, category, style):
    # Remove the original prompt from the output
    caption = raw_caption.replace(f"Generate an Instagram caption with emojis and hashtags in a {style} style for: {user_input.strip()}", "").strip()
    
    # Remove any leftover prompt text
    caption = re.sub(r'^.*?for:\s*', '', caption, flags=re.IGNORECASE)
    caption = re.sub(r'^.*?caption:\s*', '', caption, flags=re.IGNORECASE)
    
    # Clean up the caption
    caption = caption.strip()
    if not caption:
        # Fallback caption generation
        caption = generate_fallback_caption(user_input, style)
    
    # Split caption into sentences and take the first meaningful part
    sentences = caption.split('.')
    main_caption = sentences[0].strip()
    if len(main_caption) < 10 and len(sentences) > 1:
        main_caption = f"{main_caption}. {sentences[1].strip()}"
    
    # Get appropriate hashtags and emojis
    hashtags = get_category_hashtags(category)[:5]  # Limit to 5 hashtags
    emojis = get_category_emojis(category)[:3]      # Limit to 3 emojis
    
    # Format the final caption
    formatted_caption = f"{' '.join(emojis)} {main_caption}\n\n{' '.join(hashtags)}"
    
    return formatted_caption

def generate_fallback_caption(user_input, style):
    fallback_templates = {
        "casual": f"Just loving this moment! {user_input} hits different ✨",
        "professional": f"Excited to share this with you all. {user_input} represents something special.",
        "funny": f"When {user_input} becomes your whole personality 😂",
        "inspirational": f"Every moment like this reminds me why {user_input} matters. Keep chasing your dreams!"
    }
    return fallback_templates.get(style, f"Amazing {user_input} moment!")

# -----------------------------
# Hugging Face Text Generation
# -----------------------------
def generate_clean_caption(user_input, style='casual'):
    # Simplified prompt for better results
    prompt = f"Instagram caption: {user_input.strip()}"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device if torch.cuda.is_available() else "cpu")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=60,  # Reduced for cleaner output
            temperature=0.7,    # Slightly lower for more coherent text
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    result = tokenizer.decode(output[0], skip_special_tokens=True)
    raw_caption = result.replace(prompt, "").strip()
    
    category = detect_category_advanced(user_input)
    formatted_caption = clean_and_format_caption(raw_caption, user_input, category, style)
    
    return formatted_caption, category

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🌅 SunsetGram AI")
st.markdown("Generate engaging Instagram captions, hashtags & emojis powered by AI!")

user_input = st.text_input("What is your post about? (e.g., sunset at beach, morning coffee, gym selfie)")
style = st.radio("Choose Style", ["casual", "professional", "funny", "inspirational"])

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

            # Display the formatted caption
            st.markdown("#### ✅ Here's your generated caption:")
            st.markdown(f"""
            <div class='caption-section'>
                <div class='caption-text'>{caption}</div>
                <div style='font-size: 0.9rem; color: #7F8C8D; margin-top: 10px;'>
                    <strong>Style:</strong> {style.title()} | <strong>Category:</strong> {category.title()}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Copy button functionality
            st.code(caption, language=None)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            # Show fallback option
            st.info("Generating a fallback caption...")
            category = detect_category_advanced(user_input)
            fallback_caption = clean_and_format_caption("", user_input, category, style)
            st.markdown(f"<div class='generated-text'>{fallback_caption}</div>", unsafe_allow_html=True)

# -----------------------------
# History Section
# -----------------------------
if st.session_state.history:
    st.markdown("## 🕒 Your Recent Captions")
    for i, item in enumerate(st.session_state.history[:5]):
        with st.expander(f"📝 {item['input'][:50]}{'...' if len(item['input']) > 50 else ''}", expanded=(i==0)):
            st.markdown(f"""
            <div class='caption-section'>
                <div><strong>Original Input:</strong> {item["input"]}</div>
                <div><strong>Style:</strong> {item["style"]} | <strong>Category:</strong> {item["category"]}</div>
                <div style='margin-top: 15px;'><strong>Generated Caption:</strong></div>
                <div class='caption-text'>{item["caption"]}</div>
                <div style='font-size: 0.8rem; color: #888; margin-top: 10px;'>Generated on {item["timestamp"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Copy button for each caption
            st.code(item["caption"], language=None)
