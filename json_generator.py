#!/usr/bin/env python3
import argparse
import copy
import csv
import json
from json import JSONDecodeError
from pathlib import Path

def load_template(template_path: Path) -> dict:
    with template_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    if isinstance(raw, list):
        if not raw:
            raise ValueError("Template is an empty list.")
        return raw[0]
    if isinstance(raw, dict):
        return raw
    raise ValueError("Template must be a dict or a list with one object.")

def load_existing(output_path: Path):
    if not output_path.exists() or output_path.stat().st_size == 0:
        return []
    try:
        with output_path.open("r", encoding="utf-8") as f:
            existing = json.load(f)
        return existing if isinstance(existing, list) else [existing]
    except JSONDecodeError:
        return []

def sniff_delimiter(csv_path: Path, fallback: str = ",") -> str:
    try:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            sample = f.read(4096)
            return csv.Sniffer().sniff(sample, delimiters=",;|\t").delimiter
    except Exception:
        return fallback  # fallback to comma if detection fails

def main():
    ap = argparse.ArgumentParser(
        description="Copy a JSON template for each CSV row and replace one field with the CSV value."
    )
    ap.add_argument("template", type=Path, help="Path to JSON template.")
    ap.add_argument("csv_file", type=Path, help="Path to CSV input.")
    ap.add_argument("output", type=Path, help="Path to JSON output (array).")
    ap.add_argument("-d", "--delimiter", default=None,
                    help="CSV delimiter (default: auto-detect, falls back to ',').")
    args = ap.parse_args()

    template_obj = load_template(args.template)
    data_total = load_existing(args.output)

    delimiter = args.delimiter or sniff_delimiter(args.csv_file, fallback=",")
    print(f"Using CSV delimiter: '{delimiter}'")

    with args.csv_file.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)

        if not reader.fieldnames:
            raise ValueError("CSV appears to be empty or missing a header row.")

        # Nimm die ERSTE Spalte als zu ersetzendes Feld
        field_name = reader.fieldnames[0].strip()
        if not field_name:
            raise ValueError("First CSV header is empty. Please provide a valid column name.")

        print(f"Replacing template field: '{field_name}' from CSV column '{field_name}'")

        new_count = 0
        for row in reader:
            value = (row.get(field_name) or "").strip()
            if not value:
                continue  # skip empty lines
            entry = copy.deepcopy(template_obj)
            entry[field_name] = value
            data_total.append(entry)
            new_count += 1

    with args.output.open("w", encoding="utf-8") as f:
        json.dump(data_total, f, ensure_ascii=False, indent=4)

    print(f"✅ Wrote {len(data_total)} total entries to {args.output} (+{new_count} new).")

if __name__ == "__main__":
    main()
