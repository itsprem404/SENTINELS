from sqlalchemy.orm import Session

from database.models import Post
from services.rss_service import fetch_latest_news
from services.llm_service import generate_post
from agent.memory import (
    topic_already_published,
    get_recent_topics,
)


def normalize_source_url(source: str) -> str:
    """
    Convert Markdown links into a plain URL.
    """

    if not source:
        return ""

    source = source.strip()

    # Handle Markdown:
    # [https://example.com](https://example.com)
    if source.startswith("[") and "](" in source:
        source = source.rsplit("](", 1)[1]

        if source.endswith(")"):
            source = source[:-1]

    return source.strip()


def generate_one_post(
    db: Session,
    agent_id: str,
    persona_name: str,
    persona_domain: str,
    writing_style: str = "Professional",
    interests: str = "AI, Technology",
):
    """
    Generate ONE new post and save it to the database.
    """

    news = fetch_latest_news()

    if not news:
        return None

    recent_topics = get_recent_topics(
        db=db,
        agent_id=agent_id,
        limit=10,
    )

    print("Recent topics:", recent_topics)

    for article in news:

        topic = article["title"]

        # Check memory before generating.
        if topic_already_published(
            db=db,
            agent_id=agent_id,
            topic=topic,
        ):
            continue

        # Generate post using persona + memory.
        generated_post = generate_post(
            topic=topic,
            persona_name=persona_name,
            persona_domain=persona_domain,
            recent_topics=recent_topics,
            writing_style=writing_style,
            interests=interests,
        )

        # Normalize the source BEFORE saving it.
        raw_source = article.get("link", "")
        source_url = normalize_source_url(raw_source)

        print("Raw source:", repr(raw_source))
        print("Normalized source:", repr(source_url))

        # Build publishing rationale.
        rationale = (
            f"{article['reason']} "
            f"The topic is timely because it comes from a current "
            f"AI/Technology source and has direct relevance to the "
            f"persona's domain."
        )

        # Save post.
        post = Post(
            agent_id=agent_id,
            text=generated_post,
            rationale=rationale,
            sources=source_url,
            topic=topic,
            status="published",
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        return post

    # All available topics were already published.
    return None