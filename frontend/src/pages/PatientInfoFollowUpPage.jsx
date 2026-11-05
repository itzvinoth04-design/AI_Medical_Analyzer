import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAssessment } from '../context/AssessmentContext';
import { useAuth } from '../context/AuthContext';
import {
  User, Calendar, TrendingUp, HelpCircle, ArrowRight, ArrowLeft,
  CheckCircle2, AlertCircle, FileText, Sparkles
} from 'lucide-react';

const PatientInfoFollowUpPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const {
    durationDays, setDurationDays,
    severity, setSeverity,
    progressStatus, setProgressStatus,
    patientInfo, setPatientInfo,
    followUpQuestions,
    followUpAnswers, setFollowUpAnswers
  } = useAssessment();

  const handleInfoChange = (e) => {
    const { name, value } = e.target;
    setPatientInfo(prev => ({ ...prev, [name]: value }));
  };

  const handleOptionSelect = (qId, option) => {
    setFollowUpAnswers(prev => ({ ...prev, [qId]: option }));
  };

  const handleRunAnalysis = () => {
    navigate('/assessment/loading');
  };

  return (
    <div className="max-w-4xl mx-auto py-8 space-y-8">
      
      {/* Progress Header */}
      <div className="flex items-center justify-between border-b border-surface-muted pb-4">
        <div>
          <span className="text-xs font-bold text-accent uppercase tracking-wider">Step 2 of 3</span>
          <h1 className="text-2xl font-extrabold text-primary tracking-tight">Follow-Up Questions</h1>
        </div>
        <div className="hidden sm:flex items-center gap-2 text-xs font-semibold">
          <span className="w-6 h-6 rounded-full bg-status-success text-white flex items-center justify-center text-xs">✓</span>
          <span className="text-status-success font-bold">Input Symptoms</span>
          <span className="text-primary/30">→</span>
          <span className="w-6 h-6 rounded-full bg-secondary text-white flex items-center justify-center text-xs">2</span>
          <span className="text-secondary font-bold">Follow-up</span>
          <span className="text-primary/30">→</span>
          <span className="w-6 h-6 rounded-full bg-surface-muted text-primary/60 flex items-center justify-center text-xs">3</span>
          <span className="text-primary/60">Results</span>
        </div>
      </div>

      {/* Dynamic Clinical Follow-up Questions Card (if any generated) */}
      {followUpQuestions.length > 0 && (
        <div className="bg-white p-6 sm:p-7 rounded-3xl border border-secondary/20 shadow-xs space-y-6">
          <div className="flex items-start gap-3 border-b border-surface-muted pb-4">
            <div className="p-2 rounded-xl bg-secondary/15 text-secondary shrink-0 mt-0.5">
              <HelpCircle className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-base text-primary">
                Targeted Clinical Questions
              </h3>
            </div>
          </div>

          <div className="space-y-5">
            {followUpQuestions.map((q, idx) => (
              <div key={q.id || idx} className="space-y-2.5 p-4 rounded-2xl bg-surface-bg/60 border border-surface-muted">
                <div className="text-xs font-bold text-primary flex items-start gap-2">
                  <span className="w-5 h-5 rounded-full bg-secondary/20 text-secondary text-xs flex items-center justify-center shrink-0 mt-0.5 font-bold">
                    {idx + 1}
                  </span>
                  <span>{q.question}</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pl-7 pt-1">
                  {q.options?.map((opt, oIdx) => {
                    const isSelected = followUpAnswers[q.id] === opt;
                    return (
                      <button
                        key={oIdx}
                        type="button"
                        onClick={() => handleOptionSelect(q.id, opt)}
                        className={`text-left p-3 rounded-xl text-xs font-medium border transition-all ${
                          isSelected
                            ? 'bg-secondary text-white border-secondary font-bold shadow-xs'
                            : 'bg-white border-surface-muted hover:border-secondary/40 text-primary/80'
                        }`}
                      >
                        {opt}
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Patient Clinical Profile & Progression Form */}
      <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-6">
        <div className="flex items-center gap-3 border-b border-surface-muted pb-4">
          <div className="p-2 rounded-xl bg-accent/20 text-accent-dark">
            <User className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-base text-primary">Patient Demographics & Medical Profile</h3>
            <p className="text-xs text-primary/60">Helps calibrate age-specific risks and potential drug-condition interactions</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-bold text-primary mb-1">Patient Age</label>
            <input
              type="number"
              name="age"
              min="1"
              max="120"
              value={patientInfo.age || 25}
              onChange={handleInfoChange}
              className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-sm outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-primary mb-1">Biological Gender</label>
            <select
              name="gender"
              value={patientInfo.gender || 'Unspecified'}
              onChange={handleInfoChange}
              className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-sm outline-none bg-white"
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
              <option value="Unspecified">Unspecified</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-primary mb-1">Symptom Trajectory</label>
            <select
              value={progressStatus}
              onChange={(e) => setProgressStatus(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-sm outline-none bg-white font-medium"
            >
              <option value="Unchanged">Unchanged (Constant)</option>
              <option value="Worsening">Worsening over time</option>
              <option value="Improving">Gradually improving</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <div>
            <label className="block text-xs font-bold text-primary mb-1">Known Pre-Existing Conditions</label>
            <input
              type="text"
              name="chronicConditions"
              placeholder="e.g. Asthma, Hypertension, Diabetes, or None"
              value={patientInfo.chronicConditions || ''}
              onChange={handleInfoChange}
              className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-sm outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-primary mb-1">Relevant Medications / Allergies</label>
            <input
              type="text"
              name="allergies"
              placeholder="e.g. Taking Paracetamol, Allergic to Penicillin"
              value={patientInfo.allergies || ''}
              onChange={handleInfoChange}
              className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-sm outline-none"
            />
          </div>
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="flex items-center justify-between pt-4">
        <button
          type="button"
          onClick={() => navigate('/assessment/symptoms')}
          className="inline-flex items-center gap-1.5 px-5 py-3 rounded-xl border border-surface-muted text-primary/70 font-semibold text-xs hover:bg-white transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Symptoms</span>
        </button>

        <button
          type="button"
          onClick={handleRunAnalysis}
          className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-extrabold text-sm shadow-md transition-all hover:scale-102"
        >
          <span>Run AI Triage & Specialization Engine</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

    </div>
  );
};

export default PatientInfoFollowUpPage;
