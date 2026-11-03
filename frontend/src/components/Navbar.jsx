import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Activity, ShieldAlert, User, LogOut, Menu, X, Hospital,
  BrainCircuit, History, PlusCircle, Settings, ChevronDown
} from 'lucide-react';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);

  // Navigation Links based on role
  const patientLinks = [
    { name: 'Dashboard', path: '/dashboard' },
    { name: 'Start Assessment', path: '/assessment/symptoms', isCta: true },
    { name: 'Chennai Hospitals', path: '/hospitals' },
    { name: 'My History', path: '/history' },
    { name: 'AI Methodology', path: '/ai-methodology' },
  ];

  const adminLinks = [
    { name: 'Admin Console', path: '/admin', isCta: true },
    { name: 'Chennai Hospitals', path: '/hospitals' },
    { name: 'AI Analytics', path: '/ai-methodology' },
  ];

  // Navigation Links for Public Visitors
  const publicLinks = [
    { name: 'Home', path: '/' },
    { name: 'Chennai Hospitals', path: '/hospitals' },
    { name: 'AI Methodology', path: '/ai-methodology' },
  ];

  const currentLinks = !isAuthenticated
    ? publicLinks
    : user?.role === 'admin'
    ? adminLinks
    : patientLinks;

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-surface-muted/80 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo */}
          <Link to={isAuthenticated ? (user?.role === 'admin' ? "/admin" : "/dashboard") : "/"} className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary to-secondary flex items-center justify-center text-white shadow-md shadow-secondary/20 transition-transform group-hover:scale-105">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xl font-extrabold tracking-tight text-primary leading-none flex items-center gap-1.5">
                MediGuide <span className="text-secondary">AI</span>
              </div>
              <div className="text-[10px] uppercase tracking-wider font-bold text-accent leading-none mt-0.5">
                Clinical Decision Support
              </div>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-1">
            {currentLinks.map((link) => {
              const isActive = location.pathname === link.path;
              if (link.isCta) {
                return (
                  <Link
                    key={link.path}
                    to={link.path}
                    className="inline-flex items-center gap-1.5 px-3.5 py-1.5 mx-1 rounded-xl bg-secondary/15 hover:bg-secondary text-secondary hover:text-white font-bold text-xs transition-all shadow-2xs"
                  >
                    <PlusCircle className="w-3.5 h-3.5" />
                    <span>{link.name}</span>
                  </Link>
                );
              }
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                    isActive
                      ? 'bg-secondary/10 text-secondary font-bold'
                      : 'text-primary/70 hover:text-primary hover:bg-surface-bg'
                  }`}
                >
                  {link.name}
                </Link>
              );
            })}
          </nav>

          {/* Right Action Icons & Auth */}
          <div className="hidden md:flex items-center gap-3">
            {/* Emergency 112 Badge */}
            <a
              href="tel:112"
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-status-emergency/10 border border-status-emergency/30 text-status-emergency text-xs font-black hover:bg-status-emergency hover:text-white transition-all shadow-xs"
              title="Emergency Assistance (India)"
            >
              <ShieldAlert className="w-4 h-4 animate-pulse" />
              <span>Emergency 112</span>
            </a>

            {isAuthenticated ? (
              <div className="relative pl-2 border-l border-surface-muted">
                <button
                  type="button"
                  onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                  className="flex items-center gap-2 p-1.5 rounded-xl hover:bg-surface-bg transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-secondary to-accent text-white flex items-center justify-center font-bold text-xs shadow-xs">
                    {user?.full_name ? user.full_name[0].toUpperCase() : 'U'}
                  </div>
                  <div className="text-left hidden lg:block">
                    <div className="text-xs font-bold text-primary leading-tight line-clamp-1">
                      {user?.full_name || (user?.role === 'admin' ? 'Administrator' : 'Patient')}
                    </div>
                    <div className="text-[10px] text-primary/50 font-medium leading-none">
                      {user?.role === 'admin' ? 'Administrator' : 'Patient Account'}
                    </div>
                  </div>
                  <ChevronDown className="w-3.5 h-3.5 text-primary/40" />
                </button>

                {/* Dropdown Menu */}
                {userDropdownOpen && (
                  <div
                    className="absolute right-0 mt-2 w-56 rounded-2xl bg-white border border-surface-muted shadow-xl py-2 z-50 animate-fade-in"
                    onMouseLeave={() => setUserDropdownOpen(false)}
                  >
                    <div className="px-4 py-2 border-b border-surface-muted text-xs">
                      <div className="font-bold text-primary truncate">{user?.full_name}</div>
                      <div className="text-[11px] text-primary/50 truncate">{user?.email}</div>
                    </div>

                    {user?.role === 'admin' ? (
                      <>
                        <Link
                          to="/admin"
                          onClick={() => setUserDropdownOpen(false)}
                          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-secondary hover:bg-secondary/10 transition-colors"
                        >
                          <Settings className="w-4 h-4" />
                          <span>Admin Control Console</span>
                        </Link>
                        <Link
                          to="/hospitals"
                          onClick={() => setUserDropdownOpen(false)}
                          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-primary hover:bg-surface-bg transition-colors"
                        >
                          <Hospital className="w-4 h-4 text-secondary" />
                          <span>Chennai Facilities</span>
                        </Link>
                        <Link
                          to="/ai-methodology"
                          onClick={() => setUserDropdownOpen(false)}
                          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-primary hover:bg-surface-bg transition-colors"
                        >
                          <BrainCircuit className="w-4 h-4 text-secondary" />
                          <span>AI Engine Telemetry</span>
                        </Link>
                      </>
                    ) : (
                      <>
                        <Link
                          to="/dashboard"
                          onClick={() => setUserDropdownOpen(false)}
                          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-primary hover:bg-surface-bg transition-colors"
                        >
                          <Activity className="w-4 h-4 text-secondary" />
                          <span>My Health Dashboard</span>
                        </Link>

                        <Link
                          to="/history"
                          onClick={() => setUserDropdownOpen(false)}
                          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-primary hover:bg-surface-bg transition-colors"
                        >
                          <History className="w-4 h-4 text-secondary" />
                          <span>Consultation Reports</span>
                        </Link>

                        <Link
                          to="/profile"
                          onClick={() => setUserDropdownOpen(false)}
                          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-primary hover:bg-surface-bg transition-colors"
                        >
                          <Settings className="w-4 h-4 text-secondary" />
                          <span>Profile & Settings</span>
                        </Link>
                      </>
                    )}

                    <div className="border-t border-surface-muted my-1" />

                    <button
                      type="button"
                      onClick={() => {
                        setUserDropdownOpen(false);
                        logout();
                        navigate('/');
                      }}
                      className="w-full text-left flex items-center gap-2 px-4 py-2 text-xs font-bold text-status-emergency hover:bg-status-emergency/10 transition-colors"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Sign Out</span>
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center gap-2 pl-2 border-l border-surface-muted">
                <Link
                  to="/login"
                  className="px-4 py-2 rounded-xl text-xs font-bold text-primary hover:bg-surface-bg border border-surface-muted transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-secondary hover:bg-secondary-dark text-white shadow-xs transition-all hover:shadow-md"
                >
                  Register
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Toggle */}
          <div className="md:hidden flex items-center gap-2">
            <a
              href="tel:112"
              className="p-2 rounded-full bg-status-emergency/10 text-status-emergency"
              title="Emergency 112"
            >
              <ShieldAlert className="w-5 h-5" />
            </a>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-primary hover:bg-surface-bg"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-surface-muted bg-white px-4 pt-2 pb-4 space-y-1">
          {currentLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-xl text-sm font-semibold text-primary hover:bg-surface-bg"
            >
              {link.name}
            </Link>
          ))}
          {user?.role === 'admin' && (
            <Link
              to="/admin"
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-xl text-sm font-bold text-secondary hover:bg-secondary/10"
            >
              Admin Operations
            </Link>
          )}

          <div className="pt-3 border-t border-surface-muted">
            {isAuthenticated ? (
              <div className="space-y-2">
                <Link
                  to="/profile"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block px-3 py-2 rounded-xl text-sm font-medium text-primary hover:bg-surface-bg"
                >
                  My Profile ({user?.full_name})
                </Link>
                <button
                  onClick={() => {
                    logout();
                    setMobileMenuOpen(false);
                    navigate('/');
                  }}
                  className="w-full text-left px-3 py-2 rounded-xl text-sm font-bold text-status-emergency hover:bg-status-emergency/10"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <div className="flex gap-2 pt-1">
                <Link
                  to="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex-1 text-center py-2.5 rounded-xl text-xs font-bold border border-surface-muted text-primary"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex-1 text-center py-2.5 rounded-xl text-xs font-bold bg-secondary text-white"
                >
                  Register
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default Navbar;
