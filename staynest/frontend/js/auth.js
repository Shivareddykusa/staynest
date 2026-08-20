/* ========================================
   auth.js — Authentication helpers
   ======================================== */

function isLoggedIn()   { return !!getToken(); }
function currentUser()  { return getUser(); }
function isHost()       { const u = getUser(); return u && u.role === 'host'; }

function saveSession(token, user) { setToken(token); setUser(user); }

function logout() {
  clearToken();
  clearUser();
  window.location.href = '/index.html';
}

/* Update navbar based on auth state */
function updateNav() {
  const user   = getUser();
  const loggedIn = !!getToken();

  const loginBtn    = document.getElementById('nav-login');
  const registerBtn = document.getElementById('nav-register');
  const userMenuEl  = document.getElementById('nav-user-menu');
  const userInitial = document.getElementById('nav-user-initial');
  const hostLink    = document.getElementById('nav-host-link');
  const dropName    = document.getElementById('drop-name');
  const dropEmail   = document.getElementById('drop-email');

  if (loggedIn && user) {
    if (loginBtn)    loginBtn.style.display    = 'none';
    if (registerBtn) registerBtn.style.display = 'none';
    if (userMenuEl)  userMenuEl.style.display  = 'flex';
    if (userInitial) userInitial.textContent   = user.name.charAt(0).toUpperCase();
    if (dropName)    dropName.textContent       = user.name;
    if (dropEmail)   dropEmail.textContent      = user.email;
    if (hostLink)    hostLink.style.display     = user.role === 'host' ? '' : 'none';
  } else {
    if (loginBtn)    loginBtn.style.display    = '';
    if (registerBtn) registerBtn.style.display = '';
    if (userMenuEl)  userMenuEl.style.display  = 'none';
    if (hostLink)    hostLink.style.display    = 'none';
  }
}

/* Toggle user dropdown */
function toggleDropdown() {
  const dd = document.getElementById('user-dropdown');
  if (dd) dd.classList.toggle('open');
}

/* Close dropdown on outside click */
document.addEventListener('click', (e) => {
  if (!e.target.closest('.user-menu')) {
    document.querySelectorAll('.user-dropdown').forEach(d => d.classList.remove('open'));
  }
});

/* Require login — redirect if not authenticated */
function requireLogin(redirect) {
  if (!isLoggedIn()) {
    window.location.href = redirect || '/login.html';
    return false;
  }
  return true;
}

/* Require host role */
function requireHost() {
  if (!isLoggedIn()) { window.location.href = '/login.html'; return false; }
  if (!isHost())     { showToast('Only hosts can access this page', 'error'); setTimeout(()=>{ window.location.href='/index.html'; }, 1500); return false; }
  return true;
}
