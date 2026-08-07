from services.rss_service import fetch_latest_news


def research_topics():
    """
    Fetch and return relevant news topics for the agent.
    """

    news = fetch_latest_news()

    return news