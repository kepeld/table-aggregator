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

    if "ФИО" in df.columns:
        fio = df["ФИО"].str.strip().str.split(r"\s+", n=2, expand=True)
        fio.columns = ["Прізвище", "Ім'я", "По_батькові"]
        df = pd.concat([df.drop(columns=["ФИО"]), fio], axis=1)

    if "Дата рождения" in df.columns:
        df["Дата рождения"] = pd.to_datetime(
            df["Дата рождения"], format="%d.%m.%Y", errors="coerce"
        )

    if "Телефон" in df.columns:
        df["Телефон"] = (
            df["Телефон"]
            .astype(str)
            .str.replace(r"\D", "", regex=True)
            .replace("", pd.NA)
            .astype("Int64")
        )

    for col in ["Snils", "INN"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"\D", "", regex=True)
                .replace("", pd.NA)
            )

    if "Email" in df.columns:
        df["Email"] = (
            df["Email"]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace({"": pd.NA, "nan": pd.NA, "none": pd.NA})
        )

if __name__ == "__main__":
    main()
