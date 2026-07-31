from youtube_api import get_trailer
import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOCAL_POSTERS = {

    "24 7: Twenty Four Seven": os.path.join(
        BASE_DIR,
        "assets",
        "24_7_movie.jpg"
    ),

    "Star Wars: Clone Wars: Volume 1": os.path.join(
        BASE_DIR,
        "assets",
        "star_wars_clone_wars_volume1.jpg"
    )

}

print(os.path.exists(LOCAL_POSTERS["24 7: Twenty Four Seven"]))
print(LOCAL_POSTERS["24 7: Twenty Four Seven"])

@st.cache_resource
def load_posters():

    poster_file = os.path.join(
        BASE_DIR,
        "data",
        "processed",
        "posters.csv"
    )

    posters = pd.read_csv(poster_file)

    posters["poster"] = posters["poster"].fillna(
    "https://placehold.co/300x450/png?text=Movie"
)

    return dict(zip(posters["title"], posters["poster"]))

poster_dict = load_posters()
print("Movie exists:", "24 7: Twenty Four Seven" in poster_dict)
print("Poster value:", repr(poster_dict.get("24 7: Twenty Four Seven")))
print("Type:", type(poster_dict.get("24 7: Twenty Four Seven")))

from analytics import (
    rating_distribution,
    top_popular_movies_chart,
    genre_distribution_chart,
    movies_by_year_chart
)

from recommender import get_movies_dataframe

import time

start = time.time()

# ----------------------------
# Page Config
# ----------------------------

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide"
)
if "favorites" not in st.session_state:
    st.session_state.favorites = []

from recommender import (
    get_movie_list,
    recommend,
    get_trending_movies
)

from details import get_movie_details

from components import (
    hero_section,
    search_section,
    movie_card,
    footer,
    loading_progress,
)

import os

css_path = os.path.join(
    os.path.dirname(__file__),
    "style.css"
)

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ----------------------------
# Hero
# ----------------------------

hero_section()

# ----------------------------
# Sidebar Filters
# ----------------------------

st.sidebar.title("🎬 Filters")

start = time.time()
movies_df = get_movies_dataframe()

movies_df["release_year"] = (
    movies_df["release_date"]
    .astype(str)
    .str[:4]
)


all_genres = []

for genre_string in movies_df["genres"]:

    genres = str(genre_string).split()

    all_genres.extend(genres)

genre_list = sorted(list(set(all_genres)))

selected_genre = st.sidebar.selectbox(

    "🎭 Genre",

    ["All"] + genre_list
)

minimum_rating = st.sidebar.slider(

    "⭐ Minimum Rating",

    0.0,

    10.0,

    5.0,

    0.5
)

years = sorted(

    movies_df["release_year"]

    .dropna()

    .astype(int)

    .unique()

)

selected_year = st.sidebar.selectbox(

    "📅 Release Year",

    ["All"] + list(years)
)

minimum_popularity = st.sidebar.slider(

    "🔥 Minimum Popularity",

    0,

    int(movies_df["popularity"].max()),

    0
)
filtered_df = movies_df.copy()
if selected_genre != "All":

    filtered_df = filtered_df[
        filtered_df["genres"].str.contains(
            selected_genre,
            case=False,
            na=False
        )
    ]

filtered_df = filtered_df[
    filtered_df["vote_average"] >= minimum_rating
]

if selected_year != "All":

    filtered_df = filtered_df[
        filtered_df["release_year"].astype(int) == int(selected_year)
    ]

filtered_df = filtered_df[
    filtered_df["popularity"] >= minimum_popularity
]

st.sidebar.markdown("---")

st.sidebar.success(

    f"🎬 {len(filtered_df)} movies found"
)

st.sidebar.markdown("---")
st.sidebar.subheader("❤️ Favorites")

if st.session_state.favorites:

    for movie in st.session_state.favorites.copy():

        col1, col2 = st.sidebar.columns([4, 1])

        with col1:
            st.write(f"❤️ {movie}")

        with col2:
            if st.button(
                "❌",
                key=f"remove_{movie}"
            ):
                st.session_state.favorites.remove(movie)
                st.rerun()

else:

    st.sidebar.caption("No favorite movies yet.") 

st.divider()
st.subheader("🔥 Trending Movies")

from poster import get_poster

trending = get_trending_movies(5)

cols = st.columns(5)

for col, movie in zip(cols, trending):

    details = get_movie_details(movie["title"])

    poster = LOCAL_POSTERS.get(
        movie["title"],
        poster_dict.get(movie["title"])
    )

    if pd.isna(poster) or poster == "":
        poster = get_poster(movie["title"])

    with col:
        movie_card(
            title=movie["title"],
            rating=round(movie["vote_average"], 1),
            popularity=round(movie["popularity"], 1),
            similarity=100,
            genre=details["genres"] if details else "Unknown",
            year=details["release_year"] if details else "N/A",
            overview=details["overview"] if details else "",
            poster=poster,
            card_key=f"trending_{movie['title']}"
                    )

print("Trending:", time.time() - start)        
# ----------------------------
# Search
# ----------------------------

selected_movie, recommend_clicked = search_section(
    get_movie_list()
)
start = time.time()
selected_details = get_movie_details(selected_movie)

selected_poster = LOCAL_POSTERS.get(
    selected_movie,
    poster_dict.get(selected_movie)
)

print("Selected movie:", selected_movie)
print("Selected poster:", selected_poster)

if (
    pd.isna(selected_poster)
    or selected_poster == ""
):
    from poster import get_poster
    selected_poster = get_poster(selected_movie)

    from poster import get_poster
    selected_poster = get_poster(selected_movie)

trailer = get_trailer(
    selected_movie,
    selected_details["release_year"]
)

st.divider()

st.markdown("## 🎥 Selected Movie")


left, right = st.columns([1, 2])

# ---------------- LEFT COLUMN ----------------

with left:
    print("Selected movie:", selected_movie)
    print("Selected poster:", repr(selected_poster))
    st.image(selected_poster, use_container_width=True)

# ---------------- RIGHT COLUMN ----------------

with right:

    # Movie Title
    st.markdown(
    f"""
    <h1 style="
        color:white;
        font-size:46px;
        margin-bottom:10px;
    ">
        🎬 {selected_movie}
    </h1>
    """,
    unsafe_allow_html=True
)

    # Metrics
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="metric-icon">⭐</div>
            <div class="metric-label">Rating</div>
            <div class="metric-number">{round(float(selected_details["rating"]),1)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="metric-icon">🔥</div>
            <div class="metric-label">Popularity</div>
            <div class="metric-number">{round(float(selected_details["popularity"]),1)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="metric-icon">📅</div>
            <div class="metric-label">Year</div>
            <div class="metric-number">{selected_details["release_year"]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Genre
        # Genre
    st.markdown("### 🎭 Genre")

    genres = selected_details["genres"].split()

    genre_html = ""

    for g in genres:
        genre_html += f'<span class="genre-tag">{g}</span> '

    st.markdown(
        genre_html,
        unsafe_allow_html=True
    )
    
      # Story
    st.markdown("### 📝 Story")

    st.markdown(
        f"""
        <div class="story-box">
            {selected_details["overview"]}
        </div>
        """,
        unsafe_allow_html=True
    )
    if trailer:

        st.write("")

        st.markdown("### ▶ Official Trailer")

        st.video(trailer)

st.divider()
st.subheader("❤️ Recommended Movies")
   

# ----------------------------
# Recommendation Section
# ----------------------------
from poster import get_poster

loading_progress()

recommendations = recommend(selected_movie)

cols = st.columns(5)

for col, movie in zip(cols, recommendations):

    details = get_movie_details(movie["title"])

    poster = LOCAL_POSTERS.get(
        movie["title"],
        poster_dict.get(movie["title"])
    )

    if pd.isna(poster) or poster == "":
        poster = get_poster(movie["title"])

    with col:

        movie_card(
            title=movie["title"],
            rating=round(movie["vote_average"], 1),
            popularity=round(movie["popularity"], 1),
            similarity=movie["similarity"],
            genre=details["genres"] if details else "Unknown",
            year=details["release_year"] if details else "N/A",
            overview=details["overview"] if details else "",
            poster=poster,
            card_key=f"recommend_{movie['title']}"
            
        )

st.divider()
st.header("📊 Movie Analytics")

start = time.time()
movies_df = get_movies_dataframe()

# ============================
# KPI Cards
# ============================

total_movies = len(movies_df)

avg_rating = round(
    movies_df["vote_average"].mean(),
    1
)

total_genres = (
    movies_df["genres"]
    .astype(str)
    .str.replace("|", " ")
    .str.split()
    .explode()
    .nunique()
)

start_year = (
    movies_df["release_date"]
    .astype(str)
    .str[:4]
    .min()
)

end_year = (
    movies_df["release_date"]
    .astype(str)
    .str[:4]
    .max()
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="analytics-card">
        <div class="metric-icon">🎬</div>
        <div class="metric-label">Movies</div>
        <div class="metric-number">{total_movies}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="analytics-card">
        <div class="metric-icon">⭐</div>
        <div class="metric-label">Average Rating</div>
        <div class="metric-number">{avg_rating}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="analytics-card">
        <div class="metric-icon">🎭</div>
        <div class="metric-label">Genres</div>
        <div class="metric-number">{total_genres}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="analytics-card">
        <div class="metric-icon">📅</div>
        <div class="metric-label">Years</div>
        <div class="metric-number">{start_year}-{end_year}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

col1, col2 = st.columns(2)

with col1:

    fig = rating_distribution(movies_df)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="rating_chart"
    )

with col2:

    fig2 = top_popular_movies_chart(movies_df)

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="popular_chart"
    )

st.write("")

col3, col4 = st.columns(2)

with col3:

    fig3 = genre_distribution_chart()

    st.plotly_chart(
        fig3,
        use_container_width=True,
        key="genre_chart"
    )

with col4:

    fig4 = movies_by_year_chart(movies_df)

    st.plotly_chart(
        fig4,
        use_container_width=True,
        key="year_chart"
    )


# ----------------------------
# Filter Results
# ----------------------------

st.divider()

st.subheader("🎯 Filter Results")

st.dataframe(

    filtered_df[
        [
            "title",
            "genres",
            "vote_average",
            "popularity",
            "release_year"
        ]
    ],

    use_container_width=True
)

st.divider()
footer()

