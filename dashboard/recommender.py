import pickle
import os
import streamlit as st


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


@st.cache_resource
def load_models():

    movies = pickle.load(
        open(
        os.path.join(BASE_DIR,"models","movies.pkl"),
        "rb"
        )
    )


    similarity = pickle.load(
        open(
        os.path.join(BASE_DIR,"models","similarity.pkl"),
        "rb"
        )
    )

    return movies, similarity
movies, similarity = load_models()

# -----------------------------
# Get Movie List
# -----------------------------
@st.cache_data(ttl=604800)
def get_movie_list():
    return sorted(movies["title"].tolist())

# -----------------------------
# Recommendation Function
# -----------------------------
@st.cache_data(ttl=604800)
def recommend(movie_name):

    movie_index = movies[movies["title"] == movie_name].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommendations = []

    for i in movie_list:

       recommendations.append(
    {
        "title": movies.iloc[i[0]]["title"],
        "vote_average": float(movies.iloc[i[0]]["vote_average"]),
        "popularity": float(movies.iloc[i[0]]["popularity"]),
        "similarity": round(i[1] * 100, 1)
    }
)

    return recommendations

@st.cache_data(ttl=604800)
def get_trending_movies(n=10):

    trending = movies.sort_values(
        by="popularity",
        ascending=False
    ).head(n)

    return trending[
        ["title", "vote_average", "popularity"]
    ].to_dict("records")

# -----------------------------
# Get Movies DataFrame
# -----------------------------
import pandas as pd

@st.cache_data(ttl=604800)
def get_movies_dataframe():

    df = pd.read_csv(
        os.path.join(BASE_DIR, "data", "raw", "movies.csv")
    )

    return df

