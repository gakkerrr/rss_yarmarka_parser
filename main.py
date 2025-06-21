import feedparser
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

RSS_URLS = ["https://www.prima-tv.ru/news/rss/"]
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
KEYWORDS = ["ярморок","ярмарка","ярмарку","ярмарк","выставк","фестивал", "праздн", "фестивал"]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
    }
    response = requests.post(url, json=payload)
    return response.json()

def check_rss_for_keywords(url):
    feed = feedparser.parse(url)
    found_entries = []  # Список для хранения найденных новостей
    
    for entry in feed.entries:
        title = entry.get("title", "").lower()
        description = entry.get("description", "").lower()
        link = entry.get("link", "")
        
        for keyword in KEYWORDS:
            if keyword in title or keyword in description:
                # Сохраняем найденную новость
                found_entries.append({
                    'keyword': keyword,
                    'title': title,
                    'link': link
                })
                break  # Прерываем проверку других ключевых слов

    if found_entries:
        message = "🔍 Найдены новости с упоминаниями:\n\n"
        
        for i, entry in enumerate(found_entries, 1):
            message += f"{i}. [{entry['keyword']}] {entry['title']}\n{entry['link']}\n\n"
        
        send_telegram_message(message)
    else:
        print("Ничего не найдено")

if __name__ == "__main__":
    while True:
        for url in RSS_URLS:
            check_rss_for_keywords(url)
        time.sleep(60 * 60 * 8)