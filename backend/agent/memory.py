from sqlalchemy.orm import Session

from database.models import Post


def topic_already_published(
    db: Session,
    agent_id: str,
    topic: str
) -> bool:

    existing_post = (
        db.query(Post)
        .filter(
            Post.agent_id == agent_id,
            Post.topic == topic
        )
        .first()
    )

    return existing_post is not None


def get_recent_topics(
    db: Session,
    agent_id: str,
    limit: int = 10
):
    """
    Return the most recently published topics
    for a specific agent.
    """

    posts = (
        db.query(Post)
        .filter(Post.agent_id == agent_id)
        .order_by(Post.created_at.desc())
        .limit(limit)
        .all()
    )

    return [post.topic for post in posts if post.topic]