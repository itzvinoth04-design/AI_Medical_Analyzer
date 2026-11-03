from typing import Dict, Any, List

class ClinicalTriageAgent:
    """
    Intelligent Agent Representation (Unit I: Introduction to AI).
    PEAS Formulation:
    - Performance Measure (P): Clinical safety, high specificity, zero false reassurance on red-flags, avoidance of alarmist over-diagnosis for benign symptoms.
    - Environment (E): Undifferentiated patient presentations, clinical ontology, medical guidelines, Chennai healthcare directory.
    - Actuators (A): Interactive follow-up questions, urgency categorization, compatibility score reports, specialist referrals, emergency 112 alerts.
    - Sensors (S): Free-text NLP tokens, categorized symptom checkboxes, duration counters, severity sliders, patient profile demographics.
    """

    def __init__(self):
        self.peas_spec = {
            "performance_measure": [
                "Maximal diagnostic triage safety and red-flag sensitivity (100% detection of critical signs)",
                "Avoidance of alarmist diagnostic leaps on non-specific isolated symptoms (e.g., headache)",
                "Accurate routing between primary care (General Physician) and tertiary specialists",
                "Patient comprehension through transparent Explainable AI (XAI) rationale"
            ],
            "environment": [
                "Partially observable clinical states (patient reports subjective feelings with uncertainty)",
                "Medical ontology encompassing 120+ symptoms, 16 condition archetypes, 13 specialties",
                "Metropolitan healthcare ecosystem (Chennai, Tamil Nadu: 15+ key localities)",
                "Dynamic, non-deterministic patient symptom progression over time"
            ],
            "actuators": [
                "Dynamic clinical follow-up questionnaire",
                "Knowledge-base compatibility assessment report",
                "Specialist doctor referral recommendation",
                "Emergency override alarm (Dial 112 / ER navigation)",
                "Downloadable PDF clinical summary"
            ],
            "sensors": [
                "NLP entity and negation parser (analyzing user free text)",
                "Structured symptom category multi-selectors",
                "Numerical duration trackers and severity gradations",
                "Patient profile indicators (age, chronic medical conditions, allergies)",
                "Browser geolocation sensor (latitude/longitude)"
            ]
        }

    def get_agent_specs(self) -> Dict[str, Any]:
        return {
            "agent_type": "Goal-Directed Rational Triage Agent",
            "peas": self.peas_spec,
            "state_space": "Partially Observable Clinical Belief State -> Knowledge Base Formulation -> Safe Action Policy"
        }
