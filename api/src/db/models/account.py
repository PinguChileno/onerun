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


class Account(Base):
    __tablename__ = "account"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    access_token = Column(Text, nullable=True)
    access_token_expires_at = Column(DateTime, nullable=True)
    account_id = Column(Text, nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    id_token = Column(Text, nullable=True)
    password = Column(Text, nullable=True)
    provider_id = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    refresh_token_expires_at = Column(DateTime, nullable=True)
    scope = Column(Text, nullable=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    user_id = Column(
        Text,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user = relationship("User", back_populates="accounts")
