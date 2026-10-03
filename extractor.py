"""Extract emails, phone numbers and website URLs from text files into one CSV.

Usage:
    python3 extractor.py example_email.txt
    python3 extractor.py path/to/folder -o contacts.csv
"""

import argparse
import csv
import re
import sys
from pathlib import Path

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}")
PHONE_RE = re.compile(
    r"(?<!\d)(?:\+?1[-. ]?)?(?:\(\d{3}\)|\d{3})[-. ]?\d{3}[-. ]?\d{4}(?!\d)"
)
WEBSITE_RE = re.compile(
    r"(?<![@\w.-])(?:https?://)?(?:www\.)?[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*"
    r"\.(?:com|net|org|io|co|us|uk|edu|gov|info|biz)\b(?:/[^\s,;)<>\"']*)?",
    re.IGNORECASE,
)


def unique(items):
    """Remove duplicates (ignoring case) but keep the original order."""
    seen = {}
    for item in items:
        seen.setdefault(item.lower(), item)
    return list(seen.values())


def find_files(path):
    path = Path(path)
    if path.is_dir():
        return sorted(p for p in path.rglob("*.txt") if p.is_file())
    return [path]


def extract(text):
    emails = unique(EMAIL_RE.findall(text))
    phones = unique(PHONE_RE.findall(text))
    websites = unique(w.rstrip(".") for w in WEBSITE_RE.findall(text))
    return emails, phones, websites


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="a text file, or a folder of .txt files")
    parser.add_argument(
        "-o",
        "--output",
        default="contacts.csv",
        help="output CSV (default: contacts.csv)",
    )
    args = parser.parse_args()

    files = find_files(args.input)
    if not files:
        sys.exit(f"No `.txt` files found in {args.input}")

    rows = []
    for file in files:
        text = file.read_text(encoding="utf-8", errors="ignore")
        emails, phones, websites = extract(text)
        rows += [("Email", e, file.name) for e in emails]
        rows += [("Phone", p, file.name) for p in phones]
        rows += [("Website", w, file.name) for w in websites]

    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Value", "Source file"])
        writer.writerows(rows)

    print(
        f"Scanned {len(files)} file(s), saved {len(rows)} unique contacts to {args.output}"
    )


if __name__ == "__main__":
    main()
