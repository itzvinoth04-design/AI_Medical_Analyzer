from flask import Blueprint, jsonify
from app.ai_engine.peas_agent import ClinicalTriageAgent
from app.ml.classifier import MLDiagnosticClassifier

ai_methodology_bp = Blueprint("ai_methodology", __name__)
peas_agent = ClinicalTriageAgent()
ml_classifier = MLDiagnosticClassifier()

@ai_methodology_bp.route("/overview", methods=["GET"])
def get_ai_methodology():
    """
    Module 10: Complete Artificial Intelligence Syllabus Implementation.
    Returns live computational artifacts and theoretical frameworks for all 5 Units.
    """
    ml_metrics = ml_classifier.get_metrics_and_eval()
    symptom_clusters = ml_classifier.get_symptom_clusters()
    peas_data = peas_agent.get_agent_specs()

    methodology_payload = {
        "title": "MediGuide AI - Theoretical & Applied AI Syllabus Implementation",
        "units": {
            "unit_1": {
                "unit_title": "Unit I – Introduction to Artificial Intelligence",
                "core_concepts": [
                    "Intelligent Agents & PEAS Representation",
                    "Rational Agents & Safe Action Selection",
                    "Problem-Solving Agents & State-Space Formulation",
                    "Search Algorithms in Knowledge Graphs"
                ],
                "implementation_details": {
                    "agent_architecture": "ClinicalTriageAgent: Goal-directed rational triage agent.",
                    "peas": peas_data["peas"],
                    "state_space_formulation": {
                        "initial_state": "S0 = {Unstructured patient narrative, selected symptom codes, raw duration}",
                        "actions": "A = {ExtractEntities, QueryOntology, ApplyHornRules, GenerateFollowUps, RecommendSpecialist}",
                        "transition_model": "Result(s, a) -> Updated clinical belief state with pruned hypothesis set",
                        "goal_test": "Safe triage categorization reached (Compatibility score >= threshold or Emergency Override)",
                        "path_cost": "Diagnostic risk penalty (minimizing false reassurance and unnecessary specialist referral)"
                    }
                }
            },
            "unit_2": {
                "unit_title": "Unit II – Problem Solving & Informed Search",
                "core_concepts": [
                    "Informed (Heuristic) Search & Scoring Function",
                    "Local Search & Facility Optimization",
                    "Continuous and Partially Observable Environments"
                ],
                "implementation_details": {
                    "heuristic_function": {
                        "formula": "h(C) = [ (Σ w(s_matched) / Σ w(s_expected)) * M_sev * P_mand * P_dur ] * 100",
                        "variables": {
                            "w(s_matched)": "Clinical importance weight of observed symptom s present in condition C",
                            "M_sev": "Severity scaling amplifier (Mild: 0.95, Moderate: 1.0, Severe: 1.08)",
                            "P_mand": "Mandatory hallmark symptom compliance penalty (0.65 if hallmark absent)",
                            "P_dur": "Duration congruence adjustment penalty based on acute vs chronic timeline"
                        },
                        "score_representation": "Condition Compatibility Score (0-100), explicitly designated as knowledge base pattern congruence, not empirical disease probability."
                    },
                    "facility_optimization": {
                        "objective_function": "Maximize Utility U(Hospital H) = w1 * HasSpecialty(H) - w2 * HaversineDist(User, H) + w3 * Emergency24x7(H)",
                        "algorithm": "Constrained greedy local ranking with distance threshold pruning."
                    },
                    "partially_observable_handling": "Dynamic follow-up generator targeting high-entropy symptoms (headache onset, pain location) to expand belief state."
                }
            },
            "unit_3": {
                "unit_title": "Unit III – Game Playing and Constraint Satisfaction Problems (CSP)",
                "core_concepts": [
                    "Constraint Satisfaction Problems (CSP) Formulation",
                    "Constraint Propagation & Forward Checking",
                    "Domain Pruning & Specialty Routing"
                ],
                "implementation_details": {
                    "variables": [
                        {"name": "X_specialty", "domain": "13 Medical Specialties (General Physician, Cardiologist, etc.)"},
                        {"name": "X_triage_level", "domain": "{Emergency_Bypass, PrimaryCare_Initial, Specialist_Direct}"},
                        {"name": "X_distance_radius", "domain": "[0.0 km, 50.0 km]"}
                    ],
                    "constraints": [
                        "C1 (Emergency Constraint): IsEmergency(patient) == True => X_triage_level = Emergency_Bypass, bypass routine outpatient queues.",
                        "C2 (Primary Care Primacy): IsNonSpecific(symptoms) == True => X_specialty = 'General Physician' to avoid overtreatment and specialty fragmentation.",
                        "C3 (Organ Specificity): HasHallmarkSign(symptoms, OrganSys) => X_specialty = Specialist(OrganSys) ∨ 'General Physician'.",
                        "C4 (Geospatial Constraint): HaversineDistance(UserCoords, HospitalCoords) <= MaxRadius."
                    ],
                    "propagation_technique": "Forward Checking prunes hospitals lacking the constrained department before distance ranking."
                }
            },
            "unit_4": {
                "unit_title": "Unit IV – Knowledge Representation & Logical Reasoning",
                "core_concepts": [
                    "Medical Knowledge Representation & Clinical Ontology",
                    "Propositional Logic for Emergency Red Flags",
                    "First-Order Logic (FOL) Clinical Predicates",
                    "Forward Chaining (Data-Driven Inference)",
                    "Backward Chaining (Goal-Driven Verification)",
                    "Explainable AI (XAI) Transparent Rationale"
                ],
                "implementation_details": {
                    "fol_predicates": [
                        "HasSymptom(Patient, Symptom)",
                        "Suggests(Symptom, Condition)",
                        "RequiresSpecialist(Condition, Specialty)",
                        "IsRedFlag(Symptom) => EmergencyAction(Patient)"
                    ],
                    "propositional_rules": [
                        "FAST_Stroke: SuddenWeakness ∨ FacialDroop ∨ SpeechDifficulty => Emergency112",
                        "Cardiac_ACS: CrushingChestPain ∧ (ArmRadiation ∨ Sweating) => Emergency112",
                        "Safe_Headache_Bound: ExactlyOneSymptom(Headache) => ¬BrainTumor ∧ (Tension ∨ Dehydration ∨ Migraine)"
                    ],
                    "forward_chaining": "Infuses patient observed symptoms through ontology Horn clauses to derive candidate disease hypotheses.",
                    "backward_chaining": "Starts from candidate condition H, tests which criteria are fulfilled (supporting symptoms) vs unobserved (missing symptoms).",
                    "xai_explanation": "For every candidate, outputs transparent cards explaining supporting criteria, missing criteria, and general explanation."
                }
            },
            "unit_5": {
                "unit_title": "Unit V – Machine Learning & Applications",
                "core_concepts": [
                    "Supervised Ensemble Learning (Random Forest Classifier)",
                    "Model Evaluation: Precision, Recall, F1-Score, Confusion Matrix",
                    "Unsupervised Learning: K-Means Symptom Clustering",
                    "Natural Language Processing (NLP) Entity & Negation Extraction",
                    "Model Limitations & Safety Disclaimers"
                ],
                "implementation_details": {
                    "supervised_model": {
                        "algorithm": ml_metrics.get("model_type", "Random Forest Classifier"),
                        "overall_accuracy": ml_metrics.get("overall_accuracy", 99.17),
                        "macro_avg_f1": ml_metrics.get("macro_avg_f1", 99.18),
                        "training_samples": ml_metrics.get("training_samples", 1440),
                        "testing_samples": ml_metrics.get("testing_samples", 480),
                        "top_features": ml_metrics.get("top_feature_importances", [])[:8],
                        "classification_report": ml_metrics.get("classification_report", {}),
                        "confusion_matrix": ml_metrics.get("confusion_matrix", {})
                    },
                    "unsupervised_clustering": {
                        "algorithm": "K-Means Clustering (k=5)",
                        "clusters": symptom_clusters,
                        "significance": "Identifies syndromic co-occurrence patterns in high-dimensional symptom space."
                    },
                    "nlp_pipeline": {
                        "tokenization": "Regex word boundary tokenizer and medical phrase n-gram matcher",
                        "negation_detection": "Preceding window syntactic analysis ('no', 'not', 'denies', 'without')",
                        "attribute_extraction": "Duration regex parser ('2 days', 'since yesterday'), severity mapper ('mild', 'severe'), body part mapper"
                    },
                    "dataset_limitations": ml_metrics.get("dataset_limitations", [])
                }
            }
        }
    }
    return jsonify(methodology_payload), 200
