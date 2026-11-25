# Every other relationship file calls these helpers to clean words
# before comparing them.

def normalize_clue(text: str) -> str:
    # Get rid of capital letters and whitespace
    return " ".join(text.strip().lower().split())

def clue_tokens(text: str) -> list[str]:
    # Split the word into individual tokens (Like ICE CREAM to ICE and CREAM)
    cleaned = normalize_clue(text).replace("-", " ")
    return [tok for tok in cleaned.split(" ") if tok]