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

    def flatten(x):
        return x[0] if isinstance(x, list) and len(x) == 1 else pd.NA

    for col in agg.columns.difference(keys):
        agg[col] = agg[col].apply(flatten)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    agg.to_parquet(out, engine="pyarrow")


if __name__ == "__main__":
    main()