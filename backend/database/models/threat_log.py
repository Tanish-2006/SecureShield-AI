from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime, timezone

from database.connection import Base


class ThreatLog(Base):
    __tablename__ = "threat_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=True
    )

    severity = Column(
        String,
        nullable=False
    )

    threats = Column(
        String,
        nullable=False
    )

    risk_score = Column(
        Integer,
        nullable=False
    )

    action = Column(
        String,
        nullable=False
    )

    prompt = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User")
    project = relationship("Project")