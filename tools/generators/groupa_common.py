# Shared helpers for the Group A screen generators (S01–S07: onboarding and account).
# Each screen has its own script (tools/generators/Sxx-name.py) that imports this module and writes
# design/03-screens/Sxx-name.html. Run: python3 tools/generators/S03-sign-in.py
# Markup follows design/01-foundations/components.html and the S25 reference generator.
import os
import html as _html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCREENS = os.path.join(ROOT, 'design', '03-screens')
IMG = '../02-data/images/'
BRAND = '../01-foundations/brand/'

ME = dict(name='Deniz Yılmaz', first='Deniz', email='deniz.yilmaz@example.com', avatar=IMG + 'people/u-deniz.svg')
MERT = dict(name='Mert Aydın', first='Mert', email='mert.aydin@example.com', avatar=IMG + 'people/u-mert.svg')
# Lists on this phone before signing in (sample-data me.guest.deviceLists + the wedding list, flow 3)
DEVICE_LISTS = [
    ('Wedding guests', 100, 'users'),
    ('Desk setup', 20, 'armchair'),
    ('March photos clean-up', 30, 'image'),
    ('Frontend hiring, Q4', 12, 'file-spreadsheet'),
]


def esc(s):
    return _html.escape(s, quote=True)


def icon(name, size='size-5', extra=''):
    return f'<i class="i-lucide-{name} {size} {extra}" aria-hidden="true"></i>'.replace('  ', ' ').replace(' "', '"')


# ---------------------------------------------------------------- page, frames, devices
def phone(content, kind='android', screen_cls='', overlay_full=False):
    """kind: android | ios | web (mobile browser, no system bars).
    overlay_full: the frame has a sheet or dialog; its scrim and sheet extend under the system bars
    (the screen stops being the containing block and the bars draw on top)."""
    if overlay_full and kind != 'web':
        return phone(content, kind, (screen_cls + ' static').strip()).replace('class="sysbar-top"', 'class="sysbar-top relative z-50"').replace('class="sysbar-nav"', 'class="sysbar-nav relative z-50"')
    if kind == 'web':
        return f'''<div class="phone">
  <div class="screen {screen_cls}">
  {content}
  </div>
</div>'''
    cls = 'phone-ios' if kind == 'ios' else 'phone'
    return f'''<div class="{cls}">
  <div class="sysbar-top" aria-hidden="true"><span>9:41</span><span class="sysbar-icons"></span></div>
  <div class="screen {screen_cls}">
  {content}
  </div>
  <div class="sysbar-nav" aria-hidden="true"></div>
</div>'''


def desktop(content, url='swipesort.app', column_cls=''):
    return f'''<div class="desktop">
  <div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">{url}</span></div>
  <div class="desktop-column {column_cls}">
  {content}
  </div>
</div>'''


class Page:
    def __init__(self, sid, title, intro, spec):
        self.sid, self.title, self.intro, self.spec = sid, title, intro, spec
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
        body = ''.join(self.parts)
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
  <p>{self.intro} Spec: <a href="{self.spec}">{self.spec}</a>.</p>
</header>
<main class="mock-canvas">
{body}
</main>
</body>
</html>
'''
        html = html.replace('<main class="mock-canvas">\n</main>\n', '', 1)
        path = os.path.join(SCREENS, filename)
        with open(path, 'w') as f:
            f.write(html)
        print(f'{filename}: frames {html.count("data-frame=")}')


# ---------------------------------------------------------------- brand
def mark(size='size-24', extra=''):
    """App mark from brand/ (light and dark files swap with the theme)."""
    return (f'<img src="{BRAND}logo-mark.svg" alt="" class="{size} {extra} dark:hidden">'
            f'<img src="{BRAND}logo-mark-dark.svg" alt="" class="hidden {size} {extra} dark:block">')


def wordmark(size='text-title-1'):
    return f'<span class="{size} tracking-tight">SwipeSort</span>'


# ---------------------------------------------------------------- bars
def appbar(title='', back='arrow-left', href='#', label='Back', actions='', action=None, title_id=None):
    act = f' data-action="{action}"' if action else ''
    tid = f' id="{title_id}"' if title_id else ''
    back_html = f'<a href="{href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{label}"{act}>{icon(back, "size-6")}</a>' if back else '<span class="size-3"></span>'
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    {back_html}
    <h1{tid} class="min-w-0 flex-1 truncate px-1 text-title-3">{title}</h1>
    {actions}
  </header>'''


def text_action(label, href='#', action=None, primary=True):
    act = f' data-action="{action}"' if action else ''
    col = 'text-primary' if primary else ''
    return f'<a href="{href}" class="inline-flex h-12 shrink-0 items-center rounded-control px-4 text-label-lg {col}"{act}>{label}</a>'


def icon_action(name, label, href='#', action=None):
    act = f' data-action="{action}"' if action else ''
    return f'<a href="{href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{label}"{act}>{icon(name, "size-6")}</a>'


def large_title(title, actions=''):
    return f'''<header class="shrink-0">
    <div class="flex h-app-bar items-center justify-end gap-1 px-1">{actions}</div>
    <h1 class="px-gutter pb-2 text-title-1">{title}</h1>
  </header>'''


def ios_nav(title='', back_text=None, href='#', trailing='', leading=None, large=None, action=None, center_bold=True):
    """iOS navigation bar: chevron + previous title (or a text leading item such as Cancel), centered title."""
    act = f' data-action="{action}"' if action else ''
    if leading is not None:
        lead = leading
    elif back_text is not None:
        lead = f'<a href="{href}" class="inline-flex h-12 items-center gap-0.5 justify-self-start pr-2 text-body text-primary"{act}>{icon("chevron-left", "size-6")}{back_text}</a>'
    else:
        lead = '<span></span>'
    ttl = f'<h1 class="truncate text-body font-semibold">{title}</h1>' if title and not large else '<span></span>'
    lt = f'<h1 class="px-5 pb-2 pt-1 text-title-1">{large}</h1>' if large else ''
    return f'''<header class="shrink-0">
    <div class="grid h-12 grid-cols-[1fr_auto_1fr] items-center gap-2 px-2">
      {lead}
      {ttl}
      <div class="flex justify-self-end">{trailing}</div>
    </div>
    {lt}
  </header>'''


def ios_text_btn(label, href='#', bold=False, action=None, disabled=False):
    act = f' data-action="{action}"' if action else ''
    w = ' font-semibold' if bold else ''
    if disabled:
        return f'<button class="inline-flex h-12 items-center px-2 text-body text-primary opacity-50{w}" disabled>{label}</button>'
    return f'<a href="{href}" class="inline-flex h-12 items-center px-2 text-body text-primary{w}"{act}>{label}</a>'


def bottom_nav(active='settings', badge=3):
    items = [('lists', 'Lists', 'list-checks', 'S08-home.html#S08-default'),
             ('activity', 'Activity', 'activity', 'S38-activity.html#S38-default'),
             ('settings', 'Settings', 'settings', 'S06-settings.html#S06-default')]
    out = []
    for key, label, ic, href in items:
        if key == active:
            out.append(f'<a href="{href}" class="flex flex-1 flex-col items-center justify-center gap-1 text-caption" aria-current="page"><span class="flex h-8 w-16 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon(ic, "size-6")}</span><span class="font-semibold">{label}</span></a>')
        elif key == 'activity' and badge:
            out.append(f'<a href="{href}" class="flex flex-1 flex-col items-center justify-center gap-1 text-caption text-muted-foreground" aria-label="Activity, {badge} unread"><span class="relative flex h-8 w-16 items-center justify-center">{icon(ic, "size-6")}<span class="absolute right-3 top-0 flex h-5 min-w-5 items-center justify-center rounded-full bg-primary px-1 text-caption leading-none text-primary-foreground">{badge}</span></span>{label}</a>')
        else:
            out.append(f'<a href="{href}" class="flex flex-1 flex-col items-center justify-center gap-1 text-caption text-muted-foreground"><span class="flex h-8 w-16 items-center justify-center">{icon(ic, "size-6")}</span>{label}</a>')
    return f'<nav class="flex h-bottom-nav shrink-0 border-t bg-card" aria-label="Main">{"".join(out)}</nav>'


def ios_tab_bar(active='settings', badge=3):
    items = [('lists', 'Lists', 'list-checks', 'S08-home.html#S08-default'),
             ('activity', 'Activity', 'activity', 'S38-activity.html#S38-default'),
             ('settings', 'Settings', 'settings', 'S06-settings.html#S06-default')]
    out = []
    for key, label, ic, href in items:
        cur = ' aria-current="page"' if key == active else ''
        col = 'text-primary' if key == active else 'text-muted-foreground'
        b = ''
        lab = ''
        if key == 'activity' and badge:
            b = f'<span class="absolute -right-2.5 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-primary px-1 text-caption leading-none text-primary-foreground">{badge}</span>'
            lab = f' aria-label="Activity, {badge} unread"'
        out.append(f'<a href="{href}" class="flex flex-1 flex-col items-center justify-center gap-0.5 text-caption {col}"{cur}{lab}><span class="relative">{icon(ic, "size-6")}{b}</span>{label}</a>')
    return f'<nav class="flex h-14 shrink-0 border-t bg-card" aria-label="Main">{"".join(out)}</nav>'


# ---------------------------------------------------------------- buttons
_VARIANTS = {
    'primary': 'bg-primary text-primary-foreground',
    'secondary': 'bg-secondary text-secondary-foreground',
    'outline': 'border border-input bg-card',
    'ghost': '',
    'destructive': 'bg-destructive text-destructive-foreground',
    'foreground': 'bg-foreground text-background',
}


def btn(label, kind='primary', href=None, action=None, size='lg', full=True, icon_name=None, disabled=False,
        busy=False, extra='', aria=None, lead=None):
    h = {'lg': 'h-14', 'md': 'h-12', 'sm': 'h-10'}[size]
    w = 'w-full' if full else ''
    cls = f'inline-flex {h} {w} items-center justify-center gap-2 rounded-control px-5 text-label-lg {_VARIANTS[kind]} {extra}'
    cls = ' '.join(cls.split())
    ic = ''
    if busy:
        ic = icon('loader-circle', 'size-5 animate-spin')
    elif lead:
        ic = lead
    elif icon_name:
        ic = icon(icon_name)
    act = f' data-action="{action}"' if action else ''
    ar = f' aria-label="{aria}"' if aria else ''
    if disabled:
        return f'<button type="button" class="{cls} opacity-50" disabled{ar}>{ic}{label}</button>'
    if busy:
        return f'<button type="button" class="{cls}" aria-busy="true"{ar}>{ic}{label}</button>'
    if href:
        return f'<a href="{href}" class="{cls}"{act}{ar}>{ic}{label}</a>'
    return f'<button type="button" class="{cls}"{act}{ar}>{ic}{label}</button>'


def link(label, href='#', action=None, extra=''):
    act = f' data-action="{action}"' if action else ''
    return f'<a href="{href}" class="inline-flex min-h-touch items-center text-label-lg text-primary underline underline-offset-4 {extra}"{act}>{label}</a>'


# Provider marks. The coding agent replaces these stand-ins with the official assets (see S03 spec §8):
# Google "G" logo per Google Identity branding, Apple logo via the native AppleAuthenticationButton.
GOOGLE_G = '<span class="flex size-6 items-center justify-center rounded-full border border-input bg-card text-label font-bold leading-none text-foreground" aria-hidden="true">G</span>'
APPLE_MARK = icon('apple', 'size-5')


def google_btn(href='#', action='continue-google', label='Continue with Google', busy=False, disabled=False, size='lg'):
    if busy:
        return btn('Signing in…', 'outline', busy=True, size=size)
    return btn(label, 'outline', href=href, action=action, lead=GOOGLE_G, disabled=disabled, size=size)


def apple_btn(href='#', action='continue-apple', label='Continue with Apple', disabled=False, size='lg'):
    return btn(label, 'foreground', href=href, action=action, lead=APPLE_MARK, disabled=disabled, size=size)


def email_btn(href='#', action='continue-email', label='Continue with email', disabled=False, size='lg'):
    return btn(label, 'outline', href=href, action=action, icon_name='mail', disabled=disabled, size=size)


# ---------------------------------------------------------------- form fields
def field(fid, label, value='', placeholder='', type='text', state='default', helper=None, error=None,
          autocomplete=None, trailing=None, label_extra=''):
    base = 'h-12 w-full rounded-control bg-card px-3.5 text-body placeholder:text-muted-foreground'
    if state == 'focused':
        b = 'border border-primary ring-2 ring-ring/30'
    elif state == 'error':
        b = 'border-2 border-destructive'
    elif state == 'disabled':
        b = 'border border-input bg-muted text-muted-foreground'
    else:
        b = 'border border-input'
    pr = ' pr-12' if trailing else ''
    desc = ''
    aria = ''
    if error:
        desc = f'<p id="{fid}-e" class="mt-1.5 flex items-start gap-1.5 text-body-sm text-destructive">{icon("circle-alert", "size-4 mt-0.5 shrink-0")}<span>{error}</span></p>'
        aria = f' aria-invalid="true" aria-describedby="{fid}-e"'
    elif helper:
        desc = f'<p id="{fid}-h" class="mt-1.5 text-body-sm text-muted-foreground">{helper}</p>'
        aria = f' aria-describedby="{fid}-h"'
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ''
    val = f' value="{esc(value)}"' if value else ''
    ph = f' placeholder="{esc(placeholder)}"' if placeholder else ''
    dis = ' disabled' if state == 'disabled' else ''
    inp = f'<input id="{fid}" type="{type}" class="{base} {b}{pr}"{val}{ph}{ac}{aria}{dis}>'
    if trailing:
        inp = f'<div class="relative mt-1.5">{inp}{trailing}</div>'
    else:
        inp = inp.replace('class="', 'class="mt-1.5 ', 1)
    return f'<div><label for="{fid}" class="text-label {label_extra}">{label}</label>{inp}{desc}</div>'


def eye_toggle(shown=False):
    lab = 'Hide password' if shown else 'Show password'
    return f'<button type="button" class="absolute right-0 top-0 flex size-12 items-center justify-center rounded-full text-muted-foreground" aria-label="{lab}">{icon("eye-off" if shown else "eye")}</button>'


def password_field(fid, label='Password', value='', state='default', error=None, helper=None, shown=False,
                   autocomplete='current-password', placeholder=''):
    return field(fid, label, value=value, type='text' if shown else 'password', state=state, error=error,
                 helper=helper, autocomplete=autocomplete, trailing=eye_toggle(shown), placeholder=placeholder)


def pw_rules(fid, rules):
    """rules: list of (text, status) where status is 'met' | 'todo' | 'fail'."""
    out = []
    for text, st in rules:
        if st == 'met':
            out.append(f'<li class="flex items-center gap-2 text-foreground">{icon("circle-check", "size-4 shrink-0")}<span>{text}<span class="sr-only">, done</span></span></li>')
        elif st == 'fail':
            out.append(f'<li class="flex items-center gap-2 text-destructive">{icon("circle-alert", "size-4 shrink-0")}<span>{text}<span class="sr-only">, missing</span></span></li>')
        else:
            out.append(f'<li class="flex items-center gap-2 text-muted-foreground">{icon("circle", "size-4 shrink-0")}<span>{text}</span></li>')
    return f'<ul id="{fid}" class="mt-2 space-y-1 text-body-sm" aria-label="Password rules">{"".join(out)}</ul>'


# ---------------------------------------------------------------- groups and rows
def group(rows, header=None, footer=None, ios=False, extra=''):
    h = f'<h2 class="px-1 pb-2 text-label text-muted-foreground">{header}</h2>' if header else ''
    f = f'<p class="px-1 pt-2 text-body-sm text-muted-foreground">{footer}</p>' if footer else ''
    rad = 'rounded-control' if ios else 'rounded-group'
    return f'<section class="{extra}">{h}<ul class="divide-y overflow-hidden {rad} bg-card dark:border">{"".join(rows)}</ul>{f}</section>'


def _lead(icon_name, avatar=None, muted=True, destructive=False):
    if avatar:
        return avatar
    if not icon_name:
        return ''
    col = 'text-destructive' if destructive else ('text-muted-foreground' if muted else '')
    return icon(icon_name, f'size-5 shrink-0 {col}')


def nav_row(title, href='#', icon_name=None, desc=None, value=None, trailing='chevron', action=None,
            destructive=False, avatar=None, aria=None, external=False, title_cls='text-body', ios=False):
    act = f' data-action="{action}"' if action else ''
    ar = f' aria-label="{aria}"' if aria else ''
    tcol = ' text-destructive' if destructive else ''
    d = f'<span class="block text-body-sm text-muted-foreground">{desc}</span>' if desc else ''
    v = f'<span class="shrink-0 text-body text-muted-foreground">{value}</span>' if value else ''
    if external:
        tr = icon('external-link', 'size-5 shrink-0 text-muted-foreground')
    elif trailing == 'chevron':
        tr = icon('chevron-right', 'size-5 shrink-0 text-muted-foreground')
    else:
        tr = trailing or ''
    pad = 'px-4' if not ios else 'px-4'
    return f'<li><a href="{href}" class="flex min-h-14 items-center gap-4 {pad} py-3{tcol}"{act}{ar}>{_lead(icon_name, avatar, destructive=destructive)}<span class="min-w-0 flex-1"><span class="block {title_cls}">{title}</span>{d}</span>{v}{tr}</a></li>'


def button_row(title, icon_name=None, desc=None, destructive=False, action=None, href=None):
    tcol = ' text-destructive' if destructive else ''
    act = f' data-action="{action}"' if action else ''
    d = f'<span class="block text-body-sm text-muted-foreground">{desc}</span>' if desc else ''
    inner = f'{_lead(icon_name, destructive=destructive)}<span class="min-w-0 flex-1"><span class="block text-body">{title}</span>{d}</span>'
    if href:
        return f'<li><a href="{href}" class="flex min-h-14 w-full items-center gap-4 px-4 py-3 text-left{tcol}"{act}>{inner}</a></li>'
    return f'<li><button type="button" class="flex min-h-14 w-full items-center gap-4 px-4 py-3 text-left{tcol}"{act}>{inner}</button></li>'


def switch(on, label, disabled=False):
    op = ' opacity-50' if disabled else ''
    dis = ' aria-disabled="true"' if disabled else ''
    if on:
        return f'<span role="switch" aria-checked="true" aria-label="{label}" class="flex h-8 w-13 shrink-0 items-center rounded-full bg-primary p-1{op}"{dis}><span class="ml-auto size-6 rounded-full bg-primary-foreground"></span></span>'
    return f'<span role="switch" aria-checked="false" aria-label="{label}" class="flex h-8 w-13 shrink-0 items-center rounded-full border-2 border-input bg-muted p-1{op}"{dis}><span class="size-5 rounded-full bg-muted-foreground"></span></span>'


def switch_row(title, on, desc=None, icon_name=None, disabled=False, label=None, unavailable=None):
    """unavailable: (reason, link_href) for web-unavailable rows; title muted, reason at full contrast."""
    tcol = ' text-muted-foreground' if (disabled or unavailable) else ''
    d = ''
    if unavailable:
        reason, href = unavailable
        d = f'<span class="block text-body-sm text-muted-foreground">{reason} <a href="{href}" class="text-primary underline underline-offset-4">Get the app</a></span>'
    elif desc:
        d = f'<span class="block text-body-sm text-muted-foreground">{desc}</span>'
    return f'<li class="flex min-h-14 items-center gap-4 px-4 py-3">{_lead(icon_name)}<span class="min-w-0 flex-1"><span class="block text-body{tcol}">{title}</span>{d}</span>{switch(on, label or title, disabled or bool(unavailable))}</li>'


def radio_group(name, options, label):
    """options: list of (title, desc, checked)."""
    out = []
    for title, desc, checked in options:
        d = f'<span class="block text-body-sm text-muted-foreground">{desc}</span>' if desc else ''
        dot = ('<span class="flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary" aria-hidden="true"><span class="size-3 rounded-full bg-primary"></span></span>'
               if checked else '<span class="size-6 shrink-0 rounded-full border-2 border-input" aria-hidden="true"></span>')
        out.append(f'<button type="button" role="radio" aria-checked="{"true" if checked else "false"}" class="flex min-h-14 w-full items-center gap-4 px-4 py-3 text-left">{dot}<span class="min-w-0 flex-1"><span class="block text-body">{title}</span>{d}</span></button>')
    return f'<div role="radiogroup" aria-label="{label}" class="divide-y overflow-hidden rounded-group bg-card dark:border">{"".join(out)}</div>'


def avatar(src=None, initials='', size='size-10', text='text-label', alt=''):
    if src:
        return f'<img src="{src}" alt="{alt}" class="{size} shrink-0 rounded-full object-cover">'
    role = f' role="img" aria-label="{alt}"' if alt else ' aria-hidden="true"'
    return f'<span class="flex {size} shrink-0 items-center justify-center rounded-full bg-muted {text} text-muted-foreground"{role}>{initials}</span>'


# ---------------------------------------------------------------- feedback
def snackbar(text, action=None, bottom='bottom-6', role='status', icon_name=None, action_href='#', data_action=None):
    da = f' data-action="{data_action}"' if data_action else ''
    act = f'<a href="{action_href}" class="-my-1 inline-flex h-12 items-center rounded-sm px-3 text-label text-primary-inverse"{da}>{action}</a>' if action else ''
    ic = icon(icon_name, 'size-5 shrink-0') if icon_name else ''
    pad = 'py-1.5 pl-4 pr-1.5' if action else 'px-4 py-3'
    return f'<div class="absolute inset-x-4 {bottom} z-40 flex min-h-12 items-center gap-3 rounded-control bg-foreground {pad} text-background shadow-overlay" role="{role}">{ic}<span class="flex-1 text-body-sm">{text}</span>{act}</div>'


def offline_banner(text="You're offline. Signing in needs a connection."):
    return f'<div class="mb-3 flex shrink-0 items-center gap-2 bg-muted px-gutter py-2 text-body-sm" role="status">{icon("wifi-off", "size-4 shrink-0")}<span class="flex-1">{text}</span></div>'


def alert_error(title, body=None, action=None, extra=''):
    b = f'<p class="mt-0.5 text-body-sm text-muted-foreground">{body}</p>' if body else ''
    a = f'<div class="mt-2">{action}</div>' if action else ''
    return f'<div class="flex gap-3 rounded-control border border-destructive/40 bg-card p-4 {extra}" role="alert">{icon("circle-alert", "size-5 shrink-0 text-destructive")}<div class="min-w-0 flex-1"><p class="text-label">{title}</p>{b}{a}</div></div>'


def alert_info(title, body=None, icon_name='info', extra='', role='note'):
    b = f'<p class="mt-0.5 text-body-sm">{body}</p>' if body else ''
    return f'<div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground {extra}" role="{role}">{icon(icon_name, "size-5 shrink-0")}<div class="min-w-0 flex-1"><p class="text-label">{title}</p>{b}</div></div>'


def alert_neutral(title, body=None, icon_name='monitor-smartphone', action=None, extra=''):
    b = f'<p class="mt-0.5 text-body-sm text-muted-foreground">{body}</p>' if body else ''
    a = f'<div class="mt-1">{action}</div>' if action else ''
    return f'<div class="flex gap-3 rounded-control border bg-card p-4 {extra}" role="note">{icon(icon_name, "size-5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="text-label">{title}</p>{b}{a}</div></div>'


def spinner(text, extra=''):
    return f'<div class="flex items-center gap-3 text-body text-muted-foreground {extra}" role="status">{icon("loader-circle", "size-6 animate-spin text-primary")}{text}</div>'


# ---------------------------------------------------------------- overlays
def scrim(z='z-20', strength='bg-scrim/50'):
    return f'<div class="absolute inset-0 {z} {strength}" aria-hidden="true"></div>'


def dialog(did, title, body, actions, z='z-40', role='alertdialog', extra_body=''):
    return f'''{scrim('z-30')}
  <div class="absolute inset-x-6 top-1/2 {z} -translate-y-1/2 rounded-dialog bg-popover p-6 shadow-dialog" role="{role}" aria-modal="true" aria-labelledby="{did}-t" aria-describedby="{did}-d">
    <h2 id="{did}-t" class="text-title-3">{title}</h2>
    <p id="{did}-d" class="mt-2 text-body text-muted-foreground">{body}</p>
    {extra_body}
    <div class="mt-6 flex flex-wrap justify-end gap-2">{actions}</div>
  </div>'''


def dlg_btn(label, kind='ghost', href=None, action=None, disabled=False):
    cls = {'ghost': '', 'destructive': 'bg-destructive text-destructive-foreground', 'primary': 'bg-primary text-primary-foreground'}[kind]
    act = f' data-action="{action}"' if action else ''
    if disabled:
        return f'<button type="button" class="inline-flex h-12 items-center rounded-control px-4 text-label-lg {cls} opacity-50" disabled>{label}</button>'
    if href:
        return f'<a href="{href}" class="inline-flex h-12 items-center rounded-control px-4 text-label-lg {cls}"{act}>{label}</a>'
    return f'<button type="button" class="inline-flex h-12 items-center rounded-control px-4 text-label-lg {cls}"{act}>{label}</button>'


def sheet(sid, content, title=None, close_href=None, ios=False, top=None, z='z-30', pad='pb-6'):
    """Bottom sheet (Android, M3) or iOS page sheet (top set) over a scrim."""
    t = ''
    if title:
        close = f'<a href="{close_href or "#"}" class="-mr-3 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</a>'
        t = f'<div class="flex items-center justify-between gap-3 pt-2"><h2 id="{sid}-t" class="text-title-3">{title}</h2>{close}</div>'
    pos = f'{top} bottom-0' if top else 'bottom-0'
    lab = f' aria-labelledby="{sid}-t"'
    return f'''{scrim('z-20')}
  <div class="absolute inset-x-0 {pos} {z} flex flex-col rounded-t-sheet bg-popover px-gutter {pad} pt-2 shadow-sheet" role="dialog" aria-modal="true"{lab}>
    <div class="flex shrink-0 justify-center py-1.5" aria-hidden="true"><span class="h-1 {"w-9" if ios else "w-8"} rounded-full bg-muted-foreground/40"></span></div>
    {t}
    {content}
  </div>'''
