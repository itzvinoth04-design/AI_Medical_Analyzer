# MediGuide AI – Intelligent Medical Symptom Analyzer & Doctor Recommendation System

> **Academic Mini-Project • Artificial Intelligence**  
> **Department of Computer Science and Engineering**  
> **Rajalakshmi Engineering College (REC), Chennai**  
> **Project Lead:** Vinoth S (`240701592`) & Team

---

## 🌟 Executive Overview
**MediGuide AI** is an advanced clinical triage decision-support and healthcare discovery web application. It combines cutting-edge Natural Language Processing, clinical knowledge graph reasoning, supervised & unsupervised machine learning, and constraint satisfaction algorithms to provide transparent, safe, and non-alarmist health guidance.

The application is integrated with a **real-world Chennai healthcare database** stored in `SQLITE#.db`, supporting precise distance calculations via the **Haversine formula** and interactive visualization on **Leaflet OpenStreetMap**.

---

## 🎓 Complete Implementation of All 5 AI Syllabus Units

| Syllabus Unit | Key Theoretical Concept | Concrete Implementation in MediGuide AI |
| :--- | :--- | :--- |
| **Unit I: Introduction to AI** | **Intelligent Agents & PEAS** | `ClinicalTriageAgent`: Formulates **P** (Triage specificity & zero false reassurance), **E** (Patient state & Chennai hospitals), **A** (Follow-ups, recommendations, alerts), **S** (NLP tokens, sliders, GPS). |
| | **Rational & Problem-Solving Agents** | Formulates clinical triage as a state-space search problem $S_0 \to A \to \text{Goal}$. |
| **Unit II: Problem Solving** | **Informed Heuristic Search $h(C)$** | Evaluates symptom matching weight, duration congruence, and age risk adjustments to compute safe 0–100 Compatibility Scores. |
| | **Facility Optimization & Local Search** | Maximizes utility $U(H) = w_1 \cdot \text{Specialty} - w_2 \cdot \text{Dist}_{\text{Haversine}} + w_3 \cdot \text{Emergency24x7}$. |
| | **Partially Observable Belief States** | Dynamically generates clinical follow-up questions to clarify vague/high-entropy inputs. |
| **Unit III: Game Playing & CSP** | **Constraint Satisfaction Problem (CSP)** | Models doctor specialization and hospital choice as a CSP with domain pruning and forward checking. |
| **Unit IV: Logical Reasoning** | **Medical Ontology & First-Order Logic** | Represents disease criteria using FOL predicates and Horn rules. |
| | **Forward & Backward Chaining** | Forward chaining infers candidate hypotheses from symptoms; Backward chaining evaluates supporting vs missing signs. |
| | **Explainable AI (XAI)** | Generates transparent cards detailing *why* each condition was considered. |
| **Unit V: Machine Learning & NLP** | **Supervised Random Forest Classifier** | Trained ensemble model with **99.17% accuracy**, evaluated with Precision, Recall, F1, and Confusion Matrix. |
| | **Unsupervised K-Means Clustering** | Clusters 120+ symptoms into 5 clinical syndromic families ($k=5$). |
| | **NLP Entity & Negation Parsing** | Custom NLP engine extracting complaints, duration, severity, and negation (`"no fever"`). |

---

## 🛡️ Critical Clinical Safety & Red-Flag Safeguards
1. **No Alarmism for Nonspecific Signs**: A sole complaint of `"mild headache"` is bounded to benign explanations (tension headache, dehydration, eyestrain)—never brain tumor or stroke.
2. **Emergency Red-Flag Short-Circuit**: Signs satisfying FAST stroke criteria or severe substernal crushing chest pain immediately halt normal disease scoring and activate high-visibility emergency direction to call **112 (India)** or visit the nearest 24x7 casualty.
3. **Transparent Compatibility Score**: Displayed as **Condition Compatibility Score (e.g. 82/100)**, with mandatory disclaimers clarifying that it represents ontology congruence, *not* a clinical probability.

---

## 🏥 Real-World Chennai Healthcare Database (`SQLITE#.db`)
- Covers major Chennai localities: **T. Nagar, Velachery, Adyar, Anna Nagar, Tambaram, Porur, Guindy, Nungambakkam, Chromepet, OMR, Perungudi, Mylapore, Ambattur, Kilpauk, Egmore, Vadapalani, Alwarpet, Chetpet**.
- Overpass API script (`collect_chennai_hospitals.py`) with duplicate detection based on geocoordinates and token normalization.
- Consultation Fees: Displays official verified fees (e.g., ₹900) or clearly indicates **"Call to confirm"**.
- Doctor Schedules: Shows verified OPD hours or explicitly states **"Schedule not verified – contact hospital"**.

---

## 💻 Tech Stack
- **Frontend**: React.js, Vite, Tailwind CSS, Lucide React, Recharts, Leaflet, Canvas-Confetti
- **Backend**: Python 3.8+, Flask, Flask-CORS, SQLAlchemy, PyJWT, Werkzeug
- **AI & NLP**: Scikit-Learn (Random Forest, K-Means), Custom Regex/Syntactic NLP Engine, Heuristic Search Engine, CSP Solver
- **PDF Generation**: ReportLab
- **Database**: SQLite (`SQLITE#.db`)

---

## 🚀 Quick Setup & Run Instructions

### 1. Prerequisites
- Python 3.8+
- Node.js v18+ and npm

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# (Optional) Activate your Python virtual environment
# python -m venv venv
# .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize & Seed Database (Populates SQLITE#.db)
python -m scripts.seed_database

# Run Automated Test Suite (Verifies all 6 test scenarios)
python -m unittest tests.test_ai_scenarios

# Start Flask Backend Server (Port 5000)
python run.py
```

### 3. Frontend Setup
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Start Vite Development Server (Port 5173)
npm run dev
```
Open **`http://localhost:5173`** in your browser.

---

## 🧪 Pre-Configured Test Accounts & One-Click Scenarios

### Demo Credentials
- **Patient Account**: `patient@mediguide.ai` / `Patient@123`
- **Admin Account**: `admin@mediguide.ai` / `Admin@123`

### One-Click Test Scenarios (Module 15 Validation)
On the Symptom Input page, click any of the 6 scenario pills:
1. **Case 1: Mild Headache** → Bounded to tension-type/dehydration; asks dynamic follow-up questions.
2. **Case 2: Viral Triad** (`Headache + fever + body pain`) → Suggests acute viral illness; routes to **General Physician**.
3. **Case 3: Migraine & Vision Changes** → Evaluates migraine; routes to **Neurologist**.
4. **Case 4: Sudden Weakness** → Triggers immediate **112 Emergency Red-Flag Alert**.
5. **Case 5: Stomach Pain + Vomiting** → Prompts dynamic follow-up questions for location/diarrhea/fever; evaluates acute gastroenteritis.
6. **Case 6: Joint Pain + Swelling** → Routes to **Orthopedic Specialist** with 90/100 recommendation match.

---

## 📄 Documentation Sitemap
- [System Architecture](docs/architecture.md)
- [5-Unit AI Methodology & Mathematics](docs/ai_methodology.md)
- [Database Schema (SQLITE#.db)](docs/database_schema.md)
- [REST API Endpoints](docs/api_documentation.md)

---
© 2026 MediGuide AI. Developed for Academic AI Demonstration.
