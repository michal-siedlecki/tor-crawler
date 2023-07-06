import uuid

from pydantic import BaseModel, Field


class DomainSchema(BaseModel):
    id: uuid.UUID
    url: str = Field(None, title="The url")

    class Config:
        orm_mode = True
