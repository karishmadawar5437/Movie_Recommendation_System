import pandas as pd
import os
import streamlit as st


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


@st.cache_data(ttl=604800)
def load_movies():

    df = pd.read_csv(
        os.path.join(BASE_DIR,"data","raw","movies.csv")
    )

    df["title"] = (
        df["title"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return df


movies_df = load_movies()
MOVIE_LOOKUP = {}

for _, row in movies_df.iterrows():

    MOVIE_LOOKUP[row["title"]] = {
        "genres": row["genres"],
        "overview": row["overview"],
        "release_year": str(row["release_date"])[:4],
        "rating": row["vote_average"],
        "popularity": row["popularity"]
    }

@st.cache_data(ttl=604800)
def get_movie_details(title):

    return MOVIE_LOOKUP.get(
        title.strip().lower(),
        None
    )

