import streamlit as st
import pickle
import pandas as pd
import urllib.parse

# ================================
# Load Data
# ================================
movies = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies)
similarity = pickle.load(open("similarity.pkl", "rb"))
movies_list = movies["title"].values

# ================================
# Recommendation Function
# ================================
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list_sorted = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    for i in movies_list_sorted:
        recommended_movies.append(movies.iloc[i[0]]["title"])
    return recommended_movies


# ================================
# Streamlit Page Setup
# ================================
st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎥", layout="wide")

# ================================
# Custom CSS Styling
# ================================
st.markdown(
    """
    <style>
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    body {
        background: linear-gradient(-45deg, #1e1f26, #2d1b33, #251f44, #3c1a5b);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    .main-title {
        font-size: 52px;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #ff512f, #dd2476, #ffb703);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
        text-shadow: 0 0 20px rgba(255,255,255,0.2);
        animation: fadeIn 2s ease-in;
    }

    .stSelectbox label {
        font-size: 18px;
        color: #e2e2e2;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #ff512f, #dd2476);
        color: white;
        border: none;
        padding: 0.7em 1.6em;
        font-size: 16px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 15px rgba(255, 87, 34, 0.3);
    }

    div.stButton > button:hover {
        transform: scale(1.08);
        box-shadow: 0 0 25px rgba(221, 36, 118, 0.6);
    }

    .movie-card {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        margin: 12px;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
        text-align: center;
        transition: all 0.4s ease;
        animation: fadeUp 1.2s ease;
    }

    .movie-card:hover {
        transform: scale(1.05);
        background-color: rgba(255, 255, 255, 0.15);
    }

    .movie-title {
        font-size: 19px;
        font-weight: 600;
        color: #fdfdfd;
    }

    .movie-link {
        color: #ffb703 !important;
        text-decoration: none !important;
        transition: color 0.3s ease;
    }

    .movie-link:hover {
        color: #ff512f !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .footer {
        text-align: center;
        color: #ffb703;
        font-size: 17px;
        margin-top: 60px;
        padding: 15px;
        border-top: 1px solid rgba(255,255,255,0.1);
        font-weight: 600;
        animation: glow 2s infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 8px #ff512f; }
        to { text-shadow: 0 0 18px #dd2476; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================================
# App Layout
# ================================
st.markdown("<h1 class='main-title'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

selected_movie_name = st.selectbox("🎥 Choose a Movie:", movies_list)

if st.button("Get Recommendations"):
    recommended_movies = recommend(selected_movie_name)
    st.markdown("<h3 style='text-align:center; color:#ffb703;'>✨ Recommended Movies ✨</h3>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, movie in enumerate(recommended_movies):
        imdb_link = f"https://www.imdb.com/find/?q={urllib.parse.quote(movie)}&ref_=nv_sr_sm"
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class='movie-card'>
                    <a class='movie-link' href='{imdb_link}' target='_blank'>
                        🎥 <span class='movie-title'>{movie}</span>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

# ================================
# Footer
# ================================
st.markdown("<div class='footer'>🚀 Developed By <b>Ashish 😎</b></div>", unsafe_allow_html=True)
