import math
from typing import Tuple

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two geocoordinates using the Haversine formula (km).
    Formula:
      a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
      c = 2 * atan2(√a, √(1-a))
      d = R * c (where R = 6371 km)
    """
    R = 6371.0  # Earth's radius in kilometers

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)

    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    distance = R * c
    return round(distance, 2)

# Central anchor coordinates for prominent Chennai localities
CHENNAI_LOCALITY_COORDINATES = {
    "T. Nagar": (13.0418, 80.2341),
    "Adyar": (13.0012, 80.2565),
    "Velachery": (12.9759, 80.2212),
    "Anna Nagar": (13.0850, 80.2101),
    "Tambaram": (12.9249, 80.1000),
    "Porur": (13.0382, 80.1565),
    "Guindy": (13.0067, 80.2025),
    "Nungambakkam": (13.0569, 80.2425),
    "Chromepet": (12.9516, 80.1462),
    "OMR (Old Mahabalipuram Road)": (12.9345, 80.2312),
    "Perungudi": (12.9654, 80.2461),
    "Mylapore": (13.0368, 80.2676),
    "Ambattur": (13.1143, 80.1548),
    "Kilpauk": (13.0784, 80.2404),
    "Egmore": (13.0732, 80.2609),
    "Alwarpet": (13.0335, 80.2530),
    "Vadapalani": (13.0500, 80.2121),
    "Chetpet": (13.0700, 80.2360)
}
