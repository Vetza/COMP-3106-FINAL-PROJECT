def normalize_clue(text: str) -> str:
    # Get rid of capital letters and whitespace
    return " ".join(text.strip().lower().split())

def clue_tokens(text: str) -> list[str]:
    # Split the word into individual tokens
    cleaned = normalize_clue(text).replace("-", " ")
    return [tok for tok in cleaned.split(" ") if tok]