import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('mediguide_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to catch unauthorized responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Optional: Auto logout if expired
      const isAuthUrl = error.config.url.includes('/api/auth/login') || error.config.url.includes('/api/auth/register');
      if (!isAuthUrl) {
        localStorage.removeItem('mediguide_token');
        localStorage.removeItem('mediguide_user');
      }
    }
    return Promise.reject(error);
  }
);

export const authService = {
  login: (email, password) => api.post('/api/auth/login', { email, password }),
  register: (payload) => api.post('/api/auth/register', payload),
  getMe: () => api.get('/api/auth/me'),
  updateProfile: (payload) => api.put('/api/auth/profile', payload),
  forgotPassword: (email) => api.post('/api/auth/forgot-password', { email }),
};

export const symptomService = {
  getCategories: () => api.get('/api/symptoms/categories'),
  getAll: () => api.get('/api/symptoms/all'),
  extractNLP: (text) => api.post('/api/symptoms/nlp-extract', { text }),
};

export const assessmentService = {
  getFollowUps: (symptomCodes, rawText) => api.post('/api/assessment/follow-ups', { symptom_codes: symptomCodes, raw_text: rawText }),
  analyze: (payload) => api.post('/api/assessment/analyze', payload),
  getHistory: () => api.get('/api/assessment/history'),
  getById: (id) => api.get(`/api/assessment/${id}`),
  deleteById: (id) => api.delete(`/api/assessment/${id}`),
  compare: (id1, id2) => api.post('/api/assessment/compare', { assessment_id_1: id1, assessment_id_2: id2 }),
  downloadPdfUrl: (id) => `/api/assessment/${id}/pdf`,
};

export const hospitalService = {
  search: (params) => api.get('/api/hospitals/search', { params }),
  getLocalities: () => api.get('/api/hospitals/localities'),
  getById: (id) => api.get(`/api/hospitals/${id}`),
};

export const methodologyService = {
  getOverview: () => api.get('/api/ai-methodology/overview'),
};

export const adminService = {
  getStats: () => api.get('/api/admin/stats'),
  getHospitals: () => api.get('/api/admin/hospitals'),
  addHospital: (payload) => api.post('/api/admin/hospitals', payload),
  updateHospital: (id, payload) => api.put(`/api/admin/hospitals/${id}`, payload),
  deleteHospital: (id) => api.delete(`/api/admin/hospitals/${id}`),
  getRules: () => api.get('/api/admin/rules'),
  toggleRule: (id) => api.put(`/api/admin/rules/${id}/toggle`),
  getSources: () => api.get('/api/admin/sources'),
};

export default api;
