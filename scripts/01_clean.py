# scripts/01_clean.py
import argparse
from pathlib import Path
import pandas as pd

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-o", "--output", required=True)
    p.add_argument("-n", "--nrows", type=int, default=None)
    return p.parse_args()

def main():
    args = parse_args()
    inp = Path(args.input)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(
        inp,
        sep=",",
        encoding="utf-8",
        skipinitialspace=True,
        on_bad_lines="skip",
        dtype=str,
        nrows=args.nrows,
    )
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]
    if "" in df.columns:
        df = df.drop(columns=[""])

if __name__ == "__main__":
    main()
