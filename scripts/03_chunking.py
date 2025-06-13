import argparse
from pathlib import Path
import pandas as pd

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-n", "--size", type=int, default=1_000_000)
    p.add_argument("-o", "--out_dir", required=True)
    return p.parse_args()

def main():
    args = parse_args()
    df = (
        pd.read_parquet(args.input)
          .reset_index(drop=True)
          .rename_axis("index")
          .reset_index()
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for i in range(0, len(df), args.size):
        chunk = df.iloc[i : i + args.size]
        chunk.to_parquet(out_dir / f"chunk_{i//args.size:05}.parquet", index=False)

if __name__ == "__main__":
    main()
