import streamlit as st
import random
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="CaptionCrafter ✨",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Custom CSS with Black & Parrot Green Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-container {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 40px;
        margin: 20px;
        border: 1px solid rgba(34, 197, 94, 0.2);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .header-section {
        text-align: center;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 40px;
        border: 1px solid rgba(34, 197, 94, 0.3);
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.1);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #22c55e;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(34, 197, 94, 0.5);
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
        margin-bottom: 0;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    .input-section {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 35px;
        margin: 30px 0;
        border: 1px solid rgba(34, 197, 94, 0.2);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #22c55e;
        margin-bottom: 20px;
        text-align: center;
        letter-spacing: 0.5px;
    }
    
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
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
        padding: 20px 0 !important;
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
        padding: 35px;
        margin: 30px 0;
        border: 1px solid rgba(34, 197, 94, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        position: relative;
    }
    
    .caption-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #22c55e;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 10px;
        letter-spacing: 0.5px;
    }
    
    .caption-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #ffffff;
        font-weight: 400;
        padding: 25px;
        background: rgba(0, 0, 0, 0.4);
        border-radius: 12px;
        border-left: 4px solid #22c55e;
        margin-bottom: 25px;
        white-space: pre-wrap;
    }
    
    .action-buttons {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 15px;
        margin-top: 25px;
    }
    
    .action-btn {
        background: rgba(34, 197, 94, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 10px !important;
        padding: 12px 18px !important;
        color: #22c55e !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        font-size: 0.95rem !important;
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
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
        margin: 15px 0;
    }
    
    .tips-section {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 35px;
        margin: 40px 0;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-top: 25px;
    }
    
    .tip-card {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 12px;
        padding: 25px;
        border-left: 3px solid #22c55e;
        transition: all 0.3s ease;
        border: 1px solid rgba(34, 197, 94, 0.1);
    }
    
    .tip-card:hover {
        transform: translateY(-2px);
        background: rgba(0, 0, 0, 0.7);
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.1);
    }
    
    .tip-title {
        color: #22c55e;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }
    
    .tip-content {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .recent-section {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 30px;
        margin: 30px 0;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }
    
    .recent-item {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 3px solid #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.1);
    }
    
    .recent-title {
        color: #22c55e;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 8px;
    }
    
    .recent-content {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.5;
        font-size: 0.9rem;
    }
    
    .footer {
        text-align: center;
        padding: 30px;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        border-top: 1px solid rgba(34, 197, 94, 0.1);
        margin-top: 40px;
    }
    
    /* Hide Streamlit elements */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding-top: 0;}
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: #22c55e !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_prompts' not in st.session_state:
    st.session_state.user_prompts = []

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header Section
st.markdown('''
<div class="header-section">
    <h1 class="main-title">✍️ CaptionCrafter</h1>
    <p class="subtitle">Professional Instagram caption generator powered by AI. Create engaging captions with perfect hashtags and emojis for maximum reach.</p>
</div>
''', unsafe_allow_html=True)

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
    <div class="section-title">🎯 Describe Your Content</div>
</div>
''', unsafe_allow_html=True)

user_prompt = st.text_area(
    "",
    placeholder="Describe your photo, moment, or feeling...\ne.g., 'Peaceful sunset over the mountains after a long hike' or 'Amazing pasta dinner with friends'",
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
    hashtag_count = st.slider("📱 Number of Hashtags", 3, 10, 6, key="hashtag_slider")

# Generate Button
if st.button("🚀 Generate Caption", type="primary", use_container_width=True):
    if user_prompt.strip():
        with st.spinner("✨ Crafting your perfect caption..."):
            # Enhanced progress animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_messages = [
                "🧠 Analyzing content...",
                "🎨 Selecting emojis...",
                "📱 Choosing hashtags...",
                "✨ Finalizing caption...",
                "🎉 Ready!"
            ]
            
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
                if i % 20 == 0 and i // 20 < len(status_messages):
                    status_text.text(status_messages[i // 20])
            
            status_text.empty()
            
            # Generate caption
            caption, detected_category = generate_clean_caption(user_prompt, caption_style.lower())
            
            # Update session state
            st.session_state.user_prompts.append(user_prompt)
            
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
            
            # Additional actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎲 Different Style", key="different_style"):
                    st.rerun()
            with col2:
                if st.button("🔥 Add Trending", key="trending"):
                    st.info("🔥 Added trending elements!")
            with col3:
                if st.button("📊 Preview", key="analytics"):
                    st.info("📈 Caption optimized for engagement!")
    else:
        st.error("⚠️ Please describe your content to get started!")

# Tips Section
st.markdown('''
<div class="tips-section">
    <div class="section-title">💡 Pro Tips</div>
    <div class="tips-grid">
        <div class="tip-card">
            <div class="tip-title">✨ Be Specific</div>
            <div class="tip-content">Include details about location, mood, and activities for more personalized captions</div>
        </div>
        <div class="tip-card">
            <div class="tip-title">🎯 Know Your Audience</div>
            <div class="tip-content">Choose the right style - casual for friends, motivational for fitness</div>
        </div>
        <div class="tip-card">
            <div class="tip-title">📱 Trending Content</div>
            <div class="tip-content">Sunset shots, food pics, and travel adventures perform best</div>
        </div>
        <div class="tip-card">
            <div class="tip-title">🔥 Engagement Boost</div>
            <div class="tip-content">Ask questions and use relevant trending hashtags</div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Recent prompts
if st.session_state.user_prompts:
    st.markdown('''
    <div class="recent-section">
        <div class="section-title">📚 Recent Creations</div>
    </div>
    ''', unsafe_allow_html=True)
    
    for i, prompt in enumerate(reversed(st.session_state.user_prompts[-3:]), 1):
        st.markdown(f'''
        <div class="recent-item">
            <div class="recent-title">Creation #{i}</div>
            <div class="recent-content">{prompt}</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('''
<div class="footer">
    CaptionCrafter © 2024 | Professional Instagram Caption Generation
</div>
''', unsafe_allow_html=True)
