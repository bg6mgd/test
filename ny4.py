import requests
import pandas as pd
from datetime import datetime, timedelta
import time 

# 你的 API 密钥
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
            time.sleep(1)
        else:
            break
    return all_articles

def parse_articles(articles):
    article_list = []
    for article in articles:
        article_info = {
            'headline': article['headline']['main'] if 'headline' in article else 'N/A',
            'pub_date': article['pub_date'] if 'pub_date' in article else 'N/A',
            'web_url': article['web_url'] if 'web_url' in article else 'N/A',
            'snippet': article['snippet'] if 'snippet' in article else 'N/A',
            'lead_paragraph': article['lead_paragraph'] if 'lead_paragraph' in article else 'N/A',
            'source': article['source'] if 'source' in article else 'N/A'
        }
        article_list.append(article_info)
    return pd.DataFrame(article_list)

def main():
    # 设定查询参数
    tech_query = "technology"
    politics_query = "politics"

    end_date = datetime.now().strftime("%Y%m%d")
    ten_days_ago = datetime.now() - timedelta(days=7)
    begin_date = ten_days_ago.strftime("%Y%m%d")

    # 获取科技新闻
    tech_articles = fetch_all_articles(tech_query, begin_date, end_date)
    if tech_articles:
        tech_articles_df = parse_articles(tech_articles)
        tech_articles_df.to_csv('nyt_tech_articles_last_week.csv', index=False)
        print('科技新闻已保存到 nyt_tech_articles_last_week.csv')
    else:
        print('未能获取科技新闻。')

    # 获取政治新闻
    politics_articles = fetch_all_articles(politics_query, begin_date, end_date)
    if politics_articles:
        politics_articles_df = parse_articles(politics_articles)
        politics_articles_df.to_csv('nyt_politics_articles_last_week.csv', index=False)
        print('政治新闻已保存到 nyt_politics_articles_last_week.csv')
    else:
        print('未能获取政治新闻。')

if __name__ == "__main__":
    main()
