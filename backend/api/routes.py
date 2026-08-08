import uuid
from datetime import timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.schemas import InitRequest
from database.db import get_db
from database.models import Persona, Post

router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"]
)


@router.post("/init")
def initialize_agent(
    request: InitRequest,
    db: Session = Depends(get_db)
):
    agent_id = str(uuid.uuid4())

    new_persona = Persona(
        agent_id=agent_id,
        name=request.persona.name,
        domain=request.persona.domain
    )

    db.add(new_persona)
    db.commit()
    db.refresh(new_persona)

    return {
        "agentId": agent_id
    }


@router.get("/feed")
def get_feed(
    agent_id: str = Query(None, alias="agentId"),
    db: Session = Depends(get_db)
):
    query = db.query(Post)

    if agent_id:
        query = query.filter(Post.agent_id == agent_id)

    posts = (
        query
        .order_by(Post.created_at.desc())
        .all()
    )

    result = []

    for post in posts:
        created_at = post.created_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        else:
            created_at = created_at.astimezone(timezone.utc)

        result.append({
            "id": post.id,
            "createdAt": created_at.isoformat().replace("+00:00", "Z"),
            "text": post.text,
            "rationale": post.rationale,
            "sources": [post.sources] if post.sources else []
        })

    return {
        "posts": result
    }
