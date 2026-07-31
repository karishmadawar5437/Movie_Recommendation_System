import os
import hashlib
import requests
import streamlit as st

from config import YOUTUBE_API_KEY

# --------------------------------------------------
# Base Directory
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CACHE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "cache",
    "trailers"
)

os.makedirs(CACHE_DIR, exist_ok=True)


# --------------------------------------------------
# Trailer Function
# --------------------------------------------------

@st.cache_data(ttl=604800)
def get_trailer(movie_title, release_year):

    # -----------------------------
    # Create cache filename
    # -----------------------------

    filename = hashlib.md5(
        f"{movie_title}_{release_year}".lower().encode()
    ).hexdigest() + ".txt"

    cache_file = os.path.join(
        CACHE_DIR,
        filename
    )

    # -----------------------------
    # Load trailer from cache
    # -----------------------------

    if os.path.exists(cache_file):

        with open(cache_file, "r") as f:

            trailer = f.read().strip()

            if trailer:
                return trailer

    # -----------------------------
    # Search YouTube
    # -----------------------------

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {

        "part": "snippet",

        "q": f"{movie_title} {release_year} official trailer",

        "key": YOUTUBE_API_KEY,

        "maxResults": 5,

        "type": "video"

    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        for item in data.get("items", []):

            title = item["snippet"]["title"].lower()

            channel = item["snippet"]["channelTitle"].lower()

            # Ignore wrong videos

            if (
                "last airbender" in title
                or "series" in title
                or "game" in title
            ):
                continue

            if (
                "official trailer" in title
                or "official trailer" in channel
                or "trailer" in title
            ):

                video_id = item["id"]["videoId"]

                trailer_url = (
                    "https://www.youtube.com/watch?v="
                    + video_id
                )

                # -----------------------------
                # Save trailer locally
                # -----------------------------

                with open(cache_file, "w") as f:

                    f.write(trailer_url)

                return trailer_url

    except Exception as e:

        print("Trailer Error:", e)

    return None

