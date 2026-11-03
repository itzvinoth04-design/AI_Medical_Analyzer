import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Activity, User, Mail, Lock, Phone, MapPin, Calendar, AlertCircle,
  ArrowRight, ShieldCheck, CheckCircle2, Eye, EyeOff
} from 'lucide-react';

const RegisterPage = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    password: '',
    age: 22,
    gender: 'Male',
    location: 'Chennai, Tamil Nadu',
    chronic_conditions: '',
    allergies: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(formData);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed. Please check your information.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl w-full grid grid-cols-1 md:grid-cols-12 rounded-3xl overflow-hidden border border-surface-muted shadow-2xl bg-white">
        
        {/* Left Branding / Patient Safety Hero (5 cols) */}
        <div className="md:col-span-5 bg-gradient-to-br from-primary via-primary-dark to-[#081726] text-white p-8 sm:p-10 flex flex-col justify-between relative overflow-hidden">
          <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 rounded-full bg-accent/20 blur-2xl pointer-events-none" />

          <div className="relative z-10 space-y-6">
            <div className="flex items-center gap-2.5">
              <div className="w-10 h-10 rounded-xl bg-accent flex items-center justify-center text-primary-dark shadow-md">
                <Activity className="w-5 h-5 text-white" />
              </div>
              <div>
                <span className="text-lg font-black tracking-tight block leading-tight">MediGuide AI</span>
                <span className="text-[10px] text-accent font-bold uppercase tracking-wider block">Patient Registration</span>
              </div>
            </div>

            <div className="space-y-2">
              <h3 className="text-xl font-extrabold tracking-tight leading-snug">
                Private & Secure Patient Profile
              </h3>
              <p className="text-xs text-surface-muted/80 leading-relaxed">
                Create an individual patient account to access personal health dashboards, store clinical consultation histories, and securely download certified PDF reports.
              </p>
            </div>

            {/* Privacy Safeguards */}
            <div className="space-y-2.5 pt-2 border-t border-white/10 text-xs">
              <div className="flex items-center gap-1.5 text-accent font-bold text-[11px] uppercase tracking-wider">
                <ShieldCheck className="w-4 h-4" />
                <span>Patient Privacy Guarantee</span>
              </div>
              <ul className="space-y-1.5 text-[11px] text-surface-muted/90">
                <li className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-accent shrink-0" />
                  <span>Individual segregated patient dashboards</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-accent shrink-0" />
                  <span>Bcrypt password hashing & JWT encryption</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-accent shrink-0" />
                  <span>Zero unauthorized data sharing</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="relative z-10 pt-6 border-t border-white/10 text-[11px] text-surface-muted/60 space-y-1">
            <div>Rajalakshmi Engineering College (REC)</div>
            <div className="text-white font-semibold">Artificial Intelligence Mini-Project</div>
            <div className="text-accent">Vinoth S (240701592)</div>
          </div>
        </div>

        {/* Right Form Card (7 cols) */}
        <div className="md:col-span-7 p-8 sm:p-10 flex flex-col justify-center space-y-5">
          
          <div className="space-y-1">
            <span className="text-[11px] font-bold text-secondary uppercase tracking-wider">New Patient Onboarding</span>
            <h2 className="text-2xl font-extrabold text-primary tracking-tight">Create Your Account</h2>
            <p className="text-xs text-primary/60">Fill in your clinical baseline to calibrate AI triage calculations.</p>
          </div>

          {error && (
            <div className="p-3.5 rounded-xl bg-status-emergency/10 border border-status-emergency/30 text-status-emergency text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-3.5">
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-primary mb-1">Full Name *</label>
                <div className="relative">
                  <User className="w-4 h-4 text-primary/40 absolute left-3 top-3" />
                  <input
                    type="text"
                    name="full_name"
                    required
                    value={formData.full_name}
                    onChange={handleChange}
                    placeholder="e.g. Vinoth S"
                    className="w-full pl-9 pr-3 py-2 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-primary mb-1">Email Address *</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-primary/40 absolute left-3 top-3" />
                  <input
                    type="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="name@example.com"
                    className="w-full pl-9 pr-3 py-2 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-primary mb-1">Phone Number *</label>
                <div className="relative">
                  <Phone className="w-4 h-4 text-primary/40 absolute left-3 top-3" />
                  <input
                    type="tel"
                    name="phone"
                    required
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder="+91 94440 12345"
                    className="w-full pl-9 pr-3 py-2 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-primary mb-1">Password *</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-primary/40 absolute left-3 top-3" />
                  <input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    required
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="At least 6 characters"
                    className="w-full pl-9 pr-9 py-2 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-2.5 text-primary/40 hover:text-primary"
                  >
                    {showPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>
            </div>

            {/* Demographics Row */}
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-bold text-primary mb-1">Age</label>
                <input
                  type="number"
                  name="age"
                  min="1"
                  max="120"
                  value={formData.age}
                  onChange={handleChange}
                  className="w-full px-3 py-2 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-primary mb-1">Gender</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  className="w-full px-2 py-2 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none bg-white font-medium"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-primary mb-1">Locality</label>
                <input
                  type="text"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  placeholder="Chennai"
                  className="w-full px-3 py-2 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                />
              </div>
            </div>

            {/* Clinical Baseline */}
            <div className="pt-2 border-t border-surface-muted space-y-2.5">
              <div>
                <label className="block text-[11px] font-semibold text-primary mb-0.5">Known Chronic Conditions (Optional)</label>
                <input
                  type="text"
                  name="chronic_conditions"
                  value={formData.chronic_conditions}
                  onChange={handleChange}
                  placeholder="e.g. Asthma, Hypertension, Diabetes, or None"
                  className="w-full px-3 py-1.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                />
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-primary mb-0.5">Known Drug Allergies (Optional)</label>
                <input
                  type="text"
                  name="allergies"
                  value={formData.allergies}
                  onChange={handleChange}
                  placeholder="e.g. Penicillin, Sulfa, or No known allergies"
                  className="w-full px-3 py-1.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-bold text-xs sm:text-sm shadow-md transition-all flex items-center justify-center gap-2 mt-2 disabled:opacity-50"
            >
              {loading ? (
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  <span>Complete Registration & Open Dashboard</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <div className="text-center text-xs text-primary/60 pt-1 border-t border-surface-muted">
            Already have an account?{' '}
            <Link to="/login" className="font-extrabold text-secondary hover:underline">
              Sign In here
            </Link>
          </div>

        </div>

      </div>
    </div>
  );
};

export default RegisterPage;
