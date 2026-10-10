# Usage: python3 tools/generators/S31-S34-collaboration.py
# Generates the Group G1 collaboration mockups (static frames):
#   design/03-screens/S31-invite.html, S32-invite-link.html, S33-join-list.html, S34-members.html
# Structure follows tools/generators/S25-sorting.py (the quality reference).
import os
import itertools
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCREENS = os.path.join(ROOT, 'design', '03-screens')
IMG = '../02-data/images/'
BRAND = '../01-foundations/brand/'

# ---- QR code (verified against segno 1.6.6: same modules apart from the optional pad byte) ----
# Minimal QR encoder: version 2, EC level L, byte mode, mask 0 (enough for short URLs, <= 32 bytes).
def _gmul(x, y):
    z = 0
    for i in range(7, -1, -1):
        z = (z << 1) ^ ((z >> 7) * 0x11D)
        z ^= ((y >> i) & 1) * x
    return z & 0xFF

def _rs_divisor(deg):
    r = [0] * (deg - 1) + [1]; root = 1
    for _ in range(deg):
        for j in range(len(r)):
            r[j] = _gmul(r[j], root)
            if j + 1 < len(r): r[j] ^= r[j + 1]
        root = _gmul(root, 2)
    return r

def _rs_rem(data, div):
    r = [0] * len(div)
    for b in data:
        f = b ^ r.pop(0); r.append(0)
        for i, c in enumerate(div): r[i] ^= _gmul(c, f)
    return r

def qr_matrix(text):
    size, ndata, nec = 25, 34, 10
    data = text.encode()
    assert len(data) <= 32
    bits = [0, 1, 0, 0] + [(len(data) >> i) & 1 for i in range(7, -1, -1)]
    for b in data: bits += [(b >> i) & 1 for i in range(7, -1, -1)]
    bits += [0] * min(4, ndata * 8 - len(bits))
    bits += [0] * (-len(bits) % 8)
    cw = [int(''.join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    pad = [0xEC, 0x11]; i = 0
    while len(cw) < ndata: cw.append(pad[i % 2]); i += 1
    cw += _rs_rem(cw, _rs_divisor(nec))
    M = [[False] * size for _ in range(size)]; F = [[False] * size for _ in range(size)]
    def setf(x, y, d): M[y][x] = d; F[y][x] = True
    for i in range(size): setf(6, i, i % 2 == 0); setf(i, 6, i % 2 == 0)
    for cx, cy in ((3, 3), (size - 4, 3), (3, size - 4)):
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                x, y = cx + dx, cy + dy
                if 0 <= x < size and 0 <= y < size:
                    setf(x, y, max(abs(dx), abs(dy)) not in (2, 4))
    for dy in range(-2, 3):
        for dx in range(-2, 3): setf(18 + dx, 18 + dy, max(abs(dx), abs(dy)) != 1)
    def fmt(mask):
        d = (1 << 3) | mask; r = d
        for _ in range(10): r = (r << 1) ^ ((r >> 9) * 0x537)
        b = ((d << 10) | r) ^ 0x5412
        g = lambda i: (b >> i) & 1 == 1
        for i in range(6): setf(8, i, g(i))
        setf(8, 7, g(6)); setf(8, 8, g(7)); setf(7, 8, g(8))
        for i in range(9, 15): setf(14 - i, 8, g(i))
        for i in range(8): setf(size - 1 - i, 8, g(i))
        for i in range(8, 15): setf(8, size - 15 + i, g(i))
        setf(8, size - 8, True)
    fmt(0)
    i = 0; right = size - 1
    while right >= 1:
        if right == 6: right = 5
        for vert in range(size):
            for j in range(2):
                x = right - j
                up = ((right + 1) & 2) == 0
                y = size - 1 - vert if up else vert
                if not F[y][x] and i < len(cw) * 8:
                    M[y][x] = (cw[i >> 3] >> (7 - (i & 7))) & 1 == 1; i += 1
        right -= 2
    for y in range(size):
        for x in range(size):
            if not F[y][x] and (x + y) % 2 == 0: M[y][x] = not M[y][x]
    fmt(0)
    return M

def qr_svg(text, cls='size-40', label=''):
    M = qr_matrix(text); n = len(M); q = 4
    d = ''.join(f'M{x + q} {y + q}h1v1h-1z' for y in range(n) for x in range(n) if M[y][x])
    return f'<svg viewBox="0 0 {n + 2 * q} {n + 2 * q}" class="{cls}" role="img" aria-label="{label}" shape-rendering="crispEdges"><path d="{d}" fill="currentColor"/></svg>'

_ids = itertools.count(1)
def uid(prefix='g'):
    return f'{prefix}{next(_ids)}'

NAMES = ['Wedding guests', 'Deniz Yılmaz', 'Mert Aydın', 'Selin Yılmaz']
def keep(text):
    """Keep names on one line in centered text (QA-091)."""
    for n in NAMES:
        text = text.replace(n, f'<span class="whitespace-nowrap">{n}</span>')
    return text

def icon(name, size='size-5', extra=''):
    return f'<i class="i-lucide-{name} {size} {extra}" aria-hidden="true"></i>'.replace('  ', ' ').replace(' "', '"')

# ---------------------------------------------------------------- people and data
P = {
    'deniz': dict(name='Deniz Yılmaz', first='Deniz', img='people/u-deniz.svg', ini='DY', email='deniz.yilmaz@example.com', done=76, joined='Sep 27'),
    'mert': dict(name='Mert Aydın', first='Mert', img='people/u-mert.svg', ini='MA', email='mert.aydin@example.com', done=85, joined='Sep 28'),
    'selin': dict(name='Selin Yılmaz', first='Selin', img=None, ini='SY', email='selin.yilmaz@example.com', done=43, joined='Oct 2'),
}
TOKEN = 'k4Rm9Tq2'
TOKEN_NEW = 'Pz83vLwe'
TOKEN_SELIN = 's7Lw2Qe9'

AV_TXT = {'size-6': 'text-caption', 'size-8': 'text-caption', 'size-10': 'text-label', 'size-12': 'text-label-lg', 'size-14': 'text-title-3', 'size-16': 'text-title-2'}

def av(k, size='size-10', ring='', alt=False):
    p = P[k]
    if p['img']:
        a = p['name'] if alt else ''
        return f'<img src="{IMG}{p["img"]}" alt="{a}" class="{size} shrink-0 rounded-full {ring}">'
    lab = f'role="img" aria-label="{p["name"]}"' if alt else 'aria-hidden="true"'
    return f'<span class="flex {size} shrink-0 items-center justify-center rounded-full bg-muted {AV_TXT.get(size, "text-label")} text-muted-foreground {ring}" {lab}>{p["ini"]}</span>'

def avatar_stack(keys, size='size-8', ring='ring-background'):
    names = ', '.join(P[k]['first'] for k in keys)
    inner = ''.join(av(k, size, f'ring-2 {ring}') for k in keys)
    return f'<div class="flex -space-x-2" role="img" aria-label="{len(keys)} member{"s" if len(keys) != 1 else ""}: {names}">{inner}</div>'

def badge_owner():
    return f'<span class="inline-flex h-7 items-center gap-1.5 rounded-full bg-secondary px-2.5 text-caption text-secondary-foreground">{icon("crown", "size-4")}Owner</span>'

def badge_dm():
    return f'<span class="inline-flex h-7 items-center gap-1.5 rounded-full bg-primary-soft px-2.5 text-caption text-primary-soft-foreground">{icon("gavel", "size-4")}Decision Maker</span>'

def role_badges(roles):
    out = []
    if 'owner' in roles: out.append(badge_owner())
    if 'dm' in roles: out.append(badge_dm())
    if not out: out.append('<span class="inline-flex h-7 items-center text-body-sm text-muted-foreground">Collaborator</span>')
    return f'<div class="mt-1 flex flex-wrap gap-1.5">{"".join(out)}</div>'

def role_words(roles):
    w = []
    if 'owner' in roles: w.append('Owner')
    if 'dm' in roles: w.append('Decision Maker')
    return ', '.join(w) or 'Collaborator'

def role_line(roles, large=False):
    parts = []
    if 'owner' in roles: parts.append(f'<span class="inline-flex items-center gap-1 whitespace-nowrap">{icon("crown", "size-4 shrink-0")}Owner</span>')
    if 'dm' in roles: parts.append(f'<span class="inline-flex items-center gap-1 whitespace-nowrap">{icon("gavel", "size-4 shrink-0")}Decision Maker</span>')
    if not parts: parts.append('<span class="whitespace-nowrap">Collaborator</span>')
    return f'<span class="flex min-w-0 flex-wrap items-center gap-x-3 {"text-body-lg" if large else "text-body-sm"} text-muted-foreground">{"".join(parts)}</span>'

def member_block(k, roles, you=False, large=False, done=None):
    """Name, role and progress for a member: MemberRow body (role text + count on one line, bar below)."""
    p = P[k]
    d = p['done'] if done is None else done
    y = ' <span class="text-muted-foreground">(you)</span>' if you else ''
    t_cls = 'text-title-3 font-normal' if large else 'text-body'
    pct = 'w-full' if d >= 100 else ('w-0' if d == 0 else f'w-[{d}%]')
    fin = f'<span class="ml-2 inline-flex items-center gap-1 align-middle text-label text-foreground">{icon("circle-check", "size-4")}Finished</span>' if d >= 100 else ''
    cnt = f'<span class="shrink-0 {"text-body-lg" if large else "text-caption"} tabular-nums text-muted-foreground">{d} / 100 decided</span>'
    bar = f'<div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="{d}" aria-valuemin="0" aria-valuemax="100" aria-label="{p["first"]}: {d} of 100 decided"><div class="h-full {pct} rounded-full bg-primary"></div></div>'
    if large:
        return f'<div class="min-w-0 flex-1"><p class="{t_cls}">{p["name"]}{y}{fin}</p>{role_line(roles, True)}{bar}<p class="mt-1 text-body-lg tabular-nums text-muted-foreground">{d} / 100 decided</p></div>'
    bar_row = f'<div class="mt-1.5 flex items-center gap-3"><div class="min-w-0 flex-1">{bar.replace("mt-2 ", "")}</div>{cnt.replace("shrink-0", "shrink-0 whitespace-nowrap")}</div>'
    return f'<div class="min-w-0 flex-1"><p class="{t_cls}">{p["name"]}{y}{fin}</p><div class="mt-0.5">{role_line(roles)}</div>{bar_row}</div>'

def progress(done, total=100, who='', large=False):
    pct = 'w-full' if done >= total else ('w-0' if done == 0 else f'w-[{round(done * 100 / total)}%]')
    fin = done >= total
    lab = f'{who}: {done} of {total} decided' if who else f'{done} of {total} decided'
    cnt_cls = 'text-body-lg' if large else 'text-caption'
    count = (f'<span class="inline-flex shrink-0 items-center gap-1 {cnt_cls} text-foreground">{icon("circle-check", "size-4")}Finished</span>' if fin else '')
    bar = f'<div class="h-1.5 min-w-0 flex-1 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="{done}" aria-valuemin="0" aria-valuemax="{total}" aria-label="{lab}"><div class="h-full {pct} rounded-full bg-primary"></div></div>'
    if large:
        return f'<div class="mt-2">{bar}<p class="mt-1.5 flex flex-wrap items-center gap-x-3 {cnt_cls} tabular-nums text-muted-foreground">{done} / {total} decided {count}</p></div>'
    return f'<div class="mt-2 flex items-center gap-3">{bar}<span class="shrink-0 {cnt_cls} tabular-nums text-muted-foreground">{done} / {total} decided</span>{count}</div>'

# ---------------------------------------------------------------- controls
def switch(on, label, disabled=False, ios=False, extra='', href=None):
    dis = ' disabled' if disabled else ''
    op = ' opacity-50' if disabled else ''
    if ios:
        track = 'bg-primary' if on else 'bg-muted-foreground/30'
        knob_c = 'ml-auto bg-primary-foreground' if on else 'bg-card'
        inner = f'<span class="flex h-8 w-13 items-center rounded-full {track} p-0.5"><span class="size-7 rounded-full {knob_c} shadow-raised"></span></span>'
    elif on:
        inner = '<span class="flex h-8 w-13 items-center rounded-full bg-primary p-1"><span class="ml-auto size-6 rounded-full bg-primary-foreground"></span></span>'
    else:
        inner = '<span class="flex h-8 w-13 items-center rounded-full border-2 border-input bg-muted p-1"><span class="size-5 rounded-full bg-muted-foreground"></span></span>'
    attrs = f'role="switch" aria-checked="{"true" if on else "false"}" aria-label="{label}" class="-my-2 flex h-12 w-13 shrink-0 items-center{op}"{extra}'
    if href and not disabled:
        return f'<a href="{href}" {attrs}>{inner}</a>'
    return f'<button {attrs}{dis}>{inner}</button>'

def radio_dot(on, disabled=False):
    op = ' opacity-50' if disabled else ''
    if on:
        return f'<span class="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary{op}" aria-hidden="true"><span class="size-3 rounded-full bg-primary"></span></span>'
    return f'<span class="mt-0.5 size-6 shrink-0 rounded-full border-2 border-input{op}" aria-hidden="true"></span>'

def radio_row(on, title, desc, ic=None, disabled=False, href=None, action=None, large=False):
    dis = ' disabled' if disabled else ''
    t_cls = 'text-title-3 font-normal' if large else 'text-body'
    d_cls = 'text-body-lg' if large else 'text-body-sm'
    lead = icon(ic, 'size-5 shrink-0 text-muted-foreground mt-0.5') if ic else ''
    inner = f'''{radio_dot(on, disabled)}<span class="min-w-0 flex-1"><span class="flex items-center gap-2 {t_cls}">{title}</span><span class="mt-0.5 block {d_cls} text-muted-foreground">{desc}</span></span>{lead}'''
    act = f' data-action="{action}"' if action else ''
    if href and not disabled:
        return f'<a href="{href}" role="radio" aria-checked="{"true" if on else "false"}" class="flex min-h-14 items-start gap-4 px-4 py-3 text-left"{act}>{inner}</a>'
    return f'<button role="radio" aria-checked="{"true" if on else "false"}" class="flex min-h-14 w-full items-start gap-4 px-4 py-3 text-left"{dis}{act}>{inner}</button>'

def btn(text, kind='primary', href=None, action=None, ic=None, size='h-14', full=True, disabled=False, busy=False, extra='', label=None):
    cls = {
        'primary': 'bg-primary text-primary-foreground',
        'secondary': 'bg-secondary text-secondary-foreground',
        'outline': 'border border-input bg-card',
        'ghost': '',
        'destructive': 'bg-destructive text-destructive-foreground',
        'link': 'text-primary',
    }[kind]
    w = 'w-full' if full else ''
    px = 'px-5' if kind != 'link' else 'px-1'
    ico = icon('loader-circle', 'size-5 animate-spin') if busy else (icon(ic) if ic else '')
    op = ' opacity-50' if disabled else ''
    act = f' data-action="{action}"' if action else ''
    bz = ' aria-busy="true"' if busy else ''
    al = f' aria-label="{label}"' if label else ''
    c = f'flex {size} {w} items-center justify-center gap-2 rounded-control {px} text-label-lg {cls}{op} {extra}'.strip()
    if href and not disabled:
        return f'<a href="{href}" class="{c}"{act}{al}>{ico}{text}</a>'
    return f'<button class="{c}"{act}{bz}{al}{" disabled" if disabled else ""}>{ico}{text}</button>'

def snack_static(text, action=None, icon_name=None):
    """Snackbar rendered in a reserved slot (content above it is cut cleanly, QA-096)."""
    return snackbar(text, action, icon_name=icon_name).replace('absolute inset-x-4 bottom-6 z-40 ', '')

def snackbar(text, action=None, bottom='bottom-6', role='status', icon_name=None, href=None):
    if action:
        a = f'<a href="{href}" class="-my-1 inline-flex h-12 items-center rounded-sm px-3 text-label text-primary-inverse">{action}</a>' if href else f'<button class="-my-1 inline-flex h-12 items-center rounded-sm px-3 text-label text-primary-inverse">{action}</button>'
    else:
        a = ''
    ic = icon(icon_name, 'size-5 shrink-0') if icon_name else ''
    pad = 'py-1.5 pl-4 pr-1.5' if action else 'px-4 py-3'
    return f'<div class="absolute inset-x-4 {bottom} z-40 flex min-h-12 items-center gap-3 rounded-control bg-foreground {pad} text-background shadow-overlay" role="{role}">{ic}<span class="flex-1 text-body-sm">{text}</span>{a}</div>'

def offline_banner(text="You're offline. Decisions are saved on this phone."):
    return f'<div class="flex shrink-0 items-center gap-2 bg-muted px-gutter py-2 text-body-sm" role="status">{icon("wifi-off", "size-4 shrink-0")}<span class="flex-1">{text}</span></div>'

def section_label(text, hid=None, extra=''):
    i = f' id="{hid}"' if hid else ''
    return f'<h2{i} class="px-1 pb-2 text-label text-muted-foreground {extra}">{text}</h2>'.replace(' "', '"')

def group(rows, extra=''):
    return f'<ul class="divide-y overflow-hidden rounded-group bg-card dark:border {extra}">{rows}</ul>'.replace(' "', '"')

def nav_row(ic, title, desc=None, href='#', value=None, destructive=False, primary=False, action=None, chevron=True, large=False, disabled=False):
    t_cls = 'text-title-3 font-normal' if large else 'text-body'
    d_cls = 'text-body-lg' if large else 'text-body-sm'
    color = ' text-destructive' if destructive else (' text-primary' if primary else '')
    ic_cls = 'size-5 shrink-0' + ('' if (destructive or primary) else ' text-muted-foreground')
    d = f'<span class="mt-0.5 block {d_cls} text-muted-foreground">{desc}</span>' if desc else ''
    v = f'<span class="shrink-0 {d_cls} text-muted-foreground">{value}</span>' if value else ''
    ch = icon('chevron-right', 'size-5 shrink-0 text-muted-foreground') if chevron and not destructive and not primary else ''
    act = f' data-action="{action}"' if action else ''
    inner = f'{icon(ic, ic_cls)}<span class="min-w-0 flex-1"><span class="block {t_cls}">{title}</span>{d}</span>{v}{ch}'
    if disabled:
        return f'<li><button class="flex min-h-14 w-full items-center gap-4 px-4 py-3 text-left{color} opacity-50" disabled>{inner}</button></li>'
    return f'<li><a href="{href}" class="flex min-h-14 items-center gap-4 px-4 py-3{color}"{act}>{inner}</a></li>'

def dialog(title, body, actions, extra_body='', z='z-50'):
    t, d = uid('dt'), uid('dd')
    return f'''<div class="absolute inset-0 {z} bg-scrim/50"></div>
  <div class="absolute inset-0 {z} flex items-center justify-center px-6">
    <div class="w-full rounded-dialog bg-popover p-6 shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="{t}" aria-describedby="{d}">
      <h2 id="{t}" class="text-title-3">{title}</h2>
      <div id="{d}" class="mt-2 space-y-2 text-body text-muted-foreground">{"".join(f"<p>{x}</p>" for x in body.split(chr(10)))}</div>
      {extra_body}
      <div class="mt-6 flex flex-wrap justify-end gap-2">{actions}</div>
    </div>
  </div>'''

def dbtn(text, kind='ghost', href=None, action=None):
    cls = {'ghost': '', 'destructive': 'bg-destructive text-destructive-foreground', 'primary': 'bg-primary text-primary-foreground'}[kind]
    act = f' data-action="{action}"' if action else ''
    if href:
        return f'<a href="{href}" class="inline-flex h-12 items-center rounded-control px-4 text-label-lg {cls}"{act}>{text}</a>'.replace(' "', '"')
    return f'<button class="inline-flex h-12 items-center rounded-control px-4 text-label-lg {cls}"{act}>{text}</button>'.replace(' "', '"')

def handle():
    return '<div class="flex shrink-0 justify-center py-1.5"><span class="h-1 w-8 rounded-full bg-muted-foreground/40"></span></div>'

def bottom_sheet(title, content, z='z-40', tid=None, close=True, sub=None):
    t = tid or uid('sh')
    cl = f'<button class="-mr-3 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</button>' if close else ''
    s = f'<p class="text-body-sm text-muted-foreground">{sub}</p>' if sub else ''
    return f'''<div class="absolute inset-0 {z} bg-scrim/50"></div>
  <div class="absolute inset-x-0 bottom-0 {z} rounded-t-sheet bg-popover px-gutter pb-5 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="{t}">
    {handle()}
    <div class="flex items-start justify-between gap-3 pt-2"><div class="min-w-0"><h2 id="{t}" class="text-title-3">{title}</h2>{s}</div>{cl}</div>
    {content}
  </div>'''

# ---------------------------------------------------------------- frames
def phone(content, ios=False):
    cls = 'phone-ios' if ios else 'phone'
    return f'''<div class="{cls}">
  <div class="sysbar-top" aria-hidden="true"><span>9:41</span><span class="sysbar-icons"></span></div>
  <div class="screen">
  {content}
  </div>
  <div class="sysbar-nav" aria-hidden="true"></div>
</div>'''

def web_phone(content):
    return f'''<div class="phone">
  <div class="screen">
  {content}
  </div>
</div>'''

def desktop(url, content):
    return f'''<div class="desktop">
  <div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">{url}</span></div>
  <div class="desktop-column">
  {content}
  </div>
</div>'''

def scale_large(html):
    """At 200% font scale small text grows too (QA-100): caption, label and body-sm become body-lg."""
    html = re.sub(r'\btext-(caption|body-sm)\b', 'text-body-lg', html)
    return re.sub(r'\btext-label\b(?!-)', 'text-body-lg', html)

class Page:
    def __init__(self, sid, title, desc):
        self.sid, self.title, self.desc = sid, title, desc
        self.parts = []
    def section(self, title, desc):
        self.parts.append(f'</main>\n<h2 class="mock-section">{title}</h2>\n<p>{desc}</p>\n<main class="mock-canvas">')
    def frame(self, fid, label, inner):
        self.parts.append(f'''
<figure class="frame" data-frame="{fid}" id="{fid}">
  <figcaption class="frame-label">{self.sid} · {label} · <span class="theme-name"></span></figcaption>
  {inner}
</figure>''')
    def write(self, filename):
        html = f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{self.sid} {self.title}</title>
<link rel="stylesheet" href="../assets/css/app.css">
</head>
<body class="mock-page">
<header class="mock-doc">
  <h1>{self.sid} {self.title}</h1>
  <p>{self.desc}</p>
</header>
<main class="mock-canvas">
{''.join(self.parts)}
</main>
</body>
</html>
'''
        html = html.replace('<main class="mock-canvas">\n</main>\n', '', 1)
        with open(os.path.join(SCREENS, filename), 'w') as f:
            f.write(html)
        print(filename, 'frames:', html.count('data-frame='))

# ---------------------------------------------------------------- shared chrome
def appbar(title, lead='back', lead_href='#', sub=None, actions='', lead_label=None, large=False):
    ic = {'back': 'arrow-left', 'close': 'x'}[lead]
    ll = lead_label or {'back': 'Back', 'close': 'Close'}[lead]
    t_cls = 'text-title-2' if large else 'text-title-3'
    s = f'<p class="text-caption text-muted-foreground">{sub}</p>' if sub else ''
    return f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="{lead_href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{ll}">{icon(ic, "size-6")}</a>
    <div class="min-w-0 flex-1 px-1"><h1 class="truncate {t_cls}">{title}</h1>{s}</div>
    {actions}
  </header>'''

def icon_action(ic, label, href='#', action=None, disabled=False):
    act = f' data-action="{action}"' if action else ''
    if disabled:
        return f'<button class="flex size-12 shrink-0 items-center justify-center rounded-full opacity-50" aria-label="{label}" disabled>{icon(ic, "size-6")}</button>'
    return f'<a href="{href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{label}"{act}>{icon(ic, "size-6")}</a>'

def ios_bar(back=None, title='', right='', back_href='#'):
    b = f'<a href="{back_href}" class="inline-flex h-12 items-center gap-0.5 justify-self-start text-body text-primary" aria-label="Back to {back}">{icon("chevron-left", "size-6")}{back}</a>' if back else '<span></span>'
    return f'''<header class="grid h-11 shrink-0 grid-cols-[1fr_auto_1fr] items-center px-2">
    {b}
    <h1 class="text-body font-semibold">{title}</h1>
    <div class="flex justify-end">{right}</div>
  </header>'''

def logo(size='size-8'):
    return (f'<img src="{BRAND}logo-mark.svg" alt="" class="{size} dark:hidden">'
            f'<img src="{BRAND}logo-mark-dark.svg" alt="" class="hidden {size} dark:block">')

def web_brand(right=''):
    return f'''<header class="flex h-16 shrink-0 items-center gap-2 px-gutter">
    {logo()}<span class="text-title-3">SwipeSort</span>
    <div class="ml-auto flex items-center">{right}</div>
  </header>'''

def account_chip(k):
    return f'<button class="flex h-12 items-center gap-2 rounded-full pl-1 pr-3 text-label" aria-label="Account: {P[k]["name"]}">{av(k, "size-8")}<span>{P[k]["first"]}</span></button>'

# =====================================================================================
# S31 INVITE
# =====================================================================================
def link_field(token, state='ok', large=False):
    fid = uid('lnk')
    t_cls = 'text-title-3 font-normal' if large else 'text-body'
    if state == 'loading':
        return f'''<div aria-busy="true">{section_label("Invite link")}
      <div class="flex h-12 items-center gap-3 rounded-control border border-input bg-card px-3.5">{icon("link-2", "size-5 text-muted-foreground")}<span class="block h-3.5 w-48 animate-pulse rounded-full bg-muted"></span></div>
      <p class="mt-2 flex items-center gap-2 text-body-sm text-muted-foreground" role="status">{icon("loader-circle", "size-4 animate-spin text-primary")}Creating link…</p></div>'''
    if state == 'expired':
        return f'''<div>{section_label("Invite link")}
      <div class="flex h-12 items-center gap-3 rounded-control border border-dashed border-input bg-muted px-3.5">{icon("link-2-off", "size-5 text-muted-foreground")}<span class="min-w-0 flex-1 truncate text-body text-muted-foreground line-through">swipesort.app/join/{token}</span></div>
      <p class="mt-2 text-body-sm text-foreground">This link expired on Oct 8. Create a new one to invite more people.</p>
      {btn("Create new link", "secondary", ic="refresh-cw", size="h-12", extra="mt-3")}</div>'''
    wrap = 'break-all' if large else 'truncate'
    h = 'min-h-12 py-2' if large else 'h-12'
    return f'''<div><label for="{fid}" class="block px-1 pb-2 text-label text-muted-foreground">Invite link</label>
      <div class="flex {h} items-center gap-3 rounded-control border border-input bg-card px-3.5">{icon("link-2", "size-5 shrink-0 text-muted-foreground")}<input id="{fid}" readonly value="swipesort.app/join/{token}" class="min-w-0 flex-1 bg-transparent {t_cls} {wrap}"></div></div>'''

def link_meta(role='collab', expires='Oct 24, in 14 days', reset=True, reset_href='#S31-reset-confirm', large=False, who_resets=None):
    d_cls = 'text-body-lg' if large else 'text-body-sm'
    if role == 'dm':
        who = 'The first person to join with this link becomes the Decision Maker. After that, the link invites as Collaborator.'
    else:
        who = 'Anyone with the link can join as Collaborator.'
    rs = f'<a href="{reset_href}" class="-mr-2 inline-flex h-12 shrink-0 items-center rounded-control px-2 text-label text-primary" data-action="reset-link">Reset link</a>' if reset else ''
    return f'''<p class="mt-2 px-1 {d_cls}">{who}</p>
      <div class="flex items-center justify-between gap-3 px-1"><p class="flex items-center gap-1.5 {d_cls} text-muted-foreground">{icon("clock", "size-4 shrink-0")}Expires {expires}</p>{rs}</div>'''

def role_choice(sel='collab', disabled=False, large=False, dm_note="There's one Decision Maker, so the role moves from you to them."):
    rid = uid('role')
    return f'''<div>{section_label("Invite as", rid)}
      <div class="divide-y overflow-hidden rounded-group bg-card dark:border" role="radiogroup" aria-labelledby="{rid}">
        {radio_row(sel == 'collab', 'Collaborator', 'Sorts every item and adds notes. Can invite others as Collaborator.', None, disabled, href='#S31-default' if sel != 'collab' and not disabled else None, large=large)}
        {radio_row(sel == 'dm', 'Decision Maker', f'Also resolves conflicts. {dm_note}', None, disabled, href='#S31-role-dm' if sel != 'dm' and not disabled else None, action='role-dm' if sel != 'dm' else None, large=large)}
      </div></div>'''

def member_mini(k, roles, you=False):
    y = ' <span class="text-muted-foreground">(you)</span>' if you else ''
    return f'<li class="flex min-h-14 items-center gap-3 px-4 py-2.5">{av(k, "size-8")}<span class="min-w-0 flex-1"><span class="block truncate text-body">{P[k]["name"]}{y}</span><span class="block text-body-sm text-muted-foreground">{role_words(roles)}</span></span></li>'

def members_so_far(rows, note=None, count=None):
    n = f'<p class="mt-2 px-1 text-body-sm text-muted-foreground">{note}</p>' if note else ''
    return f'<div>{section_label(f"Members ({count})")}{group(rows)}{n}</div>'

FIRST_MEMBERS = members_so_far(member_mini('deniz', ['owner', 'dm'], True), "Nobody else has joined yet. People show up here as soon as they join.", 1)
ALL_MEMBERS = members_so_far(member_mini('deniz', ['owner'], True) + member_mini('mert', ['dm']) + member_mini('selin', []), None, 3)

def sheet_footer(copy_href=None, copy_action=None, share=True, disabled=False, share_icon='share-2', copy_label='Copy link', snack=''):
    sh = btn('Share…', 'secondary', ic=share_icon, size='h-12', disabled=disabled, action='share' if not disabled else None) if share else ''
    slot = f'<div class="shrink-0 px-4 pb-3 pt-2">{snack}</div>' if snack else ''
    return f'''{slot}<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3">
      {btn(copy_label, 'primary', href=copy_href, action=copy_action, ic='copy', disabled=disabled)}
      {sh}
    </div>'''

def full_sheet(title, body, footer='', top='top-4', ios=False, overlay='', intro=None, large=False):
    t = uid('fs')
    i = f'<p class="px-gutter pb-4 {"text-body-lg" if large else "text-body-sm"} text-muted-foreground">{intro}</p>' if intro else ''
    if ios:
        head = f'''<div class="flex shrink-0 justify-center pt-1.5"><span class="h-1 w-9 rounded-full bg-muted-foreground/40"></span></div>
    <div class="grid shrink-0 grid-cols-[1fr_auto_1fr] items-center px-3"><span></span><h2 id="{t}" class="text-body font-semibold">Invite</h2><a href="S34-members.html#S34-ios" class="inline-flex h-12 items-center justify-self-end px-1 text-body font-semibold text-primary">Done</a></div>
    <p class="px-gutter pb-1 pt-2 text-title-2">{title}</p>'''
    else:
        tt = 'text-title-1' if large else 'text-title-2'
        head = f'''{handle()}
    <div class="flex shrink-0 items-start justify-between gap-3 px-gutter pb-2 pt-1"><h2 id="{t}" class="pt-2 {tt}">{title}</h2><a href="S34-members.html#S34-default" class="-mr-3 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</a></div>'''
    under = '' if ios else '<div class="flex h-16 shrink-0 items-center gap-1 px-1 opacity-60" aria-hidden="true"><span class="flex size-12 items-center justify-center">' + icon('arrow-left', 'size-6') + '</span><span class="text-title-3">Wedding guests</span></div>'
    if ios:
        under = '<div class="mx-4 mt-2 h-8 rounded-t-sheet bg-card opacity-60" aria-hidden="true"></div>'
    scrim = 'bg-scrim/40' if ios else 'bg-scrim/50'
    return f'''{under}
  <!-- Proposed component: FullHeightSheet (BottomSheet at full height, background surface, sticky footer) -->
  <div class="absolute inset-0 z-10 {scrim}"></div>
  <div class="absolute inset-x-0 bottom-0 {top} z-20 flex flex-col rounded-t-sheet bg-background shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="{t}">
    {head}
    {i}
    <div class="min-h-0 flex-1 space-y-6 overflow-hidden px-gutter pb-4">{body}</div>
    {footer}
  </div>
  {overlay}'''

INTRO = 'People you invite sort the same 100 items on their own. The list then shows where you agree.'

def s31_body(role='collab', state='ok', token=TOKEN, members=FIRST_MEMBERS, choice=True, reset=True, extra_top='', large=False, choice_disabled=False, dm_note=None):
    parts = [extra_top]
    if choice:
        parts.append(role_choice(role, choice_disabled, large, **({'dm_note': dm_note} if dm_note else {})))
    if state in ('ok',):
        parts.append(f'<div>{link_field(token, large=large)}{link_meta(role, reset=reset, large=large)}</div>')
    elif state == 'loading':
        parts.append(link_field(token, 'loading'))
    elif state == 'expired':
        parts.append(link_field(token, 'expired'))
    elif state == 'offline':
        parts.append(f'''<div class="flex gap-3 rounded-control border bg-card p-4" role="alert">{icon("wifi-off", "size-5 shrink-0 text-muted-foreground")}<div class="flex-1"><p class="text-label">Invites need a connection</p><p class="mt-0.5 text-body-sm text-muted-foreground">Connect to the internet to create or copy the invite link. Your lists and decisions are safe on this phone.</p>{btn("Try again", "secondary", size="h-12", extra="mt-3", ic="refresh-cw")}</div></div>''')
    elif state == 'error':
        parts.append(f'''<div class="flex gap-3 rounded-control border border-destructive/40 bg-card p-4" role="alert">{icon("circle-alert", "size-5 shrink-0 text-destructive")}<div class="flex-1"><p class="text-label">Couldn't create the invite link</p><p class="mt-0.5 text-body-sm text-muted-foreground">SwipeSort didn't respond. Check your connection and try again.</p>{btn("Try again", "secondary", size="h-12", extra="mt-3", ic="refresh-cw")}</div></div>''')
    parts.append(members)
    return ''.join(parts)

def build_s31():
    pg = Page('S31', 'Invite', 'Sender side of sharing a list: choose the role, then copy or share the invite link. A full-height sheet over the list overview (S09) or the members screen (S34). Spec: <a href="S31-invite.md">S31-invite.md</a>. Prototype flow 3 starts at <code>S31-default</code>.')
    F = pg.frame

    pg.section('Inviting (Owner)', 'First invite for Wedding guests: nobody has joined yet, Deniz is Owner and, by default, Decision Maker (A-26). Collaborator is preselected; the link always reflects the selected role.')
    F('S31-default', 'Default: first invite, Collaborator', phone(full_sheet('Invite to Wedding guests', s31_body(), sheet_footer('#S31-link-copied', 'copy-link'), intro=INTRO)))
    proto = '<!-- Prototype-only control (not part of the app UI): jumps to the partner side of flow 3 -->\n  <a href="S32-invite-link.html#S32-web-desktop" class="absolute inset-x-4 top-2 z-50 flex min-h-12 items-center justify-center gap-2 rounded-control border-2 border-dashed border-primary bg-card px-4 text-label text-primary" data-action="partner-opens-link">' + icon('monitor', 'size-5') + 'Prototype: Mert opens the link on a computer</a>'
    F('S31-link-copied', 'Link copied (snackbar)', phone(full_sheet('Invite to Wedding guests', s31_body(members=members_so_far(member_mini('deniz', ['owner', 'dm'], True), None, 1)), sheet_footer(snack=snack_static('Invite link copied', icon_name='copy-check')), top='top-16', intro=None,
        overlay=proto)))
    dm_body = s31_body('dm', token='Dm6xW3nB')
    F('S31-role-dm', 'Inviting a Decision Maker', phone(full_sheet('Invite to Wedding guests', dm_body, sheet_footer(), intro=INTRO)))

    pg.section('Pending invites', 'Invites are links, so SwipeSort does not list people who opened a link but did not join (they are anonymous until they join). "Pending invites" are the active links: each member has their own link, so the join page can say who invited you. The Owner sees every active link and can turn off anyone\'s.')
    links = f'''<div>{section_label("Active invite links (2)")}
      {group(f"""<li class="flex min-h-16 items-center gap-3 px-4 py-3">{av("deniz", "size-8")}<span class="min-w-0 flex-1"><span class="block text-body">Your link</span><span class="block text-body-sm text-muted-foreground">Collaborator, expires Oct 24. 2 people joined.</span></span></li>
        <li class="flex min-h-16 items-center gap-3 py-3 pl-4 pr-2">{av("selin", "size-8")}<span class="min-w-0 flex-1"><span class="block text-body">Selin's link</span><span class="block text-body-sm text-muted-foreground">Collaborator, expires Oct 21. Nobody joined yet.</span></span><button class="inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label text-primary" aria-label="Turn off Selin's link">Turn off</button></li>""")}
      <p class="mt-2 px-1 text-body-sm text-muted-foreground">A link stops working when it expires, is reset or is turned off. Members who joined stay.</p></div>'''
    F('S31-pending', 'Active links and members (opened from S34)', phone(full_sheet('Invite to Wedding guests', s31_body(members=links + ALL_MEMBERS, dm_note="There's one Decision Maker, so the role moves from Mert to them."), sheet_footer(), intro=None)))

    pg.section('Reset link', 'Resetting revokes the current link (anyone holding it can no longer join) and creates a new one. Members who already joined are not affected. The same dialog pattern is listed in S40.')
    reset_dialog = dialog('Reset the invite link?', "The current link stops working right away. Members who already joined stay. Share the new link with anyone who hasn't joined yet.",
        dbtn('Cancel', href='#S31-default') + dbtn('Reset link', 'destructive', href='#S31-reset-done', action='confirm-reset'))
    F('S31-reset-confirm', 'Reset link: confirmation', phone(full_sheet('Invite to Wedding guests', s31_body(), sheet_footer(), intro=INTRO, overlay=reset_dialog)))
    reset_body = s31_body(token=TOKEN_NEW)
    F('S31-reset-done', 'Link reset: new link, snackbar', phone(full_sheet('Invite to Wedding guests', reset_body, sheet_footer(snack=snack_static('Invite link reset', icon_name='refresh-cw')), intro=INTRO)))

    pg.section('States', 'Creating the link, offline, errors, an expired link and a signed-out session.')
    F('S31-loading', 'Creating the link', phone(full_sheet('Invite to Wedding guests', s31_body(state='loading'), sheet_footer(disabled=True), intro=INTRO)))
    F('S31-offline', 'Offline: invites need a connection', phone(full_sheet('Invite to Wedding guests', s31_body(state='offline', choice_disabled=True), sheet_footer(disabled=True), intro=INTRO)))
    F('S31-error', 'Error: link could not be created', phone(full_sheet('Invite to Wedding guests', s31_body(state='error'), sheet_footer(disabled=True), intro=INTRO)))
    F('S31-expired', 'Link expired (14 days)', phone(full_sheet('Invite to Wedding guests', s31_body(state='expired'), sheet_footer(disabled=True), intro=INTRO)))
    signed_out = f'''<div class="flex h-full flex-col items-center justify-center px-4 pb-16 text-center">
        <span class="flex size-14 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon("log-in", "size-6")}</span>
        <h3 class="mt-4 text-balance text-title-2">Sign in to invite people</h3>
        <p class="mt-2 max-w-xs text-balance text-body text-muted-foreground">Sharing needs an account, so everyone sorts the same list. Your lists stay on this phone and move to your account when you sign in.</p>
        {btn("Sign in", "primary", href="S05-sign-in-prompt.html#S05-share", action="sign-in", extra="mt-6 max-w-xs")}
      </div>'''
    F('S31-signed-out', 'Not signed in: routes to the sign-in prompt (S05)', phone(full_sheet('Invite to Wedding guests', signed_out, '', intro=None)))

    pg.section('Roles', 'Collaborators can invite, but only as Collaborator. The Decision Maker choice is Owner-only.')
    collab_note = f'<div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground" role="note">{icon("info", "size-5 shrink-0")}<p class="text-body-sm">You can invite people as Collaborator. Only Deniz, the Owner, can invite a Decision Maker.</p></div>'
    collab_members = members_so_far(member_mini('deniz', ['owner'], False) + member_mini('mert', ['dm']) + member_mini('selin', [], True), None, 3)
    collab_body = collab_note + f'<div>{link_field(TOKEN_SELIN)}{link_meta("collab", "Oct 21, in 11 days", reset=True)}</div>' + collab_members
    F('S31-collaborator', 'Collaborator inviting (Selin)', phone(full_sheet('Invite to Wedding guests', collab_body, sheet_footer(), intro=None)))

    pg.section('Accessibility', 'Large text: descriptions wrap, the link wraps instead of truncating, actions stay pinned at the bottom.')
    lt_body = s31_body(large=True)
    lt_footer = f'''<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3">
      <button class="flex min-h-14 w-full items-center justify-center gap-2 rounded-control bg-primary px-5 py-2 text-title-3 text-primary-foreground">{icon("copy", "size-6")}Copy link</button>
      <button class="flex min-h-14 w-full items-center justify-center gap-2 rounded-control bg-secondary px-5 py-2 text-title-3 text-secondary-foreground">{icon("share-2", "size-6")}Share…</button>
    </div>'''
    F('S31-large-text', 'Large text (200%)', phone(scale_large(full_sheet('Invite to Wedding guests', lt_body, lt_footer, large=True, intro=None))))

    pg.section('iOS and web', 'iOS: a page sheet with grabber and Done, roles as a checkmark list, the iOS share icon. Web: Copy link always; Share… only where the browser supports the Web Share API (mobile browsers); desktop shows Copy link only.')
    def ios_role_row(on, title, desc, href=None):
        chk = icon('check', 'size-5 shrink-0 text-primary') if on else '<span class="size-5 shrink-0"></span>'
        inner = f'<span class="min-w-0 flex-1"><span class="block text-body">{title}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span>{chk}'
        if href:
            return f'<a href="{href}" role="radio" aria-checked="{"true" if on else "false"}" class="flex min-h-14 items-center gap-3 px-4 py-2.5">{inner}</a>'
        return f'<button role="radio" aria-checked="{"true" if on else "false"}" class="flex min-h-14 w-full items-center gap-3 px-4 py-2.5 text-left">{inner}</button>'
    rid = uid('role')
    ios_body = f'''<p class="text-body-sm text-muted-foreground">{INTRO}</p>
      <div>{section_label("Invite as", rid)}<div class="divide-y overflow-hidden rounded-group bg-card dark:border" role="radiogroup" aria-labelledby="{rid}">
        {ios_role_row(True, "Collaborator", "Sorts every item and adds notes.")}
        {ios_role_row(False, "Decision Maker", "Also resolves conflicts. The role moves from you to them.", "#S31-role-dm")}
      </div></div>
      <div>{link_field(TOKEN)}{link_meta("collab")}</div>
      {FIRST_MEMBERS}'''
    F('S31-ios', 'iOS page sheet', phone(full_sheet('Invite to Wedding guests', ios_body, sheet_footer(share_icon='share'), top='top-3', ios=True), ios=True))
    F('S31-web', 'Web, mobile browser (Web Share available)', web_phone(full_sheet('Invite to Wedding guests', s31_body(), sheet_footer(), intro=INTRO)))
    web_desk_footer = f'''<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3">
      {btn("Copy link", "primary", ic="copy")}
      <p class="px-1 text-body-sm text-muted-foreground">Paste the link into an email or a chat to invite people.</p>
    </div>'''
    F('S31-web-desktop', 'Web, desktop browser (copy link only)', desktop('swipesort.app/l/7Hq2xK/members', full_sheet('Invite to Wedding guests', s31_body(), web_desk_footer, intro=INTRO)))
    pg.write('S31-invite.html')

# =====================================================================================
# S32 OPENING AN INVITE LINK
# =====================================================================================
def role_card(role='collab', changed=False, large=False):
    t_cls = 'text-title-3' if large else 'text-label-lg'
    d_cls = 'text-body-lg' if large else 'text-body-sm'
    if role == 'dm':
        ic, title, desc = 'gavel', "You'll join as Decision Maker", "You sort every item and resolve conflicts. Under the current rule, your choice on a conflict is final."
    else:
        ic, title, desc = 'user-round', "You'll join as Collaborator", "You sort every item on your own. Your decisions count toward each item's final decision."
    ch = ''
    if changed:
        ch = f'<div class="mt-3 flex gap-2 rounded-control bg-primary-soft p-3 text-primary-soft-foreground" role="note">{icon("info", "size-5 shrink-0")}<p class="{d_cls}">This invite was for the Decision Maker role. Mert Aydın joined in that role first, so you\'ll join as Collaborator.</p></div>'
    return f'''<div class="rounded-group bg-card p-4 dark:border">
      <div class="flex items-start gap-3"><span class="flex size-10 shrink-0 items-center justify-center rounded-full bg-secondary text-secondary-foreground">{icon(ic)}</span><div class="min-w-0 flex-1"><p class="{t_cls}">{title}</p><p class="mt-0.5 {d_cls} text-muted-foreground">{desc}</p></div></div>
      {ch}
    </div>'''

def invite_hero(inviter='deniz', large=False):
    p = P[inviter]
    return f'''<div class="flex items-center gap-3">{av(inviter, "size-14")}<p class="{"text-title-3 font-normal" if large else "text-body-lg"}">{p["name"]} invited you to sort a list together</p></div>
      <h1 class="mt-5 {"text-display" if large else "text-title-1"}">Wedding guests</h1>
      <p class="mt-1 {"text-title-3 font-normal" if large else "text-body"} text-muted-foreground">100 items, Round 1</p>'''

def invite_members(keys_roles):
    rows = ''.join(f'<li class="flex min-h-14 items-center gap-3 px-4 py-2.5">{av(k, "size-8")}<span class="min-w-0 flex-1"><span class="block truncate text-body">{P[k]["name"]}</span><span class="block text-body-sm text-muted-foreground">{role_words(r)}</span></span></li>' for k, r in keys_roles)
    return f'<div>{section_label(f"Members ({len(keys_roles)})")}{group(rows)}</div>'

def s32_preview(cta, members, role='collab', changed=False, banner='', get_app=True, brand=None, large=False, note='No download needed. Sort right here in your browser.', hdr=''):
    brand = (not banner) if brand is None else brand
    ga = f'''<div class="mt-6 flex items-center justify-between gap-3 border-t pt-4"><p class="text-body-sm text-muted-foreground">Prefer the app? It works the same, with haptics and push notifications.</p>{btn("Get the app", "outline", href="#S32-get-app", size="h-12", full=False, extra="shrink-0", action="get-app")}</div>''' if get_app else ''
    return f'''{hdr}{banner}{web_brand() if brand else ''}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 {'pt-2' if (brand or hdr) else 'pt-6'}">
    {invite_hero(large=large)}
    <div class="mt-6 space-y-6">{role_card(role, changed, large)}{invite_members(members)}</div>
    <div class="mt-6">{cta}
    <p class="mt-3 text-balance text-center text-body-sm text-muted-foreground">{note}</p></div>
    {ga}
  </div>'''

def smart_banner():
    return f'''<!-- Proposed component: AppBanner (web only: get the app) -->
  <div class="flex shrink-0 items-center gap-2 border-b bg-card py-1 pl-1 pr-3" role="region" aria-label="Get the app">
    <button class="flex size-12 shrink-0 items-center justify-center rounded-full text-muted-foreground" aria-label="Close banner">{icon("x", "size-4")}</button>
    <img src="{BRAND}app-icon.svg" alt="" class="size-10 shrink-0 rounded-control">
    <div class="min-w-0 flex-1"><p class="text-label">SwipeSort</p><p class="truncate text-caption text-muted-foreground">Sort with swipes in the app</p></div>
    {btn("Get the app", "outline", href="#S32-get-app", size="h-12", full=False, extra="shrink-0 px-3 text-label")}
  </div>'''

def status_page(ic, title, body, actions='', brand=True, tone='muted'):
    tone_cls = {'muted': 'bg-muted text-muted-foreground', 'primary': 'bg-primary-soft text-primary-soft-foreground'}[tone]
    return f'''{web_brand() if brand else ''}
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center px-8 pb-16 text-center">
    <span class="flex size-14 items-center justify-center rounded-full {tone_cls}">{icon(ic, "size-6")}</span>
    <h1 class="mt-4 text-balance text-title-2">{keep(title)}</h1>
    <p class="mt-2 max-w-xs text-balance text-body text-muted-foreground">{keep(body)}</p>
    {actions}
  </div>'''

def build_s32():
    pg = Page('S32', 'Opening an invite link', 'What the invited person sees when they open <code>swipesort.app/join/&lt;token&gt;</code>: in the app when installed (Android App Link, iOS Universal Link), otherwise in the web app, where they can sign in, join and sort without installing anything. Spec: <a href="S32-invite-link.md">S32-invite-link.md</a>.')
    F = pg.frame
    m1 = [('deniz', ['owner', 'dm'])]
    pg.section('Web app (app not installed)', 'Prototype flow 3: Mert opens the link Deniz copied, on his laptop. The page is public (no sign-in needed to see it) but shows only what the invited person needs: who invited them, the list, their role and the members.')
    cta_desk = btn('Sign in to join', 'primary', href='S03-sign-in.html#S03-web-desktop', action='sign-in-to-join')
    F('S32-web-desktop', 'Web, desktop browser: invite preview', desktop(f'swipesort.app/join/{TOKEN}', s32_preview(cta_desk, m1)))
    cta_m = btn('Sign in to join', 'primary', href='S03-sign-in.html#S03-web-desktop')
    F('S32-web', 'Web, mobile browser with the app banner', web_phone(s32_preview(cta_m, m1, banner=smart_banner(), get_app=False)))
    # QR tile stays dark-on-light in both themes (cameras fail on inverted codes): card/foreground in light, foreground/background in dark.
    qr = f'<div class="mx-auto mt-5 flex size-44 items-center justify-center rounded-control border bg-card text-foreground dark:bg-foreground dark:text-background">{qr_svg("https://swipesort.app/get", "size-40", "QR code for swipesort.app/get")}</div>'
    get_app = dialog('Get SwipeSort on your phone', "Scan the code with your phone's camera, or search for SwipeSort in Google Play or the App Store. Your invite works in the app too.",
        dbtn('Close', href='#S32-web-desktop'), extra_body=qr + '<p class="mt-3 text-center text-body-sm text-muted-foreground">swipesort.app/get</p>')
    F('S32-get-app', 'Web, desktop: Get the app', desktop(f'swipesort.app/join/{TOKEN}', s32_preview(cta_m, m1) + get_app))
    signed_in = f'''{web_brand(account_chip("mert"))}
  <div class="relative flex min-h-0 flex-1 flex-col items-center justify-center px-8 pb-16 text-center" role="status">
    {icon("loader-circle", "size-8 animate-spin text-primary")}
    <p class="mt-4 text-balance text-title-3">Opening {keep("Wedding guests")}…</p>
    <p class="mt-1 text-body-sm text-muted-foreground">Signed in as {keep("Mert Aydın")}</p>
    <a href="S33-join-list.html#S33-web-desktop" class="absolute inset-0" data-action="continue" aria-label="Continue to the join screen (prototype: click anywhere; the app moves on by itself)"></a>
  </div>'''
    F('S32-web-signed-in', 'Web, already signed in: skips sign-in, opens Join', desktop(f'swipesort.app/join/{TOKEN}', signed_in))
    loading = f'''{web_brand()}
  <div class="min-h-0 flex-1 px-gutter pt-2" aria-busy="true" role="status" aria-label="Loading invite">
    <div class="flex items-center gap-3"><span class="size-14 animate-pulse rounded-full bg-muted"></span><div class="flex-1 space-y-2"><span class="block h-4 w-4/5 animate-pulse rounded-full bg-muted"></span><span class="block h-4 w-1/2 animate-pulse rounded-full bg-muted"></span></div></div>
    <span class="mt-6 block h-8 w-2/3 animate-pulse rounded-full bg-muted"></span>
    <span class="mt-2 block h-4 w-1/3 animate-pulse rounded-full bg-muted"></span>
    <div class="mt-6 h-24 animate-pulse rounded-group bg-muted"></div>
    <div class="mt-6 h-16 animate-pulse rounded-group bg-muted"></div>
    <div class="mt-6 h-14 animate-pulse rounded-control bg-muted"></div>
  </div>'''
    F('S32-loading', 'Web: loading the invite', web_phone(loading))

    pg.section('Default: app installed, not signed in', 'The link opens the app. Without an account (or as a guest) the app shows the same invite preview as the web page; "Sign in to join" opens S03 and returns to S33. Device lists move to the account on sign-in (S05 moving step).')
    m1d = [('deniz', ['owner', 'dm'])]
    cta_app = btn('Sign in to join', 'primary', href='S03-sign-in.html#S03-default', action='sign-in')
    F('S32-default', 'Default: app, not signed in (invite preview)', phone(s32_preview(cta_app, m1d, get_app=False, brand=False, hdr=appbar('Invite', 'close', 'S08-home.html#S08-default'),
        note='Lists on this phone move to your account when you sign in.')))
    pg.section('App installed', 'The link opens SwipeSort directly. A short loading state names the list, then the join screen (S33) replaces it. iOS behaves the same with a Universal Link (no separate frame).')
    app_open = f'''<div class="relative flex flex-1 flex-col items-center justify-center px-8 pb-16 text-center" role="status">
    {logo("size-16")}
    <div class="mt-8 flex items-center gap-3">{icon("loader-circle", "size-6 animate-spin text-primary")}<p class="text-balance text-title-3">Opening {keep("Wedding guests")}…</p></div>
    <p class="mt-2 text-body-sm text-muted-foreground">Invite from {keep("Deniz Yılmaz")}</p>
    <a href="S33-join-list.html#S33-default" class="absolute inset-0" data-action="continue" aria-label="Continue to the join screen (prototype: click anywhere; the app moves on by itself)"></a>
  </div>'''
    F('S32-app', 'App: opening the invite', phone(app_open))
    member_page = f'''{appbar("Invite", "close", "S08-home.html#S08-default")}
  <div class="flex flex-1 flex-col items-center justify-center px-8 pb-16 text-center">
    {avatar_stack(["deniz", "mert", "selin"], "size-12")}
    <h2 class="mt-5 text-balance text-title-2">You're already in {keep("Wedding guests")}</h2>
    <p class="mt-2 max-w-xs text-balance text-body text-muted-foreground">You joined on Sep 28. You're the Decision Maker.</p>
    {btn("Open list", "primary", href="S09-list-overview.html#S09-shared", extra="mt-6 max-w-xs", action="open-list")}
  </div>'''
    F('S32-already-member', 'Already a member', phone(member_page))
    offline = f'''{appbar("Invite", "close", "S08-home.html#S08-default")}
  {offline_banner("You're offline.")}
  <div class="flex flex-1 flex-col items-center justify-center px-8 pb-16 text-center">
    <span class="flex size-14 items-center justify-center rounded-full bg-muted text-muted-foreground">{icon("wifi-off", "size-6")}</span>
    <h2 class="mt-4 text-balance text-title-2">Connect to open this invite</h2>
    <p class="mt-2 max-w-xs text-balance text-body text-muted-foreground">Joining a list needs a connection. The link keeps working until it expires, so you can try again later.</p>
    {btn("Try again", "secondary", extra="mt-6 max-w-xs", ic="refresh-cw")}
  </div>'''
    F('S32-offline', 'App: offline', phone(offline))

    pg.section('Links that no longer work', 'Expired, reset and unknown links never show the list\'s contents. When the link can still be traced to its sender (expired or reset), the page names them so the person knows whom to ask.')
    go = btn('Open SwipeSort', 'secondary', href='S08-home.html#S08-default', extra='mt-6 max-w-xs')
    F('S32-expired', 'Link expired', web_phone(status_page('clock-alert', 'This invite link expired', 'Invite links work for 14 days. Ask Deniz Yılmaz to send you a new one.', go)))
    F('S32-reset', 'Link was reset', web_phone(status_page('link-2-off', 'This invite link was reset', 'Deniz Yılmaz made a new link, so this one stopped working. Ask Deniz for the new link.', go)))
    F('S32-invalid', 'Unknown or broken link', web_phone(status_page('search-x', "This invite link doesn't work", 'Check that you copied the whole link, or ask the person who sent it for a new one.', go)))
    F('S32-list-deleted', 'List was deleted', web_phone(status_page('list-x', 'This list was deleted', "Its Owner deleted it, so there's nothing to join.", go)))
    F('S32-list-archived', 'List is archived', web_phone(status_page('archive', 'This list is archived', "Its Owner archived it, so it can't take new members right now. Ask Deniz Yılmaz to restore it.", go)))

    pg.section('Role changed', 'A Decision Maker invite works for one person. If someone else took the role first (or the Owner changed it), the page says so before the person signs in.')
    m2 = [('deniz', ['owner']), ('mert', ['dm'])]
    F('S32-role-changed', 'Invite role changed to Collaborator', web_phone(s32_preview(cta_m, m2, changed=True, banner=smart_banner(), get_app=False)))
    pg.write('S32-invite-link.html')

# =====================================================================================
# S33 JOIN A LIST
# =====================================================================================
def join_facts(role='collab', large=False, no_round=False):
    # Proposed component: InfoRow list (icon + title + description, non-interactive ListGroup rows)
    t_cls = 'text-title-3 font-normal' if large else 'text-body'
    d_cls = 'text-body-lg' if large else 'text-body-sm'
    def row(ic, title, desc):
        return f'<li class="flex items-start gap-4 px-4 py-3">{icon(ic, "size-5 shrink-0 text-muted-foreground mt-0.5")}<span class="min-w-0 flex-1"><span class="block {t_cls}">{title}</span><span class="mt-0.5 block text-balance {d_cls} text-muted-foreground">{desc}</span></span></li>'
    if role == 'dm':
        r1 = row('gavel', 'Decision Maker', 'You sort every item and resolve conflicts. Under the current rule (Decision Maker decides), your choice on a conflict is final.')
    else:
        r1 = row('user-round', 'Collaborator', 'You sort every item and add notes. You can invite others as Collaborator.')
    r2 = row('list-checks', 'Every item of the next round', 'You\'ll sort every item when Deniz starts <span class="whitespace-nowrap">Round 2.</span>') if no_round else row('list-checks', 'All 100 items of Round 1', 'Everyone sorts every item of the round.')
    r3 = row('eye-off', "Others' decisions are hidden", 'While you sort, so nobody sways you.')
    return f'<div>{section_label("Your role")}{group(r1 + r2 + r3)}</div>'

def join_members(rows_spec, large=False):
    rows = ''
    for k, roles in rows_spec:
        p = P[k]
        rows += f'<li class="flex items-start gap-3 px-4 py-3">{av(k, "size-10")}{member_block(k, roles, large=large)}</li>'
    return f'<div>{section_label(f"Members ({len(rows_spec)})")}{group(rows)}</div>'

def join_hero(inviter='deniz', large=False):
    p = P[inviter]
    return f'''<div class="flex items-center gap-3">{av(inviter, "size-10")}<p class="{"text-title-3 font-normal" if large else "text-body-lg"}">{p["name"]} invited you</p></div>
    <h2 class="mt-3 {"text-display" if large else "text-title-1"}">Wedding guests</h2>
    <p class="mt-1 {"text-title-3 font-normal" if large else "text-body"} text-muted-foreground">100 items, Round 1 in progress</p>'''

def join_footer(joiner='selin', href=None, action=None, busy=False, disabled=False, note=None, web=False, get_app=False, large=False):
    p = P[joiner]
    text = 'Joining…' if busy else 'Join and start sorting'
    b = btn(text, 'primary', href=href, action=action, busy=busy, disabled=disabled or busy)
    if busy:
        b = b.replace(' opacity-50', '')
    n = f'<p class="flex items-center gap-2 text-body-sm text-foreground">{icon("wifi-off", "size-4 shrink-0 text-muted-foreground")}{note}</p>' if note else ''
    sw = f' <a href="S03-sign-in.html#S03-web-desktop" class="inline-flex min-h-12 items-center text-primary underline underline-offset-4">Switch account</a>' if web else ''
    ga = ''
    who = f'<p class="flex flex-wrap items-center justify-center gap-x-1 text-center {"text-body-lg" if large else "text-body-sm"} text-muted-foreground">Joining as {p["name"]}.{sw}</p>'
    return f'''<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3">{n}{b}{who}{ga}</div>'''

def join_screen(joiner='selin', role='collab', members=None, footer=None, top='', web=False, overlay='', large=False, dm_note=False, hdr=None, extra='', no_round=False):
    members = members or [('deniz', ['owner']), ('mert', ['dm'])]
    dn = ''
    if dm_note:
        dn = f'<div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground" role="note">{icon("info", "size-5 shrink-0")}<p class="text-body-sm">Deniz is the Decision Maker now. The role moves to you when you join.</p></div>'
    h = hdr if hdr is not None else (web_brand(account_chip(joiner)) if web else appbar('Join a list', 'close', 'S08-home.html#S08-default'))
    return f'''{h}
  {top}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-4 pt-2">
    {join_hero(large=large)}
    <div class="mt-5 space-y-5">{extra}{dn}{join_facts(role, large, no_round)}{join_members(members, large)}</div>
  </div>
  {footer or join_footer(joiner)}
  {overlay}'''

# --- sorting screen (copied structure from S25 for the "joined" step) ---
def sorting_after_join():
    members = avatar_stack(['deniz', 'mert', 'selin'], 'size-6')
    def dbtn_(kind, ic, lab, past):
        return f'<button class="flex min-w-touch flex-col items-center gap-1.5" aria-label="{lab}, 0 {past}"><span class="flex size-16 items-center justify-center rounded-full bg-{kind}-soft text-{kind}-soft-foreground">{icon(ic, "size-7")}</span><span class="text-caption text-center">{lab} <span class="tabular-nums text-muted-foreground">0</span></span></button>'
    card_body = f'''<img src="{IMG}people/c001.svg" alt="" class="h-[46%] w-full object-cover">
      <div class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-5">
        <h2 class="line-clamp-3 text-card-title">Ayşe Demir</h2>
        <p class="mt-1 text-body-lg text-muted-foreground">Family</p>
        <dl class="mt-4 space-y-2 text-body"><div class="flex gap-3"><dt class="w-16 shrink-0 text-muted-foreground">Phone</dt><dd class="min-w-0 truncate tabular-nums">+90 500 000 97 62</dd></div><div class="flex gap-3"><dt class="w-16 shrink-0 text-muted-foreground">Email</dt><dd class="min-w-0 truncate">ayse.demir@example.com</dd></div><div class="flex gap-3"><dt class="w-16 shrink-0 text-muted-foreground">City</dt><dd class="min-w-0 truncate">İstanbul</dd></div></dl>
        <div class="mt-auto flex gap-2 pt-3"><span class="inline-flex h-7 items-center rounded-full bg-secondary px-2.5 text-caption text-secondary-foreground">Bride's</span></div>
      </div>'''
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    <a href="S09-list-overview.html#S09-shared" class="flex size-12 items-center justify-center rounded-full" aria-label="Close sorting">{icon("x", "size-6")}</a>
    <div class="min-w-0 flex-1 px-1"><h1 class="truncate text-title-3">Wedding guests</h1><p class="text-caption text-muted-foreground">Round 1, shared</p></div>
    <button class="flex size-12 items-center justify-center rounded-full" aria-label="More options">{icon("ellipsis-vertical", "size-6")}</button>
  </header>
  <div class="shrink-0 px-gutter pb-1">
    <div class="flex items-center justify-between gap-3"><span class="text-label tabular-nums">0 / 100 decided</span>{members}</div>
    <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" aria-label="0 of 100 decided"><div class="h-full w-0 rounded-full bg-primary"></div></div>
  </div>
  <div class="relative mt-2 min-h-0 flex-1">
    <div class="absolute inset-x-gutter bottom-5 top-0 flex origin-top scale-95 translate-y-10 flex-col overflow-hidden rounded-hero border bg-card shadow-raised" aria-hidden="true"><img src="{IMG}people/c002.svg" alt="" class="h-[46%] w-full object-cover"></div>
    <article class="absolute inset-x-gutter bottom-5 top-0 flex origin-bottom flex-col overflow-hidden rounded-hero bg-card shadow-hero" aria-label="Ayşe Demir, Family. Phone +90 500 000 97 62. Email ayse.demir@example.com. City İstanbul." aria-roledescription="card" tabindex="0">{card_body}</article>
  </div>
  <div class="flex shrink-0 items-start justify-between px-5 pb-4 pt-2">
    <button class="flex min-w-touch flex-col items-center gap-1.5 opacity-40" aria-label="Nothing to undo" disabled><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("undo-2")}</span><span class="text-caption text-muted-foreground">Undo</span></button>
    {dbtn_("reject", "x", "Reject", "rejected")}
    {dbtn_("maybe", "circle-help", "Maybe", "maybe")}
    {dbtn_("accept", "check", "Accept", "accepted")}
    <button class="flex min-w-touch flex-col items-center gap-1.5" aria-label="Add note"><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("sticky-note")}</span><span class="text-caption text-muted-foreground">Note</span></button>
  </div>
  {snackbar("You joined Wedding guests", bottom="bottom-44", icon_name="circle-check")}'''

def build_s33():
    pg = Page('S33', 'Join a list', 'The signed-in invited person sees who invited them, the list, their role and what it means, the members and their progress, then joins and starts sorting every item of the current round (DM-16). Spec: <a href="S33-join-list.md">S33-join-list.md</a>.')
    F = pg.frame
    pg.section('Join', 'Selin joins from the app (Android). Joining takes one tap; sorting starts right away.')
    F('S33-default', 'Default: join as Collaborator (app)', phone(join_screen(footer=join_footer('selin', href='S25-sorting.html#S25-shared', action='join'))))
    F('S33-joining', 'Joining…', phone(join_screen(footer=join_footer('selin', busy=True))))
    F('S33-joined', 'Joined: sorting starts, snackbar confirms', phone(sorting_after_join()))
    F('S33-decision-maker', 'Invited as Decision Maker (Mert)', phone(join_screen('mert', 'dm', members=[('deniz', ['owner', 'dm'])], dm_note=True, footer=join_footer('mert', href='S25-sorting.html#S25-shared'))))

    pg.section('Web', 'Prototype flow 3: after signing in on the desktop browser (S03-web-desktop), Mert joins and sorts right away with keyboard shortcuts. Nothing to install; "Get the app" is offered but secondary.')
    get_app_btn = btn('Get the app', 'outline', href='S32-invite-link.html#S32-get-app', size='h-12', full=False, extra='px-3 text-label')
    desk = join_screen('mert', members=[('deniz', ['owner', 'dm'])], web=True, hdr=web_brand(f'<span class="flex items-center gap-1">{get_app_btn}{account_chip("mert")}</span>'),
        footer=join_footer('mert', href='S25-sorting.html#S25-web-desktop', action='start-sorting', web=True, get_app=True))
    F('S33-web-desktop', 'Web, desktop browser: Mert joins', desktop(f'swipesort.app/join/{TOKEN}', desk))
    F('S33-web', 'Web, mobile browser', web_phone(join_screen('mert', members=[('deniz', ['owner', 'dm'])], web=True, hdr=smart_banner().replace('#S32-get-app', 'S32-invite-link.html#S32-get-app') + web_brand(account_chip('mert')),
        footer=join_footer('mert', href='S25-sorting.html#S25-web-desktop', web=True))))

    pg.section('States', 'Loading the invite details, offline, the link reset while the person was deciding, and a list with no round in progress.')
    loading = f'''{appbar("Join a list", "close", "S08-home.html#S08-default")}
  <div class="min-h-0 flex-1 px-gutter pt-2" aria-busy="true" role="status" aria-label="Loading invite">
    <div class="flex items-center gap-3"><span class="size-12 animate-pulse rounded-full bg-muted"></span><span class="block h-4 w-1/2 animate-pulse rounded-full bg-muted"></span></div>
    <span class="mt-5 block h-8 w-2/3 animate-pulse rounded-full bg-muted"></span>
    <span class="mt-2 block h-4 w-1/2 animate-pulse rounded-full bg-muted"></span>
    <div class="mt-8 h-56 animate-pulse rounded-group bg-muted"></div>
    <div class="mt-6 h-40 animate-pulse rounded-group bg-muted"></div>
  </div>
  {join_footer("selin", disabled=True)}'''
    F('S33-loading', 'Loading', phone(loading))
    F('S33-offline', 'Offline: joining needs a connection', phone(join_screen(top=offline_banner("You're offline."), footer=join_footer('selin', disabled=True, note='Joining needs a connection. Connect and try again.'))))
    err = f'''<div class="flex gap-3 rounded-control border border-destructive/40 bg-card p-4" role="alert">{icon("circle-alert", "size-5 shrink-0 text-destructive")}<div class="flex-1"><p class="text-label">This invite link was reset</p><p class="mt-0.5 text-body-sm text-muted-foreground">Deniz made a new link while you were here, so this one can't be used to join. Ask Deniz for the new link.</p></div></div>'''
    err_footer = f'''<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3">{btn("Back to my lists", "secondary", href="S08-home.html#S08-default")}</div>'''
    F('S33-error-link-reset', 'Error: link reset while joining', phone(join_screen(extra=err, footer=err_footer)))
    no_round = f'''<div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground" role="note">{icon("info", "size-5 shrink-0")}<p class="text-body-sm">Deniz ended Round 1. You can see the results now. When Deniz starts the next round, you'll sort it with everyone.</p></div>'''
    nr_footer = f'''<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3">{btn("Join list", "primary", href="S09-list-overview.html#S09-shared")}<p class="text-center text-body-sm text-muted-foreground">Joining as Selin Yılmaz.</p></div>'''
    nr = join_screen(extra=no_round, footer=nr_footer, no_round=True).replace('100 items, Round 1 in progress', '100 items, no round in progress')
    F('S33-no-round', 'No round in progress', phone(nr))

    pg.section('Accessibility and iOS', 'Large text: the role rows grow, progress counts move below their bars, the action stays pinned. iOS: full-screen modal with Cancel in the navigation bar.')
    F('S33-large-text', 'Large text (200%)', phone(scale_large(join_screen(large=True, hdr=appbar('Join a list', 'close', 'S08-home.html#S08-default', large=True), footer=f'''<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3"><a href="S25-sorting.html#S25-shared" class="flex min-h-14 w-full items-center justify-center rounded-control bg-primary px-5 py-2 text-center text-title-3 text-primary-foreground">Join and start sorting</a></div>'''))))
    ios_hdr = ios_bar(None, 'Join a list', '').replace('<span></span>', '<a href="S08-home.html#S08-default" class="inline-flex h-12 items-center justify-self-start px-2 text-body text-primary">Cancel</a>', 1)
    F('S33-ios', 'iOS', phone(join_screen(hdr=ios_hdr, footer=join_footer('selin', href='S25-sorting.html#S25-shared')), ios=True))
    pg.write('S33-join-list.html')

# =====================================================================================
# S34 MEMBERS AND ROLES
# =====================================================================================
ROLES = {'deniz': ['owner'], 'mert': ['dm'], 'selin': []}

def member_row(k, roles, viewer='deniz', options=True, done=None, large=False, disabled=False, ios=False):
    p = P[k]
    you = ' <span class="text-muted-foreground">(you)</span>' if k == viewer else ''
    d = p['done'] if done is None else done
    opt = ''
    if options and k != viewer:
        dis = ' disabled' if disabled else ''
        op = ' opacity-50' if disabled else ''
        ic = 'ellipsis' if ios else 'ellipsis-vertical'
        href = {'selin': '#S34-member-sheet', 'mert': '#S34-member-sheet'}.get(k, '#')
        if ios:
            href = '#S34-ios-actions'
        if disabled:
            opt = f'<button class="-mr-2 flex size-12 shrink-0 items-center justify-center rounded-full{op}" aria-label="Options for {p["name"]}"{dis}>{icon(ic)}</button>'
        else:
            opt = f'<a href="{href}" class="-mr-2 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Options for {p["name"]}" data-action="member-options">{icon(ic)}</a>'
    elif options:
        opt = '<span class="-mr-2 size-12 shrink-0" aria-hidden="true"></span>'
    return f'''<li class="flex items-start gap-3 py-3 pl-4 pr-3">{av(k, "size-10")}{member_block(k, roles, k == viewer, large, d)}{opt}</li>'''

def dm_switch_row(k, on, viewer='deniz', disabled=False, ios=False, large=False):
    p = P[k]
    you = ' <span class="text-muted-foreground">(you)</span>' if k == viewer else ''
    t_cls = 'text-title-3 font-normal' if large else 'text-body'
    href = '#S34-dm-off-confirm' if on else ('#S34-dm-self-confirm' if k == viewer else '#S34-dm-confirm')
    return f'<li class="flex min-h-14 items-center gap-3 px-4 py-2">{av(k, "size-8")}<span class="min-w-0 flex-1 {t_cls}">{p["name"]}{you}</span>{switch(on, "Decision Maker: " + p["name"], disabled, ios, href=href)}</li>'

def members_screen(viewer='deniz', dm='mert', roles=None, done=None, offline=False, overlay='', ios=False, large=False,
                   scrolled=False, keys=('deniz', 'mert', 'selin'), dm_pending=None, top_extra='', hdr=None, after_members='', snack=''):
    roles = roles or {k: (['owner'] if k == 'deniz' else []) + (['dm'] if k == dm else []) for k in keys}
    done = done or {}
    owner = 'owner' in roles.get(viewer, [])
    dis = offline
    # members group
    rows = ''.join(member_row(k, roles[k], viewer, options=owner, done=done.get(k), large=large, disabled=dis, ios=ios) for k in keys)
    if owner:
        rows += nav_row('link-2', 'Invite links', '2 active, Collaborator', href='S31-invite.html#S31-pending', large=large, disabled=dis)
        rows += nav_row('user-plus', 'Invite people', href='S31-invite.html#S31-default', primary=True, chevron=False, action='invite', large=large, disabled=dis)
    else:
        rows += nav_row('user-plus', 'Invite people', 'As Collaborator', href='S31-invite.html#S31-collaborator', primary=True, chevron=False, large=large, disabled=dis)
    mem = f'<section>{section_label(f"{len(keys)} members")}{group(rows)}</section>'
    # conflicts
    rule = nav_row('git-compare-arrows', 'Conflict rule', 'Decision Maker decides', href='S35-conflict-rule.html#S35-default', action='conflict-rule', large=large)
    conf_rows = rule
    if viewer == dm:
        conf_rows += nav_row('git-pull-request-arrow', 'Review 15 conflicts', 'You resolve them as Decision Maker', href='S36-conflicts.html#S36-default', large=large)
    conf = f'<section>{section_label("Resolving conflicts")}{group(conf_rows)}</section>'
    # decision maker
    if owner:
        on_set = {dm} if dm_pending is None else ({dm, dm_pending} if dm_pending != 'none' else set())
        sw = ''.join(dm_switch_row(k, k in on_set, viewer, dis, ios, large) for k in keys)
        foot = 'Resolves conflicts and breaks ties. Only one member can have this role: turning it on for someone turns it off for the current one.' if not dis else 'Changes to members need a connection.'
        dmg = f'<section>{section_label("Decision Maker")}{group(sw)}<p class="mt-2 px-1 {"text-body-lg" if large else "text-body-sm"} text-muted-foreground">{foot}</p></section>'
    else:
        if dm == viewer:
            r = f'<li class="flex min-h-14 items-center gap-3 px-4 py-2.5">{av(dm, "size-8")}<span class="min-w-0 flex-1"><span class="block text-body">You\'re the Decision Maker</span><span class="block text-body-sm text-muted-foreground">You resolve conflicts and break ties.</span></span></li>'
        else:
            r = f'<li class="flex min-h-14 items-center gap-3 px-4 py-2.5">{av(dm, "size-8")}<span class="min-w-0 flex-1"><span class="block text-body">{P[dm]["name"]}</span><span class="block text-body-sm text-muted-foreground">Resolves conflicts and breaks ties.</span></span></li>'
        dmg = f'<section>{section_label("Decision Maker")}{group(r)}<p class="mt-2 px-1 text-body-sm text-muted-foreground">Only Deniz, the Owner, can change roles.</p></section>'
    # ownership / leave
    if owner:
        own = group(nav_row('crown', 'Transfer ownership', 'Make another member the Owner', href='#S34-transfer-pick', large=large, disabled=dis)
                    + nav_row('log-out', 'Leave list', href='#S34-leave-owner', destructive=True, large=large, disabled=dis))
    else:
        own = group(nav_row('log-out', 'Leave list', href='#S34-leave-dialog', destructive=True, action='leave', large=large, disabled=dis))
    own = f'<section>{own}</section>'
    body = (conf + dmg + own) if scrolled else (mem + after_members + conf + dmg + own)
    inv = icon_action('user-plus', 'Invite people', 'S31-invite.html#S31-default' if owner else 'S31-invite.html#S31-collaborator', disabled=dis)
    ios_hdr = f'''<header class="flex h-11 shrink-0 items-center justify-between px-2"><a href="S09-list-overview.html#S09-shared" class="inline-flex h-12 items-center gap-0.5 text-body text-primary" aria-label="Back to Wedding guests">{icon("chevron-left", "size-6")}Wedding guests</a><a href="S31-invite.html#S31-ios" class="flex size-12 items-center justify-center text-primary" aria-label="Invite people">{icon("user-plus", "size-6")}</a></header>
  <h1 class="shrink-0 px-4 pb-2 text-title-1">Members</h1>'''
    h = hdr if hdr is not None else (ios_hdr if ios
         else appbar('Members', 'back', 'S09-list-overview.html#S09-shared', sub='Wedding guests', actions=inv, lead_label='Back to Wedding guests', large=large))
    scroll = ''
    off = offline_banner("You're offline. Changes to members need a connection.") if offline else ''
    return f'''{h}
  {off}{top_extra}
  <div class="min-h-0 flex-1 overflow-hidden"><div class="space-y-5 px-gutter pb-6 pt-2 {scroll}">{body}</div></div>
  {f'<div class="shrink-0 px-4 pb-4 pt-2">{snack}</div>' if snack else ''}
  {overlay}'''

def member_sheet(k='selin', ios=False):
    p = P[k]
    on = k == 'mert'
    t = uid('ms')
    rows = f'''<li class="flex min-h-16 items-center gap-4 py-3">{icon("gavel", "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">Decision Maker</span><span class="block text-body-sm text-muted-foreground">Resolves conflicts and breaks ties. Mert has this role now.</span></span>{switch(on, "Decision Maker: " + p["name"], href="#S34-dm-confirm")}</li>
      <li><a href="#S34-transfer-dialog" class="flex min-h-14 items-center gap-4 py-3">{icon("crown", "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">Make Owner</span><span class="block text-body-sm text-muted-foreground">Hand the list over. You become a Collaborator.</span></span></a></li>
      <li><a href="#S34-remove-dialog" class="flex min-h-14 items-center gap-4 py-3 text-destructive" data-action="remove-member">{icon("user-minus", "size-5 shrink-0")}<span class="flex-1 text-body">Remove from list</span></a></li>'''
    return f'''<div class="absolute inset-0 z-40 bg-scrim/50"></div>
  <div class="absolute inset-x-0 bottom-0 z-40 rounded-t-sheet bg-popover px-gutter pb-5 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="{t}">
    {handle()}
    <div class="flex items-start gap-3 pt-3">{av(k, "size-14")}<div class="min-w-0 flex-1"><h2 id="{t}" class="text-title-3">{p["name"]}</h2><p class="truncate text-body-sm text-muted-foreground">{p["email"]}</p><p class="mt-1 text-body-sm text-muted-foreground">Collaborator, joined {p["joined"]}</p></div><button class="-mr-3 -mt-1 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</button></div>
    {progress(p["done"], who=p["first"])}
    <ul class="mt-4 divide-y border-t">{rows}</ul>
  </div>'''

def build_s34():
    pg = Page('S34', 'Members and roles', 'Who is on the list, how far each member is, who resolves conflicts, and every member-management action: invite, change roles, assign the Decision Maker with one switch (DM-10), remove, transfer ownership, leave. Spec: <a href="S34-members.md">S34-members.md</a>.')
    F = pg.frame
    pg.section('Owner view', 'Deniz (Owner) on Wedding guests. Mert is the Decision Maker. The Decision Maker group is the single place to assign the role: one switch per member, at most one on.')
    F('S34-default', 'Default: Owner view', phone(members_screen()))
    F('S34-scrolled', 'Owner view, scrolled to the end', phone(members_screen(scrolled=True)))
    F('S34-finished', 'A member finished sorting (Selin 100 / 100)', phone(members_screen(done={'selin': 100})))
    empty_after = ''
    empty_members = f'''<section>{section_label("1 member")}{group(member_row("deniz", ["owner", "dm"], "deniz"))}
      <div class="mt-3 flex flex-col items-center rounded-group bg-card px-6 py-8 text-center dark:border">{icon("users", "size-8 text-muted-foreground")}<p class="mt-3 text-balance text-title-3">Only you so far</p><p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">Invite people to sort {keep("Wedding guests")} with you. Everyone decides on their own.</p>{btn("Invite people", "primary", href="S31-invite.html#S31-default", size="h-12", extra="mt-5 max-w-xs")}</div></section>'''
    empty = f'''{appbar('Members', 'back', 'S09-list-overview.html#S09-shared', sub='Wedding guests', actions=icon_action('user-plus', 'Invite people', 'S31-invite.html#S31-default'), lead_label='Back to Wedding guests')}
  <div class="min-h-0 flex-1 overflow-hidden"><div class="space-y-5 px-gutter pb-6 pt-2">{empty_members}
    <section>{section_label("Resolving conflicts")}{group(nav_row('git-compare-arrows', 'Conflict rule', 'Decision Maker decides', href='S35-conflict-rule.html#S35-default'))}</section>
    <section>{section_label("Decision Maker")}{group(dm_switch_row('deniz', True))}<p class="mt-2 px-1 text-body-sm text-muted-foreground">You're the Decision Maker until you give the role to someone who joins.</p></section>
  </div></div>'''
    F('S34-empty', 'Only the Owner (nobody joined yet)', phone(empty))

    pg.section('Decision Maker switch (DM-10)', 'One tap on a member\'s switch. Moving the role from one member to another asks once, because it changes who resolves the open conflicts. Turning it on when nobody has the role applies immediately.')
    dm_dialog = dialog('Make Mert the Decision Maker?', "You stop being the Decision Maker. Mert will resolve the 15 open conflicts and any new ones.",
        dbtn('Cancel', href='#S34-default') + dbtn('Change Decision Maker', 'primary', href='#S34-dm-changed', action='confirm-dm'))
    F('S34-dm-confirm', 'Moving the role from Deniz to Mert: confirmation (flow 3)', phone(members_screen(dm='deniz', overlay=dm_dialog)))
    F('S34-dm-changed', 'Role moved: Mert is now the Decision Maker (flow 3)', phone(members_screen(dm='mert', snack=snack_static('Mert is now the Decision Maker', icon_name='gavel'))))
    self_dialog = dialog('Become the Decision Maker?', "Mert stops being the Decision Maker. You'll resolve the 15 open conflicts and any new ones.",
        dbtn('Cancel', href='#S34-default') + dbtn('Become Decision Maker', 'primary'))
    F('S34-dm-self-confirm', 'Owner takes the role themselves', phone(members_screen(overlay=self_dialog)))
    off_dialog = dialog('Turn off the Decision Maker?', "With the rule “Decision Maker decides”, conflicts need a Decision Maker. Without one, they stay open until members change their decisions to match. You can turn it on again at any time.",
        dbtn('Cancel', href='#S34-default') + dbtn('Turn off', 'primary'))
    F('S34-dm-off-confirm', 'Turning the role off: confirmation', phone(members_screen(overlay=off_dialog)))

    pg.section('Member options', 'Tap a member\'s options button (or the row). The sheet repeats the Decision Maker switch (same state as the group), and holds Make Owner and Remove from list.')
    F('S34-member-sheet', 'Member options sheet: role change (Selin)', phone(members_screen(overlay=member_sheet('selin'))))
    keep_id, disc_id = uid('rk'), uid('rd')
    rg = uid('rg')
    remove_extra = f'''<div class="mt-4 space-y-1" role="radiogroup" aria-label="Selin's decisions">
        <button role="radio" aria-checked="true" class="flex w-full items-start gap-3 rounded-control py-2 text-left">{radio_dot(True)}<span><span class="block text-body">Keep Selin's decisions</span><span class="block text-body-sm text-muted-foreground">They still count toward Agreed, Pending and Conflict.</span></span></button>
        <button role="radio" aria-checked="false" class="flex w-full items-start gap-3 rounded-control py-2 text-left">{radio_dot(False)}<span><span class="block text-body">Discard Selin's decisions</span><span class="block text-body-sm text-muted-foreground">Item statuses are recalculated without them.</span></span></button>
      </div>'''
    rem = dialog('Remove Selin from “Wedding guests”?', "Selin can't open the list anymore, and Selin's invite link stops working. Choose what happens to Selin's 43 decisions.",
        dbtn('Cancel', href='#S34-default') + dbtn('Remove Selin', 'destructive', href='#S34-removed', action='confirm-remove'), extra_body=remove_extra)
    F('S34-remove-dialog', 'Remove member: keep or discard decisions (DM-17)', phone(members_screen(overlay=rem)))
    F('S34-removed', 'Member removed: snackbar with Undo', phone(members_screen(keys=('deniz', 'mert'), snack=snack_static('Removed Selin', 'Undo')).replace('2 active, Collaborator', '1 active, Collaborator')))
    tr = dialog('Make Mert the Owner?', "Mert will manage members, rounds and the conflict rule, and can rename or delete the list.\nYou'll stay on the list as a Collaborator. Only Mert can make you the Owner again.",
        dbtn('Cancel', href='#S34-default') + dbtn('Make Mert Owner', 'primary', href='#S34-transferred', action='confirm-transfer'))
    F('S34-transfer-dialog', 'Transfer ownership: confirmation', phone(members_screen(overlay=tr)))
    transferred_roles = {'deniz': [], 'mert': ['owner', 'dm'], 'selin': []}
    F('S34-transferred', 'Ownership transferred: Deniz now sees the Collaborator view', phone(members_screen(roles=transferred_roles, snack=snack_static('Mert is now the Owner', icon_name='crown')).replace('Only Deniz, the Owner, can change roles.', 'Only Mert, the Owner, can change roles.')))

    pg.section('Leaving', 'Members can leave at any time; their decisions stay. The Owner must hand the list over first.')
    lo = dialog('Choose a new Owner first', '“Wedding guests” needs an Owner. Make another member the Owner, then you can leave. To remove the list for everyone, delete it instead.',
        dbtn('Cancel', href='#S34-default') + dbtn('Choose new Owner', 'primary', href='#S34-transfer-pick'))
    F('S34-leave-owner', 'Owner tries to leave', phone(members_screen(overlay=lo)))
    pick_rows = f'''<div class="mt-3 space-y-1" role="radiogroup" aria-label="New Owner">
      <button role="radio" aria-checked="true" class="flex min-h-14 w-full items-center gap-3 py-2 text-left">{radio_dot(True)}{av("mert", "size-10")}<span class="min-w-0 flex-1"><span class="block text-body">Mert Aydın</span><span class="block text-body-sm text-muted-foreground">Decision Maker</span></span></button>
      <button role="radio" aria-checked="false" class="flex min-h-14 w-full items-center gap-3 py-2 text-left">{radio_dot(False)}{av("selin", "size-10")}<span class="min-w-0 flex-1"><span class="block text-body">Selin Yılmaz</span><span class="block text-body-sm text-muted-foreground">Collaborator</span></span></button>
    </div>
    <p class="mt-3 text-body-sm text-muted-foreground">Mert will manage members, rounds and the conflict rule. You'll leave “Wedding guests”: your 76 decisions stay and still count, items you haven't decided stop waiting for you, and your private notes are deleted.</p>
    <div class="mt-5 space-y-2">{btn("Make Mert Owner and leave", "destructive", href="S08-home.html#S08-default")}{btn("Make Mert Owner and stay", "ghost", size="h-12", href="#S34-transferred")}</div>'''
    F('S34-transfer-pick', 'Choose the new Owner (from Leave list or Transfer ownership)', phone(members_screen(overlay=bottom_sheet('Choose the new Owner', pick_rows))))
    lv = dialog('Leave “Wedding guests”?', "You won't see this list anymore. Your 43 decisions stay and still count toward the list status. Items you haven't decided stop waiting for you, and your private notes are deleted. To come back, ask Deniz for a new invite.",
        dbtn('Cancel', href='#S34-collaborator') + dbtn('Leave list', 'destructive', href='S10-list-management.html#S10-left-snackbar', action='confirm-leave'))
    F('S34-leave-dialog', 'Collaborator leaves (Selin)', phone(members_screen(viewer='selin', overlay=lv)))
    lvd = dialog('Leave “Wedding guests”?', "You won't see this list anymore. Your 85 decisions stay and still count toward the list status. You're the Decision Maker, so nobody will have this role until Deniz chooses someone. The 15 open conflicts stay open.",
        dbtn('Cancel', href='#S34-decision-maker') + dbtn('Leave list', 'destructive', href='S08-home.html#S08-default', action='confirm-leave'))
    F('S34-leave-decision-maker', 'Decision Maker leaves (Mert): role left empty', phone(members_screen(viewer='mert', overlay=lvd)))

    pg.section('Other members\' views', 'Collaborators and the Decision Maker see the same screen read-only: no switches or member options. They can invite as Collaborator and leave.')
    F('S34-collaborator', 'Collaborator view (Selin)', phone(members_screen(viewer='selin')))
    F('S34-decision-maker', 'Decision Maker view (Mert)', phone(members_screen(viewer='mert')))

    pg.section('States', 'Loading, error and offline. Offline, the screen shows the last synced progress; every change is disabled with the reason.')
    load = f'''{appbar('Members', 'back', 'S09-list-overview.html#S09-shared', sub='Wedding guests', lead_label='Back to Wedding guests')}
  <div class="min-h-0 flex-1 space-y-3 px-4 pt-2" aria-busy="true" role="status" aria-label="Loading members">
    <span class="mx-1 block h-4 w-24 animate-pulse rounded-full bg-muted"></span>
    <div class="space-y-5 rounded-group bg-card p-4 dark:border">''' + ''.join('<div class="flex items-start gap-3"><span class="size-10 animate-pulse rounded-full bg-muted"></span><div class="flex-1 space-y-2"><span class="block h-4 w-1/2 animate-pulse rounded-full bg-muted"></span><span class="block h-3 w-1/4 animate-pulse rounded-full bg-muted"></span><span class="block h-1.5 w-full animate-pulse rounded-full bg-muted"></span></div></div>' for _ in range(3)) + '''</div>
    <div class="h-16 animate-pulse rounded-group bg-muted"></div>
    <div class="h-40 animate-pulse rounded-group bg-muted"></div>
  </div>'''
    F('S34-loading', 'Loading', phone(load))
    err = f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1"><a href="S09-list-overview.html#S09-shared" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Back to Wedding guests">{icon("arrow-left", "size-6")}</a><span class="flex-1"></span></header>
  <div class="flex flex-1 flex-col items-center justify-center px-8 pb-16 text-center">
    {icon("cloud-alert", "size-8 text-muted-foreground")}
    <h1 class="mt-4 text-balance text-title-3">Members couldn't be loaded</h1>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">SwipeSort didn't respond. Check your connection and try again.</p>
    <p class="mt-3 max-w-xs text-balance text-body-sm text-muted-foreground">Your decisions are saved on this phone.</p>
    {btn("Try again", "secondary", size="h-12", extra="mt-6 max-w-xs")}
    {btn("Back to list", "ghost", href="S09-list-overview.html#S09-shared", size="h-12", extra="mt-2 max-w-xs")}
  </div>'''
    F('S34-error', 'Error', phone(err))
    F('S34-offline', 'Offline: changes need a connection', phone(members_screen(offline=True)))

    pg.section('Accessibility', 'Large text: names and role badges wrap, counts move under the progress bars, the switch rows grow.')
    F('S34-large-text', 'Large text (200%)', phone(scale_large(members_screen(large=True))))

    pg.section('iOS and web', 'iOS: back chevron with the list name, inset grouped sections, iOS switches, member options as an action sheet. Web desktop: the phone layout centered; member options open as a dropdown menu next to the button.')
    F('S34-ios', 'iOS', phone(members_screen(ios=True), ios=True))
    act = f'''<div class="absolute inset-0 z-40 bg-scrim/40"></div>
  <div class="absolute inset-x-2 bottom-2 z-40 space-y-2" role="dialog" aria-modal="true" aria-label="Options for Selin Yılmaz">
    <div class="overflow-hidden rounded-dialog bg-popover text-center shadow-dialog">
      <p class="px-4 pb-2 pt-3 text-caption text-muted-foreground">Selin Yılmaz, Collaborator</p>
      <a href="#S34-dm-confirm" class="flex h-14 items-center justify-center border-t text-title-3 font-normal text-primary">Make Decision Maker</a>
      <a href="#S34-transfer-dialog" class="flex h-14 items-center justify-center border-t text-title-3 font-normal text-primary">Make Owner</a>
      <a href="#S34-remove-dialog" class="flex h-14 items-center justify-center border-t text-title-3 font-normal text-destructive">Remove from list</a>
    </div>
    <a href="#S34-ios" class="flex h-14 items-center justify-center rounded-dialog bg-popover text-title-3 text-primary shadow-dialog">Cancel</a>
  </div>'''
    F('S34-ios-actions', 'iOS member options (action sheet)', phone(members_screen(ios=True, overlay=act), ios=True))
    menu = f'''<div class="absolute right-4 top-80 z-40 w-72 overflow-hidden rounded-control bg-popover py-1.5 shadow-overlay" role="menu" aria-label="Options for Selin Yılmaz">
      <div role="menuitemcheckbox" aria-checked="false" tabindex="0" class="flex min-h-12 items-center gap-3 px-4 py-2 text-body">{icon("gavel", "size-5 shrink-0 text-muted-foreground")}<span class="flex-1">Decision Maker</span><span class="flex h-8 w-13 shrink-0 items-center rounded-full border-2 border-input bg-muted p-1" aria-hidden="true"><span class="size-5 rounded-full bg-muted-foreground"></span></span></div>
      <a href="#S34-transfer-dialog" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body">{icon("crown", "size-5 text-muted-foreground")}Make Owner</a>
      <div class="my-1.5 h-px bg-border"></div>
      <a href="#S34-remove-dialog" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body text-destructive">{icon("user-minus", "size-5")}Remove from list</a>
    </div>'''
    F('S34-web-desktop', 'Web, desktop: member options as a menu', desktop('swipesort.app/l/7Hq2xK/members', members_screen(overlay=menu)))
    pg.write('S34-members.html')

if __name__ == '__main__':
    build_s31()
    build_s32()
    build_s33()
    build_s34()
