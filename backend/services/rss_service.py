import feedparser
from agent.editor import evaluate_topic

RSS_FEEDS = [
    "https://openai.com/news/rss.xml",
    "https://huggingface.co/blog/feed.xml",
    "https://www.anthropic.com/news/rss.xml"
]


def fetch_latest_news():
    approved_news = []

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:

            title = entry.title
            summary = getattr(entry, "summary", "")

            decision = evaluate_topic(title, summary)

            if decision["publish"]:
                approved_news.append({
                    "title": title,
                    "link": entry.link,
                    "reason": decision["reason"]
                })

    return approved_news