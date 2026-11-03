from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, PatientProfile
from app.services.auth_middleware import generate_token, token_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    full_name = data.get("full_name", "").strip()
    phone = data.get("phone", "").strip()

    if not email or not password or not full_name:
        return jsonify({"error": "Full name, email, and password are required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email address already exists"}), 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        full_name=full_name,
        phone=phone,
        role="patient"
    )
    db.session.add(user)
    db.session.flush()

    # Create associated profile
    profile = PatientProfile(
        user_id=user.id,
        age=data.get("age"),
        gender=data.get("gender"),
        location=data.get("location", "Chennai, Tamil Nadu"),
        chronic_conditions=data.get("chronic_conditions"),
        allergies=data.get("allergies"),
        current_medications=data.get("current_medications"),
        emergency_contact=data.get("emergency_contact")
    )
    db.session.add(profile)
    db.session.commit()

    token = generate_token(user.id, user.role)
    return jsonify({
        "message": "User registered successfully",
        "token": token,
        "user": user.to_dict()
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email address or password"}), 401

    token = generate_token(user.id, user.role)
    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": user.to_dict()
    }), 200

@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user(current_user):
    return jsonify({"user": current_user.to_dict()}), 200

@auth_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    data = request.get_json() or {}
    
    if "full_name" in data:
        current_user.full_name = data["full_name"].strip()
    if "phone" in data:
        current_user.phone = data["phone"].strip()

    profile = current_user.profile
    if not profile:
        profile = PatientProfile(user_id=current_user.id)
        db.session.add(profile)

    if "age" in data:
        profile.age = data["age"]
    if "gender" in data:
        profile.gender = data["gender"]
    if "location" in data:
        profile.location = data["location"]
    if "chronic_conditions" in data:
        profile.chronic_conditions = data["chronic_conditions"]
    if "allergies" in data:
        profile.allergies = data["allergies"]
    if "current_medications" in data:
        profile.current_medications = data["current_medications"]
    if "emergency_contact" in data:
        profile.emergency_contact = data["emergency_contact"]

    db.session.commit()
    return jsonify({
        "message": "Profile updated successfully",
        "user": current_user.to_dict()
    }), 200

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    user = User.query.filter_by(email=email).first()
    if not user:
        # Avoid user enumeration in production
        return jsonify({"message": "If this email is registered, password reset instructions have been issued."}), 200

    # Simulated reset for academic deployment
    return jsonify({
        "message": "Password reset token generated. In this academic environment, you can reset your password using the demo portal.",
        "reset_link_active": True
    }), 200
