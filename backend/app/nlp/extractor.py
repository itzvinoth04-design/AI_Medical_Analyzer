import re
from typing import Dict, List, Any
from app.knowledge_base.medical_ontology import SYMPTOMS_DATA

class NLPEntityExtractor:
    """
    Intelligent NLP Engine for Clinical Symptom Extraction (Unit V - NLP).
    Extracts:
    - Symptoms & Synonyms
    - Negations (e.g., 'no fever', 'denies chest pain')
    - Body parts affected
    - Duration (e.g., 'for 2 days', 'since yesterday')
    - Severity indicators ('mild', 'moderate', 'severe')
    - Frequency ('intermittent', 'constant', 'comes and goes')
    - Chief complaint
    - Vagueness detection for dynamic follow-ups
    """

    NEGATION_WORDS = {
        "no", "not", "neither", "nor", "without", "denies", "denied",
        "haven't", "hasn't", "hadn't", "dont", "don't", "never", "free of"
    }

    SEVERITY_MAP = {
        "mild": ["mild", "slight", "minor", "low-grade", "dull", "bearable"],
        "moderate": ["moderate", "medium", "noticeable", "uncomfortable"],
        "severe": ["severe", "extreme", "intense", "sharp", "excruciating", "unbearable", "terrible", "worst", "heavy", "crushing"]
    }

    FREQUENCY_PATTERNS = [
        "constant", "continuous", "all day", "intermittent", "comes and goes",
        "occasionally", "frequent", "frequently", "spiking", "episodic"
    ]

    BODY_PARTS = {
        "head": ["head", "forehead", "temple", "temples", "scalp"],
        "chest": ["chest", "ribs", "breastbone", "heart", "sternum"],
        "abdomen": ["stomach", "abdomen", "belly", "tummy", "gut"],
        "throat": ["throat", "pharynx", "tonsils"],
        "neck": ["neck", "cervical"],
        "back": ["back", "lower back", "spine", "lumbar"],
        "joints": ["joint", "joints", "knee", "knees", "elbow", "wrist", "shoulder", "ankle"],
        "skin": ["skin", "face", "body", "arms", "legs"],
        "ears": ["ear", "ears"],
        "eyes": ["eye", "eyes", "vision"],
        "nose": ["nose", "nasal", "sinus", "sinuses"]
    }

    def __init__(self):
        # Build symptom lexicon lookup
        self.symptom_lexicon = {}
        for s in SYMPTOMS_DATA:
            code = s["code"]
            # Primary name
            self.symptom_lexicon[s["name"].lower()] = code
            # Synonyms
            if s.get("synonyms"):
                syns = [syn.strip().lower() for syn in s["synonyms"].split(",")]
                for syn in syns:
                    if syn:
                        self.symptom_lexicon[syn] = code

    def parse_text(self, text: str) -> Dict[str, Any]:
        if not text or not text.strip():
            return {
                "raw_text": "",
                "extracted_symptoms": [],
                "negated_symptoms": [],
                "duration_days": 1,
                "duration_raw": "Not specified",
                "severity": "Moderate",
                "frequency": "Unspecified",
                "body_parts": [],
                "chief_complaint": None,
                "is_vague": True,
                "vagueness_reason": "No text provided"
            }

        text_lower = text.lower()
        # Phonetic & colloquial spelling normalization for clinical input
        text_lower = re.sub(r"\bbreeth\b", "breath", text_lower)
        text_lower = re.sub(r"\bbreth\b", "breath", text_lower)
        text_lower = re.sub(r"\bharth\b", "heart", text_lower)
        text_lower = re.sub(r"\bhart\b", "heart", text_lower)
        text_lower = re.sub(r"\bstomack\b", "stomach", text_lower)
        text_lower = re.sub(r"\bstomache\b", "stomach", text_lower)
        text_lower = re.sub(r"\bhedache\b", "headache", text_lower)
        text_lower = re.sub(r"\bheadacke\b", "headache", text_lower)
        text_lower = re.sub(r"\bfeever\b", "fever", text_lower)

        words = re.findall(r"\b[\w'-]+\b", text_lower)

        # 1. Extract Duration
        duration_days, duration_raw = self._extract_duration(text_lower)

        # 2. Extract Severity
        severity = self._extract_severity(text_lower)

        # 3. Extract Frequency
        frequency = self._extract_frequency(text_lower)

        # 4. Extract Body Parts
        body_parts = self._extract_body_parts(text_lower)

        # 5. Extract Symptoms and Negation Scope
        extracted_symptoms = []
        negated_symptoms = []

        # Find occurrences of symptom phrases in text
        # Sort lexicon phrases by length descending to match longest phrases first (e.g. "sudden one-sided weakness" before "weakness")
        sorted_phrases = sorted(self.symptom_lexicon.keys(), key=lambda x: len(x), reverse=True)
        matched_spans = []

        for phrase in sorted_phrases:
            pattern = r"\b" + re.escape(phrase) + r"\b"
            for match in re.finditer(pattern, text_lower):
                start, end = match.span()
                # Check for overlap with already matched span
                overlap = any(s <= start < e or s < end <= e for s, e in matched_spans)
                if not overlap:
                    matched_spans.append((start, end))
                    code = self.symptom_lexicon[phrase]
                    # Check negation in preceding 4 words
                    is_negated = self._is_negated_in_context(text_lower, start)
                    
                    symptom_info = next((s for s in SYMPTOMS_DATA if s["code"] == code), None)
                    s_name = symptom_info["name"] if symptom_info else phrase.title()
                    category = symptom_info["category"] if symptom_info else "General"
                    is_red_flag = symptom_info["is_red_flag"] if symptom_info else False

                    entry = {
                        "code": code,
                        "name": s_name,
                        "category": category,
                        "is_red_flag": is_red_flag,
                        "matched_text": phrase,
                        "severity": severity
                    }

                    if is_negated:
                        if not any(ns["code"] == code for ns in negated_symptoms):
                            negated_symptoms.append(entry)
                    else:
                        if not any(es["code"] == code for es in extracted_symptoms):
                            extracted_symptoms.append(entry)

        # 6. Determine Chief Complaint
        chief_complaint = None
        if extracted_symptoms:
            # Prefer red flag or first extracted symptom
            red_flags = [s for s in extracted_symptoms if s.get("is_red_flag")]
            chief_complaint = red_flags[0]["name"] if red_flags else extracted_symptoms[0]["name"]

        # 7. Evaluate Vagueness
        is_vague, vagueness_reason = self._assess_vagueness(extracted_symptoms, words)

        return {
            "raw_text": text,
            "extracted_symptoms": extracted_symptoms,
            "negated_symptoms": negated_symptoms,
            "duration_days": duration_days,
            "duration_raw": duration_raw,
            "severity": severity,
            "frequency": frequency,
            "body_parts": body_parts,
            "chief_complaint": chief_complaint,
            "is_vague": is_vague,
            "vagueness_reason": vagueness_reason
        }

    def _is_negated_in_context(self, text: str, match_start: int) -> bool:
        # Inspect up to 35 characters preceding the match
        window_start = max(0, match_start - 35)
        preceding_text = text[window_start:match_start]
        # Remove punctuation except negation apostrophes
        cleaned_words = re.findall(r"\b[\w'-]+\b", preceding_text)
        # Check last 3 words
        last_three = cleaned_words[-3:] if len(cleaned_words) >= 3 else cleaned_words
        return any(w in self.NEGATION_WORDS for w in last_three)

    def _extract_duration(self, text: str) -> (int, str):
        # Patterns like: "2 days", "two days", "since yesterday", "3 weeks", "48 hours", "a week", "1 month"
        number_map = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
            "seven": 7, "eight": 8, "nine": 9, "ten": 10, "a": 1, "an": 1
        }

        # Check for 'since yesterday'
        if "since yesterday" in text or "from yesterday" in text:
            return 1, "1 day (since yesterday)"
        if "today" in text or "since morning" in text or "few hours" in text:
            return 1, "Less than 24 hours"

        # Regex for (number/word) + (hours/days/weeks/months)
        match = re.search(r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten|a|an)\s+(hour|hours|day|days|week|weeks|month|months)", text)
        if match:
            num_raw, unit = match.group(1), match.group(2)
            num = int(num_raw) if num_raw.isdigit() else number_map.get(num_raw, 1)
            raw_str = f"{num} {unit}"
            if "hour" in unit:
                return max(1, round(num / 24)), raw_str
            elif "day" in unit:
                return num, raw_str
            elif "week" in unit:
                return num * 7, raw_str
            elif "month" in unit:
                return num * 30, raw_str

        return 2, "2 days (standard default)"

    def _extract_severity(self, text: str) -> str:
        for sev, terms in self.SEVERITY_MAP.items():
            for t in terms:
                if re.search(r"\b" + re.escape(t) + r"\b", text):
                    return sev.capitalize()
        return "Moderate"

    def _extract_frequency(self, text: str) -> str:
        for f in self.FREQUENCY_PATTERNS:
            if f in text:
                return f.capitalize()
        return "Continuous"

    def _extract_body_parts(self, text: str) -> List[str]:
        found = []
        for bp, terms in self.BODY_PARTS.items():
            if any(re.search(r"\b" + re.escape(t) + r"\b", text) for t in terms):
                found.append(bp.capitalize())
        return found

    def _assess_vagueness(self, symptoms: List[Dict], words: List[str]) -> (bool, str):
        if not symptoms:
            return True, "No specific clinical symptoms identified from the description."
        if len(symptoms) == 1 and symptoms[0]["code"] in ["HEADACHE", "FAT", "WEAK", "STOM_PAIN", "BOD_PAIN"]:
            # Single non-specific symptom
            return True, f"Single nonspecific complaint ({symptoms[0]['name']}) requires follow-up detail to prevent misdiagnosis."
        if len(words) < 4:
            return True, "Description is very brief and provides minimal clinical context."
        return False, "Sufficient initial context provided."
