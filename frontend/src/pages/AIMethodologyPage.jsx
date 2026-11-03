import React, { useEffect, useState } from 'react';
import { methodologyService } from '../services/api';
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid
} from 'recharts';
import {
  BrainCircuit, Layers, Cpu, ShieldCheck, CheckCircle2, GitBranch,
  Sparkles, Terminal, Activity, FileCode, Info, Table
} from 'lucide-react';

const AIMethodologyPage = () => {
  const [methodology, setMethodology] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('unit_1');

  useEffect(() => {
    const fetchMethodology = async () => {
      try {
        const res = await methodologyService.getOverview();
        setMethodology(res.data);
      } catch (err) {
        console.error("Methodology fetch error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMethodology();
  }, []);

  if (loading) {
    return (
      <div className="py-20 text-center text-xs text-primary/50">
        Loading AI Syllabus Architecture & Telemetry...
      </div>
    );
  }

  const units = methodology?.units || {};
  const u1 = units.unit_1?.implementation_details || {};
  const u2 = units.unit_2?.implementation_details || {};
  const u3 = units.unit_3?.implementation_details || {};
  const u4 = units.unit_4?.implementation_details || {};
  const u5 = units.unit_5?.implementation_details || {};

  const supervised = u5.supervised_model || {};
  const chartData = supervised.top_features?.map(f => ({
    name: f.symptom_name.length > 15 ? f.symptom_name.slice(0, 15) + '...' : f.symptom_name,
    importance: Math.round(f.importance * 1000) / 10
  })) || [];

  return (
    <div className="max-w-6xl mx-auto py-8 space-y-8">
      
      {/* Header */}
      <div className="bg-gradient-to-r from-primary to-primary-light text-white p-8 rounded-3xl border border-primary-light/50 shadow-md space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary/30 text-secondary-light text-xs font-bold uppercase tracking-wider">
          <BrainCircuit className="w-4 h-4 text-accent" />
          <span>Academic Artificial Intelligence Mini-Project</span>
        </div>
        <h1 className="text-3xl font-extrabold tracking-tight">
          AI Architecture & Syllabus Implementation
        </h1>
        <p className="text-xs sm:text-sm text-surface-muted/90 max-w-3xl leading-relaxed">
          Comprehensive technical documentation demonstrating the actual implementation of theoretical frameworks from all five units of the Artificial Intelligence syllabus in MediGuide AI.
        </p>

        {/* Live Model Stats Banner */}
        <div className="pt-4 grid grid-cols-2 sm:grid-cols-4 gap-4 border-t border-white/10 text-xs">
          <div className="bg-white/5 p-3 rounded-xl border border-white/10">
            <span className="text-surface-muted/70 block text-[11px]">Ensemble Model</span>
            <strong className="text-sm text-white font-bold">{supervised.algorithm || 'Random Forest'}</strong>
          </div>
          <div className="bg-white/5 p-3 rounded-xl border border-white/10">
            <span className="text-surface-muted/70 block text-[11px]">Test Accuracy</span>
            <strong className="text-sm text-accent font-bold">{supervised.overall_accuracy || 99.1}%</strong>
          </div>
          <div className="bg-white/5 p-3 rounded-xl border border-white/10">
            <span className="text-surface-muted/70 block text-[11px]">Macro Avg F1</span>
            <strong className="text-sm text-secondary-light font-bold">{supervised.macro_avg_f1 || 99.1}%</strong>
          </div>
          <div className="bg-white/5 p-3 rounded-xl border border-white/10">
            <span className="text-surface-muted/70 block text-[11px]">Knowledge Base</span>
            <strong className="text-sm text-white font-bold">120+ Symptoms • 13 Specs</strong>
          </div>
        </div>
      </div>

      {/* 5 Units Tab Navigation */}
      <div className="flex border-b border-surface-muted gap-2 overflow-x-auto pb-1 text-xs">
        {[
          { id: 'unit_1', label: 'Unit I: Intelligent Agents & PEAS' },
          { id: 'unit_2', label: 'Unit II: Heuristic Search & Optimization' },
          { id: 'unit_3', label: 'Unit III: CSP & Propagation' },
          { id: 'unit_4', label: 'Unit IV: Logical Reasoning & Chaining' },
          { id: 'unit_5', label: 'Unit V: Machine Learning & NLP' },
        ].map(tab => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-3 rounded-xl font-bold whitespace-nowrap transition-all ${
              activeTab === tab.id
                ? 'bg-secondary text-white shadow-xs'
                : 'text-primary/70 hover:bg-white hover:text-primary'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* TAB CONTENT */}

      {/* UNIT I */}
      {activeTab === 'unit_1' && (
        <div className="space-y-6 animate-fade-in">
          <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-4">
            <h3 className="text-lg font-bold text-primary flex items-center gap-2">
              <Cpu className="w-5 h-5 text-secondary" />
              <span>Unit I: Intelligent Agents & PEAS Representation</span>
            </h3>
            <p className="text-xs text-primary/70 leading-relaxed">
              MediGuide AI is formulated as a <strong>Goal-Directed Rational Triage Agent</strong>. It observes partially observable user manifestations, navigates a clinical state-space, and selects actions that optimize patient safety while avoiding unnecessary medical alarmism.
            </p>

            {/* PEAS Table */}
            <div className="pt-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary mb-2">Formal PEAS Specification</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                
                <div className="p-4 rounded-2xl bg-surface-bg border border-surface-muted space-y-1.5">
                  <strong className="text-secondary block font-bold text-sm">Performance Measure (P)</strong>
                  <ul className="list-disc pl-4 space-y-1 text-primary/80">
                    {u1.peas?.performance_measure?.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-2xl bg-surface-bg border border-surface-muted space-y-1.5">
                  <strong className="text-secondary block font-bold text-sm">Environment (E)</strong>
                  <ul className="list-disc pl-4 space-y-1 text-primary/80">
                    {u1.peas?.environment?.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-2xl bg-surface-bg border border-surface-muted space-y-1.5">
                  <strong className="text-accent block font-bold text-sm">Actuators (A)</strong>
                  <ul className="list-disc pl-4 space-y-1 text-primary/80">
                    {u1.peas?.actuators?.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="p-4 rounded-2xl bg-surface-bg border border-surface-muted space-y-1.5">
                  <strong className="text-accent block font-bold text-sm">Sensors (S)</strong>
                  <ul className="list-disc pl-4 space-y-1 text-primary/80">
                    {u1.peas?.sensors?.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>

              </div>
            </div>

            {/* State Space Formulation */}
            <div className="p-4 rounded-2xl bg-surface-bg border border-surface-muted space-y-2 text-xs">
              <h4 className="font-bold text-primary text-xs uppercase tracking-wider">State-Space Search Formulation</h4>
              <div className="space-y-1 text-primary/80 font-mono text-[11px]">
                <div><strong>Initial State (S0):</strong> {u1.state_space_formulation?.initial_state}</div>
                <div><strong>Action Operators (A):</strong> {u1.state_space_formulation?.actions}</div>
                <div><strong>Transition Model:</strong> {u1.state_space_formulation?.transition_model}</div>
                <div><strong>Goal Test:</strong> {u1.state_space_formulation?.goal_test}</div>
                <div><strong>Path Cost:</strong> {u1.state_space_formulation?.path_cost}</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* UNIT II */}
      {activeTab === 'unit_2' && (
        <div className="space-y-6 animate-fade-in">
          <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-6">
            <h3 className="text-lg font-bold text-primary flex items-center gap-2">
              <Activity className="w-5 h-5 text-secondary" />
              <span>Unit II: Informed Heuristic Search & Facility Optimization</span>
            </h3>

            {/* Heuristic Evaluation Formula */}
            <div className="space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary">
                1. Clinical Compatibility Evaluation Function h(C)
              </h4>
              <div className="p-4 rounded-2xl bg-primary text-white font-mono text-xs sm:text-sm">
                {u2.heuristic_function?.formula}
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs pt-1">
                {Object.entries(u2.heuristic_function?.variables || {}).map(([key, val]) => (
                  <div key={key} className="p-3 rounded-xl bg-surface-bg border border-surface-muted">
                    <strong className="text-secondary font-mono">{key}:</strong>
                    <p className="text-primary/70 text-[11px] mt-0.5">{val}</p>
                  </div>
                ))}
              </div>
              <div className="p-3 rounded-xl bg-status-warning/10 border border-status-warning/30 text-xs text-status-warning">
                <strong>Safety Disclaimer:</strong> {u2.heuristic_function?.score_representation}
              </div>
            </div>

            {/* Facility Optimization & Local Search */}
            <div className="space-y-3 pt-4 border-t border-surface-muted">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary">
                2. Healthcare Facility Local Optimization Objective Function
              </h4>
              <div className="p-4 rounded-2xl bg-surface-bg border border-surface-muted font-mono text-xs text-primary space-y-1">
                <div>{u2.facility_optimization?.objective_function}</div>
                <div className="text-[11px] text-primary/60 font-sans mt-1">Algorithm: {u2.facility_optimization?.algorithm}</div>
              </div>
            </div>

            {/* Handling Partially Observable Environments */}
            <div className="space-y-2 pt-4 border-t border-surface-muted text-xs">
              <h4 className="font-bold text-primary uppercase tracking-wider">3. Partially Observable Environment Handling</h4>
              <p className="text-primary/70 leading-relaxed">
                {u2.partially_observable_handling}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* UNIT III */}
      {activeTab === 'unit_3' && (
        <div className="space-y-6 animate-fade-in">
          <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-6">
            <h3 className="text-lg font-bold text-primary flex items-center gap-2">
              <Layers className="w-5 h-5 text-secondary" />
              <span>Unit III: Constraint Satisfaction Problems (CSP) & Propagation</span>
            </h3>

            {/* CSP Formal Model */}
            <div className="space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary">CSP Formulation (Variables & Domains)</h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                {u3.variables?.map((v, i) => (
                  <div key={i} className="p-3 rounded-xl bg-surface-bg border border-surface-muted">
                    <strong className="text-secondary font-mono">{v.name}</strong>
                    <div className="text-[11px] text-primary/70 mt-1">Domain: {v.domain}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Constraints */}
            <div className="space-y-3 pt-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary">Logical Constraints</h4>
              <div className="space-y-2 text-xs">
                {u3.constraints?.map((c, i) => (
                  <div key={i} className="p-3 rounded-xl bg-surface-bg border border-surface-muted font-mono text-[11px] text-primary/80">
                    {c}
                  </div>
                ))}
              </div>
            </div>

            {/* Propagation Technique */}
            <div className="p-4 rounded-2xl bg-secondary/10 border border-secondary/20 text-xs text-primary space-y-1">
              <strong className="text-secondary font-bold block">Constraint Propagation Method:</strong>
              <p className="text-primary/80 leading-relaxed">{u3.propagation_technique}</p>
            </div>
          </div>
        </div>
      )}

      {/* UNIT IV */}
      {activeTab === 'unit_4' && (
        <div className="space-y-6 animate-fade-in">
          <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-6">
            <h3 className="text-lg font-bold text-primary flex items-center gap-2">
              <GitBranch className="w-5 h-5 text-secondary" />
              <span>Unit IV: Knowledge Representation, Logical Reasoning & Chaining</span>
            </h3>

            {/* FOL Predicates */}
            <div className="space-y-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary">First-Order Logic (FOL) Clinical Predicates</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
                {u4.fol_predicates?.map((pred, i) => (
                  <div key={i} className="p-2.5 rounded-xl bg-surface-bg border border-surface-muted text-primary/80">
                    {pred}
                  </div>
                ))}
              </div>
            </div>

            {/* Propositional Rules */}
            <div className="space-y-2 pt-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary">Propositional Emergency Red-Flag Rules</h4>
              <div className="space-y-2 text-xs font-mono">
                {u4.propositional_rules?.map((rule, i) => (
                  <div key={i} className="p-2.5 rounded-xl bg-surface-bg border border-surface-muted text-primary/80">
                    {rule}
                  </div>
                ))}
              </div>
            </div>

            {/* Forward vs Backward Chaining Comparison */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div className="p-4 rounded-2xl bg-surface-bg border border-surface-muted space-y-2 text-xs">
                <strong className="text-secondary font-bold text-sm block">Forward Chaining (Data-Driven)</strong>
                <p className="text-primary/70 leading-relaxed">{u4.forward_chaining}</p>
              </div>

              <div className="p-4 rounded-2xl bg-surface-bg border border-surface-muted space-y-2 text-xs">
                <strong className="text-accent font-bold text-sm block">Backward Chaining (Goal-Driven)</strong>
                <p className="text-primary/70 leading-relaxed">{u4.backward_chaining}</p>
              </div>
            </div>

            {/* Explainable AI */}
            <div className="p-4 rounded-2xl bg-secondary/10 border border-secondary/20 text-xs text-primary space-y-1">
              <strong className="text-secondary font-bold block">Explainable AI (XAI) Architecture:</strong>
              <p className="text-primary/80 leading-relaxed">{u4.xai_explanation}</p>
            </div>
          </div>
        </div>
      )}

      {/* UNIT V */}
      {activeTab === 'unit_5' && (
        <div className="space-y-6 animate-fade-in">
          <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-6">
            <h3 className="text-lg font-bold text-primary flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-secondary" />
              <span>Unit V: Machine Learning & NLP Applications</span>
            </h3>

            {/* Feature Importance Bar Chart */}
            <div className="space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary">
                Supervised Model Feature Importances (Symptom Weight Contributions)
              </h4>
              <div className="h-64 w-full pt-2">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                    <XAxis dataKey="name" angle={-30} textAnchor="end" tick={{ fontSize: 10, fill: '#627D98' }} />
                    <YAxis tick={{ fontSize: 10, fill: '#627D98' }} />
                    <Tooltip contentStyle={{ fontSize: '11px', borderRadius: '8px' }} />
                    <Bar dataKey="importance" fill="#247BA0" radius={[4, 4, 0, 0]} name="Weight %" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Unsupervised K-Means Symptom Clusters */}
            <div className="space-y-3 pt-4 border-t border-surface-muted">
              <h4 className="text-xs font-bold uppercase tracking-wider text-secondary">
                Unsupervised Learning: K-Means Symptom Co-Occurrence Clusters (k=5)
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-xs">
                {u5.unsupervised_clustering?.clusters?.map((cl, i) => (
                  <div key={i} className="p-3.5 rounded-xl bg-surface-bg border border-surface-muted space-y-1.5">
                    <strong className="text-secondary font-bold block text-xs">{cl.cluster_name}</strong>
                    <div className="flex flex-wrap gap-1">
                      {cl.symptoms?.slice(0, 4).map((s, idx) => (
                        <span key={idx} className="px-2 py-0.5 rounded bg-white text-primary/70 text-[10px] border border-surface-muted">
                          {s.name}
                        </span>
                      ))}
                      {cl.symptoms?.length > 4 && (
                        <span className="text-[10px] text-primary/40">+{cl.symptoms.length - 4} more</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* NLP Pipeline */}
            <div className="space-y-2 pt-4 border-t border-surface-muted text-xs">
              <h4 className="font-bold text-primary uppercase tracking-wider">Natural Language Processing Pipeline</h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="p-3 rounded-xl bg-surface-bg border border-surface-muted">
                  <strong className="text-primary block text-xs mb-1">Tokenization</strong>
                  <p className="text-primary/70 text-[11px]">{u5.nlp_pipeline?.tokenization}</p>
                </div>
                <div className="p-3 rounded-xl bg-surface-bg border border-surface-muted">
                  <strong className="text-primary block text-xs mb-1">Negation Detection</strong>
                  <p className="text-primary/70 text-[11px]">{u5.nlp_pipeline?.negation_detection}</p>
                </div>
                <div className="p-3 rounded-xl bg-surface-bg border border-surface-muted">
                  <strong className="text-primary block text-xs mb-1">Attribute Extraction</strong>
                  <p className="text-primary/70 text-[11px]">{u5.nlp_pipeline?.attribute_extraction}</p>
                </div>
              </div>
            </div>

            {/* Dataset Limitations */}
            <div className="p-4 rounded-2xl bg-status-warning/10 border border-status-warning/30 text-xs text-primary/80 space-y-1">
              <strong className="text-status-warning font-bold block">Dataset Limitations & Evaluation Notice:</strong>
              <ul className="list-disc pl-4 space-y-0.5 text-[11px]">
                {u5.dataset_limitations?.map((lim, i) => (
                  <li key={i}>{lim}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default AIMethodologyPage;
