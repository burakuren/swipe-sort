// node tools/gen-images.mjs — generates the sample-data illustrations in design/02-data/images (SVG, no text).
// Deterministic: same sample-data.json → same images. People get simple portraits, products get object
// illustrations on a soft backdrop, photos get small landscape/city/indoor scenes.
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { DESIGN, ensureDir } from './lib.mjs';

const data = JSON.parse(readFileSync(join(DESIGN, '02-data/sample-data.json'), 'utf8'));
const out = join(DESIGN, '02-data/images');
for (const d of ['people', 'products', 'photos']) ensureDir(join(out, d));

const hash = (s) => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);
const rng = (seed) => { const f = () => ((seed = (Math.imul(seed ^ (seed >>> 15), 2246822507) + 1013904223) >>> 0) / 4294967296); f(); f(); f(); return f; };
const pick = (r, a) => a[Math.floor(r() * a.length)];
const svg = (w, h, body) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">${body}</svg>\n`;

// ---------- people ----------
const skins = ['#F1C9A5', '#E0AC83', '#C68B62', '#A86F4C', '#8A5636', '#F4D7BE', '#D9A27A'];
const hairs = ['#2B1D14', '#4A2F1E', '#6B4426', '#1C1C1C', '#9A6B3F', '#C9A36B', '#7A7A7A', '#3B2A20'];
const backs = ['#D7E3F4', '#E4DCF2', '#DCEFE6', '#F4E2D3', '#E8E6DF', '#D9EBEF', '#F1DCE3', '#E3E8D5'];
const shirts = ['#3F4C6B', '#7A4E3B', '#2F6B5A', '#8C6A9E', '#B5543C', '#3B6E8F', '#5C5C5C', '#A88B3E'];
function person(id) {
  const r = rng(hash(id));
  const skin = pick(r, skins), hair = pick(r, hairs), bg = pick(r, backs), shirt = pick(r, shirts);
  const long = r() < 0.5, bald = !long && r() < 0.12, beard = !long && r() < 0.25, glasses = r() < 0.25;
  let s = `<rect width="200" height="200" fill="${bg}"/>`;
  if (long) s += `<path d="M52 92c0-38 22-58 48-58s48 20 48 58v66H52z" fill="${hair}"/>`;
  s += `<path d="M30 200c4-38 34-56 70-56s66 18 70 56z" fill="${shirt}"/>`;
  s += `<rect x="86" y="118" width="28" height="30" rx="10" fill="${skin}"/>`;
  s += `<ellipse cx="100" cy="94" rx="34" ry="40" fill="${skin}"/>`;
  if (!bald) s += long
    ? `<path d="M64 88c2-28 18-44 36-44s36 14 38 44c-14-10-26-20-34-30-10 14-24 24-40 30z" fill="${hair}"/>`
    : `<path d="M66 84c0-26 16-40 34-40s34 14 34 40c-6-8-14-14-20-18-12 8-30 12-48 18z" fill="${hair}"/>`;
  if (beard) s += `<path d="M70 100c4 26 16 34 30 34s26-8 30-34c-6 10-16 14-30 14s-24-4-30-14z" fill="${hair}" opacity=".9"/>`;
  s += `<circle cx="87" cy="96" r="3.2" fill="#2A211C"/><circle cx="113" cy="96" r="3.2" fill="#2A211C"/>`;
  s += `<path d="M90 114c6 5 14 5 20 0" stroke="#7A3E2E" stroke-width="3" fill="none" stroke-linecap="round"/>`;
  if (glasses) s += `<g fill="none" stroke="#2A2A2A" stroke-width="2.5"><circle cx="87" cy="96" r="10"/><circle cx="113" cy="96" r="10"/><path d="M97 96h6"/></g>`;
  return svg(200, 200, s);
}

// ---------- products ----------
const prodBg = ['#ECEBE6', '#E6EBF0', '#EFE8E1', '#E5ECE6', '#EEE9F0'];
const draw = {
  Chair: (c) => `<rect x="70" y="36" width="60" height="70" rx="14" fill="${c}"/><rect x="62" y="108" width="76" height="16" rx="8" fill="${c}"/><rect x="96" y="124" width="8" height="34" fill="#4A4A4A"/><path d="M64 166h72M100 158v8" stroke="#4A4A4A" stroke-width="6" stroke-linecap="round"/>`,
  Desk: (c) => `<rect x="30" y="80" width="140" height="12" rx="3" fill="${c}"/><rect x="44" y="92" width="8" height="70" fill="#3A3A3A"/><rect x="148" y="92" width="8" height="70" fill="#3A3A3A"/><rect x="36" y="160" width="24" height="5" rx="2" fill="#3A3A3A"/><rect x="140" y="160" width="24" height="5" rx="2" fill="#3A3A3A"/>`,
  Monitor: (c) => `<rect x="34" y="40" width="132" height="84" rx="6" fill="#222"/><rect x="40" y="46" width="120" height="72" rx="3" fill="${c}"/><rect x="94" y="124" width="12" height="24" fill="#333"/><rect x="70" y="148" width="60" height="7" rx="3" fill="#333"/>`,
  Keyboard: (c) => `<rect x="26" y="78" width="148" height="48" rx="8" fill="#2E2E2E"/>${Array.from({ length: 12 }, (_, i) => `<rect x="${34 + (i % 6) * 22}" y="${86 + Math.floor(i / 6) * 18}" width="18" height="13" rx="3" fill="${c}"/>`).join('')}`,
  Lamp: (c) => `<path d="M70 50h60l14 40H56z" fill="${c}"/><rect x="97" y="90" width="6" height="58" fill="#5A5A5A"/><ellipse cx="100" cy="156" rx="30" ry="8" fill="#5A5A5A"/>`,
  Accessory: (c) => `<rect x="40" y="70" width="120" height="60" rx="10" fill="${c}"/><rect x="52" y="82" width="96" height="36" rx="6" fill="#ffffff" opacity=".35"/>`,
  Headphones: (c) => `<path d="M58 112c0-34 18-56 42-56s42 22 42 56" stroke="#2E2E2E" stroke-width="10" fill="none"/><rect x="46" y="104" width="26" height="44" rx="12" fill="${c}"/><rect x="128" y="104" width="26" height="44" rx="12" fill="${c}"/>`,
  Plant: (c) => `<path d="M100 110c-30-6-40-34-34-52 18 6 30 22 34 52zM100 110c30-8 42-30 38-50-18 4-32 20-38 50zM100 110c-4-30 0-48 0-64 8 18 8 40 0 64z" fill="#4E8A5B"/><path d="M74 110h52l-8 50H82z" fill="${c}"/>`,
  Mouse: (c) => `<path d="M100 48c22 0 36 22 36 54s-14 50-36 50-36-18-36-50 14-54 36-54z" fill="${c}"/><path d="M100 50v34" stroke="#2E2E2E" stroke-width="3"/>`,
  Webcam: (c) => `<circle cx="100" cy="90" r="34" fill="#2E2E2E"/><circle cx="100" cy="90" r="16" fill="${c}"/><rect x="88" y="124" width="24" height="10" fill="#444"/><rect x="72" y="134" width="56" height="8" rx="4" fill="#444"/>`,
  Speakers: (c) => `<rect x="44" y="56" width="48" height="88" rx="6" fill="${c}"/><rect x="108" y="56" width="48" height="88" rx="6" fill="${c}"/><circle cx="68" cy="112" r="14" fill="#2E2E2E"/><circle cx="132" cy="112" r="14" fill="#2E2E2E"/><circle cx="68" cy="76" r="6" fill="#2E2E2E"/><circle cx="132" cy="76" r="6" fill="#2E2E2E"/>`,
};
const prodColors = ['#3F5E8C', '#B36B4A', '#5E8C6A', '#C9A13B', '#7A6A9E', '#2F6F7A', '#A84C5E', '#8C8C84'];
function product(p, i) {
  const r = rng(hash(p.id));
  const fn = draw[p.category] ?? draw.Accessory;
  return svg(200, 200, `<rect width="200" height="200" fill="${prodBg[i % prodBg.length]}"/><ellipse cx="100" cy="170" rx="64" ry="8" fill="#000" opacity=".07"/>${fn(pick(r, prodColors))}`);
}

// ---------- photos ----------
const skies = { day: ['#BFD8EE', '#CFE3F2', '#D9E8F0'], dusk: ['#F2C9A6', '#E9B8A6', '#F0D3B0'], overcast: ['#D5D9DE', '#CED3D8'] };
function scene(ph, i) {
  const r = rng(hash(ph.id));
  const time = pick(r, ['day', 'day', 'dusk', 'overcast']);
  const sky = pick(r, skies[time]);
  const W = ph.width > ph.height ? 400 : 300, H = ph.width > ph.height ? 300 : 400;
  let s = `<rect width="${W}" height="${H}" fill="${sky}"/>`;
  if (time !== 'overcast' && ph.scene !== 'indoor') s += `<circle cx="${W * (0.2 + r() * 0.6)}" cy="${H * 0.22}" r="${18 + r() * 10}" fill="${time === 'dusk' ? '#F7A26B' : '#FFF4D6'}"/>`;
  const g = H * 0.62;
  switch (ph.scene) {
    case 'sea':
      s += `<rect y="${g}" width="${W}" height="${H - g}" fill="${pick(r, ['#4C7FA8', '#3E6F96', '#5A8DB3'])}"/>`;
      s += `<path d="M0 ${g - 18}q${W * 0.25} -30 ${W * 0.5} -6t${W * 0.5} 4V${g}H0z" fill="#7C8E8A"/>`;
      for (let k = 0; k < 4; k++) s += `<path d="M${r() * W} ${g + 20 + k * 22}h${30 + r() * 40}" stroke="#ffffff" stroke-opacity=".4" stroke-width="3" stroke-linecap="round"/>`;
      s += `<path d="M${W * 0.62} ${g + 26}h40l-8 10h-26z" fill="#F4F1EA"/><path d="M${W * 0.66} ${g + 26}v-26l18 24z" fill="#ffffff"/>`;
      break;
    case 'city': {
      const base = pick(r, ['#C9B8A3', '#B9A48D', '#D1C2B0']);
      let x = 0;
      while (x < W) { const w = 30 + r() * 50, h = 70 + r() * 120; s += `<rect x="${x}" y="${g + 40 - h}" width="${w}" height="${h + H}" fill="${pick(r, [base, '#A88F7A', '#D8CBB9', '#9C7F6B', '#CBB49A'])}"/>`; for (let wy = g + 50 - h; wy < g + 20; wy += 22) for (let wx = x + 8; wx < x + w - 10; wx += 16) s += `<rect x="${wx}" y="${wy}" width="8" height="12" fill="#5B4A3F" opacity=".55"/>`; x += w + 2; }
      s += `<rect y="${g + 40}" width="${W}" height="${H}" fill="#7A746C"/>`;
      break;
    }
    case 'hills':
      s += `<path d="M0 ${g}q${W * 0.2} -90 ${W * 0.45} -40t${W * 0.55} -30V${H}H0z" fill="#D8B48A"/><path d="M0 ${g + 40}q${W * 0.3} -60 ${W * 0.6} -10t${W * 0.4} 0V${H}H0z" fill="#C49A6C"/>`;
      for (let k = 0; k < 3; k++) { const cx = W * (0.2 + r() * 0.6), cy = H * (0.18 + r() * 0.15); s += `<ellipse cx="${cx}" cy="${cy}" rx="18" ry="22" fill="${pick(r, ['#E86A5B', '#F2B84B', '#6FA3D9'])}"/><path d="M${cx - 6} ${cy + 22}h12v8h-12z" fill="#7A5A3E"/>`; }
      break;
    case 'forest':
      s += `<rect y="${g}" width="${W}" height="${H - g}" fill="#5F7F55"/>`;
      for (let k = 0; k < 9; k++) { const x = r() * W, h = 80 + r() * 90; s += `<path d="M${x} ${g + 30 - h}l${22} ${h}h-44z" fill="${pick(r, ['#2F5A3C', '#3D6B47', '#264D33'])}"/>`; }
      break;
    default: // indoor
      s = `<rect width="${W}" height="${H}" fill="${pick(r, ['#E9E1D6', '#DDE3E8', '#EAD9CF'])}"/><rect y="${H * 0.7}" width="${W}" height="${H * 0.3}" fill="#B08B66"/>`;
      s += `<rect x="${W * 0.15}" y="${H * 0.15}" width="${W * 0.3}" height="${H * 0.32}" fill="#BFD8EE" stroke="#ffffff" stroke-width="6"/>`;
      s += `<rect x="${W * 0.5}" y="${H * 0.5}" width="${W * 0.38}" height="${H * 0.22}" rx="10" fill="${pick(r, ['#5E7C8C', '#8C5E5E', '#6E8C5E'])}"/><circle cx="${W * 0.3}" cy="${H * 0.66}" r="${W * 0.06}" fill="#F2F2F2"/>`;
  }
  if (ph.similarTo) s += `<rect width="${W}" height="${H}" fill="#ffffff" opacity=".06"/>`;
  return svg(W, H, s);
}

let n = 0;
const write = (p, s) => { writeFileSync(join(out, p), s); n++; };
for (const c of data.contacts) if (c.photo) write(`people/${c.id}.svg`, person(c.id));
for (const m of data.members) if (m.avatar) write(`people/${m.id}.svg`, person(m.id + 'x'));
data.products.forEach((p, i) => write(`products/${p.id}.svg`, product(p, i)));
data.photos.forEach((ph, i) => write(`photos/${ph.id}.svg`, scene(ph, i)));
console.log(`gen-images: ${n} SVG files → design/02-data/images`);
