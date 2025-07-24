import streamlit as st
import random
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="CaptionCrafter ✨",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Custom CSS with Sidebar Layout
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.9) !important;
        border-right: 2px solid rgba(34, 197, 94, 0.3) !important;
    }
    
    .sidebar-content {
        padding: 20px 15px;
        height: 100vh;
        overflow-y: auto;
    }
    
    .sidebar-title {
        color: #22c55e;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 20px;
        text-align: center;
        letter-spacing: 0.5px;
    }
    
    .history-item {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        background: rgba(34, 197, 94, 0.2);
        transform: translateX(5px);
        border-color: rgba(34, 197, 94, 0.4);
    }
    
    .history-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.85rem;
        line-height: 1.4;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }
    
    .history-time {
        color: rgba(34, 197, 94, 0.7);
        font-size: 0.75rem;
        margin-top: 8px;
        font-weight: 500;
    }
    
    .clear-history {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #ef4444 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-size: 0.85rem !important;
        margin-top: 15px !important;
        width: 100% !important;
    }
    
    /* Main Content */
    .main-container {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 40px;
        margin: 20px;
        border: 1px solid rgba(34, 197, 94, 0.2);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        height: calc(100vh - 40px);
        overflow-y: auto;
    }
    
    .header-section {
        text-align: center;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 30px;
        border: 1px solid rgba(34, 197, 94, 0.3);
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.1);
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #22c55e;
        margin-bottom: 8px;
        text-shadow: 0 0 20px rgba(34, 197, 94, 0.5);
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
        margin-bottom: 0;
        line-height: 1.5;
    }
    
    .input-section {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        border: 1px solid rgba(34, 197, 94, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #22c55e;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }
    
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 18px !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
        height: 100px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.3) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stSelectbox select {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        padding: 12px !important;
    }
    
    .stSelectbox select:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.2) !important;
    }
    
    .stSlider {
        padding: 15px 0 !important;
    }
    
    .stSlider > div > div > div > div {
        background: #22c55e !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #000000 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.3) !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 35px rgba(34, 197, 94, 0.4) !important;
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
    }
    
    .caption-output {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 16px;
        padding: 25px;
        margin-top: 20px;
        border: 1px solid rgba(34, 197, 94, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    }
    
    .caption-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #22c55e;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 0.5px;
    }
    
    .caption-text {
        font-size: 1rem;
        line-height: 1.7;
        color: #ffffff;
        font-weight: 400;
        padding: 20px;
        background: rgba(0, 0, 0, 0.4);
        border-radius: 12px;
        border-left: 4px solid #22c55e;
        margin-bottom: 20px;
        white-space: pre-wrap;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .action-buttons {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }
    
    .action-btn {
        background: rgba(34, 197, 94, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        color: #22c55e !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        font-size: 0.9rem !important;
    }
    
    .action-btn:hover {
        background: rgba(34, 197, 94, 0.2) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 15px rgba(34, 197, 94, 0.2) !important;
    }
    
    .category-badge {
        display: inline-block;
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: #000000;
        padding: 6px 14px;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
        margin-bottom: 15px;
    }
    
    .tips-compact {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    .tips-compact .section-title {
        font-size: 1rem;
        margin-bottom: 12px;
    }
    
    .tip-compact {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 8px;
        padding-left: 15px;
        position: relative;
    }
    
    .tip-compact:before {
        content: "•";
        color: #22c55e;
        position: absolute;
        left: 0;
        font-weight: bold;
    }
    
    /* Hide Streamlit elements */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding-top: 0;}
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: #22c55e !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.2rem;
        }
        .main-container {
            padding: 20px;
            margin: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_prompts' not in st.session_state:
    st.session_state.user_prompts = []
if 'prompt_times' not in st.session_state:
    st.session_state.prompt_times = []

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

# Sidebar for History
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📚 Recent History</div>', unsafe_allow_html=True)
    
    if st.session_state.user_prompts:
        for i, (prompt, prompt_time) in enumerate(zip(reversed(st.session_state.user_prompts[-10:]), 
                                                      reversed(st.session_state.prompt_times[-10:]))):
            st.markdown(f'''
            <div class="history-item">
                <div class="history-text">{prompt}</div>
                <div class="history-time">{prompt_time}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state.user_prompts = []
            st.session_state.prompt_times = []
            st.rerun()
    else:
        st.markdown('''
        <div style="color: rgba(255,255,255,0.6); text-align: center; padding: 20px; font-size: 0.9rem;">
            No history yet.<br>Generate your first caption!
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header Section
st.markdown('''
<div class="header-section">
    <h1 class="main-title">✍️ CaptionCrafter</h1>
    <p class="subtitle">Professional Instagram caption generator powered by AI</p>
</div>
''', unsafe_allow_html=True)

# Input Section
st.markdown('''
<div class="input-section">
    <div class="section-title">🎯 Describe Your Content</div>
</div>
''', unsafe_allow_html=True)

user_prompt = st.text_area(
    "",
    placeholder="Describe your photo, moment, or feeling...\ne.g., 'Peaceful sunset over the mountains' or 'Amazing dinner with friends'",
    height=100,
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
    hashtag_count = st.slider("📱 Number of Hashtags", 3, 10, 6, key="hashtag_slider")

# Generate Button
if st.button("🚀 Generate Caption", type="primary", use_container_width=True):
    if user_prompt.strip():
        with st.spinner("✨ Crafting your perfect caption..."):
            # Quick progress animation
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Generate caption
            caption, detected_category = generate_clean_caption(user_prompt, caption_style.lower())
            
            # Update session state with timestamp
            current_time = datetime.now().strftime("%H:%M")
            st.session_state.user_prompts.append(user_prompt)
            st.session_state.prompt_times.append(current_time)
            
            # Success message
            st.success("🎉 Your caption is ready!")
            
            # Category badge
            st.markdown(f'<div class="category-badge">📂 {detected_category.title()}</div>', unsafe_allow_html=True)
            
            # Caption output
            st.markdown(f'''
            <div class="caption-output">
                <div class="caption-header">
                    📝 Generated Caption
                </div>
                <div class="caption-text">{caption}</div>
                <div class="action-buttons">
                    <button class="action-btn">📋 Copy</button>
                    <button class="action-btn">🔄 Regenerate</button>
                    <button class="action-btn">📤 Share</button>
                    <button class="action-btn">💾 Save</button>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
    else:
        st.error("⚠️ Please describe your content to get started!")

# Compact Tips Section
st.markdown('''
<div class="tips-compact">
    <div class="section-title">💡 Quick Tips</div>
    <div class="tip-compact">Be specific about location, mood, and activities</div>
    <div class="tip-compact">Choose the right style for your audience</div>
    <div class="tip-compact">Include trending hashtags for better reach</div>
    <div class="tip-compact">Ask questions to boost engagement</div>
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
