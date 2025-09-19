# filename: get_telegram_proxies.py

import requests
import re

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
    
    # --- ✅✅✅ تغییر نهایی و حیاتی: استفاده از non-capturing group (?:...) ---
    # این الگو حالا کل لینک پروکسی را برمی‌گرداند، نه فقط قسمت اول آن را.
    mtproto_pattern = re.compile(r'(?:https?://t\.me/proxy\?|tg://proxy\?)\S{30,}')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in TRUSTED_PAGES:
        try:
            print(f"Scraping trusted page: {url}")
            response = requests.get(url, timeout=30, headers=headers)
            response.raise_for_status()

            found_proxies = mtproto_pattern.findall(response.text)
            
            if found_proxies:
                print(f"  -> ✅ Found {len(found_proxies)} potential links.")
                for proxy in found_proxies:
                    all_proxies.add(proxy.strip())
            else:
                print(f"  -> ⚠️ No valid proxy links found on this page.")

        except requests.exceptions.RequestException as e:
            print(f"  -> ❌ Network error while scraping {url}: {e}")
        except Exception as e:
            print(f"  -> ❌ An unexpected error occurred at {url}: {e}")
    
    return sorted(list(all_proxies))

def main():
    print("\nStarting to scrape trusted pages for high-quality MTProto proxies...")
    proxies = scrape_trusted_pages()

    if not proxies:
        print("\nCould not find any new MTProto proxies from the trusted sources. Exiting.")
        # یک فایل خالی ایجاد می‌کنیم تا workflow در مقایسه فایل به مشکل نخورد
        open(OUTPUT_FILE, 'w').close()
        return

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(proxies))
        print(f"\n✅ Successfully saved {len(proxies)} unique MTProto proxy links to '{OUTPUT_FILE}'")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()
