from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Boolean

from sqlalchemy.orm import relationship

from datetime import datetime, timezone

from database.connection import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    provider = Column(
        String,
        nullable=False
    )

    encrypted_key = Column(
        String,
        nullable=False
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    last_used_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    project = relationship("Project")