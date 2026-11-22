"""Download the NYT Connections dataset from HuggingFace.

Source: https://huggingface.co/datasets/eric27n/NYT-Connections
Saves the CSV to data/raw/connections.csv (one row per word).

Run from the project folder:
    py src/download_data.py
"""

import os
import urllib.request

URL = "https://huggingface.co/datasets/eric27n/NYT-Connections/resolve/main/Connections_Data.csv"
RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "connections.csv")


def download_dataset(url=URL, path=RAW_PATH):
    # Keep the existing file so everyone on the team uses the same copy
    if os.path.exists(path):
        print("Dataset already downloaded:", os.path.normpath(path))
        return

    os.makedirs(os.path.dirname(path), exist_ok=True)
    print("Downloading", url)
    urllib.request.urlretrieve(url, path)
    print("Saved to", os.path.normpath(path))


if __name__ == "__main__":
    download_dataset()
