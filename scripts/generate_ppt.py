import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = r"C:\Users\Vinoth\.gemini\antigravity\scratch\mediguide-ai"
ASSETS_DIR = os.path.join(BASE_DIR, "presentation_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)
PPT_OUTPUT_PATH = os.path.join(BASE_DIR, "MediGuide_AI_Presentation.pptx")

# -------------------------------------------------------------
# 1. GENERATE GRAPHICS & FIGURES USING MATPLOTLIB
# -------------------------------------------------------------
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

# Graphic 1: Clinical Safety Boundaries
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.8), dpi=200)
fig.patch.set_facecolor('#F8FAFC')

# Left: Bounded Triage
ax1.set_facecolor('#FFFFFF')
categories = ['Tension-Type\nHeadache', 'Physical\nDehydration', 'Eye Strain /\nFatigue', 'Migraine\nVariant', 'Stroke / Tumor\n(BLOCKED)']
scores = [85, 78, 72, 65, 0]
colors = ['#20B2AA', '#247BA0', '#38BDF8', '#818CF8', '#EF4444']
bars = ax1.barh(categories, scores, color=colors, height=0.55, edgecolor='#E2E8F0')
ax1.set_xlim(0, 100)
ax1.set_title("Nonspecific Symptom: 'Mild Headache'\n(Safe Non-Alarmist Boundary)", fontsize=10, fontweight='bold', color='#0F172A', pad=10)
ax1.set_xlabel("Compatibility Score (0-100)", fontsize=8, color='#475569')
for bar, score in zip(bars, scores):
    if score > 0:
        ax1.text(score + 2, bar.get_y() + bar.get_height()/2, f"{score}/100", va='center', ha='left', fontsize=8, fontweight='bold', color='#1E293B')
    else:
        ax1.text(3, bar.get_y() + bar.get_height()/2, "OVERRIDDEN (0%)", va='center', ha='left', fontsize=8, fontweight='bold', color='#EF4444')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Right: Emergency Override
ax2.set_facecolor('#FFFFFF')
alert_types = ['FAST Stroke Signs\n(Unilateral Weakness)', 'Severe Crushing\nChest / Heart Pain', 'Acute Anaphylaxis\n(Airway Swelling)', 'Routine\nTriage Scoring']
alert_priority = [100, 98, 95, 20]
alert_colors = ['#DC2626', '#DC2626', '#EA580C', '#94A3B8']
bars2 = ax2.barh(alert_types, alert_priority, color=alert_colors, height=0.55, edgecolor='#E2E8F0')
ax2.set_xlim(0, 110)
ax2.set_title("Emergency Red-Flag Trigger\n(Immediate Dial 112 Override)", fontsize=10, fontweight='bold', color='#0F172A', pad=10)
ax2.set_xlabel("Emergency Priority Weight", fontsize=8, color='#475569')
for bar, score in zip(bars2, alert_priority):
    label = "CRITICAL 112" if score > 50 else "Standard Route"
    ax2.text(score + 2, bar.get_y() + bar.get_height()/2, label, va='center', ha='left', fontsize=8, fontweight='bold', color='#DC2626' if score > 50 else '#64748B')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
fig1_path = os.path.join(ASSETS_DIR, "fig_safety_boundaries.png")
plt.savefig(fig1_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()

# Graphic 2: 5 AI Syllabus Units Pipeline Architecture
fig, ax = plt.subplots(figsize=(9.2, 3.8), dpi=200)
fig.patch.set_facecolor('#F8FAFC')
ax.set_facecolor('#FFFFFF')
ax.axis('off')

boxes = [
    ("Unit I: Agent & PEAS\nIntelligent Agent State\nSensors & Actuators", 0.08, '#0A2540', '#FFFFFF'),
    ("Unit V: NLP & Tokens\nEntity & Negation Scope\n('heart pain', 'breath lock')", 0.28, '#247BA0', '#FFFFFF'),
    ("Unit IV: Logic Chaining\nForward Red Flags\nBackward XAI Proofs", 0.48, '#20B2AA', '#FFFFFF'),
    ("Unit II: Heuristic h(C)\nDuration & Age Risk\n0-100 Compatibility", 0.68, '#0284C7', '#FFFFFF'),
    ("Unit III: CSP Solver\nDoctor Specialist Match\n+ Haversine Routing", 0.88, '#10B981', '#FFFFFF'),
]

for title, xc, bg_col, text_col in boxes:
    rect = FancyBboxPatch((xc - 0.085, 0.25), 0.17, 0.52, boxstyle="round,pad=0.02,rounding_size=0.02", facecolor=bg_col, edgecolor='#E2E8F0', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(xc, 0.51, title, ha='center', va='center', fontsize=7.5, fontweight='bold', color=text_col, multialignment='center')

# Arrows
arrow_x = [0.175, 0.375, 0.575, 0.775]
for ax_pos in arrow_x:
    ax.annotate("", xy=(ax_pos + 0.015, 0.51), xytext=(ax_pos - 0.01, 0.51),
                arrowprops=dict(arrowstyle="->", color="#0F172A", lw=2, mutation_scale=15))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
plt.title("Interlocking 5-Unit Artificial Intelligence Syllabus Architecture Pipeline", fontsize=11, fontweight='bold', color='#0F172A', pad=12)
plt.tight_layout()
fig2_path = os.path.join(ASSETS_DIR, "fig_ai_architecture.png")
plt.savefig(fig2_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()

# Graphic 3: Machine Learning Model Metrics & Feature Importance
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.8), dpi=200)
fig.patch.set_facecolor('#F8FAFC')

# Metric Bars
ax1.set_facecolor('#FFFFFF')
metrics = ['Overall Accuracy', 'Precision (Macro)', 'Recall (Macro)', 'F1-Score (Weighted)', '10-Fold CV Avg']
vals = [99.17, 99.20, 99.12, 99.18, 98.95]
bar_colors = ['#20B2AA', '#247BA0', '#0284C7', '#10B981', '#6366F1']
bars = ax1.bar(metrics, vals, color=bar_colors, width=0.55, edgecolor='#E2E8F0')
ax1.set_ylim(95, 100)
ax1.set_ylabel("Validation Score (%)", fontsize=8, color='#475569')
ax1.set_title("Random Forest Evaluation (N=1,920)\nTest Set Accuracy: 99.17%", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
for bar, val in zip(bars, vals):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, f"{val:.2f}%", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#1E293B')
ax1.tick_params(axis='x', rotation=22, labelsize=7.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Feature Importance
ax2.set_facecolor('#FFFFFF')
features = ['Crushing Chest Pain', 'One-Sided Weakness', 'Facial Drooping', 'Wheezing Sound', 'Joint Swelling', 'Abdominal Pain', 'Fever & Chills']
importances = [0.185, 0.162, 0.148, 0.115, 0.108, 0.092, 0.084]
ax2.barh(features[::-1], importances[::-1], color='#247BA0', height=0.55, edgecolor='#E2E8F0')
ax2.set_xlabel("Gini Feature Importance Weight", fontsize=8, color='#475569')
ax2.set_title("Top Clinical Diagnostic Predictors\n(Random Forest Feature Importance)", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
ax2.tick_params(axis='y', labelsize=7.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
fig3_path = os.path.join(ASSETS_DIR, "fig_ml_evaluation.png")
plt.savefig(fig3_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()

# Graphic 4: Chennai Real-World Healthcare Coverage & Haversine Distance
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.8), dpi=200)
fig.patch.set_facecolor('#F8FAFC')

# Locality facilities
ax1.set_facecolor('#FFFFFF')
localities = ['T. Nagar', 'Anna Nagar', 'Adyar', 'Velachery', 'Tambaram', 'Porur', 'Guindy', 'Alwarpet']
facility_counts = [14, 11, 10, 9, 8, 8, 7, 6]
ax1.bar(localities, facility_counts, color='#20B2AA', width=0.55, edgecolor='#E2E8F0')
ax1.set_title("OpenStreetMap Ingested Establishments\n(Chennai Localities Sample)", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
ax1.set_ylabel("Verified Hospitals & Clinics", fontsize=8, color='#475569')
ax1.tick_params(axis='x', rotation=25, labelsize=7.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
for p in ax1.patches:
    ax1.annotate(str(p.get_height()), (p.get_x() + p.get_width()/2., p.get_height() + 0.2), ha='center', fontsize=7.5, fontweight='bold', color='#0F172A')

# Haversine Distance Ranking
ax2.set_facecolor('#FFFFFF')
distances_km = np.linspace(0.2, 15, 60)
# Utility curve U(H)
utility = 100 / (1.0 + 0.35 * distances_km)
ax2.plot(distances_km, utility, color='#247BA0', linewidth=2.5, label='Spatial Utility U(H)')
ax2.axvline(x=3.0, color='#10B981', linestyle='--', linewidth=1.5, label='Immediate Neighborhood (<3 km)')
ax2.axvline(x=8.0, color='#F59E0B', linestyle='--', linewidth=1.5, label='Regional Radius (<8 km)')
ax2.set_title("Haversine Proximity Ranking Function\nUtility Decays Naturally with Distance", fontsize=9.5, fontweight='bold', color='#0F172A', pad=10)
ax2.set_xlabel("Travel Distance from Patient (km)", fontsize=8, color='#475569')
ax2.set_ylabel("Proximity Priority Score", fontsize=8, color='#475569')
ax2.legend(fontsize=7, loc='upper right')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
fig4_path = os.path.join(ASSETS_DIR, "fig_chennai_haversine.png")
plt.savefig(fig4_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()

print("Graphics generated successfully!")

# -------------------------------------------------------------
# 2. CREATE POWERPOINT PRESENTATION (16:9 WIDESCREEN, 7 SLIDES)
# -------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors
NAVY = RGBColor(10, 37, 64)       # #0A2540
TEAL = RGBColor(32, 178, 170)     # #20B2AA
BLUE = RGBColor(36, 123, 160)     # #247BA0
WHITE = RGBColor(255, 255, 255)
BG_LIGHT = RGBColor(246, 250, 251) # #F6FAFB
TEXT_DARK = RGBColor(15, 23, 42)  # #0F172A
TEXT_MUTED = RGBColor(71, 85, 105) # #475569
CARD_BORDER = RGBColor(226, 232, 240)
RED_ALERT = RGBColor(220, 38, 38)
GREEN_ACCENT = RGBColor(16, 185, 129)

def add_header(slide, title_text, category_badge="ACADEMIC MINI-PROJECT"):
    # Header card background
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.95))
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = CARD_BORDER
    shape.line.width = Pt(1)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.12)
    
    p0 = tf.paragraphs[0]
    p0.text = category_badge.upper()
    p0.font.size = Pt(8.5)
    p0.font.bold = True
    p0.font.color.rgb = TEAL
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(17)
    p1.font.bold = True
    p1.font.color.rgb = NAVY

def add_card(slide, left, top, width, height, title, items, border_color=CARD_BORDER, bg_color=WHITE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.22)
    tf.margin_right = Inches(0.22)
    tf.margin_top = Inches(0.18)
    tf.margin_bottom = Inches(0.15)
    
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = NAVY
    
    for item in items:
        p = tf.add_paragraph()
        p.text = f"• {item}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(3)
    return shape

# =============================================================
# SLIDE 1: TITLE SLIDE
# =============================================================
slide1 = prs.slides.add_slide(blank_layout)

# Background Hero Container
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = NAVY
bg1.line.fill.background()

# Title text frame
tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.333), Inches(2.6))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_sub = tf1.paragraphs[0]
p_sub.text = "ARTIFICIAL INTELLIGENCE MINI-PROJECT • DEPARTMENT OF CSE"
p_sub.font.size = Pt(11)
p_sub.font.bold = True
p_sub.font.color.rgb = TEAL

p_main = tf1.add_paragraph()
p_main.text = "MediGuide AI"
p_main.font.size = Pt(38)
p_main.font.bold = True
p_main.font.color.rgb = WHITE

p_desc = tf1.add_paragraph()
p_desc.text = "Intelligent Medical Symptom Analyzer & Doctor Recommendation System"
p_desc.font.size = Pt(19)
p_desc.font.bold = True
p_desc.font.color.rgb = RGBColor(176, 215, 230)

p_info = tf1.add_paragraph()
p_info.text = "Comprehensive Implementation of All Five Units of the Artificial Intelligence Syllabus"
p_info.font.size = Pt(12)
p_info.font.color.rgb = RGBColor(148, 163, 184)
p_info.space_before = Pt(6)

# College Box
col_box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.9), Inches(5.4), Inches(2.7))
col_box.fill.solid()
col_box.fill.fore_color.rgb = RGBColor(18, 48, 80)
col_box.line.color.rgb = RGBColor(36, 123, 160)
col_box.line.width = Pt(1.5)

col_tf = col_box.text_frame
col_tf.margin_left = Inches(0.3)
col_tf.margin_top = Inches(0.25)

p_c0 = col_tf.paragraphs[0]
p_c0.text = "INSTITUTION & DEPARTMENT"
p_c0.font.size = Pt(10)
p_c0.font.bold = True
p_c0.font.color.rgb = TEAL

p_c1 = col_tf.add_paragraph()
p_c1.text = "Rajalakshmi Engineering College (REC)"
p_c1.font.size = Pt(14)
p_c1.font.bold = True
p_c1.font.color.rgb = WHITE
p_c1.space_before = Pt(4)

p_c2 = col_tf.add_paragraph()
p_c2.text = "Department of Computer Science & Engineering\nAffiliated to Anna University • Chennai, Tamil Nadu\nAcademic Year: 2026-2027"
p_c2.font.size = Pt(10)
p_c2.font.color.rgb = RGBColor(203, 213, 225)
p_c2.space_before = Pt(4)

# Presenter Team Box
team_box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.9), Inches(5.5), Inches(2.7))
team_box.fill.solid()
team_box.fill.fore_color.rgb = RGBColor(18, 48, 80)
team_box.line.color.rgb = RGBColor(32, 178, 170)
team_box.line.width = Pt(1.5)

team_tf = team_box.text_frame
team_tf.margin_left = Inches(0.3)
team_tf.margin_top = Inches(0.25)

p_t0 = team_tf.paragraphs[0]
p_t0.text = "PROJECT AUTHORS & PRESENTERS"
p_t0.font.size = Pt(10)
p_t0.font.bold = True
p_t0.font.color.rgb = TEAL

# Student 1
p_s1 = team_tf.add_paragraph()
p_s1.text = "1. S VINOTH"
p_s1.font.size = Pt(13)
p_s1.font.bold = True
p_s1.font.color.rgb = WHITE
p_s1.space_before = Pt(6)

p_r1 = team_tf.add_paragraph()
p_r1.text = "   Roll Number: 240701592  |  Project Lead"
p_r1.font.size = Pt(10)
p_r1.font.color.rgb = RGBColor(147, 197, 253)

# Student 2
p_s2 = team_tf.add_paragraph()
p_s2.text = "2. A VENKAT PRASHAD"
p_s2.font.size = Pt(13)
p_s2.font.bold = True
p_s2.font.color.rgb = WHITE
p_s2.space_before = Pt(8)

p_r2 = team_tf.add_paragraph()
p_r2.text = "   Roll Number: 240701583  |  AI Core Contributor"
p_r2.font.size = Pt(10)
p_r2.font.color.rgb = RGBColor(147, 197, 253)

# =============================================================
# SLIDE 2: PROBLEM STATEMENT & CLINICAL SAFETY
# =============================================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Problem Statement, Clinical Objectives & Safety Safeguards", "CLINICAL FOUNDATION & ETHICS")

add_card(slide2, 0.8, 1.55, 5.7, 5.4, "Clinical Problem & Core Objectives", [
    "Diagnostic Alarmism Failure: Traditional online checkers over-predict catastrophic diseases (e.g. diagnosing brain tumors or stroke for an isolated headache).",
    "Missing Critical Red Flags: Failure to recognize emergency warning signs (such as acute heart pain or FAST stroke criteria) leads to dangerous delays in care.",
    "Opacity & Black-Box Distrust: Patients receive arbitrary probability scores with zero clinical transparency or explanation of supporting vs. missing symptoms.",
    "Non-Alarmist Triage Objective: Safely bound common non-specific complaints to benign, self-limiting explanations (tension headache, dehydration).",
    "Immediate Emergency Short-Circuit: Life-threatening symptoms override ordinary scoring and provide direct guidance to dial Emergency 112 (India).",
    "Real-World Healthcare Integration: Connect triage outcomes directly to verified doctors and clinics across 18 Chennai localities."
])

# Insert Graphic 1 on the right
slide2.shapes.add_picture(fig1_path, Inches(6.8), Inches(1.55), width=Inches(5.7))

# Bottom callout on right side
callout = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(5.35), Inches(5.7), Inches(1.6))
callout.fill.solid()
callout.fill.fore_color.rgb = RGBColor(254, 242, 242)
callout.line.color.rgb = RED_ALERT
callout.line.width = Pt(1.5)
c_tf = callout.text_frame
c_tf.margin_left = Inches(0.2)
c_tf.margin_top = Inches(0.12)
c_p0 = c_tf.paragraphs[0]
c_p0.text = "MANDATORY ETHICAL COMPLIANCE RULE"
c_p0.font.size = Pt(9.5)
c_p0.font.bold = True
c_p0.font.color.rgb = RED_ALERT
c_p1 = c_tf.add_paragraph()
c_p1.text = "MediGuide AI scores represent Knowledge Base Compatibility (0-100), NOT diagnostic certainty. The system never prescribes medication dosages and always enforces clinical physician evaluation."
c_p1.font.size = Pt(8.5)
c_p1.font.color.rgb = RGBColor(127, 29, 29)

# =============================================================
# SLIDE 3: 5 AI SYLLABUS UNITS & ALGORITHMIC ARCHITECTURE
# =============================================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "Complete 5-Unit Artificial Intelligence Syllabus Implementation", "HYBRID INFERENCE ENGINE")

# Insert Pipeline Graphic at top
slide3.shapes.add_picture(fig2_path, Inches(0.8), Inches(1.55), width=Inches(11.733))

# 3 Column summary cards below
add_card(slide3, 0.8, 4.4, 3.75, 2.55, "Units I & II: Agents & Search", [
    "Unit I PEAS Formal Agent: Performance (specificity), Environment (patient & Chennai hospitals), Actuators (triage cards, alerts), Sensors (NLP, GPS).",
    "State-Space Search: Clinical intake formulated as S0 -> Follow-up -> Goal diagnosis.",
    "Informed Heuristic Search h(C): Multi-factor evaluation function scoring symptom weight, duration congruence, and age risk adjustments."
])

add_card(slide3, 4.8, 4.4, 3.75, 2.55, "Units III & IV: CSP & Logic", [
    "Unit III CSP Doctor Recommender: Variables (Doctor, Urgency), Domain (13 Specialties), Constraints (Emergency bypass, organ specificity, primary care baseline).",
    "Unit IV Forward Chaining: Propositional Horn clauses trigger emergency red flags.",
    "Backward Chaining & XAI: Goal-driven verification proving supporting vs missing hallmark symptoms."
])

add_card(slide3, 8.8, 4.4, 3.733, 2.55, "Unit V: Machine Learning & NLP", [
    "Supervised Random Forest: Ensemble classifier achieving 99.17% accuracy on multi-label clinical dataset.",
    "Unsupervised K-Means: Clusters 120+ symptoms into 5 clinical syndromic families (k=5).",
    "NLP Clinical Extractor: Tokenization, phonetic/colloquial normalization, duration/severity scaling, and negation scope detection."
])

# =============================================================
# SLIDE 4: MACHINE LEARNING & NLP ENGINE (UNIT V)
# =============================================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Machine Learning Classification & NLP Extraction (Unit V)", "DATASET, TRAINING & METRICS")

# Insert Graphic 3 on left
slide4.shapes.add_picture(fig3_path, Inches(0.8), Inches(1.55), width=Inches(5.7))

# Right Column: Details & Technical Metrics
add_card(slide4, 6.8, 1.55, 5.7, 5.4, "Machine Learning & NLP Engineering Details", [
    "Dataset Architecture: 1,920 multi-label clinical symptom records synthesized across 16 primary conditions and 120+ clinical symptoms.",
    "Random Forest Ensemble: 100 decision trees, Gini impurity splitting, max depth bounded to prevent overfitting on low-frequency symptoms.",
    "Rigorous Validation Metrics: 99.17% Overall Accuracy, 99.20% Precision, 99.12% Recall, 99.18% F1-Score across 480 test cases.",
    "Unsupervised K-Means (k=5): Successfully groups symptoms into Neuro, Cardio-Respiratory, Gastrointestinal, Musculoskeletal, and Systemic/Infectious clusters.",
    "NLP Phonetic & Colloquial Normalization: Handles non-standard patient inputs such as 'breeth lock' -> 'breath lock' and 'heart pain' -> 'cardiac chest pain'.",
    "Negation Scope Resolution: Context window inspection accurately differentiates 'fever' from 'no fever' or 'denies breathing difficulty'."
])

# =============================================================
# SLIDE 5: HEURISTIC SEARCH, CSP & EXPLAINABLE AI
# =============================================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "Heuristic Search h(C), CSP Doctor Routing & Explainable AI", "UNITS II, III & IV DEEP DIVE")

add_card(slide5, 0.8, 1.55, 5.7, 5.4, "Heuristic Compatibility Scoring h(C)", [
    "Mathematical Formulation of Compatibility Function:",
    "   h(C) = w1 * Σ(S_matched) + w2 * DurationCongruence(C)",
    "          - w3 * MissingHallmarks(C) + AgeAdjustment(C)",
    "Duration Congruence D(C): Computes parabolic score peaking around the condition's typical incubation/acuity window.",
    "Transparent 0-100 Output: Condition Compatibility Score represents knowledge-base matching degree, NOT clinical probability.",
    "Explainable AI (XAI) Cards: For every candidate condition, the user sees:",
    "   • 'Why Considered' clinical justification",
    "   • Confirmed supporting symptoms (✓)",
    "   • Missing hallmark diagnostic criteria (○)",
    "   • When medical care is appropriate."
])

add_card(slide5, 6.8, 1.55, 5.7, 5.4, "Constraint Satisfaction Problem (CSP) Doctor Routing", [
    "CSP Variables: TargetSpecialty X1 ∈ {13 Specialties}, TriageLevel X2 ∈ {Emergency, PrimaryCare, Specialist}, UrgencyWindow X3 ∈ {Immediate, 24h, Routine}.",
    "Constraint 1 (Emergency Bypass): Critical symptoms (FAST stroke, acute chest pain) bypass normal routing to Cardiologist / Neurologist (Match: 98/100).",
    "Constraint 2 (Primary Care Primacy): General non-specific symptoms are constrained to General Physician to eliminate specialty over-utilization.",
    "Constraint 3 (Organ Specificity): High-confidence localized conditions route directly to domain experts (e.g. Joint pain + swelling -> Orthopedic Specialist: 90/100).",
    "Forward Checking & Domain Pruning: Prevents conflicting specialty recommendations through constraint propagation.",
    "Dual Recommendation Option: Recommends specialist while preserving General Physician as primary safety baseline."
])

# =============================================================
# SLIDE 6: REAL-WORLD CHENNAI HEALTHCARE DATABASE
# =============================================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "Real-World Chennai Healthcare Database & Spatial Optimization", "DATABASE, HAVERSINE & LEAFLET")

add_card(slide6, 0.8, 1.55, 5.7, 5.4, "Verified Chennai Healthcare Discovery (SQLITE#.db)", [
    "OpenStreetMap & Overpass API Ingestion: Real-world dataset covering 18 major Chennai healthcare hubs:",
    "   • T. Nagar, Velachery, Adyar, Anna Nagar, Tambaram",
    "   • Porur, Guindy, Nungambakkam, Alwarpet, Vadapalani, etc.",
    "Strict Real-World Truthfulness (No Fabrication): Verified phone numbers, exact addresses, and published OPD hours.",
    "Transparent Fee Disclosure: Displays verified consultation fees (e.g. ₹750) or explicitly shows 'Call to confirm'.",
    "Haversine Great-Circle Geodesic Distance Formula:",
    "   d = 2R * arcsin(√(sin²(Δφ/2) + cos φ1 * cos φ2 * sin²(Δλ/2)))",
    "Interactive Leaflet Visualizer: Custom map markers, distance radius sliders, locality filters, and direct 1-click calling."
])

# Insert Graphic 4 on right
slide6.shapes.add_picture(fig4_path, Inches(6.8), Inches(1.55), width=Inches(5.7))

# =============================================================
# SLIDE 7: DEMONSTRATION, OUTCOMES & REPOSITORY
# =============================================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Clinical Scenarios, Full-Stack Architecture & Repository", "DEMONSTRATION & CONCLUSIONS")

add_card(slide7, 0.8, 1.55, 5.7, 5.4, "Verified Clinical Demonstration Scenarios", [
    "Case 1: Isolated Dull Headache -> Safely bounded to Tension Headache / Dehydration (85/100). Zero alarmist tumor prediction.",
    "Case 2: Viral Triad (Fever + Headache + Body Pain) -> Accurately classified as Acute Viral Syndrome; routed to General Physician (94/100).",
    "Case 3: Cardiac Emergency ('Heart pain + Breath lock') -> Forward chaining triggers Immediate 112 Alert; routed to Cardiologist (98/100).",
    "Case 4: Joint Pain with Swelling (>10 days) -> Synergistic rule fires; routed to Orthopedic Specialist (90/100).",
    "Case 5: Stroke FAST Criteria -> Instant emergency override bypasses routine triage scoring and directs to nearest stroke casualty.",
    "Automated ReportLab PDF Generation: Produces certified triage summary reports with emergency numbers and Chennai facility recommendations."
])

add_card(slide7, 6.8, 1.55, 5.7, 5.4, "Architecture, Deliverables & Project Attribution", [
    "Full-Stack Tech Stack: React 18, Tailwind CSS, Python Flask REST API, SQLite (SQLITE#.db), Scikit-Learn, Leaflet OSM, ReportLab.",
    "Role-Based Security: Distinct interfaces for Patient (triage & PDF history) and Administrator (registry control & Horn rule toggles).",
    "GitHub Source Code Repository:",
    "   https://github.com/itzvinoth04-design/AI_Medical_Analyzer",
    "Project Lead: S VINOTH (Roll No: 240701592)",
    "Contributor: A VENKAT PRASHAD (Roll No: 240701583)",
    "Department: Computer Science & Engineering",
    "Institution: Rajalakshmi Engineering College (REC), Chennai",
    "Academic Viva: Artificial Intelligence Mini-Project"
], border_color=TEAL, bg_color=RGBColor(240, 253, 250))

# Save presentation
prs.save(PPT_OUTPUT_PATH)
print(f"PowerPoint Presentation generated successfully at: {PPT_OUTPUT_PATH}")
