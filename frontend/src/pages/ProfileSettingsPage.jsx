import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { User, Phone, MapPin, Calendar, HeartPulse, ShieldAlert, CheckCircle2, Save } from 'lucide-react';

const ProfileSettingsPage = () => {
  const { user, updateProfile } = useAuth();
  const [formData, setFormData] = useState({
    full_name: '',
    phone: '',
    age: 24,
    gender: 'Male',
    location: 'Chennai, Tamil Nadu',
    chronic_conditions: '',
    allergies: '',
    current_medications: '',
    emergency_contact: ''
  });
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || '',
        phone: user.phone || '',
        age: user.profile?.age || 24,
        gender: user.profile?.gender || 'Male',
        location: user.profile?.location || 'Chennai, Tamil Nadu',
        chronic_conditions: user.profile?.chronic_conditions || '',
        allergies: user.profile?.allergies || '',
        current_medications: user.profile?.current_medications || '',
        emergency_contact: user.profile?.emergency_contact || ''
      });
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSavedSuccess(false);
    try {
      await updateProfile(formData);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      alert("Failed to update profile settings.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8 space-y-8">
      
      {/* Header */}
      <div className="border-b border-surface-muted pb-4">
        <span className="text-xs font-bold text-accent uppercase tracking-wider">Account & Health Preferences</span>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-primary tracking-tight mt-1">
          Patient Profile & Settings
        </h1>
        <p className="text-xs text-primary/60 mt-0.5">
          Manage your personal demographics and baseline health profile for calibrated AI triage
        </p>
      </div>

      {savedSuccess && (
        <div className="p-4 rounded-2xl bg-status-success/15 border border-status-success/30 text-status-success text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          <span>Profile and clinical baseline settings updated successfully!</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Basic Identity Card */}
        <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-4">
          <h3 className="font-bold text-sm text-primary flex items-center gap-2 border-b border-surface-muted pb-3">
            <User className="w-4 h-4 text-secondary" />
            <span>Personal Information</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-primary mb-1">Full Name</label>
              <input
                type="text"
                name="full_name"
                required
                value={formData.full_name}
                onChange={handleChange}
                className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-primary mb-1">Email Address</label>
              <input
                type="email"
                disabled
                value={user?.email || ''}
                className="w-full px-3 py-2.5 rounded-xl border border-surface-muted bg-surface-bg text-primary/50 text-xs outline-none cursor-not-allowed"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-primary mb-1">Phone Number</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-primary mb-1">Age</label>
              <input
                type="number"
                name="age"
                min="1"
                max="120"
                value={formData.age}
                onChange={handleChange}
                className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-primary mb-1">Biological Gender</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none bg-white font-medium"
              >
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
                <option value="Prefer not to say">Prefer not to say</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-primary mb-1">Residential Locality / City</label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g. Adyar, Chennai, Tamil Nadu"
              className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
            />
          </div>
        </div>

        {/* Clinical Baseline & Safety Card */}
        <div className="bg-white p-6 sm:p-7 rounded-3xl border border-surface-muted shadow-xs space-y-4">
          <h3 className="font-bold text-sm text-primary flex items-center gap-2 border-b border-surface-muted pb-3">
            <HeartPulse className="w-4 h-4 text-accent" />
            <span>Clinical Baseline & Safety Details</span>
          </h3>

          <div className="space-y-3">
            <div>
              <label className="block text-xs font-bold text-primary mb-1">Chronic Medical Conditions</label>
              <input
                type="text"
                name="chronic_conditions"
                value={formData.chronic_conditions}
                onChange={handleChange}
                placeholder="e.g. Type 2 Diabetes, Mild Asthma, Hypertension"
                className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-primary mb-1">Known Drug Allergies</label>
                <input
                  type="text"
                  name="allergies"
                  value={formData.allergies}
                  onChange={handleChange}
                  placeholder="e.g. Penicillin, Sulfa, Aspirin"
                  className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-primary mb-1">Emergency Contact Number</label>
                <input
                  type="tel"
                  name="emergency_contact"
                  value={formData.emergency_contact}
                  onChange={handleChange}
                  placeholder="+91 94440 99999"
                  className="w-full px-3 py-2.5 rounded-xl border border-surface-muted focus:border-secondary text-xs outline-none"
                />
              </div>
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-secondary hover:bg-secondary-dark text-white font-bold text-xs shadow-md transition-all hover:scale-102 disabled:opacity-50"
          >
            {loading ? (
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <Save className="w-4 h-4" />
            )}
            <span>Save Profile Preferences</span>
          </button>
        </div>

      </form>

    </div>
  );
};

export default ProfileSettingsPage;
