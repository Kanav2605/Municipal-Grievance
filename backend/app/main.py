from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database import Base, SessionLocal, engine
from backend.app.models import ComplaintRecord


Category = Literal[
    "roads", "water_supply", "sewage", "waterlogging",
    "sanitation", "streetlight", "fallen_tree",
    "encroachment", "other",
]
Urgency = Literal["low", "medium", "high", "critical"]
ComplaintStatus = Literal[
    "submitted", "assigned", "in_progress", "resolved", "rejected"
]


class ComplaintCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    description: str = Field(min_length=1, max_length=5000)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    address_text: str | None = Field(default=None, max_length=500)
    image_reference: str | None = Field(default=None, max_length=1000)


class Complaint(BaseModel):
    complaint_id: str
    description: str
    latitude: float | None
    longitude: float | None
    address_text: str | None
    image_reference: str | None
    language: str | None
    department: str | None
    category: str | None
    urgency: str | None
    status: str
    master_incident_id: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Municipal Grievance API",
    description="Backend API for CivicSense AI",
    version="0.2.0",
    lifespan=lifespan,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    from sqlalchemy import text

    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


@app.post(
    "/api/v1/complaints",
    response_model=Complaint,
    status_code=status.HTTP_201_CREATED,
)
def create_complaint(
    payload: ComplaintCreate,
    db: Session = Depends(get_db),
):
    if not payload.description.strip():
        raise HTTPException(422, "Complaint description cannot be empty.")

    if (payload.latitude is None) != (payload.longitude is None):
        raise HTTPException(
            422, "Provide both latitude and longitude, or neither."
        )

    record = ComplaintRecord(
        **payload.model_dump(),
        complaint_id=f"CMP-{uuid4().hex[:12].upper()}",
        created_at=datetime.now(timezone.utc),
        status="submitted",
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/api/v1/complaints")
def list_complaints(
    complaint_status: ComplaintStatus | None = Query(
        default=None, alias="status"
    ),
    category: Category | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = select(ComplaintRecord)

    if complaint_status:
        query = query.where(ComplaintRecord.status == complaint_status)

    if category:
        query = query.where(ComplaintRecord.category == category)

    query = query.order_by(ComplaintRecord.created_at.desc())
    records = db.scalars(query.limit(limit)).all()

    return {
        "items": [Complaint.model_validate(r) for r in records],
        "total": len(records),
    }


@app.get(
    "/api/v1/complaints/{complaint_id}",
    response_model=Complaint,
)
def get_complaint(
    complaint_id: str,
    db: Session = Depends(get_db),
):
    record = db.get(ComplaintRecord, complaint_id)

    if record is None:
        raise HTTPException(404, "Complaint not found.")

    return record
