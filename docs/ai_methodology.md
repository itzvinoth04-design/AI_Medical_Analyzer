# MediGuide AI – Comprehensive Artificial Intelligence Syllabus Implementation

This document provides a detailed academic and computational breakdown of how **MediGuide AI** concretely implements the concepts from all five units of the Artificial Intelligence syllabus.

---

## Unit I: Introduction to Artificial Intelligence

### 1. Intelligent Agents & PEAS Representation
MediGuide AI models clinical triage as an autonomous rational agent interacting with patients and medical entities:
- **Performance Measure (P)**:
  - Safety score: 100% sensitivity to emergency red flags (FAST criteria, ACS signs).
  - Specificity score: Non-alarmist boundaries on isolated nonspecific symptoms (e.g., headache).
  - Referral utility: Selecting the appropriate tier of care (Primary Care vs Medical/Surgical Specialist).
- **Environment (E)**:
  - Partially observable patient state (subjective symptom reporting, varying duration, hidden pathophysiology).
  - Medical Knowledge Base (120+ symptoms, 16 disease archetypes, 13 medical specialties).
  - Metropolitan Chennai Healthcare Ecosystem (18 verified localities, real coordinates, verified fees and OPD hours).
- **Actuators (A)**:
  - Dynamic follow-up questionnaire.
  - Condition compatibility assessment score (0–100).
  - Specialist recommendation and clinical rationale card.
  - Emergency 112 alert banner with immediate casualty hospital routing.
  - ReportLab PDF medical summary generator.
- **Sensors (S)**:
  - Free-form natural language text parser (NLP tokens, negations, durations).
  - Categorized symptom multi-selectors.
  - Numerical sliders (duration in days, severity level).
  - Patient baseline profile (age, chronic illnesses, allergies).
  - Geolocation coordinates (browser GPS or locality anchor).

### 2. Rational and Problem-Solving Agents
- **Formulation**: Formulates clinical triage as a goal-directed search problem:
  - **Initial State $S_0$**: Patient's initial chief complaint and reported symptoms.
  - **Actions $A$**: Query ontology, trigger Horn rules, execute dynamic follow-up questioning, solve CSP doctor constraint.
  - **Goal Test $G$**: Stable belief state reached where candidate condition hypotheses have verified supporting/missing signs and specialist routing is resolved.
  - **Path Cost**: Risk penalty function penalizing diagnostic alarmism and delayed emergency detection.

---

## Unit II: Problem Solving & Heuristic Search

### 1. Informed Heuristic Search $h(C)$
Candidate condition ranking utilizes a heuristic compatibility function $h(C)$ that quantifies congruence between observed findings and condition knowledge nodes:

$$h(C) = \left[ \left( \frac{\sum_{s \in S_{\text{matched}}} w(s)}{\sum_{s \in S_{\text{expected}}} w(s)} \right) \cdot M_{\text{sev}} \cdot P_{\text{mand}} \cdot P_{\text{dur}} \right] \times 100$$

Where:
- $w(s)$: Clinical importance weight of symptom $s$.
- $M_{\text{sev}}$: Severity amplifier ($0.95$ for Mild, $1.0$ for Moderate, $1.08$ for Severe).
- $P_{\text{mand}}$: Hallmark symptom penalty ($0.65$ if mandatory clinical sign is missing).
- $P_{\text{dur}}$: Duration congruence penalty (penalizes acute conditions lasting $>21$ days).

### 2. Local Search & Healthcare Facility Optimization
When matching patients to Chennai healthcare establishments, the system maximizes the facility utility function:

$$\max_{H \in \text{Hospitals}} U(H) = w_1 \cdot \text{HasSpecialty}(H, Sp) - w_2 \cdot \text{Dist}_{\text{Haversine}}(P, H) + w_3 \cdot \text{Emergency24x7}(H)$$

Where Haversine distance is computed as:
$$d = 2R \cdot \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)$$

---

## Unit III: Game Playing & Constraint Satisfaction Problems (CSP)

### 1. CSP Formalization for Doctor & Clinic Triage
- **Variables**:
  - $X_{\text{specialty}} \in D_{\text{specialties}}$ (Domain of 13 specialties)
  - $X_{\text{triage\_level}} \in \{\text{Emergency\_Bypass}, \text{PrimaryCare\_Initial}, \text{Specialist\_Direct}\}$
  - $X_{\text{distance\_radius}} \in [0.0\text{ km}, 50.0\text{ km}]$
- **Constraints**:
  - $C_1$: $\text{IsEmergency}(P) \implies X_{\text{triage\_level}} = \text{Emergency\_Bypass}$
  - $C_2$: $\text{IsNonspecific}(P) \implies X_{\text{specialty}} = \text{'General Physician'}$
  - $C_3$: $\text{HasHallmarkOrganSign}(P, \text{Organ}) \implies X_{\text{specialty}} \in \{\text{Specialist}(\text{Organ}), \text{'General Physician'}\}$
  - $C_4$: $\text{HaversineDistance}(P, H) \le X_{\text{distance\_radius}}$

### 2. Constraint Propagation & Forward Checking
The recommendation engine applies forward checking to prune irrelevant hospital candidates lacking the required department before computing distance ranking.

---

## Unit IV: Knowledge Representation & Logical Reasoning

### 1. Clinical Ontology & First-Order Logic (FOL)
Relationships are represented using First-Order Logic predicates:
- $\forall p, s: \text{HasSymptom}(p, s) \land \text{IsRedFlag}(s) \implies \text{EmergencyAlert}(p)$
- $\forall s, c: \text{Indicates}(s, c) \land \text{Mandatory}(s, c) \land \neg \text{HasSymptom}(p, s) \implies \text{Penalty}(c)$
- $\forall c, sp: \text{ClassifiedAs}(c, sp) \implies \text{CandidateSpecialty}(sp)$

### 2. Forward Chaining
Data-driven inference fires propositional Horn clauses starting from patient symptoms:
- Example: $\text{Fever} \land \text{Headache} \land \text{BodyPain} \implies \text{InferCandidate}(\text{Acute Viral Illness})$

### 3. Backward Chaining
Goal-driven verification starts with candidate condition hypothesis $H$:
- Tests supporting observed symptoms.
- Tests unobserved/missing hallmark criteria.
- Emits Explainable AI (XAI) rationale cards.

---

## Unit V: Machine Learning & NLP Applications

### 1. Supervised Learning: Random Forest Classifier
- **Model**: Multi-class Random Forest (100 estimators, max depth 12).
- **Dataset**: 1,920 synthesized clinical cases across 16 disease archetypes.
- **Evaluation Metrics**:
  - Overall Accuracy: **99.17%**
  - Macro Average F1-Score: **99.18%**
  - Weighted Average F1-Score: **99.18%**
- **Feature Importance**: Quantifies the contribution of each symptom feature in predicting diagnoses.

### 2. Unsupervised Learning: K-Means Symptom Clustering ($k=5$)
Clusters symptoms based on their co-occurrence distributions into 5 clinical syndromic families:
1. Head, Neurological & Sensory Syndromes
2. Respiratory & Systemic Infectious Cluster
3. Digestive & Gastrointestinal Patterns
4. Musculoskeletal & Articular Syndromes
5. Critical Emergency & Vascular Signs

### 3. Natural Language Processing (NLP)
- Tokenization & medical synonym expansion.
- Preceding syntactic window negation detection (`"no fever"`, `"denies chest pain"`).
- Duration regex parser (`"2 days"`, `"since yesterday"`).
- Severity and anatomical body part mapper.
