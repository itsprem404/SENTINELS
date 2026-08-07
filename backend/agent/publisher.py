from sqlalchemy.orm import Session

from database.models import Post
from services.rss_service import fetch_latest_news
from services.llm_service import generate_post
from agent.memory import topic_already_published


def generate_one_post(
    db: Session,
    agent_id: str,
    persona_name: str,
    persona_domain: str
):
    """
    Generate ONE new post and save it to the database.
    """

    news = fetch_latest_news()

    if not news:
        return None

    for article in news:

        topic = article["title"]

        # Check memory before generating
        if topic_already_published(
            db=db,
            agent_id=agent_id,
            topic=topic
        ):
            continue

        # Generate post
        generated_post = generate_post(
            topic=topic,
            persona_name=persona_name,
            persona_domain=persona_domain
        )

        # Save post
        post = Post(
            agent_id=agent_id,
            text=generated_post,
            rationale=article["reason"],
            sources=article["link"],
            topic=topic,
            status="published"
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        return post

    # All available topics were already published
    return None