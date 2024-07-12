import telebot
from datetime import datetime
import hijri_converter as hc
import pytz
import schedule
import time
from bs4 import BeautifulSoup
import requests
import random

api_token = '7458060169:AAHhQ-dTkcuCxSmD8uH0m9bDNpab8boCvOc'
bot = telebot.TeleBot(api_token)

def get_random_dua():
    url = "https://kalemtayeb.com/adeiah/section/16"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    dua_elements = soup.find_all("div", class_="item_nass")
    valid_duas = [dua.text.strip().replace('*', '۞').replace('"', '') for dua in dua_elements if dua.text.strip()]

    random_dua = ''
    while not random_dua or len(random_dua) > 150:
        random_dua = random.choice(valid_duas)

    return random_dua

def get_current_time():
    tz = pytz.timezone('Africa/Cairo')
    now = datetime.now(tz)
    hijri_date = hc.Gregorian(now.year, now.month, now.day).to_hijri()
    return now, hijri_date, tz

def arabic_am_pm(time_str):
    if 'AM' in time_str:
        return time_str.replace('AM', 'ص')
    elif 'PM' in time_str:
        return time_str.replace('PM', 'م')
    else:
        return time_str

def arabic_numerals(text):
    arabic_digits = {
        '0': '٠',
        '1': '١',
        '2': '٢',
        '3': '٣',
        '4': '٤',
        '5': '٥',
        '6': '٦',
        '7': '٧',
        '8': '٨',
        '9': '٩'
    }
    for eng, arabic in arabic_digits.items():
        text = text.replace(eng, arabic)
    return text

def update_group_info():
    chat_id = '-1001861299347'
    now, hijri_date, tz = get_current_time()
    current_time = now.strftime("%I:%M %p")
    current_time_arabic = arabic_am_pm(current_time)
    gregorian_date = now.strftime("%Y/%m/%d")
    gregorian_date_arabic = arabic_numerals(gregorian_date)
    
    arabic_month_names = {
        1: 'يناير',
        2: 'فبراير',
        3: 'مارس',
        4: 'أبريل',
        5: 'مايو',
        6: 'يونيو',
        7: 'يوليو',
        8: 'أغسطس',
        9: 'سبتمبر',
        10: 'أكتوبر',
        11: 'نوفمبر',
        12: 'ديسمبر'
    }
    month_arabic = arabic_month_names[now.month]
    day_name = now.strftime("%A")
    
    arabic_day_names = {
        'Monday': 'الاثنين',
        'Tuesday': 'الثلاثاء',
        'Wednesday': 'الأربعاء',
        'Thursday': 'الخميس',
        'Friday': 'الجمعة',
        'Saturday': 'السبت',
        'Sunday': 'الأحد'
    }
    
    dua = get_random_dua()
    new_about = f"«{dua}»\n" \
                "────────────────\n" \
                f"🕰╽الساعة الان بتوقيت مصر⇜ {current_time_arabic} ؛\n" \
                f"🌏╽التاريخ ⇜ {gregorian_date} ؛\n" \
                f"🌈╽اليوم⇜ {arabic_day_names[day_name]} ؛"
    
    # تحديث اسم المجموعة والوصف
    bot.set_chat_description(chat_id, new_about)

# استدعاء الدالة للتأكد من تحديث المعلومات في البداية
update_group_info()

# جدولة تحديث المعلومات بانتظام
schedule.every().minute.do(update_group_info)

while True:
    schedule.run_pending()
    time.sleep(1)