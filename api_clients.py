import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils import safe_float


TMDB_BASE = "https://api.themoviedb.org/3"
OMDB_BASE = "https://www.omdbapi.com/"
SESSION = requests.Session()
RETRY = Retry(
    total=3,
    backoff_factor=0.6,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
SESSION.mount("https://", HTTPAdapter(max_retries=RETRY))


def tmdb_get(path, api_key, params=None):
    params = params or {}
    params["api_key"] = api_key
    response = SESSION.get(f"{TMDB_BASE}{path}", params=params, timeout=20)
    response.raise_for_status()
    return response.json()


def omdb_get(api_key, imdb_id):
    params = {"apikey": api_key, "i": imdb_id}
    response = SESSION.get(OMDB_BASE, params=params, timeout=20)
    if response.status_code == 401:
        return {}
    response.raise_for_status()
    return response.json()


def fetch_movies(tmdb_key, omdb_key, count):
    movies = []
    page = 1
    while len(movies) < count:
        data = tmdb_get("/trending/movie/week", tmdb_key, params={"page": page})
        for item in data.get("results", []):
            details = tmdb_get(f"/movie/{item['id']}", tmdb_key)
            imdb_id = details.get("imdb_id")
            omdb = omdb_get(omdb_key, imdb_id) if imdb_id else {}
            movies.append(
                {
                    "title": details.get("title"),
                    "release_date": details.get("release_date"),
                    "runtime": details.get("runtime"),
                    "genres": [g["name"] for g in details.get("genres", [])],
                    "vote_average": details.get("vote_average"),
                    "vote_count": details.get("vote_count"),
                    "popularity": details.get("popularity"),
                    "imdb_rating": safe_float(omdb.get("imdbRating")),
                    "imdb_votes": safe_float(omdb.get("imdbVotes", "0").replace(",", "")),
                }
            )
            if len(movies) >= count:
                break
        page += 1
        time.sleep(0.2)
    return movies
