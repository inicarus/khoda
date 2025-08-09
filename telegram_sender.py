# filename: proxy_sender_final.py

import os
import requests
import random
import json
from datetime import datetime
import jdatetime
import pytz

# --- ⚙️ تنظیمات اصلی ---
# این مقادیر را باید در GitHub Secrets یا متغیرهای محیطی سیستم خود تنظیم کنید
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# نام فایل حاوی پروکسی‌ها
PROXY_FILE = 'telegram_proxies.txt'

# تعداد پروکسی برای ارسال در هر بار (بهتر است زوج باشد)
PROXY_COUNT_TO_SEND = 16

def create_message_header():
    """هدر زیبا و سفارشی با تاریخ و زمان فعلی ایجاد می‌کند."""
    
    # دریافت زمان و تاریخ فعلی
    now = datetime.now()
    jalali_date = jdatetime.datetime.fromgregorian(datetime=now).strftime('%Y/%m/%d')
    current_time = now.strftime('%H:%M:%S')

    # متن هدر با فونت فانتزی برای Proxyfig
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
    """لیستی از دکمه‌های شیشه‌ای برای پروکسی‌ها در دو ستون ایجاد می‌کند."""
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
        'reply_markup': json.dumps(reply_markup), # ارسال دکمه‌های شیشه‌ای
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
    """تابع اصلی برنامه: خواندن پروکسی‌ها، تبدیل فرمت و ارسال."""
    try:
        with open(PROXY_FILE, 'r', encoding='utf-8') as f:
            # ✅ تغییر کلیدی: خواندن لینک‌های tg:// و تبدیل خودکار آن‌ها
            proxies = [
                line.strip().replace('tg://proxy?', 'https://t.me/proxy?') 
                for line in f if line.strip().startswith('tg://proxy?')
            ]
    except FileNotFoundError:
        print(f"❌ خطا: فایل پروکسی '{PROXY_FILE}' پیدا نشد.")
        return

    if not proxies:
        print("فایل پروکسی خالی است یا هیچ لینک معتبر tg:// در آن پیدا نشد.")
        return
        
    # انتخاب تصادفی تعدادی پروکسی برای ارسال
    selected_proxies = random.sample(proxies, min(len(proxies), PROXY_COUNT_TO_SEND))
    
    send_proxies_to_telegram(selected_proxies)

if __name__ == "__main__":
    main()
