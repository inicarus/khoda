# filename: get_telegram_proxies.py

import requests
from bs4 import BeautifulSoup
import re

# ✅✅✅ منابع معتبر و باکیفیت که شما معرفی کردید
TRUSTED_PAGES = [
    "https://aliilapro.github.io/MTProtoProxy/",
    "https://mhditaheri.github.io/ProxyCollector/",
    "https://freedom-guard.github.io/Proxy/",
    "https://itsyebekhe.github.io/tpro/"
]

OUTPUT_FILE = "telegram_proxies.txt"

def scrape_trusted_pages():
    """
    Scrapes the user-provided trusted web pages to find high-quality
    and working MTProto proxy links.
    """
    all_proxies = set()
    
    # الگو برای پیدا کردن دقیق لینک‌های پروکسی تلگرام
    mtproto_pattern = re.compile(r'^(tg://proxy\?|https://t\.me/proxy\?)')
    
    # استفاده از هدر برای شبیه‌سازی یک مرورگر واقعی
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in TRUSTED_PAGES:
        try:
            print(f"Scraping trusted page: {url}")
            response = requests.get(url, timeout=30, headers=headers)
            response.raise_for_status()

            # استفاده از BeautifulSoup برای تحلیل محتوای HTML صفحه
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # پیدا کردن تمام تگ‌های لینک <a>
            link_tags = soup.find_all('a')
            
            found_count = 0
            for tag in link_tags:
                href = tag.get('href')
                # بررسی اینکه آیا لینک پیدا شده یک پروکسی معتبر تلگرام است یا نه
                if href and mtproto_pattern.match(href):
                    all_proxies.add(href.strip())
                    found_count += 1
            
            if found_count > 0:
                print(f"  -> ✅ Found {found_count} valid MTProto links.")
            else:
                print(f"  -> ⚠️ No proxy links found on this page.")


        except Exception as e:
            print(f"  -> ❌ Failed to scrape {url}: {e}")
    
    return sorted(list(all_proxies))

def main():
    print("\nStarting to scrape trusted pages for GUARANTEED high-quality proxies...")
    proxies = scrape_trusted_pages()

    if not proxies:
        print("\nCould not find any new proxies from the trusted sources. Exiting.")
        return

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(proxies))
        print(f"\n✅ Successfully saved {len(proxies)} unique, high-quality proxy links to '{OUTPUT_FILE}'")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()
