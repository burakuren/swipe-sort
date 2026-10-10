# Usage: python3 tools/generators/S35-S38-collaboration.py
# Generates the Group G2 collaboration mockups (static frames):
#   design/03-screens/S35-conflict-rule.html, S36-conflicts.html, S37-bulk-resolve.html, S38-activity.html
# Structure follows tools/generators/S25-sorting.py (quality reference) and S31-S34-collaboration.py (G1).
# Item data, decisions and notes are read from design/02-data/sample-data.json, so counts stay real.
import os
import json
import itertools

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCREENS = os.path.join(ROOT, 'design', '03-screens')
DATA = json.load(open(os.path.join(ROOT, 'design', '02-data', 'sample-data.json'), encoding='utf-8'))
IMG = '../02-data/images/'
GET_APP = 'https://swipesort.app/get'

_ids = itertools.count(1)
def uid(prefix='g'):
    return f'{prefix}{next(_ids)}'

def icon(name, size='size-5', extra=''):
    return f'<i class="i-lucide-{name} {size} {extra}" aria-hidden="true"></i>'.replace('  ', ' ').replace(' "', '"')

# ---------------------------------------------------------------- data
P = {
    'deniz': dict(name='Deniz Yılmaz', first='Deniz', img='people/u-deniz.svg', ini='DY', role='Owner', uid='u-deniz'),
    'mert': dict(name='Mert Aydın', first='Mert', img='people/u-mert.svg', ini='MA', role='Decision Maker', uid='u-mert'),
    'selin': dict(name='Selin Yılmaz', first='Selin', img=None, ini='SY', role='Collaborator', uid='u-selin'),
}
UID2K = {v['uid']: k for k, v in P.items()}
CONTACTS = {c['id']: c for c in DATA['contacts']}
SHARED = {i['itemId']: i for i in DATA['shared']['items']}
NOTES = DATA['shared']['notes']
CONFLICTS = [i['itemId'] for i in DATA['shared']['items'] if i['status'] == 'conflict']
assert len(CONFLICTS) == 15

def initials(name):
    w = name.replace('(', '').split()
    return (w[0][0] + w[-1][0]).upper() if len(w) > 1 else w[0][:2].upper()

def item(cid):
    c = CONTACTS[cid]
    dec = {UID2K[u]: v for u, v in SHARED[cid]['decisions'].items()}
    return dict(id=cid, name=c['name'], sub=f"{c['relationship']}, {c['city']}", photo=c['photo'].replace('images/', '') if c['photo'] else None,
                ini=initials(c['name']), dec=dec, notes=[n for n in NOTES if n['itemId'] == cid])

# Mert's decisions on the 15 conflicts (DM-11 / DM-12)
MERT = {cid: item(cid)['dec']['mert'] for cid in CONFLICTS}
MERT_DECIDED = [c for c in CONFLICTS if MERT[c]]
MERT_UNDECIDED = [c for c in CONFLICTS if not MERT[c]]
BULK = {k: sum(1 for c in MERT_DECIDED if MERT[c] == k) for k in ('reject', 'maybe', 'accept')}
assert len(MERT_DECIDED) == 12 and MERT_UNDECIDED == ['c012', 'c034', 'c056']

# Majority recalculation (S35 confirm)
def majority(cid):
    d = [v for v in item(cid)['dec'].values()]
    if None in d:
        return None
    from collections import Counter
    c = Counter(d).most_common()
    if len(c) > 1 and c[0][1] == c[1][1]:
        return 'tie'
    return c[0][0]
MAJ = {c: majority(c) for c in CONFLICTS}
MAJ_FINAL = [c for c in CONFLICTS if MAJ[c] not in (None, 'tie')]
MAJ_OPEN = [c for c in CONFLICTS if MAJ[c] is None]
MAJ_SPLIT = {k: sum(1 for c in MAJ_FINAL if MAJ[c] == k) for k in ('reject', 'maybe', 'accept')}
assert len(MAJ_FINAL) == 8 and len(MAJ_OPEN) == 7

DEC = {'accept': ('check', 'Accept', 'Accepted', 'accepted'), 'reject': ('x', 'Reject', 'Rejected', 'rejected'), 'maybe': ('circle-help', 'Maybe', 'Maybe', 'chose Maybe')}

# ---------------------------------------------------------------- atoms
AV_TXT = {'size-6': 'text-caption', 'size-8': 'text-caption', 'size-10': 'text-label', 'size-14': 'text-title-3', 'size-16': 'text-title-2', 'size-24': 'text-title-1'}

def av(k, size='size-10', ring=''):
    p = P[k]
    if p['img']:
        return f'<img src="{IMG}{p["img"]}" alt="" class="{size} shrink-0 rounded-full {ring}">'.replace(' "', '"')
    return f'<span class="flex {size} shrink-0 items-center justify-center rounded-full bg-muted {AV_TXT.get(size, "text-label")} text-muted-foreground {ring}" aria-hidden="true">{p["ini"]}</span>'.replace(' "', '"')

def item_av(it, size='size-10'):
    if it['photo']:
        return f'<img src="{IMG}{it["photo"]}" alt="" class="{size} shrink-0 rounded-full object-cover">'
    return f'<span class="flex {size} shrink-0 items-center justify-center rounded-full bg-muted {AV_TXT.get(size, "text-label")} text-muted-foreground" aria-hidden="true">{it["ini"]}</span>'

def dbadge(kind, label=None):
    if not kind:
        return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full bg-muted px-2.5 text-caption text-muted-foreground">{icon("circle-dashed", "size-4")}{label or "Not decided"}</span>'
    ic, _, state, _ = DEC[kind]
    return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full bg-{kind}-soft px-2.5 text-caption text-{kind}-soft-foreground">{icon(ic, "size-4")}{label or state}</span>'

def status_chip(kind, label=None):
    if kind == 'conflict':
        return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full bg-conflict px-2.5 text-caption text-conflict-foreground">{icon("git-compare-arrows", "size-4")}{label or "Conflict"}</span>'
    if kind == 'agreed':
        return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full border px-2.5 text-caption">{icon("check-check", "size-4")}{label or "Agreed"}</span>'
    if kind == 'pending':
        return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full bg-muted px-2.5 text-caption text-muted-foreground">{icon("clock", "size-4")}{label or "Pending"}</span>'
    if kind == 'resolved':
        return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full border px-2.5 text-caption">{icon("gavel", "size-4")}{label or "Resolved by Mert"}</span>'
    if kind == 'majority':
        return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full border px-2.5 text-caption">{icon("vote", "size-4")}{label or "Majority"}</span>'

def dot(kind, size='size-5', isize='size-3', ring='ring-card', pos='-bottom-1 -right-1'):
    if not kind:
        return f'<span class="absolute {pos} flex {size} items-center justify-center rounded-full bg-card text-muted-foreground ring-2 {ring}">{icon("circle-dashed", isize)}</span>'
    return f'<span class="absolute {pos} flex {size} items-center justify-center rounded-full bg-{kind} text-{kind}-foreground ring-2 {ring}">{icon(DEC[kind][0], isize)}</span>'

def dec_text(dec, you=None):
    parts = []
    for k in ('deniz', 'mert', 'selin'):
        v = dec.get(k)
        nm = 'You' if k == you else P[k]['first']
        parts.append(f'{nm}: {DEC[v][1] if v else "not decided"}')
    return '. '.join(parts) + '.'

def md_compact(dec, size='size-6', dsize='size-4', isize='size-2.5', ring='ring-card', you=None, gap=False):
    sp = 'gap-2.5' if gap else '-space-x-1'
    pos = '-bottom-1.5 -right-2' if gap else '-bottom-1 -right-1'
    inner = ''.join(f'<span class="relative">{av(k, size, "ring-2 " + ring)}{dot(dec.get(k), dsize, isize, ring, pos)}</span>' for k in ('deniz', 'mert', 'selin'))
    return f'<span class="flex shrink-0 {sp}" role="img" aria-label="{dec_text(dec, you)}">{inner}</span>'

def switch(on, label, disabled=False, href=None):
    op = ' opacity-50' if disabled else ''
    if on:
        inner = '<span class="flex h-8 w-13 items-center rounded-full bg-primary p-1"><span class="ml-auto size-6 rounded-full bg-primary-foreground"></span></span>'
    else:
        inner = '<span class="flex h-8 w-13 items-center rounded-full border-2 border-input bg-muted p-1"><span class="size-5 rounded-full bg-muted-foreground"></span></span>'
    attrs = f'role="switch" aria-checked="{"true" if on else "false"}" aria-label="{label}" class="-my-2 flex h-12 w-13 shrink-0 items-center{op}"'
    if href and not disabled:
        return f'<a href="{href}" {attrs}>{inner}</a>'
    return f'<button {attrs}{" disabled" if disabled else ""}>{inner}</button>'

def radio_dot(on, disabled=False):
    op = ' opacity-50' if disabled else ''
    if on:
        return f'<span class="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary{op}" aria-hidden="true"><span class="size-3 rounded-full bg-primary"></span></span>'
    return f'<span class="mt-0.5 size-6 shrink-0 rounded-full border-2 border-input{op}" aria-hidden="true"></span>'

VARIANT = {
    'primary': 'bg-primary text-primary-foreground',
    'secondary': 'bg-secondary text-secondary-foreground',
    'outline': 'border border-input bg-card',
    'ghost': '',
    'destructive': 'bg-destructive text-destructive-foreground',
    'link': 'text-primary',
}

def btn(text, kind='primary', href=None, action=None, ic=None, size='h-12', full=True, disabled=False, busy=False, extra='', label=None):
    w = 'w-full' if full else ''
    px = 'px-5' if kind != 'link' else 'px-1'
    ico = icon('loader-circle', 'size-5 animate-spin') if busy else (icon(ic) if ic else '')
    op = ' opacity-50' if disabled else ''
    act = f' data-action="{action}"' if action else ''
    bz = ' aria-busy="true"' if busy else ''
    al = f' aria-label="{label}"' if label else ''
    c = f'flex {size} {w} items-center justify-center gap-2 rounded-control {px} text-label-lg {VARIANT[kind]}{op} {extra}'
    c = ' '.join(c.split())
    if href and not disabled and not busy:
        return f'<a href="{href}" class="{c}"{act}{al}>{ico}{text}</a>'
    return f'<button class="{c}"{act}{bz}{al}{" disabled" if disabled else ""}>{ico}{text}</button>'

def dbtn(text, kind='ghost', href=None, action=None):
    cls = {'ghost': '', 'destructive': 'bg-destructive text-destructive-foreground', 'primary': 'bg-primary text-primary-foreground'}[kind]
    act = f' data-action="{action}"' if action else ''
    c = ' '.join(f'inline-flex h-12 items-center rounded-control px-4 text-label-lg {cls}'.split())
    if href:
        return f'<a href="{href}" class="{c}"{act}>{text}</a>'
    return f'<button class="{c}"{act}>{text}</button>'

def snackbar(text, action=None, bottom='bottom-6', role='status', icon_name=None, href=None, action_name=None):
    if action:
        an = f' data-action="{action_name}"' if action_name else ''
        a = (f'<a href="{href}" class="-my-1 inline-flex h-12 shrink-0 items-center rounded-sm px-3 text-label text-primary-inverse"{an}>{action}</a>' if href
             else f'<button class="-my-1 inline-flex h-12 shrink-0 items-center rounded-sm px-3 text-label text-primary-inverse"{an}>{action}</button>')
    else:
        a = ''
    ic = icon(icon_name, 'size-5 shrink-0') if icon_name else ''
    pad = 'py-1.5 pl-4 pr-1.5' if action else 'px-4 py-3'
    return f'<div class="absolute inset-x-4 {bottom} z-40 flex min-h-12 items-center gap-3 rounded-control bg-foreground {pad} text-background shadow-overlay" role="{role}">{ic}<span class="flex-1 text-body-sm">{text}</span>{a}</div>'

def offline_banner(text="You're offline. Decisions are saved on this phone."):
    return f'<div class="flex shrink-0 items-center gap-2 bg-muted px-gutter py-2 text-body-sm" role="status">{icon("wifi-off", "size-4 shrink-0")}<span class="flex-1">{text}</span></div>'

def section_label(text, extra=''):
    return f'<h2 class="px-1 pb-2 text-label text-muted-foreground {extra}">{text}</h2>'.replace(' "', '"')

def group(rows, extra=''):
    return f'<ul class="divide-y overflow-hidden rounded-group bg-card dark:border {extra}">{rows}</ul>'.replace(' "', '"')

def dialog(title, body, actions, extra_body='', z='z-50'):
    t, d = uid('dt'), uid('dd')
    return f'''<div class="absolute inset-0 {z} bg-scrim/50"></div>
  <div class="absolute inset-0 {z} flex items-center justify-center px-6">
    <div class="w-full rounded-dialog bg-popover p-6 shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="{t}" aria-describedby="{d}">
      <h2 id="{t}" class="text-title-3">{title}</h2>
      <p id="{d}" class="mt-2 text-body text-muted-foreground">{body}</p>
      {extra_body}
      <div class="mt-6 flex flex-wrap justify-end gap-2">{actions}</div>
    </div>
  </div>'''

def handle():
    return '<div class="flex shrink-0 justify-center py-1.5"><span class="h-1 w-8 rounded-full bg-muted-foreground/40"></span></div>'

def alert(kind, title, body, ic=None, action=''):
    if kind == 'info':
        return f'<div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground" role="note">{icon(ic or "info", "size-5 shrink-0")}<div class="min-w-0 flex-1"><p class="text-label">{title}</p><p class="mt-0.5 text-body-sm">{body}</p>{action}</div></div>'
    if kind == 'error':
        return f'<div class="flex gap-3 rounded-control border border-destructive/40 bg-card p-4" role="alert">{icon(ic or "circle-alert", "size-5 shrink-0 text-destructive")}<div class="min-w-0 flex-1"><p class="text-label">{title}</p><p class="mt-0.5 text-body-sm text-muted-foreground">{body}</p>{action}</div></div>'
    return f'<div class="flex gap-3 rounded-control border bg-card p-4" role="note">{icon(ic or "info", "size-5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="text-label">{title}</p><p class="mt-0.5 text-body-sm text-muted-foreground">{body}</p>{action}</div></div>'

def link(text, href='#', action=None):
    act = f' data-action="{action}"' if action else ''
    return f'<a href="{href}" class="-ml-1 mt-1 inline-flex h-12 items-center px-1 text-label text-primary underline underline-offset-4"{act}>{text}</a>'

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
        files = {'S35': 'S35-conflict-rule.html', 'S36': 'S36-conflicts.html', 'S37': 'S37-bulk-resolve.html', 'S38': 'S38-activity.html'}
        for sid, fn in files.items():
            if sid != self.sid:
                html = html.replace(f'href="#{sid}-', f'href="{fn}#{sid}-')
        with open(os.path.join(SCREENS, filename), 'w', encoding='utf-8') as f:
            f.write(html)
        print(filename, 'frames:', html.count('data-frame='))

# ---------------------------------------------------------------- chrome
def appbar(title, lead='back', lead_href='#', sub=None, actions='', lead_label=None, large=False):
    ic = {'back': 'arrow-left', 'close': 'x'}[lead]
    ll = lead_label or {'back': 'Back', 'close': 'Close'}[lead]
    t_cls = 'text-title-2' if large else 'text-title-3'
    s = f'<p class="truncate text-caption text-muted-foreground">{sub}</p>' if sub else ''
    return f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="{lead_href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{ll}" data-action="back">{icon(ic, "size-6")}</a>
    <div class="min-w-0 flex-1 px-1"><h1 class="truncate {t_cls}">{title}</h1>{s}</div>
    {actions}
  </header>'''

def icon_action(ic, label, href='#', action=None, disabled=False, extra=''):
    act = f' data-action="{action}"' if action else ''
    if disabled:
        return f'<button class="flex size-12 shrink-0 items-center justify-center rounded-full opacity-50" aria-label="{label}" disabled>{icon(ic, "size-6")}</button>'
    return f'<a href="{href}" class="flex size-12 shrink-0 items-center justify-center rounded-full {extra}" aria-label="{label}"{act}>{icon(ic, "size-6")}</a>'.replace(' "', '"')

def ios_bar(back=None, title='', right='', back_href='#'):
    b = f'<a href="{back_href}" class="inline-flex h-12 items-center gap-0.5 justify-self-start text-body text-primary" aria-label="Back to {back}">{icon("chevron-left", "size-6")}{back}</a>' if back else '<span></span>'
    return f'''<header class="grid h-11 shrink-0 grid-cols-[1fr_auto_1fr] items-center px-2">
    {b}
    <h1 class="text-body font-semibold">{title}</h1>
    <div class="flex justify-end">{right}</div>
  </header>'''

NAV = [('lists', 'Lists', 'list-checks', 'S08-home.html#S08-default'),
       ('activity', 'Activity', 'activity', 'S38-activity.html#S38-default'),
       ('settings', 'Settings', 'settings', 'S06-settings.html#S06-default')]

def bottom_nav(active='activity', large=False, badge=0):
    out = []
    lab = 'text-label' if large else 'text-caption'
    for key, label, ic, href in NAV:
        if key == active:
            b = f'<span class="absolute right-3 top-0 flex h-5 min-w-5 items-center justify-center rounded-full bg-primary px-1 text-caption leading-none text-primary-foreground">{badge}</span>' if badge and key == 'activity' else ''
            al = f' aria-label="Activity, {badge} unread"' if b else ''
            out.append(f'<a href="{href}" class="flex flex-1 flex-col items-center justify-center gap-1 {lab}" aria-current="page"{al}><span class="relative flex h-8 w-16 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon(ic, "size-6")}{b}</span><span class="font-semibold">{label}</span></a>')
        else:
            out.append(f'<a href="{href}" class="flex flex-1 flex-col items-center justify-center gap-1 {lab} text-muted-foreground"><span class="flex h-8 w-16 items-center justify-center">{icon(ic, "size-6")}</span>{label}</a>')
    return f'<nav class="flex {"min-h-24" if large else "h-bottom-nav"} shrink-0 border-t bg-card" aria-label="Main">{"".join(out)}</nav>'

def ios_tab_bar(active='activity', badge=0):
    out = []
    for key, label, ic, href in NAV:
        cur = ' aria-current="page"' if key == active else ''
        col = 'text-primary' if key == active else 'text-muted-foreground'
        b = f'<span class="absolute -right-2.5 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-primary px-1 text-caption leading-none text-primary-foreground">{badge}</span>' if badge and key == 'activity' else ''
        al = f' aria-label="Activity, {badge} unread"' if b else ''
        out.append(f'<a href="{href}" class="flex flex-1 flex-col items-center justify-center gap-0.5 text-caption {col}"{cur}{al}><span class="relative">{icon(ic, "size-6")}{b}</span>{label}</a>')
    return f'<nav class="flex h-14 shrink-0 border-t bg-card" aria-label="Main">{"".join(out)}</nav>'

def kbd(k, t):
    return f'<span class="inline-flex items-center gap-1.5"><kbd class="inline-flex h-6 min-w-6 items-center justify-center rounded-sm border border-b-2 bg-card px-1.5 text-caption text-foreground">{k}</kbd>{t}</span>'

# =====================================================================================
# S35 CONFLICT RULE
# =====================================================================================
EX = item('c002')  # Mehmet Yılmaz: Deniz Accept, Mert Reject, Selin Accept

RULES = {
    'everyone': dict(title='Everyone must agree', ic='users',
                     desc='Final only when every member chooses the same. Members can change their decision to match.',
                     result='Stays a conflict until all three match.'),
    'majority': dict(title='Majority decides', ic='vote',
                     desc='Once everyone has decided, the most chosen decision is final. Ties go to the Decision Maker.',
                     result='Accept is final, 2 of 3 chose it.'),
    'dm': dict(title='Decision Maker decides', ic='gavel',
               desc='The Decision Maker chooses the final decision for each conflict.',
               result='Mert chooses the final decision.'),
}

def example_block(large=False):
    t = 'text-title-3 font-normal' if large else 'text-body-sm'
    return f'''<div class="flex items-center gap-3 rounded-control border bg-card px-4 py-3">
      {md_compact(EX['dec'], 'size-8', 'size-5', 'size-3', 'ring-card', gap=True)}
      <p class="min-w-0 flex-1 {t}"><span class="text-muted-foreground">Example:</span> Deniz and Selin accept Mehmet Yılmaz, Mert rejects.</p>
    </div>'''

def rule_card(key, selected=False, note='', href=None, action=None, disabled=False, large=False, extra='', result_text=None):
    r = RULES[key]
    border = 'border-2 border-primary' if selected else 'border'
    if disabled:
        border = 'border-2 border-dashed border-input' if selected else 'border border-dashed border-input'
    t_cls = 'text-title-1' if large else 'text-title-3'
    d_cls = 'text-title-3 font-normal' if large else 'text-body-sm'
    result = f'<p class="mt-2 flex gap-2 {d_cls}">{icon("corner-down-right", "size-4 mt-0.5 shrink-0 text-muted-foreground")}<span><span class="text-muted-foreground">Example:</span> {result_text or r["result"]}</span></p>'
    n = f'<div class="mt-3 border-t pt-2.5 {d_cls}">{note}</div>' if note else ''
    inner = f'''<span class="flex items-start gap-3">{radio_dot(selected, disabled)}<span class="min-w-0 flex-1"><span class="flex items-center justify-between gap-2"><span class="{t_cls}{" text-muted-foreground" if disabled else ""}">{r["title"]}</span>{icon(r["ic"], "size-5 shrink-0 text-muted-foreground")}</span><span class="mt-1 block {d_cls} text-muted-foreground">{r["desc"]}</span></span></span>{result}'''
    act = f' data-action="{action}"' if action else ''
    attrs = f'role="radio" aria-checked="{"true" if selected else "false"}"'
    if href and not disabled:
        head = f'<a href="{href}" {attrs} class="block"{act}>{inner}</a>'
    else:
        head = f'<div {attrs}{" aria-disabled=\"true\"" if disabled else ""}>{inner}</div>'
    bg = 'bg-transparent' if disabled else 'bg-card'
    return f'<div class="rounded-tile {border} {bg} p-4">{head}{n}{extra}</div>'

def dm_note_row(name='mert', change_href='S34-members.html#S34-default', disabled=False):
    ch = (f'<a href="{change_href}" class="-mr-2 inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label text-primary" data-action="change-decision-maker" aria-label="Change Decision Maker">Change</a>' if not disabled
          else '<button class="-mr-2 inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label text-primary opacity-50" disabled aria-label="Change Decision Maker">Change</button>')
    return f'<div class="flex items-center gap-3">{av(name, "size-8")}<span class="min-w-0 flex-1"><span class="block text-body">{P[name]["name"]}</span><span class="block text-caption text-muted-foreground">Decision Maker</span></span>{ch}</div>'

def s35_screen(current='dm', viewer='deniz', overlay='', offline=False, dm='mert', large=False, ios=False, top='', dm_none_open=False, dm_pending=None, scrolled=False):
    owner = viewer == 'deniz'
    hdr = (ios_bar('Members', 'Conflict rule', back_href='S34-members.html#S34-ios') if ios else
           appbar('Conflict rule', 'back', 'S34-members.html#S34-default', sub='Wedding guests', lead_label='Back to Members', large=large))
    off = offline_banner("You're offline. Changing the rule needs a connection.") if offline else ''
    b = 'text-title-3 font-normal' if large else 'text-body'
    if owner:
        intro = f'<p class="px-1 {b} text-muted-foreground">When members decide an item differently, it\'s a conflict. Choose how conflicts get a final decision.</p>'
        cards = []
        for key in ('everyone', 'majority', 'dm'):
            sel = key == current
            note = ''
            href = {'everyone': '#S35-confirm-everyone', 'majority': '#S35-confirm-majority', 'dm': '#S35-default'}[key]
            action = {'everyone': 'rule-everyone', 'majority': 'rule-majority', 'dm': 'rule-decision-maker'}[key]
            if current == 'majority':
                href = {'everyone': '#S35-confirm-everyone', 'majority': '#S35-switched', 'dm': '#S35-dm-none' if dm is None else '#S35-confirm-dm'}[key]
            if key == 'dm':
                if dm and sel:
                    note = f'<p class="text-muted-foreground">Current rule. Mert has 15 conflicts to resolve.</p><div class="mt-3">{dm_note_row(dm, disabled=offline)}</div>'
                elif dm:
                    note = f'<p><span class="text-muted-foreground">If you switch:</span> Mert resolves the 7 open conflicts.</p>'
                elif dm_none_open:
                    note = 'DMNONE'
                else:
                    note = '<p class="flex gap-2">' + icon('circle-alert', 'size-4 mt-0.5 shrink-0 text-muted-foreground') + '<span>Needs a Decision Maker. Choose one when you pick this rule.</span></p>'
            elif key == 'majority':
                if dm_none_open:
                    sel = False
                    note = '<p class="text-muted-foreground">Current rule. Ties stay open because nobody is the Decision Maker.</p>'
                elif sel and dm:
                    note = f'<p class="text-muted-foreground">Current rule. {len(MAJ_FINAL)} conflicts became final. {len(MAJ_OPEN)} wait for the last member.</p>'
                elif sel and not dm:
                    note = f'''<div class="flex gap-2">{icon("circle-alert", "size-4 mt-0.5 shrink-0 text-muted-foreground")}<div><p class="text-label">No Decision Maker, so ties stay open</p><p class="mt-0.5 text-muted-foreground">A tie is when no decision has the most votes. With 3 members, that's when all three choose differently. Ties stay conflicts until someone changes their decision.</p><a href="S34-members.html#S34-default" class="-ml-1 inline-flex h-12 items-center px-1 text-label text-primary underline underline-offset-4" data-action="assign-decision-maker">Assign a Decision Maker</a></div></div>'''
                else:
                    note = f'<p><span class="text-muted-foreground">If you switch:</span> {len(MAJ_FINAL)} of 15 conflicts become final now.</p>'
            else:
                if sel:
                    note = '<p class="text-muted-foreground">Current rule. 15 conflicts wait for members to match.</p>'
                else:
                    note = '<p><span class="text-muted-foreground">If you switch:</span> all 15 conflicts stay open.</p>'
            extra = ''
            if note == 'DMNONE':
                note = ''
                rows = ''.join(f'<li class="flex min-h-14 items-center gap-3 py-1.5">{av(k, "size-8")}<span class="min-w-0 flex-1 text-body">{P[k]["name"]}{" <span class=\"text-muted-foreground\">(you)</span>" if k == viewer else ""}</span>{switch(k == dm_pending, "Decision Maker: " + P[k]["name"], href="#S35-dm-none-confirm")}</li>' for k in ('deniz', 'mert', 'selin'))
                extra = f'''<div class="mt-3 border-t pt-3"><p class="text-label">Choose the Decision Maker first</p><p class="mt-0.5 text-body-sm text-muted-foreground">This rule needs one member to resolve conflicts. Turn on one switch, then confirm the rule.</p>
          <ul class="mt-2 divide-y" aria-label="Decision Maker, one member at a time">{rows}</ul></div>'''
                sel = True
            rt = 'The Decision Maker chooses the final decision.' if (key == 'dm' and dm is None) else None
            cards.append(rule_card(key, sel, note, None if offline else href, action, offline, large, extra, rt))
        foot = f'<p class="px-1 {"text-body-lg" if large else "text-body-sm"} text-muted-foreground">Changing the rule never changes anyone\'s own decisions. Conflicts that are already resolved stay resolved.</p>'
        body = (''.join(cards[1:]) + foot) if (dm_none_open or scrolled) else (intro + example_block(large) + ''.join(cards) + foot)
    else:
        cur = RULES['dm']
        if viewer == 'mert':
            meaning = ('<p class="text-label">What it means for you</p><p class="mt-0.5 text-body-sm text-muted-foreground">You\'re the Decision Maker. When members decide an item differently, you choose its final decision. Members see "Resolved by Mert".</p>'
                       f'<div class="mt-3">{btn("Review 15 conflicts", "primary", "S36-conflicts.html#S36-default", "review-conflicts", ic="git-compare-arrows")}</div>')
        else:
            meaning = '<p class="text-label">What it means for you</p><p class="mt-0.5 text-body-sm text-muted-foreground">Keep deciding on your own. When your decision differs from someone else\'s, the item becomes a conflict and Mert chooses its final decision. You can still change your own decision; if everyone ends up choosing the same, the item is Agreed.</p>'
        current_card = f'''<div class="rounded-tile border-2 border-primary bg-card p-4">
        <div class="flex items-center justify-between gap-2"><p class="text-title-3">{cur["title"]}</p>{icon("gavel", "size-5 shrink-0 text-muted-foreground")}</div>
        <p class="mt-1 text-body-sm text-muted-foreground">{cur["desc"]}</p>
        <p class="mt-3 flex items-center gap-2 text-body-sm">{av("deniz", "size-6")}Chosen by Deniz, the Owner, on Sep 28</p>
        <div class="mt-3 flex items-center gap-3 border-t pt-3">{av("mert", "size-8")}<span class="min-w-0 flex-1"><span class="block text-body">Mert Aydın{" <span class=\"text-muted-foreground\">(you)</span>" if viewer == "mert" else ""}</span><span class="block text-caption text-muted-foreground">Decision Maker</span></span></div>
      </div>'''
        others = ''.join(f'<li class="flex gap-3 px-4 py-3">{icon(RULES[k]["ic"], "size-5 mt-0.5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">{RULES[k]["title"]}</span><span class="mt-0.5 block text-body-sm text-muted-foreground">{RULES[k]["desc"]}</span></span></li>' for k in ('everyone', 'majority'))
        body = (f'<section>{section_label("Current rule")}{current_card}</section>'
                f'<section class="rounded-group bg-card p-4 dark:border">{meaning}</section>'
                f'<section>{section_label("Other rules")}{group(others)}<p class="mt-2 px-1 text-body-sm text-muted-foreground">Only Deniz, the Owner, can change the rule.</p></section>')
    return f'''{hdr}
  {off}{top}
  <div class="min-h-0 flex-1 overflow-hidden"><div class="space-y-4 px-4 pb-6 pt-2">{body}</div></div>
  {overlay}'''

def split_rows(split, large=False):
    t = 'text-title-3 font-normal' if large else 'text-body'
    out = ''
    for k in ('reject', 'maybe', 'accept'):
        ic, verb, state, _ = DEC[k]
        n = split[k]
        tone = f'text-{k}-soft-foreground' if n else 'text-muted-foreground'
        out += f'<li class="flex min-h-10 items-center gap-3"><span class="flex size-7 shrink-0 items-center justify-center rounded-full bg-{k}-soft {tone}">{icon(ic, "size-4")}</span><span class="flex-1 {t}">{verb}</span><span class="{t} tabular-nums">{n}</span></li>'
    return f'<ul class="mt-2" aria-label="Final decisions by type">{out}</ul>'

def build_s35():
    pg = Page('S35', 'Conflict rule settings', 'How a conflict gets its final decision on a shared list: Everyone must agree, Majority decides or Decision Maker decides (DM-06 to DM-09). The Owner chooses; everyone else sees what the rule means for them. Spec: <a href="S35-conflict-rule.md">S35-conflict-rule.md</a>.')
    F = pg.frame
    pg.section('Owner', 'The Owner picks one of three rules. Each option explains itself with the same example item and says what switching does to the 15 open conflicts in Round 1. Switching asks for confirmation with the recalculation.')
    F('S35-default', 'Default: Owner, rule Decision Maker decides', phone(s35_screen()))
    maj_body = f'''<div class="mt-4 rounded-control bg-muted p-4">
        <p class="text-label">{len(MAJ_FINAL)} become final now</p>{split_rows(MAJ_SPLIT)}
        <p class="mt-3 border-t pt-3 text-label">{len(MAJ_OPEN)} stay open</p><p class="mt-0.5 text-body-sm text-muted-foreground">They wait for the last member to decide. Ties go to Mert.</p>
      </div>'''
    F('S35-confirm-majority', 'Switching to Majority decides: recalculation', phone(s35_screen(overlay=dialog(
        'Switch to Majority decides?', f'{len(MAJ_FINAL)} of 15 conflicts get a final decision right away. Members are notified.',
        dbtn('Cancel', href='#S35-default') + dbtn('Switch to Majority', 'primary', '#S35-switched', 'confirm-rule'), maj_body))))
    F('S35-switched', 'Switched: Majority decides, with Undo', phone(s35_screen('majority', scrolled=True, overlay=snackbar(f'Switched to Majority decides. {len(MAJ_FINAL)} conflicts are now final.', 'Undo', icon_name='vote'))))
    ev_body = '''<div class="mt-4 rounded-control bg-muted p-4"><p class="text-label">15 stay open</p><p class="mt-0.5 text-body-sm text-muted-foreground">Mert can no longer resolve them. Each item is final only when Deniz, Mert and Selin choose the same.</p></div>'''
    F('S35-confirm-everyone', 'Switching to Everyone must agree', phone(s35_screen(overlay=dialog(
        'Switch to Everyone must agree?', 'No conflict gets a final decision until members change their decisions to match. Members are notified.',
        dbtn('Cancel', href='#S35-default') + dbtn('Switch to Everyone must agree', 'primary', '#S35-default', 'confirm-rule'), ev_body))))
    F('S35-confirm-dm', 'Switching back to Decision Maker decides (Mert is Decision Maker)', phone(s35_screen('majority', overlay=dialog(
        'Switch to Decision Maker decides?', f'Mert resolves the {len(MAJ_OPEN)} open conflicts and any new ones. The {len(MAJ_FINAL)} conflicts that became final by majority stay final. Members are notified.',
        dbtn('Cancel', href='#S35-switched') + dbtn('Switch to Decision Maker decides', 'primary', '#S35-default', 'confirm-rule')))))
    pg.section('Without a Decision Maker', 'Majority without a Decision Maker leaves ties open. Decision Maker decides cannot work without one, so picking it asks the Owner to choose a member first, with the same switch as Members (S34).')
    F('S35-majority-no-dm', 'Majority decides, nobody is Decision Maker: ties stay open', phone(s35_screen('majority', dm=None)))
    F('S35-dm-none', 'Picking Decision Maker decides with no Decision Maker', phone(s35_screen('majority', dm=None, dm_none_open=True)))
    F('S35-dm-none-confirm', 'Mert switched on: confirm rule and role together', phone(s35_screen('majority', dm=None, dm_none_open=True, dm_pending='mert', overlay=dialog(
        'Make Mert the Decision Maker?', 'The rule changes to Decision Maker decides. Mert resolves the 7 open conflicts and any new ones. Members are notified.',
        dbtn('Cancel', href='#S35-dm-none') + dbtn('Make Mert Decision Maker', 'primary', '#S35-default', 'confirm-rule')))))
    pg.section('Members who are not the Owner', 'Read-only: the current rule, who chose it and what it means for this member. The Decision Maker gets a direct way to the conflicts.')
    F('S35-collaborator', 'Collaborator view (Selin): read-only', phone(s35_screen(viewer='selin')))
    F('S35-decision-maker', 'Decision Maker view (Mert): read-only', phone(s35_screen(viewer='mert')))
    pg.section('States', 'Loading, offline and a change that could not be saved.')
    sk = lambda w: f'<span class="block h-4 {w} animate-pulse rounded-full bg-muted"></span>'
    card_sk = f'<div class="space-y-3 rounded-tile border bg-card p-4"><div class="flex items-center gap-3"><span class="size-6 animate-pulse rounded-full bg-muted"></span>{sk("w-1/2")}</div>{sk("w-full")}{sk("w-3/4")}</div>'
    load = f'''{appbar('Conflict rule', 'back', 'S34-members.html#S34-default', sub='Wedding guests', lead_label='Back to Members')}
  <div class="flex-1 space-y-4 px-4 pt-2" role="status" aria-busy="true" aria-label="Loading conflict rule">{sk("w-full")}{sk("w-2/3")}<div class="h-16 animate-pulse rounded-control bg-muted"></div>{card_sk}{card_sk}{card_sk}</div>'''
    F('S35-loading', 'Loading', phone(load))
    F('S35-offline', 'Offline: rule shown, changes need a connection', phone(s35_screen(offline=True)))
    err_top = f'<div class="px-4 pb-2">{alert("error", "Couldn\'t change the rule", "The rule is still Decision Maker decides. Check your connection and try again.", action=btn("Try again", "secondary", "#S35-confirm-majority", "retry", extra="mt-3", full=False))}</div>'
    F('S35-error', "Change couldn't be saved", phone(s35_screen(top=err_top)))
    pg.section('Accessibility and iOS', 'At 200% text the cards grow and stay stacked. iOS: pushed screen with a back chevron; confirmations are native alerts with the same copy.')
    F('S35-large-text', 'Large text (200%)', phone(s35_screen(large=True)))
    F('S35-ios', 'iOS', phone(s35_screen(ios=True), ios=True))
    ios_alert = f'''<div class="absolute inset-0 z-50 bg-scrim/40"></div>
  <div class="absolute inset-0 z-50 flex items-center justify-center px-12">
    <div class="w-full overflow-hidden rounded-dialog bg-popover text-center shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="ia1" aria-describedby="ia2">
      <div class="px-4 pb-4 pt-5"><h2 id="ia1" class="text-body font-semibold">Switch to Majority decides?</h2><p id="ia2" class="mt-1 text-body-sm">{len(MAJ_FINAL)} of 15 conflicts get a final decision right away: {MAJ_SPLIT["reject"]} Reject, {MAJ_SPLIT["maybe"]} Maybe, {MAJ_SPLIT["accept"]} Accept. {len(MAJ_OPEN)} stay open until the last member decides. Members are notified.</p></div>
      <a href="#S35-ios" class="flex h-12 items-center justify-center border-t text-body font-semibold text-primary" data-action="confirm-rule">Switch to Majority</a>
      <a href="#S35-ios" class="flex h-12 items-center justify-center border-t text-body text-primary">Cancel</a>
    </div>
  </div>'''
    F('S35-ios-confirm', 'iOS: confirmation alert', phone(s35_screen(ios=True, overlay=ios_alert), ios=True))
    pg.write('S35-conflict-rule.html')

# =====================================================================================
# S36 CONFLICTS
# =====================================================================================
ORDER_LABEL = {'deniz': 'Owner', 'mert': 'Decision Maker', 'selin': 'Collaborator'}

def note_box(n, viewer):
    k = UID2K[n['author']]
    private = n['private']
    if private and k != viewer:
        return ''
    who = 'You' if k == viewer else P[k]['first']
    pb = f'<span class="inline-flex items-center gap-1">{icon("lock", "size-3.5")}Only you</span>' if private else ''
    box = 'border border-dashed border-input' if private else 'bg-muted'
    return f'<div class="rounded-control {box} px-3 py-2"><p class="flex items-center gap-1.5 text-caption text-muted-foreground">{av(k, "size-5")}<span class="flex-1">{who}</span>{pb}</p><p class="mt-1 line-clamp-2 text-body-sm">{n["text"]}</p></div>'

def decision_rows(dec, viewer, large=False, highlight=None):
    order = [viewer] + [k for k in ('deniz', 'mert', 'selin') if k != viewer]
    out = ''
    t = 'text-body-lg' if large else 'text-body'
    for k in order:
        you = ' <span class="text-muted-foreground">(you)</span>' if k == viewer else ''
        badge = dbadge(dec.get(k), 'Not decided yet' if (not dec.get(k) and k != viewer) else None)
        if large:
            big = badge.replace('h-7', 'h-9').replace('text-caption', 'text-label-lg').replace('size-4', 'size-5')
            out += f'<li class="flex items-start gap-3 py-2.5">{av(k, "size-10")}<span class="min-w-0 flex-1"><span class="block text-title-3 font-normal">{P[k]["first"]}{you}</span><span class="block text-body-lg text-muted-foreground">{ORDER_LABEL[k]}</span><span class="mt-1.5 flex">{big}</span></span></li>'
            continue
        out += f'<li class="flex min-h-12 items-center gap-3 py-1.5">{av(k, "size-8")}<span class="min-w-0 flex-1"><span class="block truncate {t}">{P[k]["first"]}{you}</span><span class="block text-caption text-muted-foreground">{ORDER_LABEL[k]}</span></span>{badge}</li>'
    return f'<ul class="divide-y" aria-label="Decisions by member">{out}</ul>'

STAMP = {
    'accept': ('left-5 top-6 -rotate-6', 'check'),
    'reject': ('right-5 top-6 rotate-6', 'x'),
    'maybe': ('bottom-16 left-1/2 -translate-x-1/2', 'circle-help'),
}
MOVE = {'accept': 'translate-x-28 rotate-6', 'reject': '-translate-x-28 -rotate-6', 'maybe': '-translate-y-16'}

def card_body(it, viewer='mert', dec=None, extra_notes=(), hint='', status='conflict', status_label=None, large=False, final=None):
    dec = dec or it['dec']
    notes = ''.join(note_box(n, viewer) for n in list(it['notes']) + list(extra_notes))
    if not notes:
        notes = '<p class="text-body-sm text-muted-foreground">No notes on this item.</p>'
    chip = status_chip(status, status_label)
    if final:
        chip = f'<span class="flex flex-wrap gap-1.5">{chip}{dbadge(final)}</span>'
    if it['photo'] and not large:
        head = f'''<img src="{IMG}{it["photo"]}" alt="" class="h-[26%] w-full shrink-0 object-cover">
      <div class="px-6 pt-4"><div class="flex items-start justify-between gap-3"><h2 class="line-clamp-2 text-title-1">{it["name"]}</h2>{chip}</div><p class="mt-0.5 text-body text-muted-foreground">{it["sub"]}</p></div>'''
    elif large:
        head = f'''<div class="px-5 pt-5"><h2 class="text-display">{it["name"]}</h2><p class="mt-1 text-title-3 font-normal text-muted-foreground">{it["sub"]}</p><div class="mt-2">{chip.replace('h-7', 'h-9').replace('text-caption', 'text-label-lg')}</div></div>'''
    else:
        head = f'''<div class="flex items-center gap-4 px-6 pt-6">{item_av(it, "size-16")}<div class="min-w-0 flex-1"><h2 class="line-clamp-2 text-title-1">{it["name"]}</h2><p class="mt-0.5 text-body text-muted-foreground">{it["sub"]}</p></div></div>
      <div class="px-6 pt-3">{chip}</div>'''
    h = f'<div class="mt-3 px-6">{hint}</div>' if hint else ''
    px = 'px-5' if large else 'px-6'
    notes_sec = '' if large else f'<section class="mt-3 {px}"><h3 class="text-label text-muted-foreground">Notes</h3><div class="mt-2 space-y-2">{notes}</div></section>'
    return f'''{head}
      {h}
      <section class="mt-3 {px}"><h3 class="{"text-body-lg" if large else "text-label"} text-muted-foreground">Decisions</h3>{decision_rows(dec, viewer, large)}</section>
      {notes_sec}{'<p class="mt-auto px-5 pb-5 text-body-lg text-primary">1 note in item details</p>' if large and it['notes'] else ''}'''

def ccard(body, label, drag=None, reduced=False, final=True):
    move = '' if not drag or reduced else MOVE[drag]
    shadow = 'shadow-hero-drag' if drag else 'shadow-hero'
    overlay = ''
    if drag:
        pos, ic = STAMP[drag]
        txt = f'Final: {DEC[drag][1]}' if final else DEC[drag][1]
        overlay = f'''<div class="pointer-events-none absolute inset-0 bg-{drag} opacity-25"></div>
      <div class="pointer-events-none absolute {pos} inline-flex h-11 items-center gap-2 rounded-full bg-{drag} px-4 text-label-lg text-{drag}-foreground shadow-overlay">{icon(ic, "size-6")}{txt}</div>'''
    return f'''<!-- Proposed component: ConflictCard (SwipeCard variant with expanded MemberDecisions and notes) -->
    <article class="absolute inset-x-gutter bottom-5 top-0 flex origin-bottom flex-col overflow-hidden rounded-hero bg-card {shadow} {move}" aria-label="{label}" aria-roledescription="card" tabindex="0">
      {body}
      {overlay}
    </article>'''

def cstack(top, next_it=None, z=''):
    behind = ''
    if next_it:
        behind = '<div class="absolute inset-x-gutter bottom-5 top-0 origin-top scale-95 translate-y-10 rounded-hero border bg-card shadow-raised" aria-hidden="true"></div>'
    return f'''<div class="relative mt-2 min-h-0 flex-1 {z}">
    {behind}
    {top}
  </div>'''.replace(' ">', '">')

def s36_header(sub='Wedding guests, Round 1', ios=False, back_href='S09-list-overview.html#S09-shared', list_href='#S36-list', menu_href='#S36-menu', view='cards'):
    toggle_ic, toggle_lbl, toggle_href = ('layers', 'Show as cards', '#S36-default') if view == 'list' else ('list', 'Show as list', list_href)
    if ios:
        return f'''<header class="grid h-11 shrink-0 grid-cols-[1fr_auto_1fr] items-center px-2">
    <a href="{back_href}" class="inline-flex h-12 items-center gap-0.5 justify-self-start text-body text-primary" aria-label="Back to Wedding guests">{icon("chevron-left", "size-6")}Back</a>
    <div class="text-center"><h1 class="text-body font-semibold">Conflicts</h1><p class="text-caption text-muted-foreground">Round 1</p></div>
    <div class="flex justify-end"><a href="{toggle_href}" class="flex size-12 items-center justify-center text-primary" aria-label="{toggle_lbl}">{icon(toggle_ic, "size-6")}</a><a href="{menu_href}" class="flex size-12 items-center justify-center text-primary" aria-label="More options">{icon("ellipsis", "size-6")}</a></div>
  </header>'''
    acts = icon_action(toggle_ic, toggle_lbl, toggle_href, 'toggle-view') + icon_action('ellipsis-vertical', 'More options', menu_href, 'menu')
    return appbar('Conflicts', 'back', back_href, sub=sub, actions=acts, lead_label='Back to Wedding guests')

def s36_progress(done, total, word='resolved', resolve_all=True, extra='', disabled=False, large=False, ra_href='S37-bulk-resolve.html#S37-confirm'):
    pct = 'w-0' if done == 0 else ('w-full' if done >= total else f'w-[{round(done * 100 / total)}%]')
    ra = ''
    if resolve_all:
        if disabled:
            ra = f'<button class="-my-2 -mr-2 inline-flex h-12 shrink-0 items-center gap-1.5 rounded-control px-3 text-label text-primary opacity-50" disabled>{icon("gavel", "size-4")}Resolve all</button>'
        else:
            ra = f'<a href="{ra_href}" class="-my-2 -mr-2 inline-flex h-12 shrink-0 items-center gap-1.5 rounded-control px-3 text-label text-primary" data-action="resolve-all">{icon("gavel", "size-4")}Resolve all</a>'
    t = 'text-title-3' if large else 'text-label'
    return f'''<div class="shrink-0 px-gutter pb-1">
    <div class="flex min-h-8 items-center justify-between gap-3"><span class="{t} tabular-nums">{done} / {total} {word}</span>{extra}{ra}</div>
    <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="{done}" aria-valuemin="0" aria-valuemax="{total}" aria-label="{done} of {total} conflicts {word}"><div class="h-full {pct} rounded-full bg-primary"></div></div>
  </div>'''

def cbtn(kind, state='rest', large=False, lbl_override=None, prefix='Final decision: '):
    ic, verb, _, _ = DEC[kind]
    cls = {'rest': f'bg-{kind}-soft text-{kind}-soft-foreground',
           'armed': f'bg-{kind} text-{kind}-foreground ring-4 ring-{kind}/25',
           'mine': f'bg-{kind} text-{kind}-foreground'}[state]
    pressed = ' aria-pressed="true"' if state == 'mine' else ''
    return f'<button class="flex min-w-touch flex-col items-center gap-1.5" aria-label="{prefix}{verb}" data-action="{kind}"{pressed}><span class="flex size-16 items-center justify-center rounded-full {cls}">{icon(ic, "size-7")}</span><span class="text-caption">{lbl_override or verb}</span></button>'

def s36_bar(mode='dm', armed=None, mine=None, caption=None, undo=True, undo_label='Undo last resolution (Accept on Mehmet Yılmaz)', disabled=False, hide_caption=False):
    if mode == 'dm':
        cap = caption or f'{icon("gavel", "size-4 shrink-0")}Your choice is the final decision'
        prefix = 'Final decision: '
    else:
        cap = caption
        prefix = 'My decision: '
    st = lambda k: 'armed' if armed == k else ('mine' if mine == k else 'rest')
    uattr = '' if undo else ' disabled'
    uop = '' if undo else ' opacity-40'
    bar = f'''<div class="flex shrink-0 items-start justify-between px-5 pb-4 pt-1">
    <button class="flex min-w-touch flex-col items-center gap-1.5{uop}" aria-label="{undo_label if undo else "Nothing to undo"}" data-action="undo"{uattr}><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("undo-2")}</span><span class="text-caption text-muted-foreground">Undo</span></button>
    {cbtn('reject', st('reject'), prefix=prefix)}
    {cbtn('maybe', st('maybe'), prefix=prefix)}
    {cbtn('accept', st('accept'), prefix=prefix)}
    <a href="#S36-note" class="flex min-w-touch flex-col items-center gap-1.5" aria-label="Add note" data-action="note"><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("sticky-note")}</span><span class="text-caption text-muted-foreground">Note</span></a>
  </div>'''
    if disabled:
        bar = bar.replace('<button class="flex min-w-touch', '<button disabled class="opacity-40 flex min-w-touch')
    inv = ' invisible' if hide_caption else ''
    return f'<p class="flex shrink-0 items-center justify-center gap-1.5 px-gutter pt-2 text-center text-body-sm text-muted-foreground{inv}"{" aria-hidden=\"true\"" if hide_caption else ""}>{cap}</p>{bar}'

def item_label(it, viewer='mert'):
    return f'{it["name"]}, {it["sub"]}. Conflict. {dec_text(it["dec"], viewer)}'

def s36_screen(cid='c002', next_cid='c012', done=0, total=15, viewer='mert', mode='dm', drag=None, reduced=False, overlay='', top='', hint='',
               dec=None, extra_notes=(), status='conflict', status_label=None, mine=None, caption=None, resolve_all=True, word='resolved',
               prog=None, hdr=None, undo=True, undo_label='Undo last resolution (Accept on Mehmet Yılmaz)', disabled=False, final=None):
    it = item(cid)
    body = card_body(it, viewer, dec, extra_notes, hint, status, status_label, final=final)
    snack = 'bottom-28' in overlay
    if hdr is None:
        hdr = s36_header(back_href='S09-list-overview.html#S09-shared-decision-maker' if viewer == 'mert' else 'S09-list-overview.html#S09-shared')
    nxt = item(next_cid) if next_cid else None
    return f'''{hdr}
  {top}
  {prog or s36_progress(done, total, word, resolve_all and mode == 'dm', disabled=disabled)}
  {cstack(ccard(body, item_label(it, viewer), drag, reduced, mode == 'dm'), nxt)}
  {s36_bar(mode, drag, mine, caption, undo, undo_label, disabled, snack)}
  {overlay}'''

def dec_sentence(dec, viewer):
    verbs = {'accept': 'accepted', 'reject': 'rejected', 'maybe': 'chose Maybe'}
    groups = {}
    for k in ('deniz', 'mert', 'selin'):
        groups.setdefault(dec.get(k), []).append('you' if k == viewer else P[k]['first'])
    parts = []
    for d in ('accept', 'reject', 'maybe', None):
        if d in groups:
            names = ' and '.join(groups[d])
            parts.append(f"{names} {verbs[d]}" if d else f"{names} {'haven' if names == 'you' else 'hasn'}'t decided")
    t = ', '.join(parts)
    return t[0].upper() + t[1:]

def list_row(cid, viewer='mert', resolved=None, href='#S36-default', big=False):
    it = item(cid)
    if resolved:
        trail = dbadge(resolved, DEC[resolved][1])
        meta = f'<span class="text-body-sm text-muted-foreground">Resolved by {"you" if viewer == "mert" else "Mert"}</span>'
    else:
        trail = icon('chevron-right', 'size-5 shrink-0 text-muted-foreground')
        meta = f'<span class="line-clamp-2 text-body-sm text-muted-foreground">{dec_sentence(it["dec"], viewer)}</span>'
    return f'<li><a href="{href}" class="flex min-h-16 items-center gap-3 px-4 py-2.5">{item_av(it)}<span class="min-w-0 flex-1"><span class="block truncate text-body">{it["name"]}</span><span class="mt-0.5 block">{meta}</span></span>{trail}</a></li>'

def build_s36():
    pg = Page('S36', 'Conflicts: one-by-one resolution', 'Swipe through conflicts with every member\'s decision and notes on the card. The Decision Maker sets the final decision with the same gestures and buttons as sorting (S25); other members see what is open and can change their own decision. Spec: <a href="S36-conflicts.md">S36-conflicts.md</a>.')
    F = pg.frame
    pg.section('Decision Maker: one by one', 'Mert is the Decision Maker under the rule Decision Maker decides. Right = Accept, left = Reject, up = Maybe, like sorting, but the result is the final decision. "Resolve all" applies his earlier decisions in one step (S37).')
    hint012 = alert('neutral', "You haven't decided this item", 'Resolve all skips it, so decide it here. Selin left a note.', 'circle-dashed')
    F('S36-default', 'Default: Decision Maker, first conflict (Mehmet Yılmaz)', phone(s36_screen(undo=False)))
    F('S36-drag-accept', 'Dragging right, armed: release to make Accept final', phone(s36_screen(drag='accept', undo=False)))
    F('S36-drag-reject', 'Dragging left, armed: release to make Reject final', phone(s36_screen(drag='reject', undo=False)))
    F('S36-resolved', 'Resolved: snackbar with Undo, next conflict on top', phone(s36_screen('c012', 'c015', 1, hint=hint012, overlay=snackbar('Resolved: Accept for Mehmet Yılmaz', 'Undo', bottom='bottom-28', icon_name='gavel', href='#S36-default', action_name='undo')).replace('Undo last resolution (Accept on Mehmet Yılmaz)', 'Undo last resolution (Accept on Mehmet Yılmaz)')))
    F('S36-dm-undecided', 'Conflict on an item Mert never decided (Gülşen Aydın)', phone(s36_screen('c012', 'c015', 1, hint=hint012)))
    hint020 = '<p class="flex gap-2 text-body-sm text-muted-foreground">' + icon('clock', 'size-4 mt-0.5 shrink-0') + '<span>Selin hasn\'t decided yet. Your choice is final either way; her decision is still recorded.</span></p>'
    F('S36-progress', '3 / 15 resolved: a conflict while one member is still sorting (Merve Kurt)', phone(s36_screen('c020', 'c029', 3, hint=hint020, undo_label='Undo last resolution (Reject on Cem Tekin)')))
    note_sheet = f'''<div class="absolute inset-0 z-40 bg-scrim/50"></div>
  <div class="absolute inset-x-0 bottom-0 z-40 rounded-t-sheet bg-popover px-gutter pb-6 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="ns36">
    {handle()}
    <div class="flex items-center justify-between pt-2"><h2 id="ns36" class="text-title-3">Note on Merve Kurt</h2><a href="#S36-progress" class="-mr-3 flex size-12 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</a></div>
    <label for="note36" class="sr-only">Note</label>
    <textarea id="note36" rows="3" class="mt-3 w-full resize-none rounded-control border border-primary bg-card px-3.5 py-3 text-body ring-2 ring-ring/30">Ask Deniz how close they are now.</textarea>
    <div class="mt-1 flex justify-end"><span class="text-caption tabular-nums text-muted-foreground">33 / 1,000</span></div>
    <div class="mt-2 flex min-h-14 items-center gap-4"><span class="min-w-0 flex-1"><span class="block text-body">Only visible to me</span><span class="block text-body-sm text-muted-foreground">Deniz and Selin won't see this note.</span></span>{switch(True, "Only visible to me")}</div>
    {btn("Save note", "primary", "#S36-note-saved", "save-note", extra="mt-3")}
  </div>'''
    F('S36-note', 'Adding a private note while resolving', phone(s36_screen('c020', 'c029', 3, overlay=note_sheet)))
    mnote = [dict(itemId='c020', author='u-mert', text='Ask Deniz how close they are now.', private=True)]
    F('S36-note-saved', 'Private note on the card: only the author sees it', phone(s36_screen('c020', 'c029', 3, extra_notes=mnote, overlay=snackbar('Note saved', bottom='bottom-28'))))
    menu = f'''<div class="absolute right-2 top-14 z-40 w-72 overflow-hidden rounded-control bg-popover py-1.5 shadow-overlay" role="menu" aria-label="Conflict options">
    <a href="#S36-resolved" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body" data-action="skip">{icon("skip-forward", "size-5 text-muted-foreground")}Skip for now</a>
    <a href="S26-item-detail.html#S26-shared-conflict" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body">{icon("panel-bottom-open", "size-5 text-muted-foreground")}Open item details</a>
    <a href="#S36-list" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body">{icon("list", "size-5 text-muted-foreground")}Show as list</a>
    <div class="my-1.5 h-px bg-border"></div>
    <a href="S35-conflict-rule.html#S35-decision-maker" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body">{icon("git-compare-arrows", "size-5 text-muted-foreground")}Conflict rule</a>
  </div>'''
    F('S36-menu', 'Overflow menu', phone(s36_screen(overlay=menu, undo=False)))
    resolved3 = [('c002', 'accept'), ('c012', 'reject'), ('c015', 'reject')]
    open_rows = ''.join(list_row(c, href='#S36-progress' if c == 'c020' else '#S36-default') for c in CONFLICTS if c not in dict(resolved3))
    res_rows = ''.join(list_row(c, resolved=d) for c, d in resolved3)
    listv = f'''{s36_header(view='list')}
  {s36_progress(3, 15)}
  <div class="min-h-0 flex-1 overflow-hidden"><div class="space-y-5 px-4 pb-6 pt-3">
    <section>{section_label("Open, 12")}{group(open_rows)}</section>
    <section>{section_label("Resolved, 3")}{group(res_rows)}</section>
  </div></div>'''
    F('S36-list', 'Conflicts as a list (alternative view)', phone(listv))
    done = f'''{s36_header()}
  {s36_progress(15, 15, resolve_all=False)}
  <div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
    <span class="flex size-14 items-center justify-center rounded-full bg-secondary text-secondary-foreground">{icon("check-check", "size-6")}</span>
    <h2 class="text-balance mt-4 text-title-2">All 15 conflicts resolved</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">Each one has a final decision. New conflicts show up here as Deniz and Selin keep sorting.</p>
    <div class="mt-6 w-full max-w-xs space-y-2">{btn("See results", "primary", "S28-results.html#S28-shared-resolved", "see-results")}{btn("Export", "outline", "S39-export.html#S39-shared", "export")}{btn("Back to list", "ghost", "S09-list-overview.html#S09-shared-decision-maker", "done")}</div>
  </div>'''
    F('S36-remaining', 'After Resolve all: 3 open conflicts Mert never decided', phone(s36_screen('c012', 'c034', 0, total=3, hint=hint012, undo=False,
        prog=s36_progress(0, 3, resolve_all=False))))
    F('S36-all-resolved', 'All resolved', phone(done))

    pg.section('Other rules and members', 'What members who are not resolving see, and how the screen works under the other two rules. Members always see every decision and the shared notes, and can change their own decision.')
    cap_non = f'Your decision: Accept. Mert decides the final decision.'
    nondm_top = f'<div class="shrink-0 px-4 pb-2">{alert("info", "Mert decides conflicts", "You can still change your own decision. If everyone chooses the same, the item is Agreed.", "gavel")}</div>'
    F('S36-non-dm', 'Member under Decision Maker decides (Deniz): read-only explanation', phone(s36_screen('c002', 'c012', 0, viewer='deniz', mode='member', mine='accept', caption=cap_non, top=nondm_top, word='resolved by Mert', undo=False)))
    ev_hint = '<p class="flex gap-2 text-body-sm text-muted-foreground">' + icon('users', 'size-4 mt-0.5 shrink-0') + '<span>Final only when all three match. Mert chose Accept; you and Selin chose Maybe.</span></p>'
    F('S36-everyone', 'Everyone must agree: Deniz reviews (Sinan Karakaya)', phone(s36_screen('c043', 'c049', 0, viewer='deniz', mode='member', mine='maybe', hint=ev_hint,
        caption='Your decision: Maybe. Change it to match the others.', word='agreed', undo=False)))
    F('S36-everyone-drag', 'Everyone must agree: Deniz drags right to change her own decision (no "Final")', phone(s36_screen('c043', 'c049', 0, viewer='deniz', mode='member', mine='maybe', hint=ev_hint, drag='accept',
        caption='Release to change your decision to Accept.', word='agreed', undo=False)))
    agreed_dec = dict(item('c029')['dec']); agreed_dec['selin'] = 'accept'
    F('S36-everyone-agreed', 'Everyone must agree: Selin changes to Accept, item is Agreed (Murat Ekinci)', phone(s36_screen('c029', 'c037', 1, viewer='selin', mode='member', mine='accept', dec=agreed_dec, status='agreed', status_label='Agreed', final='accept',
        caption='Your decision: Accept. Everyone chose the same.', word='agreed', undo_label='Undo my change (Maybe to Accept on Murat Ekinci)',
        overlay=snackbar('Murat Ekinci is now Agreed: Accept', bottom='bottom-28', icon_name='check-check'))))
    maj_hint = '<p class="flex gap-2 text-body-sm text-muted-foreground">' + icon('clock', 'size-4 mt-0.5 shrink-0') + '<span>Waiting for 1 member: Selin. Accept or Reject from her makes the majority final. Maybe makes it a tie, and Mert decides.</span></p>'
    F('S36-majority', 'Majority decides: waiting for 1 member (Merve Kurt)', phone(s36_screen('c020', 'c060', 0, total=7, viewer='deniz', mode='member', mine='reject', hint=maj_hint,
        status='conflict', caption='Your decision: Reject. The majority decides once everyone has.', word='final', undo=False)))
    tie_dec = dict(item('c020')['dec']); tie_dec['selin'] = 'maybe'
    tie_hint = '<p class="flex gap-2 text-body-sm text-muted-foreground">' + icon('vote', 'size-4 mt-0.5 shrink-0') + '<span>Tie: one Reject, one Maybe, one Accept. As Decision Maker, you break it.</span></p>'
    F('S36-majority-tie', 'Majority decides: a tie goes to the Decision Maker', phone(s36_screen('c020', 'c060', 0, total=1, dec=tie_dec, hint=tie_hint, status_label='Tie', word='ties resolved', undo=False)))

    pg.section('States', 'Empty, loading, error and offline. Resolutions are written on the phone first and synced; conflicts can change during sync.')
    empty = f'''{s36_header()}
  <div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
    {icon("git-compare-arrows", "size-8 text-muted-foreground")}
    <h2 class="text-balance mt-4 text-title-3">No conflicts</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">When members decide an item differently, it shows up here. 15 items in Round 1 are still waiting for your decision.</p>
    <div class="mt-6 w-full max-w-xs space-y-2">{btn("Continue sorting", "primary", "S25-sorting.html#S25-web-desktop", "continue-sorting")}{btn("Back to list", "ghost", "S09-list-overview.html#S09-shared-decision-maker")}</div>
  </div>'''
    F('S36-empty', 'No conflicts', phone(empty))
    load = f'''{s36_header()}
  <div class="shrink-0 px-gutter pb-1" aria-hidden="true"><span class="block h-4 w-28 animate-pulse rounded-full bg-muted"></span><div class="mt-2 h-1.5 rounded-full bg-muted"></div></div>
  <div class="relative mt-2 min-h-0 flex-1" role="status" aria-busy="true" aria-label="Loading conflicts">
    <div class="absolute inset-x-gutter bottom-5 top-0 flex flex-col gap-4 overflow-hidden rounded-hero bg-card p-6 shadow-hero">
      <div class="flex items-center gap-4"><span class="size-16 animate-pulse rounded-full bg-muted"></span><span class="block h-6 w-1/2 animate-pulse rounded-full bg-muted"></span></div>
      {''.join('<div class="flex items-center gap-3"><span class="size-8 animate-pulse rounded-full bg-muted"></span><span class="block h-4 flex-1 animate-pulse rounded-full bg-muted"></span><span class="block h-7 w-24 animate-pulse rounded-full bg-muted"></span></div>' for _ in range(3))}
    </div>
  </div>
  {s36_bar(undo=False, disabled=True)}'''
    F('S36-loading', 'Loading', phone(load))
    err = f'''{s36_header()}
  <div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
    {icon("cloud-alert", "size-8 text-muted-foreground")}
    <h2 class="text-balance mt-4 text-title-3">Conflicts couldn't be loaded</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">SwipeSort didn't respond. Check your connection and try again.</p><p class="mt-3 max-w-xs text-balance text-body-sm text-muted-foreground">Your resolutions are saved on this phone.</p>
    <div class="mt-6 w-full max-w-xs space-y-2">{btn("Try again", "secondary", action="try-again")}{btn("Back to list", "ghost", "S09-list-overview.html#S09-shared-decision-maker", "back")}</div>
  </div>'''
    F('S36-error', 'Error', phone(err))
    unsynced = f'<span class="inline-flex items-center gap-1.5 text-caption text-muted-foreground">{icon("cloud-off", "size-4")}2 not synced</span>'
    F('S36-offline', 'Offline: resolutions saved on the phone', phone(s36_screen('c020', 'c029', 3, top=offline_banner("You're offline. Resolutions are saved on this phone and sync when you're back online."),
        prog=s36_progress(3, 15, extra=unsynced, disabled=True), hint=hint020)))
    sync_sheet = f'''<div class="absolute inset-0 z-40 bg-scrim/50"></div>
  <div class="absolute inset-x-0 bottom-0 z-40 rounded-t-sheet bg-popover px-gutter pb-5 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="sy36">
    {handle()}
    <h2 id="sy36" class="pt-2 text-title-3">Synced 2 resolutions</h2>
    <p class="mt-1 text-body text-muted-foreground">While you were offline, the conflicts changed.</p>
    <ul class="mt-3 divide-y border-y">
      <li class="flex items-center gap-3 py-3">{item_av(item("c059"))}<span class="min-w-0 flex-1"><span class="block text-body">Sophie Laurent</span><span class="block text-body-sm text-muted-foreground">Selin changed to Accept, so everyone agrees. No longer a conflict.</span></span>{status_chip("agreed")}</li>
      <li class="flex items-center gap-3 py-3"><span class="flex size-10 shrink-0 items-center justify-center rounded-full bg-conflict text-conflict-foreground">{icon("git-compare-arrows")}</span><span class="min-w-0 flex-1"><span class="block text-body">2 new conflicts</span><span class="block text-body-sm text-muted-foreground">Selin kept sorting. They're added to the end.</span></span>{status_chip("conflict", "2")}</li>
    </ul>
    {btn("Continue resolving", "primary", "#S36-progress", "continue", extra="mt-5")}
  </div>'''
    F('S36-synced', 'Back online: conflicts changed during sync', phone(s36_screen('c020', 'c029', 3, total=16, overlay=sync_sheet)))

    pg.section('Accessibility', 'At 200% text the card shows the name, the status and the decisions only (notes move to item details) and the buttons become a labeled grid. Reduced motion: no tilt or fly-out; tint and stamp still show.')
    lt_body = card_body(item('c002'), 'mert', large=True)
    big_bar = f'''<p class="shrink-0 px-gutter pt-2 text-center text-body-lg text-muted-foreground">Your choice is the final decision</p>
  <div class="grid shrink-0 grid-cols-3 gap-2 px-4 pb-3 pt-2">
    <button class="flex min-h-16 flex-col items-center justify-center gap-1 rounded-control bg-reject-soft px-2 py-2 text-reject-soft-foreground" aria-label="Final decision: Reject" data-action="reject">{icon("x", "size-7")}<span class="text-title-3">Reject</span></button>
    <button class="flex min-h-16 flex-col items-center justify-center gap-1 rounded-control bg-maybe-soft px-2 py-2 text-maybe-soft-foreground" aria-label="Final decision: Maybe" data-action="maybe">{icon("circle-help", "size-7")}<span class="text-title-3">Maybe</span></button>
    <button class="flex min-h-16 flex-col items-center justify-center gap-1 rounded-control bg-accept-soft px-2 py-2 text-accept-soft-foreground" aria-label="Final decision: Accept" data-action="accept">{icon("check", "size-7")}<span class="text-title-3">Accept</span></button>
  </div>'''
    big_hdr = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="S09-list-overview.html#S09-shared" class="flex size-12 items-center justify-center rounded-full" aria-label="Back to Wedding guests">{icon("arrow-left", "size-7")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">Conflicts</h1>
    <a href="#S36-menu" class="flex size-12 items-center justify-center rounded-full" aria-label="More options, including Resolve all, Undo and Add note">{icon("ellipsis-vertical", "size-7")}</a>
  </header>'''
    F('S36-large-text', 'Large text (200%)', phone(f'''{big_hdr}
  {s36_progress(0, 15, resolve_all=False, large=True)}
  {cstack(ccard(lt_body, item_label(item("c002"))), item("c012"))}
  {big_bar}'''))
    F('S36-reduced-motion', 'Reduced motion: no tilt, stamp and tint still show', phone(s36_screen(drag='accept', reduced=True, undo=False)))

    pg.section('iOS and web', 'iOS: pushed screen with back chevron, UIMenu for options, page sheet for notes. Web desktop: phone layout centered with the same keyboard keys as sorting.')
    F('S36-ios', 'iOS', phone(s36_screen(hdr=s36_header(ios=True, back_href='S09-list-overview.html#S09-shared-decision-maker'), undo=False), ios=True))
    hints = f'<div class="flex shrink-0 justify-center gap-3 pb-3 text-caption text-muted-foreground" aria-label="Keyboard shortcuts">{kbd("←", "Reject")}{kbd("↑", "Maybe")}{kbd("→", "Accept")}{kbd("Z", "Undo")}{kbd("N", "Note")}</div>'
    F('S36-web-desktop', 'Web, desktop: Mert resolves with the keyboard', desktop('swipesort.app/l/7Hq2xK/conflicts', s36_screen(undo=False) + hints))
    pg.write('S36-conflicts.html')

# =====================================================================================
# S37 BULK RESOLVE
# =====================================================================================
def open_item_rows(cids, href='S36-conflicts.html#S36-remaining', big=False):
    out = ''
    t = 'text-title-3 font-normal' if big else 'text-body'
    for c in cids:
        it = item(c)
        sub = '' if big else f'<span class="block text-body-sm text-muted-foreground">{it["sub"]}</span>'
        bd = dbadge(None).replace('h-7', 'h-9').replace('text-caption', 'text-label-lg') if big else dbadge(None)
        out += f'<li class="flex min-h-14 flex-wrap items-center gap-3 py-2">{item_av(it)}<span class="min-w-0 flex-1"><span class="block {"" if big else "truncate"} {t}">{it["name"]}</span>{sub}</span>{bd}</li>'
    return f'<ul class="divide-y" aria-label="Conflicts that stay open">{out}</ul>'

def confirm_sheet(state='ok', large=False, ios=False):
    t = uid('cf')
    split = split_rows(BULK, large)
    b = 'text-title-3 font-normal' if large else 'text-body'
    lb = 'text-title-3' if large else 'text-label'
    if state == 'busy':
        primary = btn('Resolving…', 'primary', busy=True, size='h-14')
    elif state == 'offline':
        primary = btn(f'Resolve {len(MERT_DECIDED)} conflicts', 'primary', disabled=True, size='h-14')
    else:
        primary = btn(f'Resolve {len(MERT_DECIDED)} conflicts', 'primary', '#S37-summary', 'confirm-resolve', size='h-14')
    cancel = btn('Cancel', 'ghost', 'S36-conflicts.html#S36-default', 'cancel') if state != 'offline' else btn('Resolve one by one', 'ghost', 'S36-conflicts.html#S36-default', 'one-by-one')
    off = ''
    if state == 'offline':
        off = f'<div class="mb-3 mt-3">{alert("neutral", "Resolve all needs a connection", "It uses everyone\'s latest decisions, so it can\'t run offline. You can still resolve conflicts one by one; they sync later.", "wifi-off")}</div>'
    busy = ''
    if state == 'busy':
        busy = f'<p class="sr-only" role="status">Resolving {len(MERT_DECIDED)} conflicts</p>'
    title = f'Resolve {len(MERT_DECIDED)} conflicts with your decisions?'
    body = f'''{off}<p class="mt-1 {b} text-muted-foreground">15 conflicts are open. You decided {len(MERT_DECIDED)} of them while sorting; your decision becomes the final decision. Members see "Resolved by Mert".</p>
    <div class="mt-4 rounded-group border bg-card p-4">
      <p class="flex items-center gap-2 {lb}">{icon("gavel", "size-4")}{len(MERT_DECIDED)} will be resolved</p>{split}
    </div>
    <div class="mt-3 rounded-group border bg-card px-4 pb-2 pt-4">
      <p class="flex items-center gap-2 {lb}">{icon("circle-dashed", "size-4")}{len(MERT_UNDECIDED)} stay open</p>
      <p class="mt-0.5 {"text-body-lg" if large else "text-body-sm"} text-muted-foreground">You haven't decided these items. Decide them one by one afterwards.</p>
      {open_item_rows(MERT_UNDECIDED, big=large)}
    </div>
    {busy}'''
    if ios:
        return f'''<div class="absolute inset-0 z-40 bg-scrim/40"></div>
  <div class="absolute inset-x-0 bottom-0 top-14 z-40 flex flex-col rounded-t-sheet bg-popover shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="{t}">
    <div class="flex justify-center py-1.5"><span class="h-1 w-9 rounded-full bg-muted-foreground/40"></span></div>
    <div class="grid shrink-0 grid-cols-[1fr_auto_1fr] items-center px-3"><a href="S36-conflicts.html#S36-ios" class="inline-flex h-12 items-center justify-self-start px-1 text-body text-primary">Cancel</a><span class="text-body font-semibold">Resolve all</span><span></span></div>
    <div class="min-h-0 flex-1 overflow-hidden px-5 pt-2"><h2 id="{t}" class="text-title-2">{title}</h2>{body}</div>
    <div class="shrink-0 px-5 pb-4 pt-3">{primary}</div>
  </div>'''
    return f'''<div class="absolute inset-0 z-40 bg-scrim/50"></div>
  <div class="absolute inset-x-0 bottom-0 top-10 z-40 flex flex-col rounded-t-sheet bg-popover shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="{t}">
    {handle()}
    <div class="min-h-0 flex-1 overflow-hidden px-gutter pt-2"><h2 id="{t}" class="{"text-title-1" if large else "text-title-2"}">{title}</h2>{body}</div>
    <div class="shrink-0 space-y-1 px-gutter pb-4 pt-3">{primary}{cancel}</div>
  </div>'''

def summary_screen(state='ok', large=False):
    t = 'text-body-lg' if large else 'text-body'
    if state == 'error':
        head = f'''<span class="flex size-14 items-center justify-center rounded-full bg-secondary text-secondary-foreground">{icon("gavel", "size-6")}</span>
      <h2 class="mt-4 text-balance text-title-1">Resolved 9 of 12 conflicts</h2>
      <p class="mt-1 text-balance {t} text-muted-foreground">Deniz and Selin are notified.</p>'''
        err = f'<div class="mt-5 text-left">{alert("error", "3 conflicts couldn\'t be resolved", "The connection dropped while saving. Your decisions on them are safe. Try again to resolve them.", action=btn("Try again", "secondary", "#S37-summary", "retry", extra="mt-3", full=False))}</div>'
        split = {'reject': 5, 'maybe': 0, 'accept': 4}
    else:
        head = f'''<span class="flex size-14 items-center justify-center rounded-full bg-secondary text-secondary-foreground">{icon("gavel", "size-6")}</span>
      <h2 class="mt-4 text-balance {"text-display" if large else "text-title-1"}">Resolved {len(MERT_DECIDED)} conflicts</h2>
      <p class="mt-1 text-balance {t} text-muted-foreground">Your decisions are now final. Deniz and Selin are notified.</p>'''
        err = ''
        split = BULK
    rows = split_rows(split, large)
    open_sec = f'''<section class="mt-6 text-left">{section_label(f"{len(MERT_UNDECIDED)} still open")}
      <div class="rounded-group bg-card px-4 dark:border">{open_item_rows(MERT_UNDECIDED, big=large)}</div></section>'''
    actions = f'''<div class="shrink-0 space-y-2 px-gutter pb-4 pt-3">
    {btn(f"Review {len(MERT_UNDECIDED) + (3 if state == 'error' else 0)} open conflicts", "primary", "S36-conflicts.html#S36-remaining", "review-open", size="h-14")}
    <div class="grid grid-cols-2 gap-2">{btn("Export", "outline", "S39-export.html#S39-shared", "export")}{btn("Done", "ghost", "S09-list-overview.html#S09-shared-decision-maker", "done")}</div>
  </div>'''
    hdr = f'''<header class="flex min-h-16 shrink-0 items-center justify-between gap-1 px-1">
    <a href="S09-list-overview.html#S09-shared-decision-maker" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close" data-action="close">{icon("x", "size-6")}</a>
    <a href="#S37-undo" class="inline-flex h-12 items-center rounded-control px-4 text-label-lg" data-action="undo">Undo</a>
  </header>'''
    return f'''{hdr}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter">
    <div class="flex flex-col items-center pt-4 text-center">{head}</div>
    {err}
    <div class="mt-5 rounded-group bg-card px-4 py-3 dark:border">{rows}</div>
    {open_sec}
  </div>
  {actions}'''

def build_s37():
    pg = Page('S37', 'Bulk resolve: confirmation and summary', 'The Decision Maker applies their own earlier decisions to every open conflict in the current round in one action (DM-11). Conflicts on items they never decided stay open, and both the confirmation and the summary say how many (DM-12). Spec: <a href="S37-bulk-resolve.md">S37-bulk-resolve.md</a>.')
    F = pg.frame
    pg.section('Entry and confirmation', 'Mert reaches bulk resolve from the conflicts screen ("Resolve all") or from the list overview\'s conflicts row, where only the Decision Maker sees this choice.')
    entry_opts = f'''<ul class="divide-y overflow-hidden rounded-group bg-card dark:border">
      <li><a href="S36-conflicts.html#S36-default" class="flex min-h-16 items-start gap-4 px-4 py-4" data-action="one-by-one">{icon("layers", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">Resolve one by one</span><span class="mt-0.5 block text-body-sm text-muted-foreground">See every member's decision and notes, then choose the final decision for each item.</span></span>{icon("chevron-right", "size-5 mt-0.5 shrink-0 text-muted-foreground")}</a></li>
      <li><a href="#S37-confirm" class="flex min-h-16 items-start gap-4 px-4 py-4" data-action="resolve-all">{icon("gavel", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">Resolve all with my decisions</span><span class="mt-0.5 block text-body-sm text-muted-foreground">Your decision from sorting becomes final on the {len(MERT_DECIDED)} items you decided. {len(MERT_UNDECIDED)} stay open.</span></span>{icon("chevron-right", "size-5 mt-0.5 shrink-0 text-muted-foreground")}</a></li>
    </ul>'''
    entry = f'''{appbar('Resolve conflicts', 'back', 'S09-list-overview.html#S09-shared-decision-maker', sub='Wedding guests, Round 1', lead_label='Back to Wedding guests')}
  <div class="min-h-0 flex-1 overflow-hidden"><div class="space-y-5 px-4 pb-6 pt-2">
    <section class="px-1"><p class="text-title-2">15 conflicts need your decision</p><p class="mt-1 text-body text-muted-foreground">You're the Decision Maker, so you choose the final decision when members disagree.</p></section>
    <section class="rounded-group bg-card p-4 dark:border">
      <p class="text-label">Your earlier decisions on these items</p>
      {split_rows(BULK)}
      <div class="mt-1 flex min-h-10 items-center gap-3 border-t pt-2"><span class="flex size-7 shrink-0 items-center justify-center rounded-full bg-muted text-muted-foreground">{icon("circle-dashed", "size-4")}</span><span class="flex-1 text-body">Not decided</span><span class="text-body tabular-nums">{len(MERT_UNDECIDED)}</span></div>
    </section>
    {entry_opts}
    <p class="px-1 text-body-sm text-muted-foreground">Either way, you can change a final decision later in Results.</p>
  </div></div>'''
    F('S37-default', 'Entry: how bulk resolve works (Decision Maker only)', phone(entry))
    bg = s36_screen(undo=False)
    F('S37-confirm', 'Confirmation: 12 resolved with your decisions, 3 stay open', phone(bg + confirm_sheet()))
    F('S37-resolving', 'Resolving', phone(bg + confirm_sheet('busy')))
    F('S37-summary', 'Summary: Resolved 12 conflicts', phone(summary_screen()))
    pg.section('Edge cases', 'Nothing to resolve, partial failure, undo, offline and members without the role.')
    nothing_sheet = f'''<div class="absolute inset-0 z-40 bg-scrim/50"></div>
  <div class="absolute inset-x-0 bottom-0 z-40 rounded-t-sheet bg-popover px-gutter pb-4 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="nt37">
    {handle()}
    <h2 id="nt37" class="pt-2 text-title-2">Nothing to resolve with your decisions</h2>
    <p class="mt-1 text-body text-muted-foreground">You haven't decided any of the 3 open conflicts, so there's no decision of yours to apply. Decide them one by one.</p>
    <div class="mt-4 rounded-group border bg-card px-4">{open_item_rows(MERT_UNDECIDED)}</div>
    <div class="mt-4 space-y-1">{btn("Review 3 open conflicts", "primary", "S36-conflicts.html#S36-remaining", "review-open", size="h-14")}{btn("Cancel", "ghost", "S36-conflicts.html#S36-remaining")}</div>
  </div>'''
    bg3 = s36_screen('c012', 'c034', 0, total=3, prog=s36_progress(0, 3, resolve_all=False), hint=alert('neutral', "You haven't decided this item", 'Resolve all skips it, so decide it here. Selin left a note.', 'circle-dashed'))
    F('S37-nothing', 'Nothing to resolve: every open conflict is on an item Mert never decided', phone(bg3 + nothing_sheet))
    F('S37-error', 'Partial failure: 9 of 12 resolved', phone(summary_screen('error')))
    undo_dlg = dialog('Undo Resolve all?', f'The {len(MERT_DECIDED)} conflicts open again with every member\'s decision as it was. Deniz and Selin are notified.',
                      dbtn('Cancel', href='#S37-summary') + dbtn('Undo Resolve all', 'destructive', '#S37-undone', 'confirm-undo'))
    F('S37-undo', 'Undo from the summary: confirmation', phone(summary_screen() + undo_dlg))
    F('S37-undone', 'Undone: back to 15 open conflicts', phone(s36_screen(undo=False, overlay=snackbar(f'Undid Resolve all. {len(MERT_DECIDED)} conflicts are open again.', bottom='bottom-28', icon_name='undo-2'))))
    F('S37-offline', 'Offline: Resolve all is blocked, one by one still works', phone(s36_screen(top=offline_banner("You're offline. Resolutions are saved on this phone and sync when you're back online."), undo=False) + confirm_sheet('offline')))
    na = f'''{appbar('Resolve conflicts', 'back', 'S09-list-overview.html#S09-shared', sub='Wedding guests, Round 1', lead_label='Back to Wedding guests')}
  <div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
    {icon("gavel", "size-8 text-muted-foreground")}
    <h2 class="text-balance mt-4 text-title-3">Only Mert can resolve all conflicts</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">Mert is the Decision Maker. You can review the conflicts and change your own decisions.</p>
    <div class="mt-6 w-full max-w-xs space-y-2">{btn("Review conflicts", "primary", "S36-conflicts.html#S36-non-dm", "review-conflicts")}{btn("Back to list", "ghost", "S09-list-overview.html#S09-shared")}</div>
  </div>'''
    F('S37-not-allowed', 'Opened by a member who is not the Decision Maker (old link)', phone(na))
    pg.section('Accessibility and iOS', 'Large text keeps the counts and the open items readable; the sheet scrolls. iOS: the confirmation is a page sheet with Cancel in the bar.')
    F('S37-large-text', 'Large text (200%): confirmation', phone(bg + confirm_sheet(large=True)))
    F('S37-summary-large-text', 'Large text (200%): summary', phone(summary_screen(large=True)))
    F('S37-ios', 'iOS: confirmation as a page sheet', phone(s36_screen(hdr=s36_header(ios=True, back_href='S09-list-overview.html#S09-shared-decision-maker'), undo=False) + confirm_sheet(ios=True), ios=True))
    pg.write('S37-bulk-resolve.html')

# =====================================================================================
# S38 ACTIVITY
# =====================================================================================
EV_IC = {'memberJoined': 'user-plus', 'memberFinished': 'flag', 'newConflicts': 'git-compare-arrows', 'conflictsResolved': 'check-check', 'roundStarted': 'play', 'roleChanged': 'user-cog', 'ruleChanged': 'git-compare-arrows'}

# Deniz's feed (viewer = Owner). Text per domain-model.md › ActivityEvent; "you" for the viewer.
FEED = [
    ('Today', [dict(ev='ev4', type='memberFinished', actor='selin', text='Selin finished sorting Wedding guests', sub='100 / 100 decided', time='11 min ago', href='S09-list-overview.html#S09-shared', unread=True)]),
    ('Yesterday', [dict(ev='ev7', type='conflictsResolved', actor='mert', text='Mert resolved 3 conflicts in Wedding guests', sub=None, time='9:14 PM', href='S28-results.html#S28-shared-resolved', unread=True)]),
    ('Oct 3', [dict(ev='ev6', type='newConflicts', actor=None, text='15 conflicts in Wedding guests', sub='Mert decides them.', time='11:45 AM', href='S36-conflicts.html#S36-non-dm', unread=True)]),
    ('Oct 2', [dict(ev='ev5', type='memberJoined', actor='selin', text='Selin joined Wedding guests', sub=None, time='5:40 PM', href='S34-members.html#S34-default')]),
    ('Sep 28', [dict(ev='ev1', type='roundStarted', actor='deniz', text='You started Round 1 in Wedding guests', sub='100 items', time='7:05 PM', href='S25-sorting.html#S25-shared'),
                dict(ev='ev3', type='roleChanged', actor='deniz', text='You made Mert the Decision Maker', sub='Wedding guests', time='8:20 AM', href='S34-members.html#S34-default'),
                dict(ev='ev2', type='memberJoined', actor='mert', text='Mert joined Wedding guests', sub=None, time='8:15 AM', href='S34-members.html#S34-default')]),
]
MERT_FEED = [
    ('Today', [dict(type='memberFinished', actor='selin', text='Selin finished sorting Wedding guests', sub='100 / 100 decided', time='11 min ago', href='S09-list-overview.html#S09-shared', unread=True)]),
    ('Oct 3', [dict(type='newConflicts', actor=None, text='15 conflicts in Wedding guests need your decision', sub="You're the Decision Maker.", time='11:45 AM', href='S36-conflicts.html#S36-default', unread=True, action=('Review', 'S36-conflicts.html#S36-default'))]),
    ('Oct 2', [dict(type='memberJoined', actor='selin', text='Selin joined Wedding guests', sub=None, time='5:40 PM', href='S34-members.html#S34-decision-maker')]),
    ('Sep 28', [dict(type='roundStarted', actor='deniz', text='Deniz started Round 1 in Wedding guests', sub='100 items', time='7:05 PM', href='S25-sorting.html#S25-shared'),
                dict(type='roleChanged', actor='deniz', text='Deniz made you the Decision Maker', sub='Wedding guests', time='8:20 AM', href='S34-members.html#S34-decision-maker')]),
]

def ev_row(e, read_all=False, large=False):
    unread = e.get('unread') and not read_all
    ic = EV_IC[e['type']]
    if e['actor']:
        lead = f'<span class="relative shrink-0">{av(e["actor"], "size-10")}<span class="absolute -bottom-1 -right-1 flex size-5 items-center justify-center rounded-full bg-secondary text-secondary-foreground ring-2 ring-background">{icon(ic, "size-3")}</span></span>'
    else:
        lead = f'<span class="flex size-10 shrink-0 items-center justify-center rounded-full bg-conflict text-conflict-foreground">{icon(ic, "size-5")}</span>'
    t = 'text-title-2 font-normal' if large else 'text-body'
    s = 'text-title-3 font-normal' if large else 'text-body-sm'
    w = ' font-semibold' if unread else ''
    dotm = '<span class="size-2.5 rounded-full bg-primary" aria-hidden="true"></span>' if unread else ''
    sr = '<span class="sr-only">Unread. </span>' if unread else ''
    act = ''
    if e.get('action'):
        a, h = e['action']
        act = f'<a href="{h}" class="-ml-3 mt-1 inline-flex h-12 items-center rounded-control px-3 text-label text-primary" data-action="review-conflicts">{a}</a>'
    subl = f'<span class="mt-0.5 block {s} text-muted-foreground">{e["sub"]}</span>' if e.get('sub') else ''
    if large:
        body = f'''{lead}<span class="min-w-0 flex-1">{sr}<span class="block {t}{w}">{e["text"]}</span>{subl}<span class="mt-0.5 block text-body-lg text-muted-foreground">{e["time"]}</span></span>{dotm}'''
    else:
        body = f'''{lead}<span class="min-w-0 flex-1">{sr}<span class="block {t}{w}">{e["text"]}</span>{subl}</span><span class="flex shrink-0 flex-col items-end gap-2"><span class="text-caption text-muted-foreground">{e["time"]}</span>{dotm}</span>'''
    bg = ' bg-primary-soft/40' if unread else ''
    if act:
        return f'<li class="px-gutter py-3{bg}"><a href="{e["href"]}" class="flex items-start gap-3">{body}</a>{act.replace("-ml-3", "ml-10")}</li>'
    return f'<li><a href="{e["href"]}" class="flex min-h-16 items-start gap-3 px-gutter py-3{bg}">{body}</a></li>'

def feed(groups, read_all=False, large=False, filt=None):
    out = ''
    for day, evs in groups:
        evs = [e for e in evs if (filt is None or e['type'] in filt)]
        if not evs:
            continue
        rows = ''.join(ev_row(e, read_all, large) for e in evs)
        out += f'<section><h2 class="px-gutter pb-1 pt-4 {"text-title-3 font-normal" if large else "text-label"} text-muted-foreground">{day}</h2><ul class="divide-y">{rows}</ul></section>'
    return out

def s38_tabs(active='All', large=False):
    out = ''
    for t, h in (('All', '#S38-default'), ('Conflicts', '#S38-filter'), ('Members', '#S38-filter-members')):
        if t == active:
            out += f'<a href="{h}" role="tab" aria-selected="true" class="relative flex h-12 flex-1 items-center justify-center text-label">{t}<span class="absolute inset-x-6 bottom-0 h-0.5 rounded-full bg-primary"></span></a>'
        else:
            out += f'<a href="{h}" role="tab" aria-selected="false" class="flex h-12 flex-1 items-center justify-center text-label text-muted-foreground" data-action="filter-{t.lower()}">{t}</a>'
    if large:
        out = out.replace('h-12', 'h-14').replace('text-label', 'text-title-3')
    return f'<div class="flex shrink-0 border-b px-2" role="tablist" aria-label="Filter activity">{out}</div>'

def s38_header(unread=3, ios=False, offline=False, web=False):
    mark = (icon_action('check-check', 'Mark all as read', '#S38-all-read', 'mark-all-read') if unread
            else '<button class="flex size-12 shrink-0 items-center justify-center rounded-full opacity-50" aria-label="Mark all as read" disabled>' + icon('check-check', 'size-6') + '</button>')
    prefs = icon_action('settings-2', 'Notification settings', 'S06-settings.html#S06-notifications-web' if web else 'S06-settings.html#S06-notifications', 'notification-settings')
    if ios:
        return f'''<header class="flex h-11 shrink-0 items-center justify-end gap-1 px-2 text-primary">{mark.replace('rounded-full', 'rounded-full text-primary', 1)}{prefs.replace('rounded-full', 'rounded-full text-primary', 1)}</header>
  <h1 class="shrink-0 px-4 pb-2 text-title-1">Activity</h1>'''
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 pl-gutter pr-1">
    <h1 class="min-w-0 flex-1 text-title-1">Activity</h1>{mark}{prefs}
  </header>'''

def s38_screen(groups=FEED, unread=3, tab='All', top='', overlay='', read_all=False, ios=False, large=False, filt=None, web=False, nav=True, body=None):
    hdr = s38_header(0 if read_all else unread, ios, web=web)
    if top and groups is FEED:
        groups = FEED[:4]  # a top block pushes the oldest day below the fold; keep the frame free of clipped rows
    content = body if body is not None else feed(groups, read_all, large, filt)
    nb = 0 if read_all else unread
    n = (ios_tab_bar(badge=nb) if ios else bottom_nav(large=large, badge=nb)) if nav else ''
    return f'''{hdr}
  {s38_tabs(tab, large)}
  {top}
  <div class="min-h-0 flex-1 overflow-hidden">{content}</div>
  {n}
  {overlay}'''

def build_s38():
    pg = Page('S38', 'Activity and notifications', 'The Activity tab: what happened on shared lists, grouped by day, with unread state and filters. Plus how SwipeSort notifications read on the phone, the in-app banner, web in-app notifications, notification preferences and the push pre-permission. Spec: <a href="S38-activity.md">S38-activity.md</a>.')
    F = pg.frame
    pg.section('Activity feed', 'Deniz (Owner of Wedding guests). Six event types: someone joined, finished sorting, new conflicts, conflicts resolved, a new round started, a role changed. Each row opens the screen it is about.')
    F('S38-default', 'Default: 3 unread, grouped by day', phone(s38_screen()))
    F('S38-all-read', 'Mark all as read', phone(s38_screen(FEED[:4], read_all=True, overlay=snackbar('Marked 3 as read', bottom='bottom-24'))))
    F('S38-filter', 'Filter: Conflicts', phone(s38_screen(tab='Conflicts', filt={'newConflicts', 'conflictsResolved'})))
    F('S38-filter-members', 'Filter: Members', phone(s38_screen(tab='Members', filt={'memberJoined', 'memberFinished', 'roleChanged'})))
    F('S38-decision-maker', 'Decision Maker view (Mert): conflicts call for action', phone(s38_screen(MERT_FEED, unread=2)))
    pg.section('States', 'Empty, loading, error and offline.')
    empty = f'''<div class="flex h-full flex-col items-center justify-center px-8 text-center">
    {icon("activity", "size-8 text-muted-foreground")}
    <h2 class="text-balance mt-4 text-title-3">No activity yet</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">When you share a list, you'll see here when people join, finish sorting or disagree.</p>
    <div class="mt-6 w-full max-w-xs">{btn("Go to your lists", "primary", "S08-home.html#S08-default", "go-to-lists")}</div>
  </div>'''
    F('S38-empty', 'Empty: no shared lists yet', phone(s38_screen(unread=0, body=empty)))
    sk_row = '<div class="flex items-start gap-3 px-gutter py-3"><span class="size-10 shrink-0 animate-pulse rounded-full bg-muted"></span><div class="flex-1 space-y-2 pt-1"><span class="block h-4 w-3/4 animate-pulse rounded-full bg-muted"></span><span class="block h-3 w-1/3 animate-pulse rounded-full bg-muted"></span></div></div>'
    F('S38-loading', 'Loading', phone(s38_screen(unread=0, body=f'<div role="status" aria-busy="true" aria-label="Loading activity"><span class="mx-gutter mb-2 mt-5 block h-3.5 w-16 animate-pulse rounded-full bg-muted"></span>{sk_row * 5}</div>')))
    err = f'''<div class="flex h-full flex-col items-center justify-center px-8 text-center">
    {icon("cloud-alert", "size-8 text-muted-foreground")}
    <h2 class="text-balance mt-4 text-title-3">Activity couldn't be loaded</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">SwipeSort didn't respond. Check your connection and try again.</p><p class="mt-3 max-w-xs text-balance text-body-sm text-muted-foreground">Your lists and decisions are saved on this phone.</p>
    <div class="mt-6 w-full max-w-xs">{btn("Try again", "secondary", action="try-again")}</div>
  </div>'''
    F('S38-error', 'Error', phone(s38_screen(unread=0, body=err)))
    F('S38-offline', 'Offline: last synced activity', phone(s38_screen(top=offline_banner("You're offline. Showing activity from your last sync, Oct 10 at 9:30 AM."))))

    pg.section('Notifications', 'Push asks for permission only after a list is shared or joined (S12). Activity always shows every event; preferences decide which ones also push. Notifications turned off: the feed explains and links to the fix.')
    prompt = f'''<div class="px-4 pt-3"><div class="rounded-group bg-card p-4 dark:border">
      <div class="flex gap-3">{icon("bell-ring", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="text-label">Get notified about shared lists</p><p class="mt-0.5 text-body-sm text-muted-foreground">Know when someone finishes sorting or a conflict needs a decision, without opening SwipeSort.</p></div></div>
      <div class="mt-3 flex flex-wrap justify-end gap-2">{dbtn("Not now", href="#S38-default")}{dbtn("Turn on notifications", "primary", "S12-permissions.html#S12-notifications", "turn-on-notifications")}</div>
    </div></div>'''
    F('S38-permission-prompt', 'Push not asked yet: prompt above the feed', phone(s38_screen(FEED[:4], top=prompt)))
    off = f'''<div class="px-4 pt-3">{alert("neutral", "Notifications are off", "SwipeSort can't send push notifications on this phone. New events still appear here.", "bell-off", link("Turn on in Settings", "S06-settings.html#S06-notifications-denied", "fix-notifications"))}</div>'''
    F('S38-notifications-off', 'Notifications turned off on this phone', phone(s38_screen(top=off)))
    # notification content annotation
    rows = [
        ('user-plus', 'Someone joins a list', 'Wedding guests', 'Selin joined the list.', 'Members (S34)'),
        ('user-plus', 'Joins with a Decision Maker link', 'Wedding guests', 'Mert joined as Decision Maker.', 'Members (S34)'),
        ('flag', 'Someone finishes sorting', 'Wedding guests', 'Selin finished sorting. 100 / 100 decided.', 'List overview (S09)'),
        ('git-compare-arrows', 'New conflicts (members)', 'Wedding guests', '3 new conflicts. Mert decides them.', 'Conflicts (S36)'),
        ('git-compare-arrows', 'New conflicts (Decision Maker)', 'Wedding guests', '3 new conflicts need your decision.', 'Conflicts (S36)'),
        ('check-check', 'Conflicts resolved', 'Wedding guests', 'Mert resolved 12 conflicts. 3 are still open.', 'Results (S28)'),
        ('play', 'A new round starts', 'Wedding guests', 'Deniz started Round 2 with 11 items.', 'Sorting (S25)'),
        ('user-cog', 'Your role changes', 'Wedding guests', 'Deniz made you the Decision Maker.', 'Members (S34)'),
    ]
    lis = ''.join(f'''<li class="py-2"><p class="flex items-center gap-2 text-caption text-muted-foreground">{icon(ic, "size-4")}{ev}<span class="ml-auto">Opens {opens}</span></p>
        <div class="mt-1 flex gap-3 rounded-control bg-muted px-3 py-2"><img src="../01-foundations/brand/app-icon.svg" alt="" class="size-6 shrink-0 rounded-xs"><div class="min-w-0"><p class="text-label">{title}</p><p class="text-body-sm">{body}</p></div></div></li>''' for ic, ev, title, body, opens in rows)
    annot = f'''<div class="min-h-0 flex-1 overflow-hidden px-gutter pt-4">
    <h2 class="text-title-2">Notification content</h2>
    <p class="mt-1 text-body-sm text-muted-foreground">Annotation: the notification shade is system UI. Title = list name; body = one sentence, the same words as Activity.</p>
    <ul class="mt-1 divide-y">{lis}</ul>
  </div>'''
    F('S38-push-content', 'Push notification content per event (annotation)', phone(annot))
    s35bg = s35_screen()
    banner = f'''<div class="absolute inset-x-3 top-16 z-40" role="status"><a href="S09-list-overview.html#S09-shared" class="flex items-start gap-3 rounded-control bg-popover p-3 shadow-overlay" data-action="open-notification">
    <span class="relative shrink-0">{av("selin", "size-10")}<span class="absolute -bottom-1 -right-1 flex size-5 items-center justify-center rounded-full bg-secondary text-secondary-foreground ring-2 ring-popover">{icon("flag", "size-3")}</span></span>
    <span class="min-w-0 flex-1"><span class="block text-label">Selin finished sorting Wedding guests</span><span class="block text-body-sm text-muted-foreground">100 / 100 decided</span></span>
    <span class="text-caption text-muted-foreground">now</span>
  </a></div>'''
    F('S38-in-app-banner', 'In-app banner while SwipeSort is open (Android, iOS and web)', phone(s35bg + banner))
    pg.section('Web', 'Push notifications are not available on web (PLT-10): Activity and the badge update live while the tab is open, new events also show as a toast, and the feed explains why push needs the app.')
    web_note = f'''<div class="px-4 pt-3">{alert("neutral", "Push notifications need the app", "In the browser, new events show up here and as a badge while SwipeSort is open. To get notified on your phone, get SwipeSort for Android or iOS.", "monitor-smartphone", link("Get the app", GET_APP, "get-app"))}</div>'''
    F('S38-web', 'Web, mobile browser: in-app only, Get the app', web_phone(s38_screen(top=web_note, web=True)))
    toast = f'''<div class="absolute bottom-24 right-4 z-40 flex w-80 items-start gap-3 rounded-control bg-popover p-3 shadow-overlay" role="status">
    <span class="relative shrink-0">{av("selin", "size-10")}<span class="absolute -bottom-1 -right-1 flex size-5 items-center justify-center rounded-full bg-secondary text-secondary-foreground ring-2 ring-popover">{icon("flag", "size-3")}</span></span>
    <a href="S09-list-overview.html#S09-shared" class="min-w-0 flex-1" data-action="open-notification"><span class="block text-label">Selin finished sorting Wedding guests</span><span class="block text-body-sm text-muted-foreground">100 / 100 decided</span></a>
    <button class="-m-1.5 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Dismiss">{icon("x", "size-4")}</button>
  </div>'''
    host = f'''{s36_header(back_href='S09-list-overview.html#S09-shared')}
  <div class="flex flex-1 flex-col items-center justify-center px-8 pb-24 text-center">
    {icon("git-compare-arrows", "size-8 text-muted-foreground")}
    <h2 class="mt-4 text-balance text-title-3">No conflicts</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">When members decide an item differently, it shows up here. 24 items in Round 1 are still waiting for your decision.</p>
    <div class="mt-6 w-full max-w-xs">{btn("Continue sorting", "primary", "S25-sorting.html#S25-shared", "continue-sorting")}</div>
  </div>'''
    desk = host + toast.replace('bottom-24 right-4', 'bottom-6 right-4')
    F('S38-web-desktop', 'Web, desktop: toast for a new event while another screen is open', desktop('swipesort.app/l/7Hq2xK/conflicts', desk))
    pg.section('Accessibility and iOS', 'Large text: rows grow, times move under the text. iOS: large title, standard tab bar.')
    F('S38-large-text', 'Large text (200%)', phone(s38_screen(large=True)))
    F('S38-ios', 'iOS', phone(s38_screen(ios=True), ios=True))
    pg.write('S38-activity.html')

if __name__ == '__main__':
    build_s35()
    build_s36()
    build_s37()
    build_s38()
