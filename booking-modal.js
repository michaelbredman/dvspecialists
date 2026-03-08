/* ─────────────────────────────────────────────────────────────
   booking-modal.js — Opens HouseCall Pro booking in a popup window.
   Include on any page: <script src="/booking-modal.js" defer></script>
   All links with href="/book" will open the popup instead.
───────────────────────────────────────────────────────────── */
(function () {
  var HCP_URL = 'https://book.housecallpro.com/book/Dryer-Vent-Specialists/553b0ec8101a41e09809d3a4cff7a800?v2=true';

  function openBooking(e) {
    if (e) e.preventDefault();

    // Centered popup dimensions
    var w = 520;
    var h = Math.min(window.innerHeight - 60, 820);
    var left = Math.round((screen.width - w) / 2);
    var top = Math.round((screen.height - h) / 2);

    var popup = window.open(
      HCP_URL,
      'dvs_booking',
      'width=' + w + ',height=' + h + ',left=' + left + ',top=' + top +
      ',scrollbars=yes,resizable=yes,toolbar=no,menubar=no,location=no,status=no'
    );

    // Fallback: if popup was blocked, navigate directly
    if (!popup || popup.closed) {
      window.location.href = HCP_URL;
    }

    // Track in GA4
    if (typeof gtag === 'function') {
      gtag('event', 'booking_popup_open', { event_category: 'engagement' });
    }
  }

  // Intercept all /book links
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href="/book"]');
    if (link) {
      openBooking(e);
    }
  });

  // Auto-open if ?book=1 is in the URL (redirect from /book page)
  if (new URLSearchParams(window.location.search).get('book') === '1') {
    setTimeout(function () {
      openBooking();
      if (window.history.replaceState) {
        var clean = window.location.pathname + window.location.hash;
        window.history.replaceState(null, '', clean);
      }
    }, 300);
  }

  // Expose globally
  window.openBookingModal = openBooking;
})();
