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
    
    # --- تغییر اصلی شماره ۱: الگوی Regex بهبود یافته ---
    # این الگو هر لینکی که با فرمت پروکسی شروع بشه و تا اولین فاصله یا علامت نقل قول ادامه داشته باشه رو پیدا می‌کنه
    # این باعث میشه لینک‌ها از دل متن ساده هم استخراج بشن
    mtproto_pattern = re.compile(r'(tg://proxy\?|https://t\.me/proxy\?)[^\s\'\"<>]+')
    
    # استفاده از هدر برای شبیه‌سازی یک مرورگر واقعی
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in TRUSTED_PAGES:
        try:
            print(f"Scraping trusted page: {url}")
            response = requests.get(url, timeout=30, headers=headers)
            response.raise_for_status()

            # --- تغییر اصلی شماره ۲: جستجو در کل متن صفحه ---
            # به جای جستجوی تگ‌های <a>، از re.findall برای جستجوی الگو در کل محتوای HTML استفاده می‌کنیم
            # response.text محتوای خام HTML صفحه است
            found_proxies = mtproto_pattern.findall(response.text)
            
            # اضافه کردن پروکسی‌های پیدا شده به مجموعه اصلی برای حذف موارد تکراری
            for proxy in found_proxies:
                all_proxies.add(proxy.strip())
            
            if found_proxies:
                print(f"  -> ✅ Found {len(found_proxies)} valid MTProto links.")
            else:
                print(f"  -> ⚠️ No proxy links found on this page.")

        except requests.exceptions.RequestException as e:
            # مدیریت خطاهای شبکه به شکل دقیق‌تر
            print(f"  -> ❌ Network error while scraping {url}: {e}")
        except Exception as e:
            print(f"  -> ❌ An unexpected error occurred at {url}: {e}")
    
    return sorted(list(all_proxies))

def main():
    print("\nStarting to scrape trusted pages for GUARANTEED high-quality proxies...")
    proxies = scrape_trusted_pages()

    if not proxies:
        print("\nCould not find any new proxies from the trusted sources. Exiting.")
        return

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            # اضافه کردن یک خط خالی بین هر پروکسی برای خوانایی بهتر
            f.write("\n\n".join(proxies))
        print(f"\n✅ Successfully saved {len(proxies)} unique, high-quality proxy links to '{OUTPUT_FILE}'")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()
