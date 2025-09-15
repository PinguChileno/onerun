import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Text,
    func,
)

from src.db.session import Base


class Verification(Base):
    __tablename__ = "verification"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    expires_at = Column(DateTime, nullable=False)
    identifier = Column(Text, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    value = Column(Text, nullable=False)
