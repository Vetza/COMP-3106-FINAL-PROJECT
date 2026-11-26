Adnan Kazi 101304031
Marko Celenkovic 101313325
Muhammed Imran 101301582


**Claude Disclaimer: "Why do I see Claude as a collaborator?"**

We were using Claude to plan what each of us would do at the beginning of the project, and since it was set to auto-update by accident, it tried to add its own project structure files. This added Claude as a collaborator which could not be removed. You can also refer to the commit history and see that it was added on day 1 before anything was actually done, and you may also observe that not a single commit was pushed by AI. Please disregard this error!

## Dataset

We use 628 NYT Connections puzzles (2023-06-12 to 2025-02-28) from the
[eric27n/NYT-Connections](https://huggingface.co/datasets/eric27n/NYT-Connections) dataset,
split by date into train (377), tune (126) and test (125) puzzles.

```
py src/download_data.py    # download the raw CSV to data/raw/
py src/prepare_data.py     # build data/processed/train.json, tune.json, test.json
```

In code: `from src.prepare_data import load_split` then `load_split("train")`.

See [docs/DATASET.md](docs/DATASET.md) for the full dataset format and preparation steps.

## Baseline Solvers

### Random solver

Guesses 4 random words from the board each turn until the game ends (4 mistakes or all groups found). Repeated guesses are skipped.

**To test it** (from the project folder):

```
python main.py
```

This plays every puzzle in the tune set (126 puzzles) with the random solver. 

With a fixed seed (`random.seed(0)`), the result after a run:

```
Random: 0/126 wins, 0.02 groups solved on average
```

- **wins**: puzzles where all 4 groups were found before the 4th mistake.
- **groups solved**: average number of groups found per puzzle, out of 4.

Random guessing almost never wins, so this is the lowest score a solver can get. The other solvers should do better than it. 