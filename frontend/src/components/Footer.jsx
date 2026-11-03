import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, ShieldCheck, HeartPulse, ExternalLink } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-primary text-white pt-12 pb-8 border-t border-primary-light">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Main Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 pb-8 border-b border-white/10">
          
          {/* Brand Info */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-secondary flex items-center justify-center text-white font-bold">
                <Activity className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold tracking-tight text-white">MediGuide AI</span>
            </div>
            <p className="text-sm text-surface-muted/80 max-w-md leading-relaxed">
              Intelligent medical triage decision-support platform combining Natural Language Processing, clinical ontology knowledge representation, heuristic search, forward/backward reasoning, and real Chennai healthcare discovery.
            </p>
            <div className="flex flex-wrap gap-2 pt-1">
              <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-white/10 text-accent">Unit I: Intelligent Agents</span>
              <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-white/10 text-secondary-light">Unit II: Heuristic Search</span>
              <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-white/10 text-accent">Unit III: CSP & Propagation</span>
              <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-white/10 text-secondary-light">Unit IV: Logical Reasoning</span>
              <span className="px-2.5 py-1 rounded-md text-[11px] font-semibold bg-white/10 text-accent">Unit V: Machine Learning</span>
            </div>
          </div>

          {/* Academic Attribution */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-accent">Academic Mini-Project</h4>
            <div className="text-xs text-surface-muted/90 space-y-1.5 leading-relaxed">
              <p className="font-semibold text-white">Artificial Intelligence Mini Project</p>
              <p>Department of Computer Science & Engineering</p>
              <p className="font-medium text-secondary-light">Rajalakshmi Engineering College</p>
              <p className="pt-1">
                <strong>Project Lead:</strong> Vinoth S <span className="font-mono text-[11px] text-accent">(240701592)</span>
              </p>
            </div>
          </div>

          {/* Quick Navigation */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-accent">Quick Links</h4>
            <ul className="space-y-2 text-xs text-surface-muted/80">
              <li>
                <Link to="/assessment/symptoms" className="hover:text-accent transition-colors">Start Health Assessment</Link>
              </li>
              <li>
                <Link to="/hospitals" className="hover:text-accent transition-colors">Find Chennai Hospitals</Link>
              </li>
              <li>
                <Link to="/ai-methodology" className="hover:text-accent transition-colors">5-Unit AI Syllabus Methodology</Link>
              </li>
              <li>
                <a href="tel:112" className="text-status-emergency font-bold hover:underline flex items-center gap-1">
                  National Emergency: 112 (India)
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Safety Disclaimer Banner */}
        <div className="pt-6 pb-4">
          <div className="p-3.5 rounded-xl bg-primary-dark/80 border border-white/10 flex items-start gap-3">
            <ShieldCheck className="w-5 h-5 text-accent shrink-0 mt-0.5" />
            <p className="text-xs text-surface-muted/90 leading-relaxed">
              <strong>MANDATORY MEDICAL SAFETY DISCLAIMER:</strong> This web application provides preliminary AI-assisted health information and healthcare navigation. It does NOT provide a confirmed medical diagnosis, prescription, or clinical treatment. The Condition Compatibility Score reflects knowledge-base ontology congruence, not a diagnostic certainty probability. Always consult a qualified physician or healthcare provider for any medical condition. In emergency situations, immediately call <strong>112</strong> or visit the nearest hospital casualty.
            </p>
          </div>
        </div>

        {/* Bottom Credits */}
        <div className="pt-4 flex flex-col sm:flex-row items-center justify-between text-xs text-surface-muted/60 gap-2">
          <div>
            © 2026 MediGuide AI. Developed for Academic AI Demonstration.
          </div>
          <div className="flex items-center gap-4">
            <Link to="/ai-methodology" className="hover:text-white">AI Documentation</Link>
            <span>•</span>
            <span className="text-accent font-medium">Chennai, Tamil Nadu</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
