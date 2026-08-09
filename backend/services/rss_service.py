import logging
from typing import Any

import feedparser

from agent.editor import evaluate_topic

logger = logging.getLogger(__name__)

# Mix first-party company feeds with independent technology feeds. The agent
# discovers candidates live on every cycle; it does not rely on a fixed post list.
RSS_FEEDS = [
    ("OpenAI News", "https://openai.com/news/rss.xml"),
    ("Hugging Face Blog", "https://huggingface.co/blog/feed.xml"),
    ("Anthropic News", "https://www.anthropic.com/news/rss.xml"),
    ("Google AI Blog", "https://blog.google/technology/ai/rss/"),
    ("Microsoft Research", "https://www.microsoft.com/en-us/research/feed/"),
    ("AWS Machine Learning Blog", "https://aws.amazon.com/blogs/machine-learning/feed/"),
    ("GitHub Blog", "https://github.blog/feed/"),
]


def fetch_latest_news(domain: str = "AI and Technology", per_feed: int = 10) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen_links: set[str] = set()

    for source_name, url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            if getattr(feed, "bozo", False) and not feed.entries:
                logger.warning("RSS feed unavailable: %s", url)
                continue

            for entry in feed.entries[:per_feed]:
                title = str(getattr(entry, "title", "")).strip()
                link = str(getattr(entry, "link", "")).strip()
                summary = str(getattr(entry, "summary", "")).strip()

                if not title or not link or link in seen_links:
                    continue

                decision = evaluate_topic(title, summary, domain)
                if decision["publish"]:
                    seen_links.add(link)
                    candidates.append({
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "source": source_name,
                        "reason": decision["reason"],
                        "score": decision["score"],
                    })
        except Exception as exc:
            logger.warning("Could not read %s: %s", url, exc)

    # Highest editorial score first; the publisher still enforces memory and
    # publishes at most one item per autonomous cycle.
    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates
