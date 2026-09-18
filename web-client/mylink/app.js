// MYLINK · Organismo interativo do ecossistema b'AI'tcoin × KAIR-S-SONICA
// Sem dependências. Tudo gerado/animado client-side com fallback offline.
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Chain status ao vivo com fallback offline ---------- */
  async function liveChain() {
    const el = $('#chain');
    if (!el) return;
    try {
      const r = await fetch('/api/api/v1/status', { cache: 'no-store' });
      if (!r.ok) throw new Error('bad');
      const d = await r.json();
      const h = d.height ?? d.chain_height ?? d.block_height;
      const a = d.agents ?? d.agents_registered ?? d.active_agents;
      const btc = d.oracle?.prices?.BTC;
      el.innerHTML = `<b>bloco #${h ?? '—'}</b> · ${a ?? '–'} agentes${btc ? ` · BTC $${Number(btc).toLocaleString('en-US')}` : ''}`;
      el.dataset.live = '1';
    } catch {
      el.innerHTML = `<b>mainnet online</b> · usando snapshot local`;
    }
  }

  /* ---------- Streaming de texto manifesto (efeito digitação) ---------- */
  function stream(el, text, speed = 14) {
    if (!el || reduceMotion) { if (el) el.textContent = text; return; }
    el.textContent = '';
    let i = 0;
    const tick = () => {
      if (i >= text.length) return;
      el.textContent = text.slice(0, ++i);
      el.appendChild(Object.assign(document.createElement('span'), { className: 'caret' }));
      setTimeout(tick, speed + Math.random() * 18);
    };
    tick();
  }

  /* ---------- Partículas gregárias (ambiente) ---------- */
  function particles() {
    if (reduceMotion) return;
    const c = $('#particles');
    if (!c) return;
    const ctx = c.getContext('2d', { alpha: true });
    const w = () => { c.width = innerWidth * devicePixelRatio; c.height = innerHeight * devicePixelRatio; };
    w(); addEventListener('resize', w, { passive: true });
    const N = Math.min(48, Math.round((innerWidth * innerHeight) / 28000));
    const pts = Array.from({ length: N }, () => ({
      x: Math.random() * c.width,
      y: Math.random() * c.height,
      vx: (Math.random() - 0.5) * 0.35 * devicePixelRatio,
      vy: (Math.random() - 0.5) * 0.35 * devicePixelRatio,
      r: (Math.random() * 1.6 + 0.6) * devicePixelRatio,
      a: Math.random() * 0.5 + 0.2
    }));
    const loop = () => {
      ctx.clearRect(0, 0, c.width, c.height);
      for (const p of pts) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > c.width) p.vx *= -1;
        if (p.y < 0 || p.y > c.height) p.vy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(232,178,58,${p.a})`;
        ctx.fill();
      }
      // Linhas curtas entre vizinhos próximos
      for (let i = 0; i < pts.length; i++) {
        for (let j = i + 1; j < pts.length; j++) {
          const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
          const d2 = dx * dx + dy * dy;
          if (d2 < 14000 * devicePixelRatio * devicePixelRatio) {
            ctx.strokeStyle = `rgba(232,178,58,${0.07 * (1 - d2 / (14000 * devicePixelRatio * devicePixelRatio))})`;
            ctx.lineWidth = 0.7 * devicePixelRatio;
            ctx.beginPath();
            ctx.moveTo(pts[i].x, pts[i].y);
            ctx.lineTo(pts[j].x, pts[j].y);
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  /* ---------- Reveal on-scroll (IntersectionObserver) ---------- */
  function reveal() {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      }
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    $$('[data-reveal]').forEach((el, i) => { el.style.transitionDelay = (i % 5) * 60 + 'ms'; io.observe(el); });
  }

  /* ---------- Ripple tátil nos cards ---------- */
  function ripples() {
    $$('.card').forEach((card) => {
      card.addEventListener('pointerdown', (ev) => {
        const r = card.getBoundingClientRect();
        const d = document.createElement('span');
        d.className = 'ripple';
        const size = Math.max(r.width, r.height) * 1.5;
        d.style.cssText = `width:${size}px;height:${size}px;left:${ev.clientX - r.left - size/2}px;top:${ev.clientY - r.top - size/2}px;`;
        card.appendChild(d);
        setTimeout(() => d.remove(), 700);
      });
    });
  }

  /* ---------- Magnetismo suave nos cards (hover only) ---------- */
  function magnet() {
    if (reduceMotion) return;
    $$('.card').forEach((card) => {
      card.addEventListener('pointermove', (ev) => {
        const r = card.getBoundingClientRect();
        const x = ((ev.clientX - r.left) / r.width - 0.5) * 6;
        const y = ((ev.clientY - r.top) / r.height - 0.5) * 6;
        card.style.transform = `translate3d(${x}px,${y}px,0)`;
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });
  }

  /* ---------- Tilt do avatar conforme giroscópio/pointer ---------- */
  function avatarTilt() {
    const el = $('#avatar'); if (!el || reduceMotion) return;
    const r = () => {
      const rect = el.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const handler = (ev) => {
        const x = ((ev.clientX ?? cx) - cx) / rect.width;
        const y = ((ev.clientY ?? cy) - cy) / rect.height;
        el.style.transform = `rotateX(${-y * 14}deg) rotateY(${x * 14}deg)`;
      };
      window.addEventListener('pointermove', handler, { passive: true });
      window.addEventListener('deviceorientation', (e) => {
        const x = (e.gamma ?? 0) / 45;
        const y = (e.beta ?? 0) / 60;
        el.style.transform = `rotateX(${-y * 14}deg) rotateY(${x * 14}deg)`;
      });
    };
    r();
  }

  /* ---------- Contador animado dos stats ---------- */
  function counters() {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        const t = e.target; const v = Number(t.dataset.value || 0); const s = t.dataset.suffix || '';
        const step = Math.max(1, Math.ceil(v / 32));
        let cur = 0;
        const tick = () => {
          cur = Math.min(v, cur + step);
          t.firstChild ? t.firstChild.nodeValue = String(cur) : t.textContent = cur + s;
          if (cur < v) requestAnimationFrame(tick);
        };
        tick();
        io.unobserve(t);
      }
    }, { threshold: 0.5 });
    $$('[data-counter]').forEach((el) => io.observe(el));
  }

  /* ---------- Copiar o URL do hub com feedback ---------- */
  function share() {
    $('#share')?.addEventListener('click', async () => {
      const url = location.href;
      try { await navigator.clipboard.writeText(url); } catch { location.href = 'mailto:?subject=MyLink&body=' + encodeURIComponent(url); }
      if (navigator.share) { try { await navigator.share({ url: navigator.clipboard?.writeText ? url : url, title: 'MyLink · b\'AI\'tcoin' }); return; } catch {} }
      const t = $('#share'); const old = t.textContent; t.textContent = 'link copiado ✓'; t.classList.add('ok');
      setTimeout(() => { t.textContent = old; t.classList.remove('ok'); }, 1600);
    });
  }

  /* ---------- Toast de novidade vindo do manifesto ---------- */
  function ping() {
    const m = $('#manifesto'); if (!m) return;
    stream(m, 'A cadeia não dorme. / O bloco continua. / O dragão observa.', 22);
  }

  /* ---------- Boot ---------- */
  document.addEventListener('DOMContentLoaded', () => {
    particles(); reveal(); ripples(); magnet(); avatarTilt(); counters(); share(); ping(); liveChain();
    setInterval(liveChain, 30_000);
  });
})();
