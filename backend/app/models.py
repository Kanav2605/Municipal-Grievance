from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    Index,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base


class ComplaintRecord(Base):
    __tablename__ = "complaints"

    __table_args__ = (
        CheckConstraint(
            "latitude IS NULL OR latitude BETWEEN -90 AND 90",
            name="check_latitude_range",
        ),
        CheckConstraint(
            "longitude IS NULL OR longitude BETWEEN -180 AND 180",
            name="check_longitude_range",
        ),
        CheckConstraint(
            "(latitude IS NULL) = (longitude IS NULL)",
            name="check_coordinate_pair",
        ),
        Index("ix_complaints_status", "status"),
        Index("ix_complaints_category", "category"),
    )

    complaint_id: Mapped[str] = mapped_column(
        String(40), primary_key=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    address_text: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )
    image_reference: Mapped[str | None] = mapped_column(
        String(1000), nullable=True
    )

    language: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    department: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    category: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    urgency: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="submitted"
    )
    master_incident_id: Mapped[str | None] = mapped_column(
        String(40), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
