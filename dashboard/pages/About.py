import streamlit as st
import os

css_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "style.css"
)

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

st.markdown("""
<div class="hero">
    <h1>ℹ️ About CineMatch AI</h1>
    <h3>AI Powered Movie Recommendation System</h3>
    <p>Built using Machine Learning, Streamlit and TMDB Dataset</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:

    st.markdown("""
<div class="about-box">
<h2>🎬 Project Overview</h2>

<p>
CineMatch AI is an intelligent movie recommendation system that suggests
movies based on similarity between films using Machine Learning.

The project combines recommendation algorithms with a modern interactive
dashboard to provide an engaging movie discovery experience.
</p>

</div>
""", unsafe_allow_html=True)

    st.header("✨ Features")

    st.markdown("""
- 🔍 Movie Search
- ❤️ Favorite Movies
- 🔥 Trending Movies
- 🎥 Official Trailer
- 📊 Analytics Dashboard
- 🎭 Genre Filtering
- ⭐ Rating Filtering
- 📅 Year Filtering
- 🤖 AI Based Recommendations
""")

with col2:

    st.markdown("""
<div class="about-side-card">

<h3>📌 Project Type</h3>

<p>🤖 Machine Learning</p>

<p>🎬 Recommendation System</p>

<p>📊 Interactive Dashboard</p>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.header("🧠 Recommendation Engine")

st.write("""
Recommendations are generated using **Content-Based Filtering**.

The similarity between movies is calculated using movie metadata such as:

- Genres
- Keywords
- Cast
- Crew
- Overview
- Popularity
""")

st.markdown("---")

st.header("🛠 Tech Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div class="about-box">
<h3>💻 Backend</h3>

• Python<br>
• Pandas<br>
• NumPy<br>
• Scikit-Learn
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="about-box">
<h3>🎨 Frontend</h3>

• Streamlit<br>
• HTML<br>
• CSS<br>
• Plotly
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div class="about-box">
<h3>📂 Dataset</h3>

• TMDB Dataset<br>
• YouTube API<br>
• Movie Posters API
</div>
""", unsafe_allow_html=True)

st.header("📁 Project Structure")

tree = """
Movie_recommendation_system/
│
├── assets/
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── notebooks/
│
├── dashboard/
│   ├── Home.py
│   ├── components.py
│   ├── recommender.py
│   ├── analytics.py
│   ├── details.py
│   ├── poster.py
│   ├── youtube_api.py
│   ├── style.css
│   └── pages/
│
├── requirements.txt
├── README.md
└── .gitignore
"""

st.markdown(f"""
<div class="about-box">
<div class="project-tree">
{tree}
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.header("🚀 Future Improvements")

st.markdown("""
- 👤 User Login
- 🌙 Dark / Light Theme
- 🎭 Mood Based Recommendation
- 🎙 Voice Search
- 🤖 AI Chatbot
- 🎬 Watchlist
- ⭐ User Ratings
- ☁ Cloud Deployment
""")

st.markdown("---")

st.header("👩‍💻 Developer")

st.markdown("""
**Developed by Karishma**

B.Tech Artificial Intelligence & Data Science

Machine Learning • Data Science • Python • Streamlit
""")

