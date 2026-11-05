import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { hospitalService } from '../services/api';
import LeafletMap from '../components/LeafletMap';
import {
  Hospital, Search, MapPin, Phone, Globe, Navigation, Clock,
  Filter, ShieldAlert, Sparkles, Check, ChevronRight, X
} from 'lucide-react';

const HospitalDiscoveryPage = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const initialSpecialty = searchParams.get('specialty') || 'All';
  const initialEmergencyOnly = searchParams.get('emergency_only') === 'true';

  const [hospitals, setHospitals] = useState([]);
  const [localities, setLocalities] = useState([]);
  const [loading, setLoading] = useState(true);

  // Filters state
  const [selectedSpecialty, setSelectedSpecialty] = useState(initialSpecialty);
  const [selectedLocality, setSelectedLocality] = useState('All');
  const [facilityType, setFacilityType] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [maxDistance, setMaxDistance] = useState(30);
  const [emergencyOnly, setEmergencyOnly] = useState(initialEmergencyOnly);
  const [userCoords, setUserCoords] = useState(null);
  const [geoError, setGeoError] = useState(null);
  const [selectedHospitalModal, setSelectedHospitalModal] = useState(null);

  // Specialties list
  const specialtiesList = [
    'All', 'General Physician', 'Cardiologist', 'Neurologist', 'Dermatologist',
    'Gastroenterologist', 'Orthopedic Specialist', 'Pulmonologist', 'ENT Specialist',
    'Ophthalmologist', 'Endocrinologist', 'Urologist', 'Gynecologist'
  ];

  // Request browser location
  const handleUseCurrentLocation = () => {
    if (!navigator.geolocation) {
      setGeoError("Geolocation is not supported by your browser.");
      return;
    }
    setGeoError(null);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setUserCoords({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude
        });
      },
      (err) => {
        setGeoError("Permission denied. Using central Chennai (T. Nagar) as default.");
      }
    );
  };

  // Load localities
  useEffect(() => {
    const fetchLocalities = async () => {
      try {
        const res = await hospitalService.getLocalities();
        setLocalities(res.data.localities || []);
      } catch (err) {
        console.error("Failed to load localities:", err);
      }
    };
    fetchLocalities();
  }, []);

  // Fetch hospitals on filter change
  useEffect(() => {
    const fetchHospitals = async () => {
      setLoading(true);
      try {
        const params = {
          specialty: selectedSpecialty,
          locality: selectedLocality,
          facility_type: facilityType,
          q: searchQuery,
          max_distance: maxDistance,
          emergency_only: emergencyOnly,
        };
        if (userCoords) {
          params.lat = userCoords.latitude;
          params.lng = userCoords.longitude;
        }

        const res = await hospitalService.search(params);
        setHospitals(res.data.hospitals || []);
      } catch (err) {
        console.error("Failed to fetch hospitals:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchHospitals();
  }, [selectedSpecialty, selectedLocality, facilityType, searchQuery, maxDistance, emergencyOnly, userCoords]);

  return (
    <div className="space-y-6 py-6">
      
      {/* Header Banner */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-surface-muted shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full bg-secondary/15 text-secondary text-xs font-bold uppercase tracking-wider">
              Verified Healthcare Network
            </span>
            <span className="text-xs text-primary/50">Chennai, Tamil Nadu</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-primary tracking-tight mt-1">
            Chennai Hospitals & Specialist Discovery
          </h1>
        </div>

        <button
          type="button"
          onClick={handleUseCurrentLocation}
          className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-bold text-xs shadow-xs transition-all shrink-0"
        >
          <Navigation className="w-4 h-4 text-accent" />
          <span>{userCoords ? "Location Calibrated ✓" : "Use My Current Location"}</span>
        </button>
      </div>

      {geoError && (
        <div className="p-3 rounded-xl bg-status-warning/10 border border-status-warning/30 text-status-warning text-xs">
          {geoError}
        </div>
      )}

      {/* Filter Toolbar */}
      <div className="bg-white p-5 rounded-3xl border border-surface-muted shadow-xs space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          
          {/* Keyword Search */}
          <div className="relative">
            <Search className="w-4 h-4 text-primary/40 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search by hospital name or road..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none bg-surface-bg"
            />
          </div>

          {/* Specialty Selector */}
          <div>
            <select
              value={selectedSpecialty}
              onChange={(e) => setSelectedSpecialty(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none bg-surface-bg font-medium"
            >
              <option value="All">All Medical Specialties</option>
              {specialtiesList.slice(1).map(s => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          {/* Chennai Locality Selector */}
          <div>
            <select
              value={selectedLocality}
              onChange={(e) => setSelectedLocality(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none bg-surface-bg font-medium"
            >
              <option value="All">All Chennai Localities</option>
              {localities.map(loc => (
                <option key={loc.name} value={loc.name}>{loc.name}</option>
              ))}
            </select>
          </div>

          {/* Facility Type Filter */}
          <div className="flex gap-1 bg-surface-bg p-1 rounded-xl border border-surface-muted">
            {['All', 'Hospital', 'Clinic'].map((type) => (
              <button
                key={type}
                type="button"
                onClick={() => setFacilityType(type)}
                className={`flex-1 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  facilityType === type ? 'bg-white shadow-xs text-secondary font-bold' : 'text-primary/60'
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* Distance & Emergency Toggles */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-surface-muted text-xs">
          <div className="flex items-center gap-3">
            <span className="font-bold text-primary">Distance Radius:</span>
            <input
              type="range"
              min="3"
              max="45"
              value={maxDistance}
              onChange={(e) => setMaxDistance(parseInt(e.target.value))}
              className="w-32 sm:w-48 accent-secondary"
            />
            <span className="px-2 py-0.5 rounded bg-surface-bg font-bold text-primary">
              Up to {maxDistance} km
            </span>
          </div>

          <label className="flex items-center gap-2 cursor-pointer font-bold text-primary select-none">
            <input
              type="checkbox"
              checked={emergencyOnly}
              onChange={(e) => setEmergencyOnly(e.target.checked)}
              className="w-4 h-4 rounded text-status-emergency focus:ring-status-emergency"
            />
            <span className="text-status-emergency flex items-center gap-1">
              <ShieldAlert className="w-3.5 h-3.5" /> 24x7 Emergency Casualty Only
            </span>
          </label>
        </div>
      </div>

      {/* Main Grid: Left Map, Right Facility Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left: Interactive Leaflet Map (7 cols) */}
        <div className="lg:col-span-7 h-[540px] sticky top-20">
          <LeafletMap
            hospitals={hospitals}
            center={userCoords ? [userCoords.latitude, userCoords.longitude] : [13.0418, 80.2341]}
            zoom={12}
          />
        </div>

        {/* Right: Hospital Cards List (5 cols) */}
        <div className="lg:col-span-5 space-y-4 max-h-[540px] overflow-y-auto pr-1">
          <div className="text-xs font-bold text-primary/70 flex items-center justify-between">
            <span>Verified Results ({hospitals.length} establishments)</span>
            <span className="text-[11px] text-primary/50">Sorted by specialty & distance</span>
          </div>

          {loading ? (
            <div className="p-8 text-center text-xs text-primary/50 bg-white rounded-2xl border border-surface-muted">
              Searching Chennai healthcare directory...
            </div>
          ) : hospitals.length === 0 ? (
            <div className="p-8 text-center text-xs text-primary/60 bg-white rounded-2xl border border-surface-muted space-y-2">
              <Hospital className="w-8 h-8 text-primary/30 mx-auto" />
              <div className="font-bold text-primary">No establishments found matching filters</div>
              <p>Try widening the distance radius or selecting "All Localities".</p>
            </div>
          ) : (
            hospitals.map((hosp) => (
              <div
                key={hosp.id}
                className="bg-white p-5 rounded-2xl border border-surface-muted hover:border-secondary/40 shadow-xs space-y-3 transition-all"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h4 className="font-bold text-sm text-primary leading-tight">{hosp.name}</h4>
                    <span className="text-xs text-primary/60 flex items-center gap-1 mt-1">
                      <MapPin className="w-3.5 h-3.5 text-accent shrink-0" />
                      <span>{hosp.locality}, Chennai</span>
                      {hosp.distance_km && (
                        <span className="font-bold text-secondary ml-1">• {hosp.distance_km} km away</span>
                      )}
                    </span>
                  </div>

                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase shrink-0 ${
                    hosp.facility_type === 'Clinic' ? 'bg-accent/15 text-accent-dark' : 'bg-secondary/15 text-secondary'
                  }`}>
                    {hosp.facility_type}
                  </span>
                </div>

                {/* Specialties Badges */}
                <div className="flex flex-wrap gap-1">
                  {hosp.specialties?.slice(0, 4).map((sp, i) => (
                    <span key={i} className="px-2 py-0.5 rounded bg-surface-bg text-primary/70 text-[10px] font-medium border border-surface-muted">
                      {sp}
                    </span>
                  ))}
                  {hosp.specialties?.length > 4 && (
                    <span className="text-[10px] text-primary/40 font-semibold self-center">
                      +{hosp.specialties.length - 4} more
                    </span>
                  )}
                </div>

                {/* Fees and OPD Schedule (Module 8 Specifications) */}
                <div className="p-2.5 rounded-xl bg-surface-bg text-xs space-y-1 text-primary/80">
                  <div className="flex items-center justify-between">
                    <span className="text-primary/60">Published Fee:</span>
                    <strong className="text-primary font-bold">{hosp.consultation_fee}</strong>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-primary/60">OPD Hours:</span>
                    <span className="text-primary truncate max-w-[180px]">{hosp.opd_hours}</span>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center gap-2 pt-1">
                  <a
                    href={`tel:${hosp.phone}`}
                    className="flex-1 text-center py-2 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-bold text-xs shadow-xs transition-colors"
                  >
                    Call Hospital
                  </a>
                  <a
                    href={`https://maps.google.com/?q=${hosp.latitude},${hosp.longitude}`}
                    target="_blank"
                    rel="noreferrer"
                    className="flex-1 text-center py-2 rounded-xl border border-surface-muted hover:border-primary text-primary font-semibold text-xs transition-colors"
                  >
                    Directions
                  </a>
                  {hosp.website && (
                    <a
                      href={hosp.website}
                      target="_blank"
                      rel="noreferrer"
                      className="p-2 rounded-xl border border-surface-muted hover:border-secondary text-primary/60 hover:text-secondary transition-colors"
                      title="Hospital Website"
                    >
                      <Globe className="w-4 h-4" />
                    </a>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

      </div>

    </div>
  );
};

export default HospitalDiscoveryPage;
