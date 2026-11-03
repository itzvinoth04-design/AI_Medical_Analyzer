import React from 'react';
import { Link } from 'react-router-dom';
import {
  Activity, ShieldAlert, ArrowRight, BrainCircuit, Stethoscope, MapPin,
  CheckCircle2, Sparkles, FileText, ChevronRight, HelpCircle, AlertCircle
} from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="space-y-16 py-8">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary via-primary-dark to-[#091522] text-white p-8 sm:p-14 border border-primary-light/50 shadow-2xl">
        {/* Subtle background glow */}
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 rounded-full bg-secondary/20 blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-80 h-80 rounded-full bg-accent/20 blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary/20 border border-secondary/40 text-secondary-light text-xs font-bold tracking-wide uppercase">
            <Sparkles className="w-3.5 h-3.5 text-accent" />
            <span>Intelligent Healthcare Platform</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            MediGuide <span className="text-secondary-light">AI</span>
            <span className="block text-xl sm:text-2xl font-medium text-surface-muted/90 mt-2">
              Medical Symptom Analyzer & Doctor Recommendation System
            </span>
          </h1>

          <p className="text-sm sm:text-base text-surface-muted/80 leading-relaxed max-w-2xl">
            A clinical decision-support platform providing transparent symptom evaluation, condition compatibility insights, and verified Chennai healthcare recommendations.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <Link
              to="/assessment/symptoms"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-secondary to-secondary-dark text-white font-bold text-sm shadow-lg shadow-secondary/25 hover:shadow-secondary/40 hover:scale-102 transition-all"
            >
              <Stethoscope className="w-5 h-5" />
              <span>Start Health Assessment</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>

            <Link
              to="/hospitals"
              className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-white/10 hover:bg-white/15 text-white font-semibold text-sm border border-white/15 transition-colors"
            >
              <MapPin className="w-4 h-4 text-accent" />
              <span>Explore Chennai Hospitals</span>
            </Link>
          </div>

          {/* Quick Metrics */}
          <div className="pt-6 border-t border-white/10 grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
            <div>
              <div className="font-extrabold text-lg text-white">120+</div>
              <div className="text-surface-muted/70">Clinical Symptoms</div>
            </div>
            <div>
              <div className="font-extrabold text-lg text-secondary-light">13</div>
              <div className="text-surface-muted/70">Medical Specialties</div>
            </div>
            <div>
              <div className="font-extrabold text-lg text-accent">Real-World</div>
              <div className="text-surface-muted/70">Chennai Hospitals</div>
            </div>
            <div>
              <div className="font-extrabold text-lg text-white">99.1%</div>
              <div className="text-surface-muted/70">Model Accuracy</div>
            </div>
          </div>
        </div>
      </section>

      {/* Safety Principle Banner */}
      <section className="bg-white p-6 rounded-2xl border border-surface-muted shadow-xs">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-xl bg-accent/10 text-accent shrink-0">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-primary">Safety-First Clinical Triage</h3>
            <p className="text-sm text-primary/70 mt-1 leading-relaxed">
              MediGuide AI ensures non-alarmist assessments: isolated nonspecific symptoms (such as mild headache) are never escalated to extreme conditions without hallmark signs. Critical red flags (such as stroke or chest pain) immediately trigger emergency 112 guidance.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works (4-Step Pipeline) */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <span className="text-xs font-bold text-accent tracking-widest uppercase">How It Works</span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-primary tracking-tight">4-Step Guided Triage</h2>
          <p className="text-sm text-primary/60">An intelligent triage pipeline engineered for accuracy, transparency, and safety.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-2xl border border-surface-muted shadow-xs relative">
            <div className="w-8 h-8 rounded-lg bg-primary/10 text-primary font-bold flex items-center justify-center text-sm mb-4">01</div>
            <h4 className="font-bold text-primary text-base mb-1">Describe Symptoms</h4>
            <p className="text-xs text-primary/70 leading-relaxed">
              Express how you feel naturally using voice or text, or select categorized symptoms by anatomical region.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-surface-muted shadow-xs relative">
            <div className="w-8 h-8 rounded-lg bg-secondary/15 text-secondary font-bold flex items-center justify-center text-sm mb-4">02</div>
            <h4 className="font-bold text-primary text-base mb-1">Targeted Follow-Ups</h4>
            <p className="text-xs text-primary/70 leading-relaxed">
              Answer targeted clinical questions to clarify onset, severity, and associated warning signs.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-surface-muted shadow-xs relative">
            <div className="w-8 h-8 rounded-lg bg-accent/20 text-accent-dark font-bold flex items-center justify-center text-sm mb-4">03</div>
            <h4 className="font-bold text-primary text-base mb-1">Compatibility Scoring</h4>
            <p className="text-xs text-primary/70 leading-relaxed">
              The hybrid inference engine computes transparent 0–100 compatibility scores with full explanation.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-surface-muted shadow-xs relative">
            <div className="w-8 h-8 rounded-lg bg-status-success/15 text-status-success font-bold flex items-center justify-center text-sm mb-4">04</div>
            <h4 className="font-bold text-primary text-base mb-1">Doctor & Hospital Care</h4>
            <p className="text-xs text-primary/70 leading-relaxed">
              Receive specialist recommendations and discover nearby verified Chennai clinics and hospitals.
            </p>
          </div>
        </div>
      </section>

      {/* Transparent AI Showcase */}
      <section className="bg-white p-8 rounded-3xl border border-surface-muted shadow-xs flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2 max-w-xl">
          <span className="text-xs font-bold text-secondary tracking-widest uppercase">Explainable AI</span>
          <h2 className="text-2xl font-extrabold text-primary tracking-tight">Transparent Clinical Decision Support</h2>
          <p className="text-xs sm:text-sm text-primary/70 leading-relaxed">
            Every recommendation explains why a condition was considered, which symptoms were confirmed, and which hallmark signs were missing.
          </p>
        </div>
        <Link
          to="/ai-methodology"
          className="inline-flex items-center gap-1.5 px-5 py-3 rounded-xl bg-surface-bg hover:bg-secondary/10 border border-surface-muted text-xs font-bold text-secondary transition-colors shrink-0"
        >
          <span>Explore AI Methodology</span>
          <ChevronRight className="w-4 h-4" />
        </Link>
      </section>

      {/* Chennai Healthcare Directory Feature */}
      <section className="bg-gradient-to-r from-primary to-secondary p-8 rounded-3xl text-white flex flex-col md:flex-row items-center justify-between gap-6 shadow-lg">
        <div className="space-y-2 max-w-xl">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 text-xs font-bold text-accent">
            <MapPin className="w-3.5 h-3.5" />
            <span>Chennai, Tamil Nadu</span>
          </div>
          <h3 className="text-2xl font-extrabold tracking-tight">Verified Chennai Healthcare Directory</h3>
          <p className="text-xs sm:text-sm text-surface-muted/90 leading-relaxed">
            Real data from OpenStreetMap & verified registries covering T. Nagar, Adyar, Velachery, Anna Nagar, Tambaram, Porur, Guindy, and OMR. Calculates precise travel distance via the Haversine formula with verified OPD timings and published consultation fees.
          </p>
        </div>
        <Link
          to="/hospitals"
          className="px-6 py-3 rounded-xl bg-white text-primary font-bold text-sm hover:bg-surface-bg transition-colors shadow-md shrink-0"
        >
          Explore Hospital Map
        </Link>
      </section>

      {/* Final Call to Action */}
      <section className="text-center py-6 space-y-4">
        <h3 className="text-xl sm:text-2xl font-extrabold text-primary">Ready to Assess Your Health Symptoms?</h3>
        <p className="text-xs sm:text-sm text-primary/60 max-w-md mx-auto">
          Start a private, AI-guided assessment in seconds. Download your clinical report as a PDF upon completion.
        </p>
        <div>
          <Link
            to="/assessment/symptoms"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-bold text-sm shadow-md transition-all hover:scale-102"
          >
            <Stethoscope className="w-4 h-4" />
            <span>Start Free Assessment Now</span>
          </Link>
        </div>
      </section>

    </div>
  );
};

export default LandingPage;
