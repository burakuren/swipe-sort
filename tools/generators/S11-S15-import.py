# Usage: python3 tools/generators/S11-S15-import.py
# Generates the Group C1 import screens (static mockup frames) into design/03-screens/:
#   S11-source-picker.html, S12-permissions.html, S13-contacts-import.html,
#   S14-file-import.html, S15-google-sheets.html
# Shared import chrome (modal app bar, ImportStepper, bottom actions) is defined once here so every
# source looks and behaves the same (design goal 5).
import json
import os
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCREENS = os.path.join(ROOT, 'design', '03-screens')
DATA = json.load(open(os.path.join(ROOT, 'design', '02-data', 'sample-data.json'), encoding='utf-8'))
IMG = '../02-data/images/'
GET_APP = 'https://swipesort.app/get'


# =====================================================================================
# Primitives
# =====================================================================================
def icon(name, size='size-5', extra=''):
    cls = ' '.join(x for x in (f'i-lucide-{name}', size, extra) if x)
    return f'<i class="{cls}" aria-hidden="true"></i>'


def phone(content, kind='android'):
    """kind: android | ios (page sheet presentation) | web (mobile browser, no system bars)."""
    if kind == 'web':
        return f'''<div class="phone">
  <div class="screen">
  {content}
  </div>
</div>'''
    if kind == 'ios':
        return f'''<div class="phone-ios bg-muted">
  <div class="sysbar-top" aria-hidden="true"><span>9:41</span><span class="sysbar-icons"></span></div>
  <div class="screen">
  <div class="h-2.5 shrink-0" aria-hidden="true"></div>
  <div class="relative flex min-h-0 flex-1 flex-col overflow-hidden rounded-t-sheet bg-background">
  {content}
  </div>
  </div>
  <div class="sysbar-nav bg-background" aria-hidden="true"></div>
</div>'''
    return f'''<div class="phone">
  <div class="sysbar-top" aria-hidden="true"><span>9:41</span><span class="sysbar-icons"></span></div>
  <div class="screen">
  {content}
  </div>
  <div class="sysbar-nav" aria-hidden="true"></div>
</div>'''


def desktop(content, url='swipesort.app/new'):
    return f'''<div class="desktop">
  <div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">{url}</span></div>
  <div class="desktop-column">
  {content}
  </div>
</div>'''


class Page:
    def __init__(self, sid, file, title, intro):
        self.sid, self.file, self.title, self.intro = sid, file, title, intro
        self.parts = []

    def section(self, title, desc):
        self.parts.append(('section', title, desc))

    def frame(self, fid, label, inner):
        assert fid.startswith(self.sid + '-'), fid
        self.parts.append(('frame', fid, label, inner))

    def render(self):
        out, open_main = [], False
        for p in self.parts:
            if p[0] == 'section':
                if open_main:
                    out.append('</main>')
                out.append(f'<h2 class="mock-section">{p[1]}</h2>\n<p>{p[2]}</p>\n<main class="mock-canvas">')
                open_main = True
            else:
                _, fid, label, inner = p
                out.append(f'''
<figure class="frame" data-frame="{fid}" id="{fid}">
  <figcaption class="frame-label">{self.sid} · {label} · <span class="theme-name"></span></figcaption>
  {inner}
</figure>''')
        if open_main:
            out.append('</main>')
        spec = self.file.replace('.html', '.md')
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
  <p>{self.intro} Spec: <a href="{spec}">{spec}</a>. Shared import chrome (modal app bar, ImportStepper, bottom actions) matches S16–S21.</p>
</header>
{chr(10).join(out)}
</body>
</html>
'''
        html = html.replace("'", '\'')
        with open(os.path.join(SCREENS, self.file), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'{self.file}: {html.count("data-frame=")} frames')


# =====================================================================================
# Shared import chrome
# =====================================================================================
HOME = 'S08-home.html#S08-default'
WEDDING = 'S09-list-overview.html#S09-shared'


def appbar(title='Import', close_href=HOME, close_label='Close import', trailing='', big=False):
    t = 'text-title-2' if big else 'text-title-3'
    ic = 'size-7' if big else 'size-6'
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    <a href="{close_href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{close_label}" data-action="close">{icon("x", ic)}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 {t}">{title}</h1>{trailing}
  </header>'''


BACK_S11 = ('Choose source', 'S11-source-picker.html#S11-ios')


def iosbar(title='Import', back=BACK_S11, close_href=HOME, close_label='Close import'):
    """iOS import bar (same as C2): 44 pt, centered title. First step: x at the left. Later steps: back
    chevron at the left (edge-swipe back) and x at the right."""
    x = f'<a href="{close_href}" class="flex size-12 items-center justify-center rounded-full text-primary" aria-label="{close_label}" data-action="close">{icon("x", "size-6")}</a>'
    if back:
        left = f'<a href="{back[1]}" class="inline-flex h-12 items-center gap-0.5 justify-self-start pr-2 text-body text-primary" aria-label="Back to {back[0]}">{icon("chevron-left", "size-6")}Back</a>'
        right = x.replace('class="flex size-12', 'class="ml-auto flex size-12')
    else:
        left, right = x, '<span></span>'
    return f'''<header class="grid h-11 shrink-0 grid-cols-[1fr_auto_1fr] items-center px-2">
    {left}
    <h1 class="text-body font-semibold">{title}</h1>
    <div class="flex justify-end">{right}</div>
  </header>'''


STEPS5 = ['Choose source', 'Select items', 'Map fields', 'Review duplicates', 'Finish']
STEPS4 = ['Choose source', 'Select items', 'Review duplicates', 'Finish']  # manual entry
STEPS3 = ['Choose source', 'Select items', 'Finish']  # photos (A-62)


def stepper(n, total=5, big=False):
    name = {5: STEPS5, 4: STEPS4, 3: STEPS3}[total][n - 1]
    segs = ''.join(f'<span class="h-1 flex-1 rounded-full {"bg-primary" if i <= n else "bg-muted"}"></span>' for i in range(1, total + 1))
    lt, ct = ('text-title-3', 'text-body-lg') if big else ('text-label', 'text-caption')
    return f'''<div class="shrink-0 px-gutter pb-3 pt-1">
    <div class="flex items-baseline justify-between gap-3"><p class="{lt}">{name}</p><p class="{ct} shrink-0 tabular-nums text-muted-foreground">Step {n} of {total}</p></div>
    <div class="mt-2 flex gap-1" role="progressbar" aria-valuenow="{n}" aria-valuemin="1" aria-valuemax="{total}" aria-label="Step {n} of {total}, {name}">{segs}</div>
  </div>'''


def btn(label, href=None, action=None, variant='primary', disabled=False, busy=False, full=True, size='lg', extra=''):
    base = {
        'primary': 'bg-primary text-primary-foreground',
        'secondary': 'bg-secondary text-secondary-foreground',
        'outline': 'border border-input bg-card',
        'ghost': '',
        'destructive': 'bg-destructive text-destructive-foreground',
    }[variant]
    h = 'h-14 px-6' if size == 'lg' else 'h-12 px-5'
    if ' px-' in ' ' + extra:
        h = h.split()[0]
    w = 'flex w-full' if full else 'inline-flex'
    cls = f'{w} {h} items-center justify-center gap-2 rounded-control text-label-lg {base} {extra}'.strip()
    da = f' data-action="{action}"' if action else ''
    inner = (icon('loader-circle', 'size-5 animate-spin') if busy else '') + label
    if disabled:
        return f'<button class="{cls} opacity-50" disabled{da}>{inner}</button>'
    if busy:
        return f'<button class="{cls}" aria-busy="true"{da}>{inner}</button>'
    if href:
        return f'<a href="{href}" class="{cls}"{da}>{inner}</a>'
    return f'<button class="{cls}"{da}>{inner}</button>'


def bottom(primary=None, secondary=None, note='', border=True, extra=''):
    """Import bottom actions (identical to C2): optional note, full-width primary h-14, ghost secondary below."""
    b = 'border-t ' if border else ''
    n = f'<p class="mb-3 text-body-sm text-muted-foreground">{note}</p>' if note else ''
    sec = f'<div class="{"mt-1" if primary else ""}">{secondary}</div>' if secondary else ''
    return f'''<div class="shrink-0 {b}bg-background px-gutter pb-4 pt-3">
    {n}{extra}{primary or ''}{sec}
  </div>'''


def offline_banner(text="You're offline. Changes are saved on this phone. Google Sheets needs a connection."):
    return f'<div class="flex shrink-0 items-center gap-2 bg-muted px-gutter py-2 text-body-sm" role="status">{icon("wifi-off", "size-4 shrink-0")}<span class="flex-1">{text}</span></div>'


def snackbar(text, action=None, bottom_cls='bottom-6', role='status', icon_name=None):
    act = f'<button class="-my-1 inline-flex h-12 items-center rounded-sm px-3 text-label text-primary-inverse">{action}</button>' if action else ''
    ic = icon(icon_name, 'size-5 shrink-0') if icon_name else ''
    pad = 'py-1.5 pl-4 pr-1.5' if action else 'px-4 py-3'
    return f'<div class="absolute inset-x-4 {bottom_cls} z-10 flex min-h-12 items-center gap-3 rounded-control bg-foreground {pad} text-background shadow-overlay" role="{role}">{ic}<span class="flex-1 text-body-sm">{text}</span>{act}</div>'


def sheet(sid, title, body, actions='', close_href=None, z=''):
    close = (f'<a href="{close_href}" class="-mr-3 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</a>' if close_href
             else f'<button class="-mr-3 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</button>')
    return f'''<div class="absolute inset-0 z-10 bg-scrim/50"></div>
  <div class="absolute inset-x-0 bottom-0 z-20 rounded-t-sheet bg-popover px-gutter pb-5 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="{sid}">
    <div class="flex justify-center py-1.5"><span class="h-1 w-8 rounded-full bg-muted-foreground/40"></span></div>
    <div class="flex items-center justify-between gap-3 pt-2"><h2 id="{sid}" class="text-title-3">{title}</h2>{close}</div>
    {body}
    <div class="mt-5 space-y-1">{actions}</div>
  </div>'''


def dialog(did, title, body, actions):
    """AlertDialog with the S40 wrapper: scrim + vertically centred dialog (A-112)."""
    return f'''<div class="absolute inset-0 z-30 bg-scrim/50" aria-hidden="true"></div>
  <div class="absolute inset-0 z-40 flex items-center justify-center px-6">
    <div class="w-full max-w-sm rounded-dialog bg-popover p-6 shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="{did}" aria-describedby="{did}d">
      <h2 id="{did}" class="text-title-3">{title}</h2>
      <div id="{did}d" class="mt-2 space-y-2 text-body text-muted-foreground"><p>{body}</p></div>
      <div class="mt-6 flex flex-wrap justify-end gap-2">{actions}</div>
    </div>
  </div>'''


def state(ic, title, body, extra='', tone='muted'):
    icn = icon(ic, 'size-8 text-muted-foreground') if tone == 'muted' else icon(ic, 'size-8 text-destructive')
    return f'''<div class="flex min-h-0 flex-1 flex-col items-center justify-center px-8 pb-8 text-center">
    {icn}
    <h2 class="mt-4 text-title-3">{title}</h2>
    <p class="mt-1 max-w-xs text-body text-muted-foreground">{body}</p>
    {extra}
  </div>'''


def checkbox(state_='on', round_=False):
    r = 'rounded-full' if round_ else 'rounded-sm'
    if state_ == 'on':
        return f'<span class="flex size-6 shrink-0 items-center justify-center {r} bg-primary text-primary-foreground" aria-hidden="true">{icon("check", "size-4")}</span>'
    if state_ == 'mixed':
        return f'<span class="flex size-6 shrink-0 items-center justify-center {r} bg-primary text-primary-foreground" aria-hidden="true">{icon("minus", "size-4")}</span>'
    return f'<span class="size-6 shrink-0 {r} border-2 border-input" aria-hidden="true"></span>'


def switch_vis(on=True):
    if on:
        return '<span class="flex h-8 w-13 shrink-0 items-center rounded-full bg-primary p-1" aria-hidden="true"><span class="ml-auto size-6 rounded-full bg-primary-foreground"></span></span>'
    return '<span class="flex h-8 w-13 shrink-0 items-center rounded-full border-2 border-input bg-muted p-1" aria-hidden="true"><span class="size-5 rounded-full bg-muted-foreground"></span></span>'


def info_alert(title, body='', ic='info', extra=''):
    b = f'<p class="mt-0.5 text-body-sm">{body}</p>' if body else ''
    return f'<div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground" role="note">{icon(ic, "size-5 shrink-0")}<div class="min-w-0 flex-1"><p class="text-label">{title}</p>{b}{extra}</div></div>'


def error_alert(title, body='', extra=''):
    return f'<div class="flex gap-3 rounded-control border border-destructive/40 bg-card p-4" role="alert">{icon("circle-alert", "size-5 shrink-0 text-destructive")}<div class="min-w-0 flex-1"><p class="text-label">{title}</p><p class="mt-0.5 text-body-sm text-muted-foreground">{body}</p>{extra}</div></div>'


def safety_note(text='SwipeSort imports a copy. Your contacts, files and sheets are never changed.'):
    return f'<p class="flex gap-2 text-body-sm text-muted-foreground">{icon("shield-check", "size-4 mt-0.5 shrink-0")}<span>{text}</span></p>'


def search_field(fid, value='', placeholder='Search name or number', label='Search contacts', big=False, round_='rounded-full'):
    clear = f'<button class="absolute right-0 top-0 flex size-12 items-center justify-center rounded-full" aria-label="Clear search">{icon("x", "size-5 text-muted-foreground")}</button>' if value else ''
    h, t = ('h-14', 'text-body-lg') if big else ('h-12', 'text-body')
    top = 'top-4' if big else 'top-3.5'
    return f'''<div class="relative"><label for="{fid}" class="sr-only">{label}</label>{icon("search", "size-5", f"pointer-events-none absolute left-3.5 {top} text-muted-foreground")}<input id="{fid}" type="search" class="{h} w-full {round_} border-0 bg-secondary pl-11 pr-12 {t} placeholder:text-muted-foreground" placeholder="{placeholder}" value="{value}">{clear}</div>'''


# =====================================================================================
# Sources (each tile is one Source definition, see domain-model.md)
# =====================================================================================
SOURCES = [
    dict(id='contacts', name='Contacts', icon='contact', desc='From this phone', href='S12-permissions.html#S12-contacts'),
    dict(id='csv', name='CSV or Excel', icon='file-spreadsheet', desc='A .csv or .xlsx file', href='S14-file-import.html#S14-default'),
    dict(id='google', name='Google Sheets', icon='sheet', desc='From Google Drive', href='S15-google-sheets.html#S15-default'),
    dict(id='text', name='Plain text', icon='text', desc='Paste a list or a .txt file', href='S16-plain-text.html#S16-default'),
    dict(id='manual', name='Manual entry', icon='square-pen', desc='Type items one by one', href='S17-manual-entry.html#S17-default'),
    dict(id='photos', name='Photos', icon='images', desc='From your gallery', href='S12-permissions.html#S12-photos'),
]


def tile(s, state_='ok', big=False):
    if state_ in ('web', 'offline'):
        ic2, desc, href = ('monitor-smartphone', 'Needs the Android or iOS app', '#S11-web-unavailable') if state_ == 'web' else ('wifi-off', 'Needs a connection', '#S11-offline-tapped')
        return f'''<a href="{href}" class="flex min-h-28 flex-col justify-start gap-3 rounded-tile border border-dashed border-input bg-transparent p-4" aria-haspopup="dialog" data-action="source-{s["id"]}"><span class="flex w-full items-start justify-between">{icon(s["icon"], "size-6 text-muted-foreground")}{icon(ic2, "size-4 text-muted-foreground")}</span><span><span class="block text-label-lg text-muted-foreground">{s["name"]}</span><span class="block text-caption text-muted-foreground">{desc}</span></span></a>'''
    if big:
        return f'''<a href="{s["href"]}" class="flex min-h-20 items-center gap-4 rounded-tile border bg-card px-4 py-4" data-action="source-{s["id"]}">{icon(s["icon"], "size-7 shrink-0 text-primary")}<span class="min-w-0"><span class="block text-title-1">{s["name"]}</span><span class="block text-title-3 font-normal text-muted-foreground">{s["desc"]}</span></span></a>'''
    return f'''<a href="{s["href"]}" class="flex min-h-28 flex-col justify-start gap-3 rounded-tile border bg-card p-4" data-action="source-{s["id"]}">{icon(s["icon"], "size-6 text-primary")}<span><span class="block text-label-lg">{s["name"]}</span><span class="block text-caption text-muted-foreground">{s["desc"]}</span></span></a>'''


def tiles(states=None, override=None, extra_tiles=''):
    states = states or {}
    override = override or {}
    out = []
    for s in SOURCES:
        s2 = dict(s, **override.get(s['id'], {}))
        out.append(tile(s2, states.get(s['id'], 'ok')))
    return f'<div class="mt-6 grid auto-rows-fr grid-cols-2 gap-3">{"".join(out)}{extra_tiles}</div>'


# =====================================================================================
# S11 Source picker
# =====================================================================================
def build_s11():
    p = Page('S11', 'S11-source-picker.html', 'Source picker',
             'Step 1 of every import. Each tile is one Source definition; a new source is one more tile that reuses the same steps (Select items, Map fields, Review duplicates, Finish).')

    def body(grid, heading='Where are your items?', sub='Choose a source. You can add items from other sources later.', extra='', note=True):
        n = f'<div class="mt-auto pt-6">{safety_note()}</div>' if note else ''
        return f'''<div class="flex min-h-0 flex-1 flex-col px-gutter pb-5 pt-1">
    <h2 class="text-title-2">{heading}</h2>
    <p class="mt-1 text-body text-muted-foreground">{sub}</p>
    {grid}
    {extra}
    {n}
  </div>'''

    p.section('Source picker', 'Android reference. Tapping a tile opens that source\'s Select items step; contacts and photos first show the pre-permission explainer (S12) unless access was already granted.')
    p.frame('S11-default', 'Default: new list (Android)', phone(f'{appbar()}{stepper(1)}{body(tiles())}'))

    existing = f'''<h3 class="mt-7 px-1 pb-2 text-label text-muted-foreground">Already in Wedding guests</h3>
    <ul class="divide-y overflow-hidden rounded-group bg-card">
      <li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon("contact", "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">Contacts</span><span class="block text-body-sm text-muted-foreground">88 items, added Sep 27</span></span></li>
      <li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon("file-spreadsheet", "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block truncate text-body">mert-family.csv</span><span class="block text-body-sm text-muted-foreground">12 items, added Sep 28</span></span></li>
    </ul>
    <p class="mt-2 flex gap-2 px-1 text-body-sm text-muted-foreground">{icon("combine", "size-4 mt-0.5 shrink-0")}<span>A list can combine any sources. New items are checked for duplicates before they're added.</span></p>'''
    p.frame('S11-existing-list', 'Adding items to an existing list (from S21)', phone(f'''{appbar("Add items", WEDDING, "Close, back to Wedding guests")}{stepper(1)}{body(tiles(), "Add items to Wedding guests", "Choose where the new items come from. They join the current round.", existing, note=False)}'''))

    p.frame('S11-offline', 'Offline: Google Sheets unavailable, other sources work', phone(f'''{appbar()}{offline_banner()}<div class="h-3 shrink-0"></div>{stepper(1)}{body(tiles({"google": "offline"}))}'''))
    p.frame('S11-offline-tapped', 'Offline: Google Sheets tile tapped', phone(f'''{appbar()}{offline_banner()}<div class="h-3 shrink-0"></div>{stepper(1)}{body(tiles({"google": "offline"}), note=False)}
  {snackbar("Google Sheets needs a connection. Try again when you're online.", icon_name="wifi-off")}'''))

    big_tiles = ''.join(tile(s, big=True) for s in SOURCES)
    big = f'''{appbar(big=True)}{stepper(1, big=True)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    <h2 class="text-display">Where are your items?</h2>
    <p class="mt-2 text-title-3 font-normal text-muted-foreground">Choose a source. You can add items from other sources later.</p>
    <div class="mt-5 space-y-3">{big_tiles}</div>
  </div>'''
    p.frame('S11-large-text', 'Large text (200%): one tile per row, scrolls', phone(big))

    future = '<a href="#S11-new-source" class="flex min-h-28 flex-col justify-start gap-3 rounded-tile border bg-card p-4" data-action="source-calendar">' + icon('calendar', 'size-6 text-primary') + '<span><span class="block text-label-lg">Calendar</span><span class="block text-caption text-muted-foreground">Events from your calendar</span></span></a>'
    p.frame('S11-new-source', 'Extensibility: a future source (example) is one more tile', phone(f'{appbar()}{stepper(1)}{body(tiles(extra_tiles=future))}'))

    p.section('Web', 'Contacts import is unavailable in browsers: the tile stays visible with its reason and opens a sheet with “Get the app” and a CSV alternative. Photos become “Upload photos” (file upload, S18 web).')
    web_over = {'photos': dict(name='Upload photos', icon='image-up', desc='Image files from this device', href='S18-photos-import.html#S18-web')}
    web_grid = tiles({'contacts': 'web'}, web_over)
    get_line = f'<p class="mt-3 px-1 text-body-sm text-muted-foreground">Contacts import needs the Android or iOS app. <a href="{GET_APP}" class="text-primary underline underline-offset-4" data-action="get-app">Get the app</a></p>'
    p.frame('S11-web', 'Web, mobile browser', phone(f'{appbar()}{stepper(1)}{body(web_grid, extra=get_line)}', 'web'))
    sheet_body = f'''<div class="mt-2 flex gap-3">{icon("monitor-smartphone", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<p class="text-body text-muted-foreground">Browsers can't read your phone's contacts. Get SwipeSort for Android or iOS to import them, or export your contacts as a CSV file and import that here.</p></div>'''
    sheet_actions = btn('Get the app', GET_APP, 'get-app') + btn('Import a CSV instead', 'S14-file-import.html#S14-default', 'import-csv-instead', 'ghost', size='md')
    p.frame('S11-web-unavailable', 'Web: contacts tile tapped, unavailable sheet', phone(f'''{appbar()}{stepper(1)}{body(web_grid, note=False)}
  {sheet("s11wu", "Contacts import needs the app", sheet_body, sheet_actions, "#S11-web")}''', 'web'))
    p.frame('S11-web-desktop', 'Web, desktop browser: phone layout centered', desktop(f'{appbar()}{stepper(1)}{body(web_grid, extra=get_line)}'))

    p.section('iOS', 'The import opens as a page sheet: Cancel top-left, centered title. Swipe-down dismisses only while nothing is selected yet (later steps ask first).')
    ios_grid = tiles(override={'photos': dict(desc='From your photo library')})
    p.frame('S11-ios', 'iOS: page sheet', phone(f'{iosbar(back=None)}{stepper(1)}{body(ios_grid)}', 'ios'))
    return p


# =====================================================================================
# S12 Permissions
# =====================================================================================
def points_list(points, big=False):
    t, d, ic = ('text-title-2', 'text-title-3 font-normal', 'size-7') if big else ('text-label-lg', 'text-body-sm', 'size-6')
    items = ''.join(f'<li class="flex gap-4"><span class="mt-0.5 shrink-0 text-muted-foreground">{icon(i, ic)}</span><div class="min-w-0"><p class="{t}">{a}</p><p class="mt-0.5 {d} text-muted-foreground">{b}</p></div></li>' for i, a, b in points)
    return f'<ul class="mt-7 space-y-5">{items}</ul>'


def steps_list(steps):
    items = ''.join(f'<li class="flex items-start gap-3"><span class="flex size-7 shrink-0 items-center justify-center rounded-full bg-secondary text-label tabular-nums text-secondary-foreground">{i}</span><span class="pt-0.5 text-body">{s}</span></li>' for i, s in enumerate(steps, 1))
    return f'<ol class="mt-6 space-y-3" aria-label="Steps">{items}</ol>'


def explainer(ic, title, lead, inner, tone='primary', big=False):
    circle = 'bg-primary-soft text-primary-soft-foreground' if tone == 'primary' else 'bg-muted text-muted-foreground'
    h, l = ('text-display', 'text-title-2 font-normal') if big else ('text-title-2', 'text-body-lg')
    return f'''<div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-3">
    <span class="flex size-14 shrink-0 items-center justify-center rounded-full {circle}">{icon(ic, "size-7")}</span>
    <h2 class="mt-5 {h}">{title}</h2>
    <p class="mt-2 max-w-prose {l} text-muted-foreground">{lead}</p>
    {inner}
  </div>'''


CONTACT_POINTS = [
    ('list-checks', 'Only the contacts you pick', 'You choose on the next screen. Nothing else is imported.'),
    ('smartphone', 'Kept on this phone', 'Imported contacts stay on this phone until you share or back up the list.'),
    ('shield-check', "Your address book isn't changed", 'SwipeSort never edits, adds or deletes contacts. Decisions only change SwipeSort\'s copy.'),
]
PHOTO_POINTS = [
    ('images', 'Only the photos you pick', 'Choose photos or whole albums on the next screen.'),
    ('smartphone', 'Kept on this phone', 'Photos stay on this phone until you share or back up the list.'),
    ('shield-check', 'Nothing is deleted', "Rejecting a photo doesn't delete it. Your gallery isn't changed."),
]
NOTIF_EVENTS = [
    ('user-plus', 'Someone joins a list'),
    ('flag', 'A member finishes sorting'),
    ('git-compare-arrows', 'New conflicts need a decision'),
    ('gavel', 'Conflicts are resolved'),
    ('play', 'A new round starts'),
    ('user-cog', 'Your role changes'),
]


def notif_events():
    rows = ''.join(f'<li class="flex min-h-12 items-center gap-4 px-4 py-2">{icon(i, "size-5 shrink-0 text-muted-foreground")}<span class="text-body">{t}</span></li>' for i, t in NOTIF_EVENTS)
    return f'<p class="mt-6 px-1 pb-2 text-label text-muted-foreground">You\'ll hear when</p><ul class="divide-y overflow-hidden rounded-group bg-card">{rows}</ul>'


def build_s12():
    p = Page('S12', 'S12-permissions.html', 'Pre-permission explainers and recovery',
             'Shown before every system permission prompt (contacts, photos, notifications) and when access was denied. One layout for every permission: icon, title, what happens to the data, then the system prompt.')
    S13 = 'S13-contacts-import.html#S13-select-default'
    S11 = 'S11-source-picker.html#S11-default'

    contacts = explainer('contact', 'Allow access to your contacts', 'SwipeSort reads your contacts so you can pick the ones to sort. Here\'s how they\'re handled.', points_list(CONTACT_POINTS))
    contacts_bottom = bottom(btn('Continue', S13, 'continue'), btn('Not now', S11, 'not-now', 'ghost', size='md'), note='Next, Android asks you to allow access.')

    p.section('Contacts', 'Before the Android or iOS contacts prompt. “Continue” triggers the system prompt; when access is granted the import continues at S13. Denied access gets a recovery state with a working alternative.')
    p.frame('S12-default', 'Contacts explainer (same as S12-contacts)', phone(f'{appbar()}{stepper(2)}{contacts}{contacts_bottom}'))
    p.frame('S12-contacts', 'Contacts explainer (Android)', phone(f'{appbar()}{stepper(2)}{contacts}{contacts_bottom}'))

    once = explainer('contact', "SwipeSort can't see your contacts", 'You chose Don\'t allow. To pick contacts, allow access. Or use a CSV file: most contacts apps can export one.',
                     f'<div class="mt-7">{safety_note("Access only lets SwipeSort read contacts. It never changes your address book.")}</div>', tone='muted')
    p.frame('S12-contacts-denied-once', 'Contacts denied once (Android can ask again)', phone(f'''{appbar()}{stepper(2)}{once}{bottom(btn("Allow access", None, "allow-again"), btn("Import a CSV instead", "S14-file-import.html#S14-default", "import-csv-instead", "ghost", size="md"))}'''))

    blocked = explainer('contact', 'Contacts access is off', 'Android won\'t ask again, so access has to be turned on in Settings. When you come back, your contacts are ready to choose.',
                        steps_list(['Tap Open settings', 'Tap Permissions, then Contacts', 'Choose Allow']), tone='muted')
    p.frame('S12-contacts-denied', 'Contacts denied, don\'t ask again: open settings (Android)', phone(f'''{appbar()}{stepper(2)}{blocked}{bottom(btn("Open settings", None, "open-settings"), btn("Import a CSV instead", "S14-file-import.html#S14-default", "import-csv-instead", "ghost", size="md"))}'''))

    p.section('Photos', 'Before gallery access. Photos skip field mapping and duplicate review, so the stepper has 3 steps (Choose source, Select items, Finish). Limited access (iOS, Android 14+) continues with the allowed photos.')
    photos = explainer('images', 'Allow access to your photos', 'SwipeSort shows your gallery so you can pick photos to sort. Each photo becomes one card.', points_list(PHOTO_POINTS))
    p.frame('S12-photos', 'Photos explainer (Android)', phone(f'''{appbar()}{stepper(2, 3)}{photos}{bottom(btn("Continue", "S18-photos-import.html#S18-default", "continue"), btn("Not now", S11, "not-now", "ghost", size="md"), note="Next, Android asks you to allow access to all photos or only some.")}'''))

    pblocked = explainer('images', 'Photo access is off', 'To browse your gallery in SwipeSort, turn access on in Settings. Or pick photos with Android\'s photo picker, which needs no access.',
                         steps_list(['Tap Open settings', 'Tap Permissions, then Photos and videos', 'Choose Allow all']), tone='muted')
    p.frame('S12-photos-denied', 'Photos denied: open settings or use the system picker', phone(f'''{appbar()}{stepper(2, 3)}{pblocked}{bottom(btn("Open settings", None, "open-settings"), btn("Pick photos with the photo picker", "S18-photos-import.html#S18-default", "system-picker", "ghost", size="md"))}'''))

    thumbs = ''.join(f'<img src="{IMG}photos/ph{i:02d}.svg" alt="" class="aspect-square w-full rounded-xs object-cover">' for i in range(1, 8))
    thumbs += '<span class="flex aspect-square w-full items-center justify-center rounded-xs bg-muted text-label tabular-nums text-muted-foreground">+17</span>'
    limited = explainer('images', 'SwipeSort can see 24 photos', 'You allowed access to selected photos only. Sort these, select more, or allow all photos in Settings.',
                        f'<div class="mt-6 grid grid-cols-4 gap-1.5" role="img" aria-label="24 photos allowed, 7 shown">{thumbs}</div><a href="#S12-photos-limited-ios" class="mt-4 inline-flex h-12 items-center text-label-lg text-primary underline underline-offset-4" data-action="open-settings">Allow all photos in Settings</a>')
    p.frame('S12-photos-limited-ios', 'iOS: limited photo access', phone(f'''{iosbar()}{stepper(2, 3)}{limited}{bottom(btn("Continue with 24 photos", "S18-photos-import.html#S18-default", "continue"), btn("Select more photos", None, "select-more", "ghost", size="md"))}''', 'ios'))

    p.section('Notifications', 'Push pre-permission for collaboration events (Android and iOS only). Shown once, right after a list is first shared or joined, and from Activity or Settings while permission is undecided. Not part of the import stepper.')
    notif = explainer('bell', 'Get notified about shared lists', 'Know when it\'s your turn or when a decision needs you, without opening the app.', notif_events())
    notif_bar = f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1"><a href="S09-list-overview.html#S09-shared" class="flex size-12 items-center justify-center rounded-full" aria-label="Not now" data-action="close">{icon("x", "size-6")}</a></header>'''
    p.frame('S12-notifications', 'Notifications explainer (Android)', phone(f'''{notif_bar}{notif}{bottom(btn("Turn on notifications", None, "turn-on"), btn("Not now", "S09-list-overview.html#S09-shared", "not-now", "ghost", size="md"), note="Choose which ones in Settings, under Notifications.")}'''))
    ndenied = explainer('bell-off', 'Notifications are off', 'Android won\'t ask again. To get notified, turn them on in Settings. Activity always shows every update in the app.',
                        steps_list(['Tap Open settings', 'Tap Notifications', 'Turn on All SwipeSort notifications']), tone='muted')
    p.frame('S12-notifications-denied', 'Notifications denied: open settings', phone(f'''{notif_bar}{ndenied}{bottom(btn("Open settings", None, "open-settings"), btn("Not now", "S09-list-overview.html#S09-shared", "not-now", "ghost", size="md"))}'''))

    acts = [('Selin joined the list', 'Wedding guests', 'Oct 2'), ('15 new conflicts', 'Wedding guests', 'Oct 3'), ('Mert resolved 3 conflicts', 'Wedding guests', 'Yesterday')]
    act_rows = ''.join(f'<li class="flex min-h-16 items-center gap-3 px-gutter py-2"><span class="flex size-10 shrink-0 items-center justify-center rounded-full bg-muted text-muted-foreground">{icon("activity")}</span><span class="min-w-0 flex-1"><span class="block truncate text-body">{a}</span><span class="block text-body-sm text-muted-foreground">{b}</span></span><span class="text-caption text-muted-foreground">{c}</span></li>' for a, b, c in acts)
    web_bg = f'''<header class="flex h-app-bar shrink-0 items-center px-gutter"><h1 class="text-title-1">Activity</h1></header><ul class="mt-2 divide-y">{act_rows}</ul>'''
    wbody = f'''<div class="mt-2 flex gap-3">{icon("monitor-smartphone", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<p class="text-body text-muted-foreground">In the browser, updates appear in Activity while SwipeSort is open. To get notified on your phone, get SwipeSort for Android or iOS.</p></div>'''
    p.frame('S12-notifications-web', 'Web: push unavailable, in-app Activity instead', phone(f'''{web_bg}{sheet("s12nw", "Push notifications need the app", wbody, btn("Get the app", GET_APP, "get-app") + btn("Not now", "#S12-notifications-web", "not-now", "ghost", size="md"))}''', 'web'))

    p.section('iOS', 'iOS asks only once per permission: after a denial the only way back is Settings, so iOS recovery never offers “Allow access”. Contacts (iOS 18) and photos can be limited to a selection.')
    cios = explainer('contact', 'Allow access to your contacts', 'SwipeSort reads your contacts so you can pick the ones to sort. Here\'s how they\'re handled.', points_list(CONTACT_POINTS))
    p.frame('S12-contacts-ios', 'iOS: contacts explainer', phone(f'''{iosbar()}{stepper(2)}{cios}{bottom(btn("Continue", S13, "continue"), btn("Not now", S11, "not-now", "ghost", size="md"), note="Next, iOS asks once. Allow full access, or choose contacts to share.")}''', 'ios'))
    dios = explainer('contact', 'Contacts access is off', 'iOS asks only once, so access has to be turned on in Settings. When you come back, your contacts are ready to choose.',
                     steps_list(['Tap Open Settings', 'Tap Contacts', 'Choose Full Access']), tone='muted')
    p.frame('S12-contacts-denied-ios', 'iOS: contacts denied', phone(f'''{iosbar()}{stepper(2)}{dios}{bottom(btn("Open Settings", None, "open-settings"), btn("Import a CSV instead", "S14-file-import.html#S14-default", "import-csv-instead", "ghost", size="md"))}''', 'ios'))
    nios = explainer('bell', 'Get notified about shared lists', 'Know when it\'s your turn or when a decision needs you, without opening the app.', notif_events())
    nbar_ios = f'''<header class="grid h-14 shrink-0 grid-cols-[1fr_auto_1fr] items-center px-2"><a href="S09-list-overview.html#S09-shared" class="inline-flex h-12 items-center justify-self-start px-2 text-body text-primary" data-action="close">Not now</a><span></span><span></span></header>'''
    p.frame('S12-notifications-ios', 'iOS: notifications explainer', phone(f'''{nbar_ios}{nios}{bottom(btn("Turn on notifications", None, "turn-on"), note="Next, iOS asks once. Change it later in Settings.")}''', 'ios'))

    p.section('Accessibility', 'Large text: the explainer scrolls; the bottom actions stay pinned and wrap.')
    big = explainer('contact', 'Allow access to your contacts', 'SwipeSort reads your contacts so you can pick the ones to sort.', points_list(CONTACT_POINTS, big=True), big=True)
    p.frame('S12-contacts-large-text', 'Large text (200%): contacts explainer', phone(f'''{appbar(big=True)}{stepper(2, big=True)}{big}<div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">{btn("Continue", S13, "continue", extra="min-h-16 text-title-3")}<div class="mt-1">{btn("Not now", S11, "not-now", "ghost", size="md", extra="text-title-3")}</div></div>'''))
    return p


# =====================================================================================
# Contacts data (address book = 88 sample contacts imported + 8 not imported)
# =====================================================================================
EXTRAS = [
    dict(id='x01', name='Apartman Yönetimi', phones=[{'number': '+90 216 000 12 45'}]),
    dict(id='x02', name='Emlakçı Serdar', phones=[{'number': '+90 500 000 08 19'}]),
    dict(id='x03', name='Kuaför Nilay', phones=[{'number': '+90 216 000 77 30'}]),
    dict(id='x04', name='Moda Taksi Durağı', phones=[{'number': '+90 216 000 00 61'}]),
    dict(id='x05', name='Patiler Veteriner Kliniği', phones=[{'number': '+90 216 000 92 14'}, {'number': '+90 500 000 41 06'}]),
    dict(id='x06', name='Su Siparişi', phones=[{'number': '+90 444 0 000'}]),
    dict(id='x07', name='Tesisatçı Hüseyin', phones=[{'number': '+90 500 000 31 88'}]),
    dict(id='x08', name='Kurye Mehmet', phones=[{'number': '+90 500 000 13 52'}]),
]
TR = 'AÂBCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜVWXYZ'


def tr_upper(ch):
    return {'i': 'İ', 'ı': 'I'}.get(ch, ch.upper())


def sort_key(name):
    key = []
    for ch in name:
        u = tr_upper(ch)
        if u in TR:
            key.append((0, TR.index(u)))
        else:
            b = unicodedata.normalize('NFD', u)[0]
            key.append((0, TR.index(b)) if b in TR else (1, ord(u)))
    return key


def fold(s):
    out = ''
    for ch in s:
        if ch in 'ıİ':
            out += 'i'
        else:
            out += unicodedata.normalize('NFD', ch)[0].lower()
    return out


ADDRESS = [c for c in DATA['contacts'] if c['source'] == 'contacts'] + EXTRAS
ADDRESS.sort(key=lambda c: sort_key(c['name']))
UNSELECTED = {e['id'] for e in EXTRAS}
assert len(ADDRESS) == 96


def initials(name):
    import re
    n = re.sub(r'\(.*?\)', '', name).replace('Dr. ', '').strip()
    w = n.split()
    if not w:
        return '?'
    return (tr_upper(w[0][0]) + (tr_upper(w[-1][0]) if len(w) > 1 else '')).strip()


def avatar(c, size='size-10'):
    if c.get('photo'):
        return f'<img src="{IMG}{c["photo"].replace("images/", "")}" alt="" class="{size} shrink-0 rounded-full object-cover">'
    return f'<span class="flex {size} shrink-0 items-center justify-center rounded-full bg-muted text-label text-muted-foreground" aria-hidden="true">{initials(c["name"])}</span>'


def meta(c):
    ph = c.get('phones') or []
    if len(ph) > 1:
        return f'{icon("phone", "size-3.5 shrink-0")}<span>{len(ph)} phone numbers</span>'
    if ph:
        return f'<span class="tabular-nums">{ph[0]["number"]}</span>'
    if c.get('email'):
        return f'<span class="truncate">{c["email"]}</span>'
    return '<span>No phone or email</span>'


def highlight(name, q):
    if not q:
        return name
    f = fold(name)
    i = f.find(fold(q))
    if i < 0:
        return name
    j = i + len(q)
    return f'{name[:i]}<span class="font-semibold">{name[i:j]}</span>{name[j:]}'


def contact_row(c, checked=True, q=None, round_=False, big=False, pr=''):
    if big:
        return f'''<li><button type="button" role="checkbox" aria-checked="{"true" if checked else "false"}" class="flex min-h-20 w-full items-center gap-4 px-gutter py-3 text-left">{checkbox("on" if checked else "off", round_)}<span class="min-w-0 flex-1"><span class="block text-title-2 font-normal">{c["name"]}</span><span class="mt-0.5 flex items-center gap-1.5 text-title-3 font-normal text-muted-foreground">{meta(c)}</span></span></button></li>'''
    return f'''<li><button type="button" role="checkbox" aria-checked="{"true" if checked else "false"}" class="flex min-h-16 w-full items-center gap-3 px-gutter py-2 text-left {pr}">{checkbox("on" if checked else "off", round_)}{avatar(c)}<span class="min-w-0 flex-1"><span class="block truncate text-body">{highlight(c["name"], q)}</span><span class="flex items-center gap-1.5 truncate text-body-sm text-muted-foreground">{meta(c)}</span></span></button></li>'''


def section_header(letter, big=False):
    t = 'text-body-lg font-medium' if big else 'text-label'
    return f'<h3 class="sticky top-0 bg-background px-gutter pb-1 pt-3 {t} text-muted-foreground">{letter}</h3>'


def first_letter(name):
    u = tr_upper(name[0])
    return u if u in TR else '#'


def contact_sections(contacts, checked_fn, limit=12, q=None, round_=False, big=False, pr=''):
    out, cur, n = [], None, 0
    rows = []
    for c in contacts:
        if n >= limit:
            break
        L = first_letter(c['name'])
        if L != cur:
            if rows:
                out.append(f'<ul class="divide-y">{"".join(rows)}</ul>')
                rows = []
            out.append(section_header(L, big))
            cur = L
        rows.append(contact_row(c, checked_fn(c), q, round_, big, pr))
        n += 1
    if rows:
        out.append(f'<ul class="divide-y">{"".join(rows)}</ul>')
    return ''.join(out)


def select_all(state_, count, label='Select all', round_=False, big=False):
    aria = {'on': 'true', 'off': 'false', 'mixed': 'mixed'}[state_]
    t, c = ('text-title-2 font-normal', 'text-title-3 font-normal') if big else ('text-body', 'text-body-sm')
    return f'''<div class="shrink-0 border-b"><button type="button" role="checkbox" aria-checked="{aria}" class="flex min-h-14 w-full items-center gap-3 px-gutter py-2 text-left">{checkbox(state_, round_)}<span class="flex-1 {t}">{label}</span><span class="{c} tabular-nums text-muted-foreground">{count}</span></button></div>'''


# =====================================================================================
# S13 Contacts import
# =====================================================================================
def build_s13():
    p = Page('S13', 'S13-contacts-import.html', 'Contacts import',
             'Select items for the Contacts source: search and multi-select contacts from the address book (96 contacts on Deniz\'s phone: the 88 sample contacts plus 8 service numbers).')
    S19C = 'S19-field-mapping.html#S19-contacts'

    def screen(content, count, sa_state, primary, search='', fid='s13', hint='', ios=False, round_=False, big=False, bar=None, extra_top=''):
        hdr = bar or (iosbar() if ios else appbar(big=big))
        return f'''{hdr}{stepper(2, big=big)}{extra_top}
  <div class="shrink-0 px-gutter pb-2">{search_field(fid + "-q", search, big=big, round_="rounded-control" if ios else "rounded-full")}</div>
  {select_all(sa_state, count, round_=round_, big=big)}
  {hint}
  <div class="relative min-h-0 flex-1 overflow-hidden">{content}</div>
  {primary}'''

    def cont(n, href=S19C, action=None, big=False):
        lbl = f'Continue with {n} contacts'
        return bottom(btn(lbl, href, action, extra='text-title-3' if big else ''), border=True)

    sel88 = contact_sections(ADDRESS, lambda c: c['id'] not in UNSELECTED)
    all96 = contact_sections(ADDRESS, lambda c: True, limit=7)
    none_ = contact_sections(ADDRESS, lambda c: False)

    p.section('Select contacts', 'Everything starts selected: sorting is where decisions happen, so this step only removes contacts that clearly don\'t belong, like services and shops. Selection survives searching and clearing the search.')
    hint = f'<p class="flex shrink-0 items-center gap-2 bg-primary-soft px-gutter py-2.5 text-body-sm text-primary-soft-foreground" role="note">{icon("info", "size-4 shrink-0")}<span>All contacts are selected. Uncheck the ones you don\'t want to sort.</span></p>'
    p.frame('S13-default', 'Default: all 96 selected on arrival', phone(screen(all96, '96 of 96 selected', 'on', cont(96), fid='s13d', hint=hint)))
    p.frame('S13-select-default', 'After unchecking 8 service numbers: 88 of 96', phone(screen(sel88, '88 of 96 selected', 'mixed', cont(88, action='continue'), fid='s13s')))

    q = 'oz'
    res = [c for c in ADDRESS if fold(q) in fold(c['name'])]
    res_html = f'<p class="px-gutter pb-1 pt-3 text-label text-muted-foreground">{len(res)} contacts match “{q}”. Accents are ignored.</p><ul class="divide-y">{"".join(contact_row(c, c["id"] not in UNSELECTED, q) for c in res)}</ul>'
    sel_res = sum(1 for c in res if c['id'] not in UNSELECTED)
    p.frame('S13-search', 'Search active: matching ignores accents', phone(screen(res_html, f'{sel_res} of {len(res)} selected', 'on' if sel_res == len(res) else 'mixed', cont(88), search=q, fid='s13q').replace('>Select all<', '>Select all results<')))

    empty = f'''<div class="flex h-full flex-col items-center px-8 pt-16 text-center">{icon("search-x", "size-8 text-muted-foreground")}<h2 class="mt-4 text-title-3">No contacts match “Selim”</h2><p class="mt-1 max-w-xs text-body text-muted-foreground">Check the spelling, or search by phone number.</p>{btn("Clear search", "#S13-select-default", "clear-search", "secondary", full=False, size="md", extra="mt-6")}</div>'''
    p.frame('S13-search-empty', 'Search with no results', phone(screen(empty, '0 of 0 selected', 'off', cont(88), search='Selim', fid='s13e').replace('>Select all<', '>Select all results<').replace('<button type="button" role="checkbox" aria-checked="false" class="flex min-h-14', '<button type="button" role="checkbox" aria-checked="false" disabled class="opacity-50 flex min-h-14')))

    none_note = '<p class="pb-1 text-center text-body-sm text-muted-foreground">Select at least one contact to continue.</p>'
    p.frame('S13-none-selected', 'Nothing selected: Continue disabled', phone(screen(none_, '0 of 96 selected', 'off', bottom(btn('Continue', disabled=True), note='Select at least one contact to continue.', border=True), fid='s13n')))

    p.section('Loading, empty and errors', 'Contacts are read from the phone, so there is no offline state: the step works the same without a connection.')
    sk_rows = ''.join(f'<li class="flex min-h-16 items-center gap-3 px-gutter py-2"><span class="size-6 animate-pulse rounded-sm bg-muted"></span><span class="size-10 animate-pulse rounded-full bg-muted"></span><span class="flex-1 space-y-2"><span class="block h-3.5 w-{w} animate-pulse rounded-full bg-muted"></span><span class="block h-3 w-1/3 animate-pulse rounded-full bg-muted"></span></span></li>' for w in ['2/3', '1/2', '3/5', '2/5', '1/2', '2/3', '3/5', '1/2'])
    loading = f'''{appbar()}{stepper(2)}
  <div class="shrink-0 px-gutter pb-2">{search_field("s13l-q").replace('type="search"', 'type="search" disabled')}</div>
  <div class="flex min-h-14 shrink-0 items-center gap-2 border-b px-gutter text-body-sm text-muted-foreground" role="status">{icon("loader-circle", "size-5 animate-spin text-primary")}Reading contacts…</div>
  <ul class="min-h-0 flex-1 overflow-hidden" aria-hidden="true">{sk_rows}</ul>
  {bottom(btn("Continue", disabled=True), border=True)}'''
    p.frame('S13-loading', 'Loading contacts', phone(loading))

    empty_book = f'''{appbar()}{stepper(2)}{state("contact", "No contacts on this phone", "Add contacts in your phone\'s Contacts app, or import them from a CSV file.")}
  {bottom(btn("Import a CSV instead", "S14-file-import.html#S14-default", "import-csv-instead"), btn("Choose another source", "S11-source-picker.html#S11-default", "another-source", "ghost", size="md"))}'''
    p.frame('S13-empty', 'Empty address book', phone(empty_book))

    err = f'''{appbar()}{stepper(2)}{state("triangle-alert", "Contacts couldn\'t be read", "Your phone didn\'t return the contacts. Try again, or import a CSV file instead.")}
  {bottom(btn("Try again", None, "retry"), btn("Import a CSV instead", "S14-file-import.html#S14-default", "import-csv-instead", "ghost", size="md"))}'''
    p.frame('S13-error', 'Error reading contacts', phone(err))

    dlg = dialog('s13x', 'Discard import?', 'Your selection of 88 contacts will be lost. Nothing has been added to SwipeSort yet.',
                 btn('Keep importing', '#S13-select-default', 'cancel', 'ghost', full=False, size='md', extra='px-4') + btn('Discard import', HOME, 'discard', 'destructive', full=False, size='md', extra='px-4'))
    p.frame('S13-close-confirm', 'Close with a selection: discard dialog (S40 pattern)', phone(screen(sel88, '88 of 96 selected', 'mixed', cont(88), fid='s13c') + dlg))

    p.section('Very large address books', 'Thousands of contacts: sticky letter headers and a fast-scroll index on the right edge (Android and iOS). The list is virtualized; search stays the fastest route.')
    pool = sorted([c for c in DATA['contacts'] if c['name'][0] == 'M'], key=lambda c: sort_key(c['name']))
    m_rows = ''.join(contact_row(c, True, pr='pr-10') for c in pool)
    letters = 'ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZ#'
    idx = ''.join(f'<span class="{"font-semibold text-primary" if L == "M" else ""}">{L}</span>' for L in letters)
    large = f'''<h3 class="sticky top-0 bg-background px-gutter pb-1 pt-3 text-label text-muted-foreground">M</h3><ul class="divide-y">{m_rows}</ul>
    <div class="absolute inset-y-1 right-1 flex w-6 flex-col items-center justify-between text-caption leading-none text-muted-foreground" aria-hidden="true">{idx}</div>
    <div class="absolute right-12 top-40 flex size-14 items-center justify-center rounded-full bg-primary text-title-2 text-primary-foreground shadow-overlay" aria-hidden="true">M</div>'''
    p.frame('S13-large', '2,140 contacts: letter index while scrubbing', phone(screen(large, '2,140 of 2,140 selected', 'on', cont('2,140'), fid='s13g')))

    p.section('Accessibility', 'At 200% text, rows grow and names wrap instead of truncating; avatars hide to keep names readable.')
    big_list = contact_sections(ADDRESS, lambda c: c['id'] not in UNSELECTED, limit=6, big=True)
    p.frame('S13-large-text', 'Large text (200%)', phone(screen(big_list, '88 of 96', 'mixed', cont(88, big=True), fid='s13b', big=True)))

    p.section('iOS', 'Page sheet with Cancel; round selection marks (iOS convention). iOS 18 can limit contacts to a selection: the list shows only those, with a way to add more.')
    sel_ios = contact_sections(ADDRESS, lambda c: c['id'] not in UNSELECTED, round_=True)
    p.frame('S13-ios', 'iOS: full access', phone(screen(sel_ios, '88 of 96 selected', 'mixed', cont(88), fid='s13i', ios=True, round_=True), 'ios'))
    limited_ids = [c for c in ADDRESS if c['id'] not in UNSELECTED][:40]
    lim_html = contact_sections(limited_ids, lambda c: True, round_=True, limit=10)
    lim_hint = f'<div class="shrink-0 px-gutter pb-3">{info_alert("SwipeSort can see 40 contacts", "You chose which contacts to share with SwipeSort.", "contact", extra=chr(10) + btn("Share more contacts", None, "share-more", "ghost", full=False, size="md", extra="-ml-3 mt-1 h-12 px-3 text-primary-soft-foreground underline underline-offset-4"))}</div>'
    p.frame('S13-ios-limited', 'iOS: limited contacts access (iOS 18)', phone(screen(lim_html, '40 of 40 selected', 'on', cont(40), fid='s13il', ios=True, round_=True, extra_top=lim_hint), 'ios'))
    return p


# =====================================================================================
# S14 File import
# =====================================================================================
def file_row(name, meta_, ic='file-text', change='#S14-default', big=False):
    t, m = ('text-title-3 font-normal', 'text-body-lg') if big else ('text-body', 'text-body-sm')
    ch = f'<a href="{change}" class="inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label-lg text-primary" data-action="change-file">Change</a>' if change else ''
    return f'''<div class="flex min-h-16 items-center gap-3 rounded-group bg-card py-2 pl-4 pr-2">
      <span class="flex size-10 shrink-0 items-center justify-center rounded-sm bg-primary-soft text-primary-soft-foreground">{icon(ic)}</span>
      <div class="min-w-0 flex-1"><p class="truncate {t}">{name}</p><p class="truncate {m} text-muted-foreground">{meta_}</p></div>{ch}
    </div>'''


def settings_group(header_on=True, sep='Comma', detected='Detected in candidates-q4.csv', show_sep=True):
    sep_row = f'<li><button type="button" class="flex min-h-14 w-full items-center gap-4 px-4 py-3 text-left" aria-haspopup="listbox"><span class="flex-1 text-body">Separator</span><span class="text-body text-muted-foreground">{sep}</span>{icon("chevron-down", "size-5 text-muted-foreground")}</button></li>' if show_sep else ''
    return f'''<ul class="mt-3 divide-y overflow-hidden rounded-group bg-card">
      <li><button type="button" role="switch" aria-checked="{"true" if header_on else "false"}" class="flex min-h-14 w-full items-center gap-4 px-4 py-3 text-left"><span class="min-w-0 flex-1"><span class="block text-body">First row has column names</span><span class="block text-body-sm text-muted-foreground">{detected}</span></span>{switch_vis(header_on)}</button></li>
      {sep_row}
    </ul>'''


def table(cols, rows, caption, numbered=True, start=1, warn_rows=(), cellw='max-w-44'):
    th = ('<th scope="col" class="px-3 py-2.5 text-label text-muted-foreground"><span class="sr-only">Row</span></th>' if numbered else '') + ''.join(f'<th scope="col" class="whitespace-nowrap px-3 py-2.5 text-label text-muted-foreground">{c}</th>' for c in cols)
    trs = []
    for i, r in enumerate(rows):
        n = start + i
        cells = ''.join(f'<td class="px-3 py-2.5"><span class="block {cellw} truncate whitespace-nowrap text-body-sm{" text-muted-foreground" if v in ("", None) else ""}">{"—" if v in ("", None) else v}</span></td>' for v in r)
        num = f'<td class="px-3 py-2.5 text-caption tabular-nums text-muted-foreground">{n}</td>' if numbered else ''
        trs.append(f'<tr>{num}{cells}</tr>')
    return f'''<div class="min-h-0 overflow-hidden rounded-group bg-card"><div class="overflow-x-auto" tabindex="0" role="region" aria-label="{caption}, scrolls sideways"><table class="w-max min-w-full text-left"><caption class="sr-only">{caption}</caption><thead class="bg-muted"><tr>{th}</tr></thead><tbody class="divide-y">{"".join(trs)}</tbody></table></div></div>'''


CAND_COLS = ['Name', 'Role', 'Years of experience', 'Location', 'Expected salary', 'Portfolio', 'Email', 'Source']


def cand_rows():
    out = []
    for k in DATA['candidates']:
        sal = f'{k["expectedSalary"]}' if k['expectedSalary'] else ''
        out.append([k['name'], k['role'], k['yearsExperience'], k['location'], sal, (k['portfolio'] or '').replace('https://', ''), k['email'], k['source']])
    return out


def build_s14():
    p = Page('S14', 'S14-file-import.html', 'File import (CSV and Excel)',
             'Select items for the CSV or Excel source: pick a file, check the detected structure in a preview, choose Excel sheets, and recover from file errors.')
    S19 = 'S19-field-mapping.html#S19-csv'

    works = f'''<p class="mt-6 px-1 pb-2 text-label text-muted-foreground">What works</p>
    <ul class="divide-y overflow-hidden rounded-group bg-card">
      <li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon("file-text", "size-5 shrink-0 text-muted-foreground")}<span><span class="block text-body">.csv</span><span class="block text-body-sm text-muted-foreground">Comma, semicolon or tab separated</span></span></li>
      <li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon("file-spreadsheet", "size-5 shrink-0 text-muted-foreground")}<span><span class="block text-body">.xlsx</span><span class="block text-body-sm text-muted-foreground">Excel workbooks; you choose the sheets</span></span></li>
      <li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon("ruler", "size-5 shrink-0 text-muted-foreground")}<span><span class="block text-body">Up to 10,000 rows and 50 columns</span><span class="block text-body-sm text-muted-foreground">Files up to 20 MB</span></span></li>
    </ul>'''

    def start_body(extra_top='', drop='', compact=False):
        w = '<p class="mt-4 text-body-sm text-muted-foreground">Works with .csv and .xlsx files up to 20 MB, 10,000 rows and 50 columns.</p>' if compact else works
        return f'''<div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    <h2 class="text-title-2">Choose a CSV or Excel file</h2>
    <p class="mt-1 text-body text-muted-foreground">Each row becomes an item and each column a field. Column names, like Name or Price, go in the first row.</p>
    {drop}{w}
    <div class="mt-auto pb-2 pt-6">{safety_note("Your file isn\'t changed. SwipeSort imports a copy.")}</div>
  </div>'''

    p.section('Choose a file', 'The system file picker (out of scope) opens from “Choose file”. Reading starts as soon as a file is picked.')
    p.frame('S14-default', 'Default: choose a file (Android)', phone(f'{appbar()}{stepper(2)}{start_body()}{bottom(btn("Choose file", "#S14-csv-preview", "choose-file"))}'))

    reading = f'''{appbar()}{stepper(2)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("office-furniture.xlsx", "2.4 MB", "file-spreadsheet", None)}
    <div class="mt-8" role="status" aria-live="polite">
      <div class="flex items-center gap-3 text-body">{icon("loader-circle", "size-5 animate-spin text-primary")}Reading office-furniture.xlsx…</div>
      <div class="mt-3 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" aria-label="Reading, 40 percent"><div class="h-full w-[40%] rounded-full bg-primary"></div></div>
      <p class="mt-2 text-body-sm text-muted-foreground">Large files take a few seconds. Nothing is imported until you continue.</p>
    </div>
  </div>
  {bottom(btn("Continue", disabled=True), btn("Cancel", "#S14-default", "cancel", "ghost", size="md"))}'''
    p.frame('S14-reading', 'Reading a file', phone(reading))

    p.section('Preview', 'What SwipeSort detected: the header row, the separator and the rows that become items. The table scrolls sideways; mapping (S19) renames, hides and types the columns.')
    rows = cand_rows()
    prev = f'''{appbar()}{stepper(2)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("candidates-q4.csv", "12 rows, 8 columns, 3 KB")}
    {settings_group()}
    <div class="mt-5 flex items-baseline justify-between px-1 pb-2"><h2 class="text-label text-muted-foreground">Preview</h2><span class="text-caption tabular-nums text-muted-foreground">12 rows</span></div>
    {table(CAND_COLS, rows, "Preview of candidates-q4.csv", cellw="max-w-36")}
  </div>
  {bottom(btn("Continue with 12 rows", S19, "continue"), border=True)}'''
    p.frame('S14-csv-preview', 'CSV loaded: candidates-q4.csv', phone(prev))

    nh_rows = [CAND_COLS] + rows
    nh = f'''{appbar()}{stepper(2)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("candidates-q4.csv", "13 rows, 8 columns, 3 KB")}
    {settings_group(False, detected="Off: the first row is imported as an item")}
    <div class="mt-5 flex items-baseline justify-between px-1 pb-2"><h2 class="text-label text-muted-foreground">Preview</h2><span class="text-caption tabular-nums text-muted-foreground">13 rows</span></div>
    {table(["Column A", "Column B", "Column C", "Column D", "Column E", "Column F", "Column G", "Column H"], nh_rows, "Preview without a header row", cellw="max-w-36")}
  </div>
  {bottom(btn("Continue with 13 rows", S19), border=True)}'''
    p.frame('S14-no-header', 'Header row turned off: generic column names', phone(nh))

    prods = DATA['products']
    sheets = [('Shortlist', '20 rows. Name, Price, Rating, Store, Category, Link', True, False),
              ('Last year', '34 rows. Name, Price, Rating, Store, Category, Link', False, False),
              ('Price history', '12 rows. Date, Item, Price', False, False),
              ('Notes', 'No rows', False, True)]
    srows = ''
    for n, d, on, dis in sheets:
        if dis:
            srows += f'<li><button type="button" role="checkbox" aria-checked="false" disabled class="flex min-h-16 w-full items-center gap-3 px-4 py-2 text-left">{checkbox("off")}<span class="min-w-0 flex-1"><span class="block text-body text-muted-foreground">{n}</span><span class="block text-body-sm text-muted-foreground">{d}, nothing to import</span></span></button></li>'
        else:
            srows += f'<li><button type="button" role="checkbox" aria-checked="{"true" if on else "false"}" class="flex min-h-16 w-full items-center gap-3 px-4 py-2 text-left">{checkbox("on" if on else "off")}<span class="min-w-0 flex-1"><span class="block text-body">{n}</span><span class="block truncate text-body-sm text-muted-foreground">{d}</span></span></button></li>'
    ptab = table(['Name', 'Price', 'Rating', 'Store'], [[x['name'], x['price'], x['rating'], x['store']] for x in prods[:6]], 'Preview of the Shortlist sheet')
    xl = f'''{appbar()}{stepper(2)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("office-furniture.xlsx", "4 sheets, 2.4 MB", "file-spreadsheet")}
    <h2 class="mt-5 text-title-3">Choose sheets</h2>
    <p class="mt-1 text-body-sm text-muted-foreground">Pick one, or several with the same columns to combine them.</p>
    <ul class="mt-3 divide-y overflow-hidden rounded-group bg-card">{srows}</ul>
    <div class="mt-5 flex items-baseline justify-between px-1 pb-2"><h2 class="text-label text-muted-foreground">Shortlist</h2><span class="text-caption tabular-nums text-muted-foreground">20 rows</span></div>
    {ptab}
  </div>
  {bottom(btn("Continue with 20 rows", "S19-field-mapping.html#S19-default", "continue"), border=True)}'''
    p.frame('S14-excel-sheets', 'Excel with several sheets: choose sheets', phone(xl))

    big_rec = ''.join(f'<div><dt class="text-body-lg text-muted-foreground">{c}</dt><dd class="text-title-3 font-normal">{v if v not in ("", None) else "Empty"}</dd></div>' for c, v in zip(CAND_COLS[:5], rows[0][:5]))
    bigp = f'''{appbar(big=True)}{stepper(2, big=True)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1">
    {file_row("candidates-q4.csv", "12 rows, 8 columns", big=True)}
    <ul class="mt-3 overflow-hidden rounded-group bg-card"><li><button type="button" role="switch" aria-checked="true" class="flex min-h-16 w-full items-center gap-4 px-4 py-3 text-left"><span class="min-w-0 flex-1 text-title-3 font-normal">First row has column names</span>{switch_vis(True)}</button></li></ul>
    <div class="mt-4 rounded-group bg-card p-4">
      <div class="flex items-center justify-between gap-2"><h2 class="text-title-3">Row 1 of 12</h2><span class="flex"><button class="flex size-12 items-center justify-center rounded-full opacity-50" aria-label="Previous row" disabled>{icon("chevron-left", "size-6")}</button><button class="flex size-12 items-center justify-center rounded-full" aria-label="Next row">{icon("chevron-right", "size-6")}</button></span></div>
      <dl class="mt-2 space-y-3">{big_rec}</dl>
    </div>
  </div>
  {bottom(btn("Continue with 12 rows", S19, extra="min-h-16 text-title-3"), border=True)}'''
    p.frame('S14-csv-preview-large-text', 'Large text (200%): preview becomes one row at a time', phone(bigp))

    p.section('File errors', 'Each error says what happened and what to do, names the file, and offers a way forward. Error haptic on Android and iOS. The original file is never touched.')

    def err(fid, label, ic, title, body, prim, sec=None):
        p.frame(fid, label, phone(f'''{appbar()}{stepper(2)}{state(ic, title, body)}{bottom(prim, sec)}'''))

    another = btn('Choose another source', 'S11-source-picker.html#S11-default', 'another-source', 'ghost', size='md')
    err('S14-error-unreadable', 'Unreadable file', 'file-x', 'This file can\'t be read', 'budget-final.xlsx may be damaged or protected with a password. Open it in a spreadsheet app, save it as .csv or .xlsx, and try again.', btn('Choose another file', '#S14-default', 'choose-file'), another)
    err('S14-error-empty', 'Empty file', 'file-question', 'This file has no rows', 'plants.csv has column names but nothing below them. Add rows and try again, or choose another file.', btn('Choose another file', '#S14-default', 'choose-file'), another)
    err('S14-error-too-many-columns', 'Too many columns (limit 50)', 'columns-3', 'This file has 73 columns', 'SwipeSort imports up to 50 columns per list. Choose the columns you need, or continue with the first 50.', btn('Choose columns', '#S14-choose-columns', 'choose-columns'), btn('Continue with the first 50', '#S14-csv-preview', 'first-50', 'ghost', size='md'))
    err('S14-error-too-large', 'File too large (limit 20 MB)', 'file-warning', 'This file is too large', 'crm-export-full.csv is 48 MB. SwipeSort imports files up to 20 MB. Remove columns you don\'t need or split the file, then try again.', btn('Choose another file', '#S14-default', 'choose-file'), another)
    err('S14-error-too-many-rows', 'Too many rows (limit 10,000)', 'rows-3', 'This file has 14,250 rows', 'SwipeSort imports up to 10,000 rows per file. Import the first 10,000 now and add the rest to the same list later.', btn('Import the first 10,000 rows', '#S14-csv-preview', 'first-10000'), btn('Choose another file', '#S14-default', 'choose-file', 'ghost', size='md'))
    err('S14-error-unsupported', 'Unsupported file type', 'file-x', 'SwipeSort can\'t open .numbers files', 'Export it from Numbers as CSV or Excel, then choose it again. SwipeSort opens .csv and .xlsx files.', btn('Choose another file', '#S14-default', 'choose-file'), another)

    cols_list = ['Contact name', 'Company', 'Email', 'Phone', 'Deal owner', 'Stage', 'Created', 'Last activity', 'Lead source', 'City']
    samples = ['Ece Doğru', 'Kuzey Yazılım', 'ece.dogru@example.com', '+90 500 000 07 26', 'Deniz Yılmaz', 'Proposal sent', 'Sep 12, 2026', 'Oct 8, 2026', 'Referral', 'Ankara']
    crow = ''.join(f'<li><button type="button" role="checkbox" aria-checked="{"true" if i < 8 else "false"}" class="flex min-h-14 w-full items-center gap-3 px-4 py-2 text-left">{checkbox("on" if i < 8 else "off")}<span class="min-w-0 flex-1"><span class="block text-body">{c}</span><span class="block truncate text-body-sm text-muted-foreground">For example: {s}</span></span></button></li>' for i, (c, s) in enumerate(zip(cols_list[:7], samples)))
    cc = f'''{appbar()}{stepper(2)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("crm-export-2026.csv", "1,240 rows, 73 columns")}
    <h2 class="mt-5 text-title-3">Choose up to 50 columns</h2>
    <div class="mt-3">{search_field("s14c-q", placeholder="Search columns", label="Search columns")}</div>
    <div class="mt-2 flex items-center justify-between px-1"><span class="text-body-sm tabular-nums text-muted-foreground">8 of 73 selected</span>{btn("Select first 50", None, "select-50", "ghost", full=False, size="md", extra="-mr-3 px-3 text-primary")}</div>
    <ul class="mt-1 divide-y overflow-hidden rounded-group bg-card">{crow}</ul>
  </div>
  {bottom(btn("Continue with 8 columns", "#S14-csv-preview", "continue"), border=True)}'''
    p.frame('S14-choose-columns', 'Too many columns: choose columns', phone(cc))

    contacts88 = [c for c in DATA['contacts'] if c['source'] == 'contacts']
    prow = [[c['name'], (c.get('phones') or [{'number': ''}])[0]['number'], c.get('email') or '', c['city']] for c in contacts88[:7]]
    show = btn('Show skipped rows', '#S14-skipped-rows', 'show-skipped', 'ghost', full=False, size='md', extra='-ml-3 mt-1 px-3 text-primary underline underline-offset-4')
    part = f'''{appbar()}{stepper(2)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("contacts-export.csv", "88 rows, 4 columns, 9 KB")}
    <div class="mt-3">{error_alert("84 of 88 rows can be imported", "4 rows don\'t match the columns and will be skipped. The other rows are fine.", show)}</div>
    <div class="mt-5 flex items-baseline justify-between px-1 pb-2"><h2 class="text-label text-muted-foreground">Preview</h2><span class="text-caption tabular-nums text-muted-foreground">84 rows</span></div>
    {table(["Name", "Phone", "Email", "City"], prow, "Preview of contacts-export.csv")}
  </div>
  {bottom(btn("Continue with 84 rows", "S19-field-mapping.html#S19-default", "continue"), border=True)}'''
    p.frame('S14-partial', 'Partial import: 84 of 88 rows readable', phone(part))
    skipped = [('Row 23', 'Has 6 cells; the file has 4 columns'), ('Row 41', 'A quote mark isn\'t closed'), ('Row 57', 'Has 5 cells; the file has 4 columns'), ('Row 88', 'Has 6 cells; the file has 4 columns')]
    sk = ''.join(f'<li class="flex min-h-14 items-center gap-4 py-2"><span class="w-16 shrink-0 text-label tabular-nums">{a}</span><span class="text-body-sm text-muted-foreground">{b}</span></li>' for a, b in skipped)
    sbody = f'<p class="mt-1 text-body text-muted-foreground">To keep these rows, fix them in a spreadsheet app and import the file again.</p><ul class="mt-3 divide-y">{sk}</ul>'
    p.frame('S14-skipped-rows', 'Skipped rows sheet', phone(f'''{appbar()}{stepper(2)}<div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">{file_row("contacts-export.csv", "88 rows, 4 columns, 9 KB")}</div>
  {sheet("s14sk", "4 skipped rows", sbody, btn("Continue with 84 rows", "S19-field-mapping.html#S19-default", "continue") + btn("Choose another file", "#S14-default", "choose-file", "ghost", size="md"), "#S14-partial")}'''))

    p.section('Web and iOS', 'Mobile web works like Android (the browser\'s file chooser). Desktop adds a drop zone. iOS opens the Files picker from a page sheet.')
    drop = f'''<div class="mt-5 flex flex-col items-center rounded-tile border-2 border-dashed border-input px-6 py-8 text-center">
      {icon("upload", "size-8 text-muted-foreground")}
      <p class="mt-3 text-label-lg">Drop a CSV or Excel file here</p>
      <p class="mt-1 text-body-sm text-muted-foreground">or</p>
      {btn("Browse files", "#S14-csv-preview", "choose-file", full=False, size="md", extra="mt-3")}
    </div>'''
    p.frame('S14-web-desktop', 'Web, desktop: drop zone and browse', desktop(f'{appbar()}{stepper(2)}{start_body(drop=drop, compact=True)}'))
    drop_on = f'''<div class="mt-5 flex flex-col items-center rounded-tile border-2 border-dashed border-primary bg-primary-soft px-6 py-8 text-center text-primary-soft-foreground" role="status">
      {icon("upload", "size-8")}
      <p class="mt-3 text-label-lg">Drop the file to import it</p>
      <p class="mt-1 text-body-sm">.csv or .xlsx, up to 20 MB</p>
      <span class="mt-3 block h-12" aria-hidden="true"></span>
    </div>'''
    p.frame('S14-web-desktop-drag', 'Web, desktop: dragging a file over the page', desktop(f'{appbar()}{stepper(2)}{start_body(drop=drop_on, compact=True)}'))
    p.frame('S14-ios', 'iOS: page sheet, Files picker', phone(f'{iosbar()}{stepper(2)}{start_body().replace("Choose a CSV or Excel file", "Choose a CSV or Excel file")}{bottom(btn("Choose file", "#S14-csv-preview", "choose-file"), note="Opens Files. iCloud Drive and other locations work.")}', 'ios'))
    return p


# =====================================================================================
# S15 Google Sheets
# =====================================================================================
SPREADSHEETS = [
    ('Team offsite October', 'Edited yesterday'),
    ('Frontend hiring pipeline', 'Edited 3 days ago'),
    ('Home office budget', 'Shared by Mert Aydın, edited Oct 2'),
    ('Book club 2026', 'Edited Sep 14'),
    ('Flat hunt 2026', 'Edited Jul 21'),
    ('Moving checklist', 'Edited Jul 3'),
    ('Lisbon trip ideas', 'Edited Jun 12'),
    ('Running log', 'Edited May 30'),
]


def sheet_row(name, meta_, href='#S15-tabs', q=None, action=None):
    da = f' data-action="{action}"' if action else ''
    return f'<li><a href="{href}" class="flex min-h-16 items-center gap-3 px-gutter py-2"{da}><span class="flex size-10 shrink-0 items-center justify-center rounded-sm bg-secondary text-muted-foreground">{icon("sheet")}</span><span class="min-w-0 flex-1"><span class="block truncate text-body">{highlight(name, q)}</span><span class="block truncate text-body-sm text-muted-foreground">{meta_}</span></span>{icon("chevron-right", "size-5 shrink-0 text-muted-foreground")}</a></li>'


def account_row(switch=True):
    s = '<a href="#S15-account-switch" class="inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label-lg text-primary" data-action="switch-account">Switch</a>' if switch else ''
    return f'''<div class="mx-gutter flex min-h-16 items-center gap-3 rounded-group bg-card py-2 pl-4 pr-2"><img src="{IMG}people/u-deniz.svg" alt="" class="size-10 shrink-0 rounded-full"><div class="min-w-0 flex-1"><p class="truncate text-body">deniz.yilmaz@example.com</p><p class="text-body-sm text-muted-foreground">Google account, read-only</p></div>{s}</div>'''


def build_s15():
    p = Page('S15', 'S15-google-sheets.html', 'Google Sheets connection and sheet/tab selection',
             'Select items for the Google Sheets source: connect read-only, pick a spreadsheet, choose one or more tabs, preview, then map fields.')
    S11 = 'S11-source-picker.html#S11-default'
    another = btn('Choose another source', S11, 'another-source', 'ghost', size='md')

    pts = [('eye', 'Read-only', 'SwipeSort sees your spreadsheets to list them. It can\'t change them.'),
           ('file-pen-line', 'Writing only when you export', 'If you export decisions to a sheet later, SwipeSort asks first and shows what it will add.'),
           ('unplug', 'Disconnect any time', 'In Settings, under Connected accounts.')]
    connect = explainer('sheet', 'Connect Google Sheets', 'Sign in with Google to choose a spreadsheet. SwipeSort imports a copy of its rows.', points_list(pts))
    p.section('Connect', 'Google Sheets needs its own read-only permission, even when you signed in to SwipeSort with Google. No SwipeSort account is required. The Google account chooser is native (out of scope).')
    p.frame('S15-default', 'Default: connect explainer', phone(f'''{appbar()}{stepper(2)}{connect}{bottom(btn("Connect Google account", "#S15-spreadsheets", "connect"), another, note="Next, Google asks you to choose an account.")}'''))
    conn = f'''{appbar()}{stepper(2)}{state("loader-circle", "Connecting to Google…", "Finish in the Google window. This takes a few seconds.").replace("size-8 text-muted-foreground", "size-8 animate-spin text-primary").replace('<h2', '<h2 role="status"')}{bottom(None, btn("Cancel", "#S15-default", "cancel", "ghost", size="md"))}'''
    p.frame('S15-connecting', 'Connecting', phone(conn))

    p.section('Choose a spreadsheet', 'Recently edited first, including spreadsheets shared with you. Search filters as you type.')
    lst = ''.join(sheet_row(n, m, action='pick-sheet' if n == 'Flat hunt 2026' else None) for n, m in SPREADSHEETS)

    def sheets_screen(content, q='', fid='s15', bar=None):
        return f'''{bar or appbar()}{stepper(2)}
  {account_row()}
  <div class="shrink-0 px-gutter pb-1 pt-3">{search_field(fid + "-q", q, "Search spreadsheets", "Search spreadsheets")}</div>
  <div class="min-h-0 flex-1 overflow-hidden">{content}</div>'''

    p.frame('S15-spreadsheets', 'Connected: spreadsheet list', phone(sheets_screen(f'<h2 class="px-gutter pb-1 pt-3 text-label text-muted-foreground">Recent</h2><ul class="divide-y">{lst}</ul>')))
    sres = [('Flat hunt 2026', 'Edited Jul 21'), ('Flat hunt 2024', 'Edited Mar 2, 2024')]
    p.frame('S15-search', 'Searching “flat”', phone(sheets_screen(f'<h2 class="px-gutter pb-1 pt-3 text-label text-muted-foreground">2 spreadsheets match “flat”</h2><ul class="divide-y">{"".join(sheet_row(n, m, q="flat", action="pick-sheet" if n == "Flat hunt 2026" else None) for n, m in sres)}</ul>', 'flat', 's15s')))
    sk = ''.join(f'<li class="flex min-h-16 items-center gap-3 px-gutter py-2"><span class="size-10 animate-pulse rounded-sm bg-muted"></span><span class="flex-1 space-y-2"><span class="block h-3.5 w-{w} animate-pulse rounded-full bg-muted"></span><span class="block h-3 w-1/3 animate-pulse rounded-full bg-muted"></span></span></li>' for w in ['2/3', '1/2', '3/5', '2/5', '1/2', '2/3'])
    p.frame('S15-loading', 'Loading spreadsheets', phone(sheets_screen(f'<p class="flex items-center gap-2 px-gutter pb-1 pt-3 text-body-sm text-muted-foreground" role="status">{icon("loader-circle", "size-4 animate-spin text-primary")}Loading spreadsheets…</p><ul aria-hidden="true">{sk}</ul>', fid='s15l')))
    none_sheets = f'''{appbar()}{stepper(2)}{account_row()}{state("sheet", "No spreadsheets in this account", "Create one in Google Sheets, or switch to the account that has your sheet.")}{bottom(btn("Switch account", "#S15-account-switch", "switch-account"), another)}'''
    p.frame('S15-no-spreadsheets', 'Connected account has no spreadsheets', phone(none_sheets))
    sw_body = f'''<ul class="mt-2 divide-y">
      <li class="flex min-h-16 items-center gap-3 py-2"><img src="{IMG}people/u-deniz.svg" alt="" class="size-10 rounded-full"><span class="min-w-0 flex-1"><span class="block text-body">Deniz Yılmaz</span><span class="block truncate text-body-sm text-muted-foreground">deniz.yilmaz@example.com</span></span>{icon("check", "size-5 text-primary")}<span class="sr-only">Connected</span></li>
      <li><button class="flex min-h-14 w-full items-center gap-3 py-2 text-left" data-action="another-account"><span class="flex size-10 items-center justify-center rounded-full bg-secondary">{icon("user-plus")}</span><span class="text-body">Use another Google account</span></button></li>
      <li><button class="flex min-h-14 w-full items-center gap-3 py-2 text-left text-destructive" data-action="disconnect"><span class="flex size-10 items-center justify-center">{icon("unplug")}</span><span class="text-body">Disconnect Google Sheets</span></button></li>
    </ul>
    <p class="mt-2 text-body-sm text-muted-foreground">Disconnecting doesn\'t change your lists or your spreadsheets.</p>'''
    p.frame('S15-account-switch', 'Already connected: switch account sheet', phone(sheets_screen(f'<ul class="divide-y">{lst}</ul>', fid='s15w') + sheet('s15sw', 'Google account', sw_body, '', '#S15-spreadsheets')))

    p.section('Choose tabs and preview', 'One tab, or several with the same columns combined into one list. Combined tabs add a Tab field so items keep their origin. Empty tabs are listed but can\'t be selected.')
    tabs = [('Kadıköy', '4 rows. Address, Rent, Rooms, Size, Viewing, Link', True, False),
            ('Beşiktaş', '4 rows. Address, Rent, Rooms, Size, Viewing, Link', True, False),
            ('Archive 2025', '11 rows. Address, Rent, Rooms, Size, Link', False, False),
            ('Notes', 'No rows', False, True)]

    def tab_rows(tabs_):
        out = ''
        for n, d, on, dis in tabs_:
            if dis:
                out += f'<li><button type="button" role="checkbox" aria-checked="false" disabled class="flex min-h-16 w-full items-center gap-3 px-4 py-2 text-left">{checkbox("off")}<span class="min-w-0 flex-1"><span class="block text-body text-muted-foreground">{n}</span><span class="block text-body-sm text-muted-foreground">{d}, nothing to import</span></span></button></li>'
            else:
                out += f'<li><button type="button" role="checkbox" aria-checked="{"true" if on else "false"}" class="flex min-h-16 w-full items-center gap-3 px-4 py-2 text-left">{checkbox("on" if on else "off")}<span class="min-w-0 flex-1"><span class="block text-body">{n}</span><span class="block text-body-sm text-muted-foreground">{d}</span></span></button></li>'
        return out

    tabs_html = f'''{appbar()}{stepper(2)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("Flat hunt 2026", "4 tabs, edited Jul 21", "sheet", "#S15-spreadsheets")}
    <h2 class="mt-5 text-title-3">Choose tabs</h2>
    <p class="mt-1 text-body-sm text-muted-foreground">Pick one tab, or several with the same columns to combine them.</p>
    <ul class="mt-3 divide-y overflow-hidden rounded-group bg-card">{tab_rows(tabs)}</ul>
    <div class="mt-4">{info_alert("2 tabs become one list", "A Tab field keeps track of where each item came from, so you can still tell Kadıköy from Beşiktaş.", "combine")}</div>
  </div>
  {bottom(btn("Continue with 8 rows", "#S15-preview", "continue"), border=True)}'''
    p.frame('S15-tabs', 'Tabs: Kadıköy and Beşiktaş combined', phone(tabs_html))

    def tab_rows_big(tabs_):
        out = ''
        for n, d, on, dis in tabs_:
            dis_attr = ' disabled' if dis else ''
            tone = ' text-muted-foreground' if dis else ''
            d2 = f'{d}, nothing to import' if dis else d
            out += f'<li><button type="button" role="checkbox" aria-checked="{"true" if on else "false"}"{dis_attr} class="flex min-h-20 w-full items-center gap-4 px-4 py-3 text-left">{checkbox("on" if on else "off")}<span class="min-w-0 flex-1"><span class="block text-title-2 font-normal{tone}">{n}</span><span class="mt-0.5 block text-title-3 font-normal text-muted-foreground">{d2}</span></span></button></li>'
        return out

    tabs_big = f'''{appbar(big=True)}{stepper(2, big=True)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("Flat hunt 2026", "4 tabs, edited Jul 21", "sheet", "#S15-spreadsheets", big=True)}
    <h2 class="mt-5 text-title-1">Choose tabs</h2>
    <ul class="mt-3 divide-y overflow-hidden rounded-group bg-card">{tab_rows_big(tabs)}</ul>
  </div>
  {bottom(btn("Continue with 8 rows", "#S15-preview", "continue", extra="min-h-16 text-title-3"), border=True)}'''
    p.frame('S15-tabs-large-text', 'Large text (200%): tab rows grow and wrap; Continue stays pinned', phone(tabs_big))

    apts = DATA['apartments']
    arows = [[a['tab'], a['address'], f'{a["rent"]:,}', a['rooms'], a['sizeM2'], (a['viewing'] or ''), a['link'].replace('https://', '')] for a in apts]
    prev = f'''{appbar()}{stepper(2)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("Flat hunt 2026", "Kadıköy and Beşiktaş, 8 rows", "sheet", "#S15-tabs")}
    {settings_group(True, detected="Detected in both tabs", show_sep=False)}
    <div class="mt-5 flex items-baseline justify-between px-1 pb-2"><h2 class="text-label text-muted-foreground">Preview</h2><span class="text-caption tabular-nums text-muted-foreground">8 rows</span></div>
    {table(["Tab", "Address", "Rent", "Rooms", "Size", "Viewing", "Link"], arows, "Preview of Flat hunt 2026, tabs Kadıköy and Beşiktaş")}
  </div>
  {bottom(btn("Continue with 8 rows", "S19-field-mapping.html#S19-default", "continue"), border=True)}'''
    p.frame('S15-preview', 'Preview of the combined tabs', phone(prev))

    etabs = [('Packing', 'Column names only', False, True), ('Utilities', 'No rows', False, True)]
    empty_tab = f'''{appbar()}{stepper(2)}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-1 *:shrink-0">
    {file_row("Moving checklist", "2 tabs, edited Jul 3", "sheet", "#S15-spreadsheets")}
    <h2 class="mt-5 text-title-3">Choose tabs</h2>
    <ul class="mt-3 divide-y overflow-hidden rounded-group bg-card">{tab_rows(etabs)}</ul>
    <div class="mt-4 flex gap-3 rounded-control border bg-card p-4" role="note">{icon("file-question", "size-5 shrink-0 text-muted-foreground")}<div><p class="text-label">Nothing to import</p><p class="mt-0.5 text-body-sm text-muted-foreground">Moving checklist has no rows yet. Add rows in Google Sheets, then refresh, or choose another spreadsheet.</p></div></div>
  </div>
  {bottom(btn("Choose another spreadsheet", "#S15-spreadsheets", "another-sheet"), btn("Refresh", None, "refresh", "ghost", size="md"))}'''
    p.frame('S15-empty-tab', 'Empty tabs: nothing to import', phone(empty_tab))

    p.section('Errors and offline', 'Google connection failure (SRC-23), revoked access and no connection. Every state keeps a way to another source.')
    p.frame('S15-error-connection', 'Google connection failure', phone(f'''{appbar()}{stepper(2)}{state("cloud-off", "Google Sheets didn\'t respond", "Check your connection and try again. Nothing was imported.")}{bottom(btn("Try again", None, "retry"), another)}'''))
    p.frame('S15-error-access', 'Access removed in the Google account', phone(f'''{appbar()}{stepper(2)}{state("unplug", "SwipeSort can\'t see your spreadsheets", "Access to Google Sheets was removed from your Google account. Connect again to choose a sheet.")}{bottom(btn("Connect again", "#S15-default", "reconnect"), another)}'''))
    p.frame('S15-offline', 'Offline', phone(f'''{appbar()}{offline_banner()}<div class="h-3 shrink-0"></div>{stepper(2)}{state("wifi-off", "Google Sheets needs a connection", "Connect to the internet and try again, or import from another source. Contacts and files work offline.")}{bottom(btn("Try again", None, "retry"), another)}'''))

    p.section('Web and iOS', 'Desktop and mobile web use a Google popup (OAuth). iOS uses the system web sign-in sheet (out of scope), then the same screens in a page sheet.')
    waiting = f'''{appbar()}{stepper(2)}{state("app-window", "Continue in the Google window", "Choose your account and allow read-only access. SwipeSort continues here when you\'re done.")}{bottom(btn("Open the Google window again", None, "reopen-popup", "outline", size="md"), None)}'''
    popup = f'''<div class="absolute right-10 top-24 z-20 flex h-96 w-96 flex-col overflow-hidden rounded-control border bg-card shadow-dialog" aria-hidden="true">
    <div class="flex h-9 shrink-0 items-center gap-2 border-b bg-secondary px-3 text-caption text-muted-foreground">{icon("lock", "size-3.5")}accounts.google.com</div>
    <div class="flex-1 space-y-3 p-6"><span class="block h-4 w-24 rounded-full bg-muted"></span><span class="block h-6 w-48 rounded-full bg-muted"></span><span class="block h-12 rounded-control bg-muted"></span><span class="block h-12 rounded-control bg-muted"></span><p class="pt-2 text-caption text-muted-foreground">Google sign-in (native, out of scope)</p></div>
  </div>'''
    p.frame('S15-web-desktop', 'Web, desktop: Google sign-in popup open', desktop_with_popup(waiting, popup))
    blocked = f'''{appbar()}{stepper(2)}{state("app-window", "Your browser blocked the Google window", "Allow pop-ups for swipesort.app in the address bar, then try again.")}{bottom(btn("Try again", "#S15-web-desktop", "retry"), another)}'''
    p.frame('S15-web-popup-blocked', 'Web, desktop: popup blocked', desktop(blocked, 'swipesort.app/new/google'))
    ios_sheets = sheets_screen(f'<h2 class="px-gutter pb-1 pt-3 text-label text-muted-foreground">Recent</h2><ul class="divide-y">{lst}</ul>', fid='s15i', bar=iosbar())
    p.frame('S15-ios', 'iOS: spreadsheet list in a page sheet', phone(ios_sheets, 'ios'))
    return p


def desktop_with_popup(content, popup):
    return f'''<div class="desktop">
  <div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">swipesort.app/new/google</span></div>
  <div class="desktop-column">
  {content}
  </div>
  {popup}
</div>'''


if __name__ == '__main__':
    for b in (build_s11, build_s12, build_s13, build_s14, build_s15):
        b().render()
