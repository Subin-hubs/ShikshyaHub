/* ============================================================
   ShikshyaHub — Main JS v2.0
   Dark mode, Notifications, Charts, Modals, Toast
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Apply saved theme immediately ──
  const savedTheme = localStorage.getItem('shikshyahub-theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);

  // ── Sidebar toggle (mobile) ──
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar       = document.querySelector('.sidebar');
  const overlay       = document.getElementById('sidebarOverlay');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('active');
    });
    if (overlay) overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('active');
    });
  }

  // ── Auto mark active sidebar link ──
  const path = window.location.pathname;
  document.querySelectorAll('.sidebar-nav a').forEach(link => {
    const href = link.getAttribute('href');
    if (href && (href === path || (path.startsWith(href) && href !== '/'))) {
      // Only set active if not already set via template
      if (!link.classList.contains('active')) {
        link.classList.add('active');
      }
    }
  });

  // ── Flash auto-dismiss ──
  document.querySelectorAll('.flash').forEach(f => {
    setTimeout(() => {
      f.style.opacity = '0';
      f.style.transform = 'translateY(-6px)';
      f.style.transition = 'all .3s ease';
      setTimeout(() => f.remove(), 300);
    }, 4500);
  });

  // ── Modal system ──
  window.openModal  = id => { const m = document.getElementById(id); if (m) { m.classList.add('active'); document.body.style.overflow = 'hidden'; } };
  window.closeModal = id => { const m = document.getElementById(id); if (m) { m.classList.remove('active'); document.body.style.overflow = ''; } };

  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', e => {
      if (e.target === overlay) { overlay.classList.remove('active'); document.body.style.overflow = ''; }
    });
  });
  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.addEventListener('click', () => {
      const m = btn.closest('.modal-overlay');
      if (m) { m.classList.remove('active'); document.body.style.overflow = ''; }
    });
  });

  // ── Confirm-delete buttons ──
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm(btn.dataset.confirm || 'Are you sure?')) e.preventDefault();
    });
  });

  // ── Topbar clock ──
  const clock = document.getElementById('topbarClock');
  if (clock) {
    const tick = () => {
      const now = new Date();
      clock.textContent = now.toLocaleDateString('en-US', { weekday:'short', month:'short', day:'numeric' })
        + '  ' + now.toLocaleTimeString('en-US', { hour:'2-digit', minute:'2-digit' });
    };
    tick(); setInterval(tick, 30000);
  }

  // ── Charts ──
  initCharts();

  // ── Animate stat counters ──
  animateNumbers();

  // ── File input label updater ──
  document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function() {
      const label = this.closest('.file-input-wrap')?.querySelector('.file-label');
      if (label && this.files[0]) {
        label.textContent = '📎 ' + this.files[0].name;
      }
    });
  });

});

// ── Animate stat numbers ──
function animateNumbers() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target  = parseInt(el.dataset.count) || 0;
    const dur     = 600;
    const start   = performance.now();
    const step    = ts => {
      const pct = Math.min((ts - start) / dur, 1);
      const ease = 1 - Math.pow(1 - pct, 3);
      el.textContent = Math.round(ease * target).toLocaleString();
      if (pct < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });
}

// ── Chart init ──
function initCharts() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

  document.querySelectorAll('[id="attChart"], canvas[data-pct]').forEach(canvas => {
    if (canvas.tagName !== 'CANVAS') return;
    const pct     = parseFloat(canvas.dataset.pct || 0);
    const fg      = '#c4962a';
    const bg      = isDark ? '#2d3748' : '#e2e8f0';
    const textCol = isDark ? '#e2e8f0' : '#0f1f3d';
    drawDonut(canvas, pct, fg, bg, textCol, `${pct}%`);
  });

  document.querySelectorAll('.bar-chart-canvas').forEach(canvas => {
    const data   = JSON.parse(canvas.dataset.values  || '[]');
    const labels = JSON.parse(canvas.dataset.labels  || '[]');
    drawBarChart(canvas, data, labels);
  });
}

function drawDonut(canvas, pct, fgColor, bgColor, textColor, label) {
  const ctx   = canvas.getContext('2d');
  const cx    = canvas.width / 2, cy = canvas.height / 2;
  const r     = Math.min(cx, cy) - 12;
  const angle = (pct / 100) * Math.PI * 2;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // BG ring
  ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.lineWidth = 13; ctx.strokeStyle = bgColor; ctx.stroke();
  // Progress ring
  ctx.beginPath(); ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + angle);
  ctx.lineWidth = 13; ctx.strokeStyle = fgColor; ctx.lineCap = 'round'; ctx.stroke();
  // Center text
  ctx.fillStyle = textColor; ctx.font = 'bold 16px DM Sans';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(label, cx, cy);
}

function drawBarChart(canvas, data, labels) {
  const ctx   = canvas.getContext('2d');
  const w     = canvas.width, h = canvas.height;
  const max   = Math.max(...data, 1);
  const padB  = 28;
  const gap   = w / data.length;
  const barW  = gap * 0.55;
  ctx.clearRect(0, 0, w, h);
  data.forEach((val, i) => {
    const barH = (val / max) * (h - padB - 8);
    const x    = gap * i + (gap - barW) / 2;
    const y    = h - padB - barH;
    const grad = ctx.createLinearGradient(0, y, 0, h - padB);
    grad.addColorStop(0, '#c4962a');
    grad.addColorStop(1, '#e8b84b');
    ctx.fillStyle = grad;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, barW, barH, [4, 4, 0, 0]);
    else ctx.rect(x, y, barW, barH);
    ctx.fill();
    ctx.fillStyle = '#718096'; ctx.font = '10px DM Sans';
    ctx.textAlign = 'center';
    ctx.fillText(labels[i] || '', x + barW / 2, h - 8);
  });
}

// ── Toast notification ──
function showToast(msg, type) {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  container.appendChild(t);
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateX(20px)';
    t.style.transition = 'all .3s ease';
    setTimeout(() => t.remove(), 300);
  }, 2500);
}

// ── Copy text ──
function copyText(text) {
  navigator.clipboard.writeText(text).then(() => showToast('✓ Copied!')).catch(() => showToast('Copy failed'));
}
