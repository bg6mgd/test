from newsapi import NewsApiClient

# 初始化 NewsApiClient
newsapi = NewsApiClient(api_key='c0f887c82d2649599b850818c99fee5f')

def get_news() -> str:
    # 获取根据国家代码的头条新闻
    top_headlines = newsapi.get_top_headlines(
        country='cn',  # 国家代码
        language='zh'  # 语言
    )
    
    articles = top_headlines.get('articles', [])
    if not articles:
        return "目前没有热点新闻。"
    
    # 获取前5条新闻
    news_list = [f"{i+1}. {article['title']} - {article['source']['name']}" for i, article in enumerate(articles[:5])]
    return '\n'.join(news_list)

# 调用 get_news 函数并打印结果
newsaa = get_news()
print(newsaa)
