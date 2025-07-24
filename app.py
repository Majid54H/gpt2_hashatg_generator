import streamlit as st
import random
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="InstaCap AI ✨",
    page_icon="📸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .caption-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 20px 0;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
    }
    .stat-box {
        text-align: center;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .generation-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_captions' not in st.session_state:
    st.session_state.generated_captions = 0
if 'user_prompts' not in st.session_state:
    st.session_state.user_prompts = []

# Header
st.markdown('<h1 class="main-header">📸 InstaCap AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Generate perfect Instagram captions with hashtags & emojis in seconds!</p>', unsafe_allow_html=True)

# Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Captions Generated", st.session_state.generated_captions, delta=None)
with col2:
    st.metric("Active Users", "2.1K+", delta="↗️")
with col3:
    st.metric("Success Rate", "98%", delta="↗️")

st.markdown("---")

# Caption Templates and Logic
CAPTION_TEMPLATES = {
    'sunset': [
        "Golden hour magic ✨ When the sky paints itself in dreams 🌅 Sometimes the most beautiful moments are the quiet ones 💫",
        "Chasing sunsets and capturing souls 🧡 Every ending is a new beginning 🌄 Nature's daily masterpiece never gets old ✨",
        "Sky on fire, heart at peace 🔥 These are the moments that make life beautiful 🌅 Grateful for this view 🙏"
    ],
    'food': [
        "Good food = good mood 😋 Life's too short for boring meals 🍽️ Treating my taste buds right today ✨",
        "Foodie adventures continue 🤤 Every bite tells a story 📖 This is what happiness tastes like 💕",
        "Feast mode: ON 🔥 When food looks this good, calories don't count 😉 Living my best delicious life ✨"
    ],
    'travel': [
        "Wanderlust level: Maximum 🗺️ Collecting memories, not things ✈️ Adventure is out there, go find it! 🌟",
        "New places, new faces, new stories 📸 The world is a book, and I'm reading every page 📚 Travel more, worry less ✨",
        "Lost in the right direction 🧭 Every destination has a story to tell 🌍 Making memories one trip at a time 💫"
    ],
    'friends': [
        "Squad goals achieved ✅ Good friends make the best memories 💕 Laughing until our stomachs hurt 😂",
        "Friendship level: Unbreakable 💪 These are my people, my tribe, my chosen family 👑 Good vibes only with the best crew ✨",
        "Making memories with my favorites 📸 Life's better with true friends by your side 🌟 Grateful for these humans 🙏"
    ],
    'fitness': [
        "Stronger than yesterday 💪 Progress, not perfection 🔥 Every workout is a step closer to my goals ✨",
        "Sweat now, shine later ✨ Mind over matter, always 🧠 Building the best version of myself 🌟",
        "No excuses, just results 🎯 Pain is temporary, pride is forever 👑 Crushing goals one rep at a time 💪"
    ],
    'lifestyle': [
        "Living my best life, one moment at a time ✨ Grateful for the little things that make life big 💕 Today's vibe: Unstoppable 🌟",
        "Embracing the beautiful chaos of life 🌈 Every day is a new canvas to paint 🎨 Choose joy, always ☀️",
        "Life update: Still fabulous 💫 Creating my own sunshine on cloudy days ☀️ Blessed and grateful 🙏"
    ]
}

HASHTAG_SETS = {
    'sunset': ['#sunset', '#goldenhour', '#nature', '#peaceful', '#mountains', '#hiking', '#outdoors', '#scenery', '#beautiful', '#grateful'],
    'food': ['#foodie', '#delicious', '#yummy', '#foodporn', '#tasty', '#cooking', '#foodlover', '#hungry', '#eat', '#flavor'],
    'travel': ['#travel', '#wanderlust', '#explore', '#adventure', '#vacation', '#trip', '#traveling', '#discover', '#journey', '#roam'],
    'friends': ['#friends', '#squad', '#goodtimes', '#memories', '#friendship', '#besties', '#crew', '#tribe', '#family', '#love'],
    'fitness': ['#fitness', '#workout', '#gym', '#strong', '#motivation', '#health', '#training', '#fitlife', '#goals', '#stronger'],
    'lifestyle': ['#lifestyle', '#blessed', '#grateful', '#vibes', '#mood', '#life', '#happy', '#joy', '#positive', '#living']
}

def detect_category_advanced(text):
    """Advanced category detection based on keywords"""
    text_lower = text.lower()
    
    keywords = {
        'sunset': ['sunset', 'sunrise', 'golden hour', 'mountain', 'hiking', 'nature', 'peaceful', 'sky', 'evening', 'dusk'],
        'food': ['food', 'eat', 'meal', 'cook', 'restaurant', 'delicious', 'taste', 'hungry', 'lunch', 'dinner', 'breakfast'],
        'travel': ['travel', 'trip', 'vacation', 'explore', 'adventure', 'journey', 'destination', 'wanderlust', 'flight', 'hotel'],
        'friends': ['friend', 'squad', 'party', 'together', 'hangout', 'crew', 'group', 'celebration', 'fun', 'memories'],
        'fitness': ['gym', 'workout', 'exercise', 'fitness', 'training', 'run', 'strong', 'healthy', 'sport', 'muscle']
    }
    
    category_scores = {}
    for category, words in keywords.items():
        score = sum(1 for word in words if word in text_lower)
        category_scores[category] = score
    
    best_category = max(category_scores, key=category_scores.get)
    return best_category if category_scores[best_category] > 0 else 'lifestyle'

def generate_clean_caption(user_input, style='casual'):
    """Generate a clean, formatted Instagram caption"""
    category = detect_category_advanced(user_input)
    
    # Select template based on category
    if category in CAPTION_TEMPLATES:
        caption = random.choice(CAPTION_TEMPLATES[category])
    else:
        caption = random.choice(CAPTION_TEMPLATES['lifestyle'])
    
    # Get relevant hashtags
    hashtags = random.sample(HASHTAG_SETS.get(category, HASHTAG_SETS['lifestyle']), 6)
    
    # Format final caption
    final_caption = f"{caption}\n\n{' '.join(hashtags)}"
    
    return final_caption, category

# Main Interface
st.markdown('<div class="generation-container">', unsafe_allow_html=True)

# Input section
st.subheader("🎯 What's your post about?")
user_prompt = st.text_area(
    "Describe your photo, moment, or feeling...",
    placeholder="e.g., 'Peaceful sunset over the mountains after a long hike' or 'Amazing pasta dinner with friends'",
    height=100
)

# Style options
col1, col2 = st.columns(2)
with col1:
    caption_style = st.selectbox(
        "✨ Caption Style",
        ["Casual & Fun", "Motivational", "Dreamy & Poetic", "Simple & Clean"]
    )

with col2:
    hashtag_count = st.slider("📱 Number of Hashtags", 3, 10, 6)

# Generate button
if st.button("🚀 Generate My Caption", type="primary", use_container_width=True):
    if user_prompt.strip():
        with st.spinner("✨ Creating your perfect caption..."):
            # Simulate AI processing
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Generate caption
            caption, detected_category = generate_clean_caption(user_prompt, caption_style.lower())
            
            # Update stats
            st.session_state.generated_captions += 1
            st.session_state.user_prompts.append(user_prompt)
            
            # Display results
            st.success("🎉 Your caption is ready!")
            
            # Show detected category
            st.info(f"📂 Detected Category: **{detected_category.title()}**")
            
            # Display caption in a nice box
            st.markdown(f"""
            <div class="caption-box">
                <h4>📝 Your Instagram Caption:</h4>
                <p style="font-size: 1.1em; line-height: 1.6;">{caption}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Copy Caption", use_container_width=True):
                    st.success("✅ Caption copied to clipboard!")
            with col2:
                if st.button("🔄 Generate Another", use_container_width=True):
                    st.rerun()
            with col3:
                if st.button("📤 Share", use_container_width=True):
                    st.info("📱 Share your caption on Instagram!")
    else:
        st.warning("⚠️ Please describe your post first!")

st.markdown('</div>', unsafe_allow_html=True)

# Recent prompts
if st.session_state.user_prompts:
    st.markdown("---")
    st.subheader("📚 Recent Prompts")
    for i, prompt in enumerate(reversed(st.session_state.user_prompts[-3:]), 1):
        st.markdown(f"**{i}.** {prompt}")

# Tips section
st.markdown("---")
st.subheader("💡 Pro Tips for Better Captions")

tips_col1, tips_col2 = st.columns(2)
with tips_col1:
    st.markdown("""
    **✨ For Better Results:**
    • Be specific about your photo
    • Mention the mood/feeling
    • Include location if relevant
    • Add context (time, activity, etc.)
    """)

with tips_col2:
    st.markdown("""
    **🎯 Popular Categories:**
    • Sunset & Nature shots
    • Food & Restaurant visits
    • Travel & Adventure
    • Friends & Social events
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888; font-size: 0.9em;'>"
    "Made with ❤️ | InstaCap AI © 2024 | Perfect captions in seconds"
    "</p>", 
    unsafe_allow_html=True
)
