import streamlit as st
import pickle 
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
from pathlib import Path
from dotenv import load_dotenv

# configure retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
# 500: Internal Server Error
# 502: Bad Gateway
# 503: Service Unavailable
# 504: Gateway Timeout
http = requests.Session()
http.mount("https://", HTTPAdapter(max_retries=retry_strategy))

st.title("Movie Recommender System")

# Load data
try:
    current_dir = Path(__file__).parent
    movies_list = pickle.load(open(current_dir / 'movie_list.pkl', 'rb'))
    similarity = pickle.load(open(current_dir / 'similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading files: {str(e)}")
    st.stop()

# Get API key from Streamlit secrets in production, or from .env in development
if 'TMDB_API_KEY' in st.secrets:
    api_key = st.secrets['TMDB_API_KEY']
else:
    load_dotenv()
    api_key = os.getenv("TMDB_API_KEY")    

if not api_key:
    st.error("TMDB API key is not configured. Please check your environment variables or secrets.")
    st.stop()

def fetch_movie_details(movie_id):
    if not api_key:
        return {
            'poster_path': "https://via.placeholder.com/500x750?text=No+API+Key",
            'overview': "API key not configured",
            'release_date': "Unknown",
            'rating': 0.0,
            'runtime': "N/A"
        }
    
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        response = http.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        poster_path = data.get('poster_path')
        poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else "https://via.placeholder.com/500x750?text=No+Image+Available"
        
        return {
            'poster_path': poster_url,
            'overview': data.get('overview', 'No overview available'),
            'release_date': data.get('release_date', 'Release date unknown'),
            'rating': round(data.get('vote_average', 0), 1),
            'runtime': data.get('runtime', 'N/A')
        }
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not fetch details for movie ID {movie_id}. Error: {str(e)}")
        return {
            'poster_path': "https://via.placeholder.com/500x750?text=No+Image+Available",
            'overview': "Unable to fetch movie details",
            'release_date': "Unknown",
            'rating': 0.0,
            'runtime': "N/A"
        }

def recommend(movie):
    try:
        movie_index = movies_list[movies_list['title'] == movie].index[0]
        distances = similarity[movie_index]
        
        # Sort by similarity score (second element), not by index
        movies_list_recommended = sorted(
            list(enumerate(distances)), 
            key=lambda x: x[1],  # Sort by similarity score
            reverse=True
        )[1:6]  # Skip the first (the movie itself)
        
        recommended_names = []
        recommended_details = []
        
        for i in movies_list_recommended:
            movie_id = movies_list.iloc[i[0]].movie_id
            recommended_names.append(movies_list.iloc[i[0]].title)
            recommended_details.append(fetch_movie_details(movie_id))
        return recommended_names, recommended_details
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return [], []

# Movie selection dropdown
selected_movie = st.selectbox(
    'Select a movie you like',
    movies_list['title'].values
)

# Show recommendations button
if st.button('Show Recommendations'):
    with st.spinner("Finding similar movies..."):
        names, details = recommend(selected_movie)
        
        if not names:
            st.error("Could not generate recommendations. Please try again later.")
        else:
            for i in range(len(names)):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.image(details[i]['poster_path'], width=170)
                
                with col2:
                    st.markdown(f"### {names[i]}")
                    st.markdown(
                        f"**🎬 Release Date:** {details[i]['release_date']} | "
                        f"**⭐ Rating:** {details[i]['rating']}/10 | "
                        f"**⏱ Runtime:** {details[i]['runtime']} min"
                    )
                    st.markdown(f"**Overview:** {details[i]['overview'][:200]}...")
                
                st.markdown("---")