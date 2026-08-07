from pydantic import BaseModel


class PersonaRequest(BaseModel):
    name: str
    domain: str


class InitRequest(BaseModel):
    persona: PersonaRequest
