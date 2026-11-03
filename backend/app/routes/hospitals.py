from flask import Blueprint, request, jsonify
from app.models import Hospital, Specialty, HospitalSpecialty
from app.hospital_search.haversine import haversine_distance_km, CHENNAI_LOCALITY_COORDINATES

hospitals_bp = Blueprint("hospitals", __name__)

@hospitals_bp.route("/localities", methods=["GET"])
def get_localities():
    """Returns Chennai localities with coordinate anchors for manual location selection."""
    loc_list = [
        {"name": loc, "latitude": coords[0], "longitude": coords[1]}
        for loc, coords in CHENNAI_LOCALITY_COORDINATES.items()
    ]
    return jsonify({"localities": loc_list}), 200

@hospitals_bp.route("/search", methods=["GET"])
def search_hospitals():
    """
    Modules 6, 7 & 8: Search and rank Chennai healthcare establishments.
    Computes distance using Haversine formula and ranks by specialty match and proximity.
    """
    specialty_query = request.args.get("specialty", "").strip()
    locality_query = request.args.get("locality", "").strip()
    facility_type = request.args.get("facility_type", "").strip()
    search_q = request.args.get("q", "").strip().lower()
    
    # Geolocation: User lat/lng or selected locality coordinates
    user_lat = request.args.get("lat", type=float)
    user_lng = request.args.get("lng", type=float)
    
    # If locality specified but no user coordinates, lookup locality coordinates
    if (user_lat is None or user_lng is None) and locality_query in CHENNAI_LOCALITY_COORDINATES:
        user_lat, user_lng = CHENNAI_LOCALITY_COORDINATES[locality_query]
    elif user_lat is None or user_lng is None:
        # Default to Central Chennai (T. Nagar)
        user_lat, user_lng = CHENNAI_LOCALITY_COORDINATES["T. Nagar"]

    max_dist = request.args.get("max_distance", default=35.0, type=float)
    emergency_only = request.args.get("emergency_only", default="false").lower() == "true"

    # Base query
    query = Hospital.query

    if facility_type and facility_type != "All":
        query = query.filter(Hospital.facility_type == facility_type)

    if emergency_only:
        query = query.filter(Hospital.emergency_24x7 == True)

    if locality_query and locality_query != "All":
        query = query.filter(Hospital.locality.ilike(f"%{locality_query}%"))

    all_hospitals = query.all()
    results = []

    for h in all_hospitals:
        h_dict = h.to_dict()

        # Compute Haversine distance
        dist_km = haversine_distance_km(user_lat, user_lng, h.latitude, h.longitude)
        h_dict["distance_km"] = dist_km

        # Text search filter
        if search_q:
            matches_name = search_q in h.name.lower()
            matches_addr = search_q in h.address.lower()
            matches_loc = search_q in h.locality.lower()
            if not (matches_name or matches_addr or matches_loc):
                continue

        # Specialty match evaluation
        has_specialty = False
        if specialty_query and specialty_query != "All":
            has_specialty = any(specialty_query.lower() in s.lower() for s in h_dict["specialties"])
            h_dict["specialty_match"] = has_specialty
        else:
            h_dict["specialty_match"] = True

        # Distance radius filter
        if dist_km <= max_dist:
            results.append(h_dict)

    # Ranking Algorithm (Module 7):
    # 1. Specialty match (True first)
    # 2. Distance (closest first)
    # 3. 24x7 Emergency availability
    def sort_key(item):
        spec_rank = 0 if item.get("specialty_match") else 1
        return (spec_rank, item.get("distance_km", 999.0))

    results.sort(key=sort_key)

    return jsonify({
        "total_results": len(results),
        "user_coordinates": {"latitude": user_lat, "longitude": user_lng},
        "hospitals": results
    }), 200

@hospitals_bp.route("/<int:hospital_id>", methods=["GET"])
def get_hospital_details(hospital_id):
    """Returns comprehensive hospital profile including verified doctors and departments."""
    hospital = Hospital.query.get(hospital_id)
    if not hospital:
        return jsonify({"error": "Hospital record not found"}), 404

    h_dict = hospital.to_dict()
    h_dict["doctors"] = [d.to_dict() for d in hospital.doctors]
    return jsonify({"hospital": h_dict}), 200
