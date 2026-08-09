import uuid
from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from agent.editor import TECH_KEYWORDS, REJECT_KEYWORDS
from api.schemas import InitRequest
from database.db import get_db
from database.models import Persona, Post
from scheduler.scheduler import trigger_cycle

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/init")
def initialize_agent(request: InitRequest, db: Session = Depends(get_db)):

    agent_id = str(uuid.uuid4())
    role = request.persona.role or f"{request.persona.domain} Intelligence Analyst"
    description = (
        request.persona.description
        or f"An autonomous {request.persona.domain} observer that researches live "
           "technology developments, filters them editorially, remembers its "
           "coverage, and publishes measured analysis over time."
    )

    persona = Persona(
        agent_id=agent_id,
        name=request.persona.name.strip(),
        domain=request.persona.domain.strip(),
        role=role.strip(),
        description=description.strip(),
        writing_style="analytical, skeptical, concise, builder-oriented",
        interests=f"{request.persona.domain}, AI, technology, security, engineering",
    )
    db.add(persona)
    db.commit()

    trigger_cycle()

    return {"agentId": agent_id}


@router.get("/profile")
def get_profile(agent_id: str = Query(..., alias="agentId"), db: Session = Depends(get_db)):
    persona = db.query(Persona).filter(Persona.agent_id == agent_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Agent not found")

    return {
        "name": persona.name,
        "domain": persona.domain,
        "role": persona.role,
        "description": persona.description,
        "writingStyle": persona.writing_style,
        "interests": persona.interests,
    }


@router.get("/feed")
def get_feed(agent_id: str = Query(..., alias="agentId"), db: Session = Depends(get_db)):
    if not db.query(Persona).filter(Persona.agent_id == agent_id).first():
        raise HTTPException(status_code=404, detail="Agent not found")

    posts = (
        db.query(Post)
        .filter(Post.agent_id == agent_id, Post.status == "published")
        .order_by(Post.created_at.desc(), Post.id.desc())
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
            "id": f"p{post.id}",
            "createdAt": created_at.isoformat().replace("+00:00", "Z"),
            "text": post.text,
            "rationale": post.rationale,
            "sources": [post.sources] if post.sources else [],
        })

    return {"posts": result}


@router.get("/standards")
def editorial_standards():
    return {
        "selectionSignals": sorted(TECH_KEYWORDS),
        "rejectionSignals": sorted(REJECT_KEYWORDS),
        "memory": "Exact and high-overlap topic checks against the agent's previous posts.",
        "cadence": "One post per autonomous 15-minute research cycle, with an 8-second first cycle.",
    }
