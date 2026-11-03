# MediGuide AI – REST API Documentation

Base URL: `http://localhost:5000/api`

---

## 1. Authentication Endpoints

### `POST /auth/register`
Creates a new patient account with associated clinical profile.
- **Request Body**:
```json
{
  "full_name": "Vinoth S",
  "email": "vinoth@example.com",
  "password": "Password@123",
  "phone": "+91 94440 12345",
  "age": 22,
  "gender": "Male",
  "location": "Chennai, Tamil Nadu",
  "chronic_conditions": "None",
  "allergies": "No known drug allergies"
}
```
- **Response** (201 Created):
```json
{
  "message": "User registered successfully",
  "token": "eyJhbGciOi...",
  "user": { "id": 1, "email": "vinoth@example.com", "full_name": "Vinoth S" }
}
```

### `POST /auth/login`
Authenticates a user and returns a signed JWT token.
- **Request Body**:
```json
{
  "email": "patient@mediguide.ai",
  "password": "Patient@123"
}
```
- **Response** (200 OK):
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOi...",
  "user": { "id": 2, "full_name": "Vinoth S", "role": "patient" }
}
```

---

## 2. Clinical Symptom & NLP Endpoints

### `GET /symptoms/categories`
Returns verified symptoms organized by anatomical categories.

### `POST /symptoms/nlp-extract`
Extracts entities, negations, duration, severity, and body parts from raw natural language.
- **Request Body**:
```json
{
  "text": "I have been experiencing a mild headache and fever for two days, but no vomiting."
}
```
- **Response** (200 OK):
```json
{
  "extracted_symptoms": [
    { "code": "HEADACHE", "name": "Headache", "severity": "Mild" },
    { "code": "FEV", "name": "Fever", "severity": "Mild" }
  ],
  "negated_symptoms": [
    { "code": "VOMIT", "name": "Vomiting" }
  ],
  "duration_days": 2,
  "duration_raw": "2 days",
  "severity": "Mild",
  "body_parts": ["Head"]
}
```

---

## 3. Assessment & Hybrid Inference Endpoints

### `POST /assessment/follow-ups`
Generates relevant follow-up questions dynamically based on initial symptoms.

### `POST /assessment/analyze`
Executes complete hybrid inference pipeline (Units I–V).
- **Request Body**:
```json
{
  "raw_text": "Mild headache since yesterday",
  "selected_symptom_codes": ["HEADACHE"],
  "severity": "Mild",
  "duration_days": 1,
  "age": 22
}
```
- **Response** (200 OK):
```json
{
  "is_emergency": false,
  "urgency_status": "ROUTINE CLINICAL EVALUATION",
  "top_conditions": [
    {
      "condition_name": "Tension-Type Headache",
      "compatibility_score": 72,
      "recommended_specialty": "General Physician",
      "supporting_symptoms": ["Headache"],
      "missing_symptoms": ["Fatigue", "Muscle stiffness"],
      "why_considered": "Considered due to presence of characteristic symptom(s): Headache."
    }
  ],
  "doctor_recommendation": {
    "primary_specialty": "General Physician",
    "recommendation_match": 94,
    "reason": "The reported symptoms are generalized and non-specific..."
  }
}
```

### `GET /assessment/:id/pdf`
Downloads the official ReportLab clinical consultation report as a PDF.

---

## 4. Chennai Hospitals Discovery Endpoints

### `GET /hospitals/search`
Queries and ranks Chennai healthcare establishments.
- **Query Parameters**:
  - `specialty`: e.g. "Cardiologist", "General Physician"
  - `locality`: e.g. "Adyar", "Velachery", "T. Nagar"
  - `lat`, `lng`: User coordinates
  - `max_distance`: Maximum radius in km
  - `emergency_only`: Boolean
- **Response** (200 OK):
  List of facilities ranked by specialty match and Haversine distance.

---

## 5. AI Methodology Telemetry Endpoint

### `GET /ai-methodology/overview`
Returns live metrics, Random Forest classification report, confusion matrix, K-Means symptom clusters, and formal PEAS & CSP models.
