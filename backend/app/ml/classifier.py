import json
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import joblib

from app.knowledge_base.medical_ontology import SYMPTOMS_DATA, CONDITIONS_DATA

ML_DIR = Path(__file__).resolve().parent
MODEL_PATH = ML_DIR / "rf_disease_model.joblib"
METRICS_PATH = ML_DIR / "model_metrics.json"
CLUSTERS_PATH = ML_DIR / "symptom_clusters.json"

class MLDiagnosticClassifier:
    """
    Supervised and Unsupervised Machine Learning Interface (Unit V).
    Provides:
    - Probabilistic condition classification
    - Feature importance weighting per prediction
    - Evaluation metrics and cluster memberships
    """

    def __init__(self):
        self.model = None
        self.symptom_codes = [s["code"] for s in SYMPTOMS_DATA]
        self.symptom_index = {code: idx for idx, code in enumerate(self.symptom_codes)}
        self._load_model()

    def _load_model(self):
        if MODEL_PATH.exists():
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception as e:
                print(f"[MLDiagnosticClassifier] Warning: Could not load model: {e}")
                self.model = None

    def predict_conditions(self, active_symptom_codes: List[str]) -> List[Dict[str, Any]]:
        """
        Runs Random Forest model over symptom vector and outputs probabilities.
        """
        if not self.model or not active_symptom_codes:
            return []

        vector = np.zeros((1, len(self.symptom_codes)), dtype=np.float32)
        for code in active_symptom_codes:
            if code in self.symptom_index:
                vector[0, self.symptom_index[code]] = 1.0

        probs = self.model.predict_proba(vector)[0]
        classes = self.model.classes_

        results = []
        for class_code, prob in zip(classes, probs):
            if prob > 0.05:  # meaningful probability threshold
                cond_obj = next((c for c in CONDITIONS_DATA if c["code"] == class_code), None)
                results.append({
                    "condition_code": class_code,
                    "condition_name": cond_obj["name"] if cond_obj else class_code,
                    "ml_probability": round(float(prob) * 100, 1),
                    "urgency_level": cond_obj["urgency_level"] if cond_obj else "Routine",
                    "specialty": cond_obj["specialty_name"] if cond_obj else "General Physician"
                })

        results.sort(key=lambda x: x["ml_probability"], reverse=True)
        return results

    def get_metrics_and_eval(self) -> Dict[str, Any]:
        """Loads saved evaluation statistics for the AI Methodology page."""
        if METRICS_PATH.exists():
            with open(METRICS_PATH, "r") as f:
                return json.load(f)
        return {}

    def get_symptom_clusters(self) -> List[Dict[str, Any]]:
        """Loads unsupervised K-Means clusters for visualization."""
        if CLUSTERS_PATH.exists():
            with open(CLUSTERS_PATH, "r") as f:
                return json.load(f)
        return []
