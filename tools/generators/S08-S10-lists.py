# Usage: python3 tools/generators/S08-S10-lists.py
# Writes design/03-screens/S08-home.html, S09-list-overview.html and S10-list-management.html (Group B, Lists).
# Reuses Group A helpers (groupa_common.py) and follows the S25 reference markup.
import re
from groupa_common import *

F08, F09, F10 = 'S08-home.html', 'S09-list-overview.html', 'S10-list-management.html'

# Overlays (scrims, dialogs, sheets) are marked and placed at device level so the scrim also covers the
# placeholder system bars (QA-053) and, on desktop, the whole viewport (QA-065).
OV0, OV1 = '<!--OV-->', '<!--/OV-->'


def ov(x):
    return OV0 + x + OV1


_phone, _desktop = phone, desktop


def _split_ov(content):
    m = re.search(r'<!--OV-->(.*)<!--/OV-->', content, re.S)
    if not m:
        return content, ''
    return content[:m.start()] + content[m.end():], m.group(1)


def phone(content, kind='android', screen_cls=''):
    inner, over = _split_ov(content)
    if not over or kind == 'web':
        return _phone(inner + over, kind, screen_cls)
    out = _phone(inner, kind, screen_cls)
    i = out.rstrip().rfind('</div>')
    return out[:i] + over + '\n' + out[i:]


def desktop(content, url='swipesort.app', column_cls=''):
    inner, over = _split_ov(content)
    if not over:
        return _desktop(inner, url, column_cls)
    over = over.replace('absolute inset-x-6 top-1/2', 'absolute left-1/2 top-1/2 w-full max-w-sm -translate-x-1/2')
    out = _desktop(inner, url, column_cls).replace('<div class="desktop-column', '<div class="relative flex min-h-0 flex-1 flex-col"><div class="desktop-column', 1)
    i = out.rstrip().rfind('</div>')
    return out[:i] + over + '</div>\n' + out[i:]


# Count badges use primary (QA-057).
_bn, _itb, _nav_row = bottom_nav, ios_tab_bar, nav_row
_BADGE_OLD = 'bg-destructive px-1 text-caption leading-none text-destructive-foreground'
_BADGE_NEW = 'bg-primary px-1 text-caption leading-none text-primary-foreground'


def bottom_nav(*a, **k):
    return _bn(*a, **k).replace(_BADGE_OLD, _BADGE_NEW)


def ios_tab_bar(*a, **k):
    return _itb(*a, **k).replace(_BADGE_OLD, _BADGE_NEW)


def nav_row(*a, **k):
    """Value rows: the label keeps its width, the value truncates (QA-063)."""
    out = _nav_row(*a, **k)
    if k.get('value'):
        out = out.replace('<span class="min-w-0 flex-1"><span class="block', '<span class="shrink-0"><span class="block', 1)
        out = out.replace('<span class="shrink-0 text-body text-muted-foreground">', '<span class="min-w-0 flex-1 truncate text-right text-body text-muted-foreground">', 1)
    return out


def h08(f): return f'{F08}#{f}'
def h09(f): return f'{F09}#{f}'
def h10(f): return f'{F10}#{f}'


S11 = 'S11-source-picker.html#S11-default'
DECISIONS = [('reject', 'x', 'rejected'), ('maybe', 'circle-help', 'maybe'), ('accept', 'check', 'accepted')]


# ================================================================ small building blocks
def pct(n, t):
    return round(n * 100 / t) if t else 0


def wcls(p):
    return 'w-full' if p >= 100 else ('w-0' if p <= 0 else f'w-[{p}%]')


def pbar(d, t, h='h-1.5', label=None, extra='flex-1'):
    lab = label or f'{d} of {t} decided'
    return (f'<div class="{h} {extra} overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="{d}" '
            f'aria-valuemin="0" aria-valuemax="{t}" aria-label="{lab}"><div class="h-full {wcls(pct(d, t))} rounded-full bg-primary"></div></div>')


def split_bar(rej, may, acc, total, h='h-2'):
    segs = ''.join(f'<div class="{c} {wcls(pct(n, total))}"></div>' for n, c in ((rej, 'bg-reject'), (may, 'bg-maybe'), (acc, 'bg-accept')) if n)
    left = total - rej - may - acc
    rest = f', {left} not decided' if left else ''
    return f'<div class="flex {h} gap-0.5 overflow-hidden rounded-full bg-muted" role="img" aria-label="{rej} rejected, {may} maybe, {acc} accepted{rest}">{segs}</div>'


def status_bar(agreed, conflict, pending, total=100, h='h-2'):
    return (f'<div class="flex {h} gap-0.5 overflow-hidden rounded-full bg-muted" role="img" aria-label="{agreed} agreed, {conflict} in conflict, {pending} pending">'
            f'<div class="{wcls(pct(agreed, total))} bg-foreground"></div><div class="{wcls(pct(conflict, total))} bg-foreground/50"></div></div>')


def chip(text, kind='secondary', ic=None, extra=''):
    cls = {
        'secondary': 'bg-secondary text-secondary-foreground',
        'muted': 'bg-muted text-muted-foreground',
        'outline': 'border',
        'conflict': 'bg-conflict text-conflict-foreground',
        'primary': 'bg-primary-soft text-primary-soft-foreground',
        'dashed': 'border border-dashed border-input text-muted-foreground',
    }[kind]
    i = icon(ic, 'size-4') if ic else ''
    return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full px-2.5 text-caption {cls} {extra}">{i}{text}</span>'


def decision_chips(rej, may, acc, extra='mt-3'):
    vals = {'reject': rej, 'maybe': may, 'accept': acc}
    out = ''.join(f'<span class="inline-flex h-7 items-center gap-1 rounded-full bg-{k}-soft px-2 text-caption text-{k}-soft-foreground">{icon(ic, "size-4")}<span class="tabular-nums">{vals[k]}</span> {lab}</span>'
                  for k, ic, lab in DECISIONS)
    return f'<!-- Proposed component: DecisionCountChips --><div class="flex flex-wrap gap-1.5 {extra}">{out}</div>'


def counts_inline(rej, may, acc, size='text-caption'):
    vals = {'reject': rej, 'maybe': may, 'accept': acc}
    out = ''.join(f'<span class="inline-flex items-center gap-1 text-{k}-soft-foreground">{icon(ic, "size-4")}<span class="tabular-nums">{vals[k]}</span> {lab}</span>'
                  for k, ic, lab in DECISIONS)
    return f'<span class="flex flex-wrap gap-x-4 gap-y-1 {size}">{out}</span>'.replace('size-4', 'size-6' if size == 'text-body-lg' else 'size-4')


def mi(ic, text, extra=''):
    """Meta item: icon + text, as a separate labeled piece (no middle dots)."""
    return f'<span class="inline-flex items-center gap-1.5 {extra}">{icon(ic, "size-4 shrink-0")}{text}</span>'


def stack(names=('deniz', 'mert', 'selin'), size='size-7', ring='ring-card', text='text-caption'):
    out = []
    for n in names:
        if n == 'selin':
            out.append(f'<span class="flex {size} items-center justify-center rounded-full bg-muted {text} text-muted-foreground ring-2 {ring}">SY</span>')
        else:
            out.append(f'<img src="{IMG}people/u-{n}.svg" alt="" class="{size} rounded-full ring-2 {ring}">')
    return f'<span class="flex shrink-0 -space-x-2" aria-hidden="true">{"".join(out)}</span>'


def card(inner, extra='', label=None):
    lab = f' aria-labelledby="{label}"' if label else ''
    return f'<section class="rounded-group bg-card p-4 dark:border {extra}"{lab}>{inner}</section>'


def card_head(title, right='', hid=None, ic=None):
    i = icon(ic, 'size-5 shrink-0') if ic else ''
    idattr = f' id="{hid}"' if hid else ''
    r = f'<span class="shrink-0 text-caption text-muted-foreground">{right}</span>' if right else ''
    return f'<div class="flex items-center justify-between gap-3"><h2{idattr} class="flex items-center gap-2 text-label">{i}{title}</h2>{r}</div>'


def decided(d, t, extra='mt-3', size='text-title-3'):
    return f'<p class="{extra} {size} tabular-nums">{d} / {t} decided</p><div class="mt-2 flex">{pbar(d, t)}</div>'


def note_line(text, ic='info', extra='mt-3'):
    return f'<p class="{extra} flex items-start gap-2 text-body-sm text-muted-foreground">{icon(ic, "size-4 mt-0.5 shrink-0")}<span>{text}</span></p>'


def heading_row(title, link_text=None, href='#', hid=None):
    idattr = f' id="{hid}"' if hid else ''
    lk = f'<a href="{href}" class="inline-flex min-h-touch items-center px-1 text-label text-primary">{link_text}</a>' if link_text else ''
    return f'<div class="flex items-center justify-between px-1"><h2{idattr} class="text-label text-muted-foreground">{title}</h2>{lk}</div>'


def inert(s):
    """Non-interactive copy of a screen for backgrounds under menus, sheets and dialogs."""
    s = re.sub(r'<(a|button)\b([^>]*)>', r'<span\2>', s)
    s = re.sub(r'</(a|button)>', '</span>', s)
    s = re.sub(r'<(/?)h[1-6]\b', r'<\1p', s)
    s = re.sub(r'<(/?)(nav|section|header)\b', r'<\1div', s)
    s = re.sub(r'\s(id|role|href|data-action|tabindex|aria-[a-z]+)="[^"]*"', '', s)
    s = re.sub(r'\sdisabled\b', '', s)
    return f'<div class="flex min-h-0 flex-1 flex-col" aria-hidden="true">{s}</div>'


# ================================================================ S08 Home
def resume(href, name, action=None):
    act = f' data-action="{action}"' if action else ''
    return (f'<!-- Proposed component: ResumeButton (ListRow trailing action) --><a href="{href}" class="mr-3 flex min-h-touch shrink-0 items-center" aria-label="Resume sorting {name}"{act}>'
            f'<span class="inline-flex h-9 items-center gap-1.5 rounded-full bg-secondary px-3.5 text-label text-secondary-foreground">{icon("play", "size-4")}Resume</span></a>')


def list_row(name, href, meta, below='', trailing='', clamp='truncate', name_cls='text-title-3', unread=False, pad='py-4', meta_cls='text-body-sm', stack=False):
    dot = '<span class="size-2 shrink-0 rounded-full bg-primary" aria-hidden="true"></span><span class="sr-only">New activity. </span>' if unread else ''
    b = f'<span class="mt-2 flex items-center gap-3">{below}</span>' if below else ''
    if stack:
        t = f'<div class="-mt-2 px-4 pb-4">{trailing.replace("mr-3 ", "").replace("h-9 ", "h-11 ").replace("text-label ", "text-title-3 ")}</div>' if trailing else ''
        return f'''<li class="flex flex-col"><a href="{href}" class="flex min-w-0 flex-col gap-1 {pad} px-4">
        <span class="flex items-center gap-2">{dot}<span class="min-w-0 {clamp} {name_cls}">{name}</span></span>
        <span class="flex flex-wrap items-center gap-x-3 gap-y-1.5 {meta_cls} text-muted-foreground">{meta}</span>{b}
      </a>{t}</li>'''
    return f'''<li class="flex items-center"><a href="{href}" class="flex min-w-0 flex-1 flex-col gap-1 {pad} pl-4 {"pr-2" if trailing else "pr-4"}">
        <span class="flex items-center gap-2">{dot}<span class="min-w-0 {clamp} {name_cls}">{name}</span></span>
        <span class="flex flex-wrap items-center gap-x-3 gap-y-1.5 {meta_cls} text-muted-foreground">{meta}</span>{b}
      </a>{trailing}</li>'''


def bar_below(d, t, cap='text-caption'):
    return f'{pbar(d, t)}<span class="shrink-0 {cap} tabular-nums text-muted-foreground">{d} / {t}</span>'


def rows_lists(mode='signed', resume_wed=None, new_conflicts=False, drop=(), resume_action=False, big=False, device_label='On this phone only'):
    """The 4 active sample lists, ordered by latest activity. Signed in, "Frontend hiring, Q4" is on this phone
    only (A-139), so its row carries the muted per-list label (A-137); device_label=None leaves it out."""
    nc = 'text-title-1' if big else 'text-title-3'
    mc = 'text-title-3 font-normal' if big else 'text-body-sm'
    cap = 'text-body-lg' if big else 'text-caption'
    cl = 'line-clamp-2' if big else 'truncate'
    rows = []
    if 'wed' not in drop:
        if mode == 'signed':
            chips = chip('3 new conflicts' if new_conflicts else '15 conflicts', 'conflict', 'git-compare-arrows')
            if big:  # chips scale with the font (200%)
                chips = chips.replace('h-7 ', 'min-h-10 py-1 ').replace('px-2.5 text-caption', 'px-3 text-body-lg').replace('size-4', 'size-6')
            meta = mi('users', 'Shared with 2') + chips
            href = h09('S09-shared')
            rs = resume('S25-sorting.html#S25-shared', 'Wedding guests')
        else:
            meta = mi('circle-dot', 'Round 1 in progress')
            href = h09('S09-guest-wedding')
            rs = resume('S25-sorting.html#S25-default', 'Wedding guests', 'resume' if resume_action else None)
        rows.append(list_row('Wedding guests', href, meta, bar_below(76, 100, cap), rs, unread=new_conflicts, name_cls=nc, meta_cls=mc, clamp=cl, stack=big))
    if 'hiring' not in drop:
        hmeta = mi('circle-dashed', 'Not sorted yet, 12 items')
        if mode == 'signed' and device_label:
            hmeta += mi('cloud-off', device_label)
        rows.append(list_row('Frontend hiring, Q4', h09('S09-new-list'), hmeta, name_cls=nc, meta_cls=mc, clamp=cl, stack=big))
    if 'photos' not in drop and 'trip' not in drop:
        rows.append(list_row('Trip ideas', h09('S09-default'), mi('circle-dot', 'Round 1 in progress'), bar_below(12, 30, cap),
                             resume('S25-sorting.html#S25-photo', 'Trip ideas'), name_cls=nc, meta_cls=mc, clamp=cl, stack=big))
    if 'desk' not in drop:
        rows.append(list_row('Desk setup', h09('S09-solo-round-done'), mi('circle-check', 'Round 2 complete'), counts_inline(11, 1, 8, cap), name_cls=nc, meta_cls=mc, clamp=cl, stack=big))
    return rows


def lists_group(rows, ios=False, label='Lists'):
    rad = 'rounded-control' if ios else 'rounded-group'
    return f'<ul class="divide-y overflow-hidden {rad} bg-card dark:border" aria-label="{label}">{"".join(rows)}</ul>'


def archived_entry(count=2, ios=False):
    return group([nav_row('Archived lists', href=h10('S10-archived'), icon_name='archive', value=str(count), action='archived', aria=f'Archived lists, {count}')], ios=ios)


def backup_indicator(web=False, action='back-up'):
    """Not signed in (A-81). Web (D-08): browsers can clear lists that aren't opened for a while, so the line
    says so and how to keep them; two short lines, the action stays "Back up"."""
    if web:
        return (f'<a href="S05-sign-in-prompt.html#S05-web-backup" class="mx-4 flex min-h-touch items-start gap-2 rounded-control px-1 py-1 text-body-sm text-muted-foreground" data-action="{action}">'
                f'{icon("cloud-off", "size-4 mt-0.5 shrink-0")}<span class="flex-1">Browsers can clear lists you haven\'t opened for a while.</span><span class="inline-flex min-h-10 shrink-0 items-start text-label text-primary">Back up</span></a>')
    text = 'Lists are on this phone only'
    return (f'<a href="S05-sign-in-prompt.html#S05-backup" class="mx-4 flex min-h-touch items-center gap-2 rounded-control px-1 text-body-sm text-muted-foreground" data-action="{action}">'
            f'{icon("cloud-off", "size-4 shrink-0")}<span class="flex-1">{text}</span><span class="text-label text-primary">Back up</span></a>')


def fab(collapsed=False, action=None, bottom='bottom-24', big=False):
    act = f' data-action="{action}"' if action else ''
    if collapsed:
        return f'<a href="{S11}" class="absolute {bottom} right-4 z-10 flex size-14 items-center justify-center rounded-tile bg-primary text-primary-foreground shadow-overlay" aria-label="New list"{act}>{icon("plus", "size-6")}</a>'
    t = 'text-title-3' if big else 'text-label-lg'
    h = 'min-h-16 py-3' if big else 'h-14'
    return f'<a href="{S11}" class="absolute {bottom} right-4 z-10 inline-flex {h} items-center gap-3 rounded-tile bg-primary pl-5 pr-6 {t} text-primary-foreground shadow-overlay"{act}>{icon("plus", "size-6")}New list</a>'


def search_btn():
    return icon_action('search', 'Search lists', h08('S08-search'), 'search')


def home(body, top='', overlay='', nav_badge=2, fab_html=None, title='large', pad='pb-28', translate=''):
    head = large_title('Lists', search_btn()) if title == 'large' else (title if title else '')
    f = fab() if fab_html is None else fab_html
    return f'''{head}
  {top}
  <div class="min-h-0 flex-1 overflow-hidden px-4 {pad} pt-2"><div class="space-y-4 {translate}">{body}</div></div>
  {f}
  {bottom_nav('lists', badge=nav_badge)}
  {overlay}'''


def home_default(action=None, new_conflicts=False, drop=(), archived=2, top='', overlay='', fab_action=None, fab_bottom='bottom-24'):
    body = lists_group(rows_lists('signed', new_conflicts=new_conflicts, drop=drop)) + archived_entry(archived)
    return home(body, top=top, overlay=overlay, nav_badge=3 if new_conflicts else 2, fab_html=fab(action=fab_action, bottom=fab_bottom))


def home_guest(web=False, top_extra='', resume_action=False, fab_action=None, overlay=''):
    body = lists_group(rows_lists('guest', resume_action=resume_action))
    return home(body, top=backup_indicator(web) + top_extra, nav_badge=0, fab_html=fab(action=fab_action), overlay=overlay)


def empty_state(ic, title, body, actions, extra='', title_cls='text-title-2', body_cls='text-body'):
    return f'''<div class="flex flex-col items-center px-6 text-center {extra}">
      {icon(ic, "size-8 text-muted-foreground")}
      <h2 class="mt-4 max-w-xs {title_cls}">{title}</h2>
      <p class="mt-2 max-w-xs {body_cls} text-muted-foreground">{body}</p>
      <div class="mt-6 w-full max-w-xs space-y-2">{actions}</div>
    </div>'''


def first_run(kind='android'):
    actions = (btn('Import a list', href=S11, action='import-list', size='md', icon_name='download')
               + btn('Try a sample list', 'ghost', href=h09('S09-sample'), action='try-sample', size='md'))
    es = empty_state('layers', 'No lists yet', 'Import a list or try a sample to see how sorting works.', actions)
    foot = f'''<p class="mt-8 max-w-xs text-center text-body-sm text-muted-foreground">Import from phone contacts, CSV, Excel, Google Sheets or plain text, or type items yourself.</p>
      <p class="mt-2 text-body-sm text-muted-foreground">Have an account? {link("Sign in", "S03-sign-in.html#S03-default", action="sign-in")}</p>'''
    inner = f'<div class="flex min-h-0 flex-1 flex-col items-center justify-center px-gutter pb-8">{es}{foot}</div>'
    if kind == 'ios':
        return f'''{ios_nav(large='Lists')}
  {inner}
  {ios_tab_bar('lists', badge=0)}'''
    return f'''{large_title('Lists')}
  {inner}
  {bottom_nav('lists', badge=0)}'''


def skeleton_rows(n=4):
    one = '<li class="space-y-2.5 px-4 py-4"><span class="block h-5 w-2/3 animate-pulse rounded-full bg-muted"></span><span class="block h-3.5 w-1/3 animate-pulse rounded-full bg-muted"></span><span class="block h-1.5 w-full animate-pulse rounded-full bg-muted"></span></li>'
    return f'<div role="status" aria-busy="true" aria-label="Loading lists"><ul class="divide-y overflow-hidden rounded-group bg-card dark:border" aria-hidden="true">{one * n}</ul></div>'


def search_bar(query, ios=False):
    clear = f'<button type="button" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Clear search">{icon("x")}</button>'
    return f'''<!-- Proposed component: SearchAppBar --><header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    <a href="{h08('S08-default')}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close search">{icon("arrow-left", "size-6")}</a>
    <div class="flex h-12 min-w-0 flex-1 items-center rounded-full bg-secondary pl-4">{icon("search", "size-5 shrink-0 text-muted-foreground")}<input type="search" value="{query}" aria-label="Search lists" class="h-12 min-w-0 flex-1 bg-transparent px-3 text-body outline-none">{clear}</div>
    <span class="w-2"></span>
  </header>'''


def hl(name, q):
    """Highlight the matched word start (semibold, foreground)."""
    i = name.lower().find(q.lower())
    if i < 0:
        return name
    return f'{name[:i]}<mark class="rounded-xs bg-primary-soft text-primary-soft-foreground">{name[i:i + len(q)]}</mark>{name[i + len(q):]}'


# ================================================================ S09 List overview
def ov_bar(menu=h10('S10-default'), share=None, back=h08('S08-default'), back_label='Back to lists', title=None, share_disabled=False, menu_label='List options'):
    sh = ''
    if share:
        href, label, act = share
        if share_disabled:
            sh = f'<button type="button" class="flex size-12 shrink-0 items-center justify-center rounded-full opacity-50" aria-label="{label}, needs a connection" disabled>{icon("user-plus", "size-6")}</button>'
        else:
            a = f' data-action="{act}"' if act else ''
            sh = f'<a href="{href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{label}"{a}>{icon("user-plus", "size-6")}</a>'
    mn = f'<a href="{menu}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{menu_label}" data-action="menu">{icon("ellipsis-vertical", "size-6")}</a>' if menu else ''
    t = f'<p class="min-w-0 flex-1 truncate px-1 text-title-3">{title}</p>' if title else '<span class="flex-1"></span>'
    bd = ' relative z-10 border-b bg-background' if title else ''
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1{bd}">
    <a href="{back}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{back_label}" data-action="back">{icon("arrow-left", "size-6")}</a>
    {t}{sh}{mn}
  </header>'''


def ov_ios_bar(back_text='Lists', back=h08('S08-default'), share=None, menu=h10('S10-ios-action-sheet')):
    sh = f'<a href="{share[0]}" class="flex size-12 items-center justify-center text-primary" aria-label="{share[1]}">{icon("share", "size-6")}</a>' if share else ''
    mn = f'<a href="{menu}" class="flex size-12 items-center justify-center text-primary" aria-label="List options">{icon("circle-ellipsis", "size-6")}</a>'
    return ios_nav('', back_text=back_text, href=back, trailing=sh + mn, action='back')


def ov_header(name, meta_items, extra='', size='text-title-1'):
    meta = f'<div class="mt-2 flex flex-wrap items-center gap-x-4 gap-y-2 text-body-sm text-muted-foreground">{"".join(meta_items)}</div>' if meta_items else ''
    return f'<div class="px-1"><h1 class="{size}">{name}</h1>{meta}{extra}</div>'


def members_link(text='You, Mert and Selin', href='S34-members.html#S34-default'):
    return f'<!-- Proposed component: MembersLink (AvatarStack + names) --><a href="{href}" class="-my-2 inline-flex min-h-touch items-center gap-2 text-body-sm text-muted-foreground">{stack(ring="ring-background")}<span class="text-foreground underline underline-offset-4">{text}</span></a>'


def ov_screen(bar, body, top='', overlay='', pad='pb-8', translate='', clip=''):
    pt = 'pt-4' if top else 'pt-1'
    return f'''{bar}
  {top}
  <div class="min-h-0 flex-1 overflow-hidden px-4 {pad} {pt} {clip}"><div class="space-y-6 {translate}">{body}</div></div>
  {overlay}'''


SRC_TRIP = [('file-spreadsheet', 'trip-ideas.csv', '30 items, imported Oct 8')]
SRC_PHOTOS = SRC_TRIP  # D-32: the photo clean-up sample became Trip ideas (A-130); old name kept for callers
SRC_DESK = [('keyboard', 'Manual entry', '20 items, typed in Oct 4')]
SRC_HIRING = [('file-spreadsheet', 'candidates-q4.csv', '12 items, imported Oct 8')]
SRC_SAMPLE = [('flask-conical', 'Sample items', '20 items, added with the sample')]
SRC_WED = [('contact', 'Contacts', '88 items, imported Sep 28'), ('file-spreadsheet', 'mert-family.csv', '12 items, added today')]
SRC_WED_NEW = [('contact', 'Contacts', '88 items, imported Sep 28'), ('file-spreadsheet', 'mert-family.csv', '12 items, added just now', True)]
SRC_APT = [('sheet', 'Flat hunt 2026', 'Google Sheets, Kadıköy and Beşiktaş tabs, 8 items, imported Jul 2')]


def sources_group(sources, add=True, add_desc='From any source', href=None):
    """Proposed component: SourceRow. One row per source (icon, label, count and date) + Add items."""
    rows = []
    for src in sources:
        ic, label, desc = src[:3]
        new = len(src) > 3 and src[3]
        badge = chip('New', 'primary') if new else ''
        rows.append(nav_row(label, href=href or h09('S09-source-details'), icon_name=ic, desc=desc, action='source', title_cls='text-body truncate',
                            trailing=badge + icon('chevron-right', 'size-5 shrink-0 text-muted-foreground'),
                            aria=f'{label}, {desc}' + (', new' if new else '')))
    if add:
        rows.append(f'<li><a href="S21-add-items.html#S21-default" class="flex min-h-14 items-center gap-4 px-4 py-3" data-action="add-items">{icon("plus", "size-5 shrink-0 text-primary")}<span class="min-w-0 flex-1"><span class="block text-body text-primary">Add items</span><span class="block text-body-sm text-muted-foreground">{add_desc}</span></span></a></li>')
    return '<!-- Proposed component: SourceRow -->' + group(rows, header='Sources')


ACCOUNT = 'deniz.yilmaz@example.com'
BACKUP_STATES = {
    # state: (lead icon, description, switch on, switch disabled, footer)
    'on': ('cloud-check', f'Backed up to {ACCOUNT}', True, False, None),
    'off': ('cloud-off', 'On this phone only', False, False, 'Lists on this phone only don\'t move to a new phone. Back them up first.'),
    'busy': ('loader-circle', 'Backing up…', True, True, None),
    'queued': ('cloud-upload', 'Backs up when you\'re online', True, False, None),
    'paused': ('cloud-alert', 'Backup paused. It continues when you\'re online.', True, False, None),
    'shared': ('cloud-check', f'Backed up to {ACCOUNT}', True, True, 'Shared lists are always backed up.'),
    'offline-on': ('cloud-check', f'Backed up to {ACCOUNT}', True, True, 'Turning backup off needs a connection.'),
}


_BK_UID = [0]


def backup_group(state='on', web=False, big=False):
    """Proposed component: BackupSwitchRow (A-132). Its own "Backup" group under Sources, for a signed-in Owner.
    The whole row is the switch (min-h-16; like the S14/S15 switch rows): role="switch", the state line and the
    group footer (disabled reason) are its accessible description. Solo lists: the switch works; shared lists
    and offline: disabled with the reason (A-134). Prototype: on → turn-off confirmation, off → backing up."""
    ic, desc, on, dis, foot = BACKUP_STATES[state]
    if web:
        desc = desc.replace('On this phone only', 'On this browser only')
        foot = None if state == 'off' else foot
    _BK_UID[0] += 1
    uid = f'bk{_BK_UID[0]}'
    spin = ' animate-spin' if state == 'busy' else ''
    live = ' role="status"' if state in ('busy', 'queued', 'paused') else ''
    t = 'text-title-3 font-normal' if big else 'text-body'
    d = 'text-body-lg' if big else 'text-body-sm'
    # visual switch only (the row carries the role)
    sw = switch(on, 'Back up this list', dis)
    sw = re.sub(r' role="switch" aria-checked="[a-z]+" aria-label="[^"]*"', ' aria-hidden="true"', sw).replace(' aria-disabled="true"', '')
    if big:
        sw = sw.replace('h-8 w-13', 'h-10 w-16').replace('size-6 rounded-full bg-primary-foreground', 'size-8 rounded-full bg-primary-foreground').replace('size-5 rounded-full bg-muted-foreground', 'size-7 rounded-full bg-muted-foreground')
    tcol = ' text-muted-foreground' if dis and state != 'busy' else ''
    described = f'{uid}-d' + (f' {uid}-f' if foot else '')
    inner = (f'{icon(ic, ("size-6" if big else "size-5") + " shrink-0 text-muted-foreground" + spin)}'
             f'<span class="min-w-0 flex-1"><span class="block {t}{tcol}">Back up this list</span><span id="{uid}-d" class="block break-words {d} text-muted-foreground"{live}>{desc}</span></span>{sw}')
    attrs = f'role="switch" aria-checked="{"true" if on else "false"}" aria-label="Back up this list" aria-describedby="{described}"'
    cls = 'flex min-h-16 w-full items-center gap-4 px-4 py-3 text-left'
    tgt = None if (dis or web) else {'on': h10('S10-backup-off'), 'off': h09('S09-backing-up')}.get(state)
    if tgt:
        row = f'<li><a href="{tgt}" {attrs} class="{cls}" data-action="toggle-backup">{inner}</a></li>'
    elif dis:
        row = f'<li><div {attrs} aria-disabled="true" tabindex="0" class="{cls}">{inner}</div></li>'
    else:
        row = f'<li><button type="button" {attrs} class="{cls}" data-action="toggle-backup">{inner}</button></li>'
    hcls = 'text-title-3 font-normal' if big else 'text-label'
    fcls = 'text-body-lg' if big else 'text-body-sm'
    f = f'<p id="{uid}-f" class="px-1 pt-2 {fcls} text-muted-foreground">{foot}</p>' if foot else ''
    return (f'<!-- Proposed component: BackupSwitchRow --><section><h2 class="px-1 pb-2 {hcls} text-muted-foreground">Backup</h2>'
            f'<ul class="divide-y overflow-hidden rounded-group bg-card dark:border">{row}</ul>{f}</section>')


def rows_solo(results=h09('S09-default'), results_desc=None, rounds='1', template='Photo', export='S39-export.html#S39-default',
              new_round=True, start_round_desc='Choose items and card order', add=True, export_action=None, results_href='S28-results.html#S28-default',
              template_row=True, extra=None, sources=None, backup=None, backup_web=False):
    rows = [nav_row('Results', href=results_href, icon_name='list-checks', desc=results_desc, action='results')]
    if new_round:
        rows.append(nav_row('Start a new round', href='S24-start-round.html#S24-default', icon_name='list-restart', desc=start_round_desc, action='new-round'))
    rows.append(nav_row('Rounds', href='S30-round-history.html#S30-default', icon_name='history', value=rounds, action='rounds', aria=f'Rounds, {rounds}'))
    if template_row:
        rows.append(nav_row('Card template', href='S22-template-library.html#S22-default', icon_name='layout-template', value=template, action='card-template', aria=f'Card template, {template}'))
    rows.append(nav_row('Export', href=export, icon_name='file-down', desc='CSV, Excel, Google Sheets or a text summary', action=export_action))
    if extra:
        rows += extra
    src = sources_group(sources or [], add=add) if (sources or add) else ''
    bk = backup_group(backup, backup_web) if backup else ''
    return group(rows) + src + bk


def progress_photos(btn_html=None):
    b = btn_html if btn_html is not None else btn('Continue sorting', href='S25-sorting.html#S25-photo', action='continue-sorting', size='md', icon_name='play', extra='mt-4')
    return card(card_head('Round 1', 'Started Oct 8', 'pg-h') + decided(12, 30) + decision_chips(6, 1, 5)
                + note_line('Only you sort this list, so your decisions are final.') + b, label='pg-h')


def share_card(href, action=None, web=False):
    a = f' data-action="{action}"' if action else ''
    where = 'devices'
    return card(f'''<div class="flex gap-3">{icon("users", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1">
      <h2 class="text-label">Decide together</h2>
      <p class="mt-0.5 text-body-sm text-muted-foreground">Share this list so others can sort it on their own {where}. You'll see where you agree.</p>
      <a href="{href}" class="mt-3 inline-flex h-12 items-center gap-2 rounded-control border border-input bg-card px-4 text-label-lg"{a}>{icon("user-plus")}Share list</a>
    </div></div>''')


def guest_backup_line(web=False):
    text = 'On this browser only' if web else 'On this phone only'
    return (f'<a href="S05-sign-in-prompt.html#S05-backup" class="-my-2 inline-flex min-h-touch items-center gap-1.5" data-action="back-up">{icon("cloud-off", "size-4 shrink-0")}{text}'
            f'<span class="ml-1 text-label text-primary">Back up</span></a>')


TRIP_META = [mi('file-spreadsheet', '30 items from trip-ideas.csv'), mi('user', 'Solo list')]


def ov_solo_default(clip='', backup='on', translate='', bar_title=None, top='', overlay='', name='Trip ideas', menu=h10('S10-default'), meta=None, share_disabled=False):
    """Trip ideas (A-130): solo, signed in, backed up; Round 1 at 12 / 30."""
    body = (ov_header(name, meta or TRIP_META)
            + progress_photos()
            + rows_solo(template='Photo', results_desc='12 decided so far', sources=SRC_TRIP, backup=backup))
    return ov_screen(ov_bar(menu=menu, share=('S31-invite.html#S31-default', 'Share list', 'share'), title=bar_title, share_disabled=share_disabled), body, clip=clip, translate=translate, top=top, overlay=overlay)


def ov_round_done(bar_menu=h10('S10-default')):
    c = card(card_head('Round 1 complete', 'Oct 4', 'rd-h', 'circle-check')
             + '<p class="mt-3 text-title-3 tabular-nums">20 / 20 decided</p><div class="mt-2">' + split_bar(9, 6, 5, 20) + '</div>'
             + decision_chips(9, 6, 5)
             + note_line('Only you sort this list, so your decisions are final.')
             + btn('Re-sort Maybe (6)', href='S24-start-round.html#S24-maybe', action='resort-maybe', size='md', icon_name='circle-help', extra='mt-4'),
             label='rd-h')
    body = (ov_header('Desk setup', [mi('package', '20 items'), mi('user', 'Solo list')]) + c
            + rows_solo(template='Product', results_desc='5 accepted, 9 rejected, 6 maybe', export_action='export', sources=SRC_DESK, backup='on'))
    return ov_screen(ov_bar(menu=bar_menu, share=('S31-invite.html#S31-default', 'Share list', None)), body)


HIRING_META = [mi('file-spreadsheet', '12 items from candidates-q4.csv'), mi('user', 'Solo list'), mi('cloud-off', 'On this phone only')]
D08_LINE = 'Browsers can clear lists you haven\'t opened for a while. Back it up to keep it.'


def d08_note(extra='mt-3'):
    """D-08 / A-137: the browser-storage line under the S09 header meta on the web."""
    return note_line(D08_LINE, 'info', extra)


def ov_new_list(name='Frontend hiring, Q4', meta=None, n=12, template='Candidate, compact', sort='S25-sorting.html#S25-candidate', sources=SRC_HIRING,
                backup='off', translate='', bar_title=None, top='', overlay='', clip='', share=None, header_extra='', backup_web=False, share_disabled=False):
    """Never sorted. Frontend hiring, Q4 is on this phone only in the signed-in sample world (A-139): header label,
    Backup switch off, and Share opens the "Back up this list to share it" sheet (A-133)."""
    meta = meta or HIRING_META
    c = card(card_head('Not sorted yet', f'{n} items', 'nl-h', 'circle-dashed')
             + '<p class="mt-2 text-body text-muted-foreground">Every item is ready. Start sorting to make your first decisions; you can stop at any time and continue later.</p>'
             + btn('Start sorting', href=sort, action='start-sorting', size='md', icon_name='play', extra='mt-4'), label='nl-h')
    body = (ov_header(name, meta, header_extra) + c
            + rows_solo(template=template, results_desc='No decisions yet', rounds='None yet', new_round=False, sources=sources, backup=backup, backup_web=backup_web))
    sh = share or ((h10('S10-share-backup'), 'Share list', 'share') if backup in ('off', 'queued') else ((h10('S10-share-backing-up'), 'Share list', 'share') if backup == 'busy' else ('S31-invite.html#S31-default', 'Share list', None)))
    return ov_screen(ov_bar(share=sh, title=bar_title, share_disabled=share_disabled), body, translate=translate, top=top, overlay=overlay, clip=clip)


def ov_empty():
    es = card(empty_state('list-plus', 'No items yet', 'Add items from contacts, a file, Google Sheets or text, or type them yourself. Then start sorting.',
                          btn('Add items', href='S21-add-items.html#S21-default', action='add-items', size='md', icon_name='plus'), extra='py-6', title_cls='text-title-3'))
    rows = group([nav_row('Card template', href='S22-template-library.html#S22-default', icon_name='layout-template', value='Generic', aria='Card template, Generic')]) + backup_group('on')
    body = ov_header('Gift ideas for Mum', [mi('layers', '0 items'), mi('user', 'Solo list')]) + es + rows
    return ov_screen(ov_bar(share=('S31-invite.html#S31-default', 'Share list', None)), body)


def ov_sample():
    banner = alert_info('This is a sample list', '20 sample items to practice on. Sort, change decisions, try Results. Delete it from the menu when you\'re done; nothing else changes.', icon_name='flask-conical')
    c = card(card_head('Not sorted yet', '20 items', 'sm-h', 'circle-dashed')
             + '<p class="mt-2 text-body text-muted-foreground">Swipe right to accept, left to reject, up for maybe. Or use the buttons.</p>'
             + btn('Start sorting', href='S25-sorting.html#S25-product', action='start-sorting', size='md', icon_name='play', extra='mt-4'), label='sm-h')
    body = (ov_header('Desk setup (sample)', [mi('package', '20 items'), mi('cloud-off', 'On this phone only')]) + banner + c
            + rows_solo(template='Product', results_desc='No decisions yet', rounds='None yet', new_round=False, add=False, sources=SRC_SAMPLE))
    return ov_screen(ov_bar(menu=h10('S10-default'), back=h08('S08-sample')), body)


def ov_guest_wedding(web=False, share_action='share'):
    c = card(card_head('Round 1', 'Started Sep 28', 'gw-h') + decided(76, 100) + decision_chips(17, 11, 48)
             + note_line('Only you sort this list, so your decisions are final.')
             + btn('Continue sorting', href='S25-sorting.html#S25-default', action='continue-sorting', size='md', icon_name='play', extra='mt-4'), label='gw-h')
    body = (ov_header('Wedding guests', [mi('users', '100 items'), mi('user', 'Solo list'), guest_backup_line(web)], d08_note() if web else '') + c
            + share_card('S05-sign-in-prompt.html#S05-share', action=share_action)
            + rows_solo(template='Person', results_desc='76 decided so far', sources=SRC_WED))
    return ov_screen(ov_bar(share=('S05-sign-in-prompt.html#S05-share', 'Share list', None)), body)


# ---------------------------------------------------------------- shared
def my_progress(d, t, rej, may, acc, button, role_note=None, hid='mp-h'):
    n = note_line(role_note) if role_note else ''
    return card(card_head('My progress', 'Round 1, shared', hid) + decided(d, t) + decision_chips(rej, may, acc) + n + button, label=hid)


def status_legend(rows_extra=True):
    items = [('check-check', 'Agreed', 'Everyone chose the same', 32, 'bg-foreground'), ('git-compare-arrows', 'Conflict', 'Members chose differently', 15, 'bg-foreground/50'),
             ('clock', 'Pending', 'Not everyone has decided', 53, 'border border-input bg-muted')]
    out = ''.join(f'<li class="flex items-center gap-3 py-2"><span class="size-3 shrink-0 rounded-full {sw}" aria-hidden="true"></span>{icon(ic, "size-5 shrink-0")}<span class="min-w-0 flex-1"><span class="block text-body">{t}</span><span class="block text-body-sm text-muted-foreground">{d}</span></span><span class="text-title-3 tabular-nums">{n}</span></li>'
                  for ic, t, d, n, sw in items)
    return f'<!-- Proposed component: ListStatusLegend --><ul class="mt-2 divide-y">{out}</ul>'


def list_status_card(button, hid='ls-h', compact=False, right='All 3 members'):
    sw = lambda c: f'<span class="size-2.5 shrink-0 rounded-xs {c}" aria-hidden="true"></span>'
    leg = (f'<p class="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-body-sm"><span class="inline-flex items-center gap-1.5">{sw("bg-foreground")}{icon("check-check", "size-4")}<span class="tabular-nums">32</span> agreed</span>'
           f'<span class="inline-flex items-center gap-1.5">{sw("bg-foreground/50")}{icon("git-compare-arrows", "size-4")}<span class="tabular-nums">15</span> conflicts</span><span class="inline-flex items-center gap-1.5 text-muted-foreground">{sw("border border-input bg-muted")}{icon("clock", "size-4")}<span class="tabular-nums">53</span> pending</span></p>'
           if compact else status_legend())
    return card(card_head('List status', right, hid) + f'<div class="mt-3">{status_bar(32, 15, 53)}</div>' + leg + button, label=hid)


def offline_row(title, ic, desc='Needs a connection'):
    """A navigation row that needs a connection, offline (A-186): title muted, reason at full contrast."""
    return (f'<li><div class="flex min-h-14 items-center gap-4 px-4 py-3" aria-disabled="true">{icon(ic, "size-5 shrink-0 text-muted-foreground")}'
            f'<span class="min-w-0 flex-1"><span class="block text-body text-muted-foreground">{title}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span></div></li>')


def together_group(rule_href='S35-conflict-rule.html#S35-default', rule_desc='Decision Maker decides, Mert', members_desc='3 members, you\'re the Owner', readonly_rule=False, offline=False):
    if offline and not readonly_rule:
        rule = offline_row('Conflict rule', 'git-compare-arrows', f'{rule_desc}. Changing it needs a connection')
    elif readonly_rule:
        rule = f'<li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon("git-compare-arrows", "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">Conflict rule</span><span class="block text-body-sm text-muted-foreground">{rule_desc}</span></span></li>'
    else:
        rule = nav_row('Conflict rule', href=rule_href, icon_name='git-compare-arrows', desc=rule_desc, action='conflict-rule')
    mem = nav_row('Members', href='S34-members.html#S34-default', icon_name='users', desc=members_desc, action='members',
                  trailing=stack() + icon('chevron-right', 'size-5 shrink-0 text-muted-foreground'))
    return group([rule, mem], header='Deciding together')


def activity_preview(events=None):
    ev = events or [
        (f'<span class="flex size-8 shrink-0 items-center justify-center rounded-full bg-conflict text-conflict-foreground">{icon("git-compare-arrows", "size-4")}</span>', '15 new conflicts', 'Oct 3'),
        (avatar(None, 'SY', 'size-8', 'text-caption'), 'Selin joined the list', 'Oct 2'),
        (avatar(IMG + 'people/u-deniz.svg', size='size-8'), 'You started Round 1 with 88 items', 'Sep 28'),
    ]
    rows = ''.join(f'<li class="flex items-center gap-3 px-4 py-3">{a}<span class="min-w-0 flex-1"><span class="block text-body">{t}</span><span class="block text-body-sm text-muted-foreground">{w}</span></span></li>' for a, t, w in ev)
    return f'<section aria-labelledby="ap-h">{heading_row("Recent activity", "See all", "S38-activity.html#S38-default", "ap-h")}<ul class="mt-1 divide-y overflow-hidden rounded-group bg-card dark:border">{rows}</ul></section>'


ADDED_EVENTS = [
    (avatar(IMG + 'people/u-deniz.svg', size='size-8'), 'You added 12 items from mert-family.csv', 'Just now'),
    (f'<span class="flex size-8 shrink-0 items-center justify-center rounded-full bg-conflict text-conflict-foreground">{icon("git-compare-arrows", "size-4")}</span>', '15 new conflicts', 'Oct 3'),
    (avatar(None, 'SY', 'size-8', 'text-caption'), 'Selin joined the list', 'Oct 2'),
]


def rows_shared(owner=True, sources=None, offline=False):
    if offline:
        extra_round = [offline_row('Start a new round', 'list-restart')] if owner else []
    else:
        extra_round = [nav_row('Start a new round', href='S24-start-round.html#S24-default', icon_name='list-restart', desc='Starts for all 3 members', action='new-round')] if owner else []
    rows = [nav_row('Results', href='S28-results.html#S28-shared', icon_name='list-checks', desc='Final decisions and my decisions', action='results')] + extra_round + [
        nav_row('Rounds', href='S30-round-history.html#S30-default', icon_name='history', value='1', aria='Rounds, 1'),
        nav_row('Card template', href='S22-template-library.html#S22-default', icon_name='layout-template', value='Person', aria='Card template, Person'),
        nav_row('Export', href='S39-export.html#S39-shared', icon_name='file-down', desc='Includes each member\'s decision', action='export')]
    foot = None if owner else 'Deniz, the Owner, starts new rounds for everyone.'
    return group(rows, footer=foot) + sources_group(sources or SRC_WED, add_desc='New items join Round 1 for everyone')


def shared_header(who='You, Mert and Selin', role=('Owner', 'crown', 'secondary'), extra=''):
    r = chip(role[0], role[2], role[1])
    return ov_header('Wedding guests', [members_link(who), mi('users', '100 items'), r], extra)


def saved_notice(n=4):
    """S40 SyncNotice, offline state (A-115): under the S09 header meta when changes are waiting."""
    return (f'<p class="mt-3 inline-flex items-center gap-1.5 text-body-sm text-muted-foreground" role="status">{icon("cloud-off", "size-4 shrink-0")}'
            f'Saved on this phone<span class="sr-only">, {n} changes not synced yet</span></p>')


def ov_shared_owner(translate='', bar_title=None, top='', share_disabled=False, list_status_btn=None, status_right='All 3 members', added=False, overlay='', clip='', backup='shared', offline=False):
    lsb = list_status_btn if list_status_btn is not None else btn('Review conflicts', 'outline', href='S36-conflicts.html#S36-default', action='review-conflicts', size='md', icon_name='git-compare-arrows', extra='mt-3')
    body = (shared_header(extra=saved_notice() if offline else '')
            + my_progress(76, 100, 17, 11, 48, btn('Continue sorting', href='S25-sorting.html#S25-shared', action='continue-sorting', size='md', icon_name='play', extra='mt-4'))
            + list_status_card(lsb, right=status_right)
            + together_group(offline=offline)
            + activity_preview(ADDED_EVENTS if added else None)
            + rows_shared(sources=SRC_WED_NEW if added else SRC_WED, offline=offline)
            + (backup_group(backup) if backup else ''))
    return ov_screen(ov_bar(menu=h10('S10-shared-owner-menu'), share=('S31-invite.html#S31-default', 'Invite', 'invite'), title=bar_title, share_disabled=share_disabled),
                     body, top=top, translate=translate, overlay=overlay, clip=clip)


def ov_shared_dm():
    callout = '<!-- Proposed component: DecisionMakerCallout -->' + card(f'''<div class="flex gap-3"><span class="flex size-10 shrink-0 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon("gavel")}</span>
      <div class="min-w-0 flex-1"><h2 id="dm-h" class="text-title-3">15 conflicts need your decision</h2>
      <p class="mt-1 text-body-sm text-muted-foreground">You're the Decision Maker, so your choice becomes the final decision.</p></div></div>
      {btn("Resolve conflicts", href="S36-conflicts.html#S36-default", action="review-conflicts", size="md", icon_name="git-compare-arrows", extra="mt-4")}
      <a href="S37-bulk-resolve.html#S37-confirm" class="mt-2 flex min-h-touch items-center justify-center rounded-control text-label-lg" data-action="resolve-all">Resolve all with my decisions</a>
      <p class="text-center text-body-sm text-muted-foreground">12 have your decision. 3 stay open until you decide them.</p>''', label='dm-h')
    body = (ov_header('Wedding guests', [members_link('Deniz, Selin and you'), mi('users', '100 items'), chip('Decision Maker', 'primary', 'gavel')])
            + callout
            + my_progress(85, 100, 21, 14, 50, btn('Continue sorting', 'outline', href='S25-sorting.html#S25-shared', size='md', icon_name='play', extra='mt-4'), hid='mpd-h')
            + list_status_card('', hid='lsd-h', compact=True)
            + together_group(readonly_rule=True, rule_desc='Decision Maker decides. You resolve conflicts.', members_desc='3 members')
            + rows_shared(owner=False))
    return ov_screen(ov_bar(menu=h10('S10-collaborator-menu'), share=('S31-invite.html#S31-collaborator', 'Invite', None)), body)


def ov_shared_collab(translate='', bar_title=None):
    body = (ov_header('Wedding guests', [members_link('Deniz, Mert and you'), mi('users', '100 items'), chip('Collaborator', 'secondary', 'user')])
            + my_progress(43, 100, 8, 10, 25, btn('Continue sorting', href='S25-sorting.html#S25-shared', action='continue-sorting', size='md', icon_name='play', extra='mt-4'), hid='mpc-h')
            + list_status_card(btn('View conflicts', 'outline', href='S36-conflicts.html#S36-default', size='md', icon_name='git-compare-arrows', extra='mt-3'), hid='lsc-h', compact=True)
            + together_group(readonly_rule=True, rule_desc='Decision Maker decides. Mert resolves conflicts; Deniz sets the rule.', members_desc='3 members')
            + rows_shared(owner=False)
            + group([button_row('Leave list', icon_name='log-out', destructive=True, href=h10('S10-leave'), action='leave')]))
    return ov_screen(ov_bar(menu=h10('S10-collaborator-menu'), share=('S31-invite.html#S31-collaborator', 'Invite', None), title=bar_title), body, translate=translate)


def ov_shared_waiting():
    waits = ''.join(f'<li class="flex items-center gap-3 py-2.5">{a}<span class="min-w-0 flex-1"><span class="block text-body">{n}</span><span class="mt-1.5 flex items-center gap-3">{pbar(d, 100, "h-1", f"{n}: {d} of 100 decided")}<span class="shrink-0 text-caption tabular-nums text-muted-foreground">{d} / 100</span></span></span></li>'
                    for a, n, d in ((avatar(IMG + 'people/u-mert.svg', size='size-8'), 'Mert', 85), (avatar(None, 'SY', 'size-8', 'text-caption'), 'Selin', 43)))
    c = card(card_head('You decided every item', 'Round 1, shared', 'wt-h', 'circle-check')
             + '<p class="mt-3 text-title-3 tabular-nums">100 / 100 decided</p><div class="mt-2">' + split_bar(18, 15, 67, 100) + '</div>'
             + decision_chips(18, 15, 67)
             + '<p class="mt-4 text-body-sm text-muted-foreground">The list status settles as the others finish. Conflicts can be resolved now.</p>'
             + f'<ul class="mt-1 divide-y" aria-label="Still sorting">{waits}</ul>'
             + btn('See results', href='S28-results.html#S28-shared', action='results', size='md', icon_name='list-checks', extra='mt-3'), label='wt-h')
    body = (shared_header() + c
            + list_status_card(btn('Review conflicts', 'outline', href='S36-conflicts.html#S36-default', size='md', icon_name='git-compare-arrows', extra='mt-3'), hid='lsw-h', compact=True)
            + together_group())
    return ov_screen(ov_bar(menu=h10('S10-shared-owner-menu'), share=('S31-invite.html#S31-default', 'Invite', None)), body)


def ov_archived():
    banner = card(f'''<div class="flex gap-3">{icon("archive", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1">
      <h2 id="ar-h" class="text-label">Archived Jul 21</h2>
      <p class="mt-0.5 text-body-sm text-muted-foreground">This list is read-only. Restore it to sort, add items or change decisions.</p></div></div>
      {btn("Restore list", href=h10("S10-restored"), action="restore", size="md", icon_name="archive-restore", extra="mt-4")}''', label='ar-h')
    c = card(card_head('Round 1 complete', 'Jul 21', 'arc-h', 'circle-check')
             + '<p class="mt-3 text-title-3 tabular-nums">8 / 8 decided</p><div class="mt-2">' + split_bar(4, 1, 3, 8) + '</div>' + decision_chips(4, 1, 3), label='arc-h')
    rows = group([nav_row('Results', href='S28-results.html#S28-default', icon_name='list-checks', desc='Read-only'),
                  nav_row('Rounds', href='S30-round-history.html#S30-default', icon_name='history', value='1', aria='Rounds, 1'),
                  nav_row('Export', href='S39-export.html#S39-default', icon_name='file-down', desc='CSV, Excel, Google Sheets or a text summary')]) + sources_group(SRC_APT, add=False)
    body = ov_header('Apartment viewings', [mi('sheet', '8 items from Flat hunt 2026'), chip('Archived', 'secondary', 'archive')]) + banner + c + rows
    return ov_screen(ov_bar(menu=h10('S10-archived-menu'), back=h10('S10-archived'), back_label='Back to archived lists'), body)


def ov_loading():
    sk = lambda w, h='h-4': f'<span class="block {h} {w} animate-pulse rounded-full bg-muted"></span>'
    body = f'''<div class="space-y-3 px-1">{sk("w-3/4", "h-8")}{sk("w-1/2")}</div>
    <div class="space-y-3 rounded-group bg-card p-4 dark:border">{sk("w-1/4")}{sk("w-1/3", "h-6")}{sk("w-full", "h-1.5")}<div class="flex gap-2">{sk("w-24", "h-8")}{sk("w-20", "h-8")}{sk("w-24", "h-8")}</div><span class="block h-12 w-full animate-pulse rounded-control bg-muted"></span></div>
    <div class="space-y-5 rounded-group bg-card p-4 dark:border">{sk("w-1/2")}{sk("w-2/3")}{sk("w-1/2")}{sk("w-3/5")}</div>'''
    return ov_screen(ov_bar(menu=None), f'<div role="status" aria-busy="true" aria-label="Loading list" class="space-y-6">{body}</div>')


def ov_unavailable():
    es = empty_state('folder-x', 'This list was deleted', 'Deniz deleted “Wedding guests” for everyone today. Its items, decisions and notes were deleted with it.',
                     btn('Back to lists', href=h08('S08-default'), action='back-to-lists', size='md'))
    return f'''{ov_bar(menu=None)}
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center pb-24">{es}</div>'''


# ================================================================ S10 helpers
def dlg(did, title, actions, body=None, extra='', z='z-40', stacked=False, big=False, icon_html=''):
    b = f'<p id="{did}-d" class="mt-2 {"text-body-lg" if big else "text-body"} text-muted-foreground">{body}</p>' if body else ''
    desc = f' aria-describedby="{did}-d"' if body else ''
    acts = f'<div class="mt-6 flex flex-col gap-2">{actions}</div>' if stacked else f'<div class="mt-6 flex flex-wrap justify-end gap-2">{actions}</div>'
    t = 'text-title-2' if big else 'text-title-3'
    return ov(f'''{scrim('z-30')}
  <div class="absolute inset-x-6 top-1/2 {z} -translate-y-1/2 rounded-dialog bg-popover p-6 shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="{did}-t"{desc}>
    {icon_html}<h2 id="{did}-t" class="{t}">{title}</h2>
    {b}
    {extra}
    {acts}
  </div>''')


def dbtn(label, kind='ghost', href=None, action=None, disabled=False, full=False):
    cls = {'ghost': '', 'destructive': 'bg-destructive text-destructive-foreground', 'primary': 'bg-primary text-primary-foreground'}[kind]
    w = ' w-full justify-center' if full else ''
    act = f' data-action="{action}"' if action else ''
    base = f'inline-flex min-h-12 items-center rounded-control px-4 py-2 text-label-lg {cls}{w}'
    if disabled:
        return f'<button type="button" class="{base} opacity-50" disabled>{label}</button>'
    return f'<a href="{href or "#"}" class="{base}"{act}>{label}</a>'


def name_input(fid, value, count, state='default', error=None, label='List name'):
    b = {'default': 'border border-primary ring-2 ring-ring/30', 'error': 'border-2 border-destructive'}[state]
    err = ''
    aria = f' aria-describedby="{fid}-c"'
    over = 'text-destructive' if count > 80 else 'text-muted-foreground'
    if error:
        err = f'<p id="{fid}-e" class="flex min-w-0 items-start gap-1.5 text-body-sm text-destructive">{icon("circle-alert", "size-4 mt-0.5 shrink-0")}<span>{error}</span></p>'
        aria = f' aria-invalid="true" aria-describedby="{fid}-e {fid}-c"'
    return f'''<div class="mt-4"><label for="{fid}" class="text-label">{label}</label>
      <input id="{fid}" type="text" value="{esc(value)}" class="mt-1.5 h-12 w-full rounded-control bg-card px-3.5 text-body {b}"{aria}>
      <div class="mt-1.5 flex items-start justify-between gap-3">{err or "<span></span>"}<p id="{fid}-c" class="shrink-0 text-body-sm tabular-nums {over}">{count} / 80</p></div></div>'''


def radio_opts(name, options):
    out = []
    for title, desc, checked in options:
        dot = ('<span class="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary" aria-hidden="true"><span class="size-3 rounded-full bg-primary"></span></span>'
               if checked else '<span class="mt-0.5 size-6 shrink-0 rounded-full border-2 border-input" aria-hidden="true"></span>')
        out.append(f'<button type="button" role="radio" aria-checked="{"true" if checked else "false"}" class="flex min-h-14 w-full items-start gap-3 py-2.5 text-left">{dot}<span class="min-w-0 flex-1"><span class="block text-body">{title}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span></button>')
    return f'<div role="radiogroup" aria-label="{name}" class="mt-3">{"".join(out)}</div>'


def menu_sheet_rows(items):
    out = []
    for text, ic, href, kind, *rest in items:
        col = ' text-destructive' if kind == 'destructive' else ''
        icol = '' if kind == 'destructive' else ' text-muted-foreground'
        act = f' data-action="{rest[0]}"' if rest else ''
        out.append(f'<li><a href="{href}" class="-mx-gutter flex min-h-14 items-center gap-4 px-gutter text-body{col}"{act}>{icon(ic, "size-5 shrink-0" + icol)}{text}</a></li>')
    return f'<ul class="mt-1">{"".join(out)}</ul>'


def ios_action_sheet(title, msg, items, cancel_href):
    rows = ''.join(f'<a href="{href}" class="flex min-h-14 items-center justify-center border-t px-4 text-title-3 font-normal {"text-destructive" if kind == "destructive" else "text-primary"}">{text}</a>' for text, href, kind in items)
    m = f'<p class="mt-0.5 text-body-sm text-muted-foreground">{msg}</p>' if msg else ''
    return ov(f'''{scrim('z-30')}
  <div class="absolute inset-x-2 bottom-10 z-40 space-y-2" role="alertdialog" aria-modal="true" aria-labelledby="ias-t">
    <div class="overflow-hidden rounded-dialog bg-popover shadow-dialog">
      <div class="px-6 pb-3 pt-4 text-center"><p id="ias-t" class="text-body-sm font-semibold text-muted-foreground">{title}</p>{m}</div>
      {rows}
    </div>
    <a href="{cancel_href}" class="flex h-14 items-center justify-center rounded-dialog bg-popover text-title-3 text-primary shadow-dialog">Cancel</a>
  </div>''')


def archived_row(name, href, meta, counts, opt_href, idn, big=False):
    return f'''<li class="flex items-center"><a href="{href}" class="flex min-w-0 flex-1 flex-col gap-1 py-4 pl-4 pr-2">
        <span class="truncate {"text-title-2" if big else "text-title-3"}">{name}</span>
        <span class="text-body-sm text-muted-foreground">{meta}</span>
        <span class="mt-1">{counts}</span></a>
      <a href="{opt_href}" class="mr-1 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Options for {name}" data-action="options-{idn}">{icon("ellipsis-vertical")}</a></li>'''


ARCHIVED_ROWS = lambda: [
    archived_row('Apartment viewings', h09('S09-archived'), 'Archived Jul 21, 8 items', counts_inline(4, 1, 3), h10('S10-archived-menu'), 'apartments'),
    archived_row('Book club picks', h09('S09-archived'), 'Archived May 2, 12 items', counts_inline(6, 2, 4), h10('S10-archived-menu'), 'books'),
]


def archived_screen(rows=None, top='', overlay='', empty=False):
    bar = appbar('Archived lists', href=h08('S08-default'), label='Back to lists', action='back')
    if empty:
        es = empty_state('archive', 'No archived lists', 'Archive a list to put it away without deleting it. It waits here, read-only, until you restore it.',
                         btn('Back to lists', 'secondary', href=h08('S08-default'), size='md'))
        return f'''{bar}{top}
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center pb-24">{es}</div>{overlay}'''
    r = rows if rows is not None else ARCHIVED_ROWS()
    return f'''{bar}{top}
  <div class="min-h-0 flex-1 overflow-hidden px-4 pb-8 pt-1">
    <p class="px-1 pb-4 text-body-sm text-muted-foreground">Archived lists are read-only and hidden from Lists. Restore a list to sort or change it.</p>
    <ul class="divide-y overflow-hidden rounded-group bg-card dark:border" aria-label="Archived lists">{"".join(r)}</ul>
  </div>{overlay}'''


# ================================================================================================
# S08 HOME
# ================================================================================================
P = Page('S08', 'Home (Lists)', 'The Lists tab: every list with its progress, resume sorting in one tap, start a new list. First run offers a sample list; without an account a quiet indicator says lists live on this phone only.', 'S08-home.md')

P.section('First run and sample', 'No lists yet: one sentence, Import a list (main action) and Try a sample list. The sample is a copy of the 20 Desk setup products, so the first impression is neutral, not wedding-specific.')
P.frame('S08-first-run', 'First run: no lists, not signed in', phone(first_run()))
sample_row = list_row('Desk setup (sample)', h09('S09-sample'), mi('circle-dashed', 'Not sorted yet, 20 items') + chip('Sample', 'secondary', 'flask-conical'))
P.frame('S08-sample', 'Sample list added', phone(home(lists_group([sample_row])
                                                         + '<p class="px-1 text-body-sm text-muted-foreground">The sample is for practice. Delete it from its menu whenever you like. Import your own list with New list.</p>',
                                                         nav_badge=0, fab_html=fab())))

P.section('Lists', 'Lists are ordered by latest activity. Each ListRow shows the name, a status line and progress: a bar with "decided / total" for a round in progress, decision counts for a finished round. Rounds in progress have a Resume button that opens sorting directly. Shared lists show open conflicts. Signed in, a list kept on this phone only carries a muted "On this phone only" label in its status line (A-137); backed-up lists show nothing. The extended FAB starts a new list (Android); Archived lists sit at the end.')
P.frame('S08-default', 'Default: signed in as Deniz', phone(home_default(fab_action='new-list')))
P.frame('S08-guest', 'Not signed in: lists on this phone only', phone(home_guest(resume_action=True)))
P.frame('S08-new-conflicts', 'Shared list with new conflicts', phone(home_default(new_conflicts=True)))

long_rows = [
    list_row('Kadıköy and Beşiktaş apartment viewings before the move in January 2027', h09('S09-default'), mi('circle-dot', 'Round 1 in progress'), bar_below(3, 8), resume('S25-sorting.html#S25-default', 'Kadıköy and Beşiktaş apartment viewings'), clamp='line-clamp-2'),
    list_row('Konferans konuşma önerileri, program komitesi toplantısından önce gözden geçirilecek', h09('S09-shared'), mi('users', 'Shared with 4') + chip('2 conflicts', 'conflict', 'git-compare-arrows'), bar_below(18, 45), clamp='line-clamp-2'),
    list_row('Gift ideas for the whole family: birthdays, New Year and the summer trip to Ayvalık', h09('S09-new-list'), mi('circle-dashed', 'Not sorted yet, 34 items'), clamp='line-clamp-2'),
    list_row('Wedding guests', h09('S09-shared'), mi('users', 'Shared with 2') + chip('15 conflicts', 'conflict', 'git-compare-arrows'), bar_below(76, 100), resume('S25-sorting.html#S25-shared', 'Wedding guests')),
]
P.frame('S08-long-names', 'Very long list names (2 lines, then ellipsis)', phone(home(lists_group(long_rows) + archived_entry())))

many = [('Wedding guests', 'users', 'Shared with 2', (76, 100)), ('Frontend hiring, Q4', 'circle-dashed', 'Not sorted yet, 12 items', None),
        ('Trip ideas', 'circle-dot', 'Round 1 in progress', (12, 30)), ('Desk setup', 'circle-check', 'Round 2 complete', 'c'),
        ('Restaurants to try in İzmir', 'circle-dot', 'Round 1 in progress', (9, 27)), ('Podcast episode ideas', 'circle-check', 'Round 1 complete', 'c2'),
        ('Kitchen renovation quotes', 'users', 'Shared with 1', (4, 6)), ('Baby name shortlist', 'users', 'Shared with 1', (40, 120)),
        ('Summer reading', 'circle-dashed', 'Not sorted yet, 18 items', None), ('Board games to buy', 'circle-dot', 'Round 2 in progress', (61, 212))]
many_rows = []
for n, ic, m, p in many:
    below = '' if p is None else (counts_inline(11, 1, 8) if p == 'c' else (counts_inline(9, 4, 12) if p == 'c2' else bar_below(*p)))
    many_rows.append(list_row(n, h09('S09-default'), mi(ic, m) + (mi('cloud-off', 'On this phone only') if n == 'Frontend hiring, Q4' else ''), below, pad='py-3.5'))
P.frame('S08-many-lists', 'Many lists, scrolled: title collapses, FAB shrinks', phone(home(lists_group(many_rows[1:]),
                                                                                            fab_html=fab(collapsed=True), translate='-translate-y-16',
                                                                                            title=f'''<header class="relative z-10 flex h-app-bar shrink-0 items-center gap-1 border-b bg-background px-1"><h1 class="min-w-0 flex-1 truncate px-4 text-title-3">Lists</h1>{search_btn()}</header>''')))

P.section('Search', 'The search button opens a search field over the large title. Results filter live by any word in the list name (case- and accent-insensitive, so "izmir" finds "İzmir"), active lists first, archived lists in their own group.')
srch_active = list_row(hl('Trip ideas', 'tr'), h09('S09-default'), mi('circle-dot', 'Round 1 in progress'), bar_below(12, 30))
P.frame('S08-search', 'Search: results', phone(f'''{search_bar("tr")}
  <div class="min-h-0 flex-1 overflow-hidden px-4 pb-8 pt-2"><div class="space-y-5">
    <p class="px-1 text-body-sm text-muted-foreground" role="status">1 list matches</p>
    <section aria-label="Lists">{lists_group([srch_active], label="Matching lists")}</section>
  </div></div>
  {bottom_nav("lists", badge=2)}'''))
srch_arch = list_row(hl('Book club picks', 'b'), h09('S09-archived'), chip('Archived', 'secondary', 'archive') + mi('circle-check', 'Round 1 complete'))
P.frame('S08-search-archived', 'Search: an archived match', phone(f'''{search_bar("b")}
  <div class="min-h-0 flex-1 overflow-hidden px-4 pb-8 pt-2"><div class="space-y-5">
    <p class="px-1 text-body-sm text-muted-foreground" role="status">1 list matches</p>
    <section aria-labelledby="sa-h"><h2 id="sa-h" class="px-1 pb-2 text-label text-muted-foreground">Archived</h2>{lists_group([srch_arch], label="Matching archived lists")}</section>
  </div></div>
  {bottom_nav("lists", badge=2)}'''))
P.frame('S08-search-empty', 'Search: no results', phone(f'''{search_bar("budget")}
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center pb-24" role="status">{empty_state("search-x", "No lists match “budget”", "Check the spelling, or search for another word in the list name.", btn("Clear search", "secondary", href=h08("S08-default"), size="md"), title_cls="text-title-3")}</div>
  {bottom_nav("lists", badge=2)}'''))

P.section('States', 'Lists are stored on the device first, so Home opens instantly from local data. The skeleton only shows on a cold start of a large account. Offline, everything stays usable; changes sync later with a quiet notice under the title.')
P.frame('S08-loading', 'Loading (skeleton)', phone(home(skeleton_rows(), fab_html='')))
P.frame('S08-offline', 'Offline', phone(home_default(top=offline_banner("You're offline. Changes are saved on this phone."))))
sync = f'<p class="mx-4 flex min-h-touch items-center gap-2 px-1 text-body-sm text-muted-foreground" role="status">{icon("refresh-cw", "size-4 shrink-0 animate-spin")}Syncing 12 decisions…</p>'
P.frame('S08-syncing', 'Sync notice: back online, syncing', phone(home_default(top=sync)))
sync_err = (f'<div class="mx-4 mb-1 flex items-center gap-2 rounded-control border border-destructive/40 bg-card py-1 pl-3 pr-1" role="alert">{icon("circle-alert", "size-4 shrink-0 text-destructive")}'
            f'<span class="min-w-0 flex-1 text-body-sm">Couldn\'t sync 12 decisions. They\'re safe on this phone.</span>'
            f'<button type="button" class="inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label text-primary">Try again</button></div>')
P.frame('S08-sync-error', 'Sync failed: changes kept locally', phone(home_default(top=sync_err)))
err = empty_state('triangle-alert', 'Your lists couldn\'t be opened', 'They\'re still saved on this phone. Try again, or restart SwipeSort. If it keeps happening, contact us from Settings › Help.',
                  btn('Try again', 'secondary', href=h08('S08-default'), size='md'))
P.frame('S08-error', 'Error: local data couldn\'t be read', phone(f'''{large_title("Lists")}
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center pb-16" role="alert">{err}</div>
  {bottom_nav("lists", badge=0)}'''))

P.section('Accessibility', 'At 200% font size names wrap to 2 lines, meta wraps, the progress fraction moves under the bar and the FAB keeps its label. Rows grow; nothing is cut sideways.')
lt_rows = rows_lists('signed', big=True)
P.frame('S08-large-text', 'Large text (200%)', phone(f'''<header class="shrink-0"><div class="flex h-app-bar items-center justify-end gap-1 px-1">{search_btn()}</div><h1 class="px-gutter pb-2 text-display">Lists</h1></header>
  <div class="min-h-0 flex-1 overflow-hidden px-4 pb-28 pt-2">{lists_group(lt_rows)}</div>
  {fab(collapsed=True)}
  {bottom_nav("lists", badge=2).replace("text-caption", "text-label-lg")}'''))

P.section('iOS and web', 'iOS: large title with a search field below it, "+" in the navigation bar instead of a FAB, inset grouped rows, standard tab bar. Web: same layout as Android; without an account the indicator says browsers can clear lists that aren\'t opened for a while (D-08). Desktop shows the phone column centered; a list kept on Deniz\'s phone only (Frontend hiring, Q4) is not in the browser.')
ios_rows = rows_lists('signed')
ios_plus = f'<a href="{S11}" class="flex size-12 items-center justify-center text-primary" aria-label="New list">{icon("plus", "size-6")}</a>'
ios_search = f'<div class="px-4 pb-3"><label class="flex h-11 items-center gap-2 rounded-control bg-secondary px-3 text-body text-muted-foreground">{icon("search", "size-5 shrink-0")}<input type="search" placeholder="Search" aria-label="Search lists" class="h-11 min-w-0 flex-1 bg-transparent text-foreground placeholder:text-muted-foreground"></label></div>'
P.frame('S08-ios', 'iOS: large title, + in the bar, tab bar', phone(f'''{ios_nav(large='Lists', trailing=ios_plus)}
  {ios_search}
  <div class="min-h-0 flex-1 space-y-6 overflow-hidden px-4 pb-6">{lists_group(ios_rows, ios=True)}{archived_entry(ios=True)}</div>
  {ios_tab_bar('lists', badge=2)}''', kind='ios'))
P.frame('S08-ios-first-run', 'iOS: first run', phone(first_run('ios'), kind='ios'))
P.frame('S08-web', 'Web, mobile browser: not signed in', phone(home_guest(web=True), kind='web'))
desk_new = f'<a href="{S11}" class="mr-2 inline-flex h-12 items-center gap-2 rounded-control bg-primary px-4 text-label-lg text-primary-foreground">{icon("plus")}New list</a>'
P.frame('S08-web-desktop', 'Web, desktop browser: New list in the bar', desktop(home(lists_group(rows_lists('signed', drop=('hiring',))) + archived_entry(), fab_html='', title=f'<header class="shrink-0"><div class="flex h-app-bar items-center justify-end gap-1 px-1">{search_btn()}{desk_new}</div><h1 class="px-gutter pb-2 text-title-1">Lists</h1></header>'), 'swipesort.app/lists'))
P.write(F08)


# ================================================================================================
# S09 LIST OVERVIEW
# ================================================================================================
P = Page('S09', 'List overview', 'One list: where sorting stands, the next action, and everything you can do with the list. Solo lists show my progress (my decisions are final). Shared lists add list progress (Agreed, Pending, Conflict), the conflict rule, members and activity, and change by role.', 'S09-list-overview.md')

P.section('Solo lists', 'Solo rule (DM-01): only you sort the list, so your decision is the final decision. The progress card holds the one main action: Continue sorting, Start sorting, or Re-sort Maybe after a finished round.')
P.frame('S09-default', 'Default: solo list in progress (Trip ideas)', phone(ov_solo_default()))
P.frame('S09-solo-round-done', 'Solo, Round 1 complete (Desk setup)', phone(ov_round_done()))
P.frame('S09-new-list', 'New list, never sorted, on this phone only (Frontend hiring, Q4)', phone(ov_new_list()))
P.frame('S09-empty', 'List with 0 items', phone(ov_empty()))
P.frame('S09-sample', 'Sample list (from first run)', phone(ov_sample()))
P.frame('S09-guest-wedding', 'Not signed in: Wedding guests before sharing', phone(ov_guest_wedding()))

P.section('Shared lists', 'Every member decides every item (DM-02). My progress is mine; list status is everyone\'s (DM-14). What changes by role: the Owner starts rounds and sets the conflict rule; the Decision Maker resolves conflicts; Collaborators sort, see conflicts and can leave.')
P.frame('S09-shared', 'Shared, Owner view (Deniz)', phone(ov_shared_owner()))
P.frame('S09-shared-scrolled', 'Shared, Owner view scrolled', phone(ov_shared_owner(translate='-translate-y-[47%]', bar_title='Wedding guests')))
P.frame('S09-shared-added', 'Items added (from S21): new source and Undo', phone(ov_shared_owner(translate='-translate-y-[64%]', bar_title='Wedding guests', added=True, clip='mb-20',
        overlay=snackbar('Added 12 items', 'Undo', action_href=h09('S09-shared'), data_action='undo'))))
src_sheet = ov(sheet('sd', f'''<div class="flex items-center gap-3 pb-1 pt-1"><span class="flex size-10 shrink-0 items-center justify-center rounded-control bg-secondary text-muted-foreground">{icon("file-spreadsheet")}</span>
      <div class="min-w-0 flex-1"><h2 id="sd-t" class="truncate text-title-3">mert-family.csv</h2><p class="text-body-sm text-muted-foreground">CSV file</p></div><a href="{h09('S09-shared')}" class="-mr-3 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</a></div>
    <dl class="mt-3 divide-y text-body">
      <div class="flex min-h-12 items-center justify-between gap-4 py-2"><dt class="text-muted-foreground">Items</dt><dd class="tabular-nums">12</dd></div>
      <div class="flex min-h-12 items-center justify-between gap-4 py-2"><dt class="text-muted-foreground">Added</dt><dd>Today by you</dd></div>
      <div class="flex min-h-12 items-center justify-between gap-4 py-2"><dt class="text-muted-foreground">Fields</dt><dd class="min-w-0 text-right">Name, Phone, Email, Side, Relationship</dd></div>
    </dl>
    {alert_info("Your original is never changed", "Edits, notes and decisions stay in SwipeSort. Export when you want a file with them.", icon_name="shield-check", extra="mt-3")}''', title=None, pad='pb-12'))
P.frame('S09-source-details', 'Source details sheet', phone(inert(ov_shared_owner(translate='-translate-y-[64%]', bar_title='Wedding guests')) + src_sheet))
P.frame('S09-shared-decision-maker', 'Shared, Decision Maker view (Mert)', phone(ov_shared_dm()))
P.frame('S09-shared-collaborator', 'Shared, Collaborator view (Selin)', phone(ov_shared_collab()))
P.frame('S09-shared-collaborator-scrolled', 'Shared, Collaborator view scrolled', phone(ov_shared_collab(translate='-translate-y-[47%]', bar_title='Wedding guests')))
P.frame('S09-shared-waiting', 'Shared, I decided everything; others still sorting', phone(ov_shared_waiting()))

P.section('Backup (signed in)', 'A signed-in Owner of a solo list chooses per list whether it is backed up (A-132): the Backup group under Sources holds one switch. On: the list is in the account. Off: it stays on this phone only; Home and the header say so with a muted label (A-137). Turning it on needs no confirmation; turning it off asks first (S10). Shared lists are always backed up, so the Owner sees the switch disabled with the reason. Not shown without an account, on the sample, to members who don\'t own the list, or on archived lists.')
P.frame('S09-device-only', 'On this phone only: the Backup switch is off (Frontend hiring, Q4, scrolled)', phone(ov_new_list(translate='-translate-y-[30%]', bar_title='Frontend hiring, Q4')))
P.frame('S09-backing-up', 'Switch turned on: backing up', phone(ov_new_list(backup='busy', translate='-translate-y-[30%]', bar_title='Frontend hiring, Q4')))
P.frame('S09-backed-up', 'Backed up: snackbar', phone(ov_new_list(meta=HIRING_META[:2], backup='on', translate='-translate-y-[30%]', bar_title='Frontend hiring, Q4', clip='mb-20',
        overlay=snackbar('“Frontend hiring, Q4” is backed up'))))
P.frame('S09-backup-queued', 'Switch turned on while offline: backs up later', phone(ov_new_list(backup='queued', translate='-translate-y-[30%]', bar_title='Frontend hiring, Q4',
        top=offline_banner("You're offline. Changes are saved on this phone. Backing up and sharing need a connection."), share_disabled=True)))
P.frame('S09-shared-backup', 'Shared list, Owner: always backed up (switch disabled)', phone(ov_shared_owner(translate='-translate-y-[66%]', bar_title='Wedding guests')))
P.frame('S09-web-device-only', 'Web, signed in: a list on this browser only', phone(ov_new_list(meta=HIRING_META[:2] + [mi('cloud-off', 'On this browser only')], header_extra=d08_note(), backup_web=True), kind='web'))

P.section('Archived and states', 'Archived lists open read-only with Restore as the main action. Loading shows a skeleton only when the list isn\'t on the device yet (opened from a link). Offline, sorting works; inviting needs a connection.')
P.frame('S09-archived', 'Archived list: read-only (Apartment viewings)', phone(ov_archived()))
P.frame('S09-loading', 'Loading', phone(ov_loading()))
P.frame('S09-offline', 'Offline (shared list)', phone(ov_shared_owner(top=offline_banner("You're offline. Decisions are saved on this phone. Inviting needs a connection."), share_disabled=True, status_right='As of 9:24', offline=True)))
P.frame('S09-unavailable', 'List deleted by the Owner', phone(ov_unavailable()))

P.section('Accessibility', 'Large text: the title wraps, counts stack, buttons grow, rows keep their full labels.')
lt = (ov_header('Trip ideas', TRIP_META, size='text-display').replace('text-body-sm', 'text-body-lg')
      + card(card_head('Round 1', '', 'lt-h').replace('text-label', 'text-title-3') + decided(12, 30, size='text-title-2')
             + f'<ul class="mt-3 space-y-2 text-body-lg">' + ''.join(f'<li class="flex items-center gap-2 text-{k}-soft-foreground">{icon(ic, "size-6")}<span class="tabular-nums">{n}</span> {lab}</li>' for (k, ic, lab), n in zip(DECISIONS, (6, 1, 5))) + '</ul>'
             + btn('Continue sorting', href='S25-sorting.html#S25-photo', size='lg', icon_name='play', extra='mt-4 min-h-16 h-auto py-3 text-title-3'), label='lt-h'))
lt_rows = group([nav_row(t, href=h, icon_name=i, desc=d, title_cls='text-title-3 font-normal').replace('text-body-sm', 'text-body-lg') for t, h, i, d in (
    ('Results', 'S28-results.html#S28-default', 'list-checks', '12 decided so far'), ('Start a new round', 'S24-start-round.html#S24-default', 'list-restart', 'Choose items and card order'),
    ('Rounds', 'S30-round-history.html#S30-default', 'history', '1 round'), ('Card template', 'S22-template-library.html#S22-default', 'layout-template', 'Photo'),
    ('Export', 'S39-export.html#S39-default', 'file-down', 'CSV, Excel, Google Sheets or a text summary'))])
P.frame('S09-large-text', 'Large text (200%)', phone(ov_screen(ov_bar(share=('S31-invite.html#S31-default', 'Share list', None)), lt + lt_rows)))
lt_hiring_rows = group([nav_row(t, href=h, icon_name=ic, desc=d, title_cls='text-title-3 font-normal').replace('text-body-sm', 'text-body-lg') for t, h, ic, d in (
    ('Card template', 'S22-template-library.html#S22-default', 'layout-template', 'Candidate, compact'), ('Export', 'S39-export.html#S39-default', 'file-down', 'CSV, Excel, Google Sheets or a text summary'))])
lt_hiring = (lt_hiring_rows
             + sources_group(SRC_HIRING).replace('text-body-sm', 'text-body-lg').replace('text-body truncate', 'text-title-3 font-normal truncate').replace('block text-body text-primary', 'block text-title-3 font-normal text-primary').replace('pb-2 text-label', 'pb-2 text-title-3 font-normal')
             + backup_group('off', big=True))
P.frame('S09-backup-large-text', 'Large text (200%): scrolled to the Backup switch (on this phone only)', phone(ov_screen(ov_bar(share=(h10('S10-share-backup'), 'Share list', 'share'), title='Frontend hiring, Q4'), lt_hiring, translate='-translate-y-24')))

P.section('iOS and web', 'iOS: back chevron with "Lists", Share and a "…" menu (opens an action sheet), inset grouped rows, edge-swipe back. Web: same as Android; a list that is only in this browser says "On this browser only" and that browsers can clear lists that aren\'t opened for a while (D-08). Desktop: the phone column, centered.')
ios_body = (ov_header('Trip ideas', TRIP_META) + progress_photos()
            + rows_solo(template='Photo', results_desc='12 decided so far', sources=SRC_TRIP, backup='on').replace('rounded-group', 'rounded-control'))
P.frame('S09-ios', 'iOS: solo list', phone(ov_screen(ov_ios_bar(share=('S31-invite.html#S31-default', 'Share list')), ios_body), kind='ios'))
ios_shared = (shared_header()
              + my_progress(76, 100, 17, 11, 48, btn('Continue sorting', href='S25-sorting.html#S25-shared', size='md', icon_name='play', extra='mt-4'), hid='mpi-h')
              + list_status_card(btn('Review conflicts', 'outline', href='S36-conflicts.html#S36-default', size='md', icon_name='git-compare-arrows', extra='mt-3'), hid='lsi-h', compact=True)
              + together_group())
P.frame('S09-ios-shared', 'iOS: shared list (Owner)', phone(ov_screen(ov_ios_bar(share=('S31-invite.html#S31-default', 'Invite'), menu=h10('S10-ios-action-sheet')), ios_shared.replace('rounded-group', 'rounded-control')), kind='ios'))
P.frame('S09-web', 'Web, mobile browser: not signed in', phone(ov_guest_wedding(web=True, share_action=None), kind='web'))
P.frame('S09-web-desktop', 'Web, desktop browser: shared list', desktop(ov_shared_owner(), 'swipesort.app/l/7Hq2xK'))
P.write(F09)


# ================================================================================================
# S10 LIST MANAGEMENT
# ================================================================================================
P = Page('S10', 'List management', 'Rename, duplicate, archive, delete and leave, from the list\'s overflow menu (S09) or a long press on a row (S08); plus the Archived lists screen. Who sees what depends on the role: the Owner manages the list; members can duplicate and leave.', 'S10-list-management.md')

BG_PHOTOS = inert(ov_solo_default())
BG_SHARED = inert(ov_shared_owner())
BG_COLLAB = inert(ov_shared_collab())
BG_DM = inert(ov_shared_dm())

SOLO_MENU = [('Rename', 'pencil', h10('S10-rename'), 'n', None, 'rename'), ('Duplicate', 'copy', h10('S10-duplicate'), 'n', None, 'duplicate'),
             ('Archive', 'archive', h10('S10-archived-snackbar'), 'n', None, 'archive'), 'sep', ('Delete list', 'trash-2', h10('S10-delete'), 'destructive', None, 'delete')]


def dropdown_items(items, top='top-2', label='List options'):
    out = []
    for it in items:
        if it == 'sep':
            out.append('<div class="my-1.5 h-px bg-border" role="separator"></div>')
            continue
        text, ic, href, kind = it[:4]
        reason = it[4] if len(it) > 4 else None
        action = it[5] if len(it) > 5 else None
        if reason:
            out.append(f'<button type="button" role="menuitem" class="flex min-h-14 w-full items-center gap-3 px-4 py-2 text-left" disabled>{icon(ic, "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body text-muted-foreground">{text}</span><span class="block text-body-sm text-muted-foreground">{reason}</span></span></button>')
            continue
        col = ' text-destructive' if kind == 'destructive' else ''
        icol = '' if kind == 'destructive' else ' text-muted-foreground'
        act = f' data-action="{action}"' if action else ''
        out.append(f'<a href="{href}" role="menuitem" class="flex h-12 w-full items-center gap-3 px-4 text-body{col}"{act}>{icon(ic, "size-5 shrink-0" + icol)}{text}</a>')
    return f'<div class="absolute right-2 {top} z-30 w-64 overflow-hidden rounded-control bg-popover py-1.5 shadow-overlay" role="menu" aria-label="{label}">{"".join(out)}</div>'


OWNER_MENU = [('Rename', 'pencil', h10('S10-rename'), 'n', None, 'rename'), ('Duplicate', 'copy', h10('S10-duplicate-shared'), 'n', None, 'duplicate'),
              ('Archive', 'archive', h10('S10-archive-shared'), 'n', None, 'archive'), 'sep',
              ('Leave list', 'log-out', h10('S10-leave-owner-blocked'), 'destructive', None, 'leave'), ('Delete list', 'trash-2', h10('S10-delete-shared'), 'destructive', None, 'delete')]
COLLAB_MENU = [('Duplicate', 'copy', h10('S10-duplicate-shared'), 'n', None, 'duplicate'), 'sep', ('Leave list', 'log-out', h10('S10-leave'), 'destructive', None, 'leave')]
OFFLINE_MENU = [('Rename', 'pencil', h10('S10-rename'), 'n', None, 'rename'), ('Duplicate', 'copy', h10('S10-duplicate-shared'), 'n', None, 'duplicate'),
                ('Archive', 'archive', '#', 'n', 'Needs a connection'), 'sep',
                ('Leave list', 'log-out', '#', 'destructive', 'Needs a connection'), ('Delete list', 'trash-2', '#', 'destructive', 'Needs a connection')]

P.section('Actions menu', 'The overflow menu on S09 (Android DropdownMenu, anchored to the button). Items depend on the role: Owner of a solo or shared list: Rename, Duplicate, Archive, Leave (shared only), Delete list. Collaborator and Decision Maker: Duplicate, Leave list. A long press on a Home row opens the same actions as a bottom sheet. iOS uses an action sheet.')
P.frame('S10-default', 'Menu: solo list (Owner)', phone(BG_PHOTOS + dropdown_items(SOLO_MENU)))
P.frame('S10-shared-owner-menu', 'Menu: shared list, Owner', phone(BG_SHARED + dropdown_items(OWNER_MENU)))
P.frame('S10-collaborator-menu', 'Menu: shared list, Collaborator or Decision Maker', phone(BG_COLLAB + dropdown_items(COLLAB_MENU)))
row_sheet = ov(sheet('rs', f'''<div class="flex items-center gap-3 pb-2 pt-1"><div class="min-w-0 flex-1"><h2 id="rs-t" class="truncate text-title-3">Wedding guests</h2><p class="text-body-sm tabular-nums text-muted-foreground">76 / 100 decided, Round 1</p></div></div>
    {menu_sheet_rows([("Resume sorting", "play", "S25-sorting.html#S25-default", "n"), ("Share list", "user-plus", "S05-sign-in-prompt.html#S05-share", "n", "share"),
                      ("Rename", "pencil", h10("S10-rename"), "n"), ("Duplicate", "copy", h10("S10-duplicate"), "n"), ("Archive", "archive", h10("S10-archived-snackbar"), "n"),
                      ("Delete list", "trash-2", h10("S10-delete"), "destructive")])}''', pad='pb-12'))
P.frame('S10-row-sheet', 'Long press on a Home row (not signed in)', phone(inert(home_guest()) + row_sheet))
P.frame('S10-ios-action-sheet', 'iOS: action sheet', phone(inert(ov_screen(ov_ios_bar(share=('S31-invite.html#S31-default', 'Share list')), ios_body)) + ios_action_sheet(
    'Trip ideas', None, [('Rename', h10('S10-ios-rename'), 'n'), ('Duplicate', h10('S10-duplicate'), 'n'), ('Archive', h10('S10-archived-snackbar'), 'n'), ('Delete list', 'S40-global-patterns.html#S40-ios-delete-list', 'destructive')],
    h09('S09-ios')), kind='ios'))

P.section('Rename', 'A dialog with the name selected. Names are 1 to 80 characters; Save stays disabled while the name is empty or too long, and the error says how to fix it. Duplicate names are allowed (lists have IDs).')
rn_actions = lambda ok=True: dbtn('Cancel', href=h09('S09-default')) + dbtn('Save', 'primary', href=h10('S10-renamed'), action='save', disabled=not ok)
P.frame('S10-rename', 'Rename dialog', phone(BG_PHOTOS + dlg('rn', 'Rename list', rn_actions(), extra=name_input('rn-i', 'Trip ideas', 10))))
P.frame('S10-rename-empty', 'Rename: empty name', phone(BG_PHOTOS + dlg('rne', 'Rename list', rn_actions(False), extra=name_input('rne-i', '', 0, 'error', 'Enter a name for the list.'))))
too_long = 'Trip ideas: Lisbon, Cappadocia, the Black Sea coast and every other place we talked about'
P.frame('S10-rename-too-long', 'Rename: too long', phone(BG_PHOTOS + dlg('rnl', 'Rename list', rn_actions(False), extra=name_input('rnl-i', too_long, len(too_long), 'error', 'Use 80 characters or fewer.'))))
renamed = inert(ov_solo_default(clip='mb-20').replace('Trip ideas', 'Trip ideas 2027'))
P.frame('S10-renamed', 'Renamed: snackbar', phone(renamed + snackbar('List renamed')))
ios_alert = ov(f'''{scrim('z-30')}
  <div class="absolute inset-x-10 top-1/2 z-40 -translate-y-1/2 overflow-hidden rounded-dialog bg-popover text-center shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="ira-t">
    <div class="px-4 pb-4 pt-5"><h2 id="ira-t" class="text-body font-semibold">Rename list</h2><p class="mt-1 text-body-sm text-muted-foreground">1 to 80 characters</p>
      <input type="text" value="Trip ideas" aria-label="List name" class="mt-3 h-11 w-full rounded-xs border border-input bg-card px-2 text-body-sm"></div>
    <div class="grid grid-cols-2 border-t"><a href="{h09('S09-ios')}" class="flex h-12 items-center justify-center border-r text-body text-primary">Cancel</a><a href="{h10('S10-renamed')}" class="flex h-12 items-center justify-center text-body font-semibold text-primary">Save</a></div>
  </div>''')
P.frame('S10-ios-rename', 'iOS: rename alert', phone(inert(ov_screen(ov_ios_bar(share=('S31-invite.html#S31-default', 'Share list')), ios_body)) + ios_alert, kind='ios'))

P.section('Duplicate', 'Duplicate makes a new list from the same items. Choose a fresh start (items only) or keep my decisions and notes. A shared list always duplicates into a new solo list owned by me; other members, their decisions and their notes stay in the shared list. The copy opens right away.')
dup_opts = radio_opts('What to copy', [('Items only', 'A fresh start: no decisions, notes or rounds. Edits to fields are kept.', True),
                                        ('Items with decisions and notes', 'Keeps your decisions from the latest round, your notes and your edits.', False)])
dup_actions = dbtn('Cancel', href=h09('S09-default')) + dbtn('Duplicate', 'primary', href=h10('S10-duplicated'), action='confirm-duplicate')
P.frame('S10-duplicate', 'Duplicate: options', phone(BG_PHOTOS + dlg('dp', 'Duplicate “Trip ideas”', dup_actions,
                                                                     extra=name_input('dp-i', 'Trip ideas (copy)', 17, label='Name of the copy') + dup_opts)))
dup_shared_opts = radio_opts('What to copy', [('Items only', 'A fresh start: no decisions, notes or rounds.', False),
                                               ('Items with my decisions and notes', 'Your 76 decisions from Round 1 and your notes. Other members\' decisions and notes aren\'t copied.', True)])
dup_shared_note = f'<p class="mt-3 flex items-start gap-2 rounded-control bg-muted p-3 text-body-sm">{icon("user", "size-4 mt-0.5 shrink-0")}<span>The copy is a new solo list that only you can see. Mert and Selin aren\'t added.</span></p>'
P.frame('S10-duplicate-shared', 'Duplicate a shared list: becomes a solo list', phone(BG_SHARED + dlg('dps', 'Duplicate “Wedding guests”', dbtn('Cancel', href=h09('S09-shared')) + dbtn('Duplicate', 'primary', href=h10('S10-duplicated')),
                                                                                       extra=name_input('dps-i', 'Wedding guests (copy)', 21, label='Name of the copy') + dup_shared_note + dup_shared_opts)))
copy_view = ov_new_list('Trip ideas (copy)', [mi('layers', '30 items'), mi('user', 'Solo list')], 30, 'Photo', 'S25-sorting.html#S25-photo', [('copy', 'Copied from Trip ideas', '30 items, today')], backup='on')
P.frame('S10-duplicated', 'Duplicated: snackbar with Open', phone(inert(ov_solo_default(clip='mb-20')) + snackbar('Duplicated as “Trip ideas (copy)”', 'Open', action_href=h10('S10-duplicate-opened'), data_action='open-copy')))
P.frame('S10-duplicate-opened', 'The copy, opened from the snackbar', phone(copy_view))

P.section('Archive', 'Archive hides a list from Lists without deleting anything. A solo list archives at once with Undo. Archiving a shared list affects every member, so the Owner confirms; members keep read-only access.')
P.frame('S10-archived-snackbar', 'Archived: back on Home with Undo', phone(inert(home_default(drop=('photos',), archived=3, fab_bottom='bottom-40')) + snackbar('List archived', 'Undo', bottom='bottom-24', action_href=h08('S08-default'), data_action='undo')))
P.frame('S10-archive-shared', 'Archive a shared list: confirm', phone(BG_SHARED + dlg('as', 'Archive “Wedding guests” for everyone?',
                                                                                      dbtn('Cancel', href=h09('S09-shared')) + dbtn('Archive list', 'primary', href=h10('S10-archived-snackbar'), action='confirm-archive'),
                                                                                      body='Mert and Selin can still open it, but nobody can sort, add items or change decisions until you restore it. Nothing is deleted.')))

P.section('Delete', 'Delete is Owner only and always confirms. The dialog names the list, says exactly what goes and what stays safe (sources are never touched). After deleting, Home shows "List deleted" with Undo for 6 seconds; the deletion is committed when the snackbar closes. Deleting a shared list deletes it for every member, with stronger copy and a specific button.')
P.frame('S10-delete', 'Delete a solo list', phone(BG_PHOTOS + dlg('dl', 'Delete “Trip ideas”?',
                                                                  dbtn('Cancel', href=h09('S09-default')) + dbtn('Delete list', 'destructive', href=h10('S10-deleted-snackbar'), action='confirm-delete'),
                                                                  body='30 items, Round 1 and your decisions will be deleted from your account and this phone. trip-ideas.csv isn\'t changed.')))
ds_warn = f'<p class="mt-3 text-body-sm text-muted-foreground">To stop taking part without deleting it for others, <a href="S34-members.html#S34-default" class="text-primary underline underline-offset-4">make someone else the Owner</a> and leave.</p>'
ds_icon = f'<span class="mb-4 flex size-12 items-center justify-center rounded-full bg-secondary text-destructive">{icon("triangle-alert", "size-6")}</span>'
P.frame('S10-delete-shared', 'Delete a shared list: deletes for all members', phone(BG_SHARED + dlg('dls', 'Delete “Wedding guests” for everyone?',
                                                                                                    dbtn('Cancel', href=h09('S09-shared')) + dbtn('Delete for everyone', 'destructive', href=h10('S10-deleted-snackbar'), action='confirm-delete'),
                                                                                                    body='Mert and Selin lose access. All 100 items, every member\'s decisions and notes, and Round 1 are deleted for all 3 members. Your contacts and mert-family.csv aren\'t changed.',
                                                                                                    extra=ds_warn)))
P.frame('S10-deleted-snackbar', 'Deleted: back on Home with Undo', phone(inert(home_default(drop=('photos',), fab_bottom='bottom-40')) + snackbar('List deleted', 'Undo', bottom='bottom-24', action_href=h08('S08-default'), data_action='undo')))

P.section('Leave', 'Members (Collaborator, Decision Maker) can leave a shared list. Their decisions stay and still count, so other members\' results don\'t shift unexpectedly; items they haven\'t decided stop waiting for them; their private notes are deleted. The Owner can\'t leave until someone else is the Owner.')
P.frame('S10-leave', 'Leave: Collaborator (Selin)', phone(BG_COLLAB + dlg('lv', 'Leave “Wedding guests”?',
                                                                         dbtn('Cancel', href=h09('S09-shared-collaborator')) + dbtn('Leave list', 'destructive', href=h10('S10-left-snackbar'), action='confirm-leave'),
                                                                         body='You won\'t see this list anymore. Your 43 decisions stay and still count toward the list status. Items you haven\'t decided stop waiting for you, and your private notes are deleted. To come back, ask Deniz for a new invite.')))
P.frame('S10-leave-decision-maker', 'Leave: Decision Maker (Mert)', phone(BG_DM + dlg('lvd', 'Leave “Wedding guests”?',
                                                                                     dbtn('Cancel', href=h09('S09-shared-decision-maker')) + dbtn('Leave list', 'destructive', href=h10('S10-left-snackbar')),
                                                                                     body='You won\'t see this list anymore. Your 85 decisions stay and still count toward the list status. You\'re the Decision Maker, so nobody will have this role until Deniz chooses someone. The 15 open conflicts stay open.')))
P.frame('S10-leave-owner-blocked', 'Leave: Owner must choose a new Owner first', phone(BG_SHARED + dlg('lvo', 'Choose a new Owner first',
                                                                                                    dbtn('Cancel', href=h09('S09-shared')) + dbtn('Choose new Owner', 'primary', href='S34-members.html#S34-default', action='choose-owner'),
                                                                                                    body='“Wedding guests” needs an Owner. Make another member the Owner, then you can leave. To remove the list for everyone, delete it instead.')))
left_home = f'''{large_title('Lists')}
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center px-gutter pb-16">{empty_state('layers', 'No lists yet', 'Import a list to start sorting, or join one when someone shares it with you.', btn('Import a list', href=S11, size='md', icon_name='download'))}</div>
  {fab()}
  {bottom_nav('lists', badge=0)}'''.replace(fab(), '')
P.frame('S10-left-snackbar', 'Left: Home (Selin has no other lists)', phone(inert(left_home) + snackbar('You left “Wedding guests”', bottom='bottom-24')))

P.section('Archived lists', 'Reached from the "Archived lists" row at the end of Home. Rows open the list read-only (S09-archived). Each row\'s menu: Open, Restore, Duplicate, Delete forever. Restoring puts the list back in Lists exactly as it was.')
P.frame('S10-archived', 'Archived lists', phone(archived_screen()))
arch_sheet = ov(sheet('ams', f'''<div class="pb-2 pt-1"><h2 id="ams-t" class="truncate text-title-3">Book club picks</h2><p class="text-body-sm text-muted-foreground">Archived May 2, 12 items</p></div>
    {menu_sheet_rows([("Open", "eye", h09("S09-archived"), "n"), ("Restore", "archive-restore", h10("S10-restored"), "n", "restore"), ("Duplicate", "copy", h10("S10-duplicate"), "n"), ("Delete forever", "trash-2", h10("S10-delete-forever"), "destructive", "delete-forever")])}''', pad='pb-12'))
P.frame('S10-archived-menu', 'Archived list actions', phone(inert(archived_screen()) + arch_sheet))
P.frame('S10-restored', 'Restored: snackbar', phone(archived_screen(rows=ARCHIVED_ROWS()[:1], overlay=snackbar('List restored', 'View', action_href=h08('S08-default'), data_action='view'))))
P.frame('S10-delete-forever', 'Delete an archived list forever', phone(inert(archived_screen()) + dlg('df', 'Delete “Book club picks” forever?',
                                                                                                    dbtn('Cancel', href=h10('S10-archived')) + dbtn('Delete forever', 'destructive', href=h10('S10-archived-empty'), action='confirm-delete'),
                                                                                                    body='12 items, Round 1 and your decisions will be deleted from your account. Nothing outside SwipeSort is changed.')))
P.frame('S10-archived-empty', 'Archived lists: empty', phone(archived_screen(empty=True)))
arch_sk = '<li class="space-y-2.5 px-4 py-4"><span class="block h-5 w-1/2 animate-pulse rounded-full bg-muted"></span><span class="block h-3.5 w-1/3 animate-pulse rounded-full bg-muted"></span></li>'
P.frame('S10-archived-loading', 'Archived lists: loading', phone(f'''{appbar('Archived lists', href=h08('S08-default'), label='Back to lists')}
  <div class="min-h-0 flex-1 px-4 pt-1"><div role="status" aria-busy="true" aria-label="Loading archived lists"><ul class="divide-y overflow-hidden rounded-group bg-card dark:border" aria-hidden="true">{arch_sk * 2}</ul></div></div>'''))

P.section('Backup per list (signed in)', 'Turning backup off deletes the copy in the account, so it asks first and needs a connection (A-134); a snackbar with Undo confirms it. Sharing needs backup: Share on a list that is on this phone only opens a sheet that backs it up first, then invites (A-133). The overflow menu doesn\'t repeat the switch: the state lives in one place, S09\'s Backup group (and S06 › Backup).')
TRIP_SCROLL = dict(translate='-translate-y-[36%]', bar_title='Trip ideas')
bo_body = 'The copy in your account is deleted and the list leaves your other devices. If you lose this phone or move to a new one, the list can\'t be recovered.'
P.frame('S10-backup-off', 'Turn backup off: confirm (deletes the account copy)', phone(inert(ov_solo_default(**TRIP_SCROLL)) + dlg('bo', 'Keep “Trip ideas” on this phone only?',
        dbtn('Cancel', href=h09('S09-default'), action='cancel') + dbtn('Keep on this phone only', 'destructive', href=h10('S10-backup-off-done'), action='confirm-backup-off'), body=bo_body)))


def ios_alert_stacked(aid, title, msg, buttons):
    """iOS alert, buttons stacked (labels too long to sit side by side). buttons: (label, href, style, action)."""
    rows = ''.join(f'<a href="{href}" class="flex min-h-12 items-center justify-center border-t px-4 text-body {"text-destructive" if st == "destructive" else "font-semibold text-primary"}" data-action="{act}">{lab}</a>' for lab, href, st, act in buttons)
    return ov(f'''{scrim('z-30')}
  <div class="absolute inset-x-12 top-1/2 z-40 -translate-y-1/2 overflow-hidden rounded-dialog bg-popover text-center shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="{aid}-t" aria-describedby="{aid}-d">
    <div class="px-4 pb-4 pt-5"><h2 id="{aid}-t" class="text-body font-semibold">{title}</h2><p id="{aid}-d" class="mt-1 text-body-sm text-muted-foreground">{msg}</p></div>
    {rows}
  </div>''')


ios_trip = ov_screen(ov_ios_bar(share=('S31-invite.html#S31-default', 'Share list')), ios_body, translate='-translate-y-[36%]')
P.frame('S10-ios-backup-off', 'iOS: turn backup off (alert, read first)', phone(inert(ios_trip) + ios_alert_stacked('iba', 'Keep “Trip ideas” on this phone only?', bo_body.replace('this phone or', 'this iPhone or'),
        [('Keep on this phone only', h10('S10-backup-off-done'), 'destructive', 'confirm-backup-off'), ('Cancel', h09('S09-ios'), 'cancel', 'cancel')]), kind='ios'))
P.frame('S10-backup-off-offline', 'Offline: turning backup off needs a connection', phone(ov_solo_default(backup='offline-on', top=offline_banner("You're offline. Changes are saved on this phone."), share_disabled=True, **TRIP_SCROLL)))
P.frame('S10-backup-off-done', 'Backup turned off: snackbar with Undo', phone(ov_solo_default(backup='off', meta=TRIP_META + [mi('cloud-off', 'On this phone only')], clip='mb-20',
        overlay=snackbar('“Trip ideas” is on this phone only', 'Undo', action_href=h09('S09-default'), data_action='undo'), **TRIP_SCROLL)))


def share_backup_sheet(state='default'):
    """A-133: sharing needs backup. One ListMoveRow (S05) shows the list and its backup progress."""
    st = {'default': ('cloud-off', 'On this phone only', 'text-muted-foreground', ''),
          'busy': ('loader-circle', 'Backing up…', 'text-primary', ' animate-spin'),
          'offline': ('cloud-off', 'On this phone only', 'text-muted-foreground', '')}[state]
    status = f'<span class="inline-flex shrink-0 items-center gap-1.5 text-body-sm {st[2]}"{" role=\"status\"" if state == "busy" else ""}>{icon(st[0], "size-4" + st[3])}{st[1]}</span>'
    row = (f'<!-- ListMoveRow (S05) --><ul class="mt-4 divide-y border-y" aria-label="List to back up"><li class="flex min-h-14 items-center gap-3 py-2"><span class="flex size-10 shrink-0 items-center justify-center rounded-control bg-secondary text-muted-foreground">{icon("file-spreadsheet")}</span>'
           f'<div class="min-w-0 flex-1"><p class="truncate text-body">Frontend hiring, Q4</p><p class="text-body-sm tabular-nums text-muted-foreground">12 items</p></div>{status}</li></ul>')
    note = ''
    if state == 'offline':
        note = f'<div class="mt-4 flex items-start gap-2 rounded-control bg-muted px-3 py-2.5 text-body-sm" role="status">{icon("wifi-off", "size-4 mt-0.5 shrink-0")}<span>You\'re offline. Backing up and sharing need a connection. The list stays on this phone until then.</span></div>'
    next_link = ''
    if state == 'busy':
        main = btn('Backing up…', size='lg', busy=True)
        next_link = '<a href="S31-invite.html#S31-default" class="absolute inset-0" data-action="next" aria-label="Finish backing up (prototype: click the list; the sheet moves on by itself)"></a>'
    else:
        main = btn('Back up and share', href=h10('S10-share-backing-up'), action='back-up-and-share', size='lg', icon_name='cloud-upload', disabled=state == 'offline')
    return ov(sheet('sbk', f'''<div class="pt-3"><span class="flex size-12 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon("cloud-upload", "size-6")}</span></div>
    <h2 id="sbk-t" class="mt-4 text-title-2">Back up this list to share it</h2>
    <p class="mt-2 text-body text-muted-foreground">Members sort a shared list on their own devices, so it needs to be in your account.</p>
    <div class="relative">{row}{next_link}</div>{note}
    <div class="mt-6 space-y-3">{main}{btn('Not now', 'ghost', href=h09('S09-new-list'), action='not-now', size='lg')}</div>''', pad='pb-12'))


BG_HIRING = inert(ov_new_list())
P.frame('S10-share-backup', 'Share a list that is on this phone only: back it up first', phone(BG_HIRING + share_backup_sheet()))
P.frame('S10-share-backing-up', 'Back up and share: backing up, then the invite opens', phone(BG_HIRING + share_backup_sheet('busy')))
P.frame('S10-share-backup-offline', 'Back up and share: connection lost', phone(BG_HIRING + share_backup_sheet('offline')))

P.section('Offline', 'What works offline (saved on the phone, synced later; D-05): Rename (on shared lists too: the latest rename wins), Duplicate, and Archive, Restore and Delete of solo lists. What needs a connection: what changes a shared list for other members or deletes shared data (Archive, Restore and Delete for everyone, Leave), and on a list that is on this phone only, Share and turning backup off. Those items stay visible, disabled, with the reason.')
P.frame('S10-offline', 'Offline: shared list menu', phone(inert(ov_shared_owner(top=offline_banner("You're offline. Decisions are saved on this phone. Inviting needs a connection."), share_disabled=True, offline=True))
                                                       + dropdown_items(OFFLINE_MENU, top='top-12')))

P.section('Accessibility, iOS and web', 'Large text: dialog buttons stack full width. iOS: rows in Archived lists use swipe actions (Restore, Delete) in addition to the menu. Web: menus and dialogs behave like Android; on desktop the dialog sits in the phone column.')
P.frame('S10-delete-large-text', 'Large text (200%): delete dialog', phone(BG_PHOTOS + dlg('dlt', 'Delete “Trip ideas”?',
                                                                                      dbtn('Delete list', 'destructive', href=h10('S10-deleted-snackbar'), full=True).replace('text-label-lg', 'text-title-3') + dbtn('Cancel', href=h09('S09-default'), full=True).replace('text-label-lg', 'text-title-3'),
                                                                                      body='30 items, Round 1 and your decisions will be deleted from your account and this phone. trip-ideas.csv isn\'t changed.', stacked=True, big=True)))
ios_arch_rows = f'''<!-- Proposed component: SwipeActions (iOS row) --><li class="relative overflow-hidden"><div class="absolute inset-y-0 right-0 flex" aria-hidden="false">
      <a href="{h10('S10-restored')}" class="flex w-20 flex-col items-center justify-center gap-1 bg-primary text-caption text-primary-foreground">{icon('archive-restore')}Restore</a>
      <a href="{h10('S10-delete-forever')}" class="flex w-20 flex-col items-center justify-center gap-1 bg-destructive text-caption text-destructive-foreground">{icon('trash-2')}Delete</a></div>
    <div class="relative mr-40 bg-card"><a href="{h09('S09-archived')}" class="flex min-w-0 flex-col gap-1 py-4 pl-4 pr-3"><span class="truncate text-title-3">Apartment viewings</span><span class="text-body-sm text-muted-foreground">Archived Jul 21, 8 items</span><span class="mt-1">{counts_inline(4, 1, 3)}</span></a></div></li>
    {archived_row('Book club picks', h09('S09-archived'), 'Archived May 2, 12 items', counts_inline(6, 2, 4), h10('S10-archived-menu'), 'books')}'''
P.frame('S10-ios-archived', 'iOS: archived lists with swipe actions', phone(f'''{ios_nav('Archived lists', back_text='Lists', href=h08('S08-ios'))}
  <div class="min-h-0 flex-1 overflow-hidden px-4 pb-8 pt-2">
    <p class="px-1 pb-4 text-body-sm text-muted-foreground">Archived lists are read-only. Restore a list to sort or change it.</p>
    <ul class="divide-y overflow-hidden rounded-control bg-card dark:border" aria-label="Archived lists">{ios_arch_rows}</ul>
  </div>''', kind='ios'))
P.frame('S10-web-desktop', 'Web, desktop browser: delete dialog', desktop(inert(ov_solo_default()) + dlg('dlw', 'Delete “Trip ideas”?',
                                                                                                         dbtn('Cancel', href=h09('S09-default')) + dbtn('Delete list', 'destructive', href=h10('S10-deleted-snackbar')),
                                                                                                         body='30 items, Round 1 and your decisions will be deleted from your account and every device. trip-ideas.csv isn\'t changed.'),
                                                                     'swipesort.app/l/3fP9aD'))
P.write(F10)
