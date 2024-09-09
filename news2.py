from newsapi import NewsApiClient
from googletrans import Translator
from deep_translator import GoogleTranslator

# 初始化 NewsApiClient
newsapi = NewsApiClient(api_key='c0f887c82d2649599b850818c99fee5f')


def get_news() -> str:
    # 获取根据新闻来源的头条新闻
    top_headlines = newsapi.get_top_headlines(
        sources='bbc-news,the-verge',  # 新闻来源
        language='en'  # 语言
    )
    #print(top_headlines)
    
    articles = top_headlines.get('articles', [])
    if not articles:
        return "目前没有热点新闻。"
    
    # 获取前5条新闻
    news_list = [f"{i+1}. {article['title']} - {article['source']['name']}" for i, article in enumerate(articles[:5])]
    return '\n'.join(news_list)

# 调用 get_news 函数并打印结果



def translate_text(text, dest_language='zh-CN'):
    try:
        translator = GoogleTranslator(target=dest_language)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f'翻译错误: {e}')
        return text

# 测试翻译
newsaa = get_news()
han = translate_text(newsaa)
print(han)
text_to_translate = "Hello, how are you?"
translated_text = translate_text(text_to_translate)
print(translated_text)