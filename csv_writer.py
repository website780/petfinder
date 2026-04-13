# ============================================================
# csv_writer.py  –  Deduplicated, incremental CSV output
# ============================================================

import csv
import os
from logger import logger
from config import OUTPUT_CSV

FIELDNAMES = [
    "name",
    "address",
    "city",
    "phone",
    "website",
    "emails",
    "place_id",
    "source_city_query",
]


def _parse_city_from_address(address: str) -> str:
    """Best-effort city extraction from a formatted address string."""
    parts = address.split(",")
    return parts[1].strip() if len(parts) >= 2 else ""


def init_csv():
    """Create the CSV with headers if it doesn't already exist."""
    if not os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        logger.info(f"Created output file: {OUTPUT_CSV}")


def load_existing_place_ids() -> set[str]:
    """Return the set of place_ids already written (for deduplication)."""
    seen = set()
    if not os.path.exists(OUTPUT_CSV):
        return seen
    with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("place_id"):
                seen.add(row["place_id"])
    return seen


def append_shelter(shelter: dict):
    """Append a single shelter row to the CSV."""
    address = shelter.get("address", "")
    row = {
        "name":              shelter.get("name", ""),
        "address":           address,
        "city":              _parse_city_from_address(address),
        "phone":             shelter.get("phone", ""),
        "website":           shelter.get("website", ""),
        "emails":            "; ".join(shelter.get("emails", [])),
        "place_id":          shelter.get("place_id", ""),
        "source_city_query": shelter.get("source_city", ""),
    }
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)