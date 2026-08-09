import logging
import threading

from agent.publisher import generate_one_post
from database.db import SessionLocal
from database.models import Persona

logger = logging.getLogger(__name__)

_scheduler_started = False
_stop_event = threading.Event()
_wake_event = threading.Event()

PUBLISH_INTERVAL_SECONDS = 15 * 60
INITIAL_DELAY_SECONDS = 8


def run_agent_cycle():
    db = SessionLocal()
    try:
        personas = db.query(Persona).all()
        for persona in personas:
            post = generate_one_post(
                db=db,
                agent_id=persona.agent_id,
                persona_name=persona.name,
                persona_domain=persona.domain,
                writing_style=persona.writing_style or "analytical",
                interests=persona.interests or "AI, technology, security, engineering",
            )
            if post:
                logger.info("Published autonomous post %s for %s", post.id, persona.name)
    except Exception:
        logger.exception("Autonomous research/publishing cycle failed")
    finally:
        db.close()


def trigger_cycle():
    """Wake the already-running autonomous loop after initialization."""
    _wake_event.set()


def start_scheduler():
    global _scheduler_started
    if _scheduler_started:
        return

    _scheduler_started = True

    def loop():
        _wake_event.wait(INITIAL_DELAY_SECONDS)
        _wake_event.clear()

        if not _stop_event.is_set():
            run_agent_cycle()

        while not _stop_event.is_set():
            _wake_event.wait(PUBLISH_INTERVAL_SECONDS)
            _wake_event.clear()
            if _stop_event.is_set():
                break
            run_agent_cycle()


    thread = threading.Thread(
        target=loop,
        name="sentinels-autonomous-agent",
        daemon=True,
    )
    thread.start()
    logger.info("Autonomous scheduler started (15-minute cadence).")


def stop_scheduler():
    _stop_event.set()
    _wake_event.set()
