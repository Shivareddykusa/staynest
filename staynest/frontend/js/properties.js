/* ========================================
   properties.js — Home page property loading
   ======================================== */

async function loadProperties(query = '') {
  const grid = document.getElementById('properties-grid');
  if (!grid) return;
  showSpinner('properties-grid');

  try {
    let props = await PropertyAPI.list();

    // Client-side search filter
    if (query) {
      const q = query.toLowerCase();
      props = props.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.location.toLowerCase().includes(q)
      );
    }

    if (!props.length) {
      showEmpty('properties-grid', '🏠', 'No properties found', query ? `No results for "${query}"` : 'No properties available yet.',
        '<a href="index.html" class="btn btn-primary">Clear Search</a>');
      return;
    }

    grid.innerHTML = props.map(renderPropertyCard).join('');
  } catch (e) {
    showEmpty('properties-grid', '⚠️', 'Could not load properties', e.message);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const searchForm = document.getElementById('hero-search-form');
  if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = document.getElementById('search-input').value.trim();
      loadProperties(q);
    });
  }
  loadProperties();
});
