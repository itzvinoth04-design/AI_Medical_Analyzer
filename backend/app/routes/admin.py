from flask import Blueprint, request, jsonify
from app.models import (
    db, Hospital, Specialty, Symptom, Condition, MedicalRule, DataSource, User, Assessment
)
from app.services.auth_middleware import admin_required
from scripts.collect_chennai_hospitals import normalize_name

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/stats", methods=["GET"])
@admin_required
def get_admin_stats(current_user):
    """Returns platform health, record counts, and triage metrics."""
    return jsonify({
        "total_hospitals": Hospital.query.count(),
        "total_specialties": Specialty.query.count(),
        "total_conditions": Condition.query.count(),
        "total_symptoms": Symptom.query.count(),
        "total_rules": MedicalRule.query.count(),
        "total_users": User.query.count(),
        "total_assessments": Assessment.query.count(),
        "emergency_assessments": Assessment.query.filter_by(is_emergency=True).count()
    }), 200

@admin_bp.route("/hospitals", methods=["GET"])
@admin_required
def list_hospitals(current_user):
    hospitals = Hospital.query.order_by(Hospital.name).all()
    return jsonify({"hospitals": [h.to_dict() for h in hospitals]}), 200

@admin_bp.route("/hospitals", methods=["POST"])
@admin_required
def add_hospital(current_user):
    data = request.get_json() or {}
    name = data.get("name")
    if not name or not data.get("address") or not data.get("latitude") or not data.get("longitude"):
        return jsonify({"error": "Name, address, latitude, and longitude are required"}), 400

    norm = normalize_name(name)
    h = Hospital(
        name=name,
        normalized_name=norm,
        facility_type=data.get("facility_type", "Hospital"),
        address=data["address"],
        locality=data.get("locality", "Chennai"),
        pincode=data.get("pincode"),
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        phone=data.get("phone", "Call to confirm"),
        website=data.get("website"),
        emergency_24x7=data.get("emergency_24x7", True),
        source_url=data.get("source_url", "Admin Registry Manual Entry"),
        last_verified="Verified by Admin"
    )
    db.session.add(h)
    db.session.commit()
    return jsonify({"message": "Hospital added successfully", "hospital": h.to_dict()}), 201

@admin_bp.route("/hospitals/<int:hospital_id>", methods=["PUT"])
@admin_required
def update_hospital(current_user, hospital_id):
    h = Hospital.query.get(hospital_id)
    if not h:
        return jsonify({"error": "Hospital not found"}), 404

    data = request.get_json() or {}
    if "name" in data:
        h.name = data["name"]
        h.normalized_name = normalize_name(data["name"])
    if "address" in data:
        h.address = data["address"]
    if "locality" in data:
        h.locality = data["locality"]
    if "phone" in data:
        h.phone = data["phone"]
    if "website" in data:
        h.website = data["website"]
    if "emergency_24x7" in data:
        h.emergency_24x7 = data["emergency_24x7"]

    db.session.commit()
    return jsonify({"message": "Hospital updated successfully", "hospital": h.to_dict()}), 200

@admin_bp.route("/hospitals/<int:hospital_id>", methods=["DELETE"])
@admin_required
def delete_hospital(current_user, hospital_id):
    h = Hospital.query.get(hospital_id)
    if not h:
        return jsonify({"error": "Hospital not found"}), 404
    db.session.delete(h)
    db.session.commit()
    return jsonify({"message": "Hospital removed successfully"}), 200

@admin_bp.route("/rules", methods=["GET"])
@admin_required
def list_rules(current_user):
    rules = MedicalRule.query.all()
    return jsonify({"rules": [r.to_dict() for r in rules]}), 200

@admin_bp.route("/rules/<int:rule_id>/toggle", methods=["PUT"])
@admin_required
def toggle_rule(current_user, rule_id):
    r = MedicalRule.query.get(rule_id)
    if not r:
        return jsonify({"error": "Rule not found"}), 404
    r.is_active = not r.is_active
    db.session.commit()
    return jsonify({"message": f"Rule status updated to {'Active' if r.is_active else 'Disabled'}", "rule": r.to_dict()}), 200

@admin_bp.route("/sources", methods=["GET"])
@admin_required
def list_sources(current_user):
    sources = DataSource.query.all()
    return jsonify({"sources": [s.to_dict() for s in sources]}), 200
