from difflib import SequenceMatcher
from itertools import combinations
import nltk
from nltk.corpus import cmudict
import numpy as np
from src.relationships.text_utils import normalize_clue

# Download the CMU Pronouncing Dictionary if not already available
try:
    _CMU_DICT = cmudict.dict()
except LookupError:
    nltk.download("cmudict", quiet=True)
    _CMU_DICT = cmudict.dict()

# Normalize the word and get the pronunciations of a word from the CMU Pronouncing Dictionary
def get_pronunciations(clue: str) -> list[list[str]]:
    norm = normalize_clue(clue)
    if not norm:
        return []
    return _CMU_DICT.get(norm, [])

# Words have a trailing 0, 1 or 2 to indicate lexical stress, which we want to ignore for some comparisons
def strip_stress(phoneme: str) -> str:
    return phoneme.rstrip("012")

# Get the rhyme tail of a pronunciation, using the lexical stress value, which is the part of the word from the last stressed vowel to the end
def rhyme_tail(phones: list[str]) -> tuple[str, ...]:
    for idx in range(len(phones) - 1, -1, -1):
        if phones[idx][-1] in {"1", "2"}:
            return tuple(strip_stress(p) for p in phones[idx:])
    for idx in range(len(phones) - 1, -1, -1):
        if phones[idx][-1] == "0":
            return tuple(strip_stress(p) for p in phones[idx:])
    return tuple(strip_stress(p) for p in phones)

# Count the number of syllables in a pronunciation
def syllable_count(phones: list[str]) -> int:
    return sum(1 for p in phones if p[-1].isdigit())

# Compare the pronunciation similarity, homophone status, and rhyme status between two lists of pronunciations
def best_pair_sound_metrics(
    prons_a: list[list[str]],
    prons_b: list[list[str]],
) -> tuple[float, bool, bool]:
    best_sim = 0.0
    is_homophone = False
    is_rhyme = False

    for pa in prons_a:
        stripped_a = [strip_stress(p) for p in pa]
        tail_a = rhyme_tail(pa)
        for pb in prons_b:
            stripped_b = [strip_stress(p) for p in pb]
            tail_b = rhyme_tail(pb)

            sim = SequenceMatcher(None, stripped_a, stripped_b).ratio()
            if sim > best_sim:
                best_sim = sim
            if stripped_a == stripped_b:
                is_homophone = True
            if tail_a and tail_a == tail_b:
                is_rhyme = True

    return best_sim, is_homophone, is_rhyme

# Main function to compute sound features for a group of words, using the previously made functions and metrics
def compute_sound_features(words: list[str] | tuple[str, ...]) -> dict[str, float]:
    pron_lists = [get_pronunciations(w) for w in words]
    missing_count = sum(1 for p in pron_lists if not p)
    valid_prons = [p for p in pron_lists if p]

    if len(valid_prons) < 2:
        return {
            # Average sound similarity across the pairs
            "sound_mean_phoneme_sim": 0.0,
            # Most similar pair
            "sound_max_phoneme_sim": 0.0,
            # Fraction of pairs that rhyme
            "sound_rhyme_ratio": 0.0,
            # Fraction of pairs that are homophones
            "sound_homophone_ratio": 0.0,
            # How much the syllable counts vary
            "sound_syllable_std": 0.0,
            # How many words were not in the dictionary
            "sound_missing_count": float(missing_count),
        }

    pairs = list(combinations(valid_prons, 2))
    pair_sims: list[float] = []
    rhyme_hits = 0
    homophone_hits = 0

    for prons_a, prons_b in pairs:
        sim, is_homo, is_rhyme = best_pair_sound_metrics(prons_a, prons_b)
        pair_sims.append(sim)
        if is_homo:
            homophone_hits += 1
        if is_rhyme:
            rhyme_hits += 1

    syllable_counts = [syllable_count(p[0]) for p in valid_prons]

    return {
        "sound_mean_phoneme_sim": float(np.mean(pair_sims)),
        "sound_max_phoneme_sim": float(np.max(pair_sims)),
        "sound_rhyme_ratio": float(rhyme_hits / len(pairs)),
        "sound_homophone_ratio": float(homophone_hits / len(pairs)),
        "sound_syllable_std": float(np.std(syllable_counts)),
        "sound_missing_count": float(missing_count),
    }