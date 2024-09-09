import requests
import pandas as pd
from datetime import datetime, timedelta
from googletrans import Translator

API_KEY = 'dq5Aq34ntTzFkzZN0teU3KtQwFZ22ez4'
BASE_URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

def get_articles(query, begin_date, end_date, page=0):
    params = {
        'q': query,
        'begin_date': begin_date,
        'end_date': end_date,
        'api-key': API_KEY,
        'page': page
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'错误：{response.status_code}')
        return None

def fetch_all_articles(query, begin_date, end_date):
    all_articles = []
    page = 0
    while True:
        data = get_articles(query, begin_date, end_date, page)
        if data and data['response']['docs']:
            all_articles.extend(data['response']['docs'])
            page += 1
        else:
            break
    return all_articles

def translate_text(text, dest_language='zh-cn'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        print(f'翻译错误: {e}')
        return text

def parse_articles(articles):
    article_list = []
    for article in articles:
        article_info = {
            'headline': translate_text(article['headline']['main']) if 'headline' in article else 'N/A',
            'pub_date': article['pub_date'] if 'pub_date' in article else 'N/A',
            'web_url': article['web_url'] if 'web_url' in article else 'N/A',
            'snippet': translate_text(article['snippet']) if 'snippet' in article else 'N/A',
            'lead_paragraph': translate_text(article['lead_paragraph']) if 'lead_paragraph' in article else 'N/A',
            'source': article['source'] if 'source' in article else 'N/A'
        }
        article_list.append(article_info)
    return pd.DataFrame(article_list)

query = "headline"
end_date = datetime.now().strftime("%Y%m%d")
ten_days_ago = datetime.now() - timedelta(days=7)
begin_date = ten_days_ago.strftime("%Y%m%d")

all_articles = fetch_all_articles(query, begin_date, end_date)

if all_articles:
    articles_df = parse_articles(all_articles)
    articles_df.to_csv('nyt_headlines_last_week_zh.csv', index=False)
    print('头条新闻已翻译并保存到 nyt_headlines_last_week_zh.csv')
else:
    print('未能获取头条新闻。')
