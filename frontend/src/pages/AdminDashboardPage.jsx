import React, { useEffect, useState } from 'react';
import { adminService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
  ShieldAlert, Hospital, GitBranch, Database, Plus, Trash2,
  ToggleLeft, ToggleRight, CheckCircle2, RefreshCw, AlertCircle
} from 'lucide-react';

const AdminDashboardPage = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [hospitals, setHospitals] = useState([]);
  const [rules, setRules] = useState([]);
  const [sources, setSources] = useState([]);
  const [activeTab, setActiveTab] = useState('hospitals');
  const [loading, setLoading] = useState(true);

  // New Hospital Form Modal
  const [showAddHospital, setShowAddHospital] = useState(false);
  const [newHospData, setNewHospData] = useState({
    name: '',
    facility_type: 'Hospital',
    address: '',
    locality: 'T. Nagar',
    pincode: '600017',
    latitude: 13.0418,
    longitude: 80.2341,
    phone: '',
    website: '',
    emergency_24x7: true,
  });

  const loadAdminData = async () => {
    try {
      const [stRes, hospRes, ruleRes, srcRes] = await Promise.all([
        adminService.getStats(),
        adminService.getHospitals(),
        adminService.getRules(),
        adminService.getSources(),
      ]);
      setStats(stRes.data);
      setHospitals(hospRes.data.hospitals || []);
      setRules(ruleRes.data.rules || []);
      setSources(srcRes.data.sources || []);
    } catch (err) {
      console.error("Admin data fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAdminData();
  }, []);

  const handleToggleRule = async (ruleId) => {
    try {
      await adminService.toggleRule(ruleId);
      setRules(prev => prev.map(r => r.id === ruleId ? { ...r, is_active: !r.is_active } : r));
    } catch (err) {
      alert("Failed to toggle rule.");
    }
  };

  const handleDeleteHospital = async (hospId) => {
    if (!window.confirm("Are you sure you want to delete this hospital record?")) return;
    try {
      await adminService.deleteHospital(hospId);
      setHospitals(prev => prev.filter(h => h.id !== hospId));
    } catch (err) {
      alert("Failed to delete hospital.");
    }
  };

  const handleAddHospitalSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await adminService.addHospital(newHospData);
      setHospitals(prev => [res.data.hospital, ...prev]);
      setShowAddHospital(false);
      setNewHospData({
        name: '',
        facility_type: 'Hospital',
        address: '',
        locality: 'T. Nagar',
        pincode: '600017',
        latitude: 13.0418,
        longitude: 80.2341,
        phone: '',
        website: '',
        emergency_24x7: true,
      });
    } catch (err) {
      alert(err.response?.data?.error || "Failed to add hospital.");
    }
  };

  return (
    <div className="max-w-6xl mx-auto py-8 space-y-8">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-surface-muted pb-4">
        <div>
          <span className="text-xs font-bold text-status-emergency uppercase tracking-wider">
            System Administration Portal
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-primary tracking-tight mt-1">
            Platform Operations & Registry Control
          </h1>
          <p className="text-xs text-primary/60 mt-0.5">
            Manage Chennai hospital registries, medical inference Horn rules, and dataset ingestion status
          </p>
        </div>

        <button
          onClick={loadAdminData}
          className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white border border-surface-muted text-xs font-semibold text-primary hover:bg-surface-bg transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Data</span>
        </button>
      </div>

      {/* Admin Metric Cards */}
      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-2xl border border-surface-muted shadow-xs">
            <span className="text-[11px] font-semibold text-primary/60">Healthcare Facilities</span>
            <div className="text-2xl font-black text-secondary mt-1">{stats.total_hospitals}</div>
          </div>
          <div className="bg-white p-4 rounded-2xl border border-surface-muted shadow-xs">
            <span className="text-[11px] font-semibold text-primary/60">Medical Rules Active</span>
            <div className="text-2xl font-black text-accent mt-1">{stats.total_rules}</div>
          </div>
          <div className="bg-white p-4 rounded-2xl border border-surface-muted shadow-xs">
            <span className="text-[11px] font-semibold text-primary/60">Clinical Ontology Nodes</span>
            <div className="text-2xl font-black text-primary mt-1">{stats.total_symptoms + stats.total_conditions}</div>
          </div>
          <div className="bg-white p-4 rounded-2xl border border-surface-muted shadow-xs">
            <span className="text-[11px] font-semibold text-primary/60">Total Triage Sessions</span>
            <div className="text-2xl font-black text-primary mt-1">{stats.total_assessments}</div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b border-surface-muted gap-2 text-xs">
        {[
          { id: 'hospitals', label: `Hospitals (${hospitals.length})` },
          { id: 'rules', label: `Medical Rules (${rules.length})` },
          { id: 'sources', label: `Data Sources & Freshness (${sources.length})` },
        ].map(tab => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2.5 rounded-t-xl font-bold transition-colors ${
              activeTab === tab.id
                ? 'bg-white border-t border-x border-surface-muted text-secondary shadow-xs'
                : 'text-primary/60 hover:text-primary'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* HOSPITALS MANAGEMENT TAB */}
      {activeTab === 'hospitals' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-primary">Registered Healthcare Establishments (Chennai)</h3>
            <button
              onClick={() => setShowAddHospital(true)}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-secondary text-white font-bold text-xs shadow-xs hover:bg-secondary-dark"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add Facility</span>
            </button>
          </div>

          <div className="bg-white rounded-2xl border border-surface-muted overflow-hidden shadow-xs">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-primary">
                <thead className="bg-surface-bg border-b border-surface-muted text-[11px] font-bold uppercase text-primary/60">
                  <tr>
                    <th className="p-3.5">Facility Name</th>
                    <th className="p-3.5">Type</th>
                    <th className="p-3.5">Locality</th>
                    <th className="p-3.5">Contact</th>
                    <th className="p-3.5">Consultation Fee</th>
                    <th className="p-3.5 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-surface-muted/60">
                  {hospitals.map(h => (
                    <tr key={h.id} className="hover:bg-surface-bg/40">
                      <td className="p-3.5 font-bold text-primary">{h.name}</td>
                      <td className="p-3.5">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          h.facility_type === 'Clinic' ? 'bg-accent/15 text-accent-dark' : 'bg-secondary/15 text-secondary'
                        }`}>
                          {h.facility_type}
                        </span>
                      </td>
                      <td className="p-3.5">{h.locality}</td>
                      <td className="p-3.5 font-mono">{h.phone || 'N/A'}</td>
                      <td className="p-3.5 font-semibold">{h.consultation_fee}</td>
                      <td className="p-3.5 text-right">
                        <button
                          onClick={() => handleDeleteHospital(h.id)}
                          className="p-1.5 text-primary/40 hover:text-status-emergency"
                          title="Delete hospital"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* RULES MANAGEMENT TAB */}
      {activeTab === 'rules' && (
        <div className="space-y-4">
          <h3 className="text-sm font-bold text-primary">Medical Knowledge Base & Decision Rules</h3>
          <div className="space-y-3">
            {rules.map(r => (
              <div key={r.id} className="bg-white p-4 rounded-2xl border border-surface-muted shadow-xs flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs font-bold text-secondary">{r.rule_code}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-surface-bg font-semibold text-primary/60">
                      Type: {r.rule_type}
                    </span>
                  </div>
                  <p className="text-xs text-primary/80 font-medium">{r.description}</p>
                </div>

                <button
                  onClick={() => handleToggleRule(r.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-colors ${
                    r.is_active ? 'bg-status-success/15 text-status-success' : 'bg-surface-bg text-primary/50'
                  }`}
                >
                  {r.is_active ? <ToggleRight className="w-4 h-4" /> : <ToggleLeft className="w-4 h-4" />}
                  <span>{r.is_active ? 'Active' : 'Disabled'}</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* DATA SOURCES TAB */}
      {activeTab === 'sources' && (
        <div className="space-y-4">
          <h3 className="text-sm font-bold text-primary">Data Sources & Ingestion Sync Status</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {sources.map(s => (
              <div key={s.id} className="bg-white p-5 rounded-2xl border border-surface-muted shadow-xs space-y-2">
                <div className="flex items-center justify-between">
                  <strong className="text-sm font-bold text-primary">{s.source_name}</strong>
                  <span className="px-2 py-0.5 rounded bg-status-success/15 text-status-success text-[10px] font-bold">
                    {s.status}
                  </span>
                </div>
                <div className="text-xs text-primary/70 space-y-1">
                  <div>Type: {s.source_type}</div>
                  <div>Records Ingested: <strong>{s.record_count}</strong></div>
                  <div>Last Synced: <strong>{s.last_synced || 'Recent'}</strong></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ADD HOSPITAL MODAL */}
      {showAddHospital && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 sm:p-7 max-w-lg w-full space-y-4 border border-surface-muted shadow-xl">
            <h3 className="font-bold text-lg text-primary">Add New Healthcare Facility</h3>
            <form onSubmit={handleAddHospitalSubmit} className="space-y-3 text-xs">
              <div>
                <label className="block font-bold text-primary mb-1">Facility Name *</label>
                <input
                  type="text"
                  required
                  value={newHospData.name}
                  onChange={(e) => setNewHospData(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="e.g. Kauvery Hospital, Alwarpet"
                  className="w-full px-3 py-2 rounded-xl border border-surface-muted text-xs outline-none focus:border-secondary"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-primary mb-1">Facility Type</label>
                  <select
                    value={newHospData.facility_type}
                    onChange={(e) => setNewHospData(prev => ({ ...prev, facility_type: e.target.value }))}
                    className="w-full px-3 py-2 rounded-xl border border-surface-muted text-xs outline-none bg-white"
                  >
                    <option value="Hospital">Hospital</option>
                    <option value="Clinic">Clinic</option>
                  </select>
                </div>
                <div>
                  <label className="block font-bold text-primary mb-1">Locality</label>
                  <input
                    type="text"
                    value={newHospData.locality}
                    onChange={(e) => setNewHospData(prev => ({ ...prev, locality: e.target.value }))}
                    className="w-full px-3 py-2 rounded-xl border border-surface-muted text-xs outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block font-bold text-primary mb-1">Full Address *</label>
                <input
                  type="text"
                  required
                  value={newHospData.address}
                  onChange={(e) => setNewHospData(prev => ({ ...prev, address: e.target.value }))}
                  placeholder="Street and Landmark"
                  className="w-full px-3 py-2 rounded-xl border border-surface-muted text-xs outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-primary mb-1">Latitude *</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={newHospData.latitude}
                    onChange={(e) => setNewHospData(prev => ({ ...prev, latitude: parseFloat(e.target.value) }))}
                    className="w-full px-3 py-2 rounded-xl border border-surface-muted text-xs outline-none"
                  />
                </div>
                <div>
                  <label className="block font-bold text-primary mb-1">Longitude *</label>
                  <input
                    type="number"
                    step="0.0001"
                    required
                    value={newHospData.longitude}
                    onChange={(e) => setNewHospData(prev => ({ ...prev, longitude: parseFloat(e.target.value) }))}
                    className="w-full px-3 py-2 rounded-xl border border-surface-muted text-xs outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-primary mb-1">Phone Number</label>
                  <input
                    type="tel"
                    value={newHospData.phone}
                    onChange={(e) => setNewHospData(prev => ({ ...prev, phone: e.target.value }))}
                    placeholder="+91 44 ..."
                    className="w-full px-3 py-2 rounded-xl border border-surface-muted text-xs outline-none"
                  />
                </div>
                <div>
                  <label className="block font-bold text-primary mb-1">Website URL</label>
                  <input
                    type="url"
                    value={newHospData.website}
                    onChange={(e) => setNewHospData(prev => ({ ...prev, website: e.target.value }))}
                    placeholder="https://..."
                    className="w-full px-3 py-2 rounded-xl border border-surface-muted text-xs outline-none"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-surface-muted">
                <button
                  type="button"
                  onClick={() => setShowAddHospital(false)}
                  className="px-4 py-2 rounded-xl border border-surface-muted text-primary/70 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-secondary text-white font-bold shadow-xs hover:bg-secondary-dark"
                >
                  Save Facility
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default AdminDashboardPage;
