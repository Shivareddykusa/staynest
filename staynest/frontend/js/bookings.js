/* ========================================
   bookings.js — Booking list page logic
   ======================================== */

async function loadBookings() {
  const list = document.getElementById('bookings-list');
  if (!list) return;

  if (!requireLogin('/login.html')) return;
  showSpinner('bookings-list');

  try {
    const bookings = await BookingAPI.list();

    if (!bookings.length) {
      showEmpty('bookings-list', '📅', 'No bookings yet',
        'You have not made any reservations.', `<a href="index.html" class="btn btn-primary">Explore Properties</a>`);
      return;
    }

    list.innerHTML = bookings.map(b => `
      <div class="booking-card">
        <div class="booking-card-img">
          <img src="${b.property_image || 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&q=60'}"
               alt="${b.property_name}" onerror="this.src='https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&q=60'">
        </div>
        <div class="booking-card-body">
          <div class="booking-card-title">${b.property_name}</div>
          <div class="booking-card-location">📍 ${b.location || ''}</div>
          <div class="booking-card-dates">
            📅 ${formatDate(b.check_in)} → ${formatDate(b.check_out)}
            &nbsp;·&nbsp; 👥 ${b.guests} guest${b.guests > 1 ? 's' : ''}
          </div>
          <div class="booking-card-footer">
            <span class="booking-status status-${b.status}">${b.status}</span>
            <span class="booking-card-price">${formatPrice(b.total_price)}</span>
          </div>
        </div>
      </div>`).join('');

  } catch (e) {
    showEmpty('bookings-list', '⚠️', 'Could not load bookings', e.message);
  }
}

document.addEventListener('DOMContentLoaded', loadBookings);
