# 🎬 MovieMate — Smart Movie Recommendations

> **Your personal movie recommendation engine powered by Machine Learning.**

🌐 **Live App:** [https://moviemate-web.streamlit.app/](https://moviemate-web.streamlit.app/)

---

## 📌 Overview

MovieMate is a content-based movie recommendation system that suggests similar movies based on a selected title. It uses natural language processing and cosine similarity to find movies with similar plots, genres, cast, crew, and keywords from a dataset of ~5,000 movies.

The project includes:
- A **Jupyter Notebook** (`movie_rec_sys.ipynb`) for data preprocessing, feature engineering, and model building.
- A **Streamlit web app** (`app.py`) that serves the recommendation engine with a clean, interactive UI — complete with movie posters, ratings, and overviews fetched from the TMDB API.

---

## ✨ Features

- 🔍 **Search & Select** — Choose any movie from a dropdown of ~5,000 titles.
- 🎯 **Top 5 Recommendations** — Get the five most similar movies instantly.
- 🖼️ **Movie Posters** — High-quality poster images via the TMDB API.
- ⭐ **Ratings & Details** — View release date, rating (out of 10), and runtime for each recommendation.
- 📖 **Overviews** — Brief plot summaries for every recommended movie.
- 🔄 **Retry-Resilient** — Built-in HTTP retry strategy for robust API calls.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / App** | [Streamlit](https://streamlit.io/) |
| **Language** | Python 3.12+ |
| **ML / NLP** | scikit-learn (CountVectorizer, Cosine Similarity), NLTK (SnowballStemmer) |
| **Data** | Pandas, TMDB 5000 Movies & Credits datasets |
| **API** | [TMDB (The Movie Database) API v3](https://www.themoviedb.org/documentation/api) |
| **Deployment** | [Streamlit Cloud](https://streamlit.io/cloud) |

---

## 🏗️ How It Works

```
TMDB 5000 Dataset
       │
       ▼
┌─────────────────────┐
│  Data Preprocessing  │  Merge movies + credits, extract genres,
│  (Jupyter Notebook)  │  keywords, top 4 cast, director
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Feature Engineering │  Combine all features into a single
│  "tags" column       │  text column per movie
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Vectorization       │  CountVectorizer (5000 features,
│                      │  English stop words removed)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Similarity Matrix   │  Cosine similarity between all
│                      │  movie vectors
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Streamlit App       │  User selects a movie → top 5
│  (app.py)            │  similar movies displayed with
│                      │  posters & details from TMDB API
└─────────────────────┘
```

### ML Pipeline (Notebook)

1. **Load** the TMDB 5000 Movies and Credits CSV datasets.
2. **Merge** both datasets on the movie title.
3. **Select** relevant columns: `movie_id`, `title`, `overview`, `genres`, `keywords`, `cast`, `crew`.
4. **Extract** genre names, keyword names, top 4 cast members, and director name from JSON-like strings using `ast.literal_eval`.
5. **Combine** all text features into a single `tags` column per movie.
6. **Vectorize** the tags using `CountVectorizer` with a max of 5,000 features and English stop word removal.
7. **Stem** words using NLTK's `SnowballStemmer` for better matching.
8. **Compute** a cosine similarity matrix across all movie vectors.
9. **Export** the processed movie list and similarity matrix as pickle files (`movie_list.pkl`, `similarity.pkl`).

---

## 📂 Project Structure

```
MovieMate-Smart-Movie-Recommendations/
├── app.py                    # Streamlit web application
├── movie_rec_sys.ipynb       # ML pipeline notebook
├── movie_list.pkl            # Serialized movie dataframe
├── similarity.pkl            # Serialized cosine similarity matrix
├── tmdb_5000_movies.csv      # TMDB movies dataset
├── tmdb_5000_credits.csv     # TMDB credits dataset
├── requirements.txt          # Python dependencies
├── .gitignore                # Ignored files
└── README.md                 # This file
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [TMDB API Key](https://www.themoviedb.org/settings/api) (free to obtain)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/MovieMate-Smart-Movie-Recommendations.git
   cd MovieMate-Smart-Movie-Recommendations
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your TMDB API key**

   Create a `.env` file in the project root:
   ```
   TMDB_API_KEY=your_api_key_here
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`.

### (Optional) Rebuild the Model

If you want to retrain the model with fresh data or modifications:

1. Open `movie_rec_sys.ipynb` in Jupyter Notebook / JupyterLab.
2. Update the CSV file paths to your local paths.
3. Run all cells to regenerate `movie_list.pkl` and `similarity.pkl`.

---

## ☁️ Deployment

This app is deployed on **Streamlit Cloud**.

The TMDB API key is stored securely in Streamlit's **Secrets Management** (`st.secrets['TMDB_API_KEY']`), with a local `.env` fallback for development.

🔗 **Live:** [https://moviemate-web.streamlit.app/](https://moviemate-web.streamlit.app/)

---

## 📦 Dependencies

```
streamlit
pandas
requests
python-dotenv
scikit-learn
```

---

## 🙏 Acknowledgements

- [TMDB](https://www.themoviedb.org/) for the movie data and API.
- [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) on Kaggle.
- [Streamlit](https://streamlit.io/) for the app framework.

---

## 📄 License

This project is open-source and available for educational purposes.
