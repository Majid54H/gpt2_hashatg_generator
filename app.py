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
    model_name = "majid54/gpt2_captions_generator"
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
# Category Detection
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
# Hashtags and Emojis
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

# -----------------------------
# Clean Up Captions
# -----------------------------
def is_clean_caption(text):
    if not text or len(text) < 10:
        return False
    bad_patterns = [
        r'http[s]?://', r'#\w+', r'\[.*?\]', r'【.*?】', r'quote=', r'tagline=',
        r'tbtfunkyblogger', r'\u260e', r'\d{4}-\d{2}-\d{2}', r'\.com'
    ]
    for pattern in bad_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F]', text))
    if emoji_count > 3:
        return False
    letter_count = len(re.findall(r'[a-zA-Z]', text))
    total_count = len(text.replace(' ', ''))
    if total_count > 0 and letter_count / total_count < 0.6:
        return False
    return True

def clean_text(text):
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'【.*?】', '', text)
    text = re.sub(r'quote=.*?(?=\s|$)', '', text)
    text = re.sub(r'tagline=.*?(?=\s|$)', '', text)
    text = ' '.join(text.split())
    text = re.sub(r'[,\.\-]+$', '', text)
    return text

# -----------------------------
# Caption Generation
# -----------------------------
def generate_clean_caption(user_input, style='casual'):
    category = detect_category_advanced(user_input)
    clean_prompts = [
        f"{user_input.strip()}. This is amazing",
        f"Today I experienced {user_input.strip()}",
        f"Just finished {user_input.strip()}",
        f"Loving this {user_input.strip()} moment"
    ]
    best_caption = ""
    for prompt in clean_prompts:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            output = model.generate(
                **inputs, max_new_tokens=40, temperature=0.7, top_p=0.8,
                do_sample=True, pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id, repetition_penalty=1.1,
                early_stopping=True
            )
        result = tokenizer.decode(output[0], skip_special_tokens=True)
        raw_caption = result.replace(prompt, "").strip()
        if is_clean_caption(raw_caption):
            best_caption = clean_text(raw_caption)
            break
    if not best_caption or len(best_caption) < 20:
        best_caption = random.choice([
            f"Can't stop thinking about {user_input}.",
            f"Still dreaming of {user_input}.",
            f"{user_input} — unforgettable!",
            f"{user_input} was everything.",
            f"Where do I even begin with {user_input}?"
        ])
    hashtags = get_category_hashtags(category)[:5]
    emojis = get_category_emojis(category)[:2]
    if not best_caption.endswith(('.', '!', '?')):
        best_caption += "!"
    final_caption = f"{' '.join(emojis)} {best_caption}\n\n{' '.join(hashtags)}"
    return final_caption, category

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("\ud83c\udf05 SunsetGram AI")
st.markdown("Generate engaging Instagram captions, hashtags & emojis powered by AI!")

user_input = st.text_input("What is your post about?")
style = st.radio("Choose Style", ["casual", "professional", "funny", "inspirational"])

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Generate Caption ✨") and user_input.strip():
    with st.spinner("Crafting the perfect caption..."):
        caption, category = generate_clean_caption(user_input, style)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.history.insert(0, {
            "input": user_input,
            "caption": caption,
            "style": style,
            "category": category,
            "timestamp": timestamp
        })
        st.markdown("#### ✅ Here's your generated caption:")
        st.markdown(f"""
        <div class='caption-section'>
            <div class='caption-text'>{caption}</div>
            <div style='font-size: 0.9rem; color: #7F8C8D; margin-top: 10px;'>
                <strong>Style:</strong> {style.title()} | <strong>Category:</strong> {category.title()}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.code(caption)

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
            st.code(item["caption"])
