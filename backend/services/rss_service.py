import feedparser

RSS_FEEDS = [
    "https://openai.com/news/rss.xml",
    "https://huggingface.co/blog/feed.xml",
    "https://www.anthropic.com/news/rss.xml"
]


def fetch_latest_news():
    news = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            news.append({
                "title": entry.title,
                "link": entry.link
            })

    return news