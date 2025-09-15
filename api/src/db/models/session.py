import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from src.db.session import Base


class Session(Base):
    __tablename__ = "session"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    expires_at = Column(DateTime, nullable=False)
    impersonated_by = Column(Text, nullable=True)
    ip_address = Column(Text, nullable=True)
    token = Column(Text, nullable=False, unique=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    user_agent = Column(Text, nullable=True)
    user_id = Column(
        Text,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship("User", back_populates="sessions")
