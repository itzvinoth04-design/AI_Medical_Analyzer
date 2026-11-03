from flask import Blueprint, request, jsonify, send_file, make_response
from io import BytesIO
from app.models import (
    db, Assessment, AssessmentSymptom, AssessmentResult, Symptom, Condition, Specialty, Hospital
)
from app.services.auth_middleware import optional_token, token_required
from app.ai_engine.hybrid_engine import HybridClinicalInferenceEngine
from app.services.pdf_generator import MedicalReportPDFGenerator
from app.knowledge_base.medical_ontology import FOLLOW_UP_QUESTIONS_BANK

assessment_bp = Blueprint("assessment", __name__)
hybrid_engine = HybridClinicalInferenceEngine()

@assessment_bp.route("/follow-ups", methods=["POST"])
def get_follow_up_questions():
    """
    Module 3: Generates relevant follow-up questions dynamically
    based on initial symptoms (e.g. headache location/onset, stomach pain vomiting/fever).
    """
    data = request.get_json() or {}
    symptom_codes = data.get("symptom_codes", [])
    raw_text = data.get("raw_text", "")

    # Also extract from raw text if codes not provided
    if not symptom_codes and raw_text:
        nlp_res = hybrid_engine.nlp.parse_text(raw_text)
        symptom_codes = [s["code"] for s in nlp_res["extracted_symptoms"]]

    questions = []
    seen_ids = set()

    for code in symptom_codes:
        if code in FOLLOW_UP_QUESTIONS_BANK:
            for q in FOLLOW_UP_QUESTIONS_BANK[code]:
                if q["id"] not in seen_ids:
                    seen_ids.add(q["id"])
                    questions.append(q)

    return jsonify({
        "symptom_codes": symptom_codes,
        "questions": questions,
        "total_questions": len(questions)
    }), 200

@assessment_bp.route("/analyze", methods=["POST"])
@optional_token
def analyze_assessment(current_user):
    """
    Modules 4 & 5: Executes complete hybrid AI triage inference pipeline.
    Saves to SQLite database (SQLITE#.db) if user is logged in.
    """
    data = request.get_json() or {}

    raw_text = data.get("raw_text")
    selected_symptom_codes = data.get("selected_symptom_codes", [])
    severity = data.get("severity", "Moderate")
    duration_days = int(data.get("duration_days", 1))
    progress_status = data.get("progress_status", "Unchanged")
    patient_age = int(data.get("age", 25))
    patient_gender = data.get("gender", "Unspecified")
    chronic_conditions = data.get("chronic_conditions")
    follow_up_answers = data.get("follow_up_answers", {})

    # Run AI analysis
    ai_result = hybrid_engine.process_assessment(
        raw_text=raw_text,
        selected_symptom_codes=selected_symptom_codes,
        severity=severity,
        duration_days=duration_days,
        progress_status=progress_status,
        patient_age=patient_age,
        patient_gender=patient_gender,
        chronic_conditions=chronic_conditions,
        follow_up_answers=follow_up_answers
    )

    assessment_id = None

    # If user is authenticated, persist assessment in database
    if current_user:
        doc_rec = ai_result.get("doctor_recommendation", {})
        spec_name = doc_rec.get("primary_specialty", "General Physician")
        spec_obj = Specialty.query.filter_by(name=spec_name).first()

        assessment = Assessment(
            user_id=current_user.id,
            raw_input_text=raw_text,
            chief_complaint=ai_result["nlp_entities"].get("chief_complaint"),
            duration_days=duration_days,
            severity=severity,
            progress_status=progress_status,
            is_emergency=ai_result["is_emergency"],
            red_flag_reason=ai_result["emergency_alert"] if ai_result["is_emergency"] else None,
            recommended_specialty_id=spec_obj.id if spec_obj else None,
            doctor_recommendation_match=doc_rec.get("recommendation_match", 85),
            doctor_recommendation_reason=doc_rec.get("reason")
        )
        db.session.add(assessment)
        db.session.flush()

        # Link symptoms
        for sym_info in ai_result["active_symptoms"]:
            sym_obj = Symptom.query.filter_by(code=sym_info["code"]).first()
            if sym_obj:
                asym = AssessmentSymptom(
                    assessment_id=assessment.id,
                    symptom_id=sym_obj.id,
                    severity=severity,
                    is_negated=False
                )
                db.session.add(asym)

        # Link results
        for rank_idx, cond_res in enumerate(ai_result["top_conditions"]):
            cond_obj = Condition.query.filter_by(code=cond_res["condition_code"]).first()
            if cond_obj:
                ares = AssessmentResult(
                    assessment_id=assessment.id,
                    condition_id=cond_obj.id,
                    compatibility_score=cond_res["compatibility_score"],
                    supporting_symptoms="|".join(cond_res["supporting_symptoms"]),
                    missing_symptoms="|".join(cond_res["missing_symptoms"]),
                    why_considered=cond_res["why_considered"],
                    rank_order=rank_idx + 1
                )
                db.session.add(ares)

        db.session.commit()
        assessment_id = assessment.id

    response_payload = {
        "assessment_id": assessment_id,
        "is_saved": bool(current_user),
        **ai_result
    }
    return jsonify(response_payload), 200

@assessment_bp.route("/history", methods=["GET"])
@token_required
def get_user_history(current_user):
    """Module 1 & 9: Retrieves user's previous symptom analysis reports."""
    assessments = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).all()
    return jsonify({"history": [a.to_dict() for a in assessments]}), 200

@assessment_bp.route("/<int:assessment_id>", methods=["GET"])
@token_required
def get_assessment_details(current_user, assessment_id):
    """Retrieves specific assessment report ensuring user privacy."""
    assessment = Assessment.query.filter_by(id=assessment_id, user_id=current_user.id).first()
    if not assessment:
        return jsonify({"error": "Assessment record not found or access denied"}), 404
    return jsonify({"assessment": assessment.to_dict()}), 200

@assessment_bp.route("/<int:assessment_id>", methods=["DELETE"])
@token_required
def delete_assessment(current_user, assessment_id):
    """Allows user to delete medical record."""
    assessment = Assessment.query.filter_by(id=assessment_id, user_id=current_user.id).first()
    if not assessment:
        return jsonify({"error": "Assessment record not found"}), 404

    db.session.delete(assessment)
    db.session.commit()
    return jsonify({"message": "Assessment record successfully deleted"}), 200

@assessment_bp.route("/compare", methods=["POST"])
@token_required
def compare_assessments(current_user):
    """Compares two historical assessments side-by-side."""
    data = request.get_json() or {}
    id1 = data.get("assessment_id_1")
    id2 = data.get("assessment_id_2")

    a1 = Assessment.query.filter_by(id=id1, user_id=current_user.id).first()
    a2 = Assessment.query.filter_by(id=id2, user_id=current_user.id).first()

    if not a1 or not a2:
        return jsonify({"error": "One or both assessment IDs were not found"}), 404

    return jsonify({
        "assessment_1": a1.to_dict(),
        "assessment_2": a2.to_dict(),
        "comparison_notes": f"Assessment 1 from {a1.created_at.strftime('%Y-%m-%d')} compared with Assessment 2 from {a2.created_at.strftime('%Y-%m-%d')}."
    }), 200

@assessment_bp.route("/<int:assessment_id>/pdf", methods=["GET"])
@token_required
def download_pdf_report(current_user, assessment_id):
    """Module 9: Generates downloadable clinical PDF report using ReportLab."""
    assessment = Assessment.query.filter_by(id=assessment_id, user_id=current_user.id).first()
    if not assessment:
        return jsonify({"error": "Assessment record not found"}), 404

    assessment_dict = assessment.to_dict()
    patient_dict = current_user.to_dict()
    if current_user.profile:
        patient_dict.update(current_user.profile.to_dict())

    # Get sample nearby facilities matching specialty
    spec_name = assessment_dict.get("recommended_specialty", "General Physician")
    hospitals = Hospital.query.limit(4).all()
    nearby_list = [h.to_dict() for h in hospitals]

    pdf_bytes = MedicalReportPDFGenerator.generate_assessment_pdf(
        assessment_data=assessment_dict,
        patient_data=patient_dict,
        nearby_facilities=nearby_list
    )

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=MediGuide_Report_{assessment_id}.pdf"
    return response
