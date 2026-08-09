from datetime import datetime, timezone

from sqlalchemy.orm import Session

from agent.editor import evaluate_topic
from agent.memory import get_recent_topics, topic_already_published
from database.models import Post
from services.llm_service import generate_post
from services.rss_service import fetch_latest_news


def generate_one_post(
    db: Session,
    agent_id: str,
    persona_name: str,
    persona_domain: str,
    writing_style: str = "analytical",
    interests: str = "AI, technology, security, engineering",
):
    """Research -> editorial gate -> memory -> generation -> persistence.

    One call creates at most one post, which keeps publishing naturally spaced
    by the scheduler rather than dumping the whole research queue at once.
    """

    news = fetch_latest_news(persona_domain)
    if not news:
        return None

    recent_topics = get_recent_topics(db, agent_id, limit=10)

    for article in news:
        topic = article["title"]

        if topic_already_published(db, agent_id, topic):
            continue

        decision = evaluate_topic(topic, article.get("summary", ""), persona_domain)
        if not decision["publish"]:
            continue

        generated = generate_post(
            topic=topic,
            persona_name=persona_name,
            persona_domain=persona_domain,
            recent_topics=recent_topics,
            writing_style=writing_style,
            interests=interests,
            source=article.get("source", "live technology source"),
        )

        now = datetime.now(timezone.utc)
        rationale = (
            f"{decision['reason']} "
            f"Relevance now: the story was discovered from the live "
            f"{article['source']} feed during an autonomous research cycle. "
            f"It was chosen over lower-scoring or previously published "
            f"candidates because it offered a fresher, more actionable "
            f"technology signal."
        )

        post = Post(
            agent_id=agent_id,
            created_at=now,
            text=generated,
            rationale=rationale,
            sources=article["link"],
            topic=topic,
            status="published",
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    return None
