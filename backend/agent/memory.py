from sqlalchemy.orm import Session

from database.models import Post


def topic_already_published(
    db: Session,
    agent_id: str,
    topic: str
) -> bool:
    """
    Check whether this agent has already published
    a post about the given topic.
    """

    existing_post = (
        db.query(Post)
        .filter(
            Post.agent_id == agent_id,
            Post.topic == topic
        )
        .first()
    )

    return existing_post is not None
