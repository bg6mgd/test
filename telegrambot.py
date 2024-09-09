


import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from crawler.newsap1i import NewsApiClient
# 替换成你的 Telegram 机器人 Token 和 NewsAPI 密钥
TELEGRAM_TOKEN = '7350194340:AAEb8C6yZUV7OUKD-au2SF8C2yDZc8AHYzA'
NEWS_API_KEY = 'c0f887c82d2649599b850818c99fee5f'


# 初始化 NewsApiClient
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('欢迎！发送 /news 获取热点新闻。')

def get_news() -> str:
    # 获取最新头条新闻
    top_headlines = newsapi.get_top_headlines(
        country='cn',  # 你可以根据需要调整国家代码
        language='zh'  # 根据需要选择语言
    )
    
    articles = top_headlines.get('articles', [])
    if not articles:
        return "目前没有热点新闻。"
    
    # 获取前5条新闻
    news_list = [f"{i+1}. {article['title']} - {article['source']['name']}" for i, article in enumerate(articles[:5])]
    return '\n'.join(news_list)

def news(update: Update, context: CallbackContext) -> None:
    news = get_news()
    update.message.reply_text(news)

async def main() -> None:
    # 创建 Application 实例
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # 添加命令处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", news))

    # 启动机器人
    await application.initialize()
    await application.start()

    # 使用 asyncio.Event 来保持应用程序运行
    shutdown_event = asyncio.Event()
    try:
        await shutdown_event.wait()
    except asyncio.CancelledError:
        await application.stop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("机器人停止运行。")

