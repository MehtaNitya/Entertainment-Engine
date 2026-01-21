import numpy as np
from sklearn.neighbors import NearestNeighbors


def knn_recommend(df, target, k):
    work = df.copy()
    id_cols = [c for c in work.columns if c in ["title", "name", "artist"]]
    feature_cols = [c for c in work.columns if c not in id_cols]
    X = work[feature_cols].values.astype(float)

    target_vec = np.array([target.get(col, 0) for col in feature_cols]).reshape(1, -1)

    model = NearestNeighbors(n_neighbors=min(k, len(work)), metric="cosine")
    model.fit(X)
    distances, indices = model.kneighbors(target_vec)
    result = work.iloc[indices[0]].copy()
    result["score"] = 1 - distances[0]
    return result
