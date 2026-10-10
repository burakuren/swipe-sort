// Usage: node tools/generators/sample-data.mjs design/02-data/sample-data.json  (then: node tools/gen-images.mjs && npm run build:data)
// One-off generator for design/02-data/sample-data.json (deterministic).
import { writeFileSync } from 'node:fs';
const out = process.argv[2];

let seed = 20261010;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) % 4294967296) / 4294967296);
const pick = (a) => a[Math.floor(rnd() * a.length)];
const int = (a, b) => a + Math.floor(rnd() * (b - a + 1));
const pad = (n, w = 3) => String(n).padStart(w, '0');

// ---------------- contacts ----------------
// [name, side, relationship, city, flags]
const people = [
  ['Ayşe Demir', 'Bride\'s', 'Family', 'İstanbul'],
  ['Mehmet Yılmaz', 'Bride\'s', 'Family', 'İstanbul'],
  ['Zeynep Kaya', 'Groom\'s', 'Family', 'Ankara'],
  ['Emre Çelik', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Elif Şahin', 'Bride\'s', 'Friend', 'İzmir'],
  ['Burak Arslan', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Gökhan Doğan', 'Groom\'s', 'Friend', 'Bursa'],
  ['İrem Aksoy', 'Bride\'s', 'Colleague', 'İstanbul'],
  ['Oğuz Kılıç', 'Groom\'s', 'Family', 'Ankara'],
  ['Şule Erdoğan', 'Bride\'s', 'Family', 'İzmir'],
  ['Barış Koç', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Gülşen Aydın', 'Groom\'s', 'Family', 'Ankara'],
  ['Hakan Özkan', 'Bride\'s', 'Colleague', 'İstanbul'],
  ['Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein', 'Bride\'s', 'Friend', 'Berlin'],
  ['Cem Tekin', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Ebru Yıldız', 'Bride\'s', 'Friend', 'İstanbul'],
  ['Kerem Acar', 'Groom\'s', 'Friend', 'Ankara'],
  ['Pınar Şimşek', 'Bride\'s', 'Colleague', 'İstanbul'],
  ['Tolga Güneş', 'Groom\'s', 'Friend', 'İzmir'],
  ['Merve Kurt', 'Bride\'s', 'Friend', 'İstanbul'],
  ['Serkan Bulut', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Nazlı Uçar', 'Bride\'s', 'Friend', 'Bursa'],
  ['Onur Keskin', 'Groom\'s', 'Family', 'Ankara'],
  ['Sevgi Tan', 'Bride\'s', 'Family', 'İstanbul'],
  ['Yusuf Demirci', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Ece Karaca', 'Bride\'s', 'Friend', 'İzmir'],
  ['Ahmet Ateş', 'Groom\'s', 'Family', 'Ankara'],
  ['Leyla Özdemir', 'Bride\'s', 'Family', 'İstanbul'],
  ['Murat Ekinci', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Seda Uysal', 'Bride\'s', 'Colleague', 'İstanbul'],
  ['Arda Kocabaş', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Damla Erten', 'Bride\'s', 'Friend', 'Lisbon'],
  ['Kaan Sarı', 'Groom\'s', 'Friend', 'Amsterdam'],
  ['Buse Altun', 'Bride\'s', 'Friend', 'İstanbul'],
  ['Umut Çakır', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Esra Bayram', 'Bride\'s', 'Family', 'Bursa'],
  ['Volkan Taş', 'Groom\'s', 'Family', 'Ankara'],
  ['Gizem Tunç', 'Bride\'s', 'Friend', 'İstanbul'],
  ['Berk Ünal', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Ceren Işık', 'Bride\'s', 'Colleague', 'İstanbul'],
  ['Taylan Akın', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Aslı Yavuz', 'Bride\'s', 'Friend', 'İzmir'],
  ['Sinan Karakaya', 'Groom\'s', 'Family', 'Ankara'],
  ['Duygu Özer', 'Bride\'s', 'Friend', 'London'],
  ['Alper Turan', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Hande Yücel', 'Bride\'s', 'Family', 'İstanbul'],
  ['Erkan Tuna', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Özge Kara', 'Bride\'s', 'Colleague', 'İstanbul'],
  ['Yiğit Oral', 'Groom\'s', 'Friend', 'Berlin'],
  ['Dilek Sezer', 'Bride\'s', 'Family', 'İzmir'],
  ['İlker Bozkurt', 'Groom\'s', 'Family', 'Ankara'],
  ['Melis Çınar', 'Bride\'s', 'Friend', 'İstanbul'],
  ['Ozan Erbil', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Ilgın Kaplan', 'Bride\'s', 'Friend', 'İstanbul'],
  ['Çağrı Özbek', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Tuğba Sönmez', 'Bride\'s', 'Colleague', 'İstanbul'],
  ['Muhammed Abdurrahman Karaosmanoğlu Ertuğrul', 'Groom\'s', 'Family', 'Konya'],
  ['Jonas Weber', 'Bride\'s', 'Colleague', 'Berlin'],
  ['Sophie Laurent', 'Bride\'s', 'Friend', 'Lyon'],
  ['Liam O\'Connor', 'Groom\'s', 'Friend', 'Dublin'],
  ['Priya Raman', 'Bride\'s', 'Colleague', 'London'],
  ['Lucas Moreau', 'Groom\'s', 'Friend', 'Paris'],
  ['Hannah Schmidt', 'Bride\'s', 'Friend', 'Munich'],
  ['Mateo García', 'Groom\'s', 'Colleague', 'Madrid'],
  ['Chloe Bennett', 'Bride\'s', 'Friend', 'London'],
  ['Noah Fischer', 'Groom\'s', 'Colleague', 'Berlin'],
  ['Amara Okafor', 'Bride\'s', 'Friend', 'Amsterdam'],
  ['Sven Lindqvist', 'Groom\'s', 'Friend', 'Stockholm'],
  ['Isabella Rossi', 'Bride\'s', 'Colleague', 'Milan'],
  ['Kenji Watanabe', 'Groom\'s', 'Colleague', 'Tokyo'],
  ['Freya Nielsen', 'Bride\'s', 'Friend', 'Copenhagen'],
  ['Daniel Kowalski', 'Groom\'s', 'Friend', 'Warsaw'],
  ['Yasmin Haddad', 'Bride\'s', 'Friend', 'Beirut'],
  ['Tom Becker', 'Groom\'s', 'Colleague', 'Hamburg'],
  ['Olivia Hughes', 'Bride\'s', 'Friend', 'London'],
  ['Rafael Costa', 'Groom\'s', 'Friend', 'Lisbon'],
  ['Mia Andersson', 'Bride\'s', 'Colleague', 'Stockholm'],
  ['Anna-Katharina Rosenthal-Brückner', 'Bride\'s', 'Colleague', 'Vienna'],
  ['Babaanne', 'Groom\'s', 'Family', 'Ankara'],
  ['Dr. Hülya Öztürk (dentist)', 'Bride\'s', 'Friend', 'İstanbul'],
  ['Fatma Güler', 'Groom\'s', 'Family', 'Ankara'],
  ['Hasan Yalçın', 'Groom\'s', 'Family', 'Ankara'],
  ['Nur Aktaş', 'Bride\'s', 'Family', 'İstanbul'],
  ['Kemal Erdem', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Selma Korkmaz', 'Bride\'s', 'Family', 'İzmir'],
  ['Rıza Coşkun', 'Groom\'s', 'Family', 'Ankara'],
  ['Neslihan Avcı', 'Bride\'s', 'Friend', 'İstanbul'],
  ['Efe Gündoğdu', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Begüm Sağlam', 'Bride\'s', 'Friend', 'İstanbul'],
  ['Tarık Kalkan', 'Groom\'s', 'Colleague', 'İstanbul'],
  ['Canan Eren', 'Bride\'s', 'Colleague', 'Ankara'],
  ['Levent Öğüt', 'Groom\'s', 'Friend', 'İzmir'],
  ['Can Öztürk', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Zehra İnce', 'Bride\'s', 'Family', 'Bursa'],
  ['Ali Usta', 'Groom\'s', 'Friend', 'İstanbul'],
  ['Defne Altıntaş', 'Bride\'s', 'Friend', 'İstanbul'],
];
// duplicates appended later: 4 entries -> total 100
const ascii = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i').replace(/İ/g, 'I').replace(/ş/g, 's').replace(/ğ/g, 'g').replace(/ç/g, 'c').replace(/ö/g, 'o').replace(/ü/g, 'u');
const mailDomains = ['gmail.com', 'gmail.com', 'gmail.com', 'outlook.com', 'icloud.com', 'hotmail.com', 'yandex.com'];
const trPhone = () => `+90 5${int(30, 59)} ${int(100, 999)} ${pad(int(0, 99), 2)} ${pad(int(0, 99), 2)}`;
const intlPhone = (city) => {
  const m = { Berlin: '+49 30', Munich: '+49 89', Hamburg: '+49 40', London: '+44 20', Lyon: '+33 4', Paris: '+33 1', Dublin: '+353 1', Madrid: '+34 91', Amsterdam: '+31 20', Stockholm: '+46 8', Milan: '+39 02', Tokyo: '+81 3', Copenhagen: '+45', Warsaw: '+48 22', Beirut: '+961 1', Lisbon: '+351 21', Vienna: '+43 1' };
  return `${m[city] ?? '+44 20'} ${int(1000, 9999)} ${int(1000, 9999)}`;
};
const isTr = (city) => ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Konya'].includes(city);

const noPhone = new Set([13, 31, 43, 58, 71, 88]);
const multiPhone = new Set([1, 8, 11, 26, 45, 56, 79, 82]);
const noEmail = new Set([26, 78, 79, 81, 94, 85]);
const withPhoto = new Set([76, 0, 1, 2, 3, 4, 5, 7, 9, 10, 13, 15, 18, 19, 22, 24, 27, 30, 33, 37, 39, 44, 48, 51, 52, 57, 58, 59, 61, 64, 66, 70, 74, 77, 87, 91, 95]);

const contacts = people.map(([name, side, relationship, city], i) => {
  const id = `c${pad(i + 1)}`;
  const phones = [];
  if (!noPhone.has(i)) {
    phones.push({ label: 'Mobile', number: isTr(city) ? trPhone() : intlPhone(city) });
    if (multiPhone.has(i)) {
      phones.push({ label: pick(['Home', 'Work']), number: isTr(city) ? `+90 ${pick(['212', '216', '312', '232'])} ${int(200, 699)} ${pad(int(0, 99), 2)} ${pad(int(0, 99), 2)}` : intlPhone(city) });
      if (i % 3 === 0) phones.push({ label: 'Work', number: isTr(city) ? trPhone() : intlPhone(city) });
    }
  }
  const clean = ascii(name).toLowerCase().replace(/\(.*?\)/g, '').replace(/^dr\. /, '').trim();
  const parts = clean.split(/\s+/);
  const email = noEmail.has(i) ? null : `${parts[0]}.${parts[parts.length - 1]}`.replace(/[^a-z.\-]/g, '') + '@' + pick(mailDomains);
  return {
    id,
    name,
    phones,
    email,
    photo: withPhoto.has(i) ? `images/people/${id}.svg` : null,
    side,
    relationship,
    city,
    source: i < 88 ? 'contacts' : 'csv',
  };
});

// duplicates (4 more → 100)
const dup = (srcIdx, patch, reason) => {
  const s = contacts[srcIdx];
  const id = `c${pad(contacts.length + 1)}`;
  contacts.push({ ...structuredClone(s), id, photo: null, source: 'csv', ...patch });
  return { ids: [s.id, id], reason };
};
const duplicates = [
  dup(0, { name: 'Ayse Demir' }, 'Same phone number, similar name'),
  dup(92, { name: 'Can Ozturk', phones: [{ label: 'Mobile', number: trPhone() }] }, 'Same email, similar name'),
  dup(4, { phones: [{ label: 'Work', number: '+90 232 000 18 07' }], email: 'elif.sahin@example.org' }, 'Same name'),
  dup(57, {}, 'Identical name, phone and email'),
];
// fix: Ayse Demir keeps same phone; Can Ozturk keeps same email (structuredClone did that)

// ---------------- members & decisions (shared wedding list) ----------------
const members = [
  { id: 'u-deniz', name: 'Deniz Yılmaz', email: 'deniz.yilmaz@example.com', role: 'Owner', isDecisionMaker: false, isMe: true, avatar: 'images/people/u-deniz.svg', joinedAt: '2026-09-27T19:02:00Z' },
  { id: 'u-mert', name: 'Mert Aydın', email: 'mert.aydin@example.com', role: 'Collaborator', isDecisionMaker: true, isMe: false, avatar: 'images/people/u-mert.svg', joinedAt: '2026-09-28T08:15:00Z' },
  { id: 'u-selin', name: 'Selin Yılmaz', email: 'selin.yilmaz@example.com', role: 'Collaborator', isDecisionMaker: false, isMe: false, avatar: null, joinedAt: '2026-10-02T17:40:00Z' },
];
// Targets: Deniz 76 decided (A48 R17 M11), Mert 88, Selin 41.
const D = ['accept', 'reject', 'maybe'];
const ids = contacts.map((c) => c.id);
const deniz = {}, mert = {}, selin = {};
// Deniz: first 76 in original order
const dz = [...Array(48).fill('accept'), ...Array(17).fill('reject'), ...Array(11).fill('maybe')];
for (let i = dz.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [dz[i], dz[j]] = [dz[j], dz[i]]; }
ids.slice(0, 76).forEach((id, i) => (deniz[id] = dz[i]));
// Mert: 88 items: mostly same as Deniz, some diffs
ids.forEach((id, i) => {
  if (i >= 88) return;
  const d = deniz[id];
  if (d && rnd() < 0.9) mert[id] = d;
  else mert[id] = d ? pick(D.filter((x) => x !== d)) : pick(['accept', 'accept', 'reject', 'maybe']);
});
// Selin: 41 items spread across first 80, but skipping some
const selinIds = ids.filter((_, i) => i < 80 && (i % 2 === 0 || i < 12)).slice(0, 41);
selinIds.forEach((id) => {
  const base = deniz[id] ?? mert[id];
  selin[id] = rnd() < 0.88 ? base : pick(D.filter((x) => x !== base));
});
// Force a few conflicts where Mert (Decision Maker) never decided: items 89-92 by Deniz? Deniz only first 76.
// Add Selin decisions differing from Deniz on items Mert has not decided: give Mert gaps.
mert['c079'] = 'accept'; // matches Mert's note "Obviously yes."
for (const id of ['c012', 'c034', 'c056']) {
  delete mert[id];
  selin[id] = deniz[id] === 'accept' ? 'reject' : 'accept';
}
const notes = [
  { itemId: 'c001', author: 'u-deniz', text: 'Mum insists. Seat near the family table.', private: false, createdAt: '2026-09-28T20:11:00Z' },
  { itemId: 'c004', author: 'u-mert', text: 'University roommate, has to be there.', private: false, createdAt: '2026-09-29T09:02:00Z' },
  { itemId: 'c006', author: 'u-deniz', text: 'Only if we invite the whole team.', private: true, createdAt: '2026-09-28T20:14:00Z' },
  { itemId: 'c012', author: 'u-selin', text: 'Haven\'t seen her in years, maybe skip?', private: false, createdAt: '2026-10-03T11:30:00Z' },
  { itemId: 'c014', author: 'u-deniz', text: 'Flying in from Berlin. Ask about dates first.', private: false, createdAt: '2026-09-28T20:20:00Z' },
  { itemId: 'c021', author: 'u-mert', text: 'My manager. Awkward to leave out.', private: true, createdAt: '2026-09-29T09:20:00Z' },
  { itemId: 'c033', author: 'u-deniz', text: 'Plus one? Check with Buse.', private: false, createdAt: '2026-09-28T20:31:00Z' },
  { itemId: 'c057', author: 'u-mert', text: 'Dad\'s cousin from Konya. Dad wants him there.', private: false, createdAt: '2026-09-29T10:05:00Z' },
  { itemId: 'c079', author: 'u-mert', text: 'Obviously yes.', private: false, createdAt: '2026-09-29T10:12:00Z' },
  { itemId: 'c080', author: 'u-deniz', text: 'Dentist, not sure why she is in my contacts list.', private: true, createdAt: '2026-09-28T20:40:00Z' },
];
const edits = [
  { itemId: 'c007', field: 'phone', original: '+90 500 000 77 1', value: '+90 500 000 77 12', editedBy: 'u-deniz', editedAt: '2026-09-28T20:12:00Z' },
  { itemId: 'c014', field: 'name', original: 'Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein', value: 'Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein', note: 'unchanged sample: see c080', editedBy: null },
  { itemId: 'c079', field: 'name', original: 'Babaanne', value: 'Babaanne (Nermin Aydın)', editedBy: 'u-mert', editedAt: '2026-09-29T10:11:00Z' },
  { itemId: 'c045', field: 'city', original: 'İstanbul', value: 'Ankara', editedBy: 'u-deniz', editedAt: '2026-09-30T18:00:00Z' },
].filter((e) => e.editedBy);
// apply edited values to contacts (working copy) so UI shows edited value
for (const e of edits) {
  const c = contacts.find((x) => x.id === e.itemId);
  if (e.field === 'phone') { e.original = c.phones[0].number.slice(0, -1); c.phones[0].number = c.phones[0].number; e.value = c.phones[0].number; }
  else c[e.field] = e.value;
}

const all = [deniz, mert, selin];
const statusOf = (id) => {
  const ds = all.map((m) => m[id]).filter(Boolean);
  if (ds.length >= 2 && new Set(ds).size > 1) return 'conflict';
  if (ds.length < 3) return 'pending';
  return 'agreed';
};
const sharedItems = ids.map((id) => {
  const status = statusOf(id);
  return {
    itemId: id,
    decisions: { 'u-deniz': deniz[id] ?? null, 'u-mert': mert[id] ?? null, 'u-selin': selin[id] ?? null },
    status,
    finalDecision: status === 'agreed' ? deniz[id] : null,
  };
});
const count = (obj, d) => Object.values(obj).filter((x) => x === d).length;
const st = (s) => sharedItems.filter((x) => x.status === s).length;
const conflicts = sharedItems.filter((x) => x.status === 'conflict');
const dmUndecidedConflicts = conflicts.filter((x) => !x.decisions['u-mert']).length;

// ---------------- products ----------------
const products = [
  ['Ergo Mesh task chair', 389, 4.6, 1240, 'Nordhaus', 'Chair'],
  ['Walnut sit-stand desk, 140 × 70 cm', 649, 4.7, 532, 'Oakline', 'Desk'],
  ['27-inch 4K USB-C monitor', 429, 4.5, 2870, 'Pixelhaus', 'Monitor'],
  ['Low-profile mechanical keyboard', 129, 4.4, 980, 'Keystone', 'Keyboard'],
  ['Ceramic desk lamp with dimmer', 79, 4.2, 211, 'Lumen & Co', 'Lamp'],
  ['Wool felt desk mat, large', 39, 4.8, 1410, 'Oakline', 'Accessory'],
  ['Monitor arm with gas spring, single', 99, 4.3, 655, 'Pixelhaus', 'Accessory'],
  ['Noise-cancelling over-ear headphones', 299, 4.6, 5120, 'SoundForm', 'Headphones'],
  ['Pothos plant in matte pot', 24, 4.1, 88, 'Greenroom', 'Plant'],
  ['Cable tray, under-desk', 35, 4.0, 340, 'Keystone', 'Accessory'],
  ['Ergonomic vertical mouse', 59, 3.9, 1720, 'Keystone', 'Mouse'],
  ['Saddle stool with rocking base', 219, 3.7, 96, 'Nordhaus', 'Chair'],
  ['Oak monitor riser with drawer', 69, 4.5, 412, 'Oakline', 'Accessory'],
  ['Webcam 1080p with privacy shutter', 89, 4.1, 2210, 'Pixelhaus', 'Webcam'],
  ['Pendant lamp, opal glass', 149, null, 0, 'Lumen & Co', 'Lamp'],
  ['Ceramic pour-over coffee set with kettle, scale and two double-walled glass cups', 119, 4.4, 307, 'Greenroom', 'Accessory'],
  ['Acoustic felt wall panels, set of 6', 179, 4.0, 145, 'SoundForm', 'Accessory'],
  ['Bookshelf speakers, pair', 249, 4.7, 890, 'SoundForm', 'Speakers'],
  ['Footrest with massage rollers', 45, 3.8, 260, 'Nordhaus', 'Accessory'],
  ['Mesh chair, budget edition', 149, 3.5, 3080, 'DeskDepot', 'Chair'],
].map(([name, price, rating, reviews, store, category], i) => ({
  id: `p${pad(i + 1, 2)}`, name, price, currency: 'EUR', rating, reviews, store, category,
  link: `https://${store.toLowerCase().replace(/[^a-z]/g, '')}.example/p/${1000 + i * 37}`,
  photo: `images/products/p${pad(i + 1, 2)}.svg`,
}));
const productDecisions = ['accept', 'accept', 'accept', 'maybe', 'reject', 'accept', 'maybe', 'reject', 'accept', 'reject', 'reject', 'reject', 'maybe', 'reject', 'maybe', 'maybe', 'reject', 'maybe', 'reject', 'reject'];
// Round 2 (Maybe pile): p04 accept, p07 accept, p13 reject, p15 accept, p16 reject, p18 maybe

// ---------------- photos ----------------
const places = [['Moda, İstanbul', 'sea'], ['Kadıköy, İstanbul', 'city'], ['Göreme, Cappadocia', 'hills'], ['Alfama, Lisbon', 'city'], ['Belém, Lisbon', 'sea'], [null, 'indoor'], ['Belgrad Forest, İstanbul', 'forest'], ['Cihangir, İstanbul', 'city']];
const photos = Array.from({ length: 30 }, (_, i) => {
  const [location, scene] = places[Math.floor(i / 4) % places.length];
  const day = 1 + Math.floor(i / 2);
  return {
    id: `ph${pad(i + 1, 2)}`,
    fileName: `IMG_${2041 + i}.JPG`,
    takenAt: `2026-03-${pad(Math.min(day, 31), 2)}T${pad(9 + (i % 11), 2)}:${pad((i * 7) % 60, 2)}:00`,
    location,
    scene,
    sizeMB: +(1.8 + rnd() * 3.4).toFixed(1),
    width: i % 5 === 3 ? 3024 : 4032,
    height: i % 5 === 3 ? 4032 : 3024,
    similarTo: i % 4 === 1 ? `ph${pad(i, 2)}` : null,
    photo: `images/photos/ph${pad(i + 1, 2)}.svg`,
  };
});

// ---------------- small datasets for other sources ----------------
const books = ['The Remains of the Day', 'Piranesi', 'Kürk Mantolu Madonna', 'Klara and the Sun', 'Tomorrow, and Tomorrow, and Tomorrow', 'Beyaz Kale', 'A Gentleman in Moscow', 'The Overstory', 'İnce Memed', 'Station Eleven', 'Sapiens', 'The Left Hand of Darkness'];
const apartments = [
  ['Moda Cd. 112, Kadıköy', 42000, '2+1', 95, '2026-10-12 11:00', 'Kadıköy'],
  ['Bahariye Cd. 48, Kadıköy', 38500, '2+1', 88, '2026-10-12 13:30', 'Kadıköy'],
  ['Yeldeğirmeni, Misak-ı Milli Sk. 7', 31000, '1+1', 62, '2026-10-13 10:00', 'Kadıköy'],
  ['Caferağa, Dumlupınar Sk. 21', 45000, '3+1', 120, '2026-10-13 15:00', 'Kadıköy'],
  ['Abbasağa, Ihlamurdere Cd. 33', 48000, '2+1', 90, '2026-10-14 12:00', 'Beşiktaş'],
  ['Sinanpaşa, Şair Nedim Cd. 9', 52000, '3+1', 115, '2026-10-14 17:00', 'Beşiktaş'],
  ['Türkali, Ihlamur Yolu 4', 39500, '1+1', 58, null, 'Beşiktaş'],
  ['Akaretler Sıraevler 18', 95000, '3+1', 160, '2026-10-15 09:30', 'Beşiktaş'],
].map(([address, rent, rooms, sizeM2, viewing, tab], i) => ({ id: `a${pad(i + 1, 2)}`, address, rent, currency: 'TRY', rooms, sizeM2, viewing, tab, link: `https://listings.example/ist/${48210 + i * 13}` }));
const candidates = [
  ['Lena Hoffmann', 'Frontend engineer', 6, 'Berlin', 78000, 'https://lenahoffmann.example', 'lena.hoffmann@example.com', 'Referral'],
  ['Kaan Yurt', 'Frontend engineer', 4, 'İstanbul', 62000, 'https://kaanyurt.example', 'kaan.yurt@example.com', 'LinkedIn'],
  ['Aisha Bello', 'Frontend engineer', 8, 'London', 92000, 'https://aisha.example', 'aisha.bello@example.com', 'Careers page'],
  ['Marco Bianchi', 'Frontend engineer', 3, 'Milan', null, null, 'marco.bianchi@example.com', 'Careers page'],
  ['Ece Doğru', 'Frontend engineer', 5, 'Remote (Ankara)', 60000, 'https://code.example/ecedogru', 'ece.dogru@example.com', 'Referral'],
  ['Pieter de Vries', 'Frontend engineer', 10, 'Amsterdam', 105000, 'https://pieterdevries.nl', 'pieter@example.com', 'Agency'],
  ['Sun-hee Park', 'Frontend engineer', 2, 'Seoul', 54000, 'https://sunhee.park', 'sunhee.park@example.com', 'LinkedIn'],
  ['Jakub Nowak', 'Frontend engineer', 7, 'Kraków', 70000, null, 'jakub.nowak@example.com', 'Careers page'],
  ['Carolina Mendes Albuquerque de Souza', 'Frontend engineer', 5, 'Porto', 66000, 'https://carolina.codes', 'carolina.souza@example.com', 'Referral'],
  ['Tunç Ersoy', 'Frontend engineer', 9, 'İzmir', 88000, 'https://tuncersoy.com', 'tunc@example.com', 'LinkedIn'],
  ['Grace Liu', 'Frontend engineer', 4, 'Toronto', 81000, 'https://graceliu.ca', 'grace.liu@example.com', 'Careers page'],
  ['Omar Farouk', 'Frontend engineer', 6, 'Cairo', 48000, 'https://omarfarouk.example', 'omar.farouk@example.com', 'Agency'],
].map(([name, role, years, location, salary, portfolio, email, source], i) => ({ id: `k${pad(i + 1, 2)}`, name, role, yearsExperience: years, location, expectedSalary: salary, currency: 'EUR', portfolio, email, source }));

// ---------------- templates ----------------
const templates = [
  { id: 't-person', name: 'Person', builtIn: true, layout: { image: 'avatar', title: 'name', subtitle: 'relationship', rows: ['phone', 'email', 'city'], tags: ['side'] } },
  { id: 't-product', name: 'Product', builtIn: true, layout: { image: 'cover', title: 'name', subtitle: 'store', rows: ['price', 'rating'], tags: ['category'] } },
  { id: 't-photo', name: 'Photo', builtIn: true, layout: { image: 'full', title: 'takenAt', subtitle: 'location', rows: ['fileName', 'sizeMB'], tags: [] } },
  { id: 't-task', name: 'Task', builtIn: true, layout: { image: 'none', title: 'title', subtitle: 'due', rows: ['owner', 'estimate'], tags: ['priority'] } },
  { id: 't-candidate', name: 'Candidate', builtIn: true, layout: { image: 'avatar', title: 'name', subtitle: 'role', rows: ['yearsExperience', 'location', 'expectedSalary', 'portfolio'], tags: ['source'] } },
  { id: 't-generic', name: 'Generic', builtIn: true, layout: { image: 'none', title: 'first field', subtitle: 'second field', rows: ['next 4 fields'], tags: [] } },
  { id: 't-wedding-table', name: 'Guest with table side', builtIn: false, basedOn: 't-person', createdAt: '2026-09-28T19:30:00Z', usedBy: [], layout: { image: 'avatar', title: 'name', subtitle: 'side', rows: ['relationship', 'phone'], tags: ['city'] } },
  { id: 't-candidate-compact', name: 'Candidate, compact', builtIn: false, basedOn: 't-candidate', createdAt: '2026-10-08T14:00:00Z', usedBy: ['l-candidates'], layout: { image: 'none', title: 'name', subtitle: 'location', rows: ['yearsExperience', 'expectedSalary'], tags: ['source'] } },
];

// ---------------- lists ----------------
const lists = [
  {
    id: 'l-wedding', name: 'Wedding guests', emoji: null, template: 't-person', itemCount: 100,
    sources: [{ type: 'contacts', count: 88 }, { type: 'csv', fileName: 'mert-family.csv', count: 12 }],
    shared: true, owner: 'u-deniz', conflictRule: 'decisionMaker', currentRound: 'r-w1',
    updatedAt: '2026-10-09T21:14:00Z', backedUp: true, archived: false,
  },
  {
    id: 'l-desk', name: 'Desk setup', template: 't-product', itemCount: 20, sources: [{ type: 'manual', count: 20 }],
    shared: false, currentRound: 'r-d2', updatedAt: '2026-10-06T12:40:00Z', backedUp: false, archived: false,
  },
  {
    id: 'l-photos', name: 'March photos clean-up', template: 't-photo', itemCount: 30, sources: [{ type: 'photos', count: 30 }],
    shared: false, currentRound: 'r-p1', updatedAt: '2026-10-08T08:05:00Z', backedUp: false, archived: false,
  },
  {
    id: 'l-candidates', name: 'Frontend hiring, Q4', template: 't-candidate-compact', itemCount: 12,
    sources: [{ type: 'csv', fileName: 'candidates-q4.csv', count: 12 }], shared: false, currentRound: null,
    updatedAt: '2026-10-08T14:02:00Z', backedUp: false, archived: false,
  },
  {
    id: 'l-apartments', name: 'Apartment viewings', template: 't-generic', itemCount: 8,
    sources: [{ type: 'googleSheets', sheet: 'Flat hunt 2026', tabs: ['Kadıköy', 'Beşiktaş'], count: 8 }], shared: false,
    currentRound: 'r-a1', updatedAt: '2026-07-21T19:20:00Z', backedUp: true, archived: true,
  },
  {
    id: 'l-books', name: 'Book club picks', template: 't-generic', itemCount: 12, sources: [{ type: 'text', count: 12 }],
    shared: false, currentRound: 'r-b1', updatedAt: '2026-05-02T16:00:00Z', backedUp: true, archived: true,
  },
];

const rounds = [
  { id: 'r-w1', listId: 'l-wedding', number: 1, name: 'Round 1', include: 'all', order: 'original', itemCount: 100, startedBy: 'u-deniz', startedAt: '2026-09-28T19:05:00Z', completedAt: null,
    progress: { 'u-deniz': { decided: 76, accept: count(deniz, 'accept'), reject: count(deniz, 'reject'), maybe: count(deniz, 'maybe') }, 'u-mert': { decided: Object.keys(mert).length, accept: count(mert, 'accept'), reject: count(mert, 'reject'), maybe: count(mert, 'maybe') }, 'u-selin': { decided: Object.keys(selin).length, accept: count(selin, 'accept'), reject: count(selin, 'reject'), maybe: count(selin, 'maybe') } },
    listStatus: { agreed: st('agreed'), pending: st('pending'), conflict: st('conflict'), conflictsDecisionMakerUndecided: dmUndecidedConflicts } },
  { id: 'r-d1', listId: 'l-desk', number: 1, name: 'Round 1', include: 'all', order: 'original', itemCount: 20, startedAt: '2026-10-04T10:00:00Z', completedAt: '2026-10-04T10:06:00Z',
    result: { accept: 5, reject: 9, maybe: 6 }, durationSec: 352 },
  { id: 'r-d2', listId: 'l-desk', number: 2, name: 'Round 2', include: 'maybe', order: 'shuffled', itemCount: 6, startedAt: '2026-10-06T12:30:00Z', completedAt: '2026-10-06T12:33:00Z',
    result: { accept: 3, reject: 2, maybe: 1 }, durationSec: 141 },
  { id: 'r-p1', listId: 'l-photos', number: 1, name: 'Round 1', include: 'all', order: 'sortedBy:takenAt', itemCount: 30, startedAt: '2026-10-08T08:00:00Z', completedAt: null,
    progress: { me: { decided: 12, accept: 5, reject: 6, maybe: 1 } } },
  { id: 'r-a1', listId: 'l-apartments', number: 1, name: 'Round 1', include: 'all', order: 'original', itemCount: 8, completedAt: '2026-07-21T19:20:00Z', result: { accept: 3, reject: 4, maybe: 1 } },
  { id: 'r-b1', listId: 'l-books', number: 1, name: 'Round 1', include: 'all', order: 'shuffled', itemCount: 12, completedAt: '2026-05-02T16:00:00Z', result: { accept: 4, reject: 6, maybe: 2 } },
];

const activity = [
  { id: 'ev1', listId: 'l-wedding', type: 'roundStarted', actor: 'u-deniz', at: '2026-09-28T19:05:00Z', text: 'Deniz started Round 1 with 100 items' },
  { id: 'ev2', listId: 'l-wedding', type: 'memberJoined', actor: 'u-mert', at: '2026-09-28T08:15:00Z', text: 'Mert joined the list' },
  { id: 'ev3', listId: 'l-wedding', type: 'roleChanged', actor: 'u-deniz', target: 'u-mert', at: '2026-09-28T08:20:00Z', text: 'Deniz made Mert the Decision Maker' },
  { id: 'ev4', listId: 'l-wedding', type: 'memberFinished', actor: 'u-selin', at: '2026-10-10T09:30:00Z', text: 'Selin finished sorting', future: true, $note: 'Illustrative future event for S38: shown in the activity feed state after Selin decides all 100 items' },
  { id: 'ev5', listId: 'l-wedding', type: 'memberJoined', actor: 'u-selin', at: '2026-10-02T17:40:00Z', text: 'Selin joined the list' },
  { id: 'ev6', listId: 'l-wedding', type: 'newConflicts', at: '2026-10-03T11:45:00Z', count: st('conflict'), text: `${st('conflict')} new conflicts` },
  { id: 'ev7', listId: 'l-wedding', type: 'conflictsResolved', actor: 'u-mert', at: '2026-10-09T21:14:00Z', count: 3, text: 'Mert resolved 3 conflicts' },
];

const data = {
  $description: 'SwipeSort shared sample data. Every mockup uses these records. Images are generated SVG illustrations in design/02-data/images (no text, no hotlinks). Dates are ISO 8601; "today" in the mockups is 2026-10-10.',
  today: '2026-10-10',
  me: { signedIn: { id: 'u-deniz', name: 'Deniz Yılmaz', email: 'deniz.yilmaz@example.com', google: 'deniz.yilmaz@example.com', avatar: 'images/people/u-deniz.svg' }, guest: { name: null, deviceLists: ['l-desk', 'l-photos', 'l-candidates'] } },
  members,
  lists,
  templates,
  rounds,
  fields: {
    contacts: [
      { key: 'name', label: 'Name', type: 'text', title: true },
      { key: 'phones', label: 'Phone', type: 'phone', multi: true },
      { key: 'email', label: 'Email', type: 'email' },
      { key: 'photo', label: 'Photo', type: 'image' },
      { key: 'side', label: 'Side', type: 'text' },
      { key: 'relationship', label: 'Relationship', type: 'text' },
      { key: 'city', label: 'City', type: 'text' },
    ],
    products: [
      { key: 'name', label: 'Name', type: 'text', title: true }, { key: 'price', label: 'Price', type: 'number' }, { key: 'rating', label: 'Rating', type: 'number' },
      { key: 'reviews', label: 'Reviews', type: 'number' }, { key: 'store', label: 'Store', type: 'text' }, { key: 'category', label: 'Category', type: 'text' }, { key: 'link', label: 'Link', type: 'link' }, { key: 'photo', label: 'Photo', type: 'image' },
    ],
    photos: [{ key: 'photo', label: 'Photo', type: 'image' }, { key: 'takenAt', label: 'Taken', type: 'date', title: true }, { key: 'location', label: 'Location', type: 'text' }, { key: 'fileName', label: 'File name', type: 'text' }, { key: 'sizeMB', label: 'Size (MB)', type: 'number' }],
    candidates: [{ key: 'name', label: 'Name', type: 'text', title: true }, { key: 'role', label: 'Role', type: 'text' }, { key: 'yearsExperience', label: 'Years of experience', type: 'number' }, { key: 'location', label: 'Location', type: 'text' }, { key: 'expectedSalary', label: 'Expected salary', type: 'number' }, { key: 'portfolio', label: 'Portfolio', type: 'link' }, { key: 'email', label: 'Email', type: 'email' }, { key: 'source', label: 'Source', type: 'text' }],
  },
  contacts,
  duplicates,
  products,
  productDecisions: { round1: Object.fromEntries(products.map((p, i) => [p.id, productDecisions[i]])), round2: { p04: 'accept', p07: 'accept', p13: 'reject', p15: 'accept', p16: 'reject', p18: 'maybe' } },
  photos,
  photoDecisions: { round1: { ph01: 'accept', ph02: 'reject', ph03: 'accept', ph04: 'reject', ph05: 'accept', ph06: 'reject', ph07: 'maybe', ph08: 'reject', ph09: 'accept', ph10: 'reject', ph11: 'accept', ph12: 'reject' } },
  books,
  apartments,
  candidates,
  shared: {
    listId: 'l-wedding',
    myDecisions: deniz,
    items: sharedItems,
    notes,
    edits,
    summary: { agreed: st('agreed'), pending: st('pending'), conflict: st('conflict'), conflictsDecisionMakerUndecided: dmUndecidedConflicts },
  },
  activity,
  notificationPreferences: { memberJoined: true, memberFinished: true, newConflicts: true, conflictsResolved: true, roundStarted: true, roleChanged: true },
};
writeFileSync(out, JSON.stringify(data, null, 2) + '\n');
console.log('contacts', contacts.length, 'summary', data.shared.summary, 'deniz', rounds[0].progress);
console.log('conflict ids', conflicts.map((c) => c.itemId).join(' '));
