import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Activity, Lock, Mail, ArrowRight, AlertCircle, Sparkles,
  ShieldCheck, Eye, EyeOff, BrainCircuit, HeartPulse, CheckCircle2
} from 'lucide-react';

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const loggedUser = await login(email, password);
      if (loggedUser?.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Invalid credentials. Please verify your email and password.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickFill = async (demoEmail, demoPassword) => {
    setEmail(demoEmail);
    setPassword(demoPassword);
    setError('');
    setLoading(true);
    try {
      const loggedUser = await login(demoEmail, demoPassword);
      if (loggedUser?.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError('Demo login failed. Please ensure the backend database is seeded.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl w-full grid grid-cols-1 md:grid-cols-12 rounded-3xl overflow-hidden border border-surface-muted shadow-2xl bg-white">
        
        {/* Left Branding / Platform Panel (5 cols) */}
        <div className="md:col-span-5 bg-gradient-to-br from-primary via-primary-dark to-[#081726] text-white p-8 sm:p-10 flex flex-col justify-between relative overflow-hidden">
          <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 rounded-full bg-secondary/20 blur-2xl pointer-events-none" />
          
          <div className="relative z-10 space-y-6">
            <div className="flex items-center gap-2.5">
              <div className="w-10 h-10 rounded-xl bg-secondary flex items-center justify-center text-white shadow-md">
                <Activity className="w-5 h-5" />
              </div>
              <div>
                <span className="text-lg font-black tracking-tight block leading-tight">MediGuide AI</span>
                <span className="text-[10px] text-accent font-bold uppercase tracking-wider block">Clinical Triage Portal</span>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-extrabold tracking-tight leading-snug">
                Intelligent Medical Symptom Analyzer
              </h3>
              <div className="mt-4 flex flex-wrap gap-2 text-[11px] font-semibold">
                <span className="px-3 py-1 rounded-lg bg-white/10 text-secondary-light border border-white/10">Clinical Triage</span>
                <span className="px-3 py-1 rounded-lg bg-white/10 text-accent border border-white/10">Chennai Hospitals</span>
                <span className="px-3 py-1 rounded-lg bg-white/10 text-white border border-white/10">Doctor Routing</span>
              </div>
            </div>
          </div>

          <div className="relative z-10 pt-6 border-t border-white/10 text-[11px] text-surface-muted/60 space-y-1">
            <strong className="text-white block font-semibold">Rajalakshmi Engineering College (REC)</strong>
            <div className="text-accent">Vinoth S (240701592) & Team</div>
          </div>
        </div>

        {/* Right Form Card (7 cols) */}
        <div className="md:col-span-7 p-8 sm:p-10 flex flex-col justify-center space-y-5">
          
          <div>
            <h2 className="text-2xl font-extrabold text-primary tracking-tight">Sign In</h2>
            <span className="text-[11px] font-bold text-accent uppercase tracking-wider">Access Clinical Dashboard</span>
          </div>

          {/* Quick-Fill One-Click Demo Buttons */}
          <div className="p-3 rounded-2xl bg-surface-bg border border-surface-muted space-y-2">
            <span className="text-[11px] font-bold text-primary/70 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-secondary" />
              <span>One-Click Demo Profiles:</span>
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => handleQuickFill('patient@mediguide.ai', 'Patient@123')}
                disabled={loading}
                className="text-left px-3 py-2 rounded-xl bg-white border border-secondary/30 hover:border-secondary hover:bg-secondary/5 text-primary text-xs font-semibold transition-all group"
              >
                <div className="text-secondary font-bold group-hover:underline">Vinoth S (Patient)</div>
                <div className="text-[10px] text-primary/50">patient@mediguide.ai</div>
              </button>
              <button
                type="button"
                onClick={() => handleQuickFill('admin@mediguide.ai', 'Admin@123')}
                disabled={loading}
                className="text-left px-3 py-2 rounded-xl bg-white border border-primary/30 hover:border-primary hover:bg-primary/5 text-primary text-xs font-semibold transition-all group"
              >
                <div className="text-primary font-bold group-hover:underline">System Administrator</div>
                <div className="text-[10px] text-primary/50">admin@mediguide.ai</div>
              </button>
            </div>
          </div>

          {error && (
            <div className="p-3.5 rounded-xl bg-status-emergency/10 border border-status-emergency/30 text-status-emergency text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-primary mb-1">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-primary/40 absolute left-3 top-3.5" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full pl-9 pr-4 py-2.5 rounded-xl border border-surface-muted focus:border-secondary focus:ring-1 focus:ring-secondary text-xs sm:text-sm outline-none transition-all"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-bold text-primary">Password</label>
                <button
                  type="button"
                  onClick={() => handleQuickFill('patient@mediguide.ai', 'Patient@123')}
                  className="text-[11px] font-semibold text-secondary hover:underline"
                >
                  Use Demo Password
                </button>
              </div>
              <div className="relative">
                <Lock className="w-4 h-4 text-primary/40 absolute left-3 top-3.5" />
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-9 pr-10 py-2.5 rounded-xl border border-surface-muted focus:border-secondary focus:ring-1 focus:ring-secondary text-xs sm:text-sm outline-none transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3 text-primary/40 hover:text-primary"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-extrabold text-sm shadow-md transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  <span>Sign In & Open Dashboard</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <div className="text-center text-xs text-primary/60 pt-2 border-t border-surface-muted">
            New to MediGuide AI?{' '}
            <Link to="/register" className="font-extrabold text-secondary hover:underline">
              Create a free patient account
            </Link>
          </div>

        </div>

      </div>
    </div>
  );
};

export default LoginPage;
