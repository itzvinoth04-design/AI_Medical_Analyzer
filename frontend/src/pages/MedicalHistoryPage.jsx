import React, { useEffect, useState } from 'react';
import { assessmentService } from '../services/api';
import {
  History, Download, Trash2, ArrowRight, FileText, CheckCircle2,
  Calendar, Stethoscope, Columns, X, AlertTriangle
} from 'lucide-react';

const MedicalHistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedForCompare, setSelectedForCompare] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const [comparisonLoading, setComparisonLoading] = useState(false);

  const fetchHistory = async () => {
    try {
      const res = await assessmentService.getHistory();
      setHistory(res.data.history || []);
    } catch (err) {
      console.error("Failed to load history:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this consultation report? This action cannot be undone.")) return;
    try {
      await assessmentService.deleteById(id);
      setHistory(prev => prev.filter(h => h.id !== id));
      setSelectedForCompare(prev => prev.filter(item => item !== id));
    } catch (err) {
      alert("Failed to delete record.");
    }
  };

  const toggleCompareSelect = (id) => {
    if (selectedForCompare.includes(id)) {
      setSelectedForCompare(prev => prev.filter(item => item !== id));
    } else {
      if (selectedForCompare.length >= 2) {
        alert("You can select up to 2 consultations to compare side-by-side.");
        return;
      }
      setSelectedForCompare(prev => [...prev, id]);
    }
  };

  const handleLaunchComparison = async () => {
    if (selectedForCompare.length !== 2) return;
    setComparisonLoading(true);
    try {
      const res = await assessmentService.compare(selectedForCompare[0], selectedForCompare[1]);
      setComparisonData(res.data);
    } catch (err) {
      alert("Failed to generate side-by-side comparison.");
    } finally {
      setComparisonLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto py-8 space-y-8">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-surface-muted pb-4">
        <div>
          <span className="text-xs font-bold text-accent uppercase tracking-wider">Confidential Health Archive</span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-primary tracking-tight mt-1">
            Consultation History & Reports
          </h1>
          <p className="text-xs text-primary/60 mt-0.5">
            Review past triage sessions, re-download clinical PDF summaries, or compare assessments over time
          </p>
        </div>

        {selectedForCompare.length === 2 && (
          <button
            type="button"
            onClick={handleLaunchComparison}
            disabled={comparisonLoading}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-bold text-xs shadow-md transition-all shrink-0"
          >
            <Columns className="w-4 h-4" />
            <span>Compare Selected (2)</span>
          </button>
        )}
      </div>

      {/* Comparison Modal / Panel */}
      {comparisonData && (
        <div className="bg-white p-6 sm:p-7 rounded-3xl border-2 border-secondary shadow-xl space-y-6 animate-fade-in relative">
          <div className="flex items-center justify-between border-b border-surface-muted pb-3">
            <div className="flex items-center gap-2">
              <Columns className="w-5 h-5 text-secondary" />
              <h3 className="font-bold text-lg text-primary">Side-by-Side Assessment Comparison</h3>
            </div>
            <button
              onClick={() => setComparisonData(null)}
              className="p-1.5 rounded-lg text-primary/50 hover:bg-surface-bg"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[comparisonData.assessment_1, comparisonData.assessment_2].map((item, idx) => (
              <div key={item.id} className="p-4 rounded-2xl bg-surface-bg border border-surface-muted space-y-3">
                <div className="flex items-center justify-between border-b border-surface-muted pb-2">
                  <span className="text-xs font-bold text-secondary">Assessment #{item.id}</span>
                  <span className="text-xs text-primary/50">{item.created_at}</span>
                </div>
                <div className="text-sm font-bold text-primary">
                  Complaint: {item.chief_complaint || 'General Malaise'}
                </div>
                <div className="text-xs text-primary/70 space-y-1">
                  <div><strong>Severity:</strong> {item.severity} ({item.duration_days} days)</div>
                  <div><strong>Status:</strong> {item.progress_status}</div>
                  <div><strong>Specialist:</strong> {item.recommended_specialty}</div>
                  <div><strong>Match:</strong> {item.doctor_recommendation_match}/100</div>
                </div>
                <div className="pt-2">
                  <span className="text-xs font-bold text-primary block mb-1">Top Condition:</span>
                  {item.results && item.results[0] ? (
                    <div className="p-2.5 rounded-xl bg-white border border-surface-muted text-xs">
                      <div className="font-bold text-primary">{item.results[0].condition_name}</div>
                      <div className="text-secondary font-bold">Score: {item.results[0].compatibility_score}/100</div>
                    </div>
                  ) : (
                    <span className="text-xs text-primary/40">No condition results stored</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* History List */}
      {loading ? (
        <div className="p-12 text-center text-xs text-primary/50 bg-white rounded-3xl border border-surface-muted">
          Loading medical records...
        </div>
      ) : history.length === 0 ? (
        <div className="p-12 text-center text-xs text-primary/60 bg-white rounded-3xl border border-surface-muted space-y-3">
          <History className="w-10 h-10 text-primary/20 mx-auto" />
          <div className="font-bold text-sm text-primary">No previous consultations recorded</div>
          <p className="max-w-md mx-auto">
            Your assessments will be automatically archived here with downloadable clinical summaries.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="text-xs text-primary/60 flex items-center justify-between">
            <span>Select any 2 consultations to compare symptom progression over time.</span>
            <span>{history.length} records</span>
          </div>

          <div className="grid grid-cols-1 gap-3">
            {history.map((item) => {
              const isSelected = selectedForCompare.includes(item.id);
              return (
                <div
                  key={item.id}
                  className={`bg-white p-5 rounded-2xl border transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
                    isSelected ? 'border-secondary bg-secondary/5 shadow-xs' : 'border-surface-muted hover:border-primary/30'
                  }`}
                >
                  <div className="flex items-start gap-4">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => toggleCompareSelect(item.id)}
                      className="mt-1 w-4 h-4 rounded text-secondary focus:ring-secondary cursor-pointer"
                      title="Select for comparison"
                    />

                    <div className="space-y-1">
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
                        <span className="text-xs text-primary/50">#{item.id} • {item.created_at}</span>
                      </div>

                      <h4 className="font-bold text-sm text-primary">
                        {item.chief_complaint || 'General Symptom Evaluation'}
                      </h4>

                      <div className="text-xs text-primary/60 flex flex-wrap gap-x-4 gap-y-1">
                        <span>Duration: <strong>{item.duration_days} day(s)</strong></span>
                        <span>Doctor: <strong className="text-secondary">{item.recommended_specialty}</strong></span>
                        <span>Match: <strong>{item.doctor_recommendation_match}/100</strong></span>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 shrink-0 self-end sm:self-center">
                    <a
                      href={`/api/assessment/${item.id}/pdf`}
                      download
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-surface-bg hover:bg-secondary hover:text-white text-primary text-xs font-semibold border border-surface-muted transition-colors"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>PDF Report</span>
                    </a>

                    <button
                      onClick={() => handleDelete(item.id)}
                      className="p-2 rounded-xl text-primary/40 hover:text-status-emergency hover:bg-status-emergency/10 transition-colors"
                      title="Delete consultation record"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

    </div>
  );
};

export default MedicalHistoryPage;
