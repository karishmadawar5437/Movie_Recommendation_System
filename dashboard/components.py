import time
import pandas as pd
import streamlit as st

from youtube_api import get_trailer


# ==========================================
# HERO SECTION
# ==========================================

def hero_section():

    st.markdown(
        """
        <div class="hero">
            <h1>🎬 MOVIE RECOMMENDATION SYSTEM</h1>
            <h3>Discover Your Next Favourite Movie</h3>
            <p>
                Powered by Artificial Intelligence • Personalized Recommendations
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# SEARCH SECTION
# ==========================================

def search_section(movie_list):

    st.subheader("🔍 Search Movie")

    selected_movie = st.selectbox(
        "Choose a Movie",
        movie_list
    )

    recommend_clicked = st.button(
        "🎬 Recommend",
        use_container_width=True
    )

    return selected_movie, recommend_clicked


# ==========================================
# TRAILER DIALOG
# ==========================================

@st.dialog("🎥 Official Trailer")
def trailer_dialog(title, trailer_url):

    st.markdown(f"## 🎬 {title}")

    if trailer_url:

        st.video(trailer_url)

    else:

        st.warning("Trailer not available.")

# ==========================================
# MOVIE CARD
# ==========================================

def movie_card(
    title,
    rating,
    popularity,
    similarity,
    genre,
    year,
    poster,
    overview="",
    favorite=False,
    card_key=""
):

    # -----------------------------
    # Poster
    # -----------------------------

    if (
        poster is None
        or pd.isna(poster)
        or not isinstance(poster, str)
        or poster.strip() == ""
        or poster == "N/A"
    ):
        poster = "https://placehold.co/300x450/png?text=Movie"

    if "favorites" not in st.session_state:
        st.session_state.favorites = []

    with st.container(border=True):

        st.image(
            poster,
            use_container_width=True
        )

        st.markdown(f"### {title}")

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                f"""
                <div class="small-badge">
                    ⭐ {rating}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="small-badge">
                    🔥 {popularity}
                </div>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------
        # Genres
        # -----------------------------

        genre_html = ""

        for g in str(genre).split()[:3]:

            genre_html += f'<span class="genre-tag">{g}</span> '

        st.markdown(
            genre_html,
            unsafe_allow_html=True
        )

        st.markdown(
            f"<p style='color:#aaaaaa;'>📅 {year}</p>",
            unsafe_allow_html=True
        )

        # -----------------------------
        # Overview
        # -----------------------------

        if overview:

            short = (
                overview[:120] + "..."
                if len(overview) > 120
                else overview
            )

        else:

            short = "No overview available."

        st.markdown(
            f"""
            <div class="recommend-story">
                {short}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # -----------------------------
        # Favorite Button
        # -----------------------------

        if title not in st.session_state.favorites:

            if st.button(
                "❤️ Add to Favorites",
                key=f"fav_{title}_{card_key}",
                use_container_width=True
            ):

                st.session_state.favorites.append(title)

                st.rerun()

        else:

            if st.button(
                "💔 Remove Favorite",
                key=f"remove_{title}_{card_key}",
                use_container_width=True
            ):

                st.session_state.favorites.remove(title)

                st.rerun()

        # -----------------------------
        # Trailer
        # -----------------------------

        trailer = get_trailer(title, year)

        if st.button(
            "▶ Watch Trailer",
            key=f"trailer_{title}_{card_key}",
            use_container_width=True
        ):

            trailer_dialog(title, trailer)

        # -----------------------------
        # View More
        # -----------------------------

        with st.expander("📖 View More Details"):

            st.markdown(f"**⭐ Rating:** {rating}")

            st.markdown(f"**🔥 Popularity:** {popularity}")

            st.markdown(f"**🎯 Similarity:** {similarity}%")

            st.markdown(f"**🎭 Genre:** {genre}")

            st.markdown(f"**📅 Release Year:** {year}")

            st.markdown("### 📝 Story")

            st.write(overview)

# ==========================================
# FOOTER
# ==========================================

def footer():

    st.markdown(
        """
        <div class="footer">
            <h3>🎬 CineMatch AI</h3>
            <p>AI Powered Movie Recommendation Dashboard</p>
            <p>Built with ❤️ using Python • Streamlit • Machine Learning • Plotly</p>
            <p>Developed by <b>Karishma</b></p>
            <p style="font-size:14px;color:#888;">
            © 2026 CineMatch AI • All Rights Reserved
            </p>
            <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# LOADING ANIMATION
# ==========================================

def loading_progress():

    progress = st.progress(0)

    status = st.empty()

    steps = [

        "🔍 Searching similar movies...",

        "🎬 Loading posters...",

        "📖 Fetching movie details...",

        "🎥 Loading trailers...",

        "🤖 AI is preparing recommendations..."
    ]

    for i, step in enumerate(steps):

        status.info(step)

        progress.progress((i + 1) * 20)

        time.sleep(0.20)

    status.empty()

    progress.empty()



