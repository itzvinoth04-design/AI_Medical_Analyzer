from typing import List, Dict, Any, Optional

class CSPDoctorRecommender:
    """
    Constraint Satisfaction Problem (CSP) Doctor Recommendation Engine (Unit III: CSP).
    Formulation:
    - Variables:
      X1 = TargetMedicalSpecialty (Domain: 13 medical specialties)
      X2 = TriageLevel (Domain: {Emergency_Bypass, PrimaryCare_Initial, Specialist_Direct})
      X3 = UrgencyWindow (Domain: {Immediate_112, Within_24h, Routine_Days})
    - Constraints:
      C1 (Emergency Constraint): If IsEmergency == True -> TriageLevel = Emergency_Bypass, Specialty = Emergency / General Physician / Cardiologist / Neurologist depending on organ deficit.
      C2 (Primary Care Primacy): If symptoms are non-specific (e.g., headache, general fever, body pain), TargetMedicalSpecialty MUST be constrained to 'General Physician' to prevent unnecessary specialty fragmentation.
      C3 (Organ Specificity): If high confidence organ-specific signs present without red flags (e.g., Joint pain + swelling > 14 days), Specialty in {'Orthopedic Specialist', 'General Physician'}.
      C4 (Compatibility Weight): Specialty recommendation match score derived from top condition compatibility and rule confidence.
    """

    PRIMARY_CARE_SYMPTOMS = {"FEV", "FAT", "BOD_PAIN", "CHL", "WEAK", "HEADACHE", "DIZZ"}

    def __init__(self):
        pass

    def solve_recommendation(
        self,
        top_conditions: List[Dict[str, Any]],
        active_symptoms: List[str],
        is_emergency: bool,
        is_isolated_single: bool,
        severity: str
    ) -> Dict[str, Any]:
        """
        Executes Constraint Propagation and returns optimal specialty recommendation.
        """
        # Constraint C1: Emergency Override
        if is_emergency:
            # Check if stroke, cardiac, or respiratory
            if any(s in active_symptoms for s in ["SUD_WEAK", "FACE_DROP", "SPEECH_DIFF"]):
                spec = "Neurologist"
                reason = "CRITICAL EMERGENCY: Signs consistent with acute focal neurological deficit (Stroke FAST criteria). Immediate emergency hospital admission required."
            elif any(s in active_symptoms for s in ["CHEST_PAIN_SEV", "CHEST_DISCOMFORT"]) or any(c.get("condition_code") == "COND_ACS_CARDIAC" for c in top_conditions):
                spec = "Cardiologist"
                reason = "CRITICAL EMERGENCY: Severe chest or cardiac signs indicate potential acute coronary syndrome. Immediate emergency cardiology/casualty evaluation required."
            else:
                spec = "General Physician"
                reason = "CRITICAL EMERGENCY: Acute systemic distress requires immediate emergency medical department stabilization (Dial 112)."

            return {
                "primary_specialty": spec,
                "secondary_specialties": ["Emergency Medicine Specialist"],
                "recommendation_match": 98,
                "triage_level": "Emergency_Bypass",
                "reason": reason,
                "is_emergency_bypass": True
            }

        # Constraint C2: Isolated or Non-Specific Symptom Pruning (e.g. Headache alone or Viral Triad)
        active_set = set(active_symptoms)
        is_purely_primary = active_set.issubset(self.PRIMARY_CARE_SYMPTOMS) or is_isolated_single

        if is_purely_primary:
            reason = (
                "The reported symptoms are generalized and non-specific. In accordance with medical triage best practices, "
                "an initial evaluation by a primary-care General Physician is recommended to perform comprehensive physical examination "
                "and laboratory screening before any sub-specialty referral."
            )
            return {
                "primary_specialty": "General Physician",
                "secondary_specialties": [],
                "recommendation_match": 94,
                "triage_level": "PrimaryCare_Initial",
                "reason": reason,
                "is_emergency_bypass": False
            }

        # Constraint C3: Organ Specificity from Top Ranked Condition
        if top_conditions:
            top_cond = top_conditions[0]
            recommended_spec = top_cond.get("recommended_specialty", "General Physician")
            cond_name = top_cond.get("condition_name", "Clinical Condition")
            score = top_cond.get("compatibility_score", 80)

            # Check if condition suggests specific specialist or dual option
            if recommended_spec != "General Physician":
                secondary = ["General Physician"]  # Primary care remains valid safety net
                reason = (
                    f"The symptom constellation aligns most strongly with {cond_name}. "
                    f"Consulting a {recommended_spec} will facilitate specialized diagnostics and targeted therapeutic management. "
                    f"A General Physician is also suitable for initial outpatient assessment."
                )
                # Synergistic rule check (e.g. Joint pain + swelling -> Orthopedic Specialist: 90)
                if {"JOINT_PAIN", "JOINT_SWELL"}.issubset(active_set):
                    match_val = 90
                else:
                    match_val = min(96, max(85, int(score * 1.15)))
            else:
                secondary = []
                reason = (
                    f"The clinical picture suggests {cond_name}, which is routinely and effectively managed "
                    f"by a primary-care General Physician."
                )
                match_val = min(95, max(70, score))

            return {
                "primary_specialty": recommended_spec,
                "secondary_specialties": secondary,
                "recommendation_match": match_val,
                "triage_level": "Specialist_Direct" if recommended_spec != "General Physician" else "PrimaryCare_Initial",
                "reason": reason,
                "is_emergency_bypass": False
            }

        # Fallback default
        return {
            "primary_specialty": "General Physician",
            "secondary_specialties": [],
            "recommendation_match": 85,
            "triage_level": "PrimaryCare_Initial",
            "reason": "General primary-care evaluation recommended for broad baseline assessment.",
            "is_emergency_bypass": False
        }
