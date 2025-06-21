import feedparser
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

RSS_URLS = ["https://www.prima-tv.ru/news/rss/", "https://newslab.ru/news/all/rss"]
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
KEYWORDS = ["ярморок","ярмарка","ярмарку","ярмарк","выставк","фестивал", "праздн", "фестивал", "концерт"]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
    }
    response = requests.post(url, json=payload)
    return response.json()

def check_rss_for_keywords():

    found_entries = [] 
    
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "").lower()
            description = entry.get("description", "").lower()
            link = entry.get("link", "")
            
            for keyword in KEYWORDS:
                if keyword in title or keyword in description:
                    found_entries.append({
                        'keyword': keyword,
                        'title': title,
                        'link': link
                    })
                    break 

    if found_entries:
        message = "🔍 Найдены новости с упоминаниями:\n\n"
        
        for i, entry in enumerate(found_entries, 1):
            message += f"{i}. [{entry['keyword']}] {entry['title']}\n{entry['link']}\n\n"
        
        send_telegram_message(message)
    else:
        print("Ничего не найдено")

if __name__ == "__main__":
    while True:
        check_rss_for_keywords()
        time.sleep(60 * 60 * 8)