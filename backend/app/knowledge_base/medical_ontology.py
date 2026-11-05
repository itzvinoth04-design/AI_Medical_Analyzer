"""
Medical Knowledge Base & Clinical Ontology for MediGuide AI
Implements:
- Unit IV: Knowledge Representation, Propositional Logic Rules, First-Order Logic facts
- Unit I: Agent perception ground truth
- Safe Clinical Triage rules (No alarmist predictions for nonspecific complaints)
"""

SPECIALTIES_DATA = [
    {
        "name": "General Physician",
        "category": "Primary Care",
        "description": "Primary healthcare physician treating acute infections, fevers, non-specific malaise, preventative health, and systemic general illnesses."
    },
    {
        "name": "Cardiologist",
        "category": "Medical Specialist",
        "description": "Specialist in cardiovascular disorders, heart diseases, blood pressure management, and circulation issues."
    },
    {
        "name": "Neurologist",
        "category": "Medical Specialist",
        "description": "Specialist in disorders of the brain, spinal cord, nerves, migraines, neuropathy, and movement disorders."
    },
    {
        "name": "Dermatologist",
        "category": "Medical Specialist",
        "description": "Specialist in diseases and conditions affecting the skin, hair, nails, and mucous membranes."
    },
    {
        "name": "Gastroenterologist",
        "category": "Medical Specialist",
        "description": "Specialist in the digestive system, stomach, intestines, liver, gallbladder, and pancreatic conditions."
    },
    {
        "name": "Orthopedic Specialist",
        "category": "Surgical Specialist",
        "description": "Specialist in bones, joints, ligaments, tendons, fractures, arthritis, and musculoskeletal trauma."
    },
    {
        "name": "Pulmonologist",
        "category": "Medical Specialist",
        "description": "Specialist in respiratory diseases, lungs, bronchial airways, asthma, chronic bronchitis, and pneumonia."
    },
    {
        "name": "ENT Specialist",
        "category": "Surgical Specialist",
        "description": "Specialist in ear, nose, throat, sinuses, head and neck ailments (Otolaryngology)."
    },
    {
        "name": "Ophthalmologist",
        "category": "Surgical Specialist",
        "description": "Specialist in eye health, vision changes, cataracts, glaucoma, and ocular diseases."
    },
    {
        "name": "Endocrinologist",
        "category": "Medical Specialist",
        "description": "Specialist in hormones, diabetes, thyroid disorders, and metabolic conditions."
    },
    {
        "name": "Urologist",
        "category": "Surgical Specialist",
        "description": "Specialist in urinary tract infections, kidneys, bladder, and male reproductive system."
    },
    {
        "name": "Gynecologist",
        "category": "Surgical Specialist",
        "description": "Specialist in female reproductive health, pregnancy, hormonal balance, and pelvic health."
    },
    {
        "name": "Psychiatrist",
        "category": "Medical Specialist",
        "description": "Specialist in mental health, anxiety, depression, mood disorders, and psychological well-being."
    }
]

SYMPTOMS_DATA = [
    # General
    {"code": "FEV", "name": "Fever", "category": "General symptoms", "body_part": "Whole Body", "is_red_flag": False, "default_weight": 2.5, "synonyms": "high temperature,pyrexia,feverish,chills,shivering"},
    {"code": "FAT", "name": "Fatigue", "category": "General symptoms", "body_part": "Whole Body", "is_red_flag": False, "default_weight": 1.5, "synonyms": "tiredness,exhaustion,lack of energy,lethargy"},
    {"code": "BOD_PAIN", "name": "Body pain", "category": "General symptoms", "body_part": "Whole Body", "is_red_flag": False, "default_weight": 2.0, "synonyms": "body ache,muscle pain,myalgia,generalized aching"},
    {"code": "CHL", "name": "Chills and shivering", "category": "General symptoms", "body_part": "Whole Body", "is_red_flag": False, "default_weight": 2.0, "synonyms": "rigors,cold shivers,feeling freezing"},
    {"code": "WGT_LOSS", "name": "Unexplained weight loss", "category": "General symptoms", "body_part": "Whole Body", "is_red_flag": False, "default_weight": 2.0, "synonyms": "losing weight,unintentional weight drop"},
    {"code": "WEAK", "name": "Generalized weakness", "category": "General symptoms", "body_part": "Whole Body", "is_red_flag": False, "default_weight": 1.5, "synonyms": "feeling weak,asthenia,feeling faint"},

    # Head & Neurological
    {"code": "HEADACHE", "name": "Headache", "category": "Head and neurological symptoms", "body_part": "Head", "is_red_flag": False, "default_weight": 2.0, "synonyms": "head pain,head hurts,throbbing head,migraine,cephalalgia"},
    {"code": "DIZZ", "name": "Dizziness", "category": "Head and neurological symptoms", "body_part": "Head", "is_red_flag": False, "default_weight": 1.8, "synonyms": "lightheadedness,giddiness,vertigo,spinning head"},
    {"code": "SUD_WEAK", "name": "Sudden one-sided weakness", "category": "Head and neurological symptoms", "body_part": "Arms/Legs/Face", "is_red_flag": True, "default_weight": 10.0, "synonyms": "hemiparesis,arm weakness,leg weakness on one side,numbness one side"},
    {"code": "FACE_DROP", "name": "Sudden facial drooping", "category": "Head and neurological symptoms", "body_part": "Face", "is_red_flag": True, "default_weight": 10.0, "synonyms": "mouth drooping,face lopsided,facial numbness"},
    {"code": "SPEECH_DIFF", "name": "Slurred speech or difficulty speaking", "category": "Head and neurological symptoms", "body_part": "Mouth", "is_red_flag": True, "default_weight": 10.0, "synonyms": "dysarthria,aphasia,cannot speak clearly,garbled words"},
    {"code": "THUND_HEAD", "name": "Sudden severe explosive headache", "category": "Head and neurological symptoms", "body_part": "Head", "is_red_flag": True, "default_weight": 10.0, "synonyms": "worst headache of life,thunderclap headache,acute severe head pain"},
    {"code": "CONFUSION", "name": "Acute confusion or altered consciousness", "category": "Head and neurological symptoms", "body_part": "Brain", "is_red_flag": True, "default_weight": 9.0, "synonyms": "disorientation,delirium,not recognizing people"},
    {"code": "NECK_STIFF", "name": "Severe stiff neck with high fever", "category": "Head and neurological symptoms", "body_part": "Neck", "is_red_flag": True, "default_weight": 8.0, "synonyms": "nuchal rigidity,cannot bend neck to chest"},
    {"code": "VIS_CHANGE", "name": "Vision changes or blurriness", "category": "Head and neurological symptoms", "body_part": "Eyes", "is_red_flag": False, "default_weight": 2.5, "synonyms": "blurred vision,double vision,seeing flashes,visual aura"},

    # Respiratory
    {"code": "COUGH", "name": "Cough", "category": "Respiratory symptoms", "body_part": "Throat/Chest", "is_red_flag": False, "default_weight": 2.0, "synonyms": "coughing,dry cough,wet cough,phlegm cough"},
    {"code": "SORE_THROAT", "name": "Sore throat", "category": "Respiratory symptoms", "body_part": "Throat", "is_red_flag": False, "default_weight": 2.0, "synonyms": "throat pain,throat irritation,pain swallowing"},
    {"code": "SHORT_BREATH", "name": "Shortness of breath on exertion", "category": "Respiratory symptoms", "body_part": "Chest/Lungs", "is_red_flag": False, "default_weight": 3.0, "synonyms": "dyspnea,breathlessness,difficulty breathing on climbing,breeth lock,breath lock,breath locked,breathing lock,breath blocked,short of breath,shortness of breath,trouble breathing,difficulty breathing,hard to breathe,cant breathe,can't breathe,loss of breath,breath shortness,heavy breathing,struggling to breathe"},
    {"code": "SEV_BREATH_DIFF", "name": "Severe resting breathlessness", "category": "Respiratory symptoms", "body_part": "Chest/Lungs", "is_red_flag": True, "default_weight": 10.0, "synonyms": "gasping for air,struggling to breathe,cannot speak full sentences,severe breathlessness,unable to breathe,choking sensation,severe breath lock,acute shortness of breath"},
    {"code": "WHEEZE", "name": "Wheezing whistling sound", "category": "Respiratory symptoms", "body_part": "Lungs", "is_red_flag": False, "default_weight": 2.5, "synonyms": "chest whistling,asthma attack sound,bronchial wheeze"},
    {"code": "CHEST_CONGEST", "name": "Chest congestion", "category": "Respiratory symptoms", "body_part": "Chest", "is_red_flag": False, "default_weight": 2.0, "synonyms": "tight chest from mucus,phlegm in chest"},

    # Cardiovascular
    {"code": "CHEST_PAIN_SEV", "name": "Crushing chest pain radiating to arm or jaw", "category": "Cardiovascular symptoms", "body_part": "Chest", "is_red_flag": True, "default_weight": 10.0, "synonyms": "heavy chest pressure,tight squeezing chest pain,radiating to left arm,heart pain,chest pain,pain in heart,pain in chest,pain in my heart,pain in my chest,cardiac pain,heart ache,heart hurting,heart hurts,chest hurting,angina,crushing chest pain,acute chest pain,left chest pain"},
    {"code": "CHEST_DISCOMFORT", "name": "Mild chest tightness or discomfort", "category": "Cardiovascular symptoms", "body_part": "Chest", "is_red_flag": False, "default_weight": 3.5, "synonyms": "chest tightness,dull ache in chest,mild heart pain,chest ache,discomfort in chest,chest heaviness,tightness in heart,tightness in chest"},
    {"code": "PALP", "name": "Palpitations or rapid heartbeat", "category": "Cardiovascular symptoms", "body_part": "Heart", "is_red_flag": False, "default_weight": 2.5, "synonyms": "racing heart,fluttering heartbeat,tachycardia"},
    {"code": "ANKLE_SWELL", "name": "Swelling in ankles and feet", "category": "Cardiovascular symptoms", "body_part": "Legs/Ankles", "is_red_flag": False, "default_weight": 2.0, "synonyms": "pedal edema,swollen feet,puffy ankles"},

    # Digestive
    {"code": "STOM_PAIN", "name": "Stomach or abdominal pain", "category": "Digestive symptoms", "body_part": "Abdomen", "is_red_flag": False, "default_weight": 2.5, "synonyms": "tummy ache,belly pain,abdominal cramps,gastric pain"},
    {"code": "NAUSEA", "name": "Nausea", "category": "Digestive symptoms", "body_part": "Stomach", "is_red_flag": False, "default_weight": 1.8, "synonyms": "feeling sick,queasiness,urge to vomit"},
    {"code": "VOMIT", "name": "Vomiting", "category": "Digestive symptoms", "body_part": "Stomach", "is_red_flag": False, "default_weight": 2.5, "synonyms": "throwing up,emesis,puking"},
    {"code": "DIARRHEA", "name": "Diarrhea", "category": "Digestive symptoms", "body_part": "Bowels", "is_red_flag": False, "default_weight": 2.5, "synonyms": "loose stools,watery motions,frequent loose motions"},
    {"code": "ACID_REFLUX", "name": "Heartburn or acid reflux", "category": "Digestive symptoms", "body_part": "Chest/Stomach", "is_red_flag": False, "default_weight": 2.0, "synonyms": "gerd,sour burping,burning in food pipe,indigestion"},
    {"code": "CONSTIP", "name": "Constipation", "category": "Digestive symptoms", "body_part": "Bowels", "is_red_flag": False, "default_weight": 1.5, "synonyms": "hard stools,difficulty passing stool"},
    {"code": "BLOAT", "name": "Abdominal bloating or gas", "category": "Digestive symptoms", "body_part": "Abdomen", "is_red_flag": False, "default_weight": 1.5, "synonyms": "fullness,gaseous stomach,distended belly"},
    {"code": "SEV_RLQ_PAIN", "name": "Severe sharp right lower abdominal pain", "category": "Digestive symptoms", "body_part": "Right Lower Abdomen", "is_red_flag": True, "default_weight": 8.5, "synonyms": "acute appendicitis sign,right iliac fossa tenderness"},

    # Skin
    {"code": "SKIN_RASH", "name": "Skin rash", "category": "Skin symptoms", "body_part": "Skin", "is_red_flag": False, "default_weight": 2.0, "synonyms": "red bumps,eruption,skin eruption,patches"},
    {"code": "ITCH", "name": "Itching", "category": "Skin symptoms", "body_part": "Skin", "is_red_flag": False, "default_weight": 1.8, "synonyms": "pruritus,scratchy skin,itchy sensation"},
    {"code": "HIVES", "name": "Raised red itchy wheals (hives)", "category": "Skin symptoms", "body_part": "Skin", "is_red_flag": False, "default_weight": 2.5, "synonyms": "urticaria,allergic welts,nettle rash"},
    {"code": "ANAPHYLAXIS_SWELL", "name": "Rapid swelling of lips, tongue or face", "category": "Skin symptoms", "body_part": "Face/Throat", "is_red_flag": True, "default_weight": 10.0, "synonyms": "angioedema,lip swelling,tongue swelling,allergic suffocation"},

    # Musculoskeletal
    {"code": "JOINT_PAIN", "name": "Joint pain", "category": "Musculoskeletal symptoms", "body_part": "Joints", "is_red_flag": False, "default_weight": 2.2, "synonyms": "arthralgia,knee pain,shoulder pain,wrist pain"},
    {"code": "JOINT_SWELL", "name": "Joint swelling and warmth", "category": "Musculoskeletal symptoms", "body_part": "Joints", "is_red_flag": False, "default_weight": 2.5, "synonyms": "swollen knee,swollen joint,inflammation in joint"},
    {"code": "BACK_PAIN", "name": "Back pain", "category": "Musculoskeletal symptoms", "body_part": "Back", "is_red_flag": False, "default_weight": 2.0, "synonyms": "lower back pain,lumbago,spinal ache,lumbar strain"},
    {"code": "MUSCLE_STIFF", "name": "Muscle stiffness", "category": "Musculoskeletal symptoms", "body_part": "Muscles", "is_red_flag": False, "default_weight": 1.5, "synonyms": "stiff muscles,muscle tightness,cramps"},

    # ENT
    {"code": "RUNNY_NOSE", "name": "Runny nose or nasal discharge", "category": "ENT symptoms", "body_part": "Nose", "is_red_flag": False, "default_weight": 1.8, "synonyms": "rhinorrhea,sneezing,cold discharge"},
    {"code": "NASAL_BLOCK", "name": "Nasal congestion or blockage", "category": "ENT symptoms", "body_part": "Nose", "is_red_flag": False, "default_weight": 1.8, "synonyms": "blocked nose,stuffy nose,sinus block"},
    {"code": "EAR_PAIN", "name": "Earache", "category": "ENT symptoms", "body_part": "Ears", "is_red_flag": False, "default_weight": 2.0, "synonyms": "ear pain,pain in ear,otalgia"},
    {"code": "SINUS_PRESS", "name": "Facial or sinus pressure around eyes", "category": "ENT symptoms", "body_part": "Face/Sinuses", "is_red_flag": False, "default_weight": 2.0, "synonyms": "sinus headache,pressure over forehead and cheeks"},

    # Urinary
    {"code": "PAIN_URINE", "name": "Burning or painful urination", "category": "Urinary symptoms", "body_part": "Urinary Tract", "is_red_flag": False, "default_weight": 2.5, "synonyms": "dysuria,burning urine,pain when passing urine"},
    {"code": "FREQ_URINE", "name": "Frequent urination", "category": "Urinary symptoms", "body_part": "Bladder", "is_red_flag": False, "default_weight": 2.0, "synonyms": "pollakiuria,running to toilet frequently"},
    {"code": "FLANK_PAIN", "name": "Lower back flank pain", "category": "Urinary symptoms", "body_part": "Flank/Kidneys", "is_red_flag": False, "default_weight": 2.5, "synonyms": "kidney pain,side pain near ribs"}
]

# Structured Conditions Catalogue
CONDITIONS_DATA = [
    {
        "code": "COND_TENSION_HA",
        "name": "Tension-Type Headache",
        "category": "Neurological / General",
        "urgency_level": "Self-Care / Routine",
        "specialty_name": "General Physician",
        "description": "Common, dull, band-like headache typically brought on by stress, mental fatigue, dehydration, lack of sleep, or prolonged screen time.",
        "general_explanation": "A tension headache feels like a tight band wrapped around the head. It is usually mild to moderate, does not worsen with routine physical activity, and lacks alarming features like vomiting or visual aura.",
        "when_to_seek_care": "Consult a primary doctor if headaches become daily, progressively worse, or do not respond to rest and hydration.",
        "symptoms": [
            {"code": "HEADACHE", "weight": 4.0, "mandatory": True},
            {"code": "FAT", "weight": 2.0, "mandatory": False},
            {"code": "MUSCLE_STIFF", "weight": 1.5, "mandatory": False}
        ]
    },
    {
        "code": "COND_DEHYDRATION",
        "name": "Dehydration & Physical Fatigue",
        "category": "General",
        "urgency_level": "Self-Care",
        "specialty_name": "General Physician",
        "description": "Fluid deficit frequently encountered in warm tropical climates like Chennai, causing mild head discomfort and lethargy.",
        "general_explanation": "Insufficient water intake leads to decreased blood volume and temporary intracranial fluid shifts, producing dull head pain, dry lips, and lightheadedness.",
        "when_to_seek_care": "Seek medical attention if accompanied by inability to keep liquids down, high fever, or severe dizziness upon standing.",
        "symptoms": [
            {"code": "HEADACHE", "weight": 3.0, "mandatory": True},
            {"code": "FAT", "weight": 3.0, "mandatory": False},
            {"code": "DIZZ", "weight": 2.5, "mandatory": False},
            {"code": "WEAK", "weight": 2.0, "mandatory": False}
        ]
    },
    {
        "code": "COND_MIGRAINE",
        "name": "Migraine Headache",
        "category": "Neurological",
        "urgency_level": "Routine Consultation",
        "specialty_name": "Neurologist",
        "description": "Recurrent, pulsating, usually unilateral moderate-to-severe headache often accompanied by nausea and sensitivity to light or sound.",
        "general_explanation": "Migraine is a neurovascular condition characterized by episodic throbbing pain, sensory sensitivities, and sometimes visual disturbances (aura).",
        "when_to_seek_care": "See a neurologist for accurate preventive management, especially if headaches occur frequently or disrupt daily life.",
        "symptoms": [
            {"code": "HEADACHE", "weight": 4.5, "mandatory": True},
            {"code": "NAUSEA", "weight": 3.0, "mandatory": False},
            {"code": "VIS_CHANGE", "weight": 2.5, "mandatory": False},
            {"code": "DIZZ", "weight": 1.5, "mandatory": False}
        ]
    },
    {
        "code": "COND_VIRAL_FEVER",
        "name": "Acute Viral Illness / Influenza-like Illness",
        "category": "Infectious / Primary Care",
        "urgency_level": "Routine Consultation",
        "specialty_name": "General Physician",
        "description": "Systemic viral infection causing acute onset fever, generalized myalgia, headache, and fatigue.",
        "general_explanation": "Common circulating seasonal viral infections stimulate the body's immune cytokines, resulting in elevated temperature, body aches, chills, and malaise.",
        "when_to_seek_care": "Visit a primary care physician if fever persists past 3 days, rises above 102°F, or is accompanied by persistent vomiting or rash.",
        "symptoms": [
            {"code": "FEV", "weight": 4.5, "mandatory": True},
            {"code": "HEADACHE", "weight": 3.0, "mandatory": False},
            {"code": "BOD_PAIN", "weight": 3.5, "mandatory": False},
            {"code": "FAT", "weight": 2.5, "mandatory": False},
            {"code": "CHL", "weight": 2.0, "mandatory": False}
        ]
    },
    {
        "code": "COND_URI_COLD",
        "name": "Upper Respiratory Tract Infection (Common Cold)",
        "category": "Respiratory / ENT",
        "urgency_level": "Self-Care / Routine",
        "specialty_name": "General Physician",
        "description": "Mild viral inflammation of the upper airways characterized by rhinorrhea, nasal blockage, sneezing, and sore throat.",
        "general_explanation": "Rhinovirus and similar agents infect the nasal mucosa and pharynx, producing congestion, clear drainage, mild throat discomfort, and low-grade fatigue.",
        "when_to_seek_care": "Seek evaluation if you experience persistent high fever, chest pain, wheezing, or symptoms lasting longer than 10 days.",
        "symptoms": [
            {"code": "RUNNY_NOSE", "weight": 3.5, "mandatory": False},
            {"code": "NASAL_BLOCK", "weight": 3.5, "mandatory": False},
            {"code": "SORE_THROAT", "weight": 3.0, "mandatory": False},
            {"code": "COUGH", "weight": 2.5, "mandatory": False},
            {"code": "HEADACHE", "weight": 1.5, "mandatory": False}
        ]
    },
    {
        "code": "COND_ACUTE_SINUSITIS",
        "name": "Acute Sinusitis",
        "category": "ENT",
        "urgency_level": "Routine Consultation",
        "specialty_name": "ENT Specialist",
        "description": "Inflammation or secondary infection of the paranasal sinus cavities causing facial pressure and nasal obstruction.",
        "general_explanation": "Swelling blocks normal sinus drainage passages, creating pressure over the forehead, maxillary cheeks, and bridge of the nose, often worse when bending forward.",
        "when_to_seek_care": "Consult an ENT specialist if facial swelling, severe one-sided pain, high fever, or vision changes occur.",
        "symptoms": [
            {"code": "SINUS_PRESS", "weight": 4.5, "mandatory": True},
            {"code": "HEADACHE", "weight": 3.0, "mandatory": False},
            {"code": "NASAL_BLOCK", "weight": 3.0, "mandatory": False},
            {"code": "RUNNY_NOSE", "weight": 2.0, "mandatory": False},
            {"code": "FEV", "weight": 1.5, "mandatory": False}
        ]
    },
    {
        "code": "COND_GASTROENTERITIS",
        "name": "Acute Gastroenteritis (Food Poisoning / Stomach Flu)",
        "category": "Digestive",
        "urgency_level": "Routine Consultation",
        "specialty_name": "General Physician",
        "description": "Acute intestinal inflammation commonly resulting from dietary indiscretion or microbial ingestion.",
        "general_explanation": "Irritation of the mucosal lining of the stomach and intestines leads to rapid peristalsis, abdominal cramps, nausea, vomiting, and watery stools.",
        "when_to_seek_care": "Seek clinical evaluation promptly if unable to retain fluids for 24 hours, noticing blood in stool, or showing signs of severe dehydration.",
        "symptoms": [
            {"code": "STOM_PAIN", "weight": 3.5, "mandatory": False},
            {"code": "VOMIT", "weight": 4.0, "mandatory": False},
            {"code": "DIARRHEA", "weight": 4.0, "mandatory": False},
            {"code": "NAUSEA", "weight": 2.5, "mandatory": False},
            {"code": "FEV", "weight": 1.5, "mandatory": False}
        ]
    },
    {
        "code": "COND_GERD",
        "name": "Gastroesophageal Reflux Disease (GERD / Acid Reflux)",
        "category": "Digestive",
        "urgency_level": "Routine Consultation",
        "specialty_name": "Gastroenterologist",
        "description": "Reflux of acidic gastric contents upward into the esophagus causing retrosternal burning and sour taste.",
        "general_explanation": "Weakness in the lower esophageal sphincter allows digestive acid to irritate the esophageal lining, typically worse after heavy, oily, or spicy meals and when lying down.",
        "when_to_seek_care": "Consult a gastroenterologist if heartburn is persistent, causes difficulty swallowing, or fails to respond to antacids.",
        "symptoms": [
            {"code": "ACID_REFLUX", "weight": 4.5, "mandatory": True},
            {"code": "BLOAT", "weight": 2.5, "mandatory": False},
            {"code": "CHEST_DISCOMFORT", "weight": 2.5, "mandatory": False},
            {"code": "NAUSEA", "weight": 2.0, "mandatory": False}
        ]
    },
    {
        "code": "COND_ARTHRITIS_SPRAIN",
        "name": "Joint Inflammation / Musculoskeletal Strain",
        "category": "Musculoskeletal",
        "urgency_level": "Routine Consultation",
        "specialty_name": "Orthopedic Specialist",
        "description": "Acute or chronic articular inflammation or ligamentous strain causing localized joint pain, stiffness, and swelling.",
        "general_explanation": "Mechanical overuse, trauma, or localized inflammatory response within the joint capsule produces tenderness, periarticular effusion, and restricted range of motion.",
        "when_to_seek_care": "Consult an orthopedic specialist if unable to bear weight, if the joint appears deformed, or if joint warmth and high fever co-occur.",
        "symptoms": [
            {"code": "JOINT_PAIN", "weight": 4.5, "mandatory": True},
            {"code": "JOINT_SWELL", "weight": 3.5, "mandatory": False},
            {"code": "MUSCLE_STIFF", "weight": 2.5, "mandatory": False}
        ]
    },
    {
        "code": "COND_LUMBAR_STRAIN",
        "name": "Mechanical Lumbar Back Strain",
        "category": "Musculoskeletal",
        "urgency_level": "Routine Consultation",
        "specialty_name": "Orthopedic Specialist",
        "description": "Soft tissue injury or postural strain affecting the paraspinal muscles and ligaments of the lower back.",
        "general_explanation": "Lifting heavy objects, prolonged sedentary sitting, or sudden twisting can stretch spinal ligaments and muscle fibers, triggering painful muscle spasms.",
        "when_to_seek_care": "Seek prompt medical care if back pain radiates down past the knee, causes leg numbness, or is associated with bowel/bladder dysfunction.",
        "symptoms": [
            {"code": "BACK_PAIN", "weight": 4.5, "mandatory": True},
            {"code": "MUSCLE_STIFF", "weight": 3.0, "mandatory": False}
        ]
    },
    {
        "code": "COND_UTI",
        "name": "Urinary Tract Infection (Cystitis)",
        "category": "Urinary",
        "urgency_level": "Routine Consultation",
        "specialty_name": "Urologist",
        "description": "Bacterial proliferation in the urinary bladder or urethra causing irritative voiding symptoms.",
        "general_explanation": "Uropathogenic bacteria cause inflammatory irritation of the urothelium, leading to sharp burning sensations during micturition and bladder urgency.",
        "when_to_seek_care": "Promptly visit a doctor for urinalysis and targeted antibiotics; immediate care is needed if flank back pain and high fevers with chills develop.",
        "symptoms": [
            {"code": "PAIN_URINE", "weight": 4.5, "mandatory": True},
            {"code": "FREQ_URINE", "weight": 3.5, "mandatory": False},
            {"code": "FEV", "weight": 2.0, "mandatory": False},
            {"code": "FLANK_PAIN", "weight": 2.0, "mandatory": False}
        ]
    },
    {
        "code": "COND_ASTHMA_BRONCHITIS",
        "name": "Bronchial Asthma / Bronchitis",
        "category": "Pulmonary",
        "urgency_level": "Routine / Urgent",
        "specialty_name": "Pulmonologist",
        "description": "Hyperreactive airway constriction and mucous hypersecretion causing episodic wheezing, chest tightness, and cough.",
        "general_explanation": "Allergens, pollution, or viral triggers induce bronchial smooth muscle spasm and inflammation, narrowing the respiratory lumens.",
        "when_to_seek_care": "Consult a pulmonologist for long-term inhaler optimization; seek immediate emergency care if severe breathlessness or bluish discoloration occurs.",
        "symptoms": [
            {"code": "WHEEZE", "weight": 4.5, "mandatory": True},
            {"code": "COUGH", "weight": 3.5, "mandatory": False},
            {"code": "SHORT_BREATH", "weight": 3.5, "mandatory": False},
            {"code": "CHEST_CONGEST", "weight": 2.5, "mandatory": False}
        ]
    },
    {
        "code": "COND_ALLERGIC_DERM",
        "name": "Allergic Dermatitis / Urticaria (Hives)",
        "category": "Dermatology",
        "urgency_level": "Routine Consultation",
        "specialty_name": "Dermatologist",
        "description": "Histamine-mediated cutaneous hypersensitivity reaction presenting with pruritic erythematous papules or wheals.",
        "general_explanation": "Exposure to contact irritants, food triggers, or environmental allergens prompts cutaneous mast cells to release histamine, producing localized swelling and intense itching.",
        "when_to_seek_care": "Seek emergency medical care immediately if hives are accompanied by lip or tongue swelling, or throat tightness.",
        "symptoms": [
            {"code": "ITCH", "weight": 4.0, "mandatory": True},
            {"code": "SKIN_RASH", "weight": 3.5, "mandatory": False},
            {"code": "HIVES", "weight": 3.5, "mandatory": False}
        ]
    },
    # Red Flag Emergency Conditions
    {
        "code": "COND_ACUTE_STROKE",
        "name": "Possible Acute Cerebrovascular Event (Stroke Warning)",
        "category": "Neurological / Emergency",
        "urgency_level": "Emergency (Dial 112)",
        "specialty_name": "Neurologist",
        "description": "CRITICAL EMERGENCY: Acute disruption of cerebral blood flow requiring immediate thrombolytic or endovascular evaluation.",
        "general_explanation": "Sudden onset focal neurological signs such as unilateral arm weakness, facial asymmetry, or speech disruption indicate a potential ischemic or hemorrhagic stroke. Time is brain.",
        "when_to_seek_care": "IMMEDIATE EMERGENCY: Call emergency services (112 in India) or proceed immediately to the nearest hospital emergency department with CT/MRI facilities.",
        "symptoms": [
            {"code": "SUD_WEAK", "weight": 10.0, "mandatory": True},
            {"code": "FACE_DROP", "weight": 9.0, "mandatory": False},
            {"code": "SPEECH_DIFF", "weight": 9.0, "mandatory": False}
        ]
    },
    {
        "code": "COND_ACS_CARDIAC",
        "name": "Possible Acute Coronary Syndrome (Cardiac Warning)",
        "category": "Cardiovascular / Emergency",
        "urgency_level": "Emergency (Dial 112)",
        "specialty_name": "Cardiologist",
        "description": "CRITICAL EMERGENCY: Severe retrosternal chest pain or pressure suggesting acute myocardial ischemia or infarction.",
        "general_explanation": "Crushing, squeezing chest discomfort that radiates to the left arm, shoulder, or jaw, especially when associated with sweating or shortness of breath, warrants urgent ECG evaluation.",
        "when_to_seek_care": "IMMEDIATE EMERGENCY: Dial 112 or visit the nearest cardiac emergency room immediately. Do not drive yourself.",
        "symptoms": [
            {"code": "CHEST_PAIN_SEV", "weight": 10.0, "mandatory": True},
            {"code": "SHORT_BREATH", "weight": 4.0, "mandatory": False},
            {"code": "PALP", "weight": 3.0, "mandatory": False}
        ]
    },
    {
        "code": "COND_ANAPHYLAXIS",
        "name": "Severe Allergic Anaphylaxis Warning",
        "category": "Emergency / Allergy",
        "urgency_level": "Emergency (Dial 112)",
        "specialty_name": "General Physician",
        "description": "CRITICAL EMERGENCY: Rapidly progressing systemic allergic reaction with potential airway compromise.",
        "general_explanation": "Facial, lip, or tongue angioedema paired with breathing difficulty or extensive hives signifies life-threatening anaphylaxis requiring immediate intramuscular epinephrine.",
        "when_to_seek_care": "IMMEDIATE EMERGENCY: Dial 112 or visit the nearest emergency facility without delay.",
        "symptoms": [
            {"code": "ANAPHYLAXIS_SWELL", "weight": 10.0, "mandatory": True},
            {"code": "SEV_BREATH_DIFF", "weight": 8.0, "mandatory": False},
            {"code": "HIVES", "weight": 4.0, "mandatory": False}
        ]
    }
]

# Dynamic Follow-up Question Bank (Module 3 requirement)
FOLLOW_UP_QUESTIONS_BANK = {
    "HEADACHE": [
        {
            "id": "ha_loc",
            "question": "Where is the headache primarily located?",
            "options": ["Forehead and temples (band-like)", "One side of the head (throbbing)", "Behind the eyes and cheekbones", "All over the entire head"],
            "clinical_significance": "Differentiates tension headache, migraine, and sinus pressure."
        },
        {
            "id": "ha_onset",
            "question": "Did this headache start suddenly like an explosion, or did it build up gradually?",
            "options": ["Built up gradually over hours/days", "Sudden explosive onset within seconds"],
            "clinical_significance": "Sudden thunderclap onset is a red flag requiring emergency evaluation."
        },
        {
            "id": "ha_associated",
            "question": "Are you experiencing any nausea, sensitivity to light, or visual changes?",
            "options": ["No nausea or visual changes", "Mild nausea and sensitivity to bright light", "Visual aura (flashes, blind spots)"],
            "clinical_significance": "Assesses classic migraine characteristics."
        }
    ],
    "STOM_PAIN": [
        {
            "id": "st_loc",
            "question": "Which specific area of your abdomen hurts the most?",
            "options": ["Upper abdomen / just below breastbone", "Lower abdomen / pelvic area", "Right lower side (near hip)", "All over / generalized cramping"],
            "clinical_significance": "Distinguishes acid gastritis, appendicitis warning, and bowel cramping."
        },
        {
            "id": "st_assoc",
            "question": "Are you also experiencing vomiting, diarrhea, or fever?",
            "options": ["No vomiting or diarrhea", "Vomiting only", "Watery diarrhea with cramps", "Both vomiting and diarrhea with fever"],
            "clinical_significance": "Identifies acute gastroenteritis versus localized pathology."
        }
    ],
    "CHEST_DISCOMFORT": [
        {
            "id": "ch_char",
            "question": "How would you describe the chest sensation?",
            "options": ["Burning sensation after eating (acid reflux)", "Sharp ache worse when taking a deep breath", "Heavy, tight squeezing pressure that radiates to arm"],
            "clinical_significance": "Crucial discriminator between reflux, musculoskeletal chest pain, and cardiac signs."
        }
    ],
    "JOINT_PAIN": [
        {
            "id": "jt_loc",
            "question": "Which joints are affected, and is there visible swelling or redness?",
            "options": ["Single joint with swelling and warmth", "Multiple joints (both hands/knees) with morning stiffness", "Spinal/neck joints following heavy lifting"],
            "clinical_significance": "Differentiates trauma, inflammatory arthritis, and mechanical strain."
        }
    ],
    "FEV": [
        {
            "id": "fev_dur",
            "question": "How many days have you had the fever, and is it continuous or spiking with chills?",
            "options": ["1-2 days, mild elevation", "3-5 days with body chills", "More than 7 days"],
            "clinical_significance": "Determines viral self-limiting course versus prolonged bacterial investigation."
        }
    ]
}

# Propositional and First-Order Logic Rules (Unit IV)
LOGICAL_RULES = [
    {
        "code": "RULE_STROKE_FAST",
        "rule_type": "propositional_red_flag",
        "antecedent": {"or": ["SUD_WEAK", "FACE_DROP", "SPEECH_DIFF"]},
        "consequent": {"action": "EMERGENCY_OVERRIDE", "alert": "FAST Stroke warning criteria met. Immediate emergency medical intervention required."},
        "weight": 10.0,
        "description": "Propositional Rule: IF Sudden Weakness OR Facial Droop OR Speech Difficulty THEN Trigger Emergency 112 Alert."
    },
    {
        "code": "RULE_CARDIAC_RED_FLAG",
        "rule_type": "propositional_red_flag",
        "antecedent": {"or": ["CHEST_PAIN_SEV"]},
        "consequent": {"action": "EMERGENCY_OVERRIDE", "alert": "Severe chest/heart pain detected. Suspected Acute Coronary Syndrome. Immediate 112 alert."},
        "weight": 10.0,
        "description": "Propositional Rule: IF Severe Chest/Heart Pain THEN Immediate Emergency Override."
    },
    {
        "code": "RULE_CARDIAC_COMBO_ROUTE",
        "rule_type": "propositional_red_flag",
        "antecedent": {"and": ["CHEST_DISCOMFORT", "SHORT_BREATH"]},
        "consequent": {"action": "EMERGENCY_OVERRIDE", "alert": "Chest/heart discomfort paired with breathing difficulty detected. Urgent Cardiology/Emergency evaluation advised."},
        "weight": 9.5,
        "description": "Clinical Rule: IF Chest Discomfort AND Shortness of Breath THEN Route to Cardiologist / Urgent Triage."
    },
    {
        "code": "RULE_CARDIAC_PALP_ROUTE",
        "rule_type": "specialty_route",
        "antecedent": {"or": ["CHEST_PAIN_SEV", "CHEST_DISCOMFORT", "PALP"]},
        "consequent": {"specialty": "Cardiologist", "match_score": 96},
        "weight": 5.0,
        "description": "Specialist Routing: Any prominent chest pain, heart pain, or palpitations routes to Cardiologist."
    },
    {
        "code": "RULE_ANAPHYLAXIS_ALERT",
        "rule_type": "propositional_red_flag",
        "antecedent": {"or": ["ANAPHYLAXIS_SWELL", "SEV_BREATH_DIFF"]},
        "consequent": {"action": "EMERGENCY_OVERRIDE", "alert": "Severe airway/facial compromise warning. Immediate emergency care required."},
        "weight": 10.0,
        "description": "Propositional Rule: IF Facial Angioedema OR Severe Airway Compromise THEN Trigger Anaphylaxis Emergency."
    },
    {
        "code": "RULE_HEADACHE_NONSPECIFIC",
        "rule_type": "forward_chain_prune",
        "antecedent": {"exact_single": "HEADACHE"},
        "consequent": {"limit_candidates": ["COND_TENSION_HA", "COND_DEHYDRATION", "COND_MIGRAINE"], "prevent_alarmist": True},
        "weight": 5.0,
        "description": "Safe Clinical Rule: An isolated single symptom of headache must NOT trigger brain tumor or stroke predictions; prioritize tension, dehydration, and migraine."
    },
    {
        "code": "RULE_VIRAL_TRIAD",
        "rule_type": "forward_chain",
        "antecedent": {"and": ["FEV", "HEADACHE", "BOD_PAIN"]},
        "consequent": {"boost_candidate": "COND_VIRAL_FEVER", "specialty": "General Physician"},
        "weight": 4.5,
        "description": "Forward Chaining: Fever + Headache + Generalized Body Pain strongly infers Acute Viral Syndrome; route to General Physician."
    },
    {
        "code": "RULE_JOINT_SWELL_ROUTE",
        "rule_type": "specialty_route",
        "antecedent": {"and": ["JOINT_PAIN", "JOINT_SWELL"]},
        "consequent": {"specialty": "Orthopedic Specialist", "match_score": 90},
        "weight": 4.0,
        "description": "Specialist Routing: Persistent Joint Pain with visible Swelling routes to Orthopedic Specialist or Primary Rheumatology triage."
    }
]
