from typing import Dict, List, Any, Optional
from app.nlp.extractor import NLPEntityExtractor
from app.ai_engine.peas_agent import ClinicalTriageAgent
from app.ai_engine.forward_chaining import ForwardChainingEngine
from app.ai_engine.backward_chaining import BackwardChainingEngine
from app.ai_engine.heuristic_search import HeuristicSearchScorer
from app.ai_engine.csp_recommender import CSPDoctorRecommender
from app.ml.classifier import MLDiagnosticClassifier
from app.knowledge_base.medical_ontology import FOLLOW_UP_QUESTIONS_BANK, SYMPTOMS_DATA

class HybridClinicalInferenceEngine:
    """
    Master AI Hybrid Inference Engine for MediGuide AI.
    Integrates all five units of the Artificial Intelligence syllabus:
    - Unit I: Intelligent Agent (PEAS formulation and state-space goal search)
    - Unit II: Informed Heuristic Search (h(n) scoring, candidate ranking)
    - Unit III: Constraint Satisfaction Problem (CSP doctor recommendation & propagation)
    - Unit IV: Logical Reasoning (Forward chaining, backward chaining, propositional red flags, XAI)
    - Unit V: Machine Learning & NLP (Entity/negation extraction, Random Forest classifier, K-Means clusters)
    """

    def __init__(self):
        self.nlp = NLPEntityExtractor()
        self.peas_agent = ClinicalTriageAgent()
        self.forward_engine = ForwardChainingEngine()
        self.backward_engine = BackwardChainingEngine()
        self.heuristic_scorer = HeuristicSearchScorer()
        self.csp_recommender = CSPDoctorRecommender()
        self.ml_classifier = MLDiagnosticClassifier()

    def process_assessment(
        self,
        raw_text: Optional[str] = None,
        selected_symptom_codes: Optional[List[str]] = None,
        severity: str = "Moderate",
        duration_days: int = 1,
        progress_status: str = "Unchanged",
        patient_age: int = 30,
        patient_gender: str = "Unspecified",
        chronic_conditions: Optional[str] = None,
        follow_up_answers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end clinical triage pipeline.
        """
        # Step 1: NLP Entity & Negation Parsing (Unit V)
        nlp_res = self.nlp.parse_text(raw_text or "")
        
        # Merge NLP extracted symptoms with predefined selected symptoms
        active_codes = set()
        negated_codes = set(s["code"] for s in nlp_res["negated_symptoms"])

        if selected_symptom_codes:
            for sc in selected_symptom_codes:
                if sc not in negated_codes:
                    active_codes.add(sc)

        for es in nlp_res["extracted_symptoms"]:
            if es["code"] not in negated_codes:
                active_codes.add(es["code"])

        # If user explicitly overrode duration or severity from form
        final_duration = duration_days if duration_days > 0 else nlp_res["duration_days"]
        final_severity = severity if severity in ["Mild", "Moderate", "Severe"] else nlp_res["severity"]

        # Step 2: Emergency Red-Flag Propositional Logic & Forward Chaining (Unit IV)
        fc_res = self.forward_engine.infer_candidates(
            list(active_codes), final_severity, final_duration
        )

        is_emergency = fc_res["is_emergency"]
        emergency_alert = fc_res["emergency_alert"]
        is_isolated_single = fc_res.get("is_isolated_nonspecific", False)
        candidate_codes = fc_res["candidate_codes"]

        # Step 3: Heuristic Search & Scoring (Unit II)
        scored_candidates = self.heuristic_scorer.rank_candidates(
            candidate_codes=candidate_codes,
            active_symptoms=list(active_codes),
            severity=final_severity,
            duration_days=final_duration,
            patient_age=patient_age,
            is_isolated_single=is_isolated_single
        )

        # Step 4: ML Probabilities Integration (Unit V)
        ml_predictions = self.ml_classifier.predict_conditions(list(active_codes))
        ml_prob_map = {p["condition_code"]: p["ml_probability"] for p in ml_predictions}

        # Step 5: Backward Chaining Verification & XAI (Unit IV)
        final_conditions = []
        # Limit to top 3-5 conditions
        top_candidates = scored_candidates[:5] if not is_emergency else scored_candidates[:2]

        for rank_idx, cand in enumerate(top_candidates):
            c_code = cand["code"]
            base_score = cand["score"]
            
            # Blend with ML if available
            if c_code in ml_prob_map:
                ml_prob = ml_prob_map[c_code]
                # Hybrid weighting: 75% knowledge base rules & ontology, 25% supervised ML model
                blended_score = int(round((base_score * 0.75) + (ml_prob * 0.25)))
            else:
                blended_score = base_score

            if is_isolated_single:
                blended_score = min(72, blended_score)

            bc_res = self.backward_engine.verify_hypothesis(c_code, list(active_codes))

            final_conditions.append({
                "condition_code": c_code,
                "condition_name": bc_res["condition_name"],
                "compatibility_score": blended_score,
                "category": bc_res["category"],
                "urgency_level": bc_res["urgency_level"],
                "recommended_specialty": bc_res["recommended_specialty"],
                "supporting_symptoms": bc_res["supporting_symptoms"],
                "missing_symptoms": bc_res["missing_symptoms"],
                "why_considered": bc_res["why_considered"],
                "general_explanation": bc_res["general_explanation"],
                "when_to_seek_care": bc_res["when_to_seek_care"],
                "rank_order": rank_idx + 1
            })

        # Step 6: Constraint Satisfaction Problem (CSP) Doctor Recommendation (Unit III)
        doc_rec = self.csp_recommender.solve_recommendation(
            top_conditions=final_conditions,
            active_symptoms=list(active_codes),
            is_emergency=is_emergency,
            is_isolated_single=is_isolated_single,
            severity=final_severity
        )

        # Step 7: Check if dynamic follow-up questions are indicated (Module 3)
        relevant_follow_ups = []
        for code in active_codes:
            if code in FOLLOW_UP_QUESTIONS_BANK:
                relevant_follow_ups.extend(FOLLOW_UP_QUESTIONS_BANK[code])

        # Urgency status badge calculation
        if is_emergency:
            urgency_status = "CRITICAL EMERGENCY"
            urgency_badge_color = "emergency"  # #D64545
        elif final_severity == "Severe" or any(c["urgency_level"] == "Urgent" for c in final_conditions):
            urgency_status = "URGENT MEDICAL ATTENTION"
            urgency_badge_color = "warning"  # #E9A23B
        else:
            urgency_status = "ROUTINE CLINICAL EVALUATION"
            urgency_badge_color = "success"  # #2E9D72

        # Compile Chief Complaint and Symptom details
        extracted_symptom_details = []
        for code in active_codes:
            s_obj = next((s for s in SYMPTOMS_DATA if s["code"] == code), None)
            if s_obj:
                extracted_symptom_details.append({
                    "code": code,
                    "name": s_obj["name"],
                    "category": s_obj["category"],
                    "is_red_flag": s_obj["is_red_flag"]
                })

        return {
            "is_emergency": is_emergency,
            "emergency_alert": emergency_alert,
            "urgency_status": urgency_status,
            "urgency_badge_color": urgency_badge_color,
            "active_symptoms": extracted_symptom_details,
            "negated_symptoms": nlp_res["negated_symptoms"],
            "nlp_entities": {
                "body_parts": nlp_res["body_parts"],
                "frequency": nlp_res["frequency"],
                "extracted_duration": nlp_res["duration_raw"],
                "duration_days": final_duration,
                "severity": final_severity,
                "chief_complaint": nlp_res["chief_complaint"] or (extracted_symptom_details[0]["name"] if extracted_symptom_details else "General Discomfort")
            },
            "top_conditions": final_conditions,
            "doctor_recommendation": doc_rec,
            "follow_up_questions": relevant_follow_ups[:3],
            "is_vague": nlp_res["is_vague"] and len(active_codes) <= 1,
            "vagueness_reason": nlp_res["vagueness_reason"],
            "safety_disclaimer": (
                "IMPORTANT CLINICAL NOTICE: MediGuide AI provides preliminary health information and healthcare navigation support. "
                "The Condition Compatibility Score represents knowledge-base pattern matching, NOT a clinically validated diagnosis. "
                "This application does not provide medical prescriptions and does not replace evaluation by a qualified healthcare professional. "
                "In case of a medical emergency, dial 112 immediately or proceed to the nearest emergency room."
            )
        }
