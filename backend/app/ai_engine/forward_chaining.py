from typing import List, Dict, Any, Set
from app.knowledge_base.medical_ontology import CONDITIONS_DATA, LOGICAL_RULES

class ForwardChainingEngine:
    """
    Forward Chaining Inference Engine (Unit IV: Logical Reasoning).
    Infers candidate condition hypotheses from asserted facts (symptoms, duration, severities)
    using propositional Horn clauses and medical knowledge base rules.
    """

    def __init__(self):
        self.rules = LOGICAL_RULES
        self.conditions = CONDITIONS_DATA

    def infer_candidates(self, active_symptoms: List[str], severity: str, duration_days: int) -> Dict[str, Any]:
        """
        Executes forward chaining starting from observed clinical premises.
        Returns:
        - candidate_conditions: List of condition codes prioritized by forward rules
        - emergency_flag: bool
        - emergency_alert: str
        - triggered_rules: List of rule codes that fired
        """
        symptom_set: Set[str] = set(active_symptoms)
        triggered_rules = []
        emergency_flag = False
        emergency_alert = None
        candidate_codes: Set[str] = set()

        # Step 1: Propositional Logic Red-Flag Evaluation
        for rule in self.rules:
            if rule["rule_type"] == "propositional_red_flag":
                ant = rule["antecedent"]
                matched = False
                if "or" in ant:
                    matched = any(s in symptom_set for s in ant["or"])
                elif "and" in ant:
                    matched = all(s in symptom_set for s in ant["and"])

                if matched:
                    triggered_rules.append(rule["code"])
                    emergency_flag = True
                    emergency_alert = rule["consequent"]["alert"]
                    # If critical red flag fires, return immediate emergency override
                    if rule["code"] == "RULE_STROKE_FAST":
                        candidate_codes.add("COND_ACUTE_STROKE")
                    elif rule["code"] == "RULE_CARDIAC_RED_FLAG":
                        candidate_codes.add("COND_ACS_CARDIAC")
                    elif rule["code"] == "RULE_ANAPHYLAXIS_ALERT":
                        candidate_codes.add("COND_ANAPHYLAXIS")

        if emergency_flag:
            return {
                "candidate_codes": list(candidate_codes),
                "is_emergency": True,
                "emergency_alert": emergency_alert,
                "triggered_rules": triggered_rules,
                "is_isolated_nonspecific": False
            }

        # Step 2: Safe Clinical Heuristic Rule (Handling Isolated Nonspecific Symptoms)
        # e.g. Single complaint of "Headache"
        is_isolated_headache = (len(symptom_set) == 1 and "HEADACHE" in symptom_set)
        if is_isolated_headache:
            triggered_rules.append("RULE_HEADACHE_NONSPECIFIC")
            return {
                "candidate_codes": ["COND_TENSION_HA", "COND_DEHYDRATION", "COND_MIGRAINE"],
                "is_emergency": False,
                "emergency_alert": None,
                "triggered_rules": triggered_rules,
                "is_isolated_nonspecific": True,
                "explanation_note": "Single symptom of headache detected. Safely bounded to benign primary causes (Tension-type, dehydration, stress, migraine) rather than alarmist pathology."
            }

        # Step 3: General Forward Chaining across Knowledge Base Conditions
        for cond in self.conditions:
            cond_symptoms = [s["code"] for s in cond["symptoms"]]
            mandatory_symptoms = [s["code"] for s in cond["symptoms"] if s.get("mandatory")]

            # Check overlap
            overlap = symptom_set.intersection(cond_symptoms)
            if overlap:
                # If condition has mandatory symptoms, at least one mandatory or majority must be present
                if mandatory_symptoms:
                    if any(m in symptom_set for m in mandatory_symptoms):
                        candidate_codes.add(cond["code"])
                else:
                    candidate_codes.add(cond["code"])

        # Check for specific synergistic rules
        for rule in self.rules:
            if rule["rule_type"] == "forward_chain":
                ant = rule["antecedent"]
                if "and" in ant and all(s in symptom_set for s in ant["and"]):
                    triggered_rules.append(rule["code"])
                    boosted = rule["consequent"].get("boost_candidate")
                    if boosted:
                        candidate_codes.add(boosted)

        return {
            "candidate_codes": list(candidate_codes),
            "is_emergency": False,
            "emergency_alert": None,
            "triggered_rules": triggered_rules,
            "is_isolated_nonspecific": False
        }
