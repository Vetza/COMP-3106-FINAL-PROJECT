Adnan Kazi 101304031
Marko Celenkovic 101313325


**Claude Disclaimer:**

We were using Claude to plan what each of us would do and since it was set to auto, it and it tried to add its own project structure files. We have since removed the changes. You can refer to the commit history and see that it was added on day 1 before any of our significant changes.


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