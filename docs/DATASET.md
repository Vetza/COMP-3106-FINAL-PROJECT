# Dataset

## Source

- **Dataset:** [eric27n/NYT-Connections](https://huggingface.co/datasets/eric27n/NYT-Connections) on HuggingFace
- **File:** `Connections_Data.csv` (last updated upstream on 2025-03-01)
- **Downloaded:** 2026-11-21
- **Contents:** 628 NYT Connections puzzles, one per day from 2023-06-12 to 2025-02-28, with no missing days

The dataset is no longer updated, so our copy in `data/raw/` is the version everyone on the team should use.

## Files

```
data/
  raw/connections.csv        original CSV from HuggingFace (do not edit)
  processed/train.json       oldest 60% of puzzles
  processed/tune.json        next 20%
  processed/test.json        newest 20%
src/
  download_data.py           downloads the CSV
  prepare_data.py            builds puzzles, checks them, sorts and splits them
```

## Raw CSV format

Each row is **one word**, so each puzzle has 16 rows (10,048 rows in total).

| Column | Example | Meaning |
|--------|---------|---------|
| `Game ID` | `1` | Puzzle ID from the dataset |
| `Puzzle Date` | `2023-06-12` | Date the puzzle was published |
| `Word` | `SNOW` | One of the 16 words |
| `Group Name` | `WET WEATHER` | The answer category this word belongs to |
| `Group Level` | `0` | Difficulty: 0 = yellow, 1 = green, 2 = blue, 3 = purple |
| `Starting Row` | `1` | Row on the starting board (1-4) |
| `Starting Column` | `1` | Column on the starting board (1-4) |

Note: `Game ID` is **not** the official NYT puzzle number. The IDs go up to 664 with 36 numbers missing, and they do not always increase with the date. Always use `Puzzle Date` for ordering.

## Processed JSON format

Each split is a JSON list of puzzles. One puzzle looks like this:

```json
{
  "id": 1,
  "date": "2023-06-12",
  "words": ["SNOW", "LEVEL", "SHIFT", "KAYAK", "HEAT", "TAB", "BUCKS", "RETURN",
            "JAZZ", "HAIL", "OPTION", "RAIN", "SLEET", "RACECAR", "MOM", "NETS"],
  "groups": [
    {"name": "WET WEATHER",   "level": 0, "members": ["SNOW", "HAIL", "RAIN", "SLEET"]},
    {"name": "NBA TEAMS",     "level": 1, "members": ["HEAT", "BUCKS", "JAZZ", "NETS"]},
    {"name": "KEYBOARD KEYS", "level": 2, "members": ["SHIFT", "TAB", "RETURN", "OPTION"]},
    {"name": "PALINDROMES",   "level": 3, "members": ["LEVEL", "KAYAK", "RACECAR", "MOM"]}
  ]
}
```

- `words` lists the 16 words in the **original board order** (row by row, left to right), which is how the puzzle was shown to players.
- `groups` holds the answer, sorted from easiest (yellow) to hardest (purple).

## Using the data in code

```python
from src.prepare_data import load_split

train = load_split("train")   # or "tune" / "test"
puzzle = train[0]
puzzle["words"]               # 16 words to show on the board
puzzle["groups"]              # the correct answer
```

## Preparation steps

`src/prepare_data.py` does the following:

1. **Load** the CSV rows.
2. **Build puzzles** by grouping rows by `Game ID`. Words are put in board order using `Starting Row` and `Starting Column`, and grouped into their 4 answer groups.
3. **Check** each puzzle. A puzzle is dropped if it does not have exactly 4 groups of 4 words and 16 unique, non-empty words. **All 628 puzzles passed, so none were dropped.**
4. **Sort** puzzles by date.
5. **Split** them by date into train / tune / test (60% / 20% / 20%).

## Splits

| Split | Puzzles | Dates | Used for |
|-------|---------|-------|----------|
| train | 377 | 2023-06-12 to 2024-06-22 | Training the scoring model |
| tune  | 126 | 2024-06-23 to 2024-10-26 | Choosing model settings and calibrating probabilities |
| test  | 125 | 2024-10-27 to 2025-02-28 | Final results only, used once at the end |

Some dataset statistics:

- 5,296 different words appear across all puzzles.
- 141 of those are multi-word entries (e.g. phrases with spaces).
- Every puzzle has one group at each difficulty level.

### Why split by date instead of randomly?

- The test set holds the **newest** puzzles, so it shows how the solver does on puzzles it has never seen, like a real player facing tomorrow's puzzle.
- Puzzle writers reuse themes over time. A random split could put a puzzle in training and a very similar later puzzle in testing, which would make results look better than they really are.
- The test set must not be used for tuning. Use `tune` for all experiments until the final evaluation.

## How to regenerate the files

From the project folder:

```
py src/download_data.py    # skips the download if data/raw/connections.csv already exists
py src/prepare_data.py     # rebuilds data/processed/*.json
```

`prepare_data.py` always gives the same splits from the same CSV, because it uses no randomness.
