# 🎬 CineMatch AI

An AI-powered Movie Recommendation System built with **Python**, **Streamlit**, and **Machine Learning**.

CineMatch AI recommends movies based on content similarity and provides rich movie information including posters, trailers, analytics, favorites, and interactive dashboards.

---

## 🚀 Features

- 🔍 Search any movie instantly
- ❤️ Add & remove favorite movies
- 🎬 AI-powered movie recommendations
- 🎥 Watch official trailers
- 🖼 Movie posters
- 📊 Interactive analytics dashboard
- 🎭 Genre filtering
- ⭐ Rating filtering
- 📅 Release year filtering
- 🔥 Popularity filtering
- 📈 Plotly visualizations
- Modern Netflix-inspired UI

---

## 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-Learn
- Plotly
- Requests
- OMDb API
- YouTube Search API

---

## 📂 Project Structure

```
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
```

---

## 🎯 Machine Learning

The recommendation engine uses

- Content-Based Filtering
- Cosine Similarity
- Feature Engineering
- Movie Metadata

---

## 📊 Dashboard

The application provides

- Trending Movies
- Recommended Movies
- Rating Distribution
- Genre Distribution
- Popular Movies
- Movies by Release Year

---

## 📸 Screenshots

### Home Page

![Home](imaages/home.png)

---

### Search

![Search](images/search.png)

---

### Recommendations

![Recommendation](images/recommendations.png)

---

### Analytics Dashboard

![Analytics](images/analytics.png)

---

### Favorites

![Favorites](images/favorites.png)

---

### About Page

![About](images/about.png)

---

## ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/CineMatch-AI.git
```

Go to project

```bash
cd CineMatch-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Streamlit

```bash
streamlit run dashboard/Home.py
```

---

## 🔑 Environment Variables

Create a file named

```
config.py
```

Add your API keys

```python
OMDB_API_KEY = "YOUR_API_KEY"
YOUTUBE_API_KEY = "YOUR_API_KEY"
```

---

## 📈 Future Improvements

- User Login
- Collaborative Filtering
- Deep Learning Recommendation
- User Ratings
- Watchlist
- Cloud Deployment

---

## 👩‍💻 Developer

**Karishma**

Built with ❤️ using Python & Streamlit.

---