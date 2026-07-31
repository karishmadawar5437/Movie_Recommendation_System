import streamlit as st

from details import get_movie_details
from poster import get_poster
from Home import poster_dict, LOCAL_POSTERS
from components import movie_card

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

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="Favorites",
    page_icon="❤️",
    layout="wide"
)

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ---------------------------------------------------
# Hero
# ---------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>❤️ MY FAVOURITES</h1>
    <h3>Your Personal Movie Collection</h3>
    <p>Save movies you love and access them anytime.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Empty Favorites
# ---------------------------------------------------

if len(st.session_state.favorites) == 0:
    st.info("❤️ No favorite movies yet.")
    st.stop()

# ---------------------------------------------------
# Search
# ---------------------------------------------------

st.subheader("🔍 Search Favourites")

search = st.text_input(
    "Search movie",
    placeholder="Type movie name..."
)

# ---------------------------------------------------
# Filter Favorites
# ---------------------------------------------------

favorite_movies = st.session_state.favorites

if search:
    favorite_movies = [
        movie
        for movie in favorite_movies
        if search.lower() in movie.lower()
    ]

# ---------------------------------------------------
# Statistics
# ---------------------------------------------------

total_movies = len(st.session_state.favorites)

ratings = []

genres = set()

for movie in st.session_state.favorites:

    details = get_movie_details(movie)

    if details:

        ratings.append(details["rating"])

        genres.update(details["genres"].split())

avg_rating = round(sum(ratings) / len(ratings), 1)

total_movies = len(st.session_state.favorites)

ratings = []
genres = set()

for movie in st.session_state.favorites:

    details = get_movie_details(movie)

    if details:

        ratings.append(details["rating"])

        genres.update(details["genres"].split())

avg_rating = round(sum(ratings) / len(ratings), 1)

total_genres = len(genres)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="analytics-card">
        <div class="metric-icon">❤️</div>
        <div class="metric-label">Favorites</div>
        <div class="metric-number">{total_movies}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="analytics-card">
        <div class="metric-icon">⭐</div>
        <div class="metric-label">Average Rating</div>
        <div class="metric-number">{avg_rating}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="analytics-card">
        <div class="metric-icon">🎭</div>
        <div class="metric-label">Genres</div>
        <div class="metric-number">{total_genres}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# Movie Cards
# ---------------------------------------------------

cols = st.columns(4)

for index, movie in enumerate(favorite_movies):

    details = get_movie_details(movie)

    if details is None:
        continue

    poster = LOCAL_POSTERS.get(
        movie,
        poster_dict.get(movie)
    )

    if not poster:
        poster = get_poster(movie)

    with cols[index % 5]:

        movie_card(
            title=movie,
            rating=round(details["rating"], 1),
            popularity=round(details["popularity"], 1),
            similarity=100,
            genre=details["genres"],
            year=details["release_year"],
            overview=details["overview"],
            poster=poster,
            card_key=f"favorite_{movie}"
        )

        if st.button(
            "🗑 Remove",
            key=f"remove_{movie}"
        ):

            st.session_state.favorites.remove(movie)

            st.rerun()

st.divider()

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.markdown("""
<div class="footer">
<p>Your personalized collection powered by CineMatch AI</p>
</div>
""", unsafe_allow_html=True)

