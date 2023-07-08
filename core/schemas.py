import uuid

from pydantic import BaseModel, Field


class DomainSchema(BaseModel):
    id: uuid.UUID
    url: str = Field(None, title="Url for the domain")
    last_visited: int = Field(None)
    is_thread: bool = Field(None)

    class Config:
        orm_mode = True
