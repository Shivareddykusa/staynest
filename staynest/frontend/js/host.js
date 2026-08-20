/* ========================================
   host.js — Host: add property page
   ======================================== */

document.addEventListener('DOMContentLoaded', () => {
  if (!requireHost()) return;

  const form = document.getElementById('add-property-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    btn.textContent = 'Adding...';

    const data = {
      name:        document.getElementById('prop-name').value.trim(),
      description: document.getElementById('prop-desc').value.trim(),
      location:    document.getElementById('prop-location').value.trim(),
      price:       parseFloat(document.getElementById('prop-price').value),
      bedrooms:    parseInt(document.getElementById('prop-bedrooms').value),
      guests:      parseInt(document.getElementById('prop-guests').value),
      image_url:   document.getElementById('prop-image').value.trim(),
    };

    try {
      await PropertyAPI.create(data);
      showToast('Property added successfully! 🎉', 'success');
      form.reset();
      setTimeout(() => { window.location.href = '../index.html'; }, 1800);
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = 'Add Property';
    }
  });
});
