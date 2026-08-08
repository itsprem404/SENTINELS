from database.db import SessionLocal
from database.models import Post
from sqlalchemy import func


db = SessionLocal()

duplicates = (
    db.query(Post.topic, func.count(Post.id))
    .filter(Post.topic.isnot(None))
    .group_by(Post.topic)
    .having(func.count(Post.id) > 1)
    .all()
)

for topic, count in duplicates:
    posts = (
        db.query(Post)
        .filter(Post.topic == topic)
        .order_by(Post.id.desc())
        .all()
    )

    print("\nTOPIC:", topic)
    print("TOTAL:", count)

    for post in posts:
        print(
            f"  ID={post.id} | Agent={post.agent_id} | "
            f"Created={post.created_at}"
        )

db.close()
