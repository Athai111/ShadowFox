"""
ShadowFox Internship - Task 1: Web Scraper
==========================================
Scrapes data from public websites using BeautifulSoup.
Targets:
  1. books.toscrape.com  - Book titles, prices, ratings
  2. quotes.toscrape.com - Quotes, authors, tags
Demo mode activates automatically if live sites are unreachable.
Saves all results to CSV files with a full summary report.
"""

import requests
from bs4 import BeautifulSoup
import csv, time, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
SEP = "=" * 60

# ── Demo HTML (mirrors real site structure) ──────────────────────────────────
DEMO_BOOKS = """<html><body>
<article class="product_pod"><h3><a title="A Light in the Attic" href="#">x</a></h3><p class="price_color">£51.77</p><p class="star-rating Five"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="Tipping the Velvet" href="#">x</a></h3><p class="price_color">£53.74</p><p class="star-rating One"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="Soumission" href="#">x</a></h3><p class="price_color">£50.10</p><p class="star-rating One"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="Sharp Objects" href="#">x</a></h3><p class="price_color">£47.82</p><p class="star-rating Four"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="Sapiens: A Brief History of Humankind" href="#">x</a></h3><p class="price_color">£54.23</p><p class="star-rating Five"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="The Remains of the Day" href="#">x</a></h3><p class="price_color">£35.02</p><p class="star-rating Five"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="The Midnight Library" href="#">x</a></h3><p class="price_color">£29.99</p><p class="star-rating Four"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="Atomic Habits" href="#">x</a></h3><p class="price_color">£14.99</p><p class="star-rating Five"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="The Hitchhiker's Guide to the Galaxy" href="#">x</a></h3><p class="price_color">£12.49</p><p class="star-rating Five"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="1984" href="#">x</a></h3><p class="price_color">£10.99</p><p class="star-rating Five"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="To Kill a Mockingbird" href="#">x</a></h3><p class="price_color">£11.49</p><p class="star-rating Four"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="The Great Gatsby" href="#">x</a></h3><p class="price_color">£9.99</p><p class="star-rating Three"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="Brave New World" href="#">x</a></h3><p class="price_color">£13.49</p><p class="star-rating Three"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="The Alchemist" href="#">x</a></h3><p class="price_color">£16.99</p><p class="star-rating Four"></p><p class="availability">In stock</p></article>
<article class="product_pod"><h3><a title="Crime and Punishment" href="#">x</a></h3><p class="price_color">£8.99</p><p class="star-rating Two"></p><p class="availability">In stock</p></article>
</body></html>"""

DEMO_QUOTES = """<html><body>
<div class="quote"><span class="text">The world as we have created it is a process of our thinking.</span><small class="author">Albert Einstein</small><a class="tag">change</a><a class="tag">thinking</a><a class="tag">world</a></div>
<div class="quote"><span class="text">It is our choices, Harry, that show what we truly are, far more than our abilities.</span><small class="author">J.K. Rowling</small><a class="tag">abilities</a><a class="tag">choices</a></div>
<div class="quote"><span class="text">There are only two ways to live your life. One is as though nothing is a miracle.</span><small class="author">Albert Einstein</small><a class="tag">inspirational</a><a class="tag">life</a><a class="tag">miracle</a></div>
<div class="quote"><span class="text">The person who has not pleasure in a good novel must be intolerably stupid.</span><small class="author">Jane Austen</small><a class="tag">books</a><a class="tag">classic</a><a class="tag">humor</a></div>
<div class="quote"><span class="text">Imperfection is beauty, madness is genius and it is better to be absolutely ridiculous than boring.</span><small class="author">Marilyn Monroe</small><a class="tag">be-yourself</a><a class="tag">inspirational</a></div>
<div class="quote"><span class="text">Try not to become a man of success. Rather become a man of value.</span><small class="author">Albert Einstein</small><a class="tag">success</a><a class="tag">value</a></div>
<div class="quote"><span class="text">It is better to be hated for what you are than to be loved for what you are not.</span><small class="author">Andre Gide</small><a class="tag">life</a><a class="tag">love</a></div>
<div class="quote"><span class="text">I have not failed. I have just found 10,000 ways that won't work.</span><small class="author">Thomas A. Edison</small><a class="tag">failure</a><a class="tag">inspirational</a></div>
<div class="quote"><span class="text">A woman is like a tea bag; you never know how strong it is until it is in hot water.</span><small class="author">Eleanor Roosevelt</small><a class="tag">women</a><a class="tag">strength</a></div>
<div class="quote"><span class="text">A day without sunshine is like, you know, night.</span><small class="author">Steve Martin</small><a class="tag">humor</a><a class="tag">obvious</a></div>
</body></html>"""

# ── Helpers ──────────────────────────────────────────────────────────────────
def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return BeautifulSoup(r.text, "lxml")
    except Exception as e:
        print(f"  [WARN] Cannot reach {url}: {type(e).__name__}")
        return None

def parse_books(soup):
    books = []
    for a in soup.find_all("article", class_="product_pod"):
        t = a.find("h3").find("a")
        p = a.find("p", class_="price_color")
        r = a.find("p", class_="star-rating")
        av = a.find("p", class_="availability")
        books.append({
            "title": t["title"] if t else "N/A",
            "price": p.text.strip() if p else "N/A",
            "rating_stars": RATING_MAP.get((r["class"][1] if r else "Zero"), 0),
            "availability": av.text.strip() if av else "N/A",
        })
    return books

def parse_quotes(soup):
    quotes = []
    for d in soup.find_all("div", class_="quote"):
        tx = d.find("span", class_="text")
        au = d.find("small", class_="author")
        tg = d.find_all("a", class_="tag")
        quotes.append({
            "quote": tx.text.strip().strip("\u201c\u201d") if tx else "N/A",
            "author": au.text.strip() if au else "N/A",
            "tags": ", ".join(t.text.strip() for t in tg),
        })
    return quotes

# ── Scrapers ─────────────────────────────────────────────────────────────────
def scrape_books(max_pages=3):
    print(f"\n{'-'*60}\n  SCRAPER 1 -- Books (books.toscrape.com)\n{'-'*60}")
    all_books, live = [], False
    for page in range(1, max_pages + 1):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        print(f"  Fetching page {page}/{max_pages}: {url}")
        soup = fetch_page(url)
        if soup:
            live = True
            all_books.extend(parse_books(soup))
            time.sleep(0.5)
        else:
            break
    if not live:
        print("  [DEMO MODE] Using bundled HTML sample (network restricted).")
        all_books = parse_books(BeautifulSoup(DEMO_BOOKS, "lxml"))
    print(f"\n  Total books scraped: {len(all_books)}")
    return all_books

def scrape_quotes(max_pages=3):
    print(f"\n{'-'*60}\n  SCRAPER 2 -- Quotes (quotes.toscrape.com)\n{'-'*60}")
    all_quotes, live = [], False
    for page in range(1, max_pages + 1):
        url = f"https://quotes.toscrape.com/page/{page}/"
        print(f"  Fetching page {page}/{max_pages}: {url}")
        soup = fetch_page(url)
        if soup:
            live = True
            all_quotes.extend(parse_quotes(soup))
            time.sleep(0.5)
        else:
            break
    if not live:
        print("  [DEMO MODE] Using bundled HTML sample (network restricted).")
        all_quotes = parse_quotes(BeautifulSoup(DEMO_QUOTES, "lxml"))
    print(f"\n  Total quotes scraped: {len(all_quotes)}")
    return all_quotes

# ── CSV savers ───────────────────────────────────────────────────────────────
def save_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(rows)
    return path

# ── Summary printers ─────────────────────────────────────────────────────────
def print_books_summary(books):
    print(f"\n{SEP}\n  BOOKS SUMMARY\n{SEP}")
    if not books:
        print("  No data."); return
    avg_r = sum(b["rating_stars"] for b in books) / len(books)
    prices = []
    for b in books:
        try: prices.append(float(b["price"].replace("£","").replace("\xa3","").strip()))
        except: pass
    dist = {1:0,2:0,3:0,4:0,5:0}
    for b in books: dist[b["rating_stars"]] = dist.get(b["rating_stars"],0)+1
    print(f"  Total books   : {len(books)}")
    print(f"  Avg rating    : {'*'*round(avg_r)} ({avg_r:.2f}/5)")
    if prices:
        print(f"  Price range   : GBP{min(prices):.2f} - GBP{max(prices):.2f}")
        print(f"  Average price : GBP{sum(prices)/len(prices):.2f}")
    print(f"\n  Rating Distribution:")
    for s in range(5,0,-1): print(f"    {'*'*s:<5} ({dist[s]:>3}) {'#'*dist[s]}")
    print(f"\n  Sample books:")
    for b in books[:5]:
        print(f"    [{'*'*b['rating_stars']:<5}] {b['price']}  {b['title'][:48]}")

def print_quotes_summary(quotes):
    print(f"\n{SEP}\n  QUOTES SUMMARY\n{SEP}")
    if not quotes:
        print("  No data."); return
    ac, tc = {}, {}
    for q in quotes:
        ac[q["author"]] = ac.get(q["author"],0)+1
        for t in q["tags"].split(", "):
            if t: tc[t]=tc.get(t,0)+1
    top_a = sorted(ac.items(),key=lambda x:-x[1])[:5]
    top_t = sorted(tc.items(),key=lambda x:-x[1])[:6]
    print(f"  Total quotes  : {len(quotes)}")
    print(f"\n  Top Authors:")
    for a,c in top_a: print(f"    {c:>2}x  {a}")
    print(f"\n  Popular Tags  : {', '.join(f'{t}({c})' for t,c in top_t)}")
    print(f"\n  Sample quotes:")
    for q in quotes[:3]:
        txt = q["quote"][:72]+("..." if len(q["quote"])>72 else "")
        print(f'\n    "{txt}"')
        print(f"       -- {q['author']}")

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print(f"\n{SEP}\n  ShadowFox Internship -- Task 1: Web Scraper")
    print(f"  Libraries : requests + BeautifulSoup4 + lxml\n{SEP}")

    books  = scrape_books(max_pages=3)
    quotes = scrape_quotes(max_pages=3)

    bp = save_csv(os.path.join(OUTPUT_DIR,"books.csv"),
                  ["title","price","rating_stars","availability"], books)
    qp = save_csv(os.path.join(OUTPUT_DIR,"quotes.csv"),
                  ["quote","author","tags"], quotes)

    print_books_summary(books)
    print_quotes_summary(quotes)

    print(f"\n{SEP}\n  OUTPUT FILES\n{SEP}")
    print(f"  Books  -> {bp}")
    print(f"  Quotes -> {qp}")
    print(f"\n  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{SEP}\n")

if __name__ == "__main__":
    main()
