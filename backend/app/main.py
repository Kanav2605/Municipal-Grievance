from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, ConfigDict


app = FastAPI(
    title="Municipal Grievance API",
    description="Backend API for CivicSense AI",
    version="0.1.0",
)


Category = Literal[
    "roads",
    "water_supply",
    "sewage",
    "waterlogging",
    "sanitation",
    "streetlight",
    "fallen_tree",
    "encroachment",
    "other",
]

Urgency = Literal["low", "medium", "high", "critical"]

ComplaintStatus = Literal[
    "submitted",
    "assigned",
    "in_progress",
    "resolved",
    "rejected",
]


class ComplaintCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    description: str = Field(min_length=1, max_length=5000)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    address_text: str | None = Field(default=None, max_length=500)
    image_reference: str | None = Field(default=None, max_length=1000)


class Complaint(ComplaintCreate):
    complaint_id: str
    language: str | None = None
    department: str | None = None
    category: Category | None = None
    urgency: Urgency | None = None
    status: ComplaintStatus = "submitted"
    master_incident_id: str | None = None
    created_at: datetime


# Temporary storage for local development.
# Data will be lost when the server restarts.
complaints: dict[str, Complaint] = {}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/api/v1/complaints",
    response_model=Complaint,
    status_code=status.HTTP_201_CREATED,
)
def create_complaint(payload: ComplaintCreate):
    if not payload.description.strip():
        raise HTTPException(
            status_code=422,
            detail="Complaint description cannot be empty.",
        )

    if (payload.latitude is None) != (payload.longitude is None):
        raise HTTPException(
            status_code=422,
            detail="Provide both latitude and longitude, or neither.",
        )

    complaint_id = f"CMP-{uuid4().hex[:12].upper()}"

    complaint = Complaint(
        **payload.model_dump(),
        complaint_id=complaint_id,
        created_at=datetime.now(timezone.utc),
    )

    complaints[complaint_id] = complaint
    return complaint


@app.get("/api/v1/complaints")
def list_complaints(
    complaint_status: ComplaintStatus | None = Query(
        default=None, alias="status"
    ),
    category: Category | None = None,
    limit: int = Query(default=50, ge=1, le=100),
):
    results = list(complaints.values())

    if complaint_status:
        results = [c for c in results if c.status == complaint_status]

    if category:
        results = [c for c in results if c.category == category]

    results.sort(key=lambda c: c.created_at, reverse=True)

    return {
        "items": results[:limit],
        "total": len(results),
    }


@app.get("/api/v1/complaints/{complaint_id}", response_model=Complaint)
def get_complaint(complaint_id: str):
    complaint = complaints.get(complaint_id)

    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found.",
        )

    return complaint
