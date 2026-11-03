import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { AssessmentProvider } from './context/AssessmentContext';

import Navbar from './components/Navbar';
import Footer from './components/Footer';

import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import SymptomInputPage from './pages/SymptomInputPage';
import PatientInfoFollowUpPage from './pages/PatientInfoFollowUpPage';
import AnalysisLoadingPage from './pages/AnalysisLoadingPage';
import AnalysisResultsPage from './pages/AnalysisResultsPage';
import HospitalDiscoveryPage from './pages/HospitalDiscoveryPage';
import MedicalHistoryPage from './pages/MedicalHistoryPage';
import ProfileSettingsPage from './pages/ProfileSettingsPage';
import AIMethodologyPage from './pages/AIMethodologyPage';
import AdminDashboardPage from './pages/AdminDashboardPage';

// Protected Route Guard with Redirect to Login
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-8 h-8 border-3 border-secondary border-t-transparent rounded-full animate-spin" />
        <span className="text-xs font-semibold text-primary/60">Loading session...</span>
      </div>
    );
  }
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

// Patient-Only Route Guard (Admins do not take clinical assessments)
const PatientRoute = ({ children }) => {
  const { user, isAuthenticated, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-8 h-8 border-3 border-secondary border-t-transparent rounded-full animate-spin" />
        <span className="text-xs font-semibold text-primary/60">Verifying patient profile...</span>
      </div>
    );
  }
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (user?.role === 'admin') return <Navigate to="/admin" replace />;
  return children;
};

// Admin Route Guard
const AdminRoute = ({ children }) => {
  const { user, isAuthenticated, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-3">
        <div className="w-8 h-8 border-3 border-secondary border-t-transparent rounded-full animate-spin" />
        <span className="text-xs font-semibold text-primary/60">Verifying administrative access...</span>
      </div>
    );
  }
  return isAuthenticated && user?.role === 'admin' ? children : <Navigate to="/dashboard" replace />;
};

function App() {
  return (
    <AuthProvider>
      <AssessmentProvider>
        <Router>
          <div className="flex flex-col min-h-screen bg-surface-bg text-primary">
            <Navbar />
            <main className="flex-1 w-full">
              <Routes>
                {/* Public Access Pages */}
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/hospitals" element={<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><HospitalDiscoveryPage /></div>} />
                <Route path="/ai-methodology" element={<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><AIMethodologyPage /></div>} />

                {/* Patient-Only Healthcare Routes (Admins are automatically redirected to /admin) */}
                <Route path="/dashboard" element={<PatientRoute><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><DashboardPage /></div></PatientRoute>} />
                <Route path="/assessment/symptoms" element={<PatientRoute><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><SymptomInputPage /></div></PatientRoute>} />
                <Route path="/assessment/patient-info" element={<PatientRoute><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><PatientInfoFollowUpPage /></div></PatientRoute>} />
                <Route path="/assessment/loading" element={<PatientRoute><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><AnalysisLoadingPage /></div></PatientRoute>} />
                <Route path="/assessment/results" element={<PatientRoute><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><AnalysisResultsPage /></div></PatientRoute>} />
                <Route path="/history" element={<PatientRoute><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><MedicalHistoryPage /></div></PatientRoute>} />
                <Route path="/profile" element={<ProtectedRoute><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><ProfileSettingsPage /></div></ProtectedRoute>} />

                {/* Admin Operations Route */}
                <Route path="/admin" element={<AdminRoute><div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><AdminDashboardPage /></div></AdminRoute>} />

                {/* Catch All Redirect */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </Router>
      </AssessmentProvider>
    </AuthProvider>
  );
}

export default App;
