# ============================================================
# main.py  –  Orchestrator with live Google Sheets sync + resume
#             Now covers all 50 US states
# ============================================================

import time
from logger import logger
from config import USA_CITIES, DELAY_BETWEEN_REQUESTS
from places_api import fetch_shelters_for_city, fetch_place_details
from email_extractor import scrape_emails_from_website
from sheets_writer import init_sheet, load_existing_place_ids_from_sheet, append_to_sheet
from csv_writer import init_csv, append_shelter


def run():
    logger.info("=" * 60)
    logger.info("  USA Animal Shelter Scraper — Starting")
    logger.info("=" * 60)

    # ── Connect to Google Sheet ──────────────────────────────
    logger.info("Connecting to Google Sheet…")
    init_sheet()

    # ── Resume: load existing place_ids directly from sheet ──
    seen_ids      = load_existing_place_ids_from_sheet()
    total_saved   = len(seen_ids)
    total_skipped = 0

    logger.info(f"Resuming from {total_saved} already-saved shelters.\n")

    # ── Also init local CSV as backup ────────────────────────
    init_csv()

    all_states = list(USA_CITIES.keys())
    total_states = len(all_states)

    # ── Outer Loop: States ───────────────────────────────────
    for state_idx, state in enumerate(all_states, start=1):
        cities = USA_CITIES[state]
        logger.info(f"\n{'=' * 60}")
        logger.info(f"  State [{state_idx}/{total_states}]: {state} ({len(cities)} cities)")
        logger.info(f"{'=' * 60}")

        # ── Inner Loop: Cities ───────────────────────────────
        for city_idx, city in enumerate(cities, start=1):
            logger.info(f"  [{city_idx}/{len(cities)}] City: {city}, {state}")

            raw_places = fetch_shelters_for_city(city, state)
            logger.info(f"    {len(raw_places)} raw results found")

            for place in raw_places:
                place_id = place.get("place_id", "")

                # ── Resume: skip if already in sheet ────────
                if place_id in seen_ids:
                    total_skipped += 1
                    logger.debug(f"    [SKIP] {place.get('name')} — already saved")
                    continue

                seen_ids.add(place_id)

                # ── Fetch full details ───────────────────────
                name = place.get("name", "Unknown")
                logger.info(f"    → Fetching details: {name}")
                details = fetch_place_details(place_id)
                time.sleep(DELAY_BETWEEN_REQUESTS)

                name    = details.get("name") or name
                address = details.get("formatted_address") or place.get("formatted_address", "")
                phone   = details.get("formatted_phone_number", "")
                website = details.get("website", "")

                # ── Scrape emails ────────────────────────────
                emails = []
                if website:
                    logger.info(f"      Scraping: {website}")
                    emails = scrape_emails_from_website(website)
                    logger.info(f"      Emails: {emails if emails else 'none found'}")
                else:
                    logger.info(f"      No website for {name}")

                shelter_data = {
                    "name":        name,
                    "address":     address,
                    "phone":       phone,
                    "website":     website,
                    "emails":      emails,
                    "place_id":    place_id,
                    "source_city": city,
                    "source_state": state,      # ← new field
                }

                # ── Write to Google Sheet (live) ─────────────
                append_to_sheet(shelter_data)

                # ── Write to local CSV (backup) ──────────────
                append_shelter(shelter_data)

                total_saved += 1
                logger.info(f"      ✅ Saved [{total_saved}]: {name}")

            logger.info(f"    Finished {city}.")
            time.sleep(DELAY_BETWEEN_REQUESTS)

        logger.info(f"\n  ✅ State complete: {state}\n")

    # ── Summary ──────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info(f"  ✅ Done! Total saved  : {total_saved}")
    logger.info(f"           Total skipped: {total_skipped} (duplicates)")
    logger.info(f"  Live Sheet + CSV both updated.")
    logger.info("=" * 60)


if __name__ == "__main__":
    run()