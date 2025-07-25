import streamlit as st
import openai
from datetime import datetime
import json
import re

# Page configuration
st.set_page_config(
    page_title="Social Media Caption Generator",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .platform-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .generated-content {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin-top: 1rem;
    }
    
    .hashtag-section {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

class SocialMediaCaptionBot:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        
    def generate_instagram_caption(self, topic, style, target_audience, include_cta=True):
        prompt = f"""
        Create an engaging Instagram caption for the following:
        
        Topic: {topic}
        Style: {style}
        Target Audience: {target_audience}
        Include Call-to-Action: {include_cta}
        
        Requirements:
        - Make it engaging and authentic
        - Use emojis strategically
        - Keep it concise but impactful
        - Include line breaks for readability
        - Make it suitable for Instagram's casual tone
        {"- Include a compelling call-to-action" if include_cta else ""}
        
        Format the response as a ready-to-post Instagram caption.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a creative social media expert specializing in Instagram content. Create engaging, authentic captions that drive engagement."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating caption: {str(e)}"
    
    def generate_linkedin_post(self, topic, post_type, industry, tone):
        prompt = f"""
        Create a professional LinkedIn post for the following:
        
        Topic: {topic}
        Post Type: {post_type}
        Industry: {industry}
        Tone: {tone}
        
        Requirements:
        - Make it professional yet engaging
        - Include valuable insights or takeaways
        - Structure it with clear paragraphs
        - Add a strong hook in the first line
        - Include a call-to-action for engagement
        - Use minimal but strategic emojis
        - Optimize for LinkedIn's professional audience
        
        Format the response as a complete LinkedIn post.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a LinkedIn content strategist. Create professional, engaging posts that drive meaningful business conversations and networking."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating LinkedIn post: {str(e)}"
    
    def generate_hashtags(self, platform, topic, niche, num_hashtags=20):
        prompt = f"""
        Generate {num_hashtags} relevant hashtags for {platform} about:
        
        Topic: {topic}
        Niche: {niche}
        
        Requirements:
        - Mix of popular and niche-specific hashtags
        - Include trending and evergreen hashtags
        - Vary hashtag sizes (high, medium, and low competition)
        - Make them relevant to the content and audience
        - Format as #hashtag
        
        Provide a mix of:
        - 5-7 high-reach hashtags (100k+ posts)
        - 8-10 medium-reach hashtags (10k-100k posts)
        - 5-7 niche hashtags (under 10k posts)
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a social media hashtag expert for {platform}. Generate strategic hashtag combinations that maximize reach and engagement."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.6
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating hashtags: {str(e)}"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📱 Social Media Caption Generator</h1>
        <p>AI-Powered Instagram & LinkedIn Content Creator</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for API key and settings
    with st.sidebar:
        st.header("🔑 Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        
        if not api_key:
            st.warning("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")
            st.stop()
        
        st.header("🎯 Content Settings")
        platform = st.selectbox("Choose Platform", ["Instagram", "LinkedIn", "Both"])
        
        # Initialize the bot
        try:
            bot = SocialMediaCaptionBot(api_key)
            st.success("✅ Bot initialized successfully!")
        except Exception as e:
            st.error(f"❌ Error initializing bot: {str(e)}")
            st.stop()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Content Generation")
        
        # Topic input
        topic = st.text_area("What's your content about?", 
                           placeholder="e.g., Launching a new product, sharing industry insights, motivational Monday...",
                           height=100)
        
        if platform in ["Instagram", "Both"]:
            st.subheader("📸 Instagram Settings")
            col_ig1, col_ig2 = st.columns(2)
            
            with col_ig1:
                ig_style = st.selectbox("Instagram Style", 
                    ["Casual & Fun", "Inspirational", "Educational", "Behind-the-scenes", "User-generated", "Promotional"])
                ig_audience = st.selectbox("Target Audience", 
                    ["General", "Young Adults (18-25)", "Professionals", "Parents", "Entrepreneurs", "Students"])
            
            with col_ig2:
                ig_cta = st.checkbox("Include Call-to-Action", value=True)
                ig_hashtags = st.checkbox("Generate Hashtags", value=True)
        
        if platform in ["LinkedIn", "Both"]:
            st.subheader("💼 LinkedIn Settings")
            col_li1, col_li2 = st.columns(2)
            
            with col_li1:
                li_type = st.selectbox("Post Type", 
                    ["Thought Leadership", "Industry News", "Personal Story", "Tips & Advice", "Company Update", "Question/Poll"])
                li_industry = st.text_input("Industry/Niche", placeholder="e.g., Technology, Marketing, Finance...")
            
            with col_li2:
                li_tone = st.selectbox("Tone", 
                    ["Professional", "Conversational", "Authoritative", "Inspiring", "Analytical"])
                li_hashtags = st.checkbox("Generate LinkedIn Hashtags", value=True)
        
        # Generate button
        if st.button("🚀 Generate Content", type="primary"):
            if not topic:
                st.error("Please enter a topic for your content!")
            else:
                with st.spinner("Generating amazing content..."):
                    # Instagram content
                    if platform in ["Instagram", "Both"]:
                        st.markdown("### 📸 Instagram Content")
                        
                        ig_caption = bot.generate_instagram_caption(topic, ig_style, ig_audience, ig_cta)
                        
                        st.markdown(f"""
                        <div class="generated-content">
                            <h4>📝 Instagram Caption:</h4>
                            <p style="white-space: pre-line;">{ig_caption}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if ig_hashtags:
                            ig_tags = bot.generate_hashtags("Instagram", topic, ig_audience)
                            st.markdown(f"""
                            <div class="hashtag-section">
                                <h4>🏷️ Instagram Hashtags:</h4>
                                <p>{ig_tags}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # LinkedIn content
                    if platform in ["LinkedIn", "Both"]:
                        st.markdown("### 💼 LinkedIn Content")
                        
                        li_post = bot.generate_linkedin_post(topic, li_type, li_industry, li_tone)
                        
                        st.markdown(f"""
                        <div class="generated-content">
                            <h4>📝 LinkedIn Post:</h4>
                            <p style="white-space: pre-line;">{li_post}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if li_hashtags:
                            li_tags = bot.generate_hashtags("LinkedIn", topic, li_industry)
                            st.markdown(f"""
                            <div class="hashtag-section">
                                <h4>🏷️ LinkedIn Hashtags:</h4>
                                <p>{li_tags}</p>
                            </div>
                            """, unsafe_allow_html=True)
    
    with col2:
        st.header("💡 Tips & Features")
        
        st.markdown("""
        <div class="platform-card">
            <h4>📸 Instagram Tips</h4>
            <ul>
                <li>Use 3-5 hashtags in caption</li>
                <li>Add 15-20 hashtags in first comment</li>
                <li>Include emojis for engagement</li>
                <li>Ask questions to boost comments</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="platform-card">
            <h4>💼 LinkedIn Tips</h4>
            <ul>
                <li>Start with a hook</li>
                <li>Use 2-3 relevant hashtags</li>
                <li>Add value to your network</li>
                <li>Encourage professional discussions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="platform-card">
            <h4>🎯 Best Practices</h4>
            <ul>
                <li>Post consistently</li>
                <li>Engage with your audience</li>
                <li>Use trending topics</li>
                <li>Test different content types</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        Made with ❤️ using OpenAI GPT-4 | Built for Social Media Success
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
