import argparse
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-o", "--output", required=True)
    return p.parse_args()

def main():
    args = parse_args()

if __name__ == "__main__":
    main()