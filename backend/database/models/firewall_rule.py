from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from database.connection import Base


class FirewallRule(Base):
    __tablename__ = "firewall_rules"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        unique=True,
        nullable=False
    )

    risk_threshold = Column(
        Integer,
        default=70,
        nullable=False
    )

    project = relationship("Project")