"""Turn the raw CSV into puzzles, sort them by date, and split them.

Split (by date): oldest 60% = train, next 20% = tune, newest 20% = test.
Output: data/processed/train.json, tune.json, test.json

Run from the project folder:
    py src/prepare_data.py

Use the splits in other code:
    from src.prepare_data import load_split
    train = load_split("train")
"""

import csv
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_PATH = os.path.join(DATA_DIR, "raw", "connections.csv")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

TRAIN_FRAC = 0.6
TUNE_FRAC = 0.2  # test gets the rest (0.2)


def load_rows(path=RAW_PATH):
    # Each row in the CSV is one word
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_puzzles(rows):
    # Group the rows by game ID
    games = {}
    for row in rows:
        games.setdefault(int(row["Game ID"]), []).append(row)

    puzzles = []
    for game_id, game_rows in games.items():
        # Board order: sort by starting row, then column
        game_rows.sort(key=lambda r: (int(r["Starting Row"]), int(r["Starting Column"])))

        groups = {}
        for row in game_rows:
            name = row["Group Name"].strip()
            if name not in groups:
                groups[name] = {"name": name, "level": int(row["Group Level"]), "members": []}
            groups[name]["members"].append(row["Word"].strip())

        puzzles.append({
            "id": game_id,
            "date": game_rows[0]["Puzzle Date"],
            "words": [row["Word"].strip() for row in game_rows],
            "groups": sorted(groups.values(), key=lambda g: g["level"]),
        })
    return puzzles


def is_valid(puzzle):
    # Returns (True, "") or (False, reason)
    if len(puzzle["groups"]) != 4:
        return False, "does not have 4 groups"
    if any(len(g["members"]) != 4 for g in puzzle["groups"]):
        return False, "a group does not have 4 words"
    words = puzzle["words"]
    if "" in words:
        return False, "has an empty word"
    if len(set(words)) != 16:
        return False, "does not have 16 unique words"
    return True, ""


def split_by_date(puzzles, train_frac=TRAIN_FRAC, tune_frac=TUNE_FRAC):
    # Dates are YYYY-MM-DD, so sorting the strings sorts by date
    puzzles = sorted(puzzles, key=lambda p: p["date"])
    n_train = round(len(puzzles) * train_frac)
    n_tune = round(len(puzzles) * tune_frac)
    return {
        "train": puzzles[:n_train],
        "tune": puzzles[n_train:n_train + n_tune],
        "test": puzzles[n_train + n_tune:],
    }


def load_split(name):
    # name is "train", "tune" or "test"
    with open(os.path.join(PROCESSED_DIR, name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def main():
    puzzles = build_puzzles(load_rows())

    # Drop any broken puzzles
    valid = []
    for puzzle in puzzles:
        ok, reason = is_valid(puzzle)
        if ok:
            valid.append(puzzle)
        else:
            print(f"Dropped puzzle {puzzle['id']} ({puzzle['date']}): {reason}")
    print(f"{len(valid)} valid puzzles out of {len(puzzles)}")

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    for name, split in split_by_date(valid).items():
        with open(os.path.join(PROCESSED_DIR, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(split, f, indent=2)
        print(f"{name}: {len(split)} puzzles, {split[0]['date']} to {split[-1]['date']}")


if __name__ == "__main__":
    main()
