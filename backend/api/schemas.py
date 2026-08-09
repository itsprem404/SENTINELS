from pydantic import BaseModel, Field


class PersonaRequest(BaseModel):
    """Public initialization contract.

    The hackathon evaluator only sends name + domain. Role and description are
    optional so the API remains compatible with the published contract.
    """

    name: str = Field(min_length=1, max_length=80)
    domain: str = Field(min_length=1, max_length=120)
    role: str | None = Field(default=None, max_length=120)
    description: str | None = Field(default=None, max_length=500)


class InitRequest(BaseModel):
    persona: PersonaRequest
