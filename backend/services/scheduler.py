from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from services.rss_service import fetch_latest_news

scheduler = BackgroundScheduler()


def autonomous_job():
    print(f"\n===== {datetime.now()} =====")

    news = fetch_latest_news()

    if not news:
        print("No news found.")
        return

    print("Latest AI News:\n")

    for article in news[:5]:
        print(f"• {article['title']}")
        print(article['link'])
        print()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            autonomous_job,
            "interval",
            minutes=1,
            id="autonomous_job",
            replace_existing=True,
        )
        scheduler.start()
        print("Scheduler Started!")
