# Municipal Grievance - Data Dictionary

Version: 1.0

## 1. Purpose

This document defines the shared complaint data structure used by
the citizen portal, backend, AI modules, and officer dashboard.

## 2. Complaint Record

| Field | Type | Required | Description |
|---|---|---|---|
| complaint_id | string | Yes | Unique ID assigned by the backend |
| description | string | Yes | Original complaint text |
| language | string | No | Detected language, e.g. Hindi, English, Hinglish |
| latitude | number | No | Geographic latitude |
| longitude | number | No | Geographic longitude |
| address_text | string | No | Address or landmark provided by the citizen |
| department | string | No | Responsible municipal department |
| category | string | No | Normalized civic issue category |
| urgency | string | No | low, medium, high, critical |
| status | string | Yes | submitted, assigned, in_progress, resolved, rejected |
| image_reference | string | No | Reference to an uploaded image; not the image itself |
| master_incident_id | string | No | Master incident ID if the complaint is a duplicate |
| created_at | string | Yes | Creation timestamp in ISO 8601 format |

## 3. Supported Initial Categories

- roads
- water_supply
- sewage
- waterlogging
- sanitation
- streetlight
- fallen_tree
- encroachment
- other

## 4. Data Rules

- complaint_id must be unique.
- description must not be empty.
- latitude must be between -90 and 90 when provided.
- longitude must be between -180 and 180 when provided.
- urgency must be low, medium, high, or critical when provided.
- status must use one of the defined status values.
- Coordinates may be absent when a citizen does not share a location.
- The backend assigns complaint_id, status, and created_at.
- Do not store API keys, passwords, or unnecessary personal data in complaint records.

## 5. AI Module Outputs

### NLP
- department
- category
- urgency
- language
- address_text

### Computer Vision
- detected_category
- confidence_score
- verification_status

### Deduplication
- is_duplicate
- master_incident_id
- similarity_score
- distance_meters

### Predictive Maintenance
- ward_id
- risk_score
- risk_level
- prediction_timestamp

## 6. Important Integration Note

This is the initial shared contract for development. Exact API validation,
confidence thresholds, database constraints, and AI response schemas
must be finalized before production deployment.
