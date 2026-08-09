from sqlalchemy.orm import Session
from database.models import Post


def topic_already_published(db: Session, agent_id: str, topic: str) -> bool:
    exact = (
        db.query(Post)
        .filter(Post.agent_id == agent_id, Post.topic == topic)
        .first()
    )
    if exact:
        return True

    normalized = " ".join(topic.lower().split())
    words = [w for w in normalized.replace(":", " ").split() if len(w) > 4][:8]
    if len(words) < 3:
        return False

    recent = get_recent_topics(db, agent_id, limit=25)
    for old in recent:
        old_words = set(old.lower().replace(":", " ").split())
        overlap = sum(word in old_words for word in words)
        if overlap >= max(3, int(len(words) * 0.7)):
            return True
    return False


def get_recent_topics(db: Session, agent_id: str, limit: int = 10):
    posts = (
        db.query(Post)
        .filter(Post.agent_id == agent_id)
        .order_by(Post.created_at.desc())
        .limit(limit)
        .all()
    )
    return [post.topic for post in posts if post.topic]
