# ============================================================
# sheets_writer.py  –  Google Sheets via OAuth
# ============================================================

import time
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from requests.exceptions import ConnectionError, Timeout
import os
import pickle
from logger import logger
from config import (
    GOOGLE_SHEETS_CREDENTIALS_FILE,
    GOOGLE_SHEET_NAME,
    GOOGLE_WORKSHEET_NAME,
)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

TOKEN_FILE = "token.pickle"

HEADERS = [
    "name", "address", "city", "phone",
    "website", "emails", "place_id", "source_city_query", "source_state"
]

# ── Global worksheet object (set once, reused everywhere) ────
_ws: gspread.Worksheet = None


def _get_credentials():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        flow  = InstalledAppFlow.from_client_secrets_file(
            GOOGLE_SHEETS_CREDENTIALS_FILE, SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
        logger.info("✅ Token saved to token.pickle — no login needed next time.")

    return creds


def _connect() -> gspread.Worksheet:
    creds  = _get_credentials()
    client = gspread.authorize(creds)

    # ── Auto-create spreadsheet if it doesn't exist ──────────
    try:
        sheet = client.open(GOOGLE_SHEET_NAME)
        logger.info(f"✅ Found existing sheet: '{GOOGLE_SHEET_NAME}'")
    except gspread.exceptions.SpreadsheetNotFound:
        logger.info(f"Sheet '{GOOGLE_SHEET_NAME}' not found — creating it now…")
        sheet = client.create(GOOGLE_SHEET_NAME)
        sheet.share(None, perm_type="anyone", role="writer")
        logger.info(f"✅ Created new sheet: '{GOOGLE_SHEET_NAME}'")
        logger.info(f"   URL: {sheet.url}")

    # ── Get or create the named worksheet ────────────────────
    try:
        ws = sheet.worksheet(GOOGLE_WORKSHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        ws = sheet.add_worksheet(title=GOOGLE_WORKSHEET_NAME, rows="1000", cols="20")
        logger.info(f"✅ Created worksheet: '{GOOGLE_WORKSHEET_NAME}'")

    return ws


def _reconnect():
    """Force a fresh connection — called when network drops mid-run."""
    global _ws
    logger.warning("⚡ Reconnecting to Google Sheets…")
    for attempt in range(1, 6):
        try:
            _ws = _connect()
            logger.info("✅ Reconnected successfully.")
            return
        except Exception as e:
            wait = 2 ** attempt          # 2, 4, 8, 16, 32s
            logger.warning(f"Reconnect attempt {attempt}/5 failed: {e}. Waiting {wait}s…")
            time.sleep(wait)
    raise RuntimeError("❌ Could not reconnect to Google Sheets after 5 attempts.")


def init_sheet():
    """Connect and write headers if empty. Stores worksheet globally."""
    global _ws
    _ws  = _connect()
    rows = _ws.get_all_values()
    if not rows:
        _ws.append_row(HEADERS, value_input_option="RAW")
        logger.info("Sheet was empty — headers written.")
    else:
        logger.info(f"Sheet has {len(rows) - 1} existing rows.")


def load_existing_place_ids_from_sheet() -> set[str]:
    """Read all place_ids from sheet for resume."""
    global _ws
    records = _ws.get_all_records()
    ids     = {row["place_id"] for row in records if row.get("place_id")}
    logger.info(f"✅ Loaded {len(ids)} existing place_ids (resume point).")
    return ids


def _parse_city(address: str) -> str:
    parts = address.split(",")
    return parts[1].strip() if len(parts) >= 2 else ""


def append_to_sheet(shelter: dict, retries: int = 6):
    """
    Append a single shelter row with full retry + reconnect.

    Catches:
      - gspread.APIError       (quota / server-side errors)
      - requests.ConnectionError  (WinError 10054, aborted connection)
      - requests.Timeout
      - Any other Exception    (safety net)

    Strategy: exponential backoff (2^attempt seconds).
    On network errors → reconnect before retrying.
    """
    global _ws
    address = shelter.get("address", "")
    row = [
        shelter.get("name", ""),
        address,
        _parse_city(address),
        shelter.get("phone", ""),
        shelter.get("website", ""),
        "; ".join(shelter.get("emails", [])),
        shelter.get("place_id", ""),
        shelter.get("source_city", ""),
        shelter.get("source_state", ""),
    ]

    for attempt in range(1, retries + 1):
        try:
            _ws.append_row(row, value_input_option="USER_ENTERED")
            return                           # ✅ success

        except (ConnectionError, Timeout) as e:
            # ── Network-level failure (WinError 10054, etc.) ──
            wait = 2 ** attempt              # 2, 4, 8, 16, 32, 64s
            logger.warning(
                f"🔌 Network error (attempt {attempt}/{retries}): {e}. "
                f"Reconnecting + retrying in {wait}s…"
            )
            time.sleep(wait)
            try:
                _reconnect()                 # fresh connection before retry
            except RuntimeError:
                logger.error("❌ Reconnect failed — skipping this row.")
                return

        except gspread.exceptions.APIError as e:
            # ── Google API error (quota, 429, 5xx) ───────────
            wait = 2 ** attempt
            logger.warning(
                f"📋 Sheets API error (attempt {attempt}/{retries}): {e}. "
                f"Retrying in {wait}s…"
            )
            time.sleep(wait)

        except Exception as e:
            # ── Catch-all safety net ─────────────────────────
            wait = 2 ** attempt
            logger.warning(
                f"⚠️  Unexpected error (attempt {attempt}/{retries}): {e}. "
                f"Retrying in {wait}s…"
            )
            time.sleep(wait)

    logger.error(f"❌ All {retries} retries failed — skipping: {shelter.get('name')}")