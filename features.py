import pandas as pd

from utils import year_from_date


MOVIE_NUMERIC = ["runtime", "vote_average", "vote_count", "popularity", "imdb_rating", "imdb_votes", "release_year"]


def build_movie_features(movies):
    rows = []
    genre_set = set()
    for m in movies:
        for g in m.get("genres", []):
            genre_set.add(g)
    genres = sorted(genre_set)

    for m in movies:
        row = {
            "title": m.get("title"),
            "release_year": year_from_date(m.get("release_date")),
        }
        for field in MOVIE_NUMERIC:
            if field == "release_year":
                continue
            row[field] = m.get(field) or 0
        for g in genres:
            row[f"genre_{g}"] = 1 if g in m.get("genres", []) else 0
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.fillna(0)
    return df


def default_movie_target(df):
    target = df[MOVIE_NUMERIC].mean().to_dict()
    target["runtime"] = 110
    target["popularity"] = max(target["popularity"], df["popularity"].median())
    target["vote_average"] = max(target["vote_average"], 7.1)
    target["imdb_rating"] = max(target["imdb_rating"], 7.0)
    target["release_year"] = max(target["release_year"], 2018)
    for col in df.columns:
        if col.startswith("genre_") and any(key in col for key in ["Comedy", "Action", "Adventure", "Drama", "Romance"]):
            target[col] = 1
        elif col.startswith("genre_"):
            target[col] = 0
    return target
