from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), default="patient")  # 'patient' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = db.relationship("PatientProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    assessments = db.relationship("Assessment", backref="user", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "phone": self.phone,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "profile": self.profile.to_dict() if self.profile else None
        }

class PatientProfile(db.Model):
    __tablename__ = "patient_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(100), default="Chennai, Tamil Nadu")
    chronic_conditions = db.Column(db.Text, nullable=True)  # JSON or comma-separated
    allergies = db.Column(db.Text, nullable=True)
    current_medications = db.Column(db.Text, nullable=True)
    emergency_contact = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "age": self.age,
            "gender": self.gender,
            "location": self.location,
            "chronic_conditions": self.chronic_conditions,
            "allergies": self.allergies,
            "current_medications": self.current_medications,
            "emergency_contact": self.emergency_contact
        }

class Specialty(db.Model):
    __tablename__ = "specialties"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default="Specialist")  # Primary Care, Medical Specialist, Surgical Specialist

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category
        }

class Symptom(db.Model):
    __tablename__ = "symptoms"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(60), nullable=False, index=True)
    body_part = db.Column(db.String(60), nullable=True)
    is_red_flag = db.Column(db.Boolean, default=False)
    default_weight = db.Column(db.Float, default=1.0)
    synonyms = db.Column(db.Text, nullable=True)  # JSON or comma-separated
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "body_part": self.body_part,
            "is_red_flag": self.is_red_flag,
            "default_weight": self.default_weight,
            "synonyms": self.synonyms.split(",") if self.synonyms else [],
            "description": self.description
        }

class Condition(db.Model):
    __tablename__ = "conditions"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    category = db.Column(db.String(60), nullable=False)
    urgency_level = db.Column(db.String(20), default="Routine")  # Emergency, Urgent, Routine, Self-Care
    description = db.Column(db.Text, nullable=True)
    general_explanation = db.Column(db.Text, nullable=True)
    when_to_seek_care = db.Column(db.Text, nullable=True)
    recommended_specialty_id = db.Column(db.Integer, db.ForeignKey("specialties.id"), nullable=True)
    
    specialty = db.relationship("Specialty", backref="conditions")
    symptoms = db.relationship("ConditionSymptom", backref="condition", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "urgency_level": self.urgency_level,
            "description": self.description,
            "general_explanation": self.general_explanation,
            "when_to_seek_care": self.when_to_seek_care,
            "recommended_specialty": self.specialty.name if self.specialty else "General Physician"
        }

class ConditionSymptom(db.Model):
    __tablename__ = "condition_symptoms"
    id = db.Column(db.Integer, primary_key=True)
    condition_id = db.Column(db.Integer, db.ForeignKey("conditions.id"), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey("symptoms.id"), nullable=False)
    weight = db.Column(db.Float, default=1.0)
    is_mandatory = db.Column(db.Boolean, default=False)
    is_contradictory = db.Column(db.Boolean, default=False)
    typical_duration_days_min = db.Column(db.Integer, default=0)
    typical_duration_days_max = db.Column(db.Integer, default=365)

    symptom = db.relationship("Symptom")

class Hospital(db.Model):
    __tablename__ = "hospitals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    normalized_name = db.Column(db.String(150), nullable=False, index=True)
    facility_type = db.Column(db.String(30), default="Hospital")  # 'Hospital' or 'Clinic'
    address = db.Column(db.String(255), nullable=False)
    locality = db.Column(db.String(80), nullable=False, index=True)  # T. Nagar, Adyar, etc.
    city = db.Column(db.String(50), default="Chennai")
    pincode = db.Column(db.String(10), nullable=True)
    latitude = db.Column(db.Float, nullable=False, index=True)
    longitude = db.Column(db.Float, nullable=False, index=True)
    phone = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    emergency_24x7 = db.Column(db.Boolean, default=True)
    source_url = db.Column(db.String(255), nullable=True)
    last_verified = db.Column(db.String(50), nullable=True)

    specialties = db.relationship("HospitalSpecialty", backref="hospital", cascade="all, delete-orphan")
    doctors = db.relationship("Doctor", backref="hospital", cascade="all, delete-orphan")
    fees = db.relationship("ConsultationFee", backref="hospital", cascade="all, delete-orphan")
    opening_hours = db.relationship("OpeningHours", backref="hospital", cascade="all, delete-orphan")

    def to_dict(self, user_lat=None, user_lng=None):
        specs = [hs.specialty.name for hs in self.specialties if hs.specialty]
        
        # Format consultation fee
        fee_info = "Call to confirm"
        if self.fees:
            fee_obj = self.fees[0]
            if fee_obj.fee_status == "Published" and fee_obj.fee_amount:
                fee_info = f"₹{fee_obj.fee_amount:.0f}"
            elif fee_obj.fee_display:
                fee_info = fee_obj.fee_display
        
        # Format OPD hours
        opd_info = "Contact hospital for schedule"
        if self.opening_hours:
            oh = self.opening_hours[0]
            if oh.is_24x7:
                opd_info = "24x7 Emergency & General OPD"
            elif oh.opd_start and oh.opd_end:
                opd_info = f"{oh.opd_start} - {oh.opd_end}"
            elif oh.notes:
                opd_info = oh.notes
        elif self.emergency_24x7:
            opd_info = "24 Hours Emergency Service"

        return {
            "id": self.id,
            "name": self.name,
            "facility_type": self.facility_type,
            "address": self.address,
            "locality": self.locality,
            "city": self.city,
            "pincode": self.pincode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "phone": self.phone or "Not publicly available",
            "website": self.website,
            "emergency_24x7": self.emergency_24x7,
            "specialties": specs,
            "consultation_fee": fee_info,
            "opd_hours": opd_info,
            "source_url": self.source_url,
            "last_verified": self.last_verified or "Public Registry"
        }

class HospitalSpecialty(db.Model):
    __tablename__ = "hospital_specialties"
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey("specialties.id"), nullable=False)

    specialty = db.relationship("Specialty")

class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey("specialties.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    qualification = db.Column(db.String(100), nullable=True)
    opd_timing_note = db.Column(db.String(200), default="Schedule not verified – contact hospital")
    is_verified = db.Column(db.Boolean, default=True)

    specialty = db.relationship("Specialty")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "qualification": self.qualification,
            "specialty": self.specialty.name if self.specialty else "General",
            "hospital_id": self.hospital_id,
            "opd_timing_note": self.opd_timing_note,
            "is_verified": self.is_verified
        }

class ConsultationFee(db.Model):
    __tablename__ = "consultation_fees"
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=True)
    specialty_id = db.Column(db.Integer, db.ForeignKey("specialties.id"), nullable=True)
    fee_amount = db.Column(db.Float, nullable=True)
    fee_display = db.Column(db.String(50), default="Call to confirm")
    fee_status = db.Column(db.String(50), default="Call to confirm")  # 'Published' or 'Call to confirm'
    notes = db.Column(db.String(255), nullable=True)

class OpeningHours(db.Model):
    __tablename__ = "opening_hours"
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
    day_of_week = db.Column(db.String(20), default="All Days")
    opd_start = db.Column(db.String(10), nullable=True)
    opd_end = db.Column(db.String(10), nullable=True)
    is_24x7 = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(150), nullable=True)

class Assessment(db.Model):
    __tablename__ = "assessments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    raw_input_text = db.Column(db.Text, nullable=True)
    chief_complaint = db.Column(db.String(200), nullable=True)
    duration_days = db.Column(db.Integer, default=1)
    severity = db.Column(db.String(20), default="Moderate")  # Mild, Moderate, Severe
    progress_status = db.Column(db.String(30), default="Unchanged")  # Improving, Worsening, Unchanged
    is_emergency = db.Column(db.Boolean, default=False)
    red_flag_reason = db.Column(db.Text, nullable=True)
    recommended_specialty_id = db.Column(db.Integer, db.ForeignKey("specialties.id"), nullable=True)
    doctor_recommendation_match = db.Column(db.Integer, default=85)
    doctor_recommendation_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    recommended_specialty = db.relationship("Specialty")
    symptoms = db.relationship("AssessmentSymptom", backref="assessment", cascade="all, delete-orphan")
    results = db.relationship("AssessmentResult", backref="assessment", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "raw_input_text": self.raw_input_text,
            "chief_complaint": self.chief_complaint,
            "duration_days": self.duration_days,
            "severity": self.severity,
            "progress_status": self.progress_status,
            "is_emergency": self.is_emergency,
            "red_flag_reason": self.red_flag_reason,
            "recommended_specialty": self.recommended_specialty.name if self.recommended_specialty else "General Physician",
            "doctor_recommendation_match": self.doctor_recommendation_match,
            "doctor_recommendation_reason": self.doctor_recommendation_reason,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "symptoms": [s.to_dict() for s in self.symptoms],
            "results": [r.to_dict() for r in self.results]
        }

class AssessmentSymptom(db.Model):
    __tablename__ = "assessment_symptoms"
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey("symptoms.id"), nullable=False)
    severity = db.Column(db.String(20), default="Moderate")
    is_negated = db.Column(db.Boolean, default=False)
    body_part = db.Column(db.String(60), nullable=True)

    symptom = db.relationship("Symptom")

    def to_dict(self):
        return {
            "id": self.id,
            "symptom_code": self.symptom.code if self.symptom else None,
            "symptom_name": self.symptom.name if self.symptom else None,
            "category": self.symptom.category if self.symptom else None,
            "severity": self.severity,
            "is_negated": self.is_negated,
            "body_part": self.body_part
        }

class AssessmentResult(db.Model):
    __tablename__ = "assessment_results"
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id"), nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey("conditions.id"), nullable=False)
    compatibility_score = db.Column(db.Integer, nullable=False)  # 0-100
    supporting_symptoms = db.Column(db.Text, nullable=True)  # JSON or comma-separated
    missing_symptoms = db.Column(db.Text, nullable=True)
    why_considered = db.Column(db.Text, nullable=True)
    rank_order = db.Column(db.Integer, default=1)

    condition = db.relationship("Condition")

    def to_dict(self):
        return {
            "id": self.id,
            "condition_name": self.condition.name if self.condition else "Unknown Condition",
            "condition_code": self.condition.code if self.condition else "UNK",
            "category": self.condition.category if self.condition else "General",
            "urgency_level": self.condition.urgency_level if self.condition else "Routine",
            "compatibility_score": self.compatibility_score,
            "supporting_symptoms": self.supporting_symptoms.split("|") if self.supporting_symptoms else [],
            "missing_symptoms": self.missing_symptoms.split("|") if self.missing_symptoms else [],
            "why_considered": self.why_considered,
            "general_explanation": self.condition.general_explanation if self.condition else "",
            "when_to_seek_care": self.condition.when_to_seek_care if self.condition else "",
            "recommended_specialty": self.condition.specialty.name if (self.condition and self.condition.specialty) else "General Physician",
            "rank_order": self.rank_order
        }

class MedicalRule(db.Model):
    __tablename__ = "medical_rules"
    id = db.Column(db.Integer, primary_key=True)
    rule_code = db.Column(db.String(50), unique=True, nullable=False)
    rule_type = db.Column(db.String(50), default="propositional_red_flag")  # red_flag, backward_chain, specialty_route
    antecedent = db.Column(db.Text, nullable=False)  # JSON logic representation
    consequent = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Float, default=1.0)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "rule_code": self.rule_code,
            "rule_type": self.rule_type,
            "antecedent": self.antecedent,
            "consequent": self.consequent,
            "weight": self.weight,
            "description": self.description,
            "is_active": self.is_active
        }

class DataSource(db.Model):
    __tablename__ = "data_sources"
    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(100), nullable=False)
    source_type = db.Column(db.String(50), default="OpenStreetMap / Overpass API")
    source_url = db.Column(db.String(255), nullable=True)
    record_count = db.Column(db.Integer, default=0)
    last_synced = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default="Active")

    def to_dict(self):
        return {
            "id": self.id,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "source_url": self.source_url,
            "record_count": self.record_count,
            "last_synced": self.last_synced.strftime("%Y-%m-%d %H:%M:%S") if self.last_synced else None,
            "status": self.status
        }
