from itertools import combinations
import numpy as np
from src.relationships.text_utils import clue_tokens, normalize_clue

# This functio cleans the text and gets the number vector of a word
def _get_vector(clue: str, model) -> np.ndarray | None:
    norm = normalize_clue(clue)
    if norm in model:
        return np.asarray(model[norm], dtype=np.float64)

    tokens = clue_tokens(clue)
    vectors = [np.asarray(model[tok], dtype=np.float64) for tok in tokens if tok in model]
    if not vectors:
        return None
    return np.mean(vectors, axis=0)

# Compare the similarity of 2 words using their vectors
def _cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

# Compare the siliarity between a group of 4 words
def compute_meaning_features(words: list[str] | tuple[str, ...], model) -> dict[str, float]:
    vectors = [_get_vector(word, model) for word in words]
    oov_count = sum(1 for vec in vectors if vec is None)

    pair_sims: list[float] = []
    for vec_a, vec_b in combinations(vectors, 2):
        if vec_a is not None and vec_b is not None:
            pair_sims.append(_cosine_similarity(vec_a, vec_b))

    if not pair_sims:
        return {
            "emb_mean_sim": 0.0,
            "emb_min_sim": 0.0,
            "emb_max_sim": 0.0,
            "emb_oov_count": float(oov_count),
        }

    return {
        "emb_mean_sim": float(np.mean(pair_sims)),
        "emb_min_sim": float(np.min(pair_sims)),
        "emb_max_sim": float(np.max(pair_sims)),
        "emb_oov_count": float(oov_count),
    }