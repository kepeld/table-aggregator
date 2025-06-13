import argparse
from pathlib import Path
import pandas as pd


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--keys", nargs="+", required=True)
    p.add_argument("--cols", nargs="+", required=True)
    return p.parse_args()


def fill_and_filter_group(group, cols):
    filled = {}
    for col in cols:
        non_null = group[col].dropna().unique()
        filled[col] = non_null[0] if len(non_null) > 0 else None

    def is_useful(row):
        for col in cols:
            if pd.notna(row[col]) and row[col] != filled[col]:
                return True
        return False

    filtered = group[group.apply(is_useful, axis=1)]

    new_row = {col: filled[col] for col in cols}
    for key in group.columns:
        if key not in cols:
            new_row[key] = group[key].iloc[0]
    result = pd.concat([filtered, pd.DataFrame([new_row])], ignore_index=True)
    return result


def main():
    args = parse_args()
    df = pd.read_parquet(args.input)
    df = (
        df.groupby(args.keys, dropna=False, as_index=False)
          .apply(lambda g: fill_and_filter_group(g, args.cols))
          .reset_index(drop=True)
    )
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(args.output, engine="pyarrow")


if __name__ == "__main__":
    main()
