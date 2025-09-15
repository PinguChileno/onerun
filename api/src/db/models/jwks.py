import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Text,
    func,
)

from src.db.session import Base


class Jwks(Base):
    __tablename__ = "jwks"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    private_key = Column(Text, nullable=False)
    public_key = Column(Text, nullable=False)
