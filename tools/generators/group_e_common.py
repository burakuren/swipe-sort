# Shared helpers for the Group E generators (S24 Start a round, S26 Item detail, S27 Round summary).
# Markup mirrors tools/generators/S25-sorting.py and 01-foundations/components.html.
# Not a screen generator itself; imported by S24-start-round.py, S26-item-detail.py, S27-round-summary.py.
import re

IMG = '../02-data/images/'


def icon(name, size='size-5', extra=''):
    return f'<i class="i-lucide-{name} {size} {extra}" aria-hidden="true"></i>'.replace('  ', ' ').replace(' "', '"')


# ---------------------------------------------------------------- page and frames
def phone(content, ios=False, overlay=''):
    """overlay: full-frame layer (scrim + dialog) placed over the system bars too (group A pattern)."""
    cls = 'phone-ios' if ios else 'phone'
    return f'''<div class="{cls}">
  <div class="sysbar-top" aria-hidden="true"><span>9:41</span><span class="sysbar-icons"></span></div>
  <div class="screen">
  {content}
  </div>
  <div class="sysbar-nav" aria-hidden="true"></div>
  {overlay}
</div>'''


def web_phone(content):
    return f'''<div class="phone">
  <div class="screen">
  {content}
  </div>
</div>'''


def desktop(content, url, below=''):
    return f'''<div class="desktop">
  <div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">{url}</span></div>
  <div class="desktop-column">
  {content}
  {below}
  </div>
</div>'''


class Frames:
    def __init__(self, sid):
        self.sid = sid
        self.items = []

    def add(self, fid, label, inner):
        assert fid.startswith(self.sid + '-'), fid
        self.items.append(f'''
<figure class="frame" data-frame="{fid}" id="{fid}">
  <figcaption class="frame-label">{self.sid} · {label} · <span class="theme-name"></span></figcaption>
  {inner}
</figure>''')

    def section(self, title, desc):
        self.items.append(f'</main>\n<h2 class="mock-section">{title}</h2>\n<p>{desc}</p>\n<main class="mock-canvas">')

    def write(self, out, title, intro):
        html = f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../assets/css/app.css">
</head>
<body class="mock-page">
<header class="mock-doc">
  <h1>{title}</h1>
  <p>{intro}</p>
</header>
<main class="mock-canvas">
{''.join(self.items)}
</main>
</body>
</html>
'''
        html = html.replace('<main class="mock-canvas">\n</main>\n', '', 1)
        ids = re.findall(r'data-frame="([^"]+)"', html)
        assert len(ids) == len(set(ids)), 'duplicate frame ids'
        open(out, 'w').write(html)
        print(out, 'frames:', len(ids))


# ---------------------------------------------------------------- buttons
VARIANT = {
    'primary': 'bg-primary text-primary-foreground',
    'secondary': 'bg-secondary text-secondary-foreground',
    'outline': 'border border-input bg-card',
    'ghost': '',
    'destructive': 'bg-destructive text-destructive-foreground',
    'link': 'text-primary',
}


def btn(text, variant='primary', href=None, action=None, ic=None, full=True, disabled=False, extra='', aria=None, h='h-12'):
    w = 'w-full' if full else 'px-5'
    cls = f'inline-flex {h} min-w-touch {w} items-center justify-center gap-2 rounded-control text-label-lg {VARIANT[variant]} {extra}'
    if disabled:
        cls += ' opacity-50'
    inner = (icon(ic) if ic else '') + text
    da = f' data-action="{action}"' if action else ''
    al = f' aria-label="{aria}"' if aria else ''
    if href and not disabled:
        return f'<a href="{href}" class="{cls}"{da}{al}>{inner}</a>'
    dis = ' disabled' if disabled else ''
    return f'<button type="button" class="{cls}"{da}{al}{dis}>{inner}</button>'


def icon_btn(ic, label, href=None, action=None, extra='', size='size-6'):
    cls = f'flex size-12 shrink-0 items-center justify-center rounded-full {extra}'
    da = f' data-action="{action}"' if action else ''
    if href:
        return f'<a href="{href}" class="{cls}" aria-label="{label}"{da}>{icon(ic, size)}</a>'
    return f'<button type="button" class="{cls}" aria-label="{label}"{da}>{icon(ic, size)}</button>'


# ---------------------------------------------------------------- bars
def modal_bar(title, sub=None, close_href=None, close_label='Close', trailing='', action=None):
    subp = f'<p class="truncate text-caption text-muted-foreground">{sub}</p>' if sub else ''
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    {icon_btn("x", close_label, close_href, action or "close")}
    <div class="min-w-0 flex-1 px-1"><h1 class="truncate text-title-3">{title}</h1>{subp}</div>
    {trailing}
  </header>'''


def back_bar(title, back_href=None, back_label='Back', trailing='', sub=None):
    subp = f'<p class="truncate text-caption text-muted-foreground">{sub}</p>' if sub else ''
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    {icon_btn("arrow-left", back_label, back_href, "back")}
    <div class="min-w-0 flex-1 px-1"><h1 class="truncate text-title-3">{title}</h1>{subp}</div>
    {trailing}
  </header>'''


def ios_bar(left, title, right='', sub=None):
    subp = f'<p class="truncate text-caption text-muted-foreground">{sub}</p>' if sub else ''
    return f'''<header class="grid h-14 shrink-0 grid-cols-[1fr_auto_1fr] items-center gap-2 px-3">
    <div class="justify-self-start">{left}</div>
    <div class="min-w-0 text-center"><h1 class="truncate text-body font-semibold">{title}</h1>{subp}</div>
    <div class="justify-self-end">{right}</div>
  </header>'''


def ios_text_btn(text, bold=False, href=None, action=None, disabled=False):
    w = ' font-semibold' if bold else ''
    da = f' data-action="{action}"' if action else ''
    cls = f'inline-flex h-12 min-w-touch items-center justify-center px-1 text-body text-primary{w}'
    if disabled:
        return f'<button type="button" class="{cls} opacity-50" disabled>{text}</button>'
    if href:
        return f'<a href="{href}" class="{cls}"{da}>{text}</a>'
    return f'<button type="button" class="{cls}"{da}>{text}</button>'


def offline_banner(text="You're offline. Changes are saved on this phone."):
    return f'<div class="flex shrink-0 items-center gap-2 bg-muted px-gutter py-2 text-body-sm" role="status">{icon("wifi-off", "size-4 shrink-0")}<span class="flex-1">{text}</span></div>'


# ---------------------------------------------------------------- badges and small parts
DEC = {
    'accept': ('check', 'Accept', 'Accepted', 'accepted'),
    'reject': ('x', 'Reject', 'Rejected', 'rejected'),
    'maybe': ('circle-help', 'Maybe', 'Maybe', 'maybe'),
}


def badge(kind, text=None):
    base = 'inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full px-2.5 text-caption'
    if kind in DEC:
        ic, _, state, _ = DEC[kind]
        return f'<span class="{base} bg-{kind}-soft text-{kind}-soft-foreground">{icon(ic, "size-4")}{text or state}</span>'
    spec = {
        'none': ('bg-muted text-muted-foreground', 'circle-dashed', 'Not decided yet'),
        'agreed': ('border', 'check-check', 'Agreed'),
        'pending': ('bg-muted text-muted-foreground', 'clock', 'Pending'),
        'conflict': ('bg-conflict text-conflict-foreground', 'git-compare-arrows', 'Conflict'),
        'resolved': ('border', 'gavel', 'Resolved by Mert'),
        'edited': ('bg-secondary text-secondary-foreground', 'pencil-line', 'Edited'),
        'private': ('border border-dashed border-input text-muted-foreground', 'lock', 'Only you'),
        'dm': ('bg-primary-soft text-primary-soft-foreground', 'gavel', 'Decision Maker'),
        'owner': ('bg-secondary text-secondary-foreground', 'crown', 'Owner'),
        'offline': ('bg-secondary text-secondary-foreground', 'cloud-off', 'Not synced'),
    }[kind]
    return f'<span class="{base} {spec[0]}">{icon(spec[1], "size-4")}{text or spec[2]}</span>'


def count_chip(kind, n):
    """Count with decision icon, used for pile sizes (Maybe pile 11)."""
    if kind in DEC:
        return f'<span class="inline-flex h-7 shrink-0 items-center gap-1 rounded-full bg-{kind}-soft px-2.5 text-label tabular-nums text-{kind}-soft-foreground">{icon(DEC[kind][0], "size-4")}{n}</span>'
    return f'<span class="inline-flex h-7 shrink-0 items-center rounded-full px-1 text-label tabular-nums text-muted-foreground">{n}</span>'


PEOPLE_AV = {
    'deniz': ('u-deniz.svg', 'DY', 'Deniz'),
    'mert': ('u-mert.svg', 'MA', 'Mert'),
    'selin': (None, 'SY', 'Selin'),
}


def avatar(who, size='size-8', ring=''):
    """who: key of PEOPLE_AV, or ('photo path' | None, initials)."""
    if isinstance(who, str):
        photo, ini, _ = PEOPLE_AV[who]
        photo = f'people/{photo}' if photo else None
    else:
        photo, ini = who
    txt = 'text-caption' if size in ('size-6', 'size-8') else ('text-label' if size == 'size-10' else 'text-title-3')
    if photo:
        return f'<img src="{IMG}{photo}" alt="" class="{size} shrink-0 rounded-full object-cover {ring}">'
    return f'<span class="flex {size} shrink-0 items-center justify-center rounded-full bg-muted {txt} text-muted-foreground {ring}" aria-hidden="true">{ini}</span>'


def avatar_stack(names, label, size='size-6'):
    inner = ''.join(avatar(n, size, 'ring-2 ring-background') for n in names)
    return f'<span class="flex -space-x-2" role="img" aria-label="{label}">{inner}</span>'


def radio_dot(checked, disabled=False):
    op = ' opacity-50' if disabled else ''
    if checked:
        return f'<span class="flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary{op}" aria-hidden="true"><span class="size-3 rounded-full bg-primary"></span></span>'
    return f'<span class="size-6 shrink-0 rounded-full border-2 border-input{op}" aria-hidden="true"></span>'


def checkbox(checked):
    if checked:
        return f'<span class="flex size-6 shrink-0 items-center justify-center rounded-sm bg-primary text-primary-foreground" aria-hidden="true">{icon("check", "size-4")}</span>'
    return '<span class="size-6 shrink-0 rounded-sm border-2 border-input" aria-hidden="true"></span>'


def switch(on, label, disabled=False):
    dis = ' aria-disabled="true"' if disabled else ''
    op = ' opacity-50' if disabled else ''
    if on:
        return f'<button type="button" role="switch" aria-checked="true" aria-label="{label}" class="flex h-8 w-13 shrink-0 items-center rounded-full bg-primary p-1{op}"{dis}><span class="ml-auto size-6 rounded-full bg-primary-foreground"></span></button>'
    return f'<button type="button" role="switch" aria-checked="false" aria-label="{label}" class="flex h-8 w-13 shrink-0 items-center rounded-full border-2 border-input bg-muted p-1{op}"{dis}><span class="size-5 rounded-full bg-muted-foreground"></span></button>'


def segmented(options, selected, label, role='radiogroup'):
    """options: list of (text, icon or None). Pill track like components.html SegmentedControl."""
    btns = ''
    for text, ic in options:
        on = text == selected
        cls = 'bg-card text-foreground shadow-raised' if on else 'text-muted-foreground'
        btns += f'<button type="button" role="radio" aria-checked="{"true" if on else "false"}" class="inline-flex h-10 flex-1 items-center justify-center gap-1.5 rounded-full px-3 text-label {cls}">{icon(ic, "size-4") if ic else ""}{text}</button>'
    return f'<div class="flex rounded-full bg-secondary p-1" role="{role}" aria-label="{label}">{btns}</div>'


def section_header(text, extra='', trailing=''):
    if trailing:
        return f'<div class="flex items-end justify-between gap-3 px-1 pb-2 {extra}"><h2 class="text-label text-muted-foreground">{text}</h2>{trailing}</div>'
    return f'<h2 class="px-1 pb-2 text-label text-muted-foreground {extra}">{text}</h2>'


# ---------------------------------------------------------------- overlays
def scrim(op='bg-scrim/50', z='z-10'):
    return f'<div class="absolute inset-0 {z} bg-scrim/50"></div>'.replace('bg-scrim/50', op)


def snackbar(text, action=None, bottom='bottom-6', role='status', ic=None, href=None):
    act = ''
    if action:
        if href:
            act = f'<a href="{href}" class="-my-1 inline-flex h-12 items-center rounded-sm px-3 text-label text-primary-inverse">{action}</a>'
        else:
            act = f'<button type="button" class="-my-1 inline-flex h-12 items-center rounded-sm px-3 text-label text-primary-inverse">{action}</button>'
    i = icon(ic, 'size-5 shrink-0') if ic else ''
    pad = 'py-1.5 pl-4 pr-1.5' if action else 'px-4 py-3'
    return f'<div class="absolute inset-x-4 {bottom} z-30 flex min-h-12 items-center gap-3 rounded-control bg-foreground {pad} text-background shadow-overlay" role="{role}">{i}<span class="flex-1 text-body-sm">{text}</span>{act}</div>'


def sheet(inner, title_id, top='top-28', pb='pb-0', handle=True, extra=''):
    h = '<div class="flex shrink-0 justify-center py-1.5"><span class="h-1 w-8 rounded-full bg-muted-foreground/40"></span></div>' if handle else ''
    pos = f'{top} bottom-0' if top else 'bottom-0'
    return f'''<div class="absolute inset-x-0 {pos} z-20 flex flex-col overflow-hidden rounded-t-sheet bg-popover pt-2 {pb} shadow-sheet {extra}" role="dialog" aria-modal="true" aria-labelledby="{title_id}">
    {h}
    {inner}
  </div>'''


def dialog(did, title, body, actions, role='alertdialog'):
    return f'''<div class="absolute inset-0 z-30 flex items-center justify-center px-6">
    <div class="w-full rounded-dialog bg-popover p-6 shadow-dialog" role="{role}" aria-modal="true" aria-labelledby="{did}" aria-describedby="{did}d">
      <h2 id="{did}" class="text-title-3">{title}</h2>
      <div id="{did}d" class="mt-2 space-y-2 text-body text-muted-foreground">{body}</div>
      <div class="mt-6 flex flex-wrap justify-end gap-2">{actions}</div>
    </div>
  </div>'''


def kbd(k, t):
    return f'<span class="inline-flex items-center gap-1.5"><kbd class="inline-flex h-6 min-w-6 items-center justify-center rounded-sm border border-b-2 bg-card px-1.5 text-caption text-foreground">{k}</kbd>{t}</span>'


def hints(pairs, label='Keyboard shortcuts'):
    return f'<div class="flex shrink-0 flex-wrap justify-center gap-x-4 gap-y-2 border-t bg-background px-4 py-3 text-caption text-muted-foreground" aria-label="{label}">{"".join(kbd(k, t) for k, t in pairs)}</div>'


# ---------------------------------------------------------------- S25 background (non-interactive copy)
def _strip_interactive(html):
    html = re.sub(r'<(a|button)\b[^>]*>', '<span class="contents">', html)
    html = re.sub(r'</(a|button)>', '</span>', html)
    html = re.sub(r' (data-action|aria-label|role|tabindex|aria-roledescription|aria-valuenow|aria-valuemin|aria-valuemax|aria-modal|aria-labelledby)="[^"]*"', '', html)
    html = re.sub(r'<h1 ', '<p ', html).replace('</h1>', '</p>')
    html = re.sub(r'<h2 ', '<p ', html).replace('</h2>', '</p>')
    return html


def s25_row(label, value, edited=False):
    ed = f'<span class="ml-1.5 inline-flex items-center align-middle text-muted-foreground">{icon("pencil-line", "size-3.5")}</span>' if edited else ''
    return f'<div class="flex gap-3"><dt class="w-16 shrink-0 text-muted-foreground">{label}</dt><dd class="min-w-0 truncate tabular-nums">{value}{ed}</dd></div>'


def s25_photo_card(img, place, country, best, budget):
    """Photo template card body on "Trip ideas" (D-32, A-130, A-131): same markup as S25-photo and S40's card."""
    rows = ''.join(f'<div class="flex gap-3"><dt class="w-24 shrink-0 text-muted-foreground">{k}</dt><dd class="min-w-0 truncate tabular-nums">{v}</dd></div>' for k, v in (('Best time', best), ('Budget', budget)))
    return f'''<img src="{IMG}photos/{img}.svg" alt="" class="min-h-0 w-full flex-1 object-cover">
      <div class="shrink-0 px-6 pb-5 pt-4"><p class="text-title-2">{place}</p><p class="mt-0.5 text-body text-muted-foreground">{country}</p>
        <dl class="mt-3 flex flex-col gap-1.5 text-body-sm">{rows}</dl></div>'''


def s25_person(name, sub, photo, rows, tags, initials='', note=None):
    img = f'<img src="{IMG}{photo}" alt="" class="h-[46%] w-full object-cover">' if photo else f'<div class="px-6 pt-7"><span class="flex size-24 items-center justify-center rounded-full bg-muted text-title-1 text-muted-foreground">{initials}</span></div>'
    rws = ''.join(s25_row(*r) for r in rows)
    tg = ''.join(f'<span class="inline-flex h-7 items-center rounded-full bg-secondary px-2.5 text-caption text-secondary-foreground">{t}</span>' for t in tags)
    nt = f'<p class="flex items-center gap-2 text-body-sm text-muted-foreground">{icon(note[1], "size-4 shrink-0")}<span class="truncate">{note[0]}</span></p>' if note else ''
    return f'''{img}
      <div class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-5">
        <p class="line-clamp-3 text-card-title">{name}</p>
        <p class="mt-1 text-body-lg text-muted-foreground">{sub}</p>
        <dl class="mt-4 space-y-2 text-body">{rws}</dl>
        <div class="mt-auto space-y-3 pt-3">{nt}<div class="flex gap-2">{tg}</div></div>
      </div>'''


S25_MIA = s25_person('Mia Andersson', 'Colleague', 'people/c077.svg', [('Phone', '+46 8 0000 4021'), ('Email', 'mia.andersson@example.com'), ('City', 'Stockholm')], ["Bride's"])
S25_ANNA = s25_person('Anna-Katharina Rosenthal-Brückner', 'Colleague', 'people/c078.svg', [('Phone', '+43 1 0000 4117'), ('City', 'Vienna')], ["Bride's"])


def s25_header(title='Wedding guests', sub='Round 1', ios=False):
    if ios:
        return f'''<header class="grid h-11 shrink-0 grid-cols-[auto_1fr_auto] items-center px-2">
    <span class="flex size-12 items-center justify-center rounded-full text-primary">{icon("x", "size-6")}</span>
    <div class="min-w-0 text-center"><p class="truncate text-body font-semibold">{title}</p><p class="text-caption text-muted-foreground">{sub}</p></div>
    <span class="flex size-12 items-center justify-center rounded-full text-primary">{icon("ellipsis", "size-6")}</span>
  </header>'''
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    <span class="flex size-12 items-center justify-center rounded-full">{icon("x", "size-6")}</span>
    <div class="min-w-0 flex-1 px-1"><p class="truncate text-title-3">{title}</p><p class="text-caption text-muted-foreground">{sub}</p></div>
    <span class="flex size-12 items-center justify-center rounded-full">{icon("ellipsis-vertical", "size-6")}</span>
  </header>'''


def s25_progress(done, total, extra=''):
    pct = round(done * 100 / total)
    return f'''<div class="shrink-0 px-gutter pb-1">
    <div class="flex items-center justify-between gap-3"><span class="text-label tabular-nums">{done} / {total} decided</span>{extra}</div>
    <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted"><div class="h-full w-[{pct}%] rounded-full bg-primary"></div></div>
  </div>'''


def s25_bar(counts=(17, 11, 48), undo=True):
    r, m, a = counts

    def d(kind, n):
        ic, lab, _, _ = DEC[kind]
        return f'<span class="flex min-w-touch flex-col items-center gap-1.5"><span class="flex size-16 items-center justify-center rounded-full bg-{kind}-soft text-{kind}-soft-foreground">{icon(ic, "size-7")}</span><span class="text-caption">{lab} <span class="tabular-nums text-muted-foreground">{n}</span></span></span>'
    uop = '' if undo else ' opacity-40'
    return f'''<div class="flex shrink-0 items-start justify-between px-5 pb-4 pt-2">
    <span class="flex min-w-touch flex-col items-center gap-1.5{uop}"><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("undo-2")}</span><span class="text-caption text-muted-foreground">Undo</span></span>
    {d('reject', r)}{d('maybe', m)}{d('accept', a)}
    <span class="flex min-w-touch flex-col items-center gap-1.5"><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("sticky-note")}</span><span class="text-caption text-muted-foreground">Note</span></span>
  </div>'''


def s25_stack(body, nxt=S25_ANNA):
    behind = f'<div class="absolute inset-x-gutter bottom-5 top-0 flex origin-top translate-y-10 scale-95 flex-col overflow-hidden rounded-hero border bg-card shadow-raised">{nxt}</div>' if nxt else ''
    return f'''<div class="relative mt-2 min-h-0 flex-1">
    {behind}
    <div class="absolute inset-x-gutter bottom-5 top-0 flex flex-col overflow-hidden rounded-hero bg-card shadow-hero">{body}</div>
  </div>'''


def s25_background(body=S25_MIA, title='Wedding guests', sub='Round 1', done=76, total=100, counts=(17, 11, 48), extra_top='', prog_extra='', nxt=S25_ANNA, ios=False, undo=True):
    """A static, non-interactive copy of the S25 sorting screen, used behind sheets."""
    inner = f'''{s25_header(title, sub, ios)}
  {extra_top}
  {s25_progress(done, total, prog_extra)}
  {s25_stack(body, nxt)}
  {s25_bar(counts, undo)}'''
    return f'<div class="flex min-h-0 flex-1 flex-col" aria-hidden="true">{_strip_interactive(inner)}</div>'


def s25_live(body, title, sub, done, total, counts, overlay='', undo=False, card_label='', extra_top=''):
    """Interactive S25 screen (used for the S24-started result frame)."""
    r, m, a = counts

    def d(kind, n):
        ic, lab, _, past = DEC[kind]
        return f'<button type="button" class="flex min-w-touch flex-col items-center gap-1.5" aria-label="{lab}, {n} {past}" data-action="{kind}"><span class="flex size-16 items-center justify-center rounded-full bg-{kind}-soft text-{kind}-soft-foreground">{icon(ic, "size-7")}</span><span class="text-caption">{lab} <span class="tabular-nums text-muted-foreground">{n}</span></span></button>'
    udis = '' if undo else ' disabled'
    uop = '' if undo else ' opacity-40'
    ulab = 'Undo last decision' if undo else 'Nothing to undo'
    pct = round(done * 100 / total)
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    {icon_btn("x", "Close sorting", None, "close")}
    <div class="min-w-0 flex-1 px-1"><h1 class="truncate text-title-3">{title}</h1><p class="text-caption text-muted-foreground">{sub}</p></div>
    {icon_btn("ellipsis-vertical", "More options", None, "menu")}
  </header>
  {extra_top}
  <div class="shrink-0 px-gutter pb-1">
    <span class="text-label tabular-nums">{done} / {total} decided</span>
    <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="{done}" aria-valuemin="0" aria-valuemax="{total}" aria-label="{done} of {total} decided"><div class="h-full w-[{pct}%] rounded-full bg-primary"></div></div>
  </div>
  <div class="relative mt-2 min-h-0 flex-1">
    <div class="absolute inset-x-gutter bottom-5 top-0 flex origin-top translate-y-10 scale-95 flex-col overflow-hidden rounded-hero border bg-card shadow-raised" aria-hidden="true"></div>
    <article class="absolute inset-x-gutter bottom-5 top-0 flex flex-col overflow-hidden rounded-hero bg-card shadow-hero" aria-label="{card_label}" aria-roledescription="card" tabindex="0">{_strip_interactive(body)}</article>
  </div>
  <div class="flex shrink-0 items-start justify-between px-5 pb-4 pt-2">
    <button type="button" class="flex min-w-touch flex-col items-center gap-1.5{uop}" aria-label="{ulab}" data-action="undo"{udis}><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("undo-2")}</span><span class="text-caption text-muted-foreground">Undo</span></button>
    {d('reject', r)}{d('maybe', m)}{d('accept', a)}
    <button type="button" class="flex min-w-touch flex-col items-center gap-1.5" aria-label="Add note" data-action="note"><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("sticky-note")}</span><span class="text-caption text-muted-foreground">Note</span></button>
  </div>
  {overlay}'''
