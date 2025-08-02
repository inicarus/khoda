# filename: proxy_sender_inline.py

import os
import requests
import random
import json
from datetime import datetime
import jdatetime

# --- تنظیمات اصلی ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
PROXY_FILE = 'telegram_proxies.txt'
PROXY_COUNT_TO_SEND = 16 # بهتر است عددی زوج باشد تا دکمه‌ها مرتب باشند

def create_message_header():
    """هدر زیبا و سفارشی با تاریخ و زمان فعلی ایجاد می‌کند."""
    
    # دریافت زمان و تاریخ فعلی
    now = datetime.now()
    jalali_date = jdatetime.datetime.fromgregorian(datetime=now).strftime('%Y/%m/%d')
    current_time = now.strftime('%H:%M:%S')

    # متن هدر با جایگزینی‌های لازم
    # از یک فونت فانتزی برای Proxyfig استفاده کردیم
    header = f"""
╭⋟────𓄂ꪴꪰ𓆃────╮
 | 𓐄𓐅𓐆𓐇 PЯӨXYFĪG 𓐇𓐆𓐅𓐄 ⁮⁮⁮|
╰────────────⋞╯

     💀PʀᴏxʏSᴋᴜʟʟ💀 
❚⫘⫘⫘⫘⫘⫘⫘❚
        ☠️MTProto II☠️ 
            
▬▭▬▭𓐄🧌𓐄▭▬▭▬
{current_time} 𓍯 {jalali_date}
"""
    return header

def create_inline_keyboard(proxies):
    """لیستی از دکمه‌های شیشه‌ای برای پروکسی‌ها ایجاد می‌کند."""
    keyboard = []
    row = []
    # به هر پروکسی یک ایموجی و شماره اختصاص می‌دهیم
    for i, proxy_url in enumerate(proxies):
        button = {
            'text': f'🟢 اتصال {i + 1}',
            'url': proxy_url
        }
        row.append(button)
        # هر ردیف شامل ۲ دکمه خواهد بود
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    # اگر تعداد پروکسی‌ها فرد باشد، دکمه آخر را در یک ردیف جدا قرار می‌دهیم
    if row:
        keyboard.append(row)
        
    return {'inline_keyboard': keyboard}


def send_proxies_to_telegram(proxies):
    """پیام را به همراه دکمه‌های شیشه‌ای به تلگرام ارسال می‌کند."""
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ خطا: BOT_TOKEN یا CHAT_ID در متغیرهای محیطی (یا GitHub Secrets) تنظیم نشده است.")
        exit(1)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    message_text = create_message_header()
    reply_markup = create_inline_keyboard(proxies)
    
    payload = {
        'chat_id': CHAT_ID,
        'text': message_text,
        # ✅✅✅ مهم‌ترین بخش: ارسال دکمه‌های شیشه‌ای
        'reply_markup': json.dumps(reply_markup),
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
        print(f"✅ با موفقیت {len(proxies)} پروکسی به صورت دکمه‌ای به کانال ارسال شد.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ خطای HTTP از سمت تلگرام: {e.response.status_code} - {e.response.text}")
        exit(1)
    except Exception as e:
        print(f"❌ یک خطای پیش‌بینی‌نشده رخ داد: {e}")
        exit(1)

def main():
    try:
        with open(PROXY_FILE, 'r', encoding='utf-8') as f:
            # فقط خطوطی که حاوی 'https://t.me/proxy?' هستند را می‌خوانیم تا مطمئن شویم لینک پروکسی هستند
            proxies = [line.strip() for line in f if line.strip().startswith('https://t.me/proxy?')]
    except FileNotFoundError:
        print(f"❌ خطا: فایل پروکسی '{PROXY_FILE}' پیدا نشد.")
        return

    if not proxies:
        print("فایل پروکسی خالی است. پروکسی برای ارسال وجود ندارد.")
        return
        
    # انتخاب تصادفی تعدادی پروکسی برای ارسال
    selected_proxies = random.sample(proxies, min(len(proxies), PROXY_COUNT_TO_SEND))
    
    send_proxies_to_telegram(selected_proxies)

if __name__ == "__main__":
    main()
