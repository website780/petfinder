# ============================================================
# logger.py
# ============================================================

import logging
import sys
from config import PROGRESS_LOG, ERROR_LOG

def setup_logger():
    logger = logging.getLogger("ShelterScraper")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ── Console handler (INFO and above) ─────────────────────
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    # ── Progress file handler (INFO and above) ────────────────
    fh = logging.FileHandler(PROGRESS_LOG, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)

    # ── Error file handler (WARNING and above) ────────────────
    eh = logging.FileHandler(ERROR_LOG, encoding="utf-8")
    eh.setLevel(logging.WARNING)
    eh.setFormatter(fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.addHandler(eh)

    return logger

logger = setup_logger()