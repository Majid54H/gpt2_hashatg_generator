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
    # Ensure we have clean caption text
    caption = raw_caption.strip()
    
    # If caption is still messy or too short, use fallback
    if not caption or len(caption) < 20 or not is_clean_caption(caption):
        caption = generate_fallback_caption(user_input, style, category)
    
    # Final cleaning
    caption = clean_text(caption)
    
    # Make sure caption ends properly
    if caption and not caption.endswith(('.', '!', '?')):
        caption += "!"
    
    # Get clean hashtags and emojis
    hashtags = get_category_hashtags(category)[:5]  # Limit to 5 clean hashtags
    emojis = get_category_emojis(category)[:2]      # Limit to 2 emojis
    
    # Format with clear structure
    formatted_caption = f"{' '.join(emojis)} {caption}\n\n{' '.join(hashtags)}"
    
    return formatted_caption

def generate_fallback_caption(user_input, style, category):
    # More detailed, engaging templates like your example
    casual_templates = [
        f"Lost in the magic of {user_input}. There's something about moments like these that just makes everything feel right. The energy is absolutely contagious and I can't get enough of it. What's your favorite part about {user_input}?",
        f"Completely mesmerized by {user_input} today. Every detail catches my eye and I find myself getting lost in the experience. The vibes here are unmatched. Who else is obsessed with {user_input}?",
        f"Can't believe how incredible {user_input} is! The atmosphere is so alive and vibrant, I could spend hours just soaking it all in. Every moment feels like a new discovery. What draws you to {user_input}?",
        f"Falling in love with {user_input} all over again. There's this raw energy that just pulls you in and doesn't let go. I'm discovering new things every time I experience this. Tell me about your {user_input} story!",
        f"Absolutely captivated by the beauty of {user_input}. The way everything comes together creates this perfect moment that I never want to end. I could explore this forever. What's your go-to {user_input} spot?"
    ]
    
    professional_templates = [
        f"Reflecting on the incredible experience of {user_input}. The depth and richness of every moment continues to inspire me in ways I never expected. There's so much beauty in the details that often go unnoticed. What aspects of {user_input} inspire you most?",
        f"Grateful to witness the artistry behind {user_input}. The craftsmanship and attention to detail is truly remarkable. It's experiences like these that remind me why I'm passionate about sharing authentic moments. How has {user_input} influenced your perspective?",
        f"Taking time to appreciate the excellence of {user_input}. The quality and dedication that goes into creating experiences like this is truly inspiring. I'm honored to be part of this journey. What's your connection to {user_input}?",
        f"Immersed in the sophistication of {user_input}. The elegance and thoughtfulness in every element creates an atmosphere of pure excellence. Moments like these fuel my creativity and passion. Share your thoughts on {user_input}!",
        f"Experiencing the mastery of {user_input} firsthand. The level of expertise and innovation on display is absolutely remarkable. It's encounters like these that push boundaries and inspire growth. What's your favorite {user_input} memory?"
    ]
    
    funny_templates = [
        f"So apparently {user_input} has completely taken over my life and I'm not even mad about it. Like, when did I become this person who gets genuinely excited about {user_input}? Plot twist: I love every second of it. Anyone else have a mild {user_input} obsession?",
        f"Me: I'll just quickly check out {user_input}. Also me three hours later: still here, no regrets, living my best life. How did {user_input} become my entire personality? Not complaining though! Who else gets completely lost in {user_input}?",
        f"Breaking news: Local person discovers {user_input} and forgets how to act normal. The evidence is overwhelming and I'm definitely guilty as charged. Send help... or don't, I'm having too much fun! What's your {user_input} guilty pleasure?",
        f"Current mood: pretending I'm not completely obsessed with {user_input} while simultaneously planning my next {user_input} adventure. The struggle is real but so is the joy! Anyone else living this double life?",
        f"Plot twist: {user_input} was the main character all along and I'm just here for the ride. Honestly didn't see this level of addiction coming but here we are! What's the weirdest thing you love about {user_input}?"
    ]
    
    inspirational_templates = [
        f"Every encounter with {user_input} reminds me that life is full of extraordinary moments waiting to be discovered. The beauty lies not just in the destination, but in every step of the journey. Embrace the magic around you. What's inspiring you today?",
        f"In a world that moves so fast, {user_input} teaches us to slow down and truly appreciate the present moment. There's profound wisdom in taking time to connect with what matters most. Find your {user_input} and let it guide you. What brings you peace?",
        f"The power of {user_input} lies in its ability to transform ordinary moments into extraordinary memories. Every experience shapes us and helps us grow into who we're meant to become. Chase what sets your soul on fire. What's your passion?",
        f"Through {user_input}, I'm reminded that the most beautiful things in life often come from stepping outside our comfort zones. Growth happens when we embrace new experiences with an open heart. What's calling you to be brave?",
        f"There's something magical about {user_input} that speaks to the deepest parts of our being. It connects us to ourselves, to others, and to the world around us in ways we never expected. What connects you to your purpose?"
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
        category = detect_category_advanced(user_input)
        
        # Simple, clean prompts that work better with GPT-2
        clean_prompts = [
            f"{user_input.strip()}. This is amazing",
            f"Today I experienced {user_input.strip()}",
            f"Just finished {user_input.strip()}",
            f"Loving this {user_input.strip()} moment"
        ]
        
        best_caption = ""
        
        # Try each simple prompt
        for prompt in clean_prompts:
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device if torch.cuda.is_available() else "cpu")

            with torch.no_grad():
                output = model.generate(
                    **inputs,
                    max_new_tokens=40,   # Reduced to prevent gibberish
                    temperature=0.7,     # Lower temperature for more coherent text
                    top_p=0.8,          # More focused sampling
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.1,
                    early_stopping=True
                )

            result = tokenizer.decode(output[0], skip_special_tokens=True)
            raw_caption = result.replace(prompt, "").strip()
            
            # Strict validation for clean text
            if is_clean_caption(raw_caption):
                best_caption = clean_text(raw_caption)
                break
        
        # If model output is bad, always use fallback
        if not best_caption or len(best_caption) < 20:
            best_caption = generate_fallback_caption(user_input, style, category)
        
        formatted_caption = clean_and_format_caption(best_caption, user_input, category, style)
        return formatted_caption, category
        
    except Exception as e:
        # Always use fallback on error
        category = detect_category_advanced(user_input)
        fallback_caption = generate_fallback_caption(user_input, style, category)
        formatted_caption = clean_and_format_caption(fallback_caption, user_input, category, style)
        return formatted_caption, category

def is_clean_caption(text):
    """Check if the generated text is actually a clean, readable caption"""
    if not text or len(text) < 10:
        return False
    
    # Check for common bad patterns
    bad_patterns = [
        r'http[s]?://',      # URLs
        r'#\w+',             # Hashtags
        r'\[.*?\]',          # Brackets with content
        r'【.*?】',           # Japanese brackets
        r'quote=',           # Quote tags
        r'tagline=',         # Tagline tags
        r'tbtfunkyblogger',  # Specific spam
        r'☎',                # Phone emoji (weird in captions)
        r'👉.*?http',        # Arrow pointing to links
        r'\d{4}-\d{2}-\d{2}', # Dates
        r'\.com',            # Domain extensions
    ]
    
    for pattern in bad_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    
    # Check for too many emojis or symbols
    emoji_count = len(re.findall(r'[😀-🙏🌀-🗿🚀-🛿⚡-⚿]', text))
    if emoji_count > 3:
        return False
    
    # Check for gibberish (too many non-letter characters)
    letter_count = len(re.findall(r'[a-zA-Z]', text))
    total_count = len(text.replace(' ', ''))
    if total_count > 0 and letter_count / total_count < 0.6:
        return False
    
    return True

def clean_text(text):
    """Clean up the generated text"""
    # Remove any remaining bad content
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'【.*?】', '', text)
    text = re.sub(r'quote=.*?(?=\s|$)', '', text)
    text = re.sub(r'tagline=.*?(?=\s|$)', '', text)
    
    # Clean up whitespace
    text = ' '.join(text.split())
    
    # Remove trailing punctuation if it looks incomplete
    text = re.sub(r'[,.\-]+

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
            st.code(item["caption"], language=None), '', text).strip()
    
    return text

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
