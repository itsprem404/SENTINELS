import threading
import time

from database.db import SessionLocal
from database.models import Persona
from agent.publisher import generate_one_post


_scheduler_started = False


def run_agent_cycle():
    db = SessionLocal()

    try:
        personas = db.query(Persona).all()

        for persona in personas:
            generate_one_post(
                db=db,
                agent_id=persona.agent_id,
                persona_name=persona.name,
                persona_domain=persona.domain,
                writing_style=persona.writing_style,
                interests=persona.interests
            )

    finally:
        db.close()


def start_scheduler():
    global _scheduler_started

    if _scheduler_started:
        return

    _scheduler_started = True

    def loop():
        while True:
            try:
                run_agent_cycle()
            except Exception as e:
                print(f"Scheduler error: {e}")

            time.sleep(600)

    thread = threading.Thread(
        target=loop,
        daemon=True
    )

    thread.start()

    print("Autonomous scheduler started.")
