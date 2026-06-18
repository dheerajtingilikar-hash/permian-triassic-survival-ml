from pathlib import Path
import pandas as pd

BASE_URL = "https://paleobiodb.org/data1.2"

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"

def download_occurrences():

    print("Project root:", ROOT)
    print("Raw directory:", RAW_DIR)

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    url = (
        f"{BASE_URL}/occs/list.csv?"
        "base_name=Bivalvia,Brachiopoda,Gastropoda,Ammonoidea"
        "&interval=Changhsingian,Induan,Olenekian,Anisian"
        "&show=coords,time,env,strat"
    )

    print("Downloading...")

    df = pd.read_csv(url)

    print("Rows downloaded:", len(df))
    print("Columns:", list(df.columns))

    output_file = RAW_DIR / "occurrences.csv"

    df.to_csv(output_file, index=False)

    print("Saved to:", output_file)

if __name__ == "__main__":
    download_occurrences()