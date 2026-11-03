import React, { useEffect, useRef } from 'react';
import L from 'leaflet';

// Fix Leaflet default icon path issues in React Vite builds
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const LeafletMap = ({ hospitals = [], center = [13.04, 80.23], zoom = 12, onSelectHospital }) => {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersLayerRef = useRef(null);

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      const map = L.map(mapContainerRef.current).setView(center, zoom);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
      }).addTo(map);

      markersLayerRef.current = L.layerGroup().addTo(map);
      mapInstanceRef.current = map;
    } else {
      mapInstanceRef.current.setView(center, zoom);
    }
  }, [center, zoom]);

  useEffect(() => {
    if (!mapInstanceRef.current || !markersLayerRef.current) return;

    markersLayerRef.current.clearLayers();

    // Custom Hospital Pin Icon
    const hospitalIcon = L.divIcon({
      className: 'custom-hospital-marker',
      html: `
        <div style="background-color: #247BA0; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; border: 2px solid white; box-shadow: 0 4px 10px rgba(0,0,0,0.3); font-weight: bold; font-size: 14px;">
          H
        </div>
      `,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
      popupAnchor: [0, -16]
    });

    const clinicIcon = L.divIcon({
      className: 'custom-clinic-marker',
      html: `
        <div style="background-color: #20B2AA; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; border: 2px solid white; box-shadow: 0 4px 8px rgba(0,0,0,0.25); font-weight: bold; font-size: 12px;">
          +
        </div>
      `,
      iconSize: [28, 28],
      iconAnchor: [14, 14],
      popupAnchor: [0, -14]
    });

    hospitals.forEach((h) => {
      if (h.latitude && h.longitude) {
        const isClinic = h.facility_type === 'Clinic';
        const marker = L.marker([h.latitude, h.longitude], {
          icon: isClinic ? clinicIcon : hospitalIcon
        });

        const popupContent = document.createElement('div');
        popupContent.style.minWidth = '220px';
        popupContent.style.fontFamily = 'Plus Jakarta Sans, sans-serif';
        popupContent.innerHTML = `
          <div style="font-weight: 700; color: #102A43; font-size: 14px; margin-bottom: 4px;">${h.name}</div>
          <div style="font-size: 11px; color: #627D98; margin-bottom: 6px;">📍 ${h.locality}, Chennai ${h.distance_km ? `(${h.distance_km} km)` : ''}</div>
          <div style="display: flex; gap: 4px; margin-bottom: 6px;">
            <span style="font-size: 10px; padding: 2px 6px; border-radius: 4px; background: ${isClinic ? '#E0F2F1' : '#E0F2FE'}; color: ${isClinic ? '#00796B' : '#0284C7'}; font-weight: 600;">
              ${h.facility_type}
            </span>
            <span style="font-size: 10px; padding: 2px 6px; border-radius: 4px; background: #F1F5F9; color: #475569; font-weight: 600;">
              Fee: ${h.consultation_fee || 'Call to confirm'}
            </span>
          </div>
          <div style="font-size: 11px; color: #334155; margin-bottom: 8px;">🕒 ${h.opd_hours || 'Contact hospital'}</div>
          <div style="display: flex; gap: 6px;">
            <a href="tel:${h.phone}" style="flex: 1; text-align: center; background: #247BA0; color: white; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; text-decoration: none;">Call</a>
            <a href="https://maps.google.com/?q=${h.latitude},${h.longitude}" target="_blank" rel="noreferrer" style="flex: 1; text-align: center; background: #102A43; color: white; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; text-decoration: none;">Directions</a>
          </div>
        `;

        marker.bindPopup(popupContent);
        markersLayerRef.current.addLayer(marker);
      }
    });

    // Auto-fit bounds if hospitals present
    if (hospitals.length > 0) {
      const validLatLngs = hospitals
        .filter(h => h.latitude && h.longitude)
        .map(h => [h.latitude, h.longitude]);
      if (validLatLngs.length > 0) {
        const bounds = L.latLngBounds(validLatLngs);
        mapInstanceRef.current.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
      }
    }
  }, [hospitals]);

  return (
    <div className="w-full h-full relative rounded-xl overflow-hidden border border-surface-muted shadow-xs">
      <div ref={mapContainerRef} className="w-full h-full" style={{ minHeight: '400px' }} />
    </div>
  );
};

export default LeafletMap;
