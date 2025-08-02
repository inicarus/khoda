# filename: telegram_sender.py

import os
import requests
import random
import re

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
PROXY_FILE = 'telegram_proxies.txt'
PROXY_COUNT_TO_SEND = 15

def escape_markdown_v2(text):
    """Escapes special characters for Telegram's MarkdownV2 parse mode."""
    # لیست کاراکترهایی که باید در MarkdownV2 فرار داده شوند
    escape_chars = r'[_*\[\]()~`>#+\-=|{}.!]'
    return re.sub(f'({escape_chars})', r'\\\1', text)

def send_message_to_telegram(proxies):
    """Sends a formatted list of MTProto proxies using MarkdownV2."""
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: BOT_TOKEN or CHAT_ID is not set in GitHub Secrets.")
        exit(1)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    message_parts = []
    for p in proxies:
        # ✅✅✅ کار اصلی اینجاست: لینک پروکسی را escape می‌کنیم
        escaped_proxy_url = escape_markdown_v2(p)
        # سپس لینک escape شده را در فرمت MarkdownV2 قرار می‌دهیم
        message_parts.append(f"💠 [اتصال به پروکسی]({escaped_proxy_url})")
    
    header = "🚀 *لیست پروکسی‌های فعال و جدید MTProto*\n\n"
    footer = "\n\n⭐️ @proxyfig" # آیدی کانال خود را جایگزین کنید
    
    message_body = "\n\n".join(message_parts)
    final_message = header + message_body + footer
    
    payload = {
        'chat_id': CHAT_ID,
        'text': final_message,
        # ✅✅✅ تغییر مهم: استفاده از MarkdownV2
        'parse_mode': 'MarkdownV2',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status() # این خط اگر کد وضعیت خطا باشد، استثنا ایجاد می‌کند
        print(f"✅ Successfully sent {len(proxies)} MTProto proxies to the channel.")
    except requests.exceptions.HTTPError as e:
        # نمایش متن کامل خطای تلگرام برای دیباگ کردن بهتر
        print(f"❌ HTTP Error from Telegram: {e.response.status_code} - {e.response.text}")
        exit(1)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        exit(1)

def main():
    try:
        with open(PROXY_FILE, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Proxy file '{PROXY_FILE}' not found.")
        return

    if not proxies:
        print("Proxy file is empty. No proxies to send.")
        return
        
    selected_proxies = random.sample(proxies, min(len(proxies), PROXY_COUNT_TO_SEND))
    
    send_message_to_telegram(selected_proxies)

if __name__ == "__main__":
    main()
