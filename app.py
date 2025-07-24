import streamlit as st
import requests
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import random

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
    
    # Add padding token if it doesn't exist
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    return tokenizer, model

tokenizer, model = load_model()

# Emoji and hashtag databases
EMOJIS = {
    'food': ['🍕', '🍔', '🍰', '🥗', '☕', '🍷', '🥂', '🍎', '🥑', '🌮'],
    'travel': ['✈️', '🏖️', '🗺️', '📸', '🌅', '🏔️', '🌊', '🚗', '🎒', '🌴'],
    'fitness': ['💪', '🏃‍♀️', '🏋️‍♂️', '🧘‍♀️', '🚴‍♂️', '⚽', '🏀', '🥇', '💦', '🔥'],
    'lifestyle': ['☀️', '🌙', '💕', '✨', '🌸', '🎨', '📚', '🎵', '🌿', '💫'],
    'work': ['💼', '💻', '📊', '✏️', '📝', '💡', '🎯', '⏰', '☕', '🚀'],
    'friends': ['👯‍♀️', '🤝', '🎉', '🥳', '💃', '🍻', '📱', '😄', '💖', '🌟']
}

HASHTAGS = {
    'food': ['#foodie', '#delicious', '#yummy', '#foodporn', '#tasty', '#cooking', '#recipe', '#foodlover', '#hungry', '#eat'],
    'travel': ['#travel', '#wanderlust', '#explore', '#adventure', '#vacation', '#trip', '#beautiful', '#nature', '#photography', '#traveling'],
    'fitness': ['#fitness', '#workout', '#gym', '#healthy', '#strong', '#motivation', '#training', '#exercise', '#fitlife', '#wellness'],
    'lifestyle': ['#lifestyle', '#life', '#happy', '#blessed', '#grateful', '#vibes', '#mood', '#love', '#inspiration', '#daily'],
    'work': ['#work', '#business', '#entrepreneur', '#success', '#productivity', '#goals', '#hustle', '#professional', '#career', '#motivated'],
    'friends': ['#friends', '#friendship', '#fun', '#goodtimes', '#squad', '#besties', '#memories', '#together', '#friendship', '#love']
}

def detect_category(text):
    """Detect the category of the post based on keywords"""
    text_lower = text.lower()
    
    food_keywords = ['food', 'eat', 'restaurant', 'cook', 'meal', 'lunch', 'dinner', 'breakfast', 'coffee', 'drink']
    travel_keywords = ['travel', 'trip', 'vacation', 'beach', 'mountain', 'city', 'flight', 'hotel', 'explore', 'adventure']
    fitness_keywords = ['gym', 'workout', 'exercise', 'run', 'fitness', 'healthy', 'sport', 'training', 'strong']
    work_keywords = ['work', 'office', 'meeting', 'project', 'business', 'career', 'job', 'professional']
    friends_keywords = ['friend', 'party', 'fun', 'celebration', 'together', 'hanging out', 'squad']
    
    categories = {
        'food': food_keywords,
        'travel': travel_keywords, 
        'fitness': fitness_keywords,
        'work': work_keywords,
        'friends': friends_keywords
    }
    
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    
    return 'lifestyle'  # default category

def generate_hashtags_and_emojis(category, count=8):
    """Generate relevant hashtags and emojis based on category"""
    hashtags = random.sample(HASHTAGS[category], min(count, len(HASHTAGS[category])))
    emojis = random.sample(EMOJIS[category], min(3, len(EMOJIS[category])))
    return hashtags, emojis

def create_instagram_prompt(user_input):
    """Create a structured prompt for Instagram caption generation"""
    category = detect_category(user_input)
    hashtags, emojis = generate_hashtags_and_emojis(category)
    
    # Create a few example Instagram captions to guide the model
    prompt = f"""Create an Instagram caption about: {user_input}

Example Instagram captions:
"Just had the most amazing coffee this morning ☕ Nothing beats that first sip! #coffee #morning #blessed"

"Another day, another adventure! 🌟 Life is what you make it ✨ #lifestyle #motivation #blessed"

Caption about {user_input}:"""
    
    return prompt, category, hashtags, emojis

def enhance_output(generated_text, user_input, hashtags, emojis):
    """Enhance the generated text with hashtags and emojis"""
    # Remove the prompt part from generated text
    if user_input in generated_text:
        caption_start = generated_text.find(user_input) + len(user_input)
        caption = generated_text[caption_start:].strip()
    else:
        caption = generated_text.strip()
    
    # Clean up the caption (remove incomplete sentences)
    sentences = caption.split('.')
    if len(sentences) > 1 and len(sentences[-1]) < 10:
        caption = '. '.join(sentences[:-1]) + '.'
    
    # Add emojis if not present
    if not any(emoji in caption for emoji in ['😀', '😊', '❤️', '✨', '🌟', '💫', '🔥', '💪', '🌸', '☀️']):
        caption = caption + ' ' + ' '.join(emojis[:2])
    
    # Add hashtags
    caption = caption + '\n\n' + ' '.join(hashtags)
    
    return caption

# Prompt Input
prompt = st.text_input("💬 Enter your image description, moment, or thought:")

# Category Selection (Optional)
st.subheader("🎯 Category (Optional)")
category_override = st.selectbox("Choose a category to get more targeted hashtags:", 
                                ['Auto-detect', 'Food', 'Travel', 'Fitness', 'Lifestyle', 'Work', 'Friends'])

# Generate Button
if st.button("🚀 Generate Caption + Hashtags"):
    if prompt.strip() == "":
        st.warning("⚠️ Please enter a prompt to generate from.")
    else:
        with st.spinner("🔍 Thinking..."):
            # Create structured prompt
            instagram_prompt, detected_category, hashtags, emojis = create_instagram_prompt(prompt)
            
            # Override category if user selected one
            if category_override != 'Auto-detect':
                detected_category = category_override.lower()
                hashtags, emojis = generate_hashtags_and_emojis(detected_category)
            
            # Generate with the model
            inputs = tokenizer(instagram_prompt, return_tensors="pt", padding=True, truncation=True, max_length=512)
            
            with torch.no_grad():
                output = model.generate(
                    **inputs, 
                    max_new_tokens=80,
                    do_sample=True, 
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.2
                )
            
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Enhance the output
            final_caption = enhance_output(generated_text, prompt, hashtags, emojis)
        
        # Display results
        st.markdown("### 📝 Generated Instagram Post")
        st.success(final_caption)
        
        # Show detected category
        st.info(f"🏷️ Detected Category: **{detected_category.title()}**")
        
        st.markdown("---")
        st.markdown("#### 💡 Tips:")
        st.markdown("• Try different prompts for variety")
        st.markdown("• Use specific details for better captions")
        st.markdown("• Select a category manually for targeted hashtags")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Made with ❤️ using Streamlit & Transformers</p>", unsafe_allow_html=True)
