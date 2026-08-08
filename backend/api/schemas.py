from pydantic import BaseModel


class PersonaRequest(BaseModel):
    name: str
    domain: str
    role: str
    description: str


class InitRequest(BaseModel):
    persona: PersonaRequest