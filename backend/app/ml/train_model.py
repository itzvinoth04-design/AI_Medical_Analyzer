import os
import json
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

from app.knowledge_base.medical_ontology import SYMPTOMS_DATA, CONDITIONS_DATA

ML_DIR = Path(__file__).resolve().parent
MODEL_PATH = ML_DIR / "rf_disease_model.joblib"
METRICS_PATH = ML_DIR / "model_metrics.json"
CLUSTERS_PATH = ML_DIR / "symptom_clusters.json"

def generate_medical_training_data(samples_per_condition=120):
    """
    Generates structured clinical dataset for supervised and unsupervised training
    modeling symptom presence, partial manifestations, and clinical noise.
    """
    symptom_codes = [s["code"] for s in SYMPTOMS_DATA]
    symptom_index = {code: idx for idx, code in enumerate(symptom_codes)}
    num_symptoms = len(symptom_codes)

    X = []
    y = []
    labels = []

    for cond in CONDITIONS_DATA:
        cond_code = cond["code"]
        labels.append(cond_code)
        primary_symptoms = [s["code"] for s in cond["symptoms"]]
        mandatory_symptoms = [s["code"] for s in cond["symptoms"] if s.get("mandatory")]
        weights = {s["code"]: s["weight"] for s in cond["symptoms"]}

        for _ in range(samples_per_condition):
            feature_vector = np.zeros(num_symptoms, dtype=np.float32)

            # Mandatory symptoms are present with 95% probability
            for ms in mandatory_symptoms:
                if ms in symptom_index and np.random.rand() < 0.95:
                    feature_vector[symptom_index[ms]] = 1.0 + (weights.get(ms, 2.0) * 0.2)

            # Secondary symptoms present with 65-85% probability
            for ps in primary_symptoms:
                if ps not in mandatory_symptoms and ps in symptom_index:
                    if np.random.rand() < 0.75:
                        feature_vector[symptom_index[ps]] = 1.0 + (weights.get(ps, 1.5) * 0.15)

            # Random clinical noise (occasional unrelated mild fatigue or minor symptom, 5% chance)
            noise_idx = np.random.randint(0, num_symptoms)
            if symptom_codes[noise_idx] not in primary_symptoms and np.random.rand() < 0.08:
                feature_vector[noise_idx] = 0.5

            X.append(feature_vector)
            y.append(cond_code)

    return np.array(X), np.array(y), symptom_codes, labels

def train_and_evaluate_models():
    """
    Trains:
    1. Supervised Random Forest Classifier for disease matching
    2. Unsupervised K-Means clustering for symptom co-occurrence patterns
    Computes precision, recall, F1, and confusion matrix.
    """
    print("[MediGuide AI ML] Generating clinical training dataset...")
    X, y, symptom_codes, condition_labels = generate_medical_training_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print("[MediGuide AI ML] Training Random Forest Classifier...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    accuracy = float(accuracy_score(y_test, y_pred))

    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, y_pred, labels=condition_labels).tolist()

    # Feature importances (symptom contribution)
    feature_importances = []
    for code, imp in zip(symptom_codes, rf.feature_importances_):
        s_obj = next((s for s in SYMPTOMS_DATA if s["code"] == code), None)
        name = s_obj["name"] if s_obj else code
        feature_importances.append({
            "symptom_code": code,
            "symptom_name": name,
            "importance": round(float(imp), 4)
        })
    feature_importances.sort(key=lambda x: x["importance"], reverse=True)

    # 2. Unsupervised Learning: K-Means Clustering on Symptom Space
    print("[MediGuide AI ML] Running K-Means Symptom Clustering (Unit V)...")
    # Cluster symptoms based on their co-occurrence across conditions
    # Symptom feature matrix: (num_symptoms x num_conditions)
    symptom_by_condition = np.zeros((len(symptom_codes), len(condition_labels)))
    for c_idx, c_label in enumerate(condition_labels):
        cond_samples = X[y == c_label]
        symptom_by_condition[:, c_idx] = np.mean(cond_samples, axis=0)

    n_clusters = 5  # e.g., Neurological, Respiratory/Infectious, Gastrointestinal, Musculoskeletal, Acute Emergency
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(symptom_by_condition)

    clusters_output = []
    cluster_names = [
        "Head, Neurological & Sensory Syndromes",
        "Respiratory & Systemic Infectious Cluster",
        "Digestive & Gastrointestinal Patterns",
        "Musculoskeletal & Articular Syndromes",
        "Critical Emergency & Vascular Signs"
    ]

    for cluster_id in range(n_clusters):
        clustered_syms = []
        for s_idx, c_id in enumerate(cluster_labels):
            if c_id == cluster_id:
                s_obj = next((s for s in SYMPTOMS_DATA if s["code"] == symptom_codes[s_idx]), None)
                clustered_syms.append({
                    "code": symptom_codes[s_idx],
                    "name": s_obj["name"] if s_obj else symptom_codes[s_idx],
                    "category": s_obj["category"] if s_obj else "General"
                })
        clusters_output.append({
            "cluster_id": cluster_id,
            "cluster_name": cluster_names[cluster_id] if cluster_id < len(cluster_names) else f"Cluster {cluster_id+1}",
            "symptoms_count": len(clustered_syms),
            "symptoms": clustered_syms
        })

    # Save artifacts
    joblib.dump(rf, MODEL_PATH)

    metrics_payload = {
        "model_type": "Random Forest Classifier (Ensemble Supervised Learning)",
        "training_samples": len(X_train),
        "testing_samples": len(X_test),
        "overall_accuracy": round(accuracy * 100, 2),
        "macro_avg_f1": round(report["macro avg"]["f1-score"] * 100, 2),
        "weighted_avg_f1": round(report["weighted avg"]["f1-score"] * 100, 2),
        "classification_report": report,
        "confusion_matrix": {
            "labels": condition_labels,
            "matrix": cm
        },
        "top_feature_importances": feature_importances[:15],
        "dataset_limitations": [
            "Dataset synthesizes clinical guideline presentations and symptom frequency matrices.",
            "Trained for academic triage demonstration; not a substitute for clinical diagnostics.",
            "Real clinical presentations feature complex multi-morbidities and atypical presentations not fully covered by synthetic cohorts."
        ]
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics_payload, f, indent=2)

    with open(CLUSTERS_PATH, "w") as f:
        json.dump(clusters_output, f, indent=2)

    print(f"[MediGuide AI ML] Models successfully saved to {ML_DIR}")
    return metrics_payload

if __name__ == "__main__":
    train_and_evaluate_models()
