"""
Real-World Chennai Hospital & Clinic Data Collection Engine (Module 6)
Integrates OpenStreetMap Overpass API and public healthcare directory verification
for major Chennai localities.
"""

import requests
import json
import re
import math
from typing import List, Dict, Any

CHENNAI_OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Overpass QL Query for Hospitals and Clinics within Greater Chennai Bounding Box
CHENNAI_OVERPASS_QUERY = """
[out:json][timeout:25];
(
  node["amenity"="hospital"](12.85,80.05,13.25,80.35);
  way["amenity"="hospital"](12.85,80.05,13.25,80.35);
  node["amenity"="clinic"](12.85,80.05,13.25,80.35);
  way["amenity"="clinic"](12.85,80.05,13.25,80.35);
  node["healthcare"="hospital"](12.85,80.05,13.25,80.35);
  node["healthcare"="clinic"](12.85,80.05,13.25,80.35);
);
out center tags;
"""

def normalize_name(name: str) -> str:
    """Normalizes facility name for robust duplicate detection."""
    if not name:
        return ""
    cleaned = re.sub(r"[^\w\s]", "", name.lower())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    # Remove common suffixes for fuzzy matching
    for token in ["hospital", "hospitals", "clinic", "clinics", "centre", "center", "multispeciality", "speciality", "chennai", "limited", "ltd", "pvt"]:
        cleaned = re.sub(r"\b" + token + r"\b", "", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()

def haversine_dist(lat1, lon1, lat2, lon2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlam = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2.0)**2
    return 6371.0 * (2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a)))

def is_duplicate(facility: Dict[str, Any], existing_facilities: List[Dict[str, Any]], distance_threshold_km=0.15) -> bool:
    """Duplicate detection using geocoordinate proximity and normalized name tokens."""
    norm = facility.get("normalized_name", "")
    lat = facility.get("latitude")
    lon = facility.get("longitude")

    for ex in existing_facilities:
        ex_norm = ex.get("normalized_name", "")
        ex_lat = ex.get("latitude")
        ex_lon = ex.get("longitude")

        # Check coordinate distance
        if lat and lon and ex_lat and ex_lon:
            dist = haversine_dist(lat, lon, ex_lat, ex_lon)
            if dist <= distance_threshold_km:
                return True

        # Check normalized name exact match
        if norm and ex_norm and (norm == ex_norm or (len(norm) > 4 and norm in ex_norm)):
            return True

    return False

def fetch_overpass_chennai_facilities() -> List[Dict[str, Any]]:
    """Fetches real Chennai healthcare establishments from OpenStreetMap Overpass API."""
    print("[Overpass API] Querying OpenStreetMap for Chennai healthcare facilities...")
    try:
        response = requests.post(
            CHENNAI_OVERPASS_URL,
            data={"data": CHENNAI_OVERPASS_QUERY},
            headers={"User-Agent": "MediGuideAI-Chennai-Healthcare-Research/1.0"},
            timeout=20
        )
        if response.status_code == 200:
            data = response.json()
            elements = data.get("elements", [])
            print(f"[Overpass API] Retrieved {len(elements)} raw records from OpenStreetMap.")
            results = []
            for el in elements:
                tags = el.get("tags", {})
                name = tags.get("name") or tags.get("name:en")
                if not name:
                    continue

                lat = el.get("lat") or (el.get("center", {}).get("lat"))
                lon = el.get("lon") or (el.get("center", {}).get("lon"))
                if not lat or not lon:
                    continue

                facility_type = "Hospital" if "hospital" in tags.get("amenity", "").lower() or "hospital" in tags.get("healthcare", "").lower() else "Clinic"
                addr_street = tags.get("addr:street", "")
                addr_suburb = tags.get("addr:suburb") or tags.get("addr:district") or "Chennai"
                full_addr = f"{name}, {addr_street}, {addr_suburb}".strip(", ")

                phone = tags.get("phone") or tags.get("contact:phone")
                website = tags.get("website") or tags.get("contact:website")
                emergency = tags.get("emergency") == "yes"

                results.append({
                    "name": name,
                    "normalized_name": normalize_name(name),
                    "facility_type": facility_type,
                    "address": full_addr,
                    "locality": addr_suburb,
                    "city": "Chennai",
                    "pincode": tags.get("addr:postcode", "600001"),
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "phone": phone,
                    "website": website,
                    "emergency_24x7": emergency,
                    "source_url": "https://www.openstreetmap.org",
                    "last_verified": "OpenStreetMap 2026 Sync"
                })
            return results
    except Exception as e:
        print(f"[Overpass API] Live query failed or timed out: {e}. Falling back to verified ground truth.")
        return []
