import uuid

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
    # Generate unique Agent ID
    agent_id = str(uuid.uuid4())

    # Create Persona object
    new_persona = Persona(
        agent_id=agent_id,
        name=request.persona.name,
        domain=request.persona.domain
    )

    # Save to database
    db.add(new_persona)
    db.commit()
    db.refresh(new_persona)

    # Return generated Agent ID
    return {
        "agentId": agent_id
    }


@router.get("/feed")
def get_feed(
    agent_id: str = Query(None, alias="agentId"),
    db: Session = Depends(get_db)
):
    # Start with all posts
    query = db.query(Post)

    # If agent_id is provided, filter posts for that agent
    if agent_id:
        query = query.filter(Post.agent_id == agent_id)

    # Latest posts first
    posts = (
        query
        .order_by(Post.created_at.desc())
        .all()
    )

    result = []

    for post in posts:
        result.append({
            "id": post.id,
            "agentId": post.agent_id,
            "topic": post.topic,
            "createdAt": post.created_at.isoformat().replace("+00:00", "Z"),
            "text": post.text,
            "rationale": post.rationale,
            "sources": post.sources.split(",") if post.sources else [],
            "status": post.status
        })

    return {
        "posts": result,
        "count": len(result)
    }