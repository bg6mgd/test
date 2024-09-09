import requests
import pandas as pd
import json
from datetime import datetime,timedelta
API_KEY = 'dq5Aq34ntTzFkzZN0teU3KtQwFZ22ez4'
BASE_URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

def get_articles(query,begin_date,end_date):
    params = {
        'q' : query,
        'begin_date' : begin_date,
        'end_date' : end_date,
        'api-key' : API_KEY
    }
    response = requests.get(BASE_URL,params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error:{response.status_code}')
        return None
    
def parse_articles(data):
    articles =data['response']['docs']
    article_list=[]
    for article in articles:
        article_info ={
            'headline': article['headline']['main'],
            'pub_date': article['pub_date'],
            'web url': article['web_url'],
            'snippet': article['snippet'],
            'lead_paragraph': article['lead_paragraph'],
            'source': article['source']
        }
        article_list.append(article_info)
    return pd.DataFrame(article_list)
# 设定查询参数
query ="climate change"


end_date =datetime.now().strftime("%Y%m%d")
ten_days_ago = datetime.now() - timedelta(days=10)
begin_date = ten_days_ago.strftime("%Y%m%d")
print(end_date)
#获取文章数据
data = get_articles(query,begin_date, end_date)
# with open("example.txt", "w") as file:
#     json.dump(data,file,ensure_ascii=False,indent=4)
#     file.close()
if data:
    articles_df = parse_articles(data)
    articles_df.to_csv('nyt_articles.csv',index=False)
    print('articles saved to nyt_ticles.csv')
else:
    print('Failed to retrieve articles.')


