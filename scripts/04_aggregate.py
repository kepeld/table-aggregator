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

    grouped = (
        df.groupby(["Прізвище", "Ім'я", "По_батькові"], as_index=False)
          .agg({
              "Телефон": lambda s: s.dropna().astype(int).tolist(),
              "Email":   lambda s: s.dropna().tolist(),
          })
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    grouped.to_parquet(out, engine="pyarrow")

if __name__ == "__main__":
    main()