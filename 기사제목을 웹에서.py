import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string, jsonify
from googletrans import Translator

# 뉴스 사이트 URL
NEWS_URL = 'https://faceiraq.org/articles/%D8%A3%D9%85%D9%86'

app = Flask(__name__)
last_articles = []

# 기사 제목을 수집하는 함수
def fetch_articles():
    global last_articles
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(NEWS_URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('div', class_='v-card--link')

        article_data = []
        for index, article in enumerate(articles[:10], start=1):  # 최대 10개 기사 가져오기
            title_tag = article.find('p', class_='article-title')
            if title_tag:
                title = title_tag['title'].strip()
                article_data.append((index, title))

        # 새로운 기사 확인
        new_articles = []
        for article in article_data:
            if article not in last_articles:
                new_articles.append(article)

        last_articles = article_data
        return new_articles, article_data
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return [], []

@app.route('/')
def index():
    new_articles, articles = fetch_articles()
    translator = Translator()
    translated_articles = [
        (index, title, translator.translate(title, src='ar', dest='ko').text) 
        for index, title in articles
    ]
    new_translated_articles = [
        (index, title, translator.translate(title, src='ar', dest='ko').text)
        for index, title in new_articles
    ]
    
    html_content = '''
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>페이스이라크 보안관련 기사 자동업데이트 by 정매</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
            }
            h1 {
                color: #333;
            }
            ul {
                list-style-type: none;
            }
            li {
                margin: 15px 0;
            }
            .title {
                font-size: 18px;
            }
            .new-article {
                font-weight: bold;
                color: red;
            }
            .update-info {
                position: absolute;
                top: 10px;
                right: 10px;
                font-size: 14px;
                color: #333;
            }
        </style>
        <script>
            function fetchArticles() {
                fetch('/update')
                    .then(response => response.json())
                    .then(data => {
                        let ul = document.querySelector('ul');
                        ul.innerHTML = '';
                        data.articles.forEach(article => {
                            let li = document.createElement('li');
                            li.classList.add('title');
                            if (article.new) {
                                li.classList.add('new-article');
                                li.innerHTML = article.index + ". " + article.arabic_title + "<br>" + article.korean_title + " (NEW)";
                            } else {
                                li.innerHTML = article.index + ". " + article.arabic_title + "<br>" + article.korean_title;
                            }
                            ul.appendChild(li);
                        });
                        document.querySelector('.update-info').textContent = "5분마다 뉴스 갱신";
                    });
            }

            setInterval(fetchArticles, 300000); // 5분 = 300000 밀리초
            window.onload = fetchArticles;
        </script>
    </head>
    <body>
        <div class="update-info">5분마다 뉴스 갱신</div>
        <h1>페이스이라크 보안관련 기사 자동업데이트 by Armir Jung</h1>
        <ul>
            {% for article in articles %}
                <li class="title{% if article.new %} new-article{% endif %}">{{ article.index }}. {{ article.arabic_title }}<br>{{ article.korean_title }}{% if article.new %} (NEW){% endif %}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(html_content, articles=[
        {
            'index': index,
            'arabic_title': arabic_title,
            'korean_title': korean_title,
            'new': (index, arabic_title, korean_title) in new_translated_articles
        } for index, arabic_title, korean_title in translated_articles
    ])

@app.route('/update')
def update():
    new_articles, articles = fetch_articles()
    translator = Translator()
    translated_articles = [
        (index, title, translator.translate(title, src='ar', dest='ko').text) 
        for index, title in articles
    ]
    new_translated_articles = [
        (index, title, translator.translate(title, src='ar', dest='ko').text)
        for index, title in new_articles
    ]
    return jsonify({
        'articles': [
            {
                'index': index,
                'arabic_title': arabic_title,
                'korean_title': korean_title,
                'new': (index, arabic_title, korean_title) in new_translated_articles
            } for index, arabic_title, korean_title in translated_articles
        ]
    })

if __name__ == '__main__':
    app.run(host='10.20.78.76', port=5000, debug=True)
