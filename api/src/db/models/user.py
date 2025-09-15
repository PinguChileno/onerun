import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.db.session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    ban_expires = Column(DateTime, nullable=True)
    ban_reason = Column(Text, nullable=True)
    banned = Column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    email = Column(Text, nullable=True, unique=True, index=True)
    email_verified = Column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    image = Column(Text, nullable=True)
    metadata_ = Column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'"),
    )
    name = Column(Text, nullable=True, index=True)
    role = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    accounts = relationship("Account", back_populates="user")
    sessions = relationship("Session", back_populates="user")
