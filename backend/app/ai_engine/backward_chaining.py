from typing import List, Dict, Any, Set
from app.knowledge_base.medical_ontology import CONDITIONS_DATA, SYMPTOMS_DATA

class BackwardChainingEngine:
    """
    Backward Chaining Verification Engine (Unit IV: Logical Reasoning).
    Hypothesizes candidate conditions and backward-chains to verify required clinical premises:
    - Verifies supporting observed symptoms
    - Identifies missing unobserved diagnostic criteria
    - Generates Explainable AI (XAI) rationale for each hypothesis
    """

    def __init__(self):
        self.conditions = {c["code"]: c for c in CONDITIONS_DATA}
        self.symptoms_map = {s["code"]: s["name"] for s in SYMPTOMS_DATA}

    def verify_hypothesis(self, condition_code: str, active_symptoms: List[str]) -> Dict[str, Any]:
        """
        Backwards-chains from hypothesis condition_code against patient's active symptom set.
        """
        cond = self.conditions.get(condition_code)
        if not cond:
            return {
                "condition_code": condition_code,
                "verified": False,
                "supporting_symptoms": [],
                "missing_symptoms": [],
                "why_considered": "Condition record not found."
            }

        active_set: Set[str] = set(active_symptoms)
        expected_symptoms = cond["symptoms"]

        supporting_codes = []
        missing_codes = []
        mandatory_satisfied = True

        for sym_req in expected_symptoms:
            code = sym_req["code"]
            is_mand = sym_req.get("mandatory", False)
            if code in active_set:
                supporting_codes.append(code)
            else:
                missing_codes.append(code)
                if is_mand:
                    mandatory_satisfied = False

        supporting_names = [self.symptoms_map.get(c, c) for c in supporting_codes]
        missing_names = [self.symptoms_map.get(c, c) for c in missing_codes]

        # Generate Explainable AI (XAI) clinical rationale
        if len(supporting_names) > 0:
            supp_str = ", ".join(supporting_names)
            if len(missing_names) > 0:
                why = f"Considered due to presence of characteristic symptom(s): {supp_str}. However, other classic features such as {', '.join(missing_names[:2])} were not reported."
            else:
                why = f"Strong clinical match. Presents with all core hallmark signs: {supp_str}."
        else:
            why = "Considered as a differential alternative based on syndromic category, but key hallmark symptoms are absent."

        return {
            "condition_code": condition_code,
            "condition_name": cond["name"],
            "mandatory_satisfied": mandatory_satisfied,
            "supporting_symptoms": supporting_names,
            "missing_symptoms": missing_names,
            "why_considered": why,
            "category": cond["category"],
            "urgency_level": cond["urgency_level"],
            "recommended_specialty": cond["specialty_name"],
            "general_explanation": cond["general_explanation"],
            "when_to_seek_care": cond["when_to_seek_care"]
        }
