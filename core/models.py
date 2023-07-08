import uuid
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from core.database import BaseModel


class Domain(BaseModel):
    __tablename__ = "domain"

    id: uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url: str = Column(String, nullable=False)
    last_visited: int = Column(Integer, nullable=True, default=None)
    is_thread: bool = Column(Boolean, nullable=True, default=None)

    def __eq__(self, other):
        return isinstance(other, Domain) and other.url == self.url
