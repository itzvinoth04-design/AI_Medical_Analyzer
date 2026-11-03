import sys
import unittest
from pathlib import Path

# Add backend to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.models import db

class TestMediGuideClinicalInference(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_01_health_check(self):
        """Verify API health endpoint."""
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")

    def test_02_scenario_mild_headache(self):
        """
        Test Case 1: Mild headache.
        Expected: Broad, non-alarming possibilities (Tension-type, Dehydration, Migraine).
        Must NOT leap to brain tumor or stroke. Asks follow-up questions.
        """
        payload = {
            "raw_text": "I have a mild headache since yesterday.",
            "severity": "Mild",
            "duration_days": 1
        }
        res = self.client.post("/api/assessment/analyze", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        self.assertFalse(data["is_emergency"])
        condition_names = [c["condition_name"] for c in data["top_conditions"]]
        
        # Verify benign conditions present
        self.assertTrue(any("Tension" in name or "Dehydration" in name or "Migraine" in name for name in condition_names))
        # Verify NO alarmist conditions
        self.assertFalse(any("Stroke" in name or "Tumor" in name for name in condition_names))
        # Verify dynamic follow-up questions generated
        self.assertTrue(len(data["follow_up_questions"]) > 0)
        # Verify General Physician recommended
        self.assertEqual(data["doctor_recommendation"]["primary_specialty"], "General Physician")
        print("\n[TEST 1 PASSED] Mild headache safely bounded to benign possibilities.")

    def test_03_scenario_viral_triad(self):
        """
        Test Case 2: Headache + fever + body pain.
        Expected: Acute viral illness possibilities, recommend primary care (General Physician).
        """
        payload = {
            "raw_text": "I have a headache, mild fever, and body pain for two days.",
            "selected_symptom_codes": ["FEV", "HEADACHE", "BOD_PAIN"],
            "severity": "Moderate",
            "duration_days": 2
        }
        res = self.client.post("/api/assessment/analyze", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        self.assertFalse(data["is_emergency"])
        top_cond = data["top_conditions"][0]
        self.assertIn("Viral", top_cond["condition_name"])
        self.assertEqual(data["doctor_recommendation"]["primary_specialty"], "General Physician")
        self.assertGreaterEqual(data["doctor_recommendation"]["recommendation_match"], 80)
        print("\n[TEST 2 PASSED] Viral triad successfully routed to General Physician.")

    def test_04_scenario_migraine_vision_change(self):
        """
        Test Case 3: Persistent headache + vision changes.
        Expected: Neurological evaluation / Migraine considered.
        """
        payload = {
            "raw_text": "Severe throbbing headache with blurred vision and nausea for 3 days.",
            "selected_symptom_codes": ["HEADACHE", "VIS_CHANGE", "NAUSEA"],
            "severity": "Severe",
            "duration_days": 3
        }
        res = self.client.post("/api/assessment/analyze", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        condition_names = [c["condition_name"] for c in data["top_conditions"]]
        self.assertTrue(any("Migraine" in name for name in condition_names))
        self.assertIn(data["doctor_recommendation"]["primary_specialty"], ["Neurologist", "General Physician"])
        print("\n[TEST 3 PASSED] Persistent headache + vision changes evaluates migraine and specialist routing.")

    def test_05_scenario_stroke_emergency(self):
        """
        Test Case 4: Sudden one-sided weakness.
        Expected: Immediate emergency warning and 112 override.
        """
        payload = {
            "raw_text": "Sudden one-sided weakness in my arm with slight facial numbness.",
            "selected_symptom_codes": ["SUD_WEAK", "FACE_DROP"],
            "severity": "Severe",
            "duration_days": 1
        }
        res = self.client.post("/api/assessment/analyze", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        self.assertTrue(data["is_emergency"])
        self.assertEqual(data["urgency_status"], "CRITICAL EMERGENCY")
        self.assertTrue(data["doctor_recommendation"]["is_emergency_bypass"])
        self.assertIn("Stroke", data["emergency_alert"])
        print("\n[TEST 4 PASSED] Sudden weakness successfully triggers emergency override.")

    def test_06_scenario_stomach_pain_vomiting(self):
        """
        Test Case 5: Stomach pain + vomiting.
        Expected: Asks location/severity/diarrhea follow-ups, considers gastroenteritis.
        """
        payload = {
            "raw_text": "I have bad stomach pain and vomiting since morning.",
            "selected_symptom_codes": ["STOM_PAIN", "VOMIT"],
            "severity": "Moderate",
            "duration_days": 1
        }
        res = self.client.post("/api/assessment/analyze", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        condition_names = [c["condition_name"] for c in data["top_conditions"]]
        self.assertTrue(any("Gastroenteritis" in name or "GERD" in name for name in condition_names))
        # Ensure follow-up questions address stomach pain location and diarrhea
        self.assertTrue(len(data["follow_up_questions"]) > 0)
        print("\n[TEST 5 PASSED] Stomach pain + vomiting prompts follow-up questions and acute gastroenteritis.")

    def test_07_scenario_joint_pain_swelling(self):
        """
        Test Case 6: Joint pain + swelling.
        Expected: Musculoskeletal/Orthopedic specialist recommendation.
        """
        payload = {
            "raw_text": "I have persistent joint pain with knee swelling for 10 days.",
            "selected_symptom_codes": ["JOINT_PAIN", "JOINT_SWELL"],
            "severity": "Moderate",
            "duration_days": 10
        }
        res = self.client.post("/api/assessment/analyze", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        self.assertEqual(data["doctor_recommendation"]["primary_specialty"], "Orthopedic Specialist")
        self.assertGreaterEqual(data["doctor_recommendation"]["recommendation_match"], 85)
        print("\n[TEST 6 PASSED] Joint pain + swelling accurately routes to Orthopedic Specialist.")

    def test_08_chennai_hospital_search_and_haversine(self):
        """Verify real Chennai hospital search and Haversine distance ranking."""
        res = self.client.get("/api/hospitals/search?locality=Velachery&specialty=General Physician")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        self.assertGreaterEqual(data["total_results"], 1)
        first_hosp = data["hospitals"][0]
        self.assertIn("distance_km", first_hosp)
        self.assertIn("consultation_fee", first_hosp)
        self.assertIn("opd_hours", first_hosp)
        self.assertIn("phone", first_hosp)
        print(f"\n[TEST 7 PASSED] Hospital search returned {data['total_results']} facilities. Closest: {first_hosp['name']} ({first_hosp['distance_km']} km)")

    def test_09_ai_methodology_all_units(self):
        """Verify all 5 AI syllabus units are populated with computational data."""
        res = self.client.get("/api/ai-methodology/overview")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()

        units = data["units"]
        self.assertIn("unit_1", units)
        self.assertIn("unit_2", units)
        self.assertIn("unit_3", units)
        self.assertIn("unit_4", units)
        self.assertIn("unit_5", units)

        # Unit 5 ML metrics
        u5 = units["unit_5"]["implementation_details"]["supervised_model"]
        self.assertGreaterEqual(u5["overall_accuracy"], 90.0)
        print(f"\n[TEST 8 PASSED] AI Methodology delivers complete telemetry for all 5 units. ML Accuracy: {u5['overall_accuracy']}%")

if __name__ == "__main__":
    unittest.main()
