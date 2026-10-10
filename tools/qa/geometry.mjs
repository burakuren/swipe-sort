// node tools/qa/geometry.mjs [filter]
// Rendered checks QA uses to judge lint warnings:
// 1. Dialogs (role=dialog|alertdialog, not sheets): vertical centre vs the screen's centre, width, icons.
// 2. Touch targets under 48: can the target reach 48×48 with hitSlop without overlapping a neighbour target?
//    (vertical room = distance to nearest tappable element above/below that overlaps horizontally; horizontal
//    room likewise). Reports targets that cannot reach 48 in some axis.
// 3. Text overflow: elements whose scrollWidth exceeds clientWidth without truncation classes, and text
//    nodes that extend outside their frame's .screen box.
import { chromium } from 'playwright';
import { readdirSync } from 'node:fs';
import { join } from 'node:path';
import { SCREENS, fileUrl, parseArgs } from '../lib.mjs';

const { filters } = parseArgs();
const files = readdirSync(SCREENS).filter((f) => f.endsWith('.html') && (!filters.length || filters.some((x) => f.toLowerCase().includes(x))));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
const dialogs = [];
const targets = [];
const overflow = [];
for (const f of files.sort()) {
  await page.goto(fileUrl(join(SCREENS, f)), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const res = await page.evaluate(() => {
    const out = { dialogs: [], targets: [], overflow: [] };
    const SEL = 'button, [role="button"], a[href], [role="tab"], [role="menuitem"], [role="radio"], [role="checkbox"], [role="switch"], input, select, textarea';
    for (const frame of document.querySelectorAll('[data-frame]')) {
      const id = frame.dataset.frame;
      const screen = frame.querySelector('.screen') || frame;
      const sr = screen.getBoundingClientRect();
      for (const d of frame.querySelectorAll('[role="dialog"], [role="alertdialog"]')) {
        const cls = d.className || '';
        if (/sheet/.test(cls) || d.closest('[class*="rounded-t-sheet"]') || /rounded-t-sheet/.test(cls)) continue;
        const r = d.getBoundingClientRect();
        if (!r.height) continue;
        const icons = [...d.querySelectorAll('[class*="i-lucide-"]')].filter((i) => !i.closest('button, a, [role="combobox"], select, label, li, [role="radio"]')).map((i) => [...i.classList].find((c) => c.startsWith('i-lucide-')));
        out.dialogs.push({ id, offset: Math.round((r.top + r.height / 2) - (sr.top + sr.height / 2)), width: Math.round(r.width), height: Math.round(r.height), icons, label: (d.getAttribute('aria-label') || d.querySelector('h1,h2,h3,[id]')?.textContent || '').trim().slice(0, 50) });
      }
      const els = [...frame.querySelectorAll(SEL)].filter((el) => {
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) return false;
        if (el.closest('.frame-label, [aria-hidden="true"]')) return false;
        if (el.matches('input[type="checkbox"], input[type="radio"]') && el.closest('label')) return false;
        return getComputedStyle(el).visibility !== 'hidden';
      });
      const rects = els.map((el) => el.getBoundingClientRect());
      els.forEach((el, i) => {
        const r = rects[i];
        if (r.width >= 48 && r.height >= 48) return;
        if (r.width <= 2 || r.height <= 2) return; // sr-only prototype shortcuts
        // whole-row target: a larger tappable ancestor
        const anc = el.parentElement?.closest(SEL);
        if (anc) { const ar = anc.getBoundingClientRect(); if (ar.width >= 48 && ar.height >= 48) return; }
        const label = el.closest('label');
        if (label) { const lr = label.getBoundingClientRect(); if (lr.width >= 48 && lr.height >= 48) return; }
        let up = Infinity, down = Infinity, left = Infinity, right = Infinity;
        rects.forEach((o, j) => {
          if (j === i || els[j].contains(el) || el.contains(els[j])) return;
          const hOverlap = o.left < r.right && o.right > r.left;
          const vOverlap = o.top < r.bottom && o.bottom > r.top;
          if (hOverlap && o.bottom <= r.top) up = Math.min(up, r.top - o.bottom);
          if (hOverlap && o.top >= r.bottom) down = Math.min(down, o.top - r.bottom);
          if (vOverlap && o.right <= r.left) left = Math.min(left, r.left - o.right);
          if (vOverlap && o.left >= r.right) right = Math.min(right, o.left - r.right);
        });
        // hitSlop shared between neighbours: each side may use half the gap
        const reachH = r.height + Math.min(up / 2, 24) + Math.min(down / 2, 24);
        const reachW = r.width + Math.min(left / 2, 24) + Math.min(right / 2, 24);
        out.targets.push({ id, w: Math.round(r.width), h: Math.round(r.height), reachW: Math.round(reachW), reachH: Math.round(reachH), ok: reachW >= 48 && reachH >= 48, label: (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40) });
      });
      // overflow
      for (const el of screen.querySelectorAll('*')) {
        if (el.children.length && !el.matches('p,h1,h2,h3,span,button,a,label')) continue;
        const cs = getComputedStyle(el);
        if (cs.textOverflow === 'ellipsis' || /clamp/.test(el.className)) continue;
        if (el.scrollWidth > el.clientWidth + 2 && cs.overflowX !== 'visible' && cs.overflowX !== 'auto' && cs.overflowX !== 'scroll' && el.clientWidth > 0) {
          out.overflow.push({ id, kind: 'clipped-x', text: el.textContent.trim().slice(0, 50) });
        }
        const r = el.getBoundingClientRect();
        if (r.width && el.textContent.trim() && !el.children.length && (r.right > sr.right + 1 || r.left < sr.left - 1) && !el.closest('[class*="overflow-x-auto"], [class*="overflow-auto"], [aria-hidden="true"], [class*="snap-x"]')) {
          out.overflow.push({ id, kind: 'outside-screen-x', text: el.textContent.trim().slice(0, 50) });
        }
      }
    }
    return out;
  });
  dialogs.push(...res.dialogs); targets.push(...res.targets); overflow.push(...res.overflow);
}
await browser.close();
console.log('## Dialogs off-centre (|offset| > 24) or wider than 384 or with a standalone icon');
for (const d of dialogs) if (Math.abs(d.offset) > 24 || d.width > 384 || d.icons.length) console.log(`- ${d.id}: offset ${d.offset}, width ${d.width}, icons [${d.icons.join(', ')}] "${d.label}"`);
console.log(`\n## Touch targets < 48 that cannot reach 48 with hitSlop (${targets.filter((t) => !t.ok).length} of ${targets.length} small)`);
const bad = targets.filter((t) => !t.ok);
const grouped = new Map();
for (const t of bad) { const k = `${t.w}×${t.h} "${t.label}" reach ${t.reachW}×${t.reachH}`; if (!grouped.has(k)) grouped.set(k, []); grouped.get(k).push(t.id); }
for (const [k, ids] of grouped) console.log(`- ${k}: ${ids.length} frame(s) ${ids.slice(0, 6).join(', ')}${ids.length > 6 ? ' …' : ''}`);
console.log(`\n## Overflow candidates (${overflow.length})`);
const og = new Map();
for (const o of overflow) { const k = `${o.kind} "${o.text}"`; if (!og.has(k)) og.set(k, []); og.get(k).push(o.id); }
for (const [k, ids] of og) console.log(`- ${k}: ${ids.slice(0, 6).join(', ')}${ids.length > 6 ? ` … (${ids.length})` : ''}`);
