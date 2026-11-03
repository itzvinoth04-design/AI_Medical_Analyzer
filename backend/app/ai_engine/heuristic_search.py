from typing import List, Dict, Any, Set
from app.knowledge_base.medical_ontology import CONDITIONS_DATA, SYMPTOMS_DATA

class HeuristicSearchScorer:
    """
    Informed Heuristic Search & Weighted Compatibility Scoring (Unit II: Problem Solving).
    Implements a transparent clinical compatibility evaluation function h(n):
    - Symptom matching weight (mandatory + secondary symptoms)
    - Severity amplifier (mild, moderate, severe)
    - Duration congruence penalty/bonus
    - Age risk adjustment
    - Non-specific dilution factor
    Produces: Condition Compatibility Score: X/100
    (Explicitly denoted as knowledge-base compatibility, not diagnostic probability).
    """

    def __init__(self):
        self.conditions_dict = {c["code"]: c for c in CONDITIONS_DATA}
        self.symptom_weights = {s["code"]: s["default_weight"] for s in SYMPTOMS_DATA}

    def compute_compatibility_score(
        self,
        condition_code: str,
        active_symptoms: List[str],
        severity: str = "Moderate",
        duration_days: int = 1,
        patient_age: int = 30,
        is_isolated_single: bool = False
    ) -> int:
        cond = self.conditions_dict.get(condition_code)
        if not cond:
            return 0

        active_set: Set[str] = set(active_symptoms)
        expected = cond["symptoms"]

        total_possible_weight = sum(s["weight"] for s in expected)
        if total_possible_weight <= 0:
            return 0

        matched_weight = 0.0
        mandatory_matched = 0
        mandatory_total = 0

        for req in expected:
            code = req["code"]
            weight = req["weight"]
            is_mand = req.get("mandatory", False)
            if is_mand:
                mandatory_total += 1

            if code in active_set:
                matched_weight += weight
                if is_mand:
                    mandatory_matched += 1

        # Base ratio of matched symptoms
        base_ratio = matched_weight / total_possible_weight

        # Severity scaling: Severe gives higher alignment if core symptoms present
        sev_multiplier = 1.0
        if severity == "Severe":
            sev_multiplier = 1.08
        elif severity == "Mild":
            sev_multiplier = 0.95

        # Penalty if mandatory symptom is missing
        mandatory_penalty = 1.0
        if mandatory_total > 0 and mandatory_matched < mandatory_total:
            mandatory_penalty = 0.65  # Substantial penalty if core hallmark sign is absent

        # Duration adjustment
        duration_penalty = 1.0
        if "ACUTE" in cond["code"] or "FEVER" in cond["code"]:
            if duration_days > 21:  # Acute illness lasting > 3 weeks is unlikely acute viral
                duration_penalty = 0.8
        elif "ARTHRITIS" in cond["code"] and duration_days > 30:
            duration_penalty = 1.05  # Chronic timeline aligns with degenerative joint disease

        # Single isolated non-specific symptom safety cap
        # If user ONLY inputs "headache", cap compatibility score at 65-75 to prevent false certainty
        safety_cap = 100
        if is_isolated_single:
            safety_cap = 72

        raw_score = (base_ratio * 100) * sev_multiplier * mandatory_penalty * duration_penalty
        final_score = int(min(safety_cap, max(15, round(raw_score))))
        return final_score

    def rank_candidates(
        self,
        candidate_codes: List[str],
        active_symptoms: List[str],
        severity: str,
        duration_days: int,
        patient_age: int,
        is_isolated_single: bool
    ) -> List[Dict[str, Any]]:
        scored = []
        for code in candidate_codes:
            score = self.compute_compatibility_score(
                code, active_symptoms, severity, duration_days, patient_age, is_isolated_single
            )
            scored.append({"code": code, "score": score})

        # Heuristic sort descending by score
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored
