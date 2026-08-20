/* ========================================
   main.js — Shared utilities (toast, etc.)
   Included on every page.
   ======================================== */

/* ─── Toast Notifications ───────────────────────────────── */
function showToast(message, type = 'success', duration = 3500) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type] || '📢'}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('fade-out');
    toast.addEventListener('animationend', () => toast.remove());
  }, duration);
}

/* ─── Loading Spinner Helper ────────────────────────────── */
function showSpinner(containerId) {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = '<div class="loading-spinner"><div class="spinner"></div><span>Loading...</span></div>';
}

function showEmpty(containerId, icon, title, message, btnHtml = '') {
  const el = document.getElementById(containerId);
  if (el) el.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">${icon}</div>
      <h3>${title}</h3>
      <p>${message}</p>
      ${btnHtml}
    </div>`;
}

/* ─── Format helpers ────────────────────────────────────── */
function formatPrice(amount) {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(amount);
}

function formatDate(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}

function nightsBetween(checkin, checkout) {
  const d1 = new Date(checkin), d2 = new Date(checkout);
  return Math.max(0, Math.round((d2 - d1) / 86400000));
}

/* ─── Property card renderer ────────────────────────────── */
function renderPropertyCard(p) {
  const img = p.image_url
    ? `<img src="${p.image_url}" alt="${p.name}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&q=60'">`
    : `<div style="height:100%;background:var(--gray-300);display:flex;align-items:center;justify-content:center;font-size:3rem">🏠</div>`;

  return `
    <div class="property-card">
      <div class="card-image">
        ${img}
        <span class="card-badge">🏠 Rental</span>
      </div>
      <div class="card-body">
        <div class="card-location">📍 ${p.location}</div>
        <div class="card-title">${p.name}</div>
        <div class="card-meta">
          <span>🛏 ${p.bedrooms} bed${p.bedrooms > 1 ? 's' : ''}</span>
          <span>👥 Up to ${p.guests} guests</span>
        </div>
        <div class="card-footer">
          <div class="card-price">${formatPrice(p.price)}<span> / night</span></div>
          <button class="btn-card" onclick="window.location.href='property.html?id=${p.id}'">View Details</button>
        </div>
      </div>
    </div>`;
}

/* ─── Init nav on every page ────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  updateNav();
  const logoutBtn = document.getElementById('btn-logout');
  if (logoutBtn) logoutBtn.addEventListener('click', logout);
});
