from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize Database
    db.init_app(app)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.symptoms import symptoms_bp
    from app.routes.assessment import assessment_bp
    from app.routes.hospitals import hospitals_bp
    from app.routes.ai_methodology import ai_methodology_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(symptoms_bp, url_prefix="/api/symptoms")
    app.register_blueprint(assessment_bp, url_prefix="/api/assessment")
    app.register_blueprint(hospitals_bp, url_prefix="/api/hospitals")
    app.register_blueprint(ai_methodology_bp, url_prefix="/api/ai-methodology")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "MediGuide AI Clinical Triage Backend",
            "database": "SQLite (SQLITE#.db) Connected",
            "ai_engine": "Hybrid Engine Active (Units I-V)"
        }), 200

    return app
