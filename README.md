# Simple Web Crawler

A lightweight Python script for crawling and extracting text content from website pages using their sitemap.

## Features
- Fetches all URLs listed in a sitemap (`.xml`)
- Extracts readable text from each page
- Saves data incrementally to `.jsonl`
- Supports resume — skips already scraped URLs
- Low memory usage and polite rate limiting

## Requirements
- Python 3.8+
- Install dependencies:
```bash
pip install requests beautifulsoup4 lxml
```

## Configuration

Before running, open `main.py` and adjust the constants at the top to match your target site or settings:

```python
BASE = "https://example.com/"
HEADERS = {"User-Agent": "MyScraperBot/1.0 (+your-email@example.com)"}
OUTPUT_FILE = "scraped_data.jsonl"
SITEMAP_URL = "https://example.com/sitemap.xml"
```

You can customize:

* `BASE`: the site root URL.
* `HEADERS`: your custom user-agent or contact info.
* `OUTPUT_FILE`: name of the output file.
* `SITEMAP_URL`: which sitemap to use (you can use multiple if needed).

## Usage

Run the crawler:

```bash
python3 main.py
```

The script will:

1. Fetch all URLs from the sitemap.
2. Download each page’s HTML.
3. Extract and clean visible text.
4. Save results as newline-delimited JSON (`.jsonl`), one record per page.

Example output (`scraped_data.jsonl`):

```json
{"url": "https://example.com/page1", "text": "This is the main content of the page..."}
{"url": "https://example.com/page2", "text": "Another page’s extracted text..."}
```

## Notes

* The crawler skips image, PDF, and archive files automatically.
* It resumes automatically if re-run — no duplicate scraping.
* You can adjust the crawl delay (`time.sleep`) for different speeds.

## License

This project is released under the MIT License.
