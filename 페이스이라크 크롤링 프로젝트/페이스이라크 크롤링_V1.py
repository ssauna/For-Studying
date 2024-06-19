import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from googletrans import Translator

# 뉴스 사이트 URL
NEWS_URL = 'https://faceiraq.org/articles/%D8%A3%D9%85%D9%86'

# 기사 제목을 수집하는 함수
def fetch_articles():
    try:
        print("Fetching articles...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(NEWS_URL, headers=headers)
        print(f"HTTP response status code: {response.status_code}")
        response.raise_for_status()
        print("HTTP request successful")

        soup = BeautifulSoup(response.content, 'html.parser')
        print("Parsed HTML with BeautifulSoup")

        articles = soup.find_all('div', class_='v-card--link')
        print(f"Number of articles found: {len(articles)}")

        article_data = []

        for index, article in enumerate(articles[:10], start=1):  # 최대 10개 기사 가져오기
            title_tag = article.find('p', class_='article-title')
            
            if title_tag:
                title = title_tag['title'].strip()
                article_data.append((index, title))
                print(f"Found article: {index}. Title: {title}")

        print(f"Articles prepared with {len(article_data)} items")
        return article_data
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []

# GUI를 사용하여 기사 제목을 표시하는 함수
def display_articles(articles):
    root = tk.Tk()
    root.title("기사 목록")
    root.geometry("800x600")

    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    translator = Translator()

    for index, title in articles:
        frame = ttk.Frame(scrollable_frame, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        translated_title = translator.translate(title, src='ar', dest='ko').text
        title_label = ttk.Label(frame, text=f"{index}. {translated_title}", wraplength=700, font=("Arial", 14))
        title_label.pack(side=tk.LEFT, padx=10, pady=10)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    root.mainloop()

# 기사 제목을 수집하는 함수 실행
articles = fetch_articles()

# GUI로 기사 목록 표시
display_articles(articles)
