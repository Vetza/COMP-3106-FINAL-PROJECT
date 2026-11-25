# Uses WordNet, which is a dictionary that arranges word meanings in a tree,
# (for more info, see group proposal document). This helps us check
# whether 4 words belong to the same category.

from itertools import combinations
import numpy as np
from nltk.corpus import wordnet as wn
from src.relationships.text_utils import normalize_clue

# A synset (synonym set) is one meaning of a word, together with the other words that share that meaning 
# Ex. wn.synsets("mouse") returns:
#     mouse.n.01: The small rodent
#     mouse.n.02: The computer pointing device

# Function that gets the synsets of a word, checking the categories that a word is apart of
def _get_synsets(clue: str):
    norm = normalize_clue(clue)
    if not norm:
        return []
    synsets = wn.synsets(norm)
    if synsets:
        return synsets
    return wn.synsets(norm.replace(" ", "_"))

# Function that gets all the categories related to every word
def _hypernym_set(synsets) -> set:
    ancestors = set()
    for syn in synsets:
        ancestors.add(syn)
        ancestors.update(syn.closure(lambda s: s.hypernyms()))
    return ancestors

# Gets the category with the highest similarity between 2 words
def _best_pair_similarity(synsets_a, synsets_b) -> float:
    best = 0.0
    for syn_a in synsets_a:
        for syn_b in synsets_b:
            sim = syn_a.wup_similarity(syn_b)
            if sim is not None and sim > best:
                best = float(sim)
    return best

# Compare a group of 4 words for category similarities
def compute_category_features(words: list[str] | tuple[str, ...]) -> dict[str, float]:
    synset_lists = [_get_synsets(word) for word in words]
    missing_count = sum(1 for synsets in synset_lists if not synsets)
    hypernym_sets = [_hypernym_set(synsets) for synsets in synset_lists]

    pairs = list(combinations(range(len(words)), 2))
    pair_sims: list[float] = []
    shared_hypernym_hits = 0
    valid_pairs = 0

    for i, j in pairs:
        if synset_lists[i] and synset_lists[j]:
            valid_pairs += 1
            pair_sims.append(_best_pair_similarity(synset_lists[i], synset_lists[j]))
            if hypernym_sets[i] & hypernym_sets[j]:
                shared_hypernym_hits += 1

    shared_ratio = (shared_hypernym_hits / valid_pairs) if valid_pairs > 0 else 0.0

    if not pair_sims:
        return {
            # Average pair similarity
            "wn_mean_sim": 0.0,
            # Highest pair similarity
            "wn_max_sim": 0.0,
            # Fraction of pairs sharing a broader category
            "wn_shared_hypernym_ratio": 0.0,
            # Words not found in WordNet dictionary
            "wn_missing_count": float(missing_count),
        }

    return {
        "wn_mean_sim": float(np.mean(pair_sims)),
        "wn_max_sim": float(np.max(pair_sims)),
        "wn_shared_hypernym_ratio": float(shared_ratio),
        "wn_missing_count": float(missing_count),
    }