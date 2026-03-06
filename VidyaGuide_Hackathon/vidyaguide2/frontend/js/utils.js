/* VidyaGuide – Shared Utilities */

// ── Storage ───────────────────────────────────────────────
const VG = {
  save(k, v) { try { localStorage.setItem('vg_' + k, JSON.stringify(v)); } catch(e){} },
  load(k, fb = {}) { try { return JSON.parse(localStorage.getItem('vg_' + k)) ?? fb; } catch(e){ return fb; } },
  clear(k) { localStorage.removeItem('vg_' + k); }
};

// ── Active Nav Link ───────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href').split('/').pop();
    if (href === path || (path === '' && href === 'index.html')) a.classList.add('active');
  });
});

// ── Tab System ────────────────────────────────────────────
function initTabs(container) {
  const el = document.querySelector(container || '.tabs');
  if (!el) return;
  el.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.tab;
      el.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('on'));
      btn.classList.add('on');
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('on'));
      document.getElementById(id)?.classList.add('on');
    });
  });
  el.querySelector('.tab-btn')?.click();
}

// ── Score Ring ────────────────────────────────────────────
function animateRing(ringId, valId, target, color = 'var(--cyan)') {
  const ring = document.getElementById(ringId);
  const val  = document.getElementById(valId);
  if (!ring || !val) return;
  let cur = 0;
  const step = target / 55;
  const iv = setInterval(() => {
    cur = Math.min(cur + step, target);
    const deg = (cur / 100 * 360).toFixed(1) + 'deg';
    ring.style.background = `conic-gradient(${color} ${deg}, rgba(255,255,255,.06) ${deg})`;
    val.textContent = Math.round(cur);
    if (cur >= target) clearInterval(iv);
  }, 16);
}

// ── Progress Bars ─────────────────────────────────────────
function animateBars() {
  document.querySelectorAll('.prog-bar[data-w]').forEach(b => {
    setTimeout(() => { b.style.width = b.dataset.w + '%'; }, 100);
  });
}

// ── Skill Chip Helper ─────────────────────────────────────
function chipHTML(list, cls = '') {
  return list.map(s => `<span class="sk-chip ${cls}">${s}</span>`).join('');
}

// ── Loading Messages ──────────────────────────────────────
function cycleMsg(elId, msgs, interval = 900) {
  let i = 0;
  const el = document.getElementById(elId);
  if (!el) return null;
  el.textContent = msgs[0];
  return setInterval(() => { el.textContent = msgs[++i % msgs.length]; }, interval);
}

// ── Time ──────────────────────────────────────────────────
function nowTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// ── API Call ──────────────────────────────────────────────
async function apiPost(endpoint, body) {
  try {
    const r = await fetch('/api' + endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    if (!r.ok) return null;
    return await r.json();
  } catch(e) { return null; }
}

// ── Format Markdown-lite ──────────────────────────────────
function fmtText(t) {
  return t
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g,     '<em>$1</em>')
    .replace(/`(.*?)`/g,       '<code style="background:rgba(255,255,255,.08);padding:1px 5px;border-radius:4px;font-size:13px">$1</code>')
    .replace(/\n/g, '<br>');
}
