from collections import Counter
import plotly.express as px
import streamlit as st
from details import get_movie_details
from recommender import get_movie_list

@st.cache_data(ttl=604800)
def rating_distribution(df):
    
    fig = px.histogram(
        df,
        x="vote_average",
        nbins=20,
        title="⭐ Movie Rating Distribution",
        color_discrete_sequence=["#E50914"]
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f1117",
        plot_bgcolor="#181818",
        title_font=dict(
                    size=22,
                    color="white")
    )

    return fig
@st.cache_data(ttl=604800)
def top_popular_movies_chart(df):

    top_movies = (
        df.sort_values(
            by="popularity",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top_movies,
        x="popularity",
        y="title",
        orientation="h",
        title="🔥 Top 10 Most Popular Movies",
        color="popularity",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f1117",
        plot_bgcolor="#181818",
        title_x=0.5,
        title_font=dict(
            size=22,
            color="white"
        ),
        yaxis=dict(
            autorange="reversed"
        ),
        coloraxis_showscale=False
    )

    return fig

@st.cache_data(ttl=604800)
def genre_distribution_chart():

    genre_counter = Counter()

    movie_list = get_movie_list()

    for movie in movie_list:

        details = get_movie_details(movie)

        if details is None:
            continue

        genres = details["genres"]

        genres = genres.replace("|", " ").split()

        for genre in genres:
            genre_counter[genre] += 1

    top_genres = genre_counter.most_common(10)

    labels = [g[0] for g in top_genres]
    values = [g[1] for g in top_genres]

    fig = px.pie(
        names=labels,
        values=values,
        title="🎭 Top 10 Movie Genres",
        hole=0.45
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f1117",
        plot_bgcolor="#181818",
        title_x=0.5,
        title_font=dict(
            size=22,
            color="white"
        ),
        legend_title="Genres"
    )

    return fig

@st.cache_data(ttl=604800)
def movies_by_year_chart(df):

    year_df = df.copy()

    year_df["release_year"] = (
        year_df["release_date"]
        .astype(str)
        .str[:4]
    )

    year_df = (
        year_df.groupby("release_year")
        .size()
        .reset_index(name="count")
    )

    year_df = year_df[
        year_df["release_year"] != "nan"
    ]

    fig = px.line(
        year_df,
        x="release_year",
        y="count",
        title="📅 Movies Released Per Year",
        markers=True
    )

    fig.update_traces(
        line_color="#E50914",
        marker_color="#E50914"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f1117",
        plot_bgcolor="#181818",
        title_x=0.5,
        title_font=dict(
            size=22,
            color="white"
        ),
        xaxis_title="Release Year",
        yaxis_title="Number of Movies"
    )

    return fig


