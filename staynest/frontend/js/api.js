/* ========================================
   api.js — Centralized API communication
   All fetch() calls go through this file.
   The frontend NEVER talks to MySQL directly.
   ======================================== */

const API_BASE = 'http://localhost:5000/api';

// ─── Token helpers ─────────────────────────────────────────
const getToken  = ()    => localStorage.getItem('sn_token');
const setToken  = (t)   => localStorage.setItem('sn_token', t);
const clearToken = ()   => localStorage.removeItem('sn_token');

const getUser  = ()    => { try { return JSON.parse(localStorage.getItem('sn_user')); } catch { return null; } };
const setUser  = (u)   => localStorage.setItem('sn_user', JSON.stringify(u));
const clearUser = ()   => localStorage.removeItem('sn_user');

// ─── Core fetch wrapper ────────────────────────────────────
async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const resp = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const data = await resp.json().catch(() => ({}));

  if (!resp.ok) {
    const msg = data.message || `Error ${resp.status}`;
    throw new Error(msg);
  }
  return data.data;
}

// ─── Auth APIs ────────────────────────────────────────────
const AuthAPI = {
  register: (payload) => apiFetch('/register', { method: 'POST', body: JSON.stringify(payload) }),
  login:    (payload) => apiFetch('/login',    { method: 'POST', body: JSON.stringify(payload) }),
  me:       ()        => apiFetch('/me'),
};

// ─── Property APIs ────────────────────────────────────────
const PropertyAPI = {
  list:   ()    => apiFetch('/properties'),
  get:    (id)  => apiFetch(`/properties/${id}`),
  create: (data)=> apiFetch('/properties', { method: 'POST', body: JSON.stringify(data) }),
};

// ─── Booking APIs ─────────────────────────────────────────
const BookingAPI = {
  create: (data) => apiFetch('/bookings', { method: 'POST', body: JSON.stringify(data) }),
  list:   ()     => apiFetch('/bookings'),
};

// ─── Health check ─────────────────────────────────────────
const healthCheck = () => apiFetch('/health');
