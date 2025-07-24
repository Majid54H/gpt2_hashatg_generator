import streamlit as st
import random
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="CaptionCrafter",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Compact Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Remove default Streamlit spacing */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
    }
    
    .stApp {
        background: #0a0a0a;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #111111 !important;
        border-right: 1px solid #22c55e !important;
        padding-top: 0 !important;
    }
    
    .sidebar-header {
        background: #1a1a1a;
        padding: 12px;
        border-bottom: 1px solid #22c55e;
        margin-bottom: 8px;
    }
    
    .sidebar-title {
        color: #22c55e;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0;
        text-align: center;
    }
    
    .history-item {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 8px;
        margin-bottom: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.75rem;
    }
    
    .history-item:hover {
        background: #222;
        border-color: #22c55e;
    }
    
    .history-text {
        color: #e5e5e5;
        line-height: 1.3;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    
    .history-time {
        color: #22c55e;
        font-size: 0.65rem;
        margin-top: 4px;
    }
    
    /* Main content */
    .main-header {
        background: #111111;
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        text-align: center;
    }
    
    .app-title {
        color: #22c55e;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0 0 4px 0;
    }
    
    .app-subtitle {
        color: #888;
        font-size: 0.85rem;
        margin: 0;
    }
    
    .input-container {
        background: #111111;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .section-label {
        color: #22c55e;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    /* Input styling */
    .stTextArea textarea {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        font-size: 0.9rem !important;
        padding: 12px !important;
        font-family: 'Inter', sans-serif !important;
        resize: none !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 1px #22c55e !important;
    }
    
    .stSelectbox select {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
        color: #ffffff !important;
        font-size: 0.85rem !important;
        padding: 8px !important;
    }
    
    .stSlider {
        padding: 8px 0 !important;
    }
    
    .stSlider > div > div > div > div {
        background: #22c55e !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: #22c55e !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #000000 !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #16a34a !important;
        transform: translateY(-1px) !important;
    }
    
    /* Output section */
    .output-container {
        background: #111111;
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 16px;
        margin-top: 12px;
    }
    
    .output-header {
        color: #22c55e;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .caption-display {
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 12px;
        color: #ffffff;
        font-size: 0.9rem;
        line-height: 1.5;
        white-space: pre-wrap;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .action-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    
    .action-button {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 4px !important;
        padding: 6px 12px !important;
        color: #22c55e !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .action-button:hover {
        background: #222 !important;
        border-color: #22c55e !important;
    }
    
    .category-tag {
        display: inline-block;
        background: #22c55e;
        color: #000;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    /* Tips section */
    .tips-container {
        background: #111111;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 12px;
        margin-top: 12px;
    }
    
    .tip-item {
        color: #888;
        font-size: 0.8rem;
        margin-bottom: 4px;
        padding-left: 12px;
        position: relative;
    }
    
    .tip-item:before {
        content: "•";
        color: #22c55e;
        position: absolute;
        left: 0;
    }
    
    /* Clear button */
    .clear-btn {
        background: #dc2626 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 4px 8px !important;
        font-size: 0.7rem !important;
        margin-top: 8px !important;
        width: 100% !important;
    }
    
    /* Hide Streamlit elements */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding-top: 0;}
    footer {display: none;}
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: #22c55e !important;
    }
    
    /* Remove extra spacing */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    .row-widget {
        margin-bottom: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_prompts' not in st.session_state:
    st.session_state.user_prompts = []
if 'prompt_times' not in st.session_state:
    st.session_state.prompt_times = []

# Caption Templates
CAPTION_TEMPLATES = {
    'sunset': [
        "Golden hour magic ✨ When the sky paints itself in dreams 🌅 Sometimes the most beautiful moments are the quiet ones 💫",
        "Chasing sunsets and capturing souls 🧡 Every ending is a new beginning 🌄 Nature's daily masterpiece never gets old ✨"
    ],
    'food': [
        "Good food = good mood 😋 Life's too short for boring meals 🍽️ Treating my taste buds right today ✨",
        "Foodie adventures continue 🤤 Every bite tells a story 📖 This is what happiness tastes like 💕"
    ],
    'travel': [
        "Wanderlust level: Maximum 🗺️ Collecting memories, not things ✈️ Adventure is out there, go find it! 🌟",
        "New places, new faces, new stories 📸 The world is a book, and I'm reading every page 📚 Travel more, worry less ✨"
    ],
    'friends': [
        "Squad goals achieved ✅ Good friends make the best memories 💕 Laughing until our stomachs hurt 😂",
        "Friendship level: Unbreakable 💪 These are my people, my tribe, my chosen family 👑 Good vibes only with the best crew ✨"
    ],
    'fitness': [
        "Stronger than yesterday 💪 Progress, not perfection 🔥 Every workout is a step closer to my goals ✨",
        "Sweat now, shine later ✨ Mind over matter, always 🧠 Building the best version of myself 🌟"
    ],
    'lifestyle': [
        "Living my best life, one moment at a time ✨ Grateful for the little things that make life big 💕 Today's vibe: Unstoppable 🌟",
        "Embracing the beautiful chaos of life 🌈 Every day is a new canvas to paint 🎨 Choose joy, always ☀️"
    ]
}

HASHTAG_SETS = {
    'sunset': ['#sunset', '#goldenhour', '#nature', '#peaceful', '#mountains', '#hiking'],
    'food': ['#foodie', '#delicious', '#yummy', '#foodporn', '#tasty', '#cooking'],
    'travel': ['#travel', '#wanderlust', '#explore', '#adventure', '#vacation', '#trip'],
    'friends': ['#friends', '#squad', '#goodtimes', '#memories', '#friendship', '#besties'],
    'fitness': ['#fitness', '#workout', '#gym', '#strong', '#motivation', '#health'],
    'lifestyle': ['#lifestyle', '#blessed', '#grateful', '#vibes', '#mood', '#life']
}

def detect_category_advanced(text):
    text_lower = text.lower()
    keywords = {
        'sunset': ['sunset', 'sunrise', 'golden hour', 'mountain', 'hiking', 'nature', 'sky'],
        'food': ['food', 'eat', 'meal', 'cook', 'restaurant', 'delicious', 'taste'],
        'travel': ['travel', 'trip', 'vacation', 'explore', 'adventure', 'journey'],
        'friends': ['friend', 'squad', 'party', 'together', 'hangout', 'crew'],
        'fitness': ['gym', 'workout', 'exercise', 'fitness', 'training', 'run']
    }
    
    category_scores = {}
    for category, words in keywords.items():
        score = sum(1 for word in words if word in text_lower)
        category_scores[category] = score
    
    best_category = max(category_scores, key=category_scores.get)
    return best_category if category_scores[best_category] > 0 else 'lifestyle'

def generate_clean_caption(user_input, style='casual'):
    category = detect_category_advanced(user_input)
    caption = random.choice(CAPTION_TEMPLATES.get(category, CAPTION_TEMPLATES['lifestyle']))
    hashtags = random.sample(HASHTAG_SETS.get(category, HASHTAG_SETS['lifestyle']), 6)
    return f"{caption}\n\n{' '.join(hashtags)}", category

# Sidebar
with st.sidebar:
    st.markdown('''
    <div class="sidebar-header">
        <div class="sidebar-title">📚 History</div>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.session_state.user_prompts:
        for prompt, prompt_time in zip(reversed(st.session_state.user_prompts[-8:]), 
                                      reversed(st.session_state.prompt_times[-8:])):
            st.markdown(f'''
            <div class="history-item">
                <div class="history-text">{prompt}</div>
                <div class="history-time">{prompt_time}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        if st.button("Clear", key="clear", help="Clear history"):
            st.session_state.user_prompts = []
            st.session_state.prompt_times = []
            st.rerun()
    else:
        st.markdown('<div style="color: #666; text-align: center; padding: 20px; font-size: 0.8rem;">No history yet</div>', unsafe_allow_html=True)

# Main Content
st.markdown('''
<div class="main-header">
    <div class="app-title">✍️ CaptionCrafter</div>
    <div class="app-subtitle">AI-powered Instagram caption generator</div>
</div>
''', unsafe_allow_html=True)

# Input Section
st.markdown('''
<div class="input-container">
    <div class="section-label">Describe your content</div>
</div>
''', unsafe_allow_html=True)

user_prompt = st.text_area("", placeholder="e.g., 'Sunset over mountains' or 'Dinner with friends'", height=80, label_visibility="collapsed")

# Options
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Style", ["Casual", "Motivational", "Poetic", "Simple"], label_visibility="collapsed")
with col2:
    hashtags = st.slider("Hashtags", 3, 10, 6, label_visibility="collapsed")

# Generate Button
if st.button("Generate Caption"):
    if user_prompt.strip():
        with st.spinner("Generating..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.005)
                progress.progress(i + 1)
            
            caption, category = generate_clean_caption(user_prompt, style.lower())
            
            # Update history
            current_time = datetime.now().strftime("%H:%M")
            st.session_state.user_prompts.append(user_prompt)
            st.session_state.prompt_times.append(current_time)
            
            st.success("✓ Caption generated")
            
            # Output
            st.markdown(f'<div class="category-tag">{category.title()}</div>', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="output-container">
                <div class="output-header">📝 Your Caption</div>
                <div class="caption-display">{caption}</div>
                <div class="action-grid">
                    <button class="action-button">📋 Copy</button>
                    <button class="action-button">🔄 New</button>
                    <button class="action-button">📤 Share</button>
                    <button class="action-button">💾 Save</button>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.error("Please describe your content first")

# Tips
st.markdown('''
<div class="tips-container">
    <div class="section-label">💡 Tips</div>
    <div class="tip-item">Be specific about your content</div>
    <div class="tip-item">Include location and mood details</div>
    <div class="tip-item">Choose appropriate style for audience</div>
</div>
''', unsafe_allow_html=True)
