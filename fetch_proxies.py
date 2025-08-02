# filename: fetch_proxies.py

import requests
import base64
import time

# =================================================================
# !! مهم: این لیست را با لیست کامل URL ها از فایل script.js جایگزین کن !!
# =================================================================
URLS_TO_FETCH = [
    "https://raw.githubusercontent.com/yebekhe/V2Hub-Mirror/main/sub/sub_merge.json",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/v2ray-configs/main/sub/mix",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list_raw.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/V2Ray-free-configs/main/sub",
    "https://raw.githubusercontent.com/MrPooyaX/V2Ray-Configs/main/All-Configs-so-far-for-V2Ray",
    "https://raw.githubusercontent.com/MrPooyaX/V2Ray-Configs/main/All-Configs-so-far-for-V2Ray-node",
    "https://raw.githubusercontent.com/hossein-mohseni/V2RAY-CONFIGS/main/h-VPN",
    "https://raw.githubusercontent.com/Freedom-Guard/V2Ray/main/Subscription.txt",
    "https://raw.githubusercontent.com/ldc1994/v2ray-sub/main/sub/mix",
    "https://raw.githubusercontent.com/vahidhendi/V2ray-Config/main/All%20configs",
    "https://raw.githubusercontent.com/ferdosmark/V2ray-Sub/main/V2ray",
    "https://raw.githubusercontent.com/hooshmandproxy/V2Ray-Config/main/All-Configs",
    "https://raw.githubusercontent.com/hooshmandproxy/V2Ray-Config/main/sub"
]

def fetch_content_from_url(url):
    """Fetches content from a single URL."""
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.text
        else:
            print(f"  -> Failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"  -> Error fetching {url}: {e}")
        return None

def decode_base64_content(encoded_str):
    """Decodes a base64 encoded string."""
    try:
        return base64.b64decode(encoded_str).decode('utf-8')
    except Exception:
        return encoded_str # Return original if decoding fails

def main():
    """Main function to fetch, process, and save proxies."""
    all_proxies = []

    for url in URLS_TO_FETCH:
        content = fetch_content_from_url(url)
        if content:
            # Some URLs might be base64 encoded, some might be plain text.
            # We decode them, then split by lines.
            decoded_content = decode_base64_content(content)
            proxies = decoded_content.strip().split('\n')
            
            # Clean up and add valid-looking proxies
            for proxy in proxies:
                proxy = proxy.strip()
                if proxy.startswith(('vless://', 'vmess://', 'trojan://', 'ss://', 'ssr://')):
                    all_proxies.append(proxy)
        time.sleep(1) # Be respectful to servers

    # Remove duplicates
    unique_proxies = sorted(list(set(all_proxies)))

    if unique_proxies:
        with open('proxies_all.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_proxies))
        print(f"\nSuccessfully collected and saved {len(unique_proxies)} unique proxies to proxies_all.txt")
    else:
        print("\nCould not fetch any new proxies.")

if __name__ == "__main__":
    main()
