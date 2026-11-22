from nltk.corpus import wordnet as wn
from src.relationships.connectors import COMMON_CONNECTORS
from src.relationships.text_utils import normalize_clue

# Checks to see if a word combined with an anchor word from connectors.py forms a word that exsists or not
def phrase_exists(candidate: str, model=None) -> bool:
    joined = candidate.replace(" ", "")
    underscored = candidate.replace(" ", "_")

    if model is not None:
        if joined in model or underscored in model or candidate in model:
            return True

    return bool(wn.synsets(underscored) or wn.synsets(joined))

# Checks a group of 4 words to see how many have matching connector words, either at the beginning or end of the word
def compute_phrase_features(
    words: list[str] | tuple[str, ...],
    model=None,
    connectors: tuple[str, ...] | list[str] = COMMON_CONNECTORS,
) -> dict[str, float]:
    normalized = [normalize_clue(w) for w in words]
    best_group_coverage = 0
    best_prefix_coverage = 0
    best_suffix_coverage = 0
    matching_connectors = 0

    for conn in connectors:
        after_hits = sum(1 for w in normalized if w and phrase_exists(f"{w} {conn}", model))
        before_hits = sum(1 for w in normalized if w and phrase_exists(f"{conn} {w}", model))
        group_hits = max(after_hits, before_hits)

        if group_hits >= 2:
            matching_connectors += 1
        if after_hits > best_prefix_coverage:
            best_prefix_coverage = after_hits
        if before_hits > best_suffix_coverage:
            best_suffix_coverage = before_hits
        if group_hits > best_group_coverage:
            best_group_coverage = group_hits

    n = max(len(normalized), 1)
    return {
        "phrase_best_coverage": float(best_group_coverage) / n,
        "phrase_best_after_coverage": float(best_prefix_coverage) / n,
        "phrase_best_before_coverage": float(best_suffix_coverage) / n,
        "phrase_connector_count": float(matching_connectors),
    }