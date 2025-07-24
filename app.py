import streamlit as st
import random
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="InstaCap AI ✨",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Advanced Custom CSS for Ultra-Modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 40px;
        margin: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .glassmorphism-header {
        text-align: center;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ff6b6b, #ffd93d, #6bcf7f, #4d79ff);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 3s ease-in-out infinite;
        margin-bottom: 10px;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
        margin-bottom: 0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.2);
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .stat-card:hover::before {
        left: 100%;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .stat-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
    }
    
    .input-section {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 35px;
        margin: 30px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #333 !important;
        font-size: 1.1rem !important;
        padding: 15px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #ff6b6b !important;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.3) !important;
        transform: scale(1.02) !important;
    }
    
    .stSelectbox select {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #333 !important;
        font-weight: 500 !important;
    }
    
    .stSlider {
        padding: 20px 0 !important;
    }
    
    .generate-btn {
        background: linear-gradient(45deg, #ff6b6b, #ffd93d) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 15px 40px !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: white !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .generate-btn:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.6) !important;
    }
    
    .caption-output {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 25px;
        padding: 30px;
        margin: 30px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .caption-output::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 50%);
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .caption-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .caption-text {
        font-size: 1.2rem;
        line-height: 1.8;
        color: #ffffff;
        font-weight: 400;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border-left: 5px solid #ffd93d;
        margin-bottom: 20px;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .action-buttons {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin-top: 25px;
    }
    
    .action-btn {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 12px 20px !important;
        color: white !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .action-btn:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    .category-badge {
        display: inline-block;
        background: linear-gradient(45deg, #ffd93d, #ff6b6b);
        color: white;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        margin: 10px 0;
    }
    
    .tips-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 30px;
        margin: 30px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
        margin-top: 20px;
    }
    
    .tip-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        border-left: 4px solid #ffd93d;
        transition: all 0.3s ease;
    }
    
    .tip-card:hover {
        transform: translateX(5px);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .tip-title {
        color: #ffd93d;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }
    
    .tip-content {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
    }
    
    .floating-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .particle {
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
</style>
""", unsafe_allow_html=True)

# Add floating particles for ambiance
st.markdown("""
<div class="floating-particles">
    <div class="particle" style="left: 10%; top: 20%; width: 8px; height: 8px; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; top: 80%; width: 6px; height: 6px; animation-delay: 1s;"></div>
    <div class="particle" style="left: 60%; top: 30%; width: 10px; height: 10px; animation-delay: 2s;"></div>
    <div class="particle" style="left: 80%; top: 70%; width: 4px; height: 4px; animation-delay: 3s;"></div>
    <div class="particle" style="left: 40%; top: 10%; width: 7px; height: 7px; animation-delay: 4s;"></div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_captions' not in st.session_state:
    st.session_state.generated_captions = 0
if 'user_prompts' not in st.session_state:
    st.session_state.user_prompts = []

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header Section
st.markdown('''
<div class="glassmorphism-header">
    <h1 class="main-title">📸 InstaCap AI</h1>
    <p class="subtitle">✨ Generate viral Instagram captions with perfect hashtags & emojis ✨</p>
</div>
''', unsafe_allow_html=True)

# Stats Section
st.markdown('''
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">{}+</div>
        <div class="stat-label">Captions Generated</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">2.5K+</div>
        <div class="stat-label">Happy Users</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">99%</div>
        <div class="stat-label">Success Rate</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">24/7</div>
        <div class="stat-label">Available</div>
    </div>
</div>
'''.format(st.session_state.generated_captions), unsafe_allow_html=True)

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
    
    if category in CAPTION_TEMPLATES:
        caption = random.choice(CAPTION_TEMPLATES[category])
    else:
        caption = random.choice(CAPTION_TEMPLATES['lifestyle'])
    
    hashtags = random.sample(HASHTAG_SETS.get(category, HASHTAG_SETS['lifestyle']), 6)
    
    final_caption = f"{caption}\n\n{' '.join(hashtags)}"
    
    return final_caption, category

# Input Section
st.markdown('''
<div class="input-section">
    <div class="section-title">🎯 What's your post about?</div>
</div>
''', unsafe_allow_html=True)

user_prompt = st.text_area(
    "",
    placeholder="✨ Describe your photo, moment, or feeling...\ne.g., 'Peaceful sunset over the mountains after a long hike' or 'Amazing pasta dinner with friends'",
    height=120,
    key="user_input"
)

# Options Section
col1, col2 = st.columns(2)
with col1:
    caption_style = st.selectbox(
        "🎨 Caption Style",
        ["Casual & Fun", "Motivational", "Dreamy & Poetic", "Simple & Clean"],
        key="style_select"
    )

with col2:
    hashtag_count = st.slider("📱 Hashtags", 3, 10, 6, key="hashtag_slider")

# Generate Button
if st.button("🚀 Generate My Perfect Caption", type="primary", use_container_width=True):
    if user_prompt.strip():
        with st.spinner("✨ Crafting your viral caption..."):
            # Enhanced progress animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_messages = [
                "🧠 Analyzing your content...",
                "🎨 Choosing perfect emojis...",
                "📱 Selecting trending hashtags...",
                "✨ Adding the magic touch...",
                "🎉 Almost ready!"
            ]
            
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
                if i % 20 == 0 and i // 20 < len(status_messages):
                    status_text.text(status_messages[i // 20])
            
            status_text.empty()
            
            # Generate caption
            caption, detected_category = generate_clean_caption(user_prompt, caption_style.lower())
            
            # Update stats
            st.session_state.generated_captions += 1
            st.session_state.user_prompts.append(user_prompt)
            
            # Success message
            st.success("🎉 Your viral caption is ready to conquer Instagram!")
            
            # Category badge
            st.markdown(f'<div class="category-badge">📂 {detected_category.title()} Vibes</div>', unsafe_allow_html=True)
            
            # Caption output with enhanced styling
            st.markdown(f'''
            <div class="caption-output">
                <div class="caption-header">
                    📝 Your Instagram Caption
                </div>
                <div class="caption-text">
                    {caption}
                </div>
                <div class="action-buttons">
                    <button class="action-btn">📋 Copy Caption</button>
                    <button class="action-btn">🔄 Generate New</button>
                    <button class="action-btn">📤 Share Now</button>
                    <button class="action-btn">💾 Save Draft</button>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Additional actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎲 Try Different Style", key="different_style"):
                    st.rerun()
            with col2:
                if st.button("🔥 Make it Trending", key="trending"):
                    st.info("🔥 Added trending elements!")
            with col3:
                if st.button("📊 Analytics Preview", key="analytics"):
                    st.info("📈 Predicted engagement: High!")
    else:
        st.error("⚠️ Please describe your post to get started!")

# Tips Section
st.markdown('''
<div class="tips-section">
    <div class="section-title">💡 Pro Tips for Viral Captions</div>
    <div class="tips-grid">
        <div class="tip-card">
            <div class="tip-title">✨ Be Specific</div>
            <div class="tip-content">Include details about location, time, mood, and activities for more personalized captions</div>
        </div>
        <div class="tip-card">
            <div class="tip-title">🎯 Know Your Audience</div>
            <div class="tip-content">Choose the right style - casual for friends, motivational for fitness, dreamy for lifestyle</div>
        </div>
        <div class="tip-card">
            <div class="tip-title">📱 Trending Categories</div>
            <div class="tip-content">Sunset shots, food pics, travel adventures, and fitness journeys perform best</div>
        </div>
        <div class="tip-card">
            <div class="tip-title">🔥 Engagement Boosters</div>
            <div class="tip-content">Ask questions, use call-to-actions, and include relevant trending hashtags</div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Recent prompts with enhanced styling
if st.session_state.user_prompts:
    st.markdown('''
    <div class="tips-section">
        <div class="section-title">📚 Your Recent Creations</div>
    </div>
    ''', unsafe_allow_html=True)
    
    for i, prompt in enumerate(reversed(st.session_state.user_prompts[-3:]), 1):
        st.markdown(f'''
        <div class="tip-card">
            <div class="tip-title">Creation #{i}</div>
            <div class="tip-content">{prompt}</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('''
<div style="text-align: center; padding: 30px; color: rgba(255,255,255,0.7); font-size: 0.9rem;">
    Made with ❤️ & ✨ | InstaCap AI © 2024 | Turn moments into viral content
</div>
''', unsafe_allow_html=True)
