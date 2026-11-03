import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAssessment } from '../context/AssessmentContext';
import { assessmentService } from '../services/api';
import {
  Activity, BrainCircuit, ShieldCheck, Cpu, Stethoscope, CheckCircle2
} from 'lucide-react';

const STAGES = [
  { id: 1, name: "NLP Entity Extraction & Negation Scope", unit: "Unit V: NLP", desc: "Parsing syntactic tokens, detecting negations, and mapping clinical synonyms." },
  { id: 2, name: "Propositional Logic Red-Flag Guard", unit: "Unit IV: Propositional Logic", desc: "Checking FAST stroke criteria, substernal chest signs, and emergency alerts." },
  { id: 3, name: "Forward & Backward Clinical Chaining", unit: "Unit IV: Knowledge Chaining", desc: "Traversing medical ontology Horn clauses and verifying missing criteria." },
  { id: 4, name: "Random Forest Supervised Classification", unit: "Unit V: Machine Learning", desc: "Executing ensemble probability weighting and feature importance scoring." },
  { id: 5, name: "CSP Doctor & Chennai Hospital Solver", unit: "Unit III: Constraint Satisfaction", desc: "Propagating constraints to select appropriate primary care vs specialist routing." }
];

const AnalysisLoadingPage = () => {
  const navigate = useNavigate();
  const {
    rawText, selectedSymptoms, severity, durationDays,
    progressStatus, patientInfo, followUpAnswers,
    setAssessmentResults
  } = useAssessment();

  const [currentStageIndex, setCurrentStageIndex] = useState(0);

  useEffect(() => {
    // Stage increment animation interval
    const interval = setInterval(() => {
      setCurrentStageIndex(prev => (prev < STAGES.length - 1 ? prev + 1 : prev));
    }, 700);

    // Call API in parallel
    const runInference = async () => {
      try {
        const payload = {
          raw_text: rawText,
          selected_symptom_codes: selectedSymptoms,
          severity: severity,
          duration_days: durationDays,
          progress_status: progressStatus,
          age: patientInfo.age || 25,
          gender: patientInfo.gender || 'Unspecified',
          chronic_conditions: patientInfo.chronicConditions,
          follow_up_answers: followUpAnswers
        };

        const res = await assessmentService.analyze(payload);
        setAssessmentResults(res.data);

        // Small delay so user observes the multi-stage animation
        setTimeout(() => {
          navigate('/assessment/results');
        }, 3200);

      } catch (err) {
        console.error("AI Analysis error:", err);
        alert("An error occurred during AI analysis. Please review your input.");
        navigate('/assessment/symptoms');
      }
    };

    runInference();

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-[75vh] flex flex-col items-center justify-center py-12 px-4 max-w-xl mx-auto space-y-8">
      
      {/* Central Pulsing AI Icon */}
      <div className="relative flex items-center justify-center">
        <div className="w-24 h-24 rounded-3xl bg-gradient-to-tr from-secondary to-accent flex items-center justify-center text-white shadow-xl shadow-secondary/30 animate-pulse">
          <BrainCircuit className="w-12 h-12" />
        </div>
        <div className="absolute w-32 h-32 rounded-3xl border-2 border-secondary/30 animate-ping pointer-events-none" />
      </div>

      <div className="text-center space-y-2">
        <h2 className="text-2xl font-extrabold text-primary tracking-tight">
          MediGuide AI Hybrid Engine Processing
        </h2>
        <p className="text-xs text-primary/60 max-w-md">
          Synthesizing knowledge graph reasoning, supervised machine learning, and clinical safety heuristics...
        </p>
      </div>

      {/* Animated Multi-Stage Progress Stepper */}
      <div className="w-full bg-white p-6 rounded-3xl border border-surface-muted shadow-md space-y-4">
        {STAGES.map((stg, idx) => {
          const isDone = idx < currentStageIndex;
          const isCurrent = idx === currentStageIndex;

          return (
            <div
              key={stg.id}
              className={`flex items-start gap-3 p-3 rounded-xl transition-all ${
                isCurrent ? 'bg-secondary/10 border border-secondary/30' : ''
              }`}
            >
              <div className="mt-0.5 shrink-0">
                {isDone ? (
                  <CheckCircle2 className="w-5 h-5 text-status-success" />
                ) : isCurrent ? (
                  <div className="w-5 h-5 rounded-full border-2 border-secondary border-t-transparent animate-spin" />
                ) : (
                  <div className="w-5 h-5 rounded-full bg-surface-muted/80 text-[10px] font-bold text-primary/50 flex items-center justify-center">
                    {stg.id}
                  </div>
                )}
              </div>

              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className={`text-xs font-bold ${isCurrent ? 'text-secondary' : isDone ? 'text-primary' : 'text-primary/50'}`}>
                    {stg.name}
                  </span>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-surface-bg text-accent">
                    {stg.unit}
                  </span>
                </div>
                <p className="text-[11px] text-primary/60 mt-0.5">{stg.desc}</p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="text-[11px] text-primary/40 text-center italic">
        Evaluating across 120+ clinical ontological nodes • Chennai hospital discovery enabled
      </div>

    </div>
  );
};

export default AnalysisLoadingPage;
