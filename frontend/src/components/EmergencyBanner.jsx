import React from 'react';
import { AlertTriangle, PhoneCall, ArrowRight, ShieldAlert } from 'lucide-react';
import { Link } from 'react-router-dom';

const EmergencyBanner = ({ alertReason, onNavigateHospitals }) => {
  return (
    <div className="bg-gradient-to-r from-status-emergency/90 via-status-emergency to-red-700 text-white p-5 rounded-2xl shadow-xl shadow-status-emergency/20 border-2 border-white/20 animate-pulse-subtle my-6">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        
        {/* Warning Icon & Text */}
        <div className="flex items-start gap-3.5">
          <div className="p-2.5 rounded-xl bg-white/20 text-white shrink-0 shadow-inner">
            <ShieldAlert className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 rounded text-[11px] font-black uppercase tracking-wider bg-white text-status-emergency">
                Critical Red Flag Detected
              </span>
              <h3 className="text-lg font-bold text-white tracking-tight">Immediate Medical Emergency Alert</h3>
            </div>
            <p className="text-sm text-white/95 mt-1 font-medium leading-relaxed max-w-2xl">
              {alertReason || "The reported symptoms fulfill clinical emergency red-flag criteria (e.g. stroke FAST sign, acute cardiac sign, or acute airway distress). Ordinary outpatient disease scoring has been bypassed."}
            </p>
            <div className="text-xs text-white/80 mt-1 font-semibold">
              ⚠️ Do not drive yourself. Seek immediate assistance from bystanders or emergency medical transport.
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-3 shrink-0 w-full md:w-auto">
          <a
            href="tel:112"
            className="flex-1 md:flex-initial inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-white text-status-emergency hover:bg-red-50 font-extrabold text-sm shadow-md transition-transform hover:scale-105"
          >
            <PhoneCall className="w-4 h-4 animate-bounce" />
            <span>Call 112 (India)</span>
          </a>
          <Link
            to="/hospitals?emergency_only=true"
            className="flex-1 md:flex-initial inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl bg-black/25 hover:bg-black/40 text-white font-semibold text-sm border border-white/20 transition-colors"
          >
            <span>Find 24x7 Emergency ER</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default EmergencyBanner;
