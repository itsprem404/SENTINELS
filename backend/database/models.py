from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database.db import Base


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)

    # Unique agent ID returned after initialization
    agent_id = Column(String, unique=True, nullable=False)

    # Persona information
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)

    # Optional fields for future use
    writing_style = Column(String, default="Professional")
    interests = Column(Text, default="AI, Technology")
    created_at = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    # Which agent created this post
    agent_id = Column(String, nullable=False)

    # Time of publishing
    created_at = Column(DateTime, default=datetime.utcnow)

    # Generated content
    text = Column(Text, nullable=False)

    # Why this topic was selected
    rationale = Column(Text, nullable=False)

    # Store sources as a comma-separated string for now
    # (Later we can convert this to JSON if needed)
    sources = Column(Text, nullable=False)

    # Topic title
    topic = Column(String)

    # Future use
    status = Column(String, default="published")
