# ============================================================
# email_extractor.py  –  Scrape emails from shelter websites
# ============================================================

import re
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from logger import logger
from config import (
    DELAY_BETWEEN_SCRAPES, REQUEST_TIMEOUT,
    MAX_RETRIES, USER_AGENT
)

# Regex that matches most common email formats
EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

# Pages most likely to have contact info
CONTACT_PATHS = [
    "/contact", "/contact-us", "/contactus",
    "/about",   "/about-us",   "/aboutus",
    "/info",    "/reach-us",   "/get-in-touch",
]

# Domains we never want to treat as emails
IGNORED_DOMAINS = {
    "sentry.io", "example.com", "domain.com",
    "yourdomain.com", "email.com", "wixpress.com",
    "squarespace.com", "wordpress.com",
}


def _is_valid_email(email: str) -> bool:
    domain = email.split("@")[-1].lower()
    if domain in IGNORED_DOMAINS:
        return False
    if domain.endswith((".png", ".jpg", ".gif", ".svg", ".js", ".css")):
        return False
    return True


def _fetch_html(url: str, session: requests.Session) -> str | None:
    headers = {"User-Agent": USER_AGENT}
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:
            wait = attempt * 2
            logger.debug(f"    Fetch failed ({url}) attempt {attempt}: {e}. Waiting {wait}s…")
            time.sleep(wait)
    return None


def _extract_emails_from_html(html: str) -> set[str]:
    emails = set(EMAIL_REGEX.findall(html))
    return {e.lower() for e in emails if _is_valid_email(e)}


def _try_contact_pages(base_url: str, session: requests.Session) -> set[str]:
    """Try known contact-page paths and collect any emails found."""
    found = set()
    parsed = urlparse(base_url)
    root   = f"{parsed.scheme}://{parsed.netloc}"

    for path in CONTACT_PATHS:
        url  = urljoin(root, path)
        html = _fetch_html(url, session)
        if html:
            emails = _extract_emails_from_html(html)
            if emails:
                logger.debug(f"    Found emails on {url}: {emails}")
                found.update(emails)
        time.sleep(0.3)   # small pause between sub-page fetches

    return found


def scrape_emails_from_website(website_url: str) -> list[str]:
    """
    1. Fetch the homepage and extract any visible emails.
    2. If none found, probe common contact-page paths.
    Returns a sorted, deduplicated list of emails.
    """
    if not website_url:
        return []

    emails: set[str] = set()

    with requests.Session() as session:
        # Step 1 – homepage
        html = _fetch_html(website_url, session)
        if html:
            emails.update(_extract_emails_from_html(html))

            # Also check href="mailto:…" links via BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup.find_all("a", href=True):
                href = tag["href"]
                if href.startswith("mailto:"):
                    email = href[7:].split("?")[0].strip().lower()
                    if email and _is_valid_email(email):
                        emails.add(email)

        # Step 2 – probe contact pages if homepage gave nothing
        if not emails:
            logger.debug(f"    No emails on homepage, probing contact pages for {website_url}")
            emails.update(_try_contact_pages(website_url, session))

    time.sleep(DELAY_BETWEEN_SCRAPES)
    return sorted(emails)