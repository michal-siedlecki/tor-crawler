import uuid

from pydantic import BaseModel, Field


class DomainSchema(BaseModel):
    id: uuid.UUID
    url: str = Field(None, title="Url for the domain")

    class Config:
        orm_mode = True
