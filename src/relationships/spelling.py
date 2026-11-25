# This file looks at how words are written, ignoring meaning. 

from difflib import SequenceMatcher
from itertools import combinations
import numpy as np
from src.relationships.text_utils import normalize_clue

# Normalize the letter and remove non-alphabetic characters from a clue
def clean_letters(clue: str) -> str:
    norm = normalize_clue(clue)
    return "".join(ch for ch in norm if ch.isalpha())

# Compute the length of the longest prefix shared across all words
def common_prefix_len(words: list[str]) -> int:
    if not words or any(not w for w in words):
        return 0
    shortest = min(words, key=len)
    for idx, ch in enumerate(shortest):
        if any(w[idx] != ch for w in words):
            return idx
    return len(shortest)

# Compute the length of the longest suffix shared across all words
def common_suffix_len(words: list[str]) -> int:
    reversed_words = [w[::-1] for w in words]
    return common_prefix_len(reversed_words)

# Compute the length of the longest contiguous substring present in all words
def longest_shared_substring_len(words: list[str]) -> int:
    if not words or any(not w for w in words):
        return 0
    shortest = min(words, key=len)
    max_len = len(shortest)
    for length in range(max_len, 0, -1):
        for start in range(max_len - length + 1):
            sub = shortest[start : start + length]
            if all(sub in w for w in words):
                return length
    return 0

# Compute spelling features for a group of words using the previous functions and metrics
def compute_spelling_features(words: list[str] | tuple[str, ...]) -> dict[str, float]:
    cleaned = [clean_letters(w) for w in words]
    valid = [w for w in cleaned if w]

    if len(valid) < 2:
        return {
            # Average letter-sequence similarity across the pairs
            "spell_mean_seq_sim": 0.0,
            # Average overlap of the set of letters used (shared letters / all distinct letters)
            "spell_mean_char_jaccard": 0.0,
            # Shared start
            "spell_common_prefix_len": 0.0,
            # Shared end 
            "spell_common_suffix_len": 0.0,
            "spell_shared_substr_len": 0.0,
            "spell_len_std": 0.0,
            "spell_anagram_ratio": 0.0,
        }

    pairs = list(combinations(valid, 2))
    seq_sims: list[float] = []
    jaccards: list[float] = []
    anagram_hits = 0

    for a, b in pairs:
        seq_sims.append(SequenceMatcher(None, a, b).ratio())
        set_a, set_b = set(a), set(b)
        union = set_a | set_b
        jaccards.append((len(set_a & set_b) / len(union)) if union else 0.0)
        if sorted(a) == sorted(b):
            anagram_hits += 1

    lengths = [len(w) for w in valid]
    return {
        "spell_mean_seq_sim": float(np.mean(seq_sims)),
        "spell_mean_char_jaccard": float(np.mean(jaccards)),
        "spell_common_prefix_len": float(common_prefix_len(valid)),
        "spell_common_suffix_len": float(common_suffix_len(valid)),
        "spell_shared_substr_len": float(longest_shared_substring_len(valid)),
        "spell_len_std": float(np.std(lengths)),
        "spell_anagram_ratio": float(anagram_hits / len(pairs)),
    }