import uuid
from sqlalchemy import Column, String, DateTime, Null
from sqlalchemy.dialects.postgresql import UUID
from core.database import BaseModel


class Domain(BaseModel):
    __tablename__ = "domain"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, nullable=False)
    last_visited = Column(DateTime, nullable=True, default=None)

    def __eq__(self, other):
        return isinstance(other, Domain) and other.url == self.url
