from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database.db import Base


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)

    writing_style = Column(String, default="Professional")
    interests = Column(Text, default="AI, Technology")
    created_at = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

    agent_id = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    text = Column(Text, nullable=False)

    rationale = Column(Text, nullable=False)

    sources = Column(Text, nullable=False)

    topic = Column(String)

    status = Column(String, default="published")