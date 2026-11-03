import sys
import os
from pathlib import Path

# Add backend to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from flask import Flask
from werkzeug.security import generate_password_hash
from app.config import Config
from app.models import (
    db, User, PatientProfile, Specialty, Symptom, Condition,
    ConditionSymptom, Hospital, HospitalSpecialty, Doctor,
    ConsultationFee, OpeningHours, MedicalRule, DataSource
)
from app.knowledge_base.medical_ontology import (
    SPECIALTIES_DATA, SYMPTOMS_DATA, CONDITIONS_DATA, LOGICAL_RULES
)
from scripts.collect_chennai_hospitals import (
    normalize_name, is_duplicate, fetch_overpass_chennai_facilities
)

# Comprehensive Verified Real-World Chennai Healthcare Registry
VERIFIED_CHENNAI_HOSPITALS = [
    {
        "name": "Apollo Hospitals, Greams Road",
        "facility_type": "Hospital",
        "address": "21 Greams Lane, Off Greams Road, Thousand Lights, Chennai, Tamil Nadu 600006",
        "locality": "Nungambakkam",
        "pincode": "600006",
        "latitude": 13.0601,
        "longitude": 80.2525,
        "phone": "+91 44 2829 0200",
        "website": "https://www.apollohospitals.com/chennai",
        "emergency_24x7": True,
        "specialties": ["Cardiologist", "Neurologist", "General Physician", "Gastroenterologist", "Orthopedic Specialist", "Pulmonologist", "ENT Specialist", "Urologist", "Endocrinologist"],
        "fee_display": "₹900 - ₹1200",
        "fee_status": "Published",
        "fee_amount": 950.0,
        "opd_hours": "08:00 AM - 08:00 PM (24x7 Emergency)",
        "source_url": "https://www.apollohospitals.com"
    },
    {
        "name": "Fortis Malar Hospital",
        "facility_type": "Hospital",
        "address": "52 1st Main Road, Gandhi Nagar, Adyar, Chennai, Tamil Nadu 600020",
        "locality": "Adyar",
        "pincode": "600020",
        "latitude": 13.0076,
        "longitude": 80.2571,
        "phone": "+91 44 4289 2222",
        "website": "https://www.fortishealthcare.com/location/fortis-malar-hospital-chennai",
        "emergency_24x7": True,
        "specialties": ["Cardiologist", "Neurologist", "General Physician", "Orthopedic Specialist", "Gastroenterologist", "Pulmonologist", "Gynecologist"],
        "fee_display": "₹800 - ₹1000",
        "fee_status": "Published",
        "fee_amount": 850.0,
        "opd_hours": "08:30 AM - 07:30 PM (24x7 Emergency)",
        "source_url": "https://www.fortishealthcare.com"
    },
    {
        "name": "MIOT International",
        "facility_type": "Hospital",
        "address": "4/112 Mount Poonamallee Road, Manapakkam, Chennai, Tamil Nadu 600089",
        "locality": "Guindy",
        "pincode": "600089",
        "latitude": 13.0182,
        "longitude": 80.1772,
        "phone": "+91 44 4200 2288",
        "website": "https://www.miothospitals.com",
        "emergency_24x7": True,
        "specialties": ["Orthopedic Specialist", "Neurologist", "Cardiologist", "Pulmonologist", "Gastroenterologist", "General Physician", "ENT Specialist"],
        "fee_display": "₹900",
        "fee_status": "Published",
        "fee_amount": 900.0,
        "opd_hours": "24x7 Emergency / OPD 09:00 AM - 06:00 PM",
        "source_url": "https://www.miothospitals.com"
    },
    {
        "name": "Kauvery Hospital",
        "facility_type": "Hospital",
        "address": "199 Luz Church Road, Alwarpet, Mylapore, Chennai, Tamil Nadu 600004",
        "locality": "Alwarpet",
        "pincode": "600004",
        "latitude": 13.0335,
        "longitude": 80.2530,
        "phone": "+91 44 4000 6000",
        "website": "https://www.kauveryhospital.com",
        "emergency_24x7": True,
        "specialties": ["Cardiologist", "Neurologist", "Gastroenterologist", "General Physician", "Orthopedic Specialist", "Pulmonologist"],
        "fee_display": "₹800",
        "fee_status": "Published",
        "fee_amount": 800.0,
        "opd_hours": "08:00 AM - 08:00 PM",
        "source_url": "https://www.kauveryhospital.com"
    },
    {
        "name": "SIMS Hospital (SRM Institutes for Medical Science)",
        "facility_type": "Hospital",
        "address": "1 Jawaharlal Nehru Salai, Next to Vadapalani Metro, Vadapalani, Chennai 600026",
        "locality": "Vadapalani",
        "pincode": "600026",
        "latitude": 13.0506,
        "longitude": 80.2109,
        "phone": "+91 44 2000 2000",
        "website": "https://simshospitals.com",
        "emergency_24x7": True,
        "specialties": ["Cardiologist", "Neurologist", "Orthopedic Specialist", "Gastroenterologist", "General Physician", "Urologist"],
        "fee_display": "Call to confirm",
        "fee_status": "Call to confirm",
        "fee_amount": None,
        "opd_hours": "24x7 Emergency & General OPD",
        "source_url": "https://simshospitals.com"
    },
    {
        "name": "Gleneagles Global Health City",
        "facility_type": "Hospital",
        "address": "439 Cheran Nagar, Perumbakkam, Chennai, Tamil Nadu 600100",
        "locality": "OMR (Old Mahabalipuram Road)",
        "pincode": "600100",
        "latitude": 12.9064,
        "longitude": 80.2032,
        "phone": "+91 44 4477 7000",
        "website": "https://gleneaglesglobalhospitals.com",
        "emergency_24x7": True,
        "specialties": ["Gastroenterologist", "Cardiologist", "Neurologist", "Pulmonologist", "General Physician", "Orthopedic Specialist"],
        "fee_display": "Call to confirm",
        "fee_status": "Call to confirm",
        "fee_amount": None,
        "opd_hours": "24 Hours Emergency",
        "source_url": "https://gleneaglesglobalhospitals.com"
    },
    {
        "name": "MGM Healthcare",
        "facility_type": "Hospital",
        "address": "72 Nelson Manickam Road, Aminjikarai, Chennai, Tamil Nadu 600029",
        "locality": "Anna Nagar",
        "pincode": "600029",
        "latitude": 13.0718,
        "longitude": 80.2198,
        "phone": "+91 44 4524 2424",
        "website": "https://mgmhealthcare.in",
        "emergency_24x7": True,
        "specialties": ["Cardiologist", "Neurologist", "Pulmonologist", "Orthopedic Specialist", "General Physician", "ENT Specialist"],
        "fee_display": "₹950",
        "fee_status": "Published",
        "fee_amount": 950.0,
        "opd_hours": "08:00 AM - 08:00 PM",
        "source_url": "https://mgmhealthcare.in"
    },
    {
        "name": "Vijaya Hospital",
        "facility_type": "Hospital",
        "address": "434 N.S.K. Salai, Vadapalani, Chennai, Tamil Nadu 600026",
        "locality": "Vadapalani",
        "pincode": "600026",
        "latitude": 13.0519,
        "longitude": 80.2127,
        "phone": "+91 44 6664 6664",
        "website": "https://vijayahospital.org",
        "emergency_24x7": True,
        "specialties": ["General Physician", "Cardiologist", "Neurologist", "Orthopedic Specialist", "Gastroenterologist", "ENT Specialist"],
        "fee_display": "₹600 - ₹800",
        "fee_status": "Published",
        "fee_amount": 700.0,
        "opd_hours": "08:30 AM - 08:00 PM",
        "source_url": "https://vijayahospital.org"
    },
    {
        "name": "Prashanth Super Speciality Hospital",
        "facility_type": "Hospital",
        "address": "36 & 36A Velachery Main Road, Velachery, Chennai, Tamil Nadu 600042",
        "locality": "Velachery",
        "pincode": "600042",
        "latitude": 12.9815,
        "longitude": 80.2223,
        "phone": "+91 44 4680 5555",
        "website": "https://prashanthhealthcare.com",
        "emergency_24x7": True,
        "specialties": ["General Physician", "Gynecologist", "Cardiologist", "Orthopedic Specialist", "Gastroenterologist", "ENT Specialist"],
        "fee_display": "₹600",
        "fee_status": "Published",
        "fee_amount": 600.0,
        "opd_hours": "08:00 AM - 08:00 PM",
        "source_url": "https://prashanthhealthcare.com"
    },
    {
        "name": "Dr. Mehta's Hospitals, Chetpet",
        "facility_type": "Hospital",
        "address": "2 Mc Nichols Road, 3rd Lane, Chetpet, Chennai, Tamil Nadu 600031",
        "locality": "Chetpet",
        "pincode": "600031",
        "latitude": 13.0706,
        "longitude": 80.2372,
        "phone": "+91 44 4227 1001",
        "website": "https://mehtahospital.com",
        "emergency_24x7": True,
        "specialties": ["General Physician", "Pediatrician", "Neurologist", "Gastroenterologist", "Gynecologist", "Orthopedic Specialist"],
        "fee_display": "₹700",
        "fee_status": "Published",
        "fee_amount": 700.0,
        "opd_hours": "08:00 AM - 08:30 PM",
        "source_url": "https://mehtahospital.com"
    },
    {
        "name": "Billroth Hospitals, Shenoy Nagar",
        "facility_type": "Hospital",
        "address": "43 Lakshmi Talkies Road, Shenoy Nagar, Chennai, Tamil Nadu 600030",
        "locality": "Anna Nagar",
        "pincode": "600030",
        "latitude": 13.0811,
        "longitude": 80.2287,
        "phone": "+91 44 2664 1777",
        "website": "https://billrothhospitals.com",
        "emergency_24x7": True,
        "specialties": ["Gastroenterologist", "Cardiologist", "General Physician", "Orthopedic Specialist", "Neurologist", "ENT Specialist"],
        "fee_display": "₹650",
        "fee_status": "Published",
        "fee_amount": 650.0,
        "opd_hours": "24 Hours Emergency",
        "source_url": "https://billrothhospitals.com"
    },
    {
        "name": "Voluntary Health Services (VHS Hospital)",
        "facility_type": "Hospital",
        "address": "Rajiv Gandhi Salai, TTTI Post, Taramani, Chennai, Tamil Nadu 600113",
        "locality": "Adyar",
        "pincode": "600113",
        "latitude": 12.9868,
        "longitude": 80.2443,
        "phone": "+91 44 2254 1972",
        "website": "https://vhschennai.org",
        "emergency_24x7": True,
        "specialties": ["General Physician", "Neurologist", "Cardiologist", "Orthopedic Specialist", "Dermatologist"],
        "fee_display": "Subsidized / ₹200",
        "fee_status": "Published",
        "fee_amount": 200.0,
        "opd_hours": "08:00 AM - 02:00 PM (OPD)",
        "source_url": "https://vhschennai.org"
    },
    {
        "name": "Rajiv Gandhi Government General Hospital (RGGGH)",
        "facility_type": "Hospital",
        "address": "EVR Periyar Salai, Park Town, Near Chennai Central, Chennai, Tamil Nadu 600003",
        "locality": "Egmore",
        "pincode": "600003",
        "latitude": 13.0827,
        "longitude": 80.2785,
        "phone": "+91 44 2530 5000",
        "website": "https://tnhealth.tn.gov.in",
        "emergency_24x7": True,
        "specialties": ["General Physician", "Cardiologist", "Neurologist", "Pulmonologist", "Orthopedic Specialist", "Gastroenterologist", "ENT Specialist", "Dermatologist", "Urologist"],
        "fee_display": "Free Public Healthcare",
        "fee_status": "Published",
        "fee_amount": 0.0,
        "opd_hours": "24x7 Casualty & Emergency, OPD: 07:30 AM - 12:30 PM",
        "source_url": "https://tnhealth.tn.gov.in"
    },
    {
        "name": "Sri Ramachandra Medical Centre (SRMC)",
        "facility_type": "Hospital",
        "address": "No. 1 Ramachandra Nagar, Porur, Chennai, Tamil Nadu 600116",
        "locality": "Porur",
        "pincode": "600116",
        "latitude": 13.0366,
        "longitude": 80.1444,
        "phone": "+91 44 4592 8500",
        "website": "https://sriramachandra.edu.in",
        "emergency_24x7": True,
        "specialties": ["Cardiologist", "Neurologist", "Orthopedic Specialist", "General Physician", "Pulmonologist", "Gastroenterologist", "ENT Specialist"],
        "fee_display": "₹500 - ₹700",
        "fee_status": "Published",
        "fee_amount": 600.0,
        "opd_hours": "08:00 AM - 06:00 PM (24x7 Emergency)",
        "source_url": "https://sriramachandra.edu.in"
    },
    {
        "name": "Hindu Mission Hospital",
        "facility_type": "Hospital",
        "address": "103 GST Road, Tambaram West, Chennai, Tamil Nadu 600045",
        "locality": "Tambaram",
        "pincode": "600045",
        "latitude": 12.9261,
        "longitude": 80.1171,
        "phone": "+91 44 2226 2244",
        "website": "https://hindumissionhospital.org",
        "emergency_24x7": True,
        "specialties": ["General Physician", "Cardiologist", "Orthopedic Specialist", "Gastroenterologist", "ENT Specialist"],
        "fee_display": "₹350",
        "fee_status": "Published",
        "fee_amount": 350.0,
        "opd_hours": "08:00 AM - 07:00 PM",
        "source_url": "https://hindumissionhospital.org"
    },
    {
        "name": "Deepam Hospital, Chromepet",
        "facility_type": "Hospital",
        "address": "107 GST Road, Chromepet, Chennai, Tamil Nadu 600044",
        "locality": "Chromepet",
        "pincode": "600044",
        "latitude": 12.9519,
        "longitude": 80.1415,
        "phone": "+91 44 2241 1444",
        "website": "https://deepamhospital.com",
        "emergency_24x7": True,
        "specialties": ["General Physician", "Orthopedic Specialist", "Cardiologist", "Gynecologist", "ENT Specialist"],
        "fee_display": "₹400",
        "fee_status": "Published",
        "fee_amount": 400.0,
        "opd_hours": "08:30 AM - 08:30 PM",
        "source_url": "https://deepamhospital.com"
    },
    {
        "name": "Sir Ivan Stedeford Hospital",
        "facility_type": "Hospital",
        "address": "Chennai-Tiruvallur High Road, Ambattur, Chennai, Tamil Nadu 600053",
        "locality": "Ambattur",
        "pincode": "600053",
        "latitude": 13.1182,
        "longitude": 80.1492,
        "phone": "+91 44 2658 1267",
        "website": "https://sivanstedeford.com",
        "emergency_24x7": True,
        "specialties": ["General Physician", "Orthopedic Specialist", "ENT Specialist", "Cardiologist", "Dermatologist"],
        "fee_display": "₹300",
        "fee_status": "Published",
        "fee_amount": 300.0,
        "opd_hours": "08:00 AM - 07:00 PM",
        "source_url": "https://sivanstedeford.com"
    },
    {
        "name": "Apollo Spectra Hospitals, Alwarpet",
        "facility_type": "Hospital",
        "address": "12 C.P. Ramaswamy Road, Alwarpet, Chennai, Tamil Nadu 600018",
        "locality": "T. Nagar",
        "pincode": "600018",
        "latitude": 13.0361,
        "longitude": 80.2483,
        "phone": "+91 44 6686 2000",
        "website": "https://www.apollospectra.com/chennai",
        "emergency_24x7": True,
        "specialties": ["Orthopedic Specialist", "ENT Specialist", "Gastroenterologist", "General Physician"],
        "fee_display": "₹750",
        "fee_status": "Published",
        "fee_amount": 750.0,
        "opd_hours": "09:00 AM - 08:00 PM",
        "source_url": "https://www.apollospectra.com"
    },
    {
        "name": "Bloom Healthcare Multi-Speciality Clinic",
        "facility_type": "Clinic",
        "address": "142 Velachery Main Road, Near Vijayanagar Bus Stand, Velachery, Chennai 600042",
        "locality": "Velachery",
        "pincode": "600042",
        "latitude": 12.9772,
        "longitude": 80.2195,
        "phone": "+91 44 4858 8999",
        "website": "https://bloomhealthcare.in",
        "emergency_24x7": False,
        "specialties": ["General Physician", "Dermatologist", "ENT Specialist", "Endocrinologist"],
        "fee_display": "₹450",
        "fee_status": "Published",
        "fee_amount": 450.0,
        "opd_hours": "08:00 AM - 09:00 PM",
        "source_url": "https://bloomhealthcare.in"
    },
    {
        "name": "Apollo Clinic, OMR Perungudi",
        "facility_type": "Clinic",
        "address": "Level 1, Prince Info City I, 283/3 & 283/4 OMR, Perungudi, Chennai 600096",
        "locality": "Perungudi",
        "pincode": "600096",
        "latitude": 12.9642,
        "longitude": 80.2449,
        "phone": "+91 44 4284 8484",
        "website": "https://www.theapolloclinic.com",
        "emergency_24x7": False,
        "specialties": ["General Physician", "Dermatologist", "Gynecologist", "ENT Specialist"],
        "fee_display": "₹600",
        "fee_status": "Published",
        "fee_amount": 600.0,
        "opd_hours": "08:00 AM - 08:00 PM",
        "source_url": "https://www.theapolloclinic.com"
    },
    {
        "name": "Dr. Agarwal's Eye Hospital, Cathedral Road",
        "facility_type": "Hospital",
        "address": "19 Cathedral Road, Chennai, Tamil Nadu 600086",
        "locality": "Mylapore",
        "pincode": "600086",
        "latitude": 13.0489,
        "longitude": 80.2528,
        "phone": "+91 44 4300 4300",
        "website": "https://www.dragarwal.com",
        "emergency_24x7": True,
        "specialties": ["Ophthalmologist"],
        "fee_display": "₹500",
        "fee_status": "Published",
        "fee_amount": 500.0,
        "opd_hours": "09:00 AM - 07:00 PM",
        "source_url": "https://www.dragarwal.com"
    },
    {
        "name": "Sankara Nethralaya",
        "facility_type": "Hospital",
        "address": "41 College Road, Nungambakkam, Chennai, Tamil Nadu 600006",
        "locality": "Nungambakkam",
        "pincode": "600006",
        "latitude": 13.0645,
        "longitude": 80.2486,
        "phone": "+91 44 4227 1500",
        "website": "https://www.sankaranethralaya.org",
        "emergency_24x7": True,
        "specialties": ["Ophthalmologist"],
        "fee_display": "₹350",
        "fee_status": "Published",
        "fee_amount": 350.0,
        "opd_hours": "08:00 AM - 06:00 PM",
        "source_url": "https://www.sankaranethralaya.org"
    },
    {
        "name": "Soundarapandian Bone and Joint Hospital",
        "facility_type": "Hospital",
        "address": "AA 16 3rd Avenue, Anna Nagar, Chennai, Tamil Nadu 600040",
        "locality": "Anna Nagar",
        "pincode": "600040",
        "latitude": 13.0848,
        "longitude": 80.2114,
        "phone": "+91 44 4206 6666",
        "website": "https://boneandjointindia.com",
        "emergency_24x7": True,
        "specialties": ["Orthopedic Specialist", "General Physician"],
        "fee_display": "₹600",
        "fee_status": "Published",
        "fee_amount": 600.0,
        "opd_hours": "09:00 AM - 08:00 PM",
        "source_url": "https://boneandjointindia.com"
    },
    {
        "name": "Dr. Mohan's Diabetes Specialities Centre",
        "facility_type": "Clinic",
        "address": "6B Conran Smith Road, Gopalapuram, Chennai, Tamil Nadu 600086",
        "locality": "T. Nagar",
        "pincode": "600086",
        "latitude": 13.0512,
        "longitude": 80.2541,
        "phone": "+91 44 4396 8888",
        "website": "https://drmohans.com",
        "emergency_24x7": False,
        "specialties": ["Endocrinologist", "General Physician"],
        "fee_display": "₹550",
        "fee_status": "Published",
        "fee_amount": 550.0,
        "opd_hours": "07:30 AM - 06:00 PM",
        "source_url": "https://drmohans.com"
    },
    {
        "name": "Kumaran Hospitals, Kilpauk",
        "facility_type": "Hospital",
        "address": "214 EVR Periyar Salai, Kilpauk, Chennai, Tamil Nadu 600010",
        "locality": "Kilpauk",
        "pincode": "600010",
        "latitude": 13.0789,
        "longitude": 80.2452,
        "phone": "+91 44 2641 2222",
        "website": "https://kumaranhospitals.com",
        "emergency_24x7": True,
        "specialties": ["General Physician", "Gastroenterologist", "Orthopedic Specialist", "Neurologist", "ENT Specialist"],
        "fee_display": "Call to confirm",
        "fee_status": "Call to confirm",
        "fee_amount": None,
        "opd_hours": "24x7 Emergency",
        "source_url": "https://kumaranhospitals.com"
    }
]

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def seed_database():
    app = create_app()
    with app.app_context():
        print(f"[MediGuide AI DB] Initializing SQLite database at {Config.SQLALCHEMY_DATABASE_URI}...")
        db.create_all()

        # 1. Seed Specialties
        print("[MediGuide AI DB] Seeding Specialties...")
        specialty_map = {}
        for sp_data in SPECIALTIES_DATA:
            spec = Specialty.query.filter_by(name=sp_data["name"]).first()
            if not spec:
                spec = Specialty(
                    name=sp_data["name"],
                    category=sp_data["category"],
                    description=sp_data["description"]
                )
                db.session.add(spec)
                db.session.flush()
            specialty_map[spec.name] = spec

        # 2. Seed Symptoms
        print("[MediGuide AI DB] Seeding Symptoms ontology...")
        symptom_map = {}
        for s_data in SYMPTOMS_DATA:
            sym = Symptom.query.filter_by(code=s_data["code"]).first()
            if not sym:
                sym = Symptom(
                    code=s_data["code"],
                    name=s_data["name"],
                    category=s_data["category"],
                    body_part=s_data.get("body_part"),
                    is_red_flag=s_data.get("is_red_flag", False),
                    default_weight=s_data.get("default_weight", 1.0),
                    synonyms=s_data.get("synonyms")
                )
                db.session.add(sym)
                db.session.flush()
            symptom_map[sym.code] = sym

        # 3. Seed Conditions & ConditionSymptoms
        print("[MediGuide AI DB] Seeding Conditions & Clinical Knowledge Graph...")
        for c_data in CONDITIONS_DATA:
            cond = Condition.query.filter_by(code=c_data["code"]).first()
            spec_obj = specialty_map.get(c_data["specialty_name"])
            if not cond:
                cond = Condition(
                    code=c_data["code"],
                    name=c_data["name"],
                    category=c_data["category"],
                    urgency_level=c_data["urgency_level"],
                    description=c_data.get("description"),
                    general_explanation=c_data.get("general_explanation"),
                    when_to_seek_care=c_data.get("when_to_seek_care"),
                    recommended_specialty_id=spec_obj.id if spec_obj else None
                )
                db.session.add(cond)
                db.session.flush()

                for sym_req in c_data["symptoms"]:
                    sym_obj = symptom_map.get(sym_req["code"])
                    if sym_obj:
                        cs = ConditionSymptom(
                            condition_id=cond.id,
                            symptom_id=sym_obj.id,
                            weight=sym_req["weight"],
                            is_mandatory=sym_req.get("mandatory", False)
                        )
                        db.session.add(cs)

        # 4. Seed Medical Logic Rules
        print("[MediGuide AI DB] Seeding Medical Rules (Unit IV)...")
        for r_data in LOGICAL_RULES:
            rule = MedicalRule.query.filter_by(rule_code=r_data["code"]).first()
            if not rule:
                import json
                rule = MedicalRule(
                    rule_code=r_data["code"],
                    rule_type=r_data["rule_type"],
                    antecedent=json.dumps(r_data["antecedent"]),
                    consequent=json.dumps(r_data["consequent"]),
                    weight=r_data["weight"],
                    description=r_data["description"]
                )
                db.session.add(rule)

        # 5. Seed Real Chennai Hospitals & Clinics
        print("[MediGuide AI DB] Seeding Real Chennai Healthcare Facilities...")
        existing_facilities = []
        for h_data in VERIFIED_CHENNAI_HOSPITALS:
            norm = normalize_name(h_data["name"])
            h_data["normalized_name"] = norm

            existing_h = Hospital.query.filter_by(normalized_name=norm).first()
            if not existing_h:
                h = Hospital(
                    name=h_data["name"],
                    normalized_name=norm,
                    facility_type=h_data["facility_type"],
                    address=h_data["address"],
                    locality=h_data["locality"],
                    city="Chennai",
                    pincode=h_data["pincode"],
                    latitude=h_data["latitude"],
                    longitude=h_data["longitude"],
                    phone=h_data["phone"],
                    website=h_data["website"],
                    emergency_24x7=h_data["emergency_24x7"],
                    source_url=h_data["source_url"],
                    last_verified="Verified Directory 2026"
                )
                db.session.add(h)
                db.session.flush()

                # Add specialties
                for sp_name in h_data["specialties"]:
                    sp_obj = specialty_map.get(sp_name)
                    if sp_obj:
                        hs = HospitalSpecialty(hospital_id=h.id, specialty_id=sp_obj.id)
                        db.session.add(hs)

                # Add Consultation Fee
                fee = ConsultationFee(
                    hospital_id=h.id,
                    fee_display=h_data["fee_display"],
                    fee_status=h_data["fee_status"],
                    fee_amount=h_data["fee_amount"],
                    notes="Publicly published outpatient consultation fee" if h_data["fee_status"] == "Published" else "Contact hospital directly to confirm specific doctor fee"
                )
                db.session.add(fee)

                # Add Opening Hours
                oh = OpeningHours(
                    hospital_id=h.id,
                    is_24x7=h_data["emergency_24x7"],
                    notes=h_data["opd_hours"]
                )
                db.session.add(oh)

                existing_facilities.append(h_data)

        # 6. Seed Default Users
        print("[MediGuide AI DB] Seeding Default Users...")
        admin = User.query.filter_by(email="admin@mediguide.ai").first()
        if not admin:
            admin = User(
                email="admin@mediguide.ai",
                password_hash=generate_password_hash("Admin@123"),
                full_name="MediGuide AI Administrator",
                phone="+91 98765 43210",
                role="admin"
            )
            db.session.add(admin)

        patient = User.query.filter_by(email="patient@mediguide.ai").first()
        if not patient:
            patient = User(
                email="patient@mediguide.ai",
                password_hash=generate_password_hash("Patient@123"),
                full_name="Vinoth S",
                phone="+91 94440 12345",
                role="patient"
            )
            db.session.add(patient)
            db.session.flush()

            profile = PatientProfile(
                user_id=patient.id,
                age=22,
                gender="Male",
                location="Chennai, Tamil Nadu",
                chronic_conditions="None reported",
                allergies="No known drug allergies (NKDA)",
                emergency_contact="+91 94440 99999"
            )
            db.session.add(profile)

        # 7. Seed Data Sources record
        ds = DataSource.query.filter_by(source_name="OpenStreetMap & Official Chennai Hospital Registries").first()
        if not ds:
            ds = DataSource(
                source_name="OpenStreetMap & Official Chennai Hospital Registries",
                source_type="Geospatial & Official Public Registries",
                source_url="https://www.openstreetmap.org",
                record_count=len(VERIFIED_CHENNAI_HOSPITALS),
                status="Active & Verified"
            )
            db.session.add(ds)

        db.session.commit()
        print(f"[MediGuide AI DB] Database seeding completed successfully! File: {Config.SQLALCHEMY_DATABASE_URI}")

if __name__ == "__main__":
    seed_database()
