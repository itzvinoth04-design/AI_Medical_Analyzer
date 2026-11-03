import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAssessment } from '../context/AssessmentContext';
import { symptomService, assessmentService } from '../services/api';
import {
  Stethoscope, Search, Sparkles, AlertCircle, ArrowRight, Check,
  Clock, Thermometer, ShieldAlert, CheckCircle2, ChevronDown, ChevronUp,
  Layers, Mic, MicOff, X, Filter, RefreshCw
} from 'lucide-react';

// Anatomical Body Navigator Tabs
const BODY_TABS = [
  { id: 'all', label: 'All Symptoms', icon: '🩺' },
  { id: 'head', label: 'Head & Brain', icon: '🧠', categoryKey: 'Head and neurological symptoms' },
  { id: 'chest', label: 'Chest & Lungs', icon: '🫁', categoryKey: 'Respiratory symptoms' },
  { id: 'cardio', label: 'Heart & Blood', icon: '❤️', categoryKey: 'Cardiovascular symptoms' },
  { id: 'digestive', label: 'Stomach & Digestion', icon: '🍽️', categoryKey: 'Digestive symptoms' },
  { id: 'joints', label: 'Joints & Back', icon: '🦴', categoryKey: 'Musculoskeletal symptoms' },
  { id: 'general', label: 'Fever & General', icon: '🌡️', categoryKey: 'General symptoms' },
  { id: 'ent', label: 'Ear, Nose & Throat', icon: '👂', categoryKey: 'ENT symptoms' },
  { id: 'skin', label: 'Skin & Allergy', icon: '🧴', categoryKey: 'Skin symptoms' },
  { id: 'urinary', label: 'Urinary Tract', icon: '💧', categoryKey: 'Urinary symptoms' },
];

const SymptomInputPage = () => {
  const navigate = useNavigate();
  const {
    rawText, setRawText,
    selectedSymptoms, setSelectedSymptoms,
    severity, setSeverity,
    durationDays, setDurationDays,
    setFollowUpQuestions
  } = useAssessment();

  const [categories, setCategories] = useState([]);
  const [activeBodyTab, setActiveBodyTab] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [nlpLoading, setNlpLoading] = useState(false);
  const [nlpFeedback, setNlpFeedback] = useState(null);
  const [showPresets, setShowPresets] = useState(false);

  // Voice Recognition (Speech-to-Text) State
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(() => {
    const loadCategories = async () => {
      try {
        const res = await symptomService.getCategories();
        setCategories(res.data.categories || []);
      } catch (err) {
        console.error("Failed to load categories:", err);
      } finally {
        setLoading(false);
      }
    };
    loadCategories();

    // Initialize Web Speech API if supported by browser
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-IN'; // English (India)

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setRawText(prev => prev ? `${prev} ${transcript}` : transcript);
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleVoiceRecording = () => {
    if (!recognitionRef.current) {
      alert("Voice input is not supported in this browser. Please use Google Chrome, Edge, or enter text manually.");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  const handleToggleSymptom = (code) => {
    setSelectedSymptoms(prev =>
      prev.includes(code) ? prev.filter(c => c !== code) : [...prev, code]
    );
  };

  // Instant NLP Entity & Negation Extractor
  const handleRunNlp = async () => {
    if (!rawText.trim()) return;
    setNlpLoading(true);
    try {
      const res = await symptomService.extractNLP(rawText);
      setNlpFeedback(res.data);
      // Auto merge extracted symptoms
      const extractedCodes = res.data.extracted_symptoms.map(s => s.code);
      setSelectedSymptoms(prev => Array.from(new Set([...prev, ...extractedCodes])));
      if (res.data.duration_days) {
        setDurationDays(res.data.duration_days);
      }
      if (res.data.severity) {
        setSeverity(res.data.severity);
      }
    } catch (err) {
      console.error("NLP extraction error:", err);
    } finally {
      setNlpLoading(false);
    }
  };

  // One-Click Demonstration Test Cases (Module 15)
  const applyScenario = (scenario) => {
    setRawText(scenario.text);
    setSelectedSymptoms(scenario.codes);
    setSeverity(scenario.severity);
    setDurationDays(scenario.duration);
    setNlpFeedback(null);
  };

  const scenarios = [
    {
      title: "Case 1: Mild Headache",
      desc: "Nonspecific sign -> Tension/Dehydration check",
      text: "I have been experiencing a mild dull headache since yesterday morning.",
      codes: ["HEADACHE"],
      severity: "Mild",
      duration: 1
    },
    {
      title: "Case 2: Viral Triad",
      desc: "Headache + fever + body pain -> Primary care",
      text: "I have had a headache, mild fever, and generalized body pain for two days.",
      codes: ["FEV", "HEADACHE", "BOD_PAIN"],
      severity: "Moderate",
      duration: 2
    },
    {
      title: "Case 3: Migraine & Vision",
      desc: "Persistent throbbing -> Neurologist triage",
      text: "Severe throbbing one-sided headache with nausea and blurred vision.",
      codes: ["HEADACHE", "VIS_CHANGE", "NAUSEA"],
      severity: "Severe",
      duration: 3
    },
    {
      title: "Case 4: Emergency Stroke",
      desc: "FAST sign -> Critical 112 emergency override",
      text: "Sudden one-sided weakness in arm and slight facial drooping.",
      codes: ["SUD_WEAK", "FACE_DROP"],
      severity: "Severe",
      duration: 1
    },
    {
      title: "Case 5: Stomach Pain",
      desc: "Stomach pain + vomiting -> Dynamic follow-up",
      text: "Experiencing stomach pain and vomiting since yesterday.",
      codes: ["STOM_PAIN", "VOMIT"],
      severity: "Moderate",
      duration: 1
    },
    {
      title: "Case 6: Joint Swelling",
      desc: "Articular sign -> Orthopedic specialist",
      text: "Persistent knee joint pain with visible swelling for 10 days.",
      codes: ["JOINT_PAIN", "JOINT_SWELL"],
      severity: "Moderate",
      duration: 10
    }
  ];

  const handleProceed = async () => {
    if (selectedSymptoms.length === 0 && !rawText.trim()) {
      alert("Please describe your symptoms or select at least one symptom from the list.");
      return;
    }

    try {
      const res = await assessmentService.getFollowUps(selectedSymptoms, rawText);
      setFollowUpQuestions(res.data.questions || []);
    } catch (err) {
      console.error("Failed to fetch follow-ups:", err);
    }

    navigate('/assessment/patient-info');
  };

  // Filter symptoms based on active body tab and search term
  const displayedCategories = categories.filter(c => {
    if (activeBodyTab === 'all') return true;
    const tabObj = BODY_TABS.find(t => t.id === activeBodyTab);
    return tabObj && c.category === tabObj.categoryKey;
  });

  // Flat symptom list for pill display
  const allSymptomMap = {};
  categories.forEach(c => c.symptoms.forEach(s => { allSymptomMap[s.code] = s.name; }));

  return (
    <div className="max-w-5xl mx-auto py-8 space-y-6">
      
      {/* Step Indicator Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-surface-muted pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-md text-[10px] font-black uppercase tracking-wider bg-secondary text-white">
              Step 1 of 3
            </span>
            <span className="text-xs text-primary/50 font-semibold">Triage Intake</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-primary tracking-tight mt-1">
            Intelligent Medical Symptom Input
          </h1>
          <p className="text-xs text-primary/60 mt-0.5">
            Describe symptoms naturally or navigate verified anatomical categories
          </p>
        </div>

        {/* Visual Progress Stepper */}
        <div className="flex items-center gap-2 text-xs font-semibold shrink-0">
          <span className="w-7 h-7 rounded-full bg-secondary text-white flex items-center justify-center font-bold text-xs shadow-xs">
            1
          </span>
          <span className="text-secondary font-bold">Input</span>
          <span className="text-primary/30">→</span>
          <span className="w-7 h-7 rounded-full bg-surface-muted text-primary/60 flex items-center justify-center font-bold text-xs">
            2
          </span>
          <span className="text-primary/60">Follow-up</span>
          <span className="text-primary/30">→</span>
          <span className="w-7 h-7 rounded-full bg-surface-muted text-primary/60 flex items-center justify-center font-bold text-xs">
            3
          </span>
          <span className="text-primary/60">Results</span>
        </div>
      </div>

      {/* Collapsible Quick Test Scenarios */}
      <div className="bg-white rounded-2xl border border-surface-muted shadow-xs overflow-hidden">
        <button
          type="button"
          onClick={() => setShowPresets(!showPresets)}
          className="w-full px-5 py-3.5 flex items-center justify-between text-left hover:bg-surface-bg/50 transition-colors"
        >
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-accent" />
            <span className="text-xs font-bold text-primary">
              Quick Test Scenarios (Cases 1–6)
            </span>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-secondary/10 text-secondary font-bold">
              Demo Presets
            </span>
          </div>
          {showPresets ? <ChevronUp className="w-4 h-4 text-primary/50" /> : <ChevronDown className="w-4 h-4 text-primary/50" />}
        </button>

        {showPresets && (
          <div className="p-4 pt-1 bg-surface-bg/40 border-t border-surface-muted grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
            {scenarios.map((sc, i) => (
              <button
                key={i}
                type="button"
                onClick={() => applyScenario(sc)}
                className="text-left p-2.5 rounded-xl border border-surface-muted bg-white hover:border-secondary hover:bg-secondary/5 transition-all text-xs group shadow-2xs"
              >
                <div className="font-bold text-primary group-hover:text-secondary truncate">{sc.title}</div>
                <div className="text-[10px] text-primary/50 truncate mt-0.5">{sc.desc}</div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Option A: Natural Language & Voice Input Card */}
      <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5">
            <div className="p-2.5 rounded-xl bg-secondary/15 text-secondary">
              <Stethoscope className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-base text-primary">Describe How You Feel (Text or Voice)</h3>
              <p className="text-xs text-primary/60">Type or speak your symptoms in your own words</p>
            </div>
          </div>

          <div className="flex items-center gap-2 self-start sm:self-auto">
            {/* Voice Recognition Button */}
            <button
              type="button"
              onClick={toggleVoiceRecording}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all shadow-xs ${
                isListening
                  ? 'bg-status-emergency text-white animate-pulse'
                  : 'bg-surface-bg text-primary border border-surface-muted hover:border-primary/40'
              }`}
              title="Speak your symptoms using microphone"
            >
              {isListening ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5 text-accent-dark" />}
              <span>{isListening ? 'Listening...' : 'Voice Input'}</span>
            </button>

            {/* Run NLP Button */}
            <button
              type="button"
              onClick={handleRunNlp}
              disabled={nlpLoading || !rawText.trim()}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-bold text-xs shadow-xs transition-colors disabled:opacity-40"
            >
              {nlpLoading ? (
                <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Sparkles className="w-3.5 h-3.5" />
              )}
              <span>Analyze with NLP</span>
            </button>
          </div>
        </div>

        <textarea
          rows={3}
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
          placeholder="Describe how you are feeling. For example, I have been experiencing a headache and mild fever for two days, but no vomiting..."
          className="w-full p-4 rounded-2xl border border-surface-muted focus:border-secondary focus:ring-1 focus:ring-secondary text-sm outline-none resize-y leading-relaxed bg-surface-bg/40 font-normal"
        />

        {/* NLP Feedback Pills */}
        {nlpFeedback && (
          <div className="p-3.5 rounded-2xl bg-secondary/5 border border-secondary/20 space-y-2 text-xs">
            <div className="font-bold text-secondary flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-accent" />
                <span>Extracted Clinical Entities:</span>
              </span>
              <span className="text-[11px] text-primary/50 font-normal">
                Duration: {nlpFeedback.duration_raw} • Severity: {nlpFeedback.severity}
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {nlpFeedback.extracted_symptoms?.map((s) => (
                <span key={s.code} className="px-2.5 py-1 rounded-lg bg-white border border-secondary/30 text-secondary font-semibold">
                  + {s.name}
                </span>
              ))}
              {nlpFeedback.negated_symptoms?.map((s) => (
                <span key={s.code} className="px-2.5 py-1 rounded-lg bg-white border border-status-warning/40 text-status-warning font-semibold line-through">
                  ¬ {s.name} (Negated)
                </span>
              ))}
              {nlpFeedback.body_parts?.map((bp, i) => (
                <span key={i} className="px-2.5 py-1 rounded-lg bg-white border border-surface-muted text-primary/70">
                  📍 {bp}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Global Severity & Duration Selectors */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Severity */}
        <div className="bg-white p-5 rounded-3xl border border-surface-muted shadow-xs space-y-2">
          <label className="text-xs font-bold text-primary flex items-center gap-1.5">
            <Thermometer className="w-4 h-4 text-secondary" />
            <span>Overall Symptom Severity</span>
          </label>
          <div className="grid grid-cols-3 gap-2">
            {['Mild', 'Moderate', 'Severe'].map((lvl) => (
              <button
                key={lvl}
                type="button"
                onClick={() => setSeverity(lvl)}
                className={`py-2 rounded-xl text-xs font-bold border transition-all ${
                  severity === lvl
                    ? lvl === 'Severe'
                      ? 'bg-status-emergency text-white border-status-emergency shadow-xs'
                      : lvl === 'Moderate'
                      ? 'bg-secondary text-white border-secondary shadow-xs'
                      : 'bg-accent text-white border-accent shadow-xs'
                    : 'bg-surface-bg border-surface-muted text-primary/70 hover:bg-white'
                }`}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>

        {/* Duration in Days */}
        <div className="bg-white p-5 rounded-3xl border border-surface-muted shadow-xs space-y-2">
          <label className="text-xs font-bold text-primary flex items-center gap-1.5">
            <Clock className="w-4 h-4 text-secondary" />
            <span>Duration of Symptoms</span>
          </label>
          <div className="flex items-center gap-3">
            <input
              type="range"
              min="1"
              max="30"
              value={durationDays}
              onChange={(e) => setDurationDays(parseInt(e.target.value))}
              className="w-full accent-secondary"
            />
            <span className="px-3 py-1.5 rounded-xl bg-surface-bg border border-surface-muted font-bold text-xs text-primary shrink-0 min-w-[75px] text-center">
              {durationDays} {durationDays === 1 ? 'day' : 'days'}
            </span>
          </div>
        </div>
      </div>

      {/* Option B: Categorized Symptoms by Body Area */}
      <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2.5 rounded-xl bg-accent/20 text-accent-dark">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-base text-primary">Browse Symptoms by Body Area</h3>
              <p className="text-xs text-primary/60">Select symptoms from anatomical categories or search directly</p>
            </div>
          </div>

          {/* Search Box */}
          <div className="relative w-full sm:w-64">
            <Search className="w-4 h-4 text-primary/40 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search symptoms (e.g. fever)..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none bg-surface-bg"
            />
          </div>
        </div>

        {/* Anatomical Body Navigator Tabs */}
        <div className="flex gap-1.5 overflow-x-auto pb-1 text-xs">
          {BODY_TABS.map(tab => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveBodyTab(tab.id)}
              className={`px-3 py-1.5 rounded-xl font-bold whitespace-nowrap transition-all flex items-center gap-1.5 ${
                activeBodyTab === tab.id
                  ? 'bg-secondary text-white shadow-xs'
                  : 'bg-surface-bg text-primary/70 hover:bg-surface-muted/60'
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Active Symptoms Counter Bar */}
        {selectedSymptoms.length > 0 && (
          <div className="p-3.5 rounded-2xl bg-secondary/10 border border-secondary/20 flex flex-wrap items-center justify-between gap-2">
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-xs font-bold text-secondary mr-1">Active Symptoms ({selectedSymptoms.length}):</span>
              {selectedSymptoms.map(code => (
                <span
                  key={code}
                  className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-lg bg-white border border-secondary/30 text-secondary text-xs font-semibold"
                >
                  <span>{allSymptomMap[code] || code}</span>
                  <button
                    type="button"
                    onClick={() => handleToggleSymptom(code)}
                    className="hover:text-status-emergency ml-0.5"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
            <button
              type="button"
              onClick={() => setSelectedSymptoms([])}
              className="text-[11px] font-bold text-status-emergency hover:underline"
            >
              Clear all
            </button>
          </div>
        )}

        {/* Symptoms Grid */}
        <div className="space-y-4 pt-1">
          {displayedCategories.map((catGroup) => {
            const filteredSymptoms = catGroup.symptoms.filter(s =>
              s.name.toLowerCase().includes(searchTerm.toLowerCase())
            );

            if (searchTerm && filteredSymptoms.length === 0) return null;

            return (
              <div key={catGroup.category} className="space-y-2">
                <span className="text-xs font-bold text-primary/60 uppercase tracking-wider block">
                  {catGroup.category}
                </span>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                  {filteredSymptoms.map((sym) => {
                    const isSelected = selectedSymptoms.includes(sym.code);
                    return (
                      <button
                        key={sym.code}
                        type="button"
                        onClick={() => handleToggleSymptom(sym.code)}
                        className={`p-3 rounded-2xl text-left text-xs font-medium border flex items-center justify-between gap-2 transition-all ${
                          isSelected
                            ? 'bg-secondary/10 border-secondary text-secondary font-bold shadow-xs'
                            : 'border-surface-muted hover:border-primary/40 text-primary/80 bg-white'
                        }`}
                      >
                        <span className="truncate">{sym.name}</span>
                        {isSelected ? (
                          <Check className="w-4 h-4 text-secondary shrink-0" />
                        ) : sym.is_red_flag ? (
                          <span className="text-[9px] px-1.5 py-0.5 rounded bg-status-emergency/15 text-status-emergency font-black shrink-0">
                            Red Flag
                          </span>
                        ) : null}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Floating / Sticky Continue Footer */}
      <div className="sticky bottom-4 z-30 bg-white/95 backdrop-blur-md p-4 rounded-2xl border border-surface-muted shadow-xl flex items-center justify-between gap-4">
        <div className="text-xs text-primary/70">
          <strong className="text-primary font-bold">{selectedSymptoms.length}</strong> symptom(s) identified
        </div>

        <button
          type="button"
          onClick={handleProceed}
          className="inline-flex items-center gap-2 px-8 py-3 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-extrabold text-sm shadow-md transition-all hover:scale-102"
        >
          <span>Continue to Patient Details & Follow-Ups</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

    </div>
  );
};

export default SymptomInputPage;
