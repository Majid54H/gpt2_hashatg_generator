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
    caption = raw_caption.replace(f"Instagram caption: {user_input.strip()}", "").strip()
    
    # Remove any leftover prompt text and common prefixes
    caption = re.sub(r'^.*?caption:\s*', '', caption, flags=re.IGNORECASE)
    caption = re.sub(r'^.*?for:\s*', '', caption, flags=re.IGNORECASE)
    caption = re.sub(r'^[:\-\s]*', '', caption)
    
    # Remove hashtags from the generated text (we'll add our own)
    caption = re.sub(r'#\w+', '', caption)
    
    # Clean up the caption
    caption = caption.strip()
    
    # Check if we have meaningful caption text (not just hashtags or very short text)
    if not caption or len(caption) < 10 or caption.count('#') > caption.count(' '):
        # Use fallback caption generation
        caption = generate_fallback_caption(user_input, style, category)
    else:
        # Split caption into sentences and take meaningful parts
        sentences = [s.strip() for s in caption.split('.') if s.strip()]
        if sentences:
            main_caption = sentences[0]
            if len(main_caption) < 15 and len(sentences) > 1:
                main_caption = f"{main_caption}. {sentences[1]}"
            caption = main_caption
    
    # Ensure caption doesn't end with incomplete sentence
    if caption and not caption.endswith(('.', '!', '?')):
        if len(caption) > 50:
            caption = caption.rsplit(' ', 1)[0] + "!"
        else:
            caption += "!"
    
    # Get appropriate hashtags and emojis
    hashtags = get_category_hashtags(category)[:6]  # Limit to 6 hashtags
    emojis = get_category_emojis(category)[:2]      # Limit to 2 emojis for cleaner look
    
    # Format the final caption
    formatted_caption = f"{' '.join(emojis)} {caption}\n\n{' '.join(hashtags)}"
    
    return formatted_caption

def generate_fallback_caption(user_input, style, category):
    casual_templates = [
        f"Absolutely loving this {user_input} moment!",
        f"Can't get enough of {user_input} vibes",
        f"This {user_input} just hits different",
        f"Living for these {user_input} moments",
        f"Pure {user_input} bliss right here"
    ]
    
    professional_templates = [
        f"Excited to share this incredible {user_input} experience with you all",
        f"Grateful for moments like these. {user_input} never gets old",
        f"Taking a moment to appreciate the beauty of {user_input}",
        f"Sometimes you just have to stop and enjoy {user_input}",
        f"Sharing some {user_input} inspiration with my community"
    ]
    
    funny_templates = [
        f"When {user_input} becomes your entire personality and you're not even mad about it",
        f"Me: I won't post about {user_input} today. Also me:",
        f"Plot twist: {user_input} was the main character all along",
        f"Breaking news: Local person obsessed with {user_input}",
        f"Is it really {user_input} if you don't post about it?"
    ]
    
    inspirational_templates = [
        f"Every {user_input} reminds me that life is full of beautiful moments",
        f"Find your {user_input} and chase it with everything you've got",
        f"In a world full of chaos, be someone's {user_input}",
        f"The magic happens when you embrace moments like {user_input}",
        f"Life is short, make every {user_input} count"
    ]
    
    templates = {
        "casual": casual_templates,
        "professional": professional_templates,
        "funny": funny_templates,
        "inspirational": inspirational_templates
    }
    
    selected_templates = templates.get(style, casual_templates)
    return random.choice(selected_templates)

# -----------------------------
# Hugging Face Text Generation
# -----------------------------
def generate_clean_caption(user_input, style='casual'):
    try:
        # Try multiple prompt variations for better results
        prompts = [
            f"Write a {style} Instagram caption about {user_input.strip()}:",
            f"Caption: {user_input.strip()}",
            f"{user_input.strip()}"
        ]
        
        best_caption = ""
        category = detect_category_advanced(user_input)
        
        # Try each prompt until we get a good result
        for prompt in prompts:
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device if torch.cuda.is_available() else "cpu")

            with torch.no_grad():
                output = model.generate(
                    **inputs,
                    max_new_tokens=50,
                    temperature=0.8,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.1
                )

            result = tokenizer.decode(output[0], skip_special_tokens=True)
            raw_caption = result.replace(prompt, "").strip()
            
            # Check if this gives us a meaningful caption
            if raw_caption and len(raw_caption) > 10 and not raw_caption.startswith('#'):
                best_caption = raw_caption
                break
        
        # If no good caption from model, use fallback
        if not best_caption or len(best_caption) < 10:
            best_caption = generate_fallback_caption(user_input, style, category)
        
        formatted_caption = clean_and_format_caption(best_caption, user_input, category, style)
        return formatted_caption, category
        
    except Exception as e:
        # Complete fallback
        category = detect_category_advanced(user_input)
        fallback_caption = generate_fallback_caption(user_input, style, category)
        formatted_caption = clean_and_format_caption(fallback_caption, user_input, category, style)
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
            st.info("Generating a custom caption for you...")
            category = detect_category_advanced(user_input)
            fallback_caption = generate_fallback_caption(user_input, style, category)
            formatted_caption = clean_and_format_caption(fallback_caption, user_input, category, style)
            
            # Save fallback to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.history.insert(0, {
                "input": user_input,
                "caption": formatted_caption,
                "style": style,
                "category": category,
                "timestamp": timestamp
            })
            
            st.markdown(f"""
            <div class='caption-section'>
                <div class='caption-text'>{formatted_caption}</div>
                <div style='font-size: 0.9rem; color: #7F8C8D; margin-top: 10px;'>
                    <strong>Style:</strong> {style.title()} | <strong>Category:</strong> {category.title()}
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.code(formatted_caption, language=None)

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
