"""
بعد از اتمام ین پروژه
یک ورودی از کاربر دریافت کنیم
از سایت دیوار اگهی های مرتبط را استخراج کنیم
شماره تماس اگهی را در یک فایل اکسل ذخیره کنیم
"""

# نصب نیامندی های پروژه
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# مرحله اول  دریافت ورودی از کاربر
keyword = input("کلمه کلیدی مورد نظر را وارد کنید: ")
search_url = f"https://divar.ir/s/tehran/car?q={keyword}"

# مرحله ۲: راه‌اندازی مرورگر

service = Service("./chromedriver-win64/chromedriver-win64/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # بدون باز شدن پنجره مرورگر
driver = webdriver.Chrome(service=service, options=options)

# مرحله ۳: رفتن به صفحه جستجو

driver.get(search_url)
time.sleep(5)

# مرحله ۴: اسکرول برای لود آگهی‌های بیشتر (اختیاری، فعلاً یک بار فقط)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# مرحله ۵: استخراج لینک‌ها
ads = driver.find_elements(By.CSS_SELECTOR, "a.kt-post-card.kt-post-card--outlined")
ad_links = ["https://divar.ir" + ad.get_attribute("href") for ad in ads if ad.get_attribute("href")]

results = []
# استخراج شماره تماس از هر آگهی
for link in ad_links[:5]:  # فقط ۵ مورد اول برای تست
    driver.get(link)
    time.sleep(3)
    phone = "یافت نشد"

    try:
        # دکمه نمایش شماره
        phone_btn = driver.find_element(By.CSS_SELECTOR, 'div.kt-base-button__text')
        if "شماره" in phone_btn.text:
            phone_btn.click()
            time.sleep(2)
            phone_elem = driver.find_element(By.CSS_SELECTOR, 'a.kt-unexpandable-row__action')
            phone = phone_elem.text
    except (NoSuchElementException, ElementClickInterceptedException):
        pass

    print(f"✅ آگهی بررسی شد: {link} -> شماره: {phone}")
    results.append({
        "لینک آگهی": link,
        "شماره تماس": phone
    })


# ذخیره در اکسل
df = pd.DataFrame(results)
df.to_excel("divar_contacts.xlsx", index=False)

driver.quit()
print("📁 فایل 'divar_contacts.xlsx' ایجاد شد.")