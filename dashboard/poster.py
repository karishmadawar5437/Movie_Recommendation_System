import os
import hashlib
import requests
import streamlit as st

from config import OMDB_API_KEY

PLACEHOLDER = "https://placehold.co/300x450/png?text=Movie"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CACHE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "cache",
    "posters"
)

os.makedirs(CACHE_DIR, exist_ok=True)


@st.cache_data(ttl=604800)
def get_poster(movie_title):

    filename = hashlib.md5(
        movie_title.lower().encode()
    ).hexdigest() + ".txt"

    cache_file = os.path.join(
        CACHE_DIR,
        filename
    )

    # -------------------------
    # Check local cache first
    # -------------------------

    if os.path.exists(cache_file):

        with open(cache_file, "r") as f:

            return f.read().strip()

    url = "https://www.omdbapi.com/"

    try:

        # Exact title search
        response = requests.get(
            url,
            params={
                "apikey": OMDB_API_KEY,
                "t": movie_title
            },
            timeout=(3, 10)
        )

        data = response.json()

        if data.get("Response") == "True":

            poster = data.get("Poster")

            if poster and poster != "N/A":

                with open(cache_file, "w") as f:
                    f.write(poster)

                return poster

        # -------------------------
        # Fallback search
        # -------------------------

        response = requests.get(
            url,
            params={
                "apikey": OMDB_API_KEY,
                "s": movie_title
            },
            timeout=(3, 10)
        )

        data = response.json()

        if data.get("Response") == "True":

            imdb_id = data["Search"][0]["imdbID"]

            response = requests.get(
                url,
                params={
                    "apikey": OMDB_API_KEY,
                    "i": imdb_id
                },
                timeout=(3, 10)
            )

            movie = response.json()

            poster = movie.get("Poster")

            if poster and poster != "N/A":

                with open(cache_file, "w") as f:
                    f.write(poster)

                return poster

    except Exception as e:

        print("Poster Error:", e)

    return PLACEHOLDER
