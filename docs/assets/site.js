/* ZeroMatrixTech site script: theme toggle, mobile menu, project filter, copy email, hero dot matrix.
   Every page works without it; this only adds conveniences. */
(() => {
"use strict";
const root = document.documentElement, $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

/* theme */
try { const s = localStorage.getItem("zmt-theme"); if (s) root.dataset.theme = s; } catch (e) {}
$(".theme")?.addEventListener("click", () => {
  const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark";
  try { localStorage.setItem("zmt-theme", root.dataset.theme); } catch (e) {}
});

/* remember the chosen language, used only when someone follows the language switch */
$(".lang")?.addEventListener("click", e => { try { localStorage.setItem("zmt-lang", e.currentTarget.getAttribute("hreflang")); } catch (err) {} });

/* mobile menu */
const menu = $(".menu"), nav = $(".nav");
menu?.addEventListener("click", () => { const open = nav.classList.toggle("open"); menu.setAttribute("aria-expanded", String(open)); });

/* project filter */
const chips = $$(".chip[data-cat]"), cards = $$(".grid [data-cat]");
chips.forEach(b => b.addEventListener("click", () => {
  const k = b.dataset.cat;
  chips.forEach(c => c.setAttribute("aria-pressed", String(c === b)));
  cards.forEach(c => c.hidden = k !== "all" && c.dataset.cat !== k);
}));

/* copy email */
$$("[data-copy]").forEach(b => b.addEventListener("click", () => {
  const target = document.getElementById(b.dataset.copy), text = target.textContent.trim(), label = b.textContent;
  const done = ok => { b.textContent = ok ? b.dataset.ok : b.dataset.fail; setTimeout(() => b.textContent = label, 1600); };
  const select = () => { getSelection().selectAllChildren(target); done(false); };
  if (navigator.clipboard) navigator.clipboard.writeText(text).then(() => done(true), select); else select();
}));

/* hero dot matrix: a slow light wave across a 16x12 grid that spells "ZM" */
const mc = $("#matrix");
if (mc) {
  const g = mc.getContext("2d"), COLS = 16, ROWS = 12;
  const LOGO = ["", "", "", "0011111001100110", "0000010001111110", "0000100001011010", "0001000001000010", "0011111001000010"];
  const css = n => getComputedStyle(root).getPropertyValue(n).trim();
  let start = performance.now(), visible = true;
  const tick = now => {
    const w = mc.clientWidth, h = mc.clientHeight, d = Math.min(devicePixelRatio || 1, 2);
    if (mc.width !== Math.round(w * d)) { mc.width = Math.round(w * d); mc.height = Math.round(h * d); }
    g.setTransform(d, 0, 0, d, 0, 0); g.clearRect(0, 0, w, h);
    const t = reduce ? 6 : (now - start) / 1000, cw = w / (COLS + 1), ch = h / (ROWS + 1), r = Math.min(cw, ch) * .32;
    const acc = css("--accent"), line = css("--line"), warm = css("--warm");
    for (let j = 0; j < ROWS; j++) for (let i = 0; i < COLS; i++) {
      const x = (i + 1) * cw, y = (j + 1) * ch;
      const wave = .5 + .5 * Math.sin(i * .55 - t * 1.6 + Math.sin(j * .4 + t * .5) * 1.4);
      const on = LOGO[j] && LOGO[j][i] === "1";
      const logo = on ? (reduce ? 1 : Math.min(1, Math.max(0, (t - .2 - (i + j) * .04) / .5))) : 0;
      const glint = wave > .9 ? (wave - .9) / .1 : 0, lit = logo > 0 ? Math.min(1, .55 + .45 * glint) * logo : glint * .35;
      g.globalAlpha = 1; g.fillStyle = line; g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); g.fill();
      if (lit > 0) { g.globalAlpha = lit; g.fillStyle = on ? (i < 8 ? warm : acc) : acc; g.beginPath(); g.arc(x, y, r * (1 + .15 * lit), 0, Math.PI * 2); g.fill(); }
    }
    g.globalAlpha = 1;
    if (visible && !reduce) requestAnimationFrame(tick);
  };
  new IntersectionObserver(es => { const was = visible; visible = es.some(e => e.isIntersecting); if (visible && !was) requestAnimationFrame(tick); }).observe(mc);
  requestAnimationFrame(tick);
}
})();
