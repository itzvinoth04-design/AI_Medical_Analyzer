import React, { useEffect, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { assessmentService, hospitalService } from '../services/api';
import {
  Stethoscope, PlusCircle, History, Hospital, ArrowRight, FileText,
  Clock, ShieldAlert, CheckCircle2, MapPin, Download, AlertTriangle
} from 'lucide-react';

const DashboardPage = () => {
  const { user } = useAuth();
  const [history, setHistory] = useState([]);
  const [nearbyHospitals, setNearbyHospitals] = useState([]);
  const [loading, setLoading] = useState(true);

  // If user is admin, immediately route to the Admin Console
  if (user?.role === 'admin') {
    return <Navigate to="/admin" replace />;
  }

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const histRes = await assessmentService.getHistory();
        setHistory(histRes.data.history || []);
        
        const hospRes = await hospitalService.search({ locality: 'T. Nagar', limit: 3 });
        setNearbyHospitals(hospRes.data.hospitals?.slice(0, 3) || []);
      } catch (err) {
        console.error("Dashboard data load error:", err);
      } finally {
        setLoading(false);
      }
    };
    loadDashboardData();
  }, []);

  const latestAssessment = history.length > 0 ? history[0] : null;

  return (
    <div className="space-y-8 py-6">
      
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-primary to-primary-light text-white p-6 sm:p-8 rounded-3xl border border-primary-light/50 shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-0.5 rounded-full bg-secondary/30 text-secondary-light text-xs font-bold uppercase tracking-wider">
            Patient Portal
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome, {user?.full_name || 'Patient'}
          </h1>
        </div>

        {/* Prominent CTA */}
        <Link
          to="/assessment/symptoms"
          className="inline-flex items-center gap-2 px-6 py-4 rounded-2xl bg-secondary hover:bg-secondary-dark text-white font-extrabold text-sm shadow-xl shadow-secondary/25 transition-all hover:scale-105 shrink-0"
        >
          <PlusCircle className="w-5 h-5 text-accent" />
          <span>Start New Health Assessment</span>
          <ArrowRight className="w-4 h-4 ml-1" />
        </Link>
      </div>

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div className="bg-white p-5 rounded-2xl border border-surface-muted shadow-xs flex items-center gap-4">
          <div className="p-3 rounded-xl bg-secondary/15 text-secondary shrink-0">
            <FileText className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-black text-primary">{history.length}</div>
            <div className="text-xs font-semibold text-primary/60">Triage Reports Saved</div>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-surface-muted shadow-xs flex items-center gap-4">
          <div className="p-3 rounded-xl bg-accent/20 text-accent-dark shrink-0">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <div className="text-xs font-semibold text-primary/60">Last Health Check</div>
            <div className="text-sm font-bold text-primary truncate max-w-[200px]">
              {latestAssessment ? latestAssessment.created_at.split(' ')[0] : 'No assessments yet'}
            </div>
          </div>
        </div>
      </div>

      {/* Two Column Layout: Recent Reports & Chennai Clinics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Recent Consultations (2 cols) */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <History className="w-5 h-5 text-secondary" />
              <h3 className="text-lg font-bold text-primary">Recent Health Assessments</h3>
            </div>
            {history.length > 0 && (
              <Link to="/history" className="text-xs font-bold text-secondary hover:underline">
                View All History ({history.length})
              </Link>
            )}
          </div>

          {loading ? (
            <div className="p-12 text-center bg-white rounded-2xl border border-surface-muted text-xs text-primary/50">
              Loading assessments...
            </div>
          ) : history.length === 0 ? (
            <div className="p-10 text-center bg-white rounded-2xl border border-surface-muted space-y-3">
              <Stethoscope className="w-10 h-10 text-primary/20 mx-auto" />
              <div className="font-bold text-primary text-sm">No health assessments yet</div>
              <p className="text-xs text-primary/60 max-w-sm mx-auto">
                Begin your first AI-assisted clinical symptom assessment to receive condition compatibility insights and doctor recommendations.
              </p>
              <Link
                to="/assessment/symptoms"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-secondary text-white font-bold text-xs shadow-xs"
              >
                <span>Start First Assessment</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {history.slice(0, 3).map((item) => (
                <div
                  key={item.id}
                  className="bg-white p-5 rounded-2xl border border-surface-muted hover:border-secondary/40 shadow-xs transition-all space-y-3"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          item.is_emergency
                            ? 'bg-status-emergency/15 text-status-emergency'
                            : item.severity === 'Severe'
                            ? 'bg-status-warning/15 text-status-warning'
                            : 'bg-status-success/15 text-status-success'
                        }`}>
                          {item.is_emergency ? 'Critical Emergency' : `${item.severity} Severity`}
                        </span>
                        <span className="text-xs text-primary/50 font-medium">#{item.id} • {item.created_at}</span>
                      </div>
                      <h4 className="text-base font-bold text-primary mt-1">
                        Chief Complaint: {item.chief_complaint || 'General Malaise'}
                      </h4>
                    </div>

                    <a
                      href={`/api/assessment/${item.id}/pdf`}
                      download
                      className="p-2 rounded-xl text-primary/60 hover:text-secondary hover:bg-secondary/10 transition-colors"
                      title="Download PDF Report"
                    >
                      <Download className="w-4 h-4" />
                    </a>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs pt-1 border-t border-surface-muted/60">
                    <div>
                      <span className="text-primary/50 block text-[11px]">Recommended Doctor</span>
                      <strong className="text-secondary font-bold">{item.recommended_specialty || 'General Physician'}</strong>
                    </div>
                    <div>
                      <span className="text-primary/50 block text-[11px]">Duration</span>
                      <span className="font-semibold text-primary">{item.duration_days} day(s)</span>
                    </div>
                    <div>
                      <span className="text-primary/50 block text-[11px]">Match Rating</span>
                      <span className="font-semibold text-primary">{item.doctor_recommendation_match || 85}/100</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Column: Nearby Chennai Hospitals Snapshot */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Hospital className="w-5 h-5 text-secondary" />
              <h3 className="text-lg font-bold text-primary">Chennai Healthcare</h3>
            </div>
            <Link to="/hospitals" className="text-xs font-bold text-secondary hover:underline">
              View Map
            </Link>
          </div>

          <div className="space-y-3">
            {nearbyHospitals.map((hosp) => (
              <div key={hosp.id} className="bg-white p-4 rounded-2xl border border-surface-muted shadow-xs space-y-2">
                <div className="flex items-start justify-between gap-2">
                  <h5 className="font-bold text-sm text-primary line-clamp-1">{hosp.name}</h5>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-surface-bg text-secondary shrink-0">
                    {hosp.facility_type}
                  </span>
                </div>
                <div className="text-xs text-primary/60 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-accent shrink-0" />
                  <span className="truncate">{hosp.locality}, Chennai</span>
                </div>
                <div className="flex items-center justify-between text-xs pt-2 border-t border-surface-muted/50">
                  <span className="font-semibold text-primary/80">Fee: {hosp.consultation_fee}</span>
                  <a
                    href={`tel:${hosp.phone}`}
                    className="text-secondary font-bold hover:underline"
                  >
                    Call Hospital
                  </a>
                </div>
              </div>
            ))}

            <Link
              to="/hospitals"
              className="block text-center py-2.5 rounded-xl border border-secondary text-secondary font-bold text-xs hover:bg-secondary/5 transition-colors"
            >
              Search All Chennai Hospitals & Clinics
            </Link>
          </div>
        </div>

      </div>

    </div>
  );
};

export default DashboardPage;
