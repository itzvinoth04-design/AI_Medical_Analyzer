from flask import Blueprint, request, jsonify
from app.models import Symptom
from app.nlp.extractor import NLPEntityExtractor

symptoms_bp = Blueprint("symptoms", __name__)
nlp_extractor = NLPEntityExtractor()

@symptoms_bp.route("/categories", methods=["GET"])
def get_symptom_categories():
    """Returns symptoms grouped by anatomical and clinical category (Module 2 Option B)."""
    symptoms = Symptom.query.order_by(Symptom.category, Symptom.name).all()
    categories_dict = {}

    for s in symptoms:
        cat = s.category
        if cat not in categories_dict:
            categories_dict[cat] = []
        categories_dict[cat].append(s.to_dict())

    # Format into array with category title and symptoms list
    response = [{"category": cat, "symptoms": syms} for cat, syms in categories_dict.items()]
    return jsonify({"categories": response}), 200

@symptoms_bp.route("/all", methods=["GET"])
def get_all_symptoms():
    """Returns flat searchable list of all symptoms."""
    symptoms = Symptom.query.order_by(Symptom.name).all()
    return jsonify({"symptoms": [s.to_dict() for s in symptoms]}), 200

@symptoms_bp.route("/nlp-extract", methods=["POST"])
def nlp_extract():
    """Extracts clinical entities, negations, duration, severity from free-text (Module 2 Option A)."""
    data = request.get_json() or {}
    text = data.get("text", "")
    extraction_result = nlp_extractor.parse_text(text)
    return jsonify(extraction_result), 200
