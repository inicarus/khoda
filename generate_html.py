# filename: generate_html.py

from datetime import datetime
import pytz
import jdatetime

INPUT_FILE = "telegram_proxies.txt"
OUTPUT_HTML_FILE = "index.html" # نام فایل باید index.html باشد
REPOSITORY_URL = "https://github.com/inicarus/khoda" # آدرس ریپازیتوری خودتان را اینجا بگذارید

def generate_html_page(proxies):
    """
    از لیست پروکسی‌ها یک صفحه HTML ساده و زیبا می‌سازد.
    """
    # دریافت زمان و تاریخ فعلی به وقت تهران
    tehran_tz = pytz.timezone('Asia/Tehran')
    now_tehran = datetime.now(tehran_tz)
    jalali_date = jdatetime.datetime.fromgregorian(datetime=now_tehran).strftime('%Y/%m/%d')
    current_time = now_tehran.strftime('%H:%M:%S')

    # شروع ساخت محتوای HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لیست پروکسی‌های MTProto تلگرام</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Vazir', Roboto, Helvetica, Arial, sans-serif; background-color: #1a1a1a; color: #e0e0e0; line-height: 1.6; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background-color: #2c2c2c; padding: 25px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); }}
        h1, h2 {{ text-align: center; color: #4CAF50; }}
        .header-info {{ text-align: center; color: #aaa; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; border: 1px solid #444; text-align: center; }}
        th {{ background-color: #333; }}
        a {{ color: #81C784; text-decoration: none; font-weight: bold; }}
        a:hover {{ color: #a5d6a7; text-decoration: underline; }}
        footer {{ text-align: center; margin-top: 30px; color: #777; font-size: 0.9em; }}
        .btn {{ display: inline-block; padding: 10px 15px; background-color: #4CAF50; color: #fff; border-radius: 5px; text-decoration: none; transition: background-color 0.3s; }}
        .btn:hover {{ background-color: #45a049; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 پروکسی‌های MTProto تلگرام 🚀</h1>
        <div class="header-info">
            <p>آخرین بروزرسانی: <b>{jalali_date} - {current_time}</b> (به وقت ایران)</p>
            <p>این صفحه به صورت خودکار هر ۴ ساعت یک‌بار بروزرسانی می‌شود.</p>
        </div>
        
        <h2>لیست پروکسی‌های فعال</h2>
        <table>
            <thead>
                <tr>
                    <th>ردیف</th>
                    <th>لینک اتصال</th>
                </tr>
            </thead>
            <tbody>
    """

    # اضافه کردن هر پروکسی به عنوان یک ردیف در جدول
    for i, proxy in enumerate(proxies):
        html_content += f"""
                <tr>
                    <td>{i + 1}</td>
                    <td><a href="{proxy}" class="btn" target="_blank">اتصال به پروکسی</a></td>
                </tr>
        """

    # بستن تگ‌های HTML
    html_content += f"""
            </tbody>
        </table>
        <footer>
            <p>ساخته شده توسط پروژه <a href="{REPOSITORY_URL}" target="_blank">ProxyFig</a></p>
        </footer>
    </div>
</body>
</html>
    """

    # نوشتن محتوای نهایی در فایل
    try:
        with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ صفحه HTML با {len(proxies)} پروکسی در '{OUTPUT_HTML_FILE}' با موفقیت ساخته شد.")
    except IOError as e:
        print(f"❌ خطا در ساخت فایل HTML: {e}")

def main():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ فایل '{INPUT_FILE}' پیدا نشد. ابتدا اسکریپت get_telegram_proxies.py را اجرا کنید.")
        return

    if not proxies:
        print("⚠️ هیچ پروکسی برای ساخت صفحه HTML پیدا نشد.")
        return

    generate_html_page(proxies)

if __name__ == "__main__":
    main()
