import os
import sys
from pathlib import Path

# Ensure backend root is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"================================================================")
    print(f" MediGuide AI - Medical Symptom Analyzer & Doctor Recommendation")
    print(f" Intelligent Clinical Triage Decision-Support Platform")
    print(f" Backend REST API running at http://localhost:{port}")
    print(f" Database: SQLITE#.db")
    print(f"================================================================")
    app.run(host="0.0.0.0", port=port, debug=True)
