import argparse
from pathlib import Path
import pandas as pd

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-o", "--output", required=True)
    return p.parse_args()

def main():
    args = parse_args()
    df = pd.read_parquet(args.input)

    keys = ["Прізвище", "Ім'я", "По_батькові", "Дата рождения"]
    agg = (
        df.groupby(keys, dropna=False, as_index=False)
          .agg(lambda s: s.dropna().unique().tolist())
    )

if __name__ == "__main__":
    main()