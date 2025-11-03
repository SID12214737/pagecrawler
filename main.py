#!/usr/bin/env python3
# quick_scrape_brb.py
# Requires: pip install requests beautifulsoup4 lxml

import os
import time
import json
import random
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

BASE = "https://brb.uz/"
HEADERS = {"User-Agent": "MyScraperBot/1.0 (+your-email@example.com)"}
OUTPUT_FILE = "brb_scraped.jsonl"
SITEMAP_URL = "https://brb.uz/sitemap-uz.xml"


def get_sitemap_urls(sitemap_url):
    """Fetch and parse sitemap.xml -> list of URLs."""
    r = requests.get(sitemap_url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    urls = [
        elem.findtext("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")
    ]
    return [u for u in urls if u]


def extract_main_text(html):
    """Extract main visible text from HTML."""
    soup = BeautifulSoup(html, "lxml")
    candidates = soup.select("main, article, .content, .article, .news-item, #content")

    if candidates:
        texts = []
        for c in candidates:
            for s in c(["script", "style", "noscript"]):
                s.decompose()
            texts.append(c.get_text(separator=" ", strip=True))
        return "\n\n".join(texts)

    body = soup.body
    if not body:
        return ""
    for s in body(["script", "style", "noscript"]):
        s.decompose()
    return body.get_text(separator=" ", strip=True)


def load_done_urls():
    """Read already scraped URLs from JSONL output (for resume)."""
    if not os.path.exists(OUTPUT_FILE):
        return set()
    done = set()
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                done.add(record["url"])
            except Exception:
                continue
    return done


def save_page(url, text):
    """Append one scraped page to JSONL file."""
    record = {"url": url, "text": text}
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    urls = get_sitemap_urls(SITEMAP_URL)
    print(f"Found {len(urls)} URLs in sitemap")

    done = load_done_urls()
    print(f"Already scraped {len(done)} pages, skipping those")

    for i, u in enumerate(urls):
        if u in done:
            continue
        if u.endswith((".pdf", ".jpg", ".png", ".zip")):
            continue
        try:
            r = requests.get(u, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                print(f"[skip] {u} ({r.status_code})")
                continue

            text = extract_main_text(r.text)
            if text and len(text) > 50:
                save_page(u, text)
                print(f"[{i+1}/{len(urls)}] {u} -> {len(text):,} chars (saved)")
            else:
                print(f"[{i+1}/{len(urls)}] {u} -> too short, skipped")

        except Exception as e:
            print(f"[error] {u}: {e}")

        # polite randomized delay (0.8–1.5s)
        time.sleep(random.uniform(0.8, 1.5))

    print("\n✅ Done. All data saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
