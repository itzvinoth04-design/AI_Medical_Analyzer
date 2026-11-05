import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAssessment } from '../context/AssessmentContext';
import { useAuth } from '../context/AuthContext';
import ScoreIndicator from '../components/ScoreIndicator';
import EmergencyBanner from '../components/EmergencyBanner';
import confetti from 'canvas-confetti';
import {
  Activity, Stethoscope, AlertTriangle, CheckCircle2, ShieldAlert,
  Download, MapPin, ArrowRight, RefreshCw, FileText, ChevronRight,
  Info, Sparkles, UserCheck, HeartPulse
} from 'lucide-react';

const AnalysisResultsPage = () => {
  const navigate = useNavigate();
  const { assessmentResults, resetAssessment } = useAssessment();
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    // If not emergency, launch small clean confetti for completing the assessment
    if (assessmentResults && !assessmentResults.is_emergency) {
      try {
        confetti({
          particleCount: 40,
          spread: 60,
          origin: { y: 0.8 },
          colors: ['#247BA0', '#20B2AA', '#2E9D72']
        });
      } catch (e) {
        // Optional
      }
    }
  }, [assessmentResults]);

  if (!assessmentResults) {
    return (
      <div className="text-center py-20 space-y-4">
        <Stethoscope className="w-12 h-12 text-primary/30 mx-auto" />
        <h2 className="text-xl font-bold text-primary">No Active Assessment Results</h2>
        <p className="text-xs text-primary/60">Please start a new health assessment to view AI triage results.</p>
        <Link
          to="/assessment/symptoms"
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-secondary text-white font-bold text-xs shadow-xs"
        >
          <span>Start Assessment</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  const {
    is_emergency, emergency_alert, urgency_status, urgency_badge_color,
    active_symptoms, negated_symptoms, nlp_entities,
    top_conditions, doctor_recommendation, safety_disclaimer, assessment_id
  } = assessmentResults;

  return (
    <div className="max-w-5xl mx-auto py-8 space-y-8">
      
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-surface-muted pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className={`px-2.5 py-0.5 rounded-md text-[11px] font-black uppercase tracking-wider ${
              is_emergency
                ? 'bg-status-emergency text-white'
                : urgency_badge_color === 'warning'
                ? 'bg-status-warning text-white'
                : 'bg-status-success text-white'
            }`}>
              {urgency_status}
            </span>
            <span className="text-xs text-primary/50 font-semibold">
              Assessment Report #{assessment_id || 'TEMP'}
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-primary tracking-tight mt-1">
            Symptom Analysis & Doctor Recommendations
          </h1>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2 shrink-0">
          {assessment_id && (
            <a
              href={`/api/assessment/${assessment_id}/pdf`}
              download
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white border border-surface-muted hover:border-secondary text-primary font-bold text-xs shadow-xs transition-colors"
            >
              <Download className="w-4 h-4 text-secondary" />
              <span>Download PDF</span>
            </a>
          )}
          <button
            onClick={() => {
              resetAssessment();
              navigate('/assessment/symptoms');
            }}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-surface-bg border border-surface-muted hover:bg-white text-primary/70 font-semibold text-xs transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>New Assessment</span>
          </button>
        </div>
      </div>

      {/* Emergency Red-Flag Override Banner (Module 4 requirement) */}
      {is_emergency && (
        <EmergencyBanner alertReason={emergency_alert} />
      )}

      {/* Doctor Specialization Recommendation Card (Module 5 requirement) */}
      <div className="bg-gradient-to-r from-secondary/10 via-white to-accent/10 p-6 sm:p-7 rounded-3xl border-2 border-secondary/30 shadow-md space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-surface-muted/80 pb-4">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-secondary text-white shadow-md shadow-secondary/20">
              <Stethoscope className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs font-bold text-accent uppercase tracking-wider">
                Recommended Medical Specialist
              </span>
              <h2 className="text-xl sm:text-2xl font-extrabold text-primary">
                {doctor_recommendation?.primary_specialty || "General Physician"}
              </h2>
            </div>
          </div>

          <div className="text-left sm:text-right shrink-0">
            <div className="text-xs font-bold text-primary/60">Recommendation Match</div>
            <div className="text-2xl font-black text-secondary">
              {doctor_recommendation?.recommendation_match || 90}/100
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <div className="text-xs font-bold text-primary">Triage Routing Rationale:</div>
          <p className="text-xs sm:text-sm text-primary/80 leading-relaxed bg-white/80 p-4 rounded-2xl border border-surface-muted/60">
            {doctor_recommendation?.reason || "Appropriate for initial comprehensive assessment."}
          </p>
        </div>

        {/* CTA to find Chennai Doctors */}
        <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-3">
          <span className="text-xs font-semibold text-primary/70">
            Would you like to find verified doctors and hospitals near you in Chennai?
          </span>
          <Link
            to={`/hospitals?specialty=${encodeURIComponent(doctor_recommendation?.primary_specialty || 'General Physician')}`}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary hover:bg-primary-dark text-white font-bold text-xs shadow-md transition-all hover:scale-102"
          >
            <MapPin className="w-4 h-4 text-accent" />
            <span>Find {doctor_recommendation?.primary_specialty || "Doctors"} Near You</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* Reported Symptoms & NLP Summary */}
      <div className="bg-white p-5 rounded-2xl border border-surface-muted shadow-xs space-y-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-primary/60">Clinical Context Observed</h4>
        <div className="flex flex-wrap gap-2 text-xs">
          {active_symptoms?.map(s => (
            <span key={s.code} className="px-3 py-1 rounded-lg bg-surface-bg border border-surface-muted font-bold text-primary flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-secondary" />
              <span>{s.name}</span>
            </span>
          ))}
          {negated_symptoms?.map(s => (
            <span key={s.code} className="px-3 py-1 rounded-lg bg-surface-bg border border-status-warning/40 font-medium text-status-warning line-through">
              {s.name} (absent)
            </span>
          ))}
          <span className="px-3 py-1 rounded-lg bg-surface-bg border border-surface-muted font-semibold text-primary/60">
            Duration: {nlp_entities?.duration_days} day(s)
          </span>
          <span className="px-3 py-1 rounded-lg bg-surface-bg border border-surface-muted font-semibold text-primary/60">
            Severity: {nlp_entities?.severity}
          </span>
        </div>
      </div>

      {/* Possible Conditions Catalogue (Module 4 requirement: Top 3-5 conditions) */}
      <div className="space-y-4">
        <div>
          <h3 className="text-lg font-bold text-primary">Possible Health Explanations</h3>
        </div>

        <div className="space-y-4">
          {top_conditions?.map((cond, idx) => (
            <div
              key={cond.condition_code || idx}
              className="bg-white p-6 rounded-3xl border border-surface-muted shadow-xs hover:border-secondary/40 transition-all space-y-4"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-surface-muted/60 pb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="w-6 h-6 rounded-full bg-secondary/15 text-secondary text-xs font-bold flex items-center justify-center">
                      {idx + 1}
                    </span>
                    <h4 className="text-lg font-bold text-primary">{cond.condition_name}</h4>
                  </div>
                  <span className="text-xs text-primary/50 ml-8 font-medium">
                    Category: {cond.category} • Urgency: {cond.urgency_level}
                  </span>
                </div>

                <ScoreIndicator score={cond.compatibility_score} size="md" />
              </div>

              {/* Explainable AI (XAI) Section */}
              <div className="space-y-3 text-xs leading-relaxed">
                <div>
                  <span className="font-bold text-primary block mb-1">Why this was considered:</span>
                  <p className="text-primary/80 bg-surface-bg p-3 rounded-xl border border-surface-muted">
                    {cond.why_considered}
                  </p>
                </div>

                {/* Supporting vs Missing Criteria Chips */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                  <div className="space-y-1.5">
                    <span className="font-bold text-status-success text-[11px] uppercase tracking-wider block">
                      Supporting Symptoms Present:
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {cond.supporting_symptoms?.length > 0 ? (
                        cond.supporting_symptoms.map((sym, i) => (
                          <span key={i} className="px-2 py-0.5 rounded-md bg-status-success/10 text-status-success text-[11px] font-semibold">
                            ✓ {sym}
                          </span>
                        ))
                      ) : (
                        <span className="text-primary/40 italic">None reported</span>
                      )}
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <span className="font-bold text-primary/50 text-[11px] uppercase tracking-wider block">
                      Missing Hallmark Signs:
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {cond.missing_symptoms?.length > 0 ? (
                        cond.missing_symptoms.map((sym, i) => (
                          <span key={i} className="px-2 py-0.5 rounded-md bg-surface-bg text-primary/60 text-[11px]">
                            ○ {sym}
                          </span>
                        ))
                      ) : (
                        <span className="text-primary/40 italic">All hallmark signs accounted for</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* General Explanation & Care Advice */}
                <div className="pt-2 border-t border-surface-muted/60 grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <span className="font-bold text-primary block text-[11px]">General Information:</span>
                    <p className="text-primary/70 text-[11px] mt-0.5">{cond.general_explanation}</p>
                  </div>
                  <div>
                    <span className="font-bold text-primary block text-[11px]">When Clinical Care is Appropriate:</span>
                    <p className="text-primary/70 text-[11px] mt-0.5">{cond.when_to_seek_care}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Safety Notice Card */}
      <div className="p-5 rounded-2xl bg-white border border-surface-muted shadow-xs text-xs text-primary/70 leading-relaxed">
        <strong>CLINICAL INTERPRETATION NOTE:</strong> {safety_disclaimer}
      </div>

      {/* Bottom Action Footer */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-surface-muted">
        <Link
          to="/hospitals"
          className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-bold text-xs shadow-xs"
        >
          <MapPin className="w-4 h-4 text-accent" />
          <span>Locate Nearby Chennai Hospitals</span>
        </Link>

        {assessment_id && (
          <a
            href={`/api/assessment/${assessment_id}/pdf`}
            download
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl border border-surface-muted hover:border-secondary text-primary font-bold text-xs bg-white"
          >
            <Download className="w-4 h-4 text-secondary" />
            <span>Download Official PDF Medical Report</span>
          </a>
        )}
      </div>

    </div>
  );
};

export default AnalysisResultsPage;
