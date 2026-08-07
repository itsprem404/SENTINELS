import uuid

from fastapi import APIRouter, Depends
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
def get_feed(db: Session = Depends(get_db)):

    posts = db.query(Post).order_by(Post.created_at.desc()).all()

    response = []

    for post in posts:
        response.append({
            "id": str(post.id),
            "createdAt": post.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "text": post.text,
            "rationale": post.rationale,
            "sources": post.sources.split(",") if post.sources else []
        })

    return {
        "posts": response
    }