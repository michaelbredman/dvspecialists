/* ─────────────────────────────────────────────────────────────
   booking-modal.js — HouseCall Pro booking modal overlay
   Include on any page: <script src="/booking-modal.js" defer></script>
   All links with href="/book" will open the modal instead.
───────────────────────────────────────────────────────────── */
(function () {
  var HCP_URL = 'https://book.housecallpro.com/book/Dryer-Vent-Specialists/553b0ec8101a41e09809d3a4cff7a800?v2=true';
  var modal = null;
  var iframe = null;

  function createModal() {
    modal = document.createElement('div');
    modal.id = 'bookingModal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-label', 'Book a Service');
    modal.style.cssText =
      'display:none;position:fixed;inset:0;z-index:9999;' +
      'align-items:center;justify-content:center;padding:1rem;';

    // Backdrop
    var backdrop = document.createElement('div');
    backdrop.style.cssText =
      'position:absolute;inset:0;background:rgba(0,0,0,.50);' +
      'transition:opacity .25s ease;';
    backdrop.addEventListener('click', closeModal);
    modal.appendChild(backdrop);

    // Modal content container
    var container = document.createElement('div');
    container.style.cssText =
      'position:relative;width:100%;max-width:520px;max-height:92vh;' +
      'background:#fff;border-radius:16px;overflow:hidden;' +
      'box-shadow:0 20px 60px rgba(0,0,0,.35),0 4px 16px rgba(0,0,0,.15);' +
      'display:flex;flex-direction:column;' +
      'animation:bookingSlideUp .3s cubic-bezier(.22,1,.36,1) forwards;';
    modal.appendChild(container);

    // Header bar
    var header = document.createElement('div');
    header.style.cssText =
      'display:flex;align-items:center;justify-content:space-between;' +
      'padding:.75rem 1rem;background:#026766;flex-shrink:0;';

    var title = document.createElement('span');
    title.textContent = 'Book Your Service';
    title.style.cssText =
      "font-family:'Barlow Condensed',sans-serif;font-weight:700;" +
      'font-size:1.15rem;color:#fff;letter-spacing:.03em;';
    header.appendChild(title);

    var closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.setAttribute('aria-label', 'Close booking');
    closeBtn.style.cssText =
      'background:none;border:none;color:#fff;font-size:1.6rem;' +
      'cursor:pointer;padding:0 .25rem;line-height:1;opacity:.7;' +
      'transition:opacity .15s;';
    closeBtn.addEventListener('mouseenter', function () { this.style.opacity = '1'; });
    closeBtn.addEventListener('mouseleave', function () { this.style.opacity = '.7'; });
    closeBtn.addEventListener('click', closeModal);
    header.appendChild(closeBtn);

    container.appendChild(header);

    // Loading indicator
    var loader = document.createElement('div');
    loader.id = 'bookingLoader';
    loader.style.cssText =
      'display:flex;align-items:center;justify-content:center;' +
      'padding:3rem 1rem;flex-shrink:0;';
    loader.innerHTML =
      '<div style="width:32px;height:32px;border:3px solid rgba(2,103,102,.15);' +
      'border-top-color:#026766;border-radius:50;animation:bookingSpin .7s linear infinite;"></div>';
    container.appendChild(loader);

    // Iframe wrapper (scrollable)
    var iframeWrap = document.createElement('div');
    iframeWrap.style.cssText = 'flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;';

    iframe = document.createElement('iframe');
    iframe.title = 'Book a Service with Dryer Vent Specialists';
    iframe.allow = 'payment';
    iframe.style.cssText = 'width:100%;min-height:650px;border:none;display:block;';
    iframe.addEventListener('load', function () {
      loader.style.display = 'none';
    });

    iframeWrap.appendChild(iframe);
    container.appendChild(iframeWrap);

    // Help footer
    var helpBar = document.createElement('div');
    helpBar.style.cssText =
      'text-align:center;padding:.65rem 1rem;font-size:.82rem;' +
      'color:#888;border-top:1px solid #eee;flex-shrink:0;' +
      "font-family:'Nunito',sans-serif;";
    helpBar.innerHTML =
      'Prefer to call? <a href="tel:+16504844418" style="color:#f3651a;font-weight:700;text-decoration:none;">(650) 484-4418</a>';
    container.appendChild(helpBar);

    // Inject keyframe animations
    var style = document.createElement('style');
    style.textContent =
      '@keyframes bookingSlideUp{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}' +
      '@keyframes bookingSpin{to{transform:rotate(360deg)}}';
    document.head.appendChild(style);

    document.body.appendChild(modal);
  }

  function openModal(e) {
    if (e) e.preventDefault();
    if (!modal) createModal();

    // Load iframe src only when opening (lazy)
    if (!iframe.src) {
      iframe.src = HCP_URL;
    }

    // Show loader again if iframe hasn't loaded yet
    var loader = document.getElementById('bookingLoader');
    if (loader && !iframe.contentDocument) {
      loader.style.display = 'flex';
    }

    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Track in GA4
    if (typeof gtag === 'function') {
      gtag('event', 'booking_modal_open', { event_category: 'engagement' });
    }
  }

  function closeModal() {
    if (!modal) return;
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }

  // ESC key closes modal
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
  });

  // Intercept all /book links
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href="/book"]');
    if (link) {
      openModal(e);
    }
  });

  // Auto-open if ?book=1 is in the URL (redirect from /book page)
  if (new URLSearchParams(window.location.search).get('book') === '1') {
    // Small delay to let page render first
    setTimeout(function () {
      openModal();
      // Clean up the URL without reloading
      if (window.history.replaceState) {
        var clean = window.location.pathname + window.location.hash;
        window.history.replaceState(null, '', clean);
      }
    }, 300);
  }

  // Expose globally so buttons can call it directly
  window.openBookingModal = openModal;
  window.closeBookingModal = closeModal;
})();
