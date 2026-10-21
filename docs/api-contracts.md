# Municipal Grievance - API Contracts

Version: 1.0
Base URL (local development): http://localhost:8000

## 1. Health Check

### GET /health

Purpose: Check whether the backend is running.

Success response (200):

{
  "status": "ok"
}

## 2. Submit a Complaint

### POST /api/v1/complaints

Purpose: Submit a new civic complaint.

Example request:

{
  "description": "Gali mein paani bhar gaya hai",
  "latitude": 28.4595,
  "longitude": 77.0266,
  "address_text": "Near local market",
  "image_reference": null
}

Expected response: 201 Created

The backend generates complaint_id, status, and created_at.

## 3. Retrieve a Complaint

### GET /api/v1/complaints/{complaint_id}

Purpose: Retrieve a complaint by its unique ID.

Expected responses:
- 200: Complaint found
- 404: Complaint not found

## 4. List Complaints

### GET /api/v1/complaints

Purpose: Retrieve complaints for the officer dashboard.

Initial optional query parameters:
- status
- category
- department
- ward_id

Expected response: 200 OK with a list of complaint records.

## 5. Classify a Complaint

### POST /api/v1/ai/classify

Purpose: Obtain structured complaint classification from the NLP module.

Example request:

{
  "description": "Street light teen din se band hai"
}

Expected response fields:
- department
- category
- urgency
- language
- address_text

## 6. Verify an Image

### POST /api/v1/ai/verify-image

Purpose: Check whether an uploaded image supports the reported civic issue.

Expected response fields:
- detected_category
- confidence_score
- verification_status

Image upload and storage details will be finalized during backend implementation.

## 7. Find Duplicate Complaints

### POST /api/v1/ai/deduplicate

Purpose: Compare a complaint against nearby active incidents.

Expected response fields:
- is_duplicate
- master_incident_id
- similarity_score
- distance_meters

## 8. Predict Maintenance Risk

### GET /api/v1/maintenance/risk/{ward_id}

Purpose: Retrieve the predictive maintenance risk assessment for a ward.

Expected response fields:
- ward_id
- risk_score
- risk_level
- prediction_timestamp

## 9. General Rules

- Use JSON for request and response bodies unless an endpoint requires file upload.
- Use ISO 8601 timestamps.
- Return appropriate HTTP status codes.
- Validate all incoming data on the backend.
- Never expose API keys or private citizen information in error messages.
- These are initial contracts; request schemas, authentication,
  pagination, error formats, and production security will be finalized
  during implementation.
