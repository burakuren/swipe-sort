# Shared helpers for group C2 import screens (S16–S21).
# Each screen generator imports this module:  python3 tools/generators/S19-field-mapping.py
# Markup follows design/01-foundations/components.html and the S25 reference frames.
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCREENS = os.path.join(ROOT, 'design', '03-screens')
ICONS = os.path.join(ROOT, 'node_modules', 'lucide-static', 'icons')
IMG = '../02-data/images/'
DATA = json.load(open(os.path.join(ROOT, 'design', '02-data', 'sample-data.json'), encoding='utf-8'))
CONTACTS = {c['id']: c for c in DATA['contacts']}

_missing_icons = set()


def icon(name, size='size-5', extra=''):
    if not os.path.exists(os.path.join(ICONS, name + '.svg')):
        _missing_icons.add(name)
    cls = f'i-lucide-{name} {size} {extra}'.strip()
    return f'<i class="{cls}" aria-hidden="true"></i>'


# ---------------------------------------------------------------- frames and page
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


def desktop(content, url):
    return f'''<div class="desktop">
  <div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">{url}</span></div>
  <div class="desktop-column">
  {content}
  </div>
</div>'''


class Page:
    def __init__(self, sid, title, intro):
        self.sid, self.title, self.intro = sid, title, intro
        self.parts = []

    def section(self, title, desc):
        self.parts.append(f'</main>\n<h2 class="mock-section">{title}</h2>\n<p>{desc}</p>\n<main class="mock-canvas">')

    def frame(self, fid, label, inner):
        assert fid.startswith(self.sid + '-'), fid
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
  <p>{self.intro}</p>
</header>
<main class="mock-canvas">
{''.join(self.parts)}
</main>
</body>
</html>
'''
        html = html.replace('<main class="mock-canvas">\n</main>\n', '', 1)
        out = os.path.join(SCREENS, filename)
        open(out, 'w', encoding='utf-8').write(html)
        ids = html.count('data-frame=')
        if _missing_icons:
            print('MISSING ICONS:', sorted(_missing_icons), file=sys.stderr)
            sys.exit(1)
        print(f'{filename}: {ids} frames')


# ---------------------------------------------------------------- app bars and stepper
def modal_bar(title='Import', close_href='S08-home.html#S08-default', close_label='Close import', action='', ios=False, back=None):
    """Modal app bar (components.html C-navigation): close x + title + optional text action.
    iOS: 44 pt bar, centered title; first step shows x in primary at the left, later steps a back chevron
    (edge-swipe back) with x at the right."""
    if ios:
        if back:
            left = f'<a href="{back[1]}" class="inline-flex h-12 items-center gap-0.5 justify-self-start pr-2 text-body text-primary" aria-label="Back to {back[0]}">{icon("chevron-left", "size-6")}Back</a>'
            right = action or f'<a href="{close_href}" class="ml-auto flex size-12 items-center justify-center rounded-full text-primary" aria-label="{close_label}" data-action="close">{icon("x", "size-6")}</a>'
        else:
            left = f'<a href="{close_href}" class="flex size-12 items-center justify-center rounded-full text-primary" aria-label="{close_label}" data-action="close">{icon("x", "size-6")}</a>'
            right = action or '<span></span>'
        return f'''<header class="grid h-11 shrink-0 grid-cols-[1fr_auto_1fr] items-center px-2">
    {left}
    <h1 class="text-body font-semibold">{title}</h1>
    <div class="flex justify-end">{right}</div>
  </header>'''
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    <a href="{close_href}" class="flex size-12 items-center justify-center rounded-full" aria-label="{close_label}" data-action="close">{icon("x", "size-6")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-3">{title}</h1>
    {action}
  </header>'''


def stepper(name, n, total):
    segs = ''.join(f'<span class="h-1 flex-1 rounded-full {"bg-primary" if i <= n else "bg-muted"}"></span>' for i in range(1, total + 1))
    return f'''<div class="shrink-0 px-gutter pb-3 pt-1">
    <div class="flex items-baseline justify-between gap-3"><p class="text-label">{name}</p><p class="shrink-0 text-caption tabular-nums text-muted-foreground">Step {n} of {total}</p></div>
    <div class="mt-2 flex gap-1" role="progressbar" aria-valuenow="{n}" aria-valuemin="1" aria-valuemax="{total}" aria-label="Step {n} of {total}, {name}">{segs}</div>
  </div>'''


# ---------------------------------------------------------------- buttons
PRIMARY = 'flex h-14 w-full items-center justify-center gap-2 rounded-control bg-primary px-6 text-label-lg text-primary-foreground'


def bottom(label, href=None, action=None, disabled=False, note='', secondary='', busy=False, border=True):
    """Bottom action area: full-width primary h-14 (+ optional note above, ghost secondary below)."""
    note_html = f'<p class="mb-3 text-body-sm text-muted-foreground">{note}</p>' if note else ''
    da = f' data-action="{action}"' if action else ''
    if disabled:
        btn = f'<button class="{PRIMARY} opacity-50" disabled>{label}</button>'
    elif busy:
        btn = f'<button class="{PRIMARY}" aria-busy="true" disabled>{icon("loader-circle", "size-5 animate-spin")}{label}</button>'
    elif href:
        btn = f'<a href="{href}" class="{PRIMARY}"{da}>{label}</a>'
    else:
        btn = f'<button class="{PRIMARY}"{da}>{label}</button>'
    bt = 'border-t' if border else ''
    return f'''<div class="shrink-0 {bt} bg-background px-gutter pb-4 pt-3">
    {note_html}{btn}{secondary}
  </div>'''


def ghost_full(label, href='#', action=None):
    da = f' data-action="{action}"' if action else ''
    return f'<a href="{href}" class="mt-1 flex h-12 w-full items-center justify-center rounded-control px-5 text-label-lg"{da}>{label}</a>'


def btn(label, variant='outline', ic=None, href=None, size='h-12', extra='', action=None, aria=None, disabled=False):
    base = {
        'primary': 'bg-primary text-primary-foreground',
        'secondary': 'bg-secondary text-secondary-foreground',
        'outline': 'border border-input bg-card',
        'ghost': '',
        'destructive': 'bg-destructive text-destructive-foreground',
        'ghost-destructive': 'text-destructive',
        'link': 'text-primary underline underline-offset-4',
    }[variant]
    pad = 'px-1' if variant == 'link' else 'px-4'
    ic_html = icon(ic) if ic else ''
    da = f' data-action="{action}"' if action else ''
    ar = f' aria-label="{aria}"' if aria else ''
    dis = ' disabled' if disabled else ''
    op = ' opacity-50' if disabled else ''
    cls = f'inline-flex {size} items-center justify-center gap-2 rounded-control {pad} text-label-lg {base}{op} {extra}'.strip()
    if href and not disabled:
        return f'<a href="{href}" class="{cls}"{da}{ar}>{ic_html}{label}</a>'
    return f'<button class="{cls}"{da}{ar}{dis}>{ic_html}{label}</button>'


def icon_btn(ic, label, href=None, extra='', size='size-5', action=None):
    da = f' data-action="{action}"' if action else ''
    cls = f'flex size-12 shrink-0 items-center justify-center rounded-full {extra}'.strip()
    if href:
        return f'<a href="{href}" class="{cls}" aria-label="{label}"{da}>{icon(ic, size)}</a>'
    return f'<button class="{cls}" aria-label="{label}"{da}>{icon(ic, size)}</button>'


# ---------------------------------------------------------------- controls
def switch(on, label, disabled=False, extra=''):
    """M3 switch inside a 48 target. `label` is the accessible name."""
    dis = ' disabled' if disabled else ''
    op = ' opacity-50' if disabled else ''
    if on:
        track = '<span class="flex h-8 w-13 items-center rounded-full bg-primary p-1"><span class="ml-auto size-6 rounded-full bg-primary-foreground"></span></span>'
    else:
        track = '<span class="flex h-8 w-13 items-center rounded-full border-2 border-input bg-muted p-1"><span class="size-5 rounded-full bg-muted-foreground"></span></span>'
    return f'<button role="switch" aria-checked="{"true" if on else "false"}" aria-label="{label}" class="flex min-h-touch shrink-0 items-center{op} {extra}"{dis}>{track}</button>'


def checkbox_box(state):
    if state is True:
        return f'<span class="flex size-6 shrink-0 items-center justify-center rounded-sm bg-primary text-primary-foreground">{icon("check", "size-4")}</span>'
    if state == 'mixed':
        return f'<span class="flex size-6 shrink-0 items-center justify-center rounded-sm bg-primary text-primary-foreground">{icon("minus", "size-4")}</span>'
    return '<span class="size-6 shrink-0 rounded-sm border-2 border-input bg-card"></span>'


def radio_dot(on):
    if on:
        return '<span class="flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary"><span class="size-3 rounded-full bg-primary"></span></span>'
    return '<span class="size-6 shrink-0 rounded-full border-2 border-input"></span>'


def badge(text, ic=None, tone='secondary'):
    cls = {
        'secondary': 'bg-secondary text-secondary-foreground',
        'primary': 'bg-primary-soft text-primary-soft-foreground',
        'outline': 'border',
        'muted': 'bg-muted text-muted-foreground',
        'accept': 'bg-accept-soft text-accept-soft-foreground',
        'reject': 'bg-reject-soft text-reject-soft-foreground',
        'maybe': 'bg-maybe-soft text-maybe-soft-foreground',
        'dashed': 'border border-dashed border-input text-muted-foreground',
    }[tone]
    ic_html = icon(ic, 'size-4') if ic else ''
    return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full px-2.5 text-caption {cls}">{ic_html}{text}</span>'


def label_input(fid, label, value='', placeholder='', helper='', error='', focused=False, suffix='', required=False, ty='text'):
    req = ' <span class="text-muted-foreground">(required)</span>' if required else ''
    if error:
        border = 'border-2 border-destructive'
    elif focused:
        border = 'border border-primary ring-2 ring-ring/30'
    else:
        border = 'border border-input'
    desc = ''
    aria = ''
    if error:
        desc = f'<p id="{fid}-e" class="mt-1.5 flex items-start gap-1.5 text-caption text-destructive">{icon("circle-alert", "size-4 shrink-0")}<span>{error}</span></p>'
        aria = f' aria-invalid="true" aria-describedby="{fid}-e"'
    elif helper:
        desc = f'<p id="{fid}-h" class="mt-1.5 text-caption text-muted-foreground">{helper}</p>'
        aria = f' aria-describedby="{fid}-h"'
    val = f' value="{value}"' if value else ''
    ph = f' placeholder="{placeholder}"' if placeholder else ''
    if suffix:
        field = f'<div class="mt-1.5 flex h-12 items-center rounded-control {border} bg-card"><input id="{fid}" type="{ty}" class="h-full min-w-0 flex-1 rounded-control bg-transparent px-3.5 text-body placeholder:text-muted-foreground"{val}{ph}{aria}><span class="pr-3.5 text-body text-muted-foreground">{suffix}</span></div>'
    else:
        field = f'<input id="{fid}" type="{ty}" class="mt-1.5 h-12 w-full rounded-control {border} bg-card px-3.5 text-body placeholder:text-muted-foreground"{val}{ph}{aria}>'
    return f'<div><label class="text-label" for="{fid}">{label}{req}</label>{field}{desc}</div>'


def select_trigger(value, label, extra='', ic=None, error=False, placeholder=False):
    border = 'border-2 border-destructive' if error else 'border border-input'
    ic_html = icon(ic, 'size-5 text-muted-foreground') if ic else ''
    tcls = 'text-muted-foreground' if placeholder else ''
    return f'<button class="flex h-12 w-full items-center gap-2 rounded-control {border} bg-card px-3.5 text-left text-body {extra}" aria-haspopup="dialog" aria-label="{label}">{ic_html}<span class="min-w-0 flex-1 truncate {tcls}">{value}</span>{icon("chevron-down", "size-5 text-muted-foreground")}</button>'


# ---------------------------------------------------------------- feedback
def alert(kind, title, body='', actions='', ic=None, role=None):
    if kind == 'info':
        cls = 'bg-primary-soft text-primary-soft-foreground'
        ic = ic or 'info'
        body_cls = 'text-body-sm'
        role = role or 'note'
        icls = ''
    elif kind == 'error':
        cls = 'border border-destructive/40 bg-card'
        ic = ic or 'circle-alert'
        body_cls = 'text-body-sm text-muted-foreground'
        role = role or 'alert'
        icls = 'text-destructive'
    else:  # neutral
        cls = 'border bg-card'
        ic = ic or 'info'
        body_cls = 'text-body-sm text-muted-foreground'
        role = role or 'note'
        icls = 'text-muted-foreground'
    b = f'<p class="mt-0.5 {body_cls}">{body}</p>' if body else ''
    a = f'<div class="mt-2 flex flex-wrap gap-x-4">{actions}</div>' if actions else ''
    return f'<div class="flex gap-3 rounded-control {cls} p-4" role="{role}">{icon(ic, f"size-5 shrink-0 {icls}".strip())}<div class="min-w-0 flex-1"><p class="text-label">{title}</p>{b}{a}</div></div>'


def alert_link(label, href='#', action=None):
    da = f' data-action="{action}"' if action else ''
    return f'<a href="{href}" class="inline-flex min-h-touch items-center text-label text-primary underline underline-offset-4"{da}>{label}</a>'


def alert_button(label, action=None):
    da = f' data-action="{action}"' if action else ''
    return f'<button class="inline-flex min-h-touch items-center text-label text-primary underline underline-offset-4"{da}>{label}</button>'


def offline_banner(text="You're offline. Local sources still work."):
    return f'<div class="flex shrink-0 items-center gap-2 bg-muted px-gutter py-2 text-body-sm" role="status">{icon("wifi-off", "size-4 shrink-0")}<span class="flex-1">{text}</span></div>'


def snackbar(text, action=None, bottom='bottom-28', role='status', icon_name=None, action_href=None):
    if action and action_href:
        act = f'<a href="{action_href}" class="-my-1 inline-flex h-12 items-center rounded-sm px-3 text-label text-primary-inverse">{action}</a>'
    elif action:
        act = f'<button class="-my-1 inline-flex h-12 items-center rounded-sm px-3 text-label text-primary-inverse">{action}</button>'
    else:
        act = ''
    ic = icon(icon_name, 'size-5 shrink-0') if icon_name else ''
    pad = 'py-1.5 pl-4 pr-1.5' if action else 'px-4 py-3'
    return f'<div class="absolute inset-x-4 {bottom} z-30 flex min-h-12 items-center gap-3 rounded-control bg-foreground {pad} text-background shadow-overlay" role="{role}">{ic}<span class="flex-1 text-body-sm">{text}</span>{act}</div>'


def scrim(z='z-10', op='bg-scrim/50'):
    return f'<div class="absolute inset-0 {z} {op}"></div>'


def sheet(sid, title, body, actions='', top=None, close=True, subtitle=''):
    """Android bottom sheet (M3): handle, title row, content, bottom actions. `top` makes it tall (e.g. 'top-16')."""
    pos = f'{top} ' if top else ''
    flex = 'flex flex-col ' if top else ''
    cl = f'<button class="-mr-3 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</button>' if close else ''
    sub = f'<p class="mt-0.5 text-body-sm text-muted-foreground">{subtitle}</p>' if subtitle else ''
    act = f'<div class="shrink-0 pt-3">{actions}</div>' if actions else ''
    return f'''{scrim()}
  <div class="absolute inset-x-0 bottom-0 {pos}z-20 {flex}rounded-t-sheet bg-popover px-gutter pb-6 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="{sid}">
    <div class="flex shrink-0 justify-center py-1.5"><span class="h-1 w-8 rounded-full bg-muted-foreground/40"></span></div>
    <div class="flex shrink-0 {"items-start" if subtitle else "items-center"} justify-between gap-2 pt-2"><div class="min-w-0"><h2 id="{sid}" class="text-title-3">{title}</h2>{sub}</div>{cl}</div>
    {body}
    {act}
  </div>'''


def ios_sheet(sid, title, body, left='Cancel', right='Done', top='top-12'):
    """iOS page sheet with grabber and Cancel / Done in its own nav bar."""
    return f'''{scrim(op='bg-scrim/40')}
  <div class="absolute inset-x-0 bottom-0 {top} z-20 flex flex-col rounded-t-sheet bg-popover px-5 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="{sid}">
    <div class="flex shrink-0 justify-center py-1.5"><span class="h-1 w-9 rounded-full bg-muted-foreground/40"></span></div>
    <div class="grid shrink-0 grid-cols-[1fr_auto_1fr] items-center pt-1"><button class="inline-flex h-12 items-center justify-self-start px-1 text-body text-primary">{left}</button><h2 id="{sid}" class="text-body font-semibold">{title}</h2><button class="inline-flex h-12 min-w-12 items-center justify-end justify-self-end px-1 text-body font-semibold text-primary">{right}</button></div>
    {body}
  </div>'''


def dialog(did, title, body, actions):
    return f'''{scrim()}
  <div class="absolute inset-x-6 top-1/3 z-20 rounded-dialog bg-popover p-6 shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="{did}" aria-describedby="{did}-d">
    <h2 id="{did}" class="text-title-3">{title}</h2>
    <p id="{did}-d" class="mt-2 text-body text-muted-foreground">{body}</p>
    <div class="mt-6 flex flex-wrap justify-end gap-2">{actions}</div>
  </div>'''


def spinner_line(text):
    return f'<div class="flex items-center gap-3 text-body text-muted-foreground" role="status">{icon("loader-circle", "size-6 animate-spin text-primary")}{text}</div>'


# ---------------------------------------------------------------- data helpers
TYPES = {
    'text': ('type', 'Text'),
    'number': ('hash', 'Number'),
    'phone': ('phone', 'Phone'),
    'email': ('mail', 'Email'),
    'date': ('calendar', 'Date'),
    'link': ('link', 'Link'),
    'image': ('image', 'Image'),
}


def initials(name):
    parts = [p for p in name.replace('(', ' ').replace(')', ' ').split() if p[0].isalpha()]
    if not parts:
        return '?'
    return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else '')).upper()


def avatar(cid=None, name=None, size='size-10', photo=None, text='text-label'):
    if cid:
        c = CONTACTS[cid]
        name = c['name']
        photo = c.get('photo')
    if photo:
        return f'<img src="{IMG}{photo.replace("images/", "")}" alt="" class="{size} shrink-0 rounded-full object-cover">'
    return f'<span class="flex {size} shrink-0 items-center justify-center rounded-full bg-muted {text} text-muted-foreground" aria-hidden="true">{initials(name)}</span>'


def fmt_int(n):
    return f'{n:,}'
