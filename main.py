import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from api_clients import fetch_movies
from features import (
    build_movie_features,
    default_movie_target,
)
from recommender import knn_recommend
from report import export_recommendations, write_report


def ensure_env():
    missing = []
    for key in ["TMDB_API_KEY", "OMDB_API_KEY"]:
        if not os.getenv(key):
            missing.append(key)
    return missing


def main():
    parser = argparse.ArgumentParser(description="Entertainment Engine")
    parser.add_argument("--movies", type=int, default=30, help="How many movies to fetch")
    parser.add_argument("--k", type=int, default=8, help="Number of recommendations")
    args = parser.parse_args()

    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()
    missing = ensure_env()
    if missing:
        print("Missing environment variables:")
        for key in missing:
            print(f"- {key}")
        print("Create a .env file based on .env.example")
        return

    tmdb_key = os.getenv("TMDB_API_KEY")
    omdb_key = os.getenv("OMDB_API_KEY")

    print("Fetching movies...")
    movies = fetch_movies(tmdb_key, omdb_key, args.movies)
    print(f"Movies fetched: {len(movies)}")

    movie_features = build_movie_features(movies)

    movie_target = default_movie_target(movie_features)

    movie_recs = knn_recommend(movie_features, movie_target, args.k)

    write_report(
        movies,
        movie_recs,
        output_path=os.path.join("output", "report.txt"),
        html_path=os.path.join("output", "report.html"),
    )
    export_recommendations(
        movie_recs,
        csv_path=os.path.join("output", "recommendations.csv"),
        json_path=os.path.join("output", "recommendations.json"),
    )

    print("Done. Reports written to output\\report.txt and output\\report.html")
    print("Exports written to output\\recommendations.csv and output\\recommendations.json")


if __name__ == "__main__":
    main()
