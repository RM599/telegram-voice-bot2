# Telegram Translation & Voice Bot

این یک بات تلگرام است که متن کاربر را به زبان‌های مختلف ترجمه می‌کند و خروجی را به صورت **متن یا وویس** (صوتی) ارسال می‌کند.

## ✨ ویژگی‌ها
- دریافت متن از کاربر
- انتخاب نوع خروجی: متن یا وویس
- ترجمه به زبان‌های:
  - 🇺🇸 انگلیسی (`en`)
  - 🇫🇷 فرانسوی (`fr`)
  - 🇩🇪 آلمانی (`de`)
  - 🇮🇹 ایتالیایی (`it`)
  - 🇪🇸 اسپانیایی (`es`)
  - 🇸🇦 عربی (`ar`)
- تولید فایل صوتی با استفاده از `gTTS` (Google Text-to-Speech)
- پشتیبانی از چند کاربر به صورت همزمان

## 🛠 تکنولوژی‌ها
- Python 3.x
- [python-telegram-bot](https://python-telegram-bot.org)
- [deep-translator](https://pypi.org/project/deep-translator/)
- [gTTS](https://pypi.org/project/gTTS/)

## 🚀 اجرای پروژه

### 1. کلون کردن مخزن
```bash
git clone https://github.com/YourUsername/telegram-voice-bot.git
cd telegram-voice-bot
