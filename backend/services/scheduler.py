from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()


def autonomous_job():
    print(f"[{datetime.now()}] Autonomous Agent is running...")


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
