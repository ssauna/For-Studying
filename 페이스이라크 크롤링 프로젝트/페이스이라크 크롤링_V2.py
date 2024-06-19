import requests
import tkinter as tk
from tkinter import ttk
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import webbrowser
from io import BytesIO
from PIL import Image, ImageTk

# 뉴스 사이트 URL
NEWS_URL = 'https://faceiraq.org/articles/%D8%A3%D9%85%D9%86'

# 기사 제목, 이미지 URL, 원문 링크를 수집하는 함수
def fetch_articles():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')  # SSL 오류 무시
        options.add_argument('--disable-gpu')  # 필요시 GPU 비활성화
        options.add_argument('--disable-dev-shm-usage')  # /dev/shm 사용 비활성화
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(NEWS_URL)

        articles = driver.find_elements(By.CLASS_NAME, 'v-card--link')
        article_data = []

        for index, article in enumerate(articles[:10], start=1):  # 최대 10개 기사 가져오기
            try:
                title_tag = article.find_element(By.CLASS_NAME, 'article-title')
                title = title_tag.get_attribute('title').strip()
                
                image_tag = article.find_element(By.CSS_SELECTOR, 'div.card__image img')
                image_url = image_tag.get_attribute('src')
                
                link = article.get_attribute('href')
                
                article_data.append((index, title, image_url, link))
                print(f"Found article: {index}. Title: {title}, Image URL: {image_url}, Link: {link}")
            except Exception as e:
                print(f"Error processing article {index}: {e}")

        driver.quit()
        return article_data
    except Exception as e:
        print(f"Error fetching articles: {e}")
        if 'driver' in locals():
            driver.quit()  # 예외 발생 시 드라이버 종료
        return []

# GUI를 사용하여 기사 제목, 이미지, 링크를 표시하는 함수
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

    for index, title, image_url, link in articles:
        frame = ttk.Frame(scrollable_frame, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        translated_title = translator.translate(title, src='ar', dest='ko').text

        title_label = ttk.Label(frame, text=f"{index}. {translated_title}", wraplength=500, font=("Arial", 14))
        title_label.pack(side=tk.LEFT, padx=10, pady=10)

        # 이미지 다운로드 및 표시
        try:
            image_response = requests.get(image_url, stream=True, timeout=5)
            image_response.raise_for_status()
            image_data = image_response.content
            image = Image.open(BytesIO(image_data))
            image = image.resize((100, 100), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {image_url}: {e}")
            photo = None

        if photo:
            image_label = ttk.Label(frame, image=photo)
            image_label.image = photo
            image_label.pack(side=tk.LEFT, padx=10, pady=10)

        link_label = ttk.Label(frame, text=link, font=("Arial", 10), foreground="blue", cursor="hand2")
        link_label.pack(side=tk.LEFT, padx=10, pady=10)
        link_label.bind("<Button-1>", lambda e, url=link: webbrowser.open_new(url))

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    root.mainloop()

# 기사 제목, 이미지 URL, 원문 링크를 수집하는 함수 실행
articles = fetch_articles()

# GUI로 기사 목록 표시
display_articles(articles)
