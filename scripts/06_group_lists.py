import argparse
from pathlib import Path
import sys
import pandas as pd


def parse():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--keys", nargs="+", required=True)
    p.add_argument("--cols", nargs="+", required=True)
    return p.parse_args()


def main():
    a = parse()
    df = pd.read_parquet(a.input)

    missing = [c for c in a.keys + a.cols if c not in df.columns]
    if missing:
        sys.stderr.write(f"Columns not found: {', '.join(missing)}\n")
        sys.exit(1)

    agg = {c: lambda s: s.dropna().unique().tolist() for c in a.cols}
    grouped = df.groupby(a.keys, as_index=False, dropna=False).agg(agg)

    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    grouped.to_parquet(out, engine="pyarrow")


if __name__ == "__main__":
    main()