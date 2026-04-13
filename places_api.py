# ============================================================
# places_api.py  –  Fetch shelters from Google Places API
# ============================================================

import time
import requests
from logger import logger
from config import (
    GOOGLE_API_KEY, SEARCH_QUERY,
    DELAY_BETWEEN_REQUESTS, REQUEST_TIMEOUT,
    MAX_RETRIES, MAX_PAGES_PER_CITY
)

BASE_URL      = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL   = "https://maps.googleapis.com/maps/api/place/details/json"


def _get_with_retry(url: str, params: dict) -> dict | None:
    """GET request with exponential back-off retry."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            wait = attempt * 2
            logger.warning(f"Request failed (attempt {attempt}/{MAX_RETRIES}): {e}. Retrying in {wait}s…")
            time.sleep(wait)
    logger.error(f"All {MAX_RETRIES} attempts failed for URL: {url}")
    return None


def fetch_place_details(place_id: str) -> dict:
    """Return phone + website for a single place_id."""
    params = {
        "place_id": place_id,
        "fields": "name,formatted_phone_number,website,formatted_address",
        "key": GOOGLE_API_KEY,
    }
    data = _get_with_retry(DETAILS_URL, params)
    if data and data.get("status") == "OK":
        return data.get("result", {})
    return {}


def fetch_shelters_for_city(city: str, state: str) -> list[dict]:
    """
    Run a paginated Text Search for 'animal shelter in <city>, <state>'.
    Returns a list of raw place dicts (name, place_id, address).

    Args:
        city:  City name, e.g. "Houston"
        state: Full state name, e.g. "Texas"  ← now passed in, not hardcoded
    """
    query   = f"{SEARCH_QUERY} in {city}, {state}"
    params  = {"query": query, "key": GOOGLE_API_KEY}
    places  = []
    page    = 0

    logger.info(f"    Searching: '{query}'")

    while page < MAX_PAGES_PER_CITY:
        data = _get_with_retry(BASE_URL, params)
        if not data:
            break

        status = data.get("status")
        if status == "ZERO_RESULTS":
            logger.info(f"      No results for {city}, {state} (page {page + 1})")
            break
        if status != "OK":
            logger.warning(f"      Unexpected status '{status}' for {city}, {state}")
            break

        results = data.get("results", [])
        logger.info(f"      Page {page + 1}: {len(results)} results")
        places.extend(results)

        next_token = data.get("next_page_token")
        if not next_token:
            break

        page += 1
        # Google requires a short pause before using next_page_token
        time.sleep(DELAY_BETWEEN_REQUESTS + 0.5)
        params = {"pagetoken": next_token, "key": GOOGLE_API_KEY}

    return places