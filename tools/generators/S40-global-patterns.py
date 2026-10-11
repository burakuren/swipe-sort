# Usage: python3 tools/generators/S40-global-patterns.py design/03-screens/S40-global-patterns.html
# Generates the S40 Global patterns catalog: destructive confirmations (Android, iOS, web), snackbars,
# offline banner, sync notice, error and not-found screens, and the desktop-browser frame.
# Backgrounds behind dialogs are inert, simplified copies of the screens that open them (no focusable
# elements, aria-hidden). Helpers: group_e_common.py (icon, phone, desktop).
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from group_e_common import icon, phone, web_phone  # noqa

OUT = sys.argv[1]
IMG = '../02-data/images/'
_uid = [0]


def uid(p='d'):
    _uid[0] += 1
    return f'{p}{_uid[0]}'


# ================================================================ frames and page
class Page:
    def __init__(self):
        self.items = []
        self.index = []  # (section, [(fid, name)])

    def section(self, title, desc):
        self.items.append(f'</main>\n<h2 class="mock-section">{title}</h2>\n<p>{desc}</p>\n<main class="mock-canvas">')
        self.index.append((title, []))

    def add(self, fid, label, inner, short=None):
        assert fid.startswith('S40-'), fid
        self.items.append(f'''
<figure class="frame" data-frame="{fid}" id="{fid}">
  <figcaption class="frame-label">S40 · {label} · <span class="theme-name"></span></figcaption>
  {inner}
</figure>''')
        self.index[-1][1].append((fid, short or label))

    def write(self, out):
        idx = ''.join(
            f'<p><strong>{sec}:</strong> ' + ', '.join(f'<a href="#{f}">{n}</a>' for f, n in frames) + '.</p>\n  '
            for sec, frames in self.index)
        html = f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>S40 Global patterns</title>
<link rel="stylesheet" href="../assets/css/app.css">
</head>
<body class="mock-page">
<header class="mock-doc">
  <h1>S40 Global patterns</h1>
  <p>The one catalog of confirmations, snackbars, offline and sync notices, error and not-found screens and the desktop browser frame. Every other screen uses these exact patterns and strings. Spec with the full catalog table and every string: <a href="S40-global-patterns.md">S40-global-patterns.md</a>. Components: <a href="../01-foundations/components.html">components.html</a>.</p>
  {idx}
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


P = Page()


# ================================================================ static (inert) building blocks
def ib(name, size='size-6', extra=''):
    """Icon-button look, not focusable (backgrounds only)."""
    return f'<span class="flex size-12 shrink-0 items-center justify-center rounded-full {extra}">{icon(name, size)}</span>'


def bg(*parts, cls='flex min-h-0 flex-1 flex-col'):
    return f'<div class="{cls}" aria-hidden="true" inert>' + ''.join(parts) + '</div>'


def top_bar(lead='arrow-left', title=None, sub=None, trailing=()):
    t = ''
    if title:
        s = f'<p class="truncate text-caption text-muted-foreground">{sub}</p>' if sub else ''
        t = f'<div class="min-w-0 flex-1 px-1"><p class="truncate text-title-3">{title}</p>{s}</div>'
    else:
        t = '<span class="flex-1"></span>'
    tr = ''.join(ib(x) for x in trailing)
    return f'<div class="flex h-app-bar shrink-0 items-center gap-1 px-1">{ib(lead)}{t}{tr}</div>'


def large_title(title, trailing=('search',)):
    tr = ''.join(ib(x) for x in trailing)
    return f'<div class="shrink-0"><div class="flex h-app-bar items-center justify-end gap-1 px-1">{tr}</div><p class="px-gutter pb-2 text-title-1">{title}</p></div>'


def nav(active='lists', badge=2, ios=False):
    items = [('lists', 'list-checks', 'Lists'), ('activity', 'activity', 'Activity'), ('settings', 'settings', 'Settings')]
    out = []
    for key, ic, lab in items:
        on = key == active
        b = f'<span class="absolute right-3 top-0 flex h-5 min-w-5 items-center justify-center rounded-full bg-primary px-1 text-caption leading-none text-primary-foreground">{badge}</span>' if key == 'activity' and badge else ''
        if ios:
            col = 'text-primary' if on else 'text-muted-foreground'
            b = b.replace('right-3 top-0', '-right-2.5 -top-1')
            out.append(f'<span class="flex flex-1 flex-col items-center justify-center gap-0.5 text-caption {col}"><span class="relative">{icon(ic, "size-6")}{b}</span>{lab}</span>')
            continue
        pill = 'bg-primary-soft text-primary-soft-foreground' if on else ''
        col = '' if on else 'text-muted-foreground'
        fw = '<span class="font-semibold">' + lab + '</span>' if on else lab
        out.append(f'<span class="flex flex-1 flex-col items-center justify-center gap-1 text-caption {col}"><span class="relative flex h-8 w-16 items-center justify-center rounded-full {pill}">{icon(ic, "size-6")}{b}</span>{fw}</span>')
    h = 'h-14' if ios else 'h-bottom-nav'
    return f'<div class="flex {h} shrink-0 border-t bg-card">{"".join(out)}</div>'


def bar(pct, cls='bg-primary'):
    return f'<span class="block h-1.5 flex-1 overflow-hidden rounded-full bg-muted"><span class="block h-full w-[{pct}%] rounded-full {cls}"></span></span>'


def chip(text, ic=None, cls='bg-secondary text-secondary-foreground'):
    i = icon(ic, 'size-4') if ic else ''
    return f'<span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full px-2.5 text-caption {cls}">{i}{text}</span>'


def counts(r, m, a):
    return ('<span class="flex flex-wrap gap-1.5">'
            + chip(f'<span class="tabular-nums">{r}</span> rejected', 'x', 'bg-reject-soft text-reject-soft-foreground')
            + chip(f'<span class="tabular-nums">{m}</span> maybe', 'circle-help', 'bg-maybe-soft text-maybe-soft-foreground')
            + chip(f'<span class="tabular-nums">{a}</span> accepted', 'check', 'bg-accept-soft text-accept-soft-foreground')
            + '</span>')


def fake_btn(text, variant='primary', ic=None, extra=''):
    v = {'primary': 'bg-primary text-primary-foreground', 'secondary': 'bg-secondary text-secondary-foreground',
         'outline': 'border border-input bg-card', 'ghost': '', 'destructive': 'bg-destructive text-destructive-foreground'}[variant]
    i = icon(ic) if ic else ''
    return f'<span class="flex h-12 w-full items-center justify-center gap-2 rounded-control text-label-lg {v} {extra}">{i}{text}</span>'


def row(ic, title, desc=None, trailing='chevron-right', destructive=False, value=None, lead_html=None):
    col = 'text-destructive' if destructive else ''
    icol = 'text-destructive' if destructive else 'text-muted-foreground'
    lead = lead_html if lead_html else (icon(ic, 'size-5', f'shrink-0 {icol}') if ic else '')
    d = f'<span class="block text-body-sm text-muted-foreground">{desc}</span>' if desc else ''
    v = f'<span class="shrink-0 text-body-sm text-muted-foreground">{value}</span>' if value else ''
    tr = icon(trailing, 'size-5', 'shrink-0 text-muted-foreground') if trailing else ''
    return f'<li class="flex min-h-14 items-center gap-4 px-4 py-3"><span class="flex shrink-0 items-center">{lead}</span><span class="min-w-0 flex-1"><span class="block text-body {col}">{title}</span>{d}</span>{v}{tr}</li>'


def group(rows, header=None):
    h = f'<p class="px-1 pb-2 text-label text-muted-foreground">{header}</p>' if header else ''
    return f'<div>{h}<ul class="divide-y overflow-hidden rounded-group bg-card dark:border">{"".join(rows)}</ul></div>'


def avatar(who, size='size-10'):
    imgs = {'deniz': 'u-deniz', 'mert': 'u-mert'}
    if who in imgs:
        return f'<img src="{IMG}people/{imgs[who]}.svg" alt="" class="{size} shrink-0 rounded-full">'
    initials = {'selin': 'SY', 'gokhan': 'GD', 'alper': 'AT'}.get(who, who)
    return f'<span class="flex {size} shrink-0 items-center justify-center rounded-full bg-muted text-label text-muted-foreground">{initials}</span>'


def stepper(name, step, total):
    segs = ''.join(f'<span class="h-1 flex-1 rounded-full {"bg-primary" if i < step else "bg-muted"}"></span>' for i in range(total))
    return f'<div class="shrink-0 px-gutter pb-3"><div class="flex items-baseline justify-between gap-3"><span class="text-label">{name}</span><span class="text-caption text-muted-foreground">Step {step} of {total}</span></div><div class="mt-2 flex gap-1">{segs}</div></div>'


def checkbox(on=True):
    if on:
        return f'<span class="flex size-6 shrink-0 items-center justify-center rounded-sm bg-primary text-primary-foreground">{icon("check", "size-4")}</span>'
    return '<span class="size-6 shrink-0 rounded-sm border-2 border-input"></span>'


def radio(on):
    if on:
        return '<span class="flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary"><span class="size-3 rounded-full bg-primary"></span></span>'
    return '<span class="size-6 shrink-0 rounded-full border-2 border-input"></span>'


# ================================================================ backgrounds (inert screens)
HOME_ROWS = [
    # name, meta icon, meta, extra chip, progress (pct, label), resume, href
    ('Wedding guests', 'users', 'Shared with 2', 'conflicts', (76, '76 / 100'), True, 'S09-list-overview.html#S09-shared'),
    ('Frontend hiring, Q4', 'circle-dashed', 'Not sorted yet, 12 items', 'device', None, False, 'S09-list-overview.html#S09-new-list'),
    ('Trip ideas', 'circle-dot', 'Round 1 in progress', None, (40, '12 / 30'), True, 'S09-list-overview.html#S09-default'),
    ('Desk setup', 'circle-check', 'Round 2 complete', 'counts', None, False, 'S09-list-overview.html#S09-solo-round-done'),
]


def home_rows(live=False, exclude=(), focus=False, rows=None, archived=True):
    """The S08 Lists content (same rows as S08-default), as inert spans or real links. A list kept on this phone
    only carries the muted per-list label (A-137); other devices never show it (exclude it there)."""
    lis = []
    for name, ic, meta, extra, prog, resume, href in (rows or HOME_ROWS):
        if name in exclude:
            continue
        x = chip('15 conflicts', 'git-compare-arrows', 'bg-conflict text-conflict-foreground') if extra == 'conflicts' else ''
        if extra == 'device':
            x = f'<span class="inline-flex items-center gap-1.5">{icon("cloud-off", "size-4")}On this phone only</span>'
        under = ''
        if prog:
            under = f'<span class="mt-2 flex items-center gap-3">{bar(prog[0])}<span class="shrink-0 text-caption tabular-nums text-muted-foreground">{prog[1]}</span></span>'
        elif extra == 'counts':
            c = lambda cls, i, n, w: f'<span class="inline-flex items-center gap-1 {cls}">{icon(i, "size-4")}<span class="tabular-nums">{n}</span> {w}</span>'
            under = f'<span class="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-caption">{c("text-reject-soft-foreground", "x", 11, "rejected")}{c("text-maybe-soft-foreground", "circle-help", 1, "maybe")}{c("text-accept-soft-foreground", "check", 8, "accepted")}</span>'
        inner = (f'<span class="truncate text-title-3">{name}</span><span class="flex flex-wrap items-center gap-x-3 gap-y-1.5 text-body-sm text-muted-foreground">'
                 f'<span class="inline-flex items-center gap-1.5">{icon(ic, "size-4")}{meta}</span>{x}</span>{under}')
        pr = 'pr-2' if resume else 'pr-4'
        pill = f'<span class="inline-flex h-9 items-center gap-1.5 rounded-full bg-secondary px-3.5 text-label text-secondary-foreground">{icon("play", "size-4")}Resume</span>'
        if live:
            f = ' rounded-control ring-2 ring-inset ring-ring' if focus and not lis else ''
            main = f'<a href="{href}" class="flex min-w-0 flex-1 flex-col gap-1 py-4 pl-4 {pr}{f}" data-action="open-list">{inner}</a>'
            res = f'<a href="S25-sorting.html#S25-web-desktop" class="mr-3 flex min-h-touch shrink-0 items-center" aria-label="Resume sorting {name}">{pill}</a>' if resume else ''
        else:
            main = f'<span class="flex min-w-0 flex-1 flex-col gap-1 py-4 pl-4 {pr}">{inner}</span>'
            res = f'<span class="mr-3 flex min-h-touch shrink-0 items-center">{pill}</span>' if resume else ''
        lis.append(f'<li class="flex items-center">{main}{res}</li>')
    al = ' aria-label="Lists"' if live else ''
    lists = f'<ul class="divide-y overflow-hidden rounded-group bg-card dark:border"{al}>{"".join(lis)}</ul>'
    if not archived:
        return f'<div class="space-y-4">{lists}</div>'
    arch_inner = f'{icon("archive", "size-5", "shrink-0 text-muted-foreground")}<span class="shrink-0 text-body">Archived lists</span><span class="min-w-0 flex-1 text-right text-body text-muted-foreground">2</span>{icon("chevron-right", "size-5", "shrink-0 text-muted-foreground")}'
    if live:
        arch = f'<ul class="overflow-hidden rounded-group bg-card dark:border"><li><a href="S10-list-management.html#S10-archived" class="flex min-h-14 items-center gap-4 px-4 py-3" aria-label="Archived lists, 2">{arch_inner}</a></li></ul>'
    else:
        arch = f'<ul class="overflow-hidden rounded-group bg-card dark:border"><li class="flex min-h-14 items-center gap-4 px-4 py-3">{arch_inner}</li></ul>'
    return f'<div class="space-y-4">{lists}{arch}</div>'


def bg_s08(offline=False, ios=False, nav_on=True, fab='bottom-24', exclude=(), rows=None, archived=True, top=''):
    off = offline_banner("You're offline. Changes are saved on this phone.") if offline else ''
    fab_html = '' if (ios or not fab) else f'<span class="absolute {fab} right-4 inline-flex h-14 items-center gap-3 rounded-tile bg-primary pl-5 pr-6 text-label-lg text-primary-foreground shadow-overlay">{icon("plus", "size-6")}New list</span>'
    head = large_title('Lists', ('search',) if not ios else ('search', 'plus'))
    return bg(head, off, top, f'<div class="relative min-h-0 flex-1 overflow-hidden px-4 pt-2">{home_rows(exclude=exclude, rows=rows, archived=archived)}</div>', fab_html, nav('lists', ios=ios) if nav_on else '', cls='relative flex min-h-0 flex-1 flex-col')


def s09_header(name, meta_html, sync_html=''):
    return f'<div class="px-1"><p class="text-title-1">{name}</p><div class="mt-2 flex flex-wrap items-center gap-x-4 gap-y-2 text-body-sm text-muted-foreground">{meta_html}</div>{sync_html}</div>'


def members_meta(role='Owner', who=None):
    stack = (f'<span class="flex shrink-0 -space-x-2">{avatar("deniz", "size-7 ring-2 ring-background")}{avatar("mert", "size-7 ring-2 ring-background")}'
             f'<span class="flex size-7 items-center justify-center rounded-full bg-muted text-caption text-muted-foreground ring-2 ring-background">SY</span></span>')
    mert = role == 'Decision Maker' or who == 'mert'
    who = 'You, Mert and Selin' if role == 'Owner' else ('Deniz, Selin and you' if mert else 'Deniz, Mert and you')
    ric = {'Owner': 'crown', 'Decision Maker': 'gavel'}.get(role, 'user')
    return (f'<span class="inline-flex items-center gap-2">{stack}<span class="text-foreground underline underline-offset-4">{who}</span></span>'
            f'<span class="inline-flex items-center gap-1.5">{icon("list", "size-4")}100 items</span>{chip(role, ric)}')


def bg_s09_shared(role='Owner', banner='', sync_html='', alert_html='', ios=False, as_html=False, who=None):
    mine = (76, 17, 11, 48) if role == 'Owner' else ((85, 21, 14, 50) if (role == 'Decision Maker' or who == 'mert') else (43, 9, 6, 28))
    status = ''.join(
        f'<li class="flex items-center gap-3 py-2.5"><span class="inline-flex h-7 w-28 shrink-0 items-center gap-1.5 rounded-full px-2.5 text-caption {cls}">{icon(ic, "size-4")}{lab}</span><span class="min-w-0 flex-1 text-body-sm text-muted-foreground">{desc}</span><span class="text-label tabular-nums">{n}</span></li>'
        for lab, ic, cls, desc, n in [
            ('Agreed', 'check-check', 'border', 'Everyone chose the same', 32),
            ('Conflict', 'git-compare-arrows', 'bg-conflict text-conflict-foreground', 'Mert decides these', 15),
            ('Pending', 'clock', 'bg-muted text-muted-foreground', 'Not everyone has decided', 53)])
    trailing = ('user-plus', 'ellipsis-vertical') if role == 'Owner' else ('ellipsis-vertical',)
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-1"><div class="space-y-6">
      {s09_header('Wedding guests', members_meta(role, who), sync_html)}
      {alert_html}
      <div class="rounded-group bg-card p-4 dark:border"><div class="flex items-center justify-between gap-3"><span class="text-label">My progress</span><span class="text-caption text-muted-foreground">Round 1, shared</span></div><p class="mt-3 text-title-3 tabular-nums">{mine[0]} / 100 decided</p><span class="mt-2 flex">{bar(mine[0])}</span><span class="mt-3 block">{counts(*mine[1:])}</span>{fake_btn("Continue sorting", "primary", "play", "mt-4")}</div>
      <div class="rounded-group bg-card p-4 dark:border"><div class="flex items-center justify-between gap-3"><span class="text-label">List status</span><span class="text-caption text-muted-foreground">All members</span></div><ul class="mt-1 divide-y">{status}</ul></div>
    </div></div>'''
    head = ios_nav('Lists', '', trailing_icons=trailing) if ios else top_bar('arrow-left', None, None, trailing)
    if as_html:
        return head + banner + body
    return bg(head, banner, body)


def bg_s09_solo(name='Trip ideas', items=30, decided=12, cnt=(6, 1, 5), src='trip-ideas.csv', src_icon='file-spreadsheet', ios=False,
               round_label='Round 1', button=('Continue sorting', 'play'), rows=None, template='Photo', round_items=None, extra='', shift=''):
    round_items = round_items or items
    pct = round(decided * 100 / round_items)
    rows = rows or [row('list-checks', 'Results', f'{decided} decided'), row('history', 'Rounds', 'Round 1 in progress'),
                    row('layout-template', 'Card template', template), row('file-down', 'Export', 'CSV, Excel, Google Sheets or a text summary')]
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-1"><div class="space-y-6 {shift}">
      {s09_header(name, f'<span class="inline-flex items-center gap-1.5">{icon("lock", "size-4")}Only you</span><span class="inline-flex items-center gap-1.5">{icon(src_icon, "size-4")}{items} items from {src}</span>')}
      <div class="rounded-group bg-card p-4 dark:border"><div class="flex items-center justify-between gap-3"><span class="text-label">Progress</span><span class="text-caption text-muted-foreground">{round_label}</span></div><p class="mt-3 text-title-3 tabular-nums">{decided} / {round_items} decided</p><span class="mt-2 flex">{bar(pct)}</span><span class="mt-3 block">{counts(*cnt)}</span>{fake_btn(button[0], "primary", button[1], "mt-4")}</div>
      {group(rows)}{extra}
    </div></div>'''
    head = ios_nav('Lists', '', trailing_icons=('ellipsis',)) if ios else top_bar('arrow-left', None, None, ('ellipsis-vertical',))
    return bg(head, body)


def bg_s09_solo_large():
    c = lambda cls, i, n, w: f'<span class="inline-flex h-12 items-center gap-2 rounded-full px-4 text-title-3 font-medium {cls}">{icon(i, "size-6")}<span class="tabular-nums">{n}</span> {w}</span>'
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-1"><div class="space-y-6">
      <div class="px-1"><p class="text-display">Trip ideas</p><p class="mt-2 flex items-center gap-2 text-title-2 font-normal text-muted-foreground">{icon("lock", "size-7")}Only you</p></div>
      <div class="rounded-group bg-card p-4 dark:border"><p class="text-title-2 font-medium">Progress</p><p class="mt-3 text-display tabular-nums">12 / 30 decided</p><span class="mt-3 flex">{bar(40)}</span>
        <span class="mt-4 flex flex-wrap gap-2">{c("bg-reject-soft text-reject-soft-foreground", "x", 6, "rejected")}{c("bg-maybe-soft text-maybe-soft-foreground", "circle-help", 1, "maybe")}{c("bg-accept-soft text-accept-soft-foreground", "check", 5, "accepted")}</span></div>
    </div></div>'''
    return bg(top_bar('arrow-left', None, None, ('ellipsis-vertical',)), body)


def member_row(who, name, role_ic, role, prog, you=False):
    r = f'<span class="inline-flex items-center gap-1">{icon(role_ic, "size-4")}{role}</span>' if role_ic else role
    y = ' (you)' if you else ''
    return (f'<li class="flex min-h-16 items-center gap-3 px-4 py-3">{avatar(who)}<span class="min-w-0 flex-1"><span class="block text-body">{name}{y}</span>'
            f'<span class="flex flex-wrap gap-x-3 text-body-sm text-muted-foreground">{r}<span class="tabular-nums">{prog}</span></span></span>{icon("ellipsis-vertical", "size-5", "shrink-0 text-muted-foreground")}</li>')


def bg_s34(ios=False):
    members = ''.join([
        member_row('deniz', 'Deniz Yılmaz', 'crown', 'Owner', '76 / 100 decided', True),
        member_row('mert', 'Mert Aydın', 'gavel', 'Decision Maker', '85 / 100 decided'),
        member_row('selin', 'Selin Yılmaz', None, 'Collaborator', '43 / 100 decided'),
    ])
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-2"><div class="space-y-6">
      <div><p class="px-1 pb-2 text-label text-muted-foreground">3 members</p><ul class="divide-y overflow-hidden rounded-group bg-card dark:border">{members}</ul></div>
      {group([row('user-plus', 'Invite people', 'Invite links: 2 active, Collaborator')])}
      {group([row('scale', 'Conflict rule', 'Decision Maker decides')], 'Resolving conflicts')}
      {group([row('arrow-right-left', 'Transfer ownership', 'Make another member the Owner'), row('log-out', 'Leave list', None, None)], 'Ownership')}
    </div></div>'''
    head = ios_nav('Wedding guests', 'Members') if ios else top_bar('arrow-left', 'Members', 'Wedding guests')
    return bg(head, body)


CARD_NEXT = ('c078', 'Anna-Katharina Rosenthal-Brückner', 'Colleague', [('Phone', '+43 1 0000 4117'), ('City', 'Vienna')], "Bride's")
CARD_TOP = ('c077', 'Mia Andersson', 'Colleague', [('Phone', '+46 8 0000 4021'), ('Email', 'mia.andersson@example.com'), ('City', 'Stockholm')], "Bride's")


def card_inner(c):
    img, name, sub, rows_, tag = c
    dl = ''.join(f'<span class="flex gap-3"><span class="w-16 shrink-0 text-muted-foreground">{k}</span><span class="min-w-0 truncate tabular-nums">{v}</span></span>' for k, v in rows_)
    return (f'<img src="{IMG}people/{img}.svg" alt="" class="h-[46%] w-full object-cover"><span class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-5">'
            f'<span class="line-clamp-3 text-card-title">{name}</span><span class="mt-1 text-body-lg text-muted-foreground">{sub}</span>'
            f'<span class="mt-4 flex flex-col gap-2 text-body">{dl}</span><span class="mt-auto pt-3">{chip(tag)}</span></span>')


def photo_inner(img, place, country, best='Apr to Jun', budget='€900'):
    """Trip ideas on the Photo template (A-130, A-131): the image link, Place as title, Country, then Best time
    and Budget (EUR)."""
    rows_ = ''.join(f'<span class="flex gap-3"><span class="w-24 shrink-0 text-muted-foreground">{k}</span><span class="min-w-0 truncate tabular-nums">{v}</span></span>' for k, v in (('Best time', best), ('Budget', budget)))
    return (f'<img src="{IMG}photos/{img}.svg" alt="" class="min-h-0 w-full flex-1 object-cover">'
            f'<span class="block shrink-0 px-6 pb-5 pt-4"><span class="block text-title-2">{place}</span><span class="mt-0.5 block text-body text-muted-foreground">{country}</span><span class="mt-3 flex flex-col gap-1.5 text-body-sm">{rows_}</span></span>')


def dbutton(kind, ic, label, n):
    return (f'<span class="flex min-w-touch flex-col items-center gap-1.5"><span class="flex size-16 items-center justify-center rounded-full bg-{kind}-soft text-{kind}-soft-foreground">{icon(ic, "size-7")}</span>'
            f'<span class="text-center text-caption">{label} <span class="tabular-nums text-muted-foreground">{n}</span></span></span>')


def small_round(ic, label):
    return (f'<span class="flex min-w-touch flex-col items-center gap-1.5"><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon(ic, "size-5")}</span>'
            f'<span class="text-caption text-muted-foreground">{label}</span></span>')


def s25_body(shared=False, decided=76, cnt=(17, 11, 48), status_html='', kbd=False, ios=False, banner='', name='Wedding guests', total=100, photo=False):
    sub = 'Round 1, shared' if shared else 'Round 1'
    if ios:
        head = f'<div class="grid h-14 shrink-0 grid-cols-3 items-center px-2"><span class="px-2 text-body text-primary">Close</span><span class="text-center"><span class="block truncate text-body font-semibold">{name}</span><span class="block text-caption text-muted-foreground">{sub}</span></span><span class="flex justify-end">{ib("ellipsis", "size-6", "text-primary")}</span></div>'
    else:
        head = f'<div class="flex h-app-bar shrink-0 items-center gap-1 px-1">{ib("x")}<div class="min-w-0 flex-1 px-1"><p class="truncate text-title-3">{name}</p><p class="text-caption text-muted-foreground">{sub}</p></div>{ib("ellipsis-vertical")}</div>'
    hints = ''
    if kbd:
        k = lambda key, lab: f'<span class="inline-flex items-center gap-1.5"><kbd class="inline-flex h-6 min-w-6 items-center justify-center rounded-sm border border-b-2 bg-card px-1.5 text-caption text-foreground">{key}</kbd>{lab}</span>'
        hints = f'<div class="flex shrink-0 flex-wrap items-center justify-center gap-x-4 gap-y-1 pb-4 text-caption text-muted-foreground">{k("←", "Reject")}{k("↑", "Maybe")}{k("→", "Accept")}{k("Z", "Undo")}{k("N", "Note")}</div>'
    return f'''{head}{banner}
  <div class="shrink-0 px-gutter pb-1"><div class="flex items-center justify-between gap-3"><span class="text-label tabular-nums">{decided} / {total} decided</span>{status_html}</div><span class="mt-2 flex">{bar(round(decided * 100 / total))}</span></div>
  <div class="relative mt-2 min-h-0 flex-1">
    <div class="absolute inset-x-gutter bottom-5 top-0 flex origin-top translate-y-10 scale-95 flex-col overflow-hidden rounded-hero border bg-card shadow-raised">{photo_inner('ph12', 'Göreme, Cappadocia', 'Türkiye', 'Apr to May', '€700') if photo else card_inner(CARD_NEXT)}</div>
    <div class="absolute inset-x-gutter bottom-5 top-0 flex flex-col overflow-hidden rounded-hero bg-card shadow-hero">{photo_inner('ph13', 'Alfama, Lisbon', 'Portugal', 'Apr to Jun', '€900') if photo else card_inner(CARD_TOP)}</div>
  </div>
  <div class="flex shrink-0 items-start justify-between px-5 pb-4 pt-2">{small_round("undo-2", "Undo")}{dbutton("reject", "x", "Reject", cnt[0])}{dbutton("maybe", "circle-help", "Maybe", cnt[1])}{dbutton("accept", "check", "Accept", cnt[2])}{small_round("sticky-note", "Note")}</div>{hints}'''


def bg_s25(**kw):
    return bg(s25_body(**kw))


def bg_s24(shared=False):
    if shared:
        name, notice, summary = 'Wedding guests', 'Starting Round 2 ends Round 1 for everyone. Decisions made so far are kept.', 'Round 2 will have 6 items'
        opts = [('All items', 'Every item in the list, decided or not', '100', False), ('Maybe pile', 'Final decision is Maybe', '6', True),
                ('Accepted items', 'Final decision is Accept', '22', False), ('Custom selection', 'Filter by a field or pick items by hand', '', False)]
    else:
        name, notice, summary = 'Trip ideas', '12 of 30 decided. Starting Round 2 ends Round 1.', 'Round 2 will have 5 items'
        opts = [('All items', 'Every item in the list, decided or not', '30', False), ('Maybe pile', 'Items marked Maybe in Round 1', '1', False),
                ('Accepted items', 'Narrow down what you accepted', '5', True), ('Custom selection', 'Filter by a field or pick items by hand', '', False)]
    lis = ''.join(f'<li class="flex min-h-16 items-center gap-4 px-4 py-3">{radio(on)}<span class="min-w-0 flex-1"><span class="block text-body">{t}</span><span class="block text-body-sm text-muted-foreground">{d}</span></span>{chip(n) if n else ""}</li>' for t, d, n, on in opts)
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-2"><div class="space-y-6">
      <div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground">{icon("info", "size-5", "shrink-0")}<div><p class="text-label">Round 1 is still open</p><p class="mt-0.5 text-body-sm">{notice}</p></div></div>
      <div><p class="flex items-baseline justify-between px-1 pb-2 text-label text-muted-foreground"><span>Items</span>{'<span class="text-caption">Based on final decisions</span>' if shared else ''}</p><ul class="divide-y overflow-hidden rounded-group bg-card dark:border">{lis}</ul></div>
    </div></div>
    <div class="shrink-0 border-t px-gutter pb-4 pt-3"><p class="pb-3 text-center text-body-sm text-muted-foreground">{summary}</p>{fake_btn("Start round")}</div>'''
    return bg(top_bar('x', 'Start a round', name), body)


def bg_s13():
    names = [('c001', 'Ayşe Demir', '+90 500 000 97 62'), ('c002', 'Mehmet Yılmaz', '2 phone numbers'), ('c003', 'Zeynep Kaya', '+90 500 000 97 10'),
             ('c004', 'Emre Çelik', '+90 500 000 67 46'), ('c005', 'Elif Şahin', '+90 500 000 45 82'), ('c006', 'Burak Arslan', '+90 500 000 95 92'), (None, 'Gökhan Doğan', '+90 500 000 97 41')]
    lis = ''.join(f'<li class="flex min-h-16 items-center gap-4 px-4 py-2">{checkbox(True)}{f"<img src=\"{IMG}people/{i}.svg\" alt=\"\" class=\"size-10 shrink-0 rounded-full\">" if i else avatar("gokhan")}<span class="min-w-0 flex-1"><span class="block truncate text-body">{n}</span><span class="block text-body-sm text-muted-foreground">{p}</span></span></li>' for i, n, p in names)
    body = f'''{stepper("Select items", 2, 5)}
    <div class="shrink-0 px-4 pb-2"><span class="flex h-12 items-center gap-3 rounded-full bg-secondary px-4 text-body text-muted-foreground">{icon("search")}Search 96 contacts</span></div>
    <div class="flex shrink-0 items-center gap-4 px-8 py-2">{checkbox(True)}<span class="text-label">88 of 96 selected</span></div>
    <ul class="min-h-0 flex-1 divide-y overflow-hidden px-4">{lis}</ul>
    <div class="shrink-0 px-gutter pb-4 pt-3">{fake_btn("Continue with 88 contacts", extra="h-14")}</div>'''
    return bg(top_bar('x', 'Import', 'New list'), body)


def bg_s21():
    cols = [('Ad Soyad', 'Name', 'Ayşe Aydın'), ('Telefon', 'Phone', '+90 500 000 20 77'), ('E-posta', 'Email', 'ayse.aydin@example.com'), ('Taraf', 'Side', "Groom's"), ('Yakınlık', 'Relationship', 'Family'), ('Şehir', 'City', 'Ankara'), ('Adres', 'New field: Address', 'Çankaya, Ankara')]
    lis = ''.join(f'<li class="flex min-h-16 items-center gap-3 px-4 py-2"><span class="min-w-0 flex-1"><span class="block text-body">{a}</span><span class="block truncate text-body-sm text-muted-foreground">{s}</span></span>{icon("arrow-right", "size-4", "shrink-0 text-muted-foreground")}<span class="w-36 shrink-0 truncate rounded-control border border-input bg-card px-3 py-2 text-body-sm">{b}</span></li>' for a, b, s in cols)
    body = f'''{stepper("Map fields", 3, 5)}
    <div class="min-h-0 flex-1 overflow-hidden px-4"><div class="space-y-4"><p class="px-1 text-body-sm text-muted-foreground">mert-family.csv, 15 rows. Columns go into the fields of Wedding guests.</p>
    <ul class="divide-y overflow-hidden rounded-group bg-card dark:border">{lis}</ul></div></div>
    <div class="shrink-0 px-gutter pb-4 pt-3">{fake_btn("Continue", extra="h-14")}</div>'''
    return bg(top_bar('x', 'Add items', 'Wedding guests'), body)


def bg_s17():
    fields = ''.join(chip(f, None, 'border bg-card text-foreground') for f in ['Name', 'Price (€)', 'Store', 'Photo', 'Link'])
    items = ''.join(f'<li class="flex min-h-16 items-center gap-3 px-4 py-2"><img src="{IMG}products/{i}.svg" alt="" class="size-10 shrink-0 rounded-control object-cover"><span class="min-w-0 flex-1"><span class="block truncate text-body">{n}</span><span class="block text-body-sm text-muted-foreground">{p}</span></span>{icon("ellipsis-vertical", "size-5", "shrink-0 text-muted-foreground")}</li>'
                    for i, n, p in [('p01', 'Walnut sit-stand desk, 140 × 70 cm', '€649, Oakline'), ('p02', 'Ergo Mesh task chair', '€389, Nordhaus'), ('p03', 'Low-profile mechanical keyboard', '€129, Keystone')])
    body = f'''{stepper("Set up fields", 2, 4)}
    <div class="min-h-0 flex-1 overflow-hidden px-4"><div class="space-y-6">
      <div><p class="px-1 pb-2 text-label text-muted-foreground">Fields</p><div class="flex flex-wrap gap-2 rounded-group bg-card p-4 dark:border">{fields}</div></div>
      <div><p class="px-1 pb-2 text-label text-muted-foreground">3 items</p><ul class="divide-y overflow-hidden rounded-group bg-card dark:border">{items}</ul></div>
    </div></div>
    <div class="shrink-0 px-gutter pb-4 pt-3">{fake_btn("Continue", extra="h-14")}</div>'''
    return bg(top_bar('x', 'New list', 'Manual entry'), body)


def bg_s22():
    def tile(name, sel=False, custom=False, img=True):
        schem = f'<span class="flex h-24 flex-col gap-1.5 rounded-control bg-muted p-2">{"<span class=\"h-8 rounded-sm bg-background\"></span>" if img else ""}<span class="h-2.5 w-2/3 rounded-full bg-background"></span><span class="h-2 w-1/2 rounded-full bg-background"></span><span class="h-2 w-3/4 rounded-full bg-background"></span></span>'
        b = chip('Custom') if custom else ''
        brd = 'border-2 border-primary' if sel else 'border'
        return f'<span class="flex flex-col gap-2 rounded-tile {brd} bg-card p-3">{schem}<span class="flex items-center justify-between gap-2"><span class="truncate text-label">{name}</span>{b}</span></span>'
    grid = ''.join([tile('Person'), tile('Product'), tile('Photo'), tile('Task', img=False), tile('Candidate', img=False), tile('Generic', img=False)])
    custom = ''.join([tile('Guest with table side', custom=True), tile('Candidate, compact', custom=True, img=False)])
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-2"><div class="space-y-6">
      <div><p class="px-1 pb-2 text-label text-muted-foreground">Your templates</p><div class="grid grid-cols-2 gap-3">{custom}</div></div>
      <div><p class="px-1 pb-2 text-label text-muted-foreground">Built-in</p><div class="grid grid-cols-2 gap-3">{grid}</div></div>
    </div></div>'''
    return bg(top_bar('arrow-left', 'Card templates', None, ('plus',)), body)


def bg_s23():
    rows_ = [('Title', 'Name'), ('Subtitle', 'Location'), ('Row 1', 'Years of experience'), ('Row 2', 'Expected salary'), ('Tags', 'Source')]
    lis = ''.join(f'<li class="flex min-h-14 items-center gap-3 px-4 py-2">{icon("grip-vertical", "size-5", "shrink-0 text-muted-foreground")}<span class="w-20 shrink-0 text-body-sm text-muted-foreground">{a}</span><span class="min-w-0 flex-1 truncate text-body">{b}</span>{icon("chevron-down", "size-5", "shrink-0 text-muted-foreground")}</li>' for a, b in rows_)
    card = (f'<div class="mx-auto w-64 rounded-hero bg-card p-5 shadow-hero"><p class="text-title-2">Lena Hoffmann</p><p class="mt-1 text-body text-muted-foreground">Berlin</p>'
            f'<div class="mt-3 space-y-1.5 text-body-sm"><p class="flex gap-2"><span class="w-24 shrink-0 text-muted-foreground">Experience</span>6</p><p class="flex gap-2"><span class="w-24 shrink-0 text-muted-foreground">Salary</span>€78,000</p></div>'
            f'<div class="mt-3">{chip("Referral")}</div></div>')
    body = f'''<div class="shrink-0 bg-muted px-gutter py-5">{card}<p class="mt-3 text-center text-caption text-muted-foreground">Item 1 of 12</p></div>
    <div class="min-h-0 flex-1 overflow-hidden px-4 pt-4"><p class="px-1 pb-2 text-label text-muted-foreground">Layout</p><ul class="divide-y overflow-hidden rounded-group bg-card dark:border">{lis}</ul></div>
    <div class="shrink-0 px-gutter pb-4 pt-3">{fake_btn("Save template")}</div>'''
    return bg(top_bar('x', 'Edit template', 'Candidate, compact'), body)


def field_row(label, value, extra=''):
    return f'<li class="px-4 py-3"><span class="block text-body-sm text-muted-foreground">{label}</span><span class="block text-body">{value}</span>{extra}</li>'


def bg_s26(kind='edited'):
    if kind == 'edit':
        def inp(label, value, focus=False):
            ring = 'border-primary ring-2 ring-ring/30' if focus else 'border-input'
            return f'<div><span class="text-label">{label}</span><span class="mt-1.5 flex h-12 items-center rounded-control border {ring} bg-card px-3.5 text-body">{value}</span></div>'
        body = f'''<div class="min-h-0 flex-1 overflow-hidden px-gutter pt-2"><div class="space-y-4">
          <p class="flex gap-2 text-body-sm text-muted-foreground">{icon("info", "size-4", "mt-0.5 shrink-0")}Changes stay in SwipeSort. The source isn't changed.</p>
          {inp("Name", "Gökhan Doğan")}{inp("Phone", "+90 500 000 97 41", True)}<p class="-mt-2 text-body-sm text-muted-foreground">Original: +90 500 000 97 4</p>{inp("Email", "gokhan.dogan@example.com")}{inp("City", "Bursa")}
        </div></div>
        <div class="flex shrink-0 gap-2 px-gutter pb-4 pt-3">{fake_btn("Cancel", "outline")}{fake_btn("Save changes")}</div>'''
        return bg(top_bar('x', 'Edit Gökhan Doğan'), body)
    seg = ''.join(f'<span class="flex h-10 flex-1 items-center justify-center gap-1.5 rounded-full text-label">{icon(i, "size-4")}{t}</span>' for i, t in [('x', 'Reject'), ('circle-help', 'Maybe'), ('check', 'Accept')])
    if kind == 'note':
        who, name, sub = 'deniz', 'Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein', 'Friend'
        extra = (f'<div><p class="px-1 pb-2 text-label text-muted-foreground">Notes</p><div class="rounded-group bg-card p-4 dark:border"><div class="flex items-center justify-between"><span class="text-label">My note</span><span class="text-caption text-muted-foreground">Sep 28</span></div>'
                 f'<p class="mt-1 text-body">Flying in from Berlin. Ask about dates first.</p><div class="mt-2 flex gap-4 text-label text-primary"><span>Edit</span><span>Delete</span></div></div></div>')
        fields = [field_row('Phone', 'Add phone'), field_row('Email', 'maximiliane.vonhohenberg@example.com')]
        avatar_html = f'<img src="{IMG}people/c014.svg" alt="" class="size-14 shrink-0 rounded-full">'
    else:
        name, sub = 'Alper Turan', 'Friend'
        extra = ''
        fields = [field_row('Phone', '+90 500 000 07 64'), field_row('Email', 'alper.turan@example.com'), field_row('Side', "Groom's"),
                  field_row('City', 'Ankara', f'<span class="mt-1 flex items-center gap-1.5 text-body-sm text-muted-foreground">{icon("pencil-line", "size-4")}Edited. Original: İstanbul</span><span class="mt-1 block text-label text-primary">Revert to original</span>')]
        avatar_html = avatar('alper', 'size-14')
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-1"><div class="space-y-6">
      <div class="flex items-center gap-4 px-1">{avatar_html}<div class="min-w-0"><p class="text-title-2">{name}</p><p class="text-body text-muted-foreground">{sub}</p></div></div>
      <div><p class="px-1 pb-2 text-label text-muted-foreground">My decision</p><div class="flex rounded-full bg-secondary p-1">{seg}</div></div>
      {extra}
      <div><p class="px-1 pb-2 text-label text-muted-foreground">Fields</p><ul class="divide-y overflow-hidden rounded-group bg-card dark:border">{"".join(fields)}</ul></div>
    </div></div>'''
    return bg(top_bar('arrow-left', 'Item details', None, ('pencil',)), body)


def bg_s31():
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-2"><div class="space-y-6">
      <p class="px-1 text-body text-muted-foreground">People you invite sort the same 100 items on their own. The list then shows where you agree.</p>
      <div><p class="px-1 pb-2 text-label text-muted-foreground">Invite as</p><ul class="divide-y overflow-hidden rounded-group bg-card dark:border">
        <li class="flex min-h-16 items-center gap-4 px-4 py-3">{radio(True)}<span class="min-w-0 flex-1"><span class="block text-body">Collaborator</span><span class="block text-body-sm text-muted-foreground">Sorts every item and adds notes.</span></span></li>
        <li class="flex min-h-16 items-center gap-4 px-4 py-3">{radio(False)}<span class="min-w-0 flex-1"><span class="block text-body">Decision Maker</span><span class="block text-body-sm text-muted-foreground">Also resolves conflicts.</span></span></li></ul></div>
      <div><p class="px-1 pb-2 text-label text-muted-foreground">Invite link</p><div class="rounded-group bg-card p-4 dark:border"><p class="truncate text-body">swipesort.app/join/k7Qm2xPa</p><p class="mt-1 text-body-sm text-muted-foreground">Expires Oct 21, in 11 days</p><p class="mt-3 text-label text-primary">Reset link</p></div></div>
    </div></div>
    <div class="flex shrink-0 flex-col gap-2 px-gutter pb-4 pt-3">{fake_btn("Copy link", "primary", "copy")}{fake_btn("Share…", "ghost", "share-2")}</div>'''
    return bg(top_bar('x', 'Invite to Wedding guests'), body)


def bg_s35():
    def card(t, d, on, cur=False):
        brd = 'border-2 border-primary' if on else 'border'
        c = f'<span class="mt-2 block">{chip("Current rule")}</span>' if cur else ''
        return f'<li class="flex gap-4 rounded-tile {brd} bg-card p-4">{radio(on)}<span class="min-w-0 flex-1"><span class="block text-body">{t}</span><span class="block text-body-sm text-muted-foreground">{d}</span>{c}</span></li>'
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-2"><div class="space-y-4">
      <p class="px-1 text-body text-muted-foreground">When members decide an item differently, the item is a conflict. The rule decides what happens next.</p>
      <ul class="space-y-3">{card("Everyone must agree", "Conflicts stay open until members change their decisions to match.", False)}{card("Majority decides", "The decision most members chose is final. Ties go to the Decision Maker.", True)}{card("Decision Maker decides", "Mert chooses the final decision of every conflict.", False, True)}</ul>
    </div></div>'''
    return bg(top_bar('arrow-left', 'Conflict rule', 'Wedding guests'), body)


def bg_s06(offline=False, paused=False, ios=False):
    backup = row('cloud-alert' if paused else 'cloud-check', 'Backup', 'Backup paused. 12 changes waiting' if paused else 'Backed up today at 09:12')
    groups = [
        group([row(None, 'Deniz Yılmaz', 'deniz.yilmaz@example.com', lead_html=avatar('deniz')), backup], 'Account'),
        group([row('sun-moon', 'Appearance', None, value='System'), row('vibrate', 'Haptics', None, trailing=None, value='On'), row('bell', 'Notifications', None, value='On'), row('layout-template', 'Card templates')], 'Preferences'),
        group([row('shield', 'Privacy'), row('life-buoy', 'Help and feedback'), row('log-out', 'Sign out', None, None)]),
    ]
    off = offline_banner("You're offline. Changes are saved on this phone.") if offline else ''
    return bg(large_title('Settings', ()), off, f'<div class="min-h-0 flex-1 overflow-hidden px-4 pt-2"><div class="space-y-6">{"".join(groups)}</div></div>', nav('settings', ios=ios))


def bg_s07():
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-2"><div class="space-y-6">
      <div class="flex flex-col items-center gap-2 py-2">{avatar("deniz", "size-24")}<p class="text-title-2">Deniz Yılmaz</p><p class="text-body text-muted-foreground">deniz.yilmaz@example.com</p></div>
      {group([row(None, 'Google', 'deniz.yilmaz@example.com', value='Connected', lead_html='<span class="flex size-6 items-center justify-center rounded-full border text-caption">G</span>'), row('key-round', 'Email and password', 'Password set Sep 27')], 'Sign-in methods')}
      {group([row('trash-2', 'Delete account', 'Delete your account, your lists and your notes', None, True)])}
    </div></div>'''
    return bg(top_bar('arrow-left', 'Profile'), body)


def bg_s07_confirm():
    li = lambda ic, t: f'<li class="flex gap-3">{icon(ic, "size-5", "mt-0.5 shrink-0 text-muted-foreground")}<span>{t}</span></li>'
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-gutter pt-2"><div class="space-y-5">
      <p class="text-title-2">Confirm deletion</p><p class="text-body text-muted-foreground">This is the last step. After this, your account can't be restored.</p>
      <ul class="space-y-3 rounded-group bg-card p-4 text-body dark:border">{li("arrow-right-left", "“Wedding guests” moves to Mert Aydın")}{li("trash-2", "“Desk setup”, “Trip ideas” and 2 archived lists are deleted")}{li("smartphone", "“Frontend hiring, Q4” is on this phone only. It stays on this phone, without an account.")}{li("trash-2", "Your profile, decisions and notes are deleted")}</ul>
      <div><span class="text-label">To confirm, type delete</span><span class="mt-1.5 flex h-12 items-center rounded-control border border-input bg-card px-3.5 text-body">delete</span><p class="mt-1.5 text-body-sm text-muted-foreground">Lowercase is fine.</p></div>
    </div></div>
    <div class="flex shrink-0 flex-col gap-2 px-gutter pb-4 pt-3">{fake_btn("Delete account", "destructive", extra="h-14")}{fake_btn("Keep my account", "ghost")}</div>'''
    return bg(top_bar('arrow-left', 'Delete account'), body)


def bg_s10_archived():
    lis = ''.join(f'<li class="flex min-h-16 items-center gap-3 px-4 py-3"><span class="min-w-0 flex-1"><span class="block text-title-3">{n}</span><span class="block text-body-sm text-muted-foreground">{m}</span></span>{icon("ellipsis-vertical", "size-5", "shrink-0 text-muted-foreground")}</li>'
                  for n, m in [('Apartment viewings', 'Archived Jul 21, 8 items'), ('Book club picks', 'Archived May 2, 12 items')])
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-4 pt-2"><div class="space-y-4"><p class="px-1 text-body-sm text-muted-foreground">Archived lists are read-only and hidden from Lists. Restore a list to sort or change it.</p>
      <ul class="divide-y overflow-hidden rounded-group bg-card dark:border">{lis}</ul></div></div>'''
    return bg(top_bar('arrow-left', 'Archived lists'), body)


# ================================================================ iOS backgrounds
def ios_nav(back, title, trailing_icons=()):
    tr = ''.join(f'<span class="flex size-12 items-center justify-center text-primary">{icon(x, "size-6")}</span>' for x in trailing_icons)
    return (f'<div class="grid h-14 shrink-0 grid-cols-3 items-center px-2"><span class="flex items-center gap-0.5 text-body text-primary">{icon("chevron-left", "size-6")}<span class="truncate">{back}</span></span>'
            f'<span class="truncate text-center text-body font-semibold">{title}</span><span class="flex justify-end">{tr}</span></div>')


# ================================================================ overlays
def scrim(z='z-30', op='bg-scrim/50'):
    return f'<div class="absolute inset-0 {z} {op}" aria-hidden="true"></div>'


BTN = 'inline-flex min-h-12 items-center justify-center rounded-control px-4 py-2 text-label-lg'
VAR = {'destructive': 'bg-destructive text-destructive-foreground', 'primary': 'bg-primary text-primary-foreground', 'ghost': ''}


def action(text, variant='ghost', href=None, act=None, extra='', focus=False):
    base = BTN.replace(' text-label-lg', '') if ' text-' in f' {extra}' else BTN
    cls = f'{base} {VAR[variant]} {extra}'
    if focus:
        cls += ' ring-2 ring-ring ring-offset-2 ring-offset-popover'
    da = f' data-action="{act}"' if act else ''
    if href:
        return f'<a href="{href}" class="{cls}"{da}>{text}</a>'
    return f'<button type="button" class="{cls}"{da}>{text}</button>'


def dialog(title, body, cancel, confirm, variant='destructive', extra='', cancel_href=None, confirm_href=None,
           act='confirm', stacked=False, large=False, focus_cancel=False, note=None):
    t, d = uid('t'), uid('d')
    paras = ''.join(f'<p>{p}</p>' for p in (body if isinstance(body, (list, tuple)) else [body]))
    tcls = 'text-display' if large else 'text-title-3'
    bcls = 'text-title-1 font-normal' if large else 'text-body'
    n = f'<p class="mt-3 text-body-sm text-muted-foreground">{note}</p>' if note else ''
    c = action(cancel, 'ghost', cancel_href, 'cancel', 'min-h-16 text-title-1 font-medium' if large else '', focus=focus_cancel)
    k = action(confirm, variant, confirm_href, act, 'min-h-16 text-title-1 font-medium' if large else '')
    if stacked:
        btns = f'<div class="mt-6 flex flex-col gap-2">{k.replace("inline-flex", "flex w-full")}{c.replace("inline-flex", "flex w-full")}</div>'
    else:
        btns = f'<div class="mt-6 flex flex-wrap justify-end gap-3">{c}{k}</div>'
    return f'''{scrim()}
  <div class="absolute inset-0 z-40 flex items-center justify-center px-6">
    <div class="w-full max-w-sm rounded-dialog bg-popover p-6 shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="{t}" aria-describedby="{d}">
      <h2 id="{t}" class="{tcls}">{title}</h2>
      <div id="{d}" class="mt-2 space-y-2 {bcls} text-muted-foreground">{paras}</div>{n}{extra}
      {btns}
    </div>
  </div>'''


def ios_sheet(title, message, actions_, cancel='Cancel', cancel_href=None):
    """iOS action sheet. actions_ = [(label, destructive, href, act)]"""
    t = uid('t')
    head = ''
    if title or message:
        tt = f'<p id="{t}" class="text-body-sm font-semibold text-muted-foreground">{title}</p>' if title else ''
        mm = f'<p class="mt-1 text-body-sm text-muted-foreground">{message}</p>' if message else ''
        head = f'<div class="px-6 pb-3 pt-4 text-center">{tt}{mm}</div>'
    acts = ''
    for lab, destr, href, act in actions_:
        col = 'text-destructive' if destr else 'text-primary'
        tag_open = f'<a href="{href}"' if href else '<button type="button"'
        tag_close = '</a>' if href else '</button>'
        acts += f'{tag_open} class="flex min-h-14 w-full items-center justify-center border-t px-4 text-center text-title-3 font-normal {col}" data-action="{act}">{lab}{tag_close}'
    ch = f'<a href="{cancel_href}"' if cancel_href else '<button type="button"'
    cc = '</a>' if cancel_href else '</button>'
    lab = f' aria-labelledby="{t}"' if title else f' aria-label="{message[:60]}"'
    return f'''{scrim()}
  <div class="absolute inset-x-2 bottom-2 z-40 space-y-2" role="alertdialog" aria-modal="true"{lab}>
    <div class="overflow-hidden rounded-dialog bg-popover shadow-dialog">{head}{acts}</div>
    {ch} class="flex h-14 w-full items-center justify-center rounded-dialog bg-popover text-title-3 text-primary shadow-dialog" data-action="cancel">{cancel}{cc}
  </div>'''


def ios_alert(title, message, buttons, vertical=False):
    """buttons = [(label, style, href, act)] style: 'cancel' | 'default' | 'destructive'"""
    t, d = uid('t'), uid('d')
    out = []
    for lab, style, href, act in buttons:
        col = {'cancel': 'text-primary font-semibold', 'default': 'text-primary', 'destructive': 'text-destructive'}[style]
        o = f'<a href="{href}"' if href else '<button type="button"'
        c = '</a>' if href else '</button>'
        b = 'border-t' + ('' if vertical else ' first:border-r-0')
        out.append(f'{o} class="flex min-h-12 flex-1 items-center justify-center px-3 text-center text-body {col}" data-action="{act}">{lab}{c}')
    if vertical:
        btns = ''.join(f'<div class="flex border-t">{x.replace("flex-1", "w-full")}</div>' for x in out)
    else:
        btns = f'<div class="flex divide-x border-t">{"".join(out)}</div>'
    return f'''{scrim('z-30', 'bg-scrim/40')}
  <div class="absolute inset-x-12 top-1/2 z-40 -translate-y-1/2 overflow-hidden rounded-dialog bg-popover text-center shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="{t}" aria-describedby="{d}">
    <div class="px-4 pb-4 pt-5"><h2 id="{t}" class="text-body font-semibold">{title}</h2><p id="{d}" class="mt-1 text-body-sm text-muted-foreground">{message}</p></div>
    {btns}
  </div>'''


def snackbar(text, act=None, href=None, kind='status', ic=None, pos='bottom-24', large=False, two_line=False):
    i = icon(ic, 'size-8' if large else 'size-5', 'shrink-0') if ic else ''
    tcls = 'text-title-1 font-normal' if large else 'text-body-sm'
    if act:
        acls = f'-my-1 inline-flex h-12 shrink-0 items-center rounded-sm px-3 {"min-h-16 text-title-1" if large else "text-label"} text-primary-inverse'
        a = f'<a href="{href}" class="{acls}" data-action="{act.lower().replace(" ", "-")}">{act}</a>' if href else f'<button type="button" class="{acls}" data-action="{act.lower().replace(" ", "-")}">{act}</button>'
    else:
        a = ''
    if two_line and act:
        return (f'<div class="absolute inset-x-4 {pos} z-20 rounded-control bg-foreground py-3 pl-4 pr-1.5 text-background shadow-overlay" role="{kind}">'
                f'<div class="flex gap-3 pr-2.5">{i}<span class="flex-1 {tcls}">{text}</span></div><div class="mt-1 flex justify-end">{a.replace("-my-1 ", "")}</div></div>')
    pad = 'py-1.5 pl-4 pr-1.5' if act else 'px-4 py-3'
    return f'<div class="absolute inset-x-4 {pos} z-20 flex min-h-12 items-center gap-3 rounded-control bg-foreground {pad} text-background shadow-overlay" role="{kind}">{i}<span class="flex-1 {tcls}">{text}</span>{a}</div>'


def offline_banner(text, web=False):
    return f'<div class="flex shrink-0 items-center gap-2 bg-muted px-gutter py-2 text-body-sm" role="status">{icon("wifi-off", "size-4", "shrink-0")}<span class="flex-1">{text}</span></div>'


def scr(*parts, cls=''):
    """Content for a .screen where background + overlays are siblings (screen is position relative)."""
    return ''.join(parts)


def frame_android(*parts):
    return phone(''.join(parts))


def frame_ios(*parts):
    return phone(''.join(parts), ios=True)


# ================================================================ SECTION: dialogs
P.section('Dialogs: destructive and consequential confirmations',
          'AlertDialog over the screen that opens it. Title names the object as a question; the body states the consequence and what stays safe; buttons are a specific verb and Cancel (or Keep …). Destructive variant when something is deleted, discarded or someone loses access; primary when the change is consequential but nothing is lost. Exact strings and the screens that open each dialog are in the spec, §4 and §6.')

P.add('S40-default', 'Delete list (solo): the reference dialog', frame_android(
    bg_s09_solo(),
    dialog('Delete “Trip ideas”?',
           '30 items, Round 1 and your decisions will be deleted from your account and this phone. trip-ideas.csv isn\'t changed.',
           'Cancel', 'Delete list', cancel_href='S09-list-overview.html#S09-default', confirm_href='S10-list-management.html#S10-deleted-snackbar', act='confirm-delete')),
    'Delete list (solo)')

P.add('S40-delete-list-shared', 'Delete list (shared): Delete for everyone', frame_android(
    bg_s09_shared(),
    dialog('Delete “Wedding guests” for everyone?',
           "Mert and Selin lose access. All 100 items, every member's decisions and notes, and Round 1 are deleted for all 3 members. Your contacts and mert-family.csv aren't changed.",
           'Cancel', 'Delete for everyone', cancel_href='S09-list-overview.html#S09-shared', confirm_href='S10-list-management.html#S10-deleted-snackbar', act='confirm-delete',
           note='To stop taking part without deleting it for others, <a href="S34-members.html#S34-transfer-pick" class="text-primary underline underline-offset-4">make someone else the Owner</a> and leave.')),
    'Delete list (shared)')

P.add('S40-delete-archived', 'Delete an archived list', frame_android(
    bg_s10_archived(),
    dialog('Delete “Book club picks” forever?',
           '12 items, Round 1 and your decisions will be deleted from your account. Nothing outside SwipeSort is changed.',
           'Cancel', 'Delete forever', cancel_href='S10-list-management.html#S10-archived', confirm_href='S10-list-management.html#S10-deleted-snackbar', act='confirm-delete')),
    'Delete archived list')

P.add('S40-archive-shared', 'Archive a shared list for everyone', frame_android(
    bg_s09_shared(),
    dialog('Archive “Wedding guests” for everyone?',
           'Mert and Selin can still open it, but nobody can sort, add items or change decisions until you restore it. Nothing is deleted.',
           'Cancel', 'Archive list', variant='primary', cancel_href='S09-list-overview.html#S09-shared', confirm_href='S10-list-management.html#S10-archived-snackbar', act='confirm-archive')),
    'Archive shared list')

P.add('S40-leave-list', 'Leave list (Collaborator)', frame_android(
    bg_s09_shared(role='Collaborator'),
    dialog('Leave “Wedding guests”?',
           ["You won't see this list anymore. Your 43 decisions stay and still count toward the list status. Items you haven't decided stop waiting for you, and your private notes are deleted.",
            'To come back, ask Deniz for a new invite.'],
           'Cancel', 'Leave list', cancel_href='S09-list-overview.html#S09-shared', confirm_href='S10-list-management.html#S10-left-snackbar', act='confirm-leave')),
    'Leave list')

P.add('S40-leave-owner', 'Leave list as Owner: transfer first', frame_android(
    bg_s34(),
    dialog('Choose a new Owner first',
           '“Wedding guests” needs an Owner. Make another member the Owner, then you can leave. To remove the list for everyone, delete it instead.',
           'Cancel', 'Choose new Owner', variant='primary', cancel_href='S34-members.html#S34-default', confirm_href='S34-members.html#S34-transfer-pick', act='choose-owner')),
    'Owner leaving')

remove_extra = '''
      <div class="mt-4 space-y-1" role="radiogroup" aria-label="Selin's decisions">
        <button type="button" role="radio" aria-checked="true" class="flex min-h-12 w-full items-start gap-3 rounded-control py-2 text-left"><span class="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary" aria-hidden="true"><span class="size-3 rounded-full bg-primary"></span></span><span><span class="block text-body">Keep Selin's decisions</span><span class="block text-body-sm text-muted-foreground">They still count toward Agreed, Pending and Conflict.</span></span></button>
        <button type="button" role="radio" aria-checked="false" class="flex min-h-12 w-full items-start gap-3 rounded-control py-2 text-left"><span class="mt-0.5 size-6 shrink-0 rounded-full border-2 border-input" aria-hidden="true"></span><span><span class="block text-body">Discard Selin's decisions</span><span class="block text-body-sm text-muted-foreground">Item statuses are recalculated without them.</span></span></button>
      </div>'''
P.add('S40-remove-member', 'Remove member, keep or discard decisions (DM-17)', frame_android(
    bg_s34(),
    dialog('Remove Selin from “Wedding guests”?',
           "Selin can't open the list anymore. Choose what happens to Selin's 43 decisions.",
           'Cancel', 'Remove Selin', extra=remove_extra, cancel_href='S34-members.html#S34-default', confirm_href='S34-members.html#S34-removed', act='confirm-remove')),
    'Remove member')

P.add('S40-transfer-ownership', 'Transfer ownership', frame_android(
    bg_s34(),
    dialog('Make Mert the Owner?',
           ["Mert will manage members, rounds and the conflict rule, and can rename or delete the list.",
            "You'll stay on the list as a Collaborator. Only Mert can make you the Owner again."],
           'Cancel', 'Make Mert Owner', variant='primary', cancel_href='S34-members.html#S34-default', confirm_href='S34-members.html#S34-transferred', act='confirm-transfer')),
    'Transfer ownership')

P.add('S40-end-round', 'End round (solo), from the sorting menu', frame_android(
    bg_s25(name='Trip ideas', total=30, decided=12, cnt=(6, 1, 5), photo=True),
    dialog('End Round 1?',
           "18 items aren't decided yet. Your 12 decisions are kept, and you can continue Round 1 from the summary until you start a new round.",
           'Cancel', 'End Round 1', variant='primary', cancel_href='S25-sorting.html#S25-photo', confirm_href='S27-round-summary.html#S27-ended-early', act='confirm-end-round')),
    'End round (solo)')

P.add('S40-end-round-shared', 'End round (shared, Owner): for everyone', frame_android(
    bg_s25(shared=True),
    dialog('End Round 1 for everyone?',
           ['Mert and Selin are still sorting. Decisions made so far are kept, and items nobody decided stay undecided.',
            'Everyone sees the round summary.'],
           'Cancel', 'End Round 1', variant='primary', cancel_href='S25-sorting.html#S25-shared', confirm_href='S27-round-summary.html#S27-ended-early', act='confirm-end-round')),
    'End round (shared)')

P.add('S40-new-round', 'Start a new round while one is open (A-34, solo)', frame_android(
    bg_s24(),
    dialog('End Round 1 and start Round 2?',
           "18 items in Round 1 aren't decided yet. Your decisions so far are kept. Round 2 starts with 5 items.",
           'Cancel', 'End Round 1 and start', variant='primary', cancel_href='S24-start-round.html#S24-maybe', confirm_href='S24-start-round.html#S24-started', act='confirm-end-round')),
    'New round while one is open')

P.add('S40-new-round-shared', 'Start a new round while one is open (shared, Owner)', frame_android(
    bg_s24(shared=True),
    dialog('End Round 1 for everyone and start Round 2?',
           ['Mert and Selin are still sorting. Decisions made so far are kept, and items nobody decided stay undecided.',
            'Round 2 starts for all 3 members with 6 items.'],
           'Cancel', 'End Round 1 and start', variant='primary', cancel_href='S24-start-round.html#S24-round-in-progress', confirm_href='S25-sorting.html#S25-shared', act='confirm-end-round')),
    'New round while one is open (shared)')

P.add('S40-discard-import', 'Discard import', frame_android(
    bg_s13(),
    dialog('Discard import?',
           'Your selection of 88 contacts will be lost. Nothing has been added to SwipeSort yet.',
           'Keep importing', 'Discard import', cancel_href='S13-contacts-import.html#S13-select-default', confirm_href='S08-home.html#S08-default', act='discard')),
    'Discard import')

def bg_s16():
    lines = ['The Overstory', 'Piranesi', 'Klara and the Sun', 'Tomorrow, and Tomorrow, and Tomorrow', 'Lessons in Chemistry', 'The Midnight Library']
    txt = ''.join(f'<span class="block">{l}</span>' for l in lines)
    body = f'''{stepper("Select items", 2, 4)}
    <div class="min-h-0 flex-1 overflow-hidden px-4"><div class="space-y-3">
      <div class="flex rounded-full bg-secondary p-1"><span class="flex h-10 flex-1 items-center justify-center rounded-full bg-card text-label shadow-raised">Text</span><span class="flex h-10 flex-1 items-center justify-center text-label text-muted-foreground">Preview</span></div>
      <div class="rounded-control border border-input bg-card px-3.5 py-3 text-body">{txt}</div>
      <p class="px-1 text-body-sm text-muted-foreground">6 items. One item per line.</p>
      {fake_btn("Choose a .txt file", "outline", "file-text")}
    </div></div>
    <div class="shrink-0 px-gutter pb-4 pt-3">{fake_btn("Continue", extra="h-14")}</div>'''
    return bg(top_bar('x', 'Import', 'Plain text'), body)


P.add('S40-replace-text', 'Replace typed text with a chosen file', frame_android(
    bg_s16(),
    dialog('Replace the text in the box?',
           'The 6 lines you typed are replaced by book-club.txt.',
           'Cancel', 'Replace', cancel_href='S16-plain-text.html#S16-default', confirm_href='S16-plain-text.html#S16-default', act='confirm-replace')),
    'Replace typed text')

P.add('S40-discard-add-items', 'Discard adding items', frame_android(
    bg_s21(),
    dialog('Discard adding items?',
           'Your choices for mert-family.csv will be lost. Nothing has been added to Wedding guests yet.',
           'Keep adding', 'Discard', cancel_href='S21-add-items.html#S21-default', confirm_href='S09-list-overview.html#S09-shared', act='discard')),
    'Discard adding items')

P.add('S40-discard-template', 'Discard template changes', frame_android(
    bg_s23(),
    dialog('Discard changes to “Candidate, compact”?',
           "Your layout changes won't be saved. Frontend hiring, Q4 keeps the current layout.",
           'Keep editing', 'Discard changes', cancel_href='S23-template-editor.html#S23-default', confirm_href='S22-template-library.html#S22-default', act='discard')),
    'Discard template changes')

P.add('S40-discard-edits', 'Discard item edits', frame_android(
    bg_s26('edit'),
    dialog('Discard changes to Gökhan Doğan?',
           "Your edits won't be saved. The item keeps its current values.",
           'Keep editing', 'Discard changes', cancel_href='S26-item-detail.html#S26-edit', confirm_href='S26-item-detail.html#S26-default', act='discard')),
    'Discard item edits')

tpl_extra = f'''
      <div class="mt-4"><p class="text-label" id="tplrep">Card template for Wedding guests</p><button type="button" class="mt-1.5 flex h-12 w-full items-center gap-2 rounded-control border border-input bg-card px-3.5 text-left text-body" aria-haspopup="listbox" aria-label="Card template for Wedding guests: Person"><span class="min-w-0 flex-1 truncate">Person</span>{icon("chevron-down", "size-5", "text-muted-foreground")}</button><p class="mt-1.5 text-caption text-muted-foreground">Person is the template it was based on.</p></div>'''
P.add('S40-delete-template', 'Delete a template in use: choose a replacement', frame_android(
    bg_s22(),
    dialog('Delete “Guest with table side”?',
           'Wedding guests uses this template. Its cards switch to the template you choose, for every member of the list.',
           'Cancel', 'Delete template', extra=tpl_extra, cancel_href='S22-template-library.html#S22-default', confirm_href='S22-template-library.html#S22-deleted', act='confirm-delete')),
    'Delete template')

P.add('S40-revert-field', 'Revert an edited field', frame_android(
    bg_s26('edited'),
    dialog('Revert City to the original?',
           'City goes back to “İstanbul”, the value from Contacts. Your edit “Ankara” is removed.',
           'Cancel', 'Revert', cancel_href='S26-item-detail.html#S26-edited', confirm_href='S26-item-detail.html#S26-reverted', act='confirm-revert')),
    'Revert field')

P.add('S40-delete-note', 'Delete note', frame_android(
    bg_s26('note'),
    dialog('Delete your note?',
           '“Flying in from Berlin. Ask about dates first.” will be deleted from this item.',
           'Cancel', 'Delete note', cancel_href='S26-item-detail.html#S26-long-text', confirm_href='S26-item-detail.html#S26-long-text', act='confirm-delete')),
    'Delete note')

P.add('S40-remove-field', 'Remove a field that has values (manual entry)', frame_android(
    bg_s17(),
    dialog('Remove Price (€)?',
           '3 items have a value in Price (€). The values are removed with the field.',
           'Cancel', 'Remove field', cancel_href='S17-manual-entry.html#S17-default', confirm_href='S17-manual-entry.html#S17-default', act='confirm-remove')),
    'Remove field')

P.add('S40-reset-invite-link', 'Reset invite link', frame_android(
    bg_s31(),
    dialog('Reset the invite link?',
           "The current link stops working right away. Members who already joined stay. Share the new link with anyone who hasn't joined yet.",
           'Cancel', 'Reset link', cancel_href='S31-invite.html#S31-default', confirm_href='S31-invite.html#S31-reset-done', act='confirm-reset')),
    'Reset invite link')

rule_extra = f'''
      <ul class="mt-4 space-y-3 rounded-control bg-secondary p-3 text-body-sm">
        <li><span class="block text-label">8 become final now</span><span class="mt-1.5 flex flex-wrap gap-1.5">{chip('Reject 1', 'x', 'bg-reject-soft text-reject-soft-foreground')}{chip('Maybe 1', 'circle-help', 'bg-maybe-soft text-maybe-soft-foreground')}{chip('Accept 6', 'check', 'bg-accept-soft text-accept-soft-foreground')}</span></li>
        <li><span class="block text-label">7 stay open</span><span class="block text-muted-foreground">They wait for the last member to decide. Ties go to Mert.</span></li>
      </ul>'''
P.add('S40-change-conflict-rule', 'Change conflict rule', frame_android(
    bg_s35(),
    dialog('Switch to Majority decides?',
           '8 of 15 conflicts get a final decision right away. Members are notified.',
           'Cancel', 'Switch to Majority', variant='primary', extra=rule_extra, cancel_href='S35-conflict-rule.html#S35-default', confirm_href='S35-conflict-rule.html#S35-switched', act='confirm-rule')),
    'Change conflict rule')

P.add('S40-disconnect-google', 'Disconnect Google', frame_android(
    bg_s07(),
    dialog('Disconnect Google?',
           "You'll sign in with deniz.yilmaz@example.com and your password instead. Your lists aren't affected.",
           'Cancel', 'Disconnect', cancel_href='S07-profile.html#S07-default', confirm_href='S07-profile.html#S07-google-disconnected', act='confirm-disconnect')),
    'Disconnect Google')

P.add('S40-sign-out', 'Sign out (everything backed up)', frame_android(
    bg_s06(),
    dialog('Sign out?',
           ["Lists backed up to deniz.yilmaz@example.com are removed from this phone until you sign in again.",
            "“Frontend hiring, Q4” stays on this phone, hidden until you sign in again."],
           'Cancel', 'Sign out', cancel_href='S06-settings.html#S06-default', confirm_href='S08-home.html#S08-first-run', act='confirm-sign-out')),
    'Sign out')

P.add('S40-sign-out-unsynced', 'Sign out with changes not backed up', frame_android(
    bg_s06(offline=True, paused=True),
    dialog('Sign out without backing up?',
           "12 changes haven't been backed up because you're offline. Signing out now removes them from this phone, and they can't be recovered.",
           'Cancel', 'Sign out anyway', cancel_href='S06-settings.html#S06-default', confirm_href='S08-home.html#S08-first-run', act='confirm-sign-out')),
    'Sign out, unsynced')

P.add('S40-delete-account', 'Delete account: the final confirmation', frame_android(
    bg_s07_confirm(),
    dialog('Delete your account?',
           ["This can't be undone. “Wedding guests” moves to Mert Aydın. Your other 4 lists (2 of them archived), your decisions and your notes are deleted.",
            "“Frontend hiring, Q4” is on this phone only. It stays on this phone, without an account."],
           'Cancel', 'Delete account', cancel_href='S07-profile.html#S07-delete-confirm', confirm_href='S07-profile.html#S07-deleting', act='confirm-delete-account')),
    'Delete account')

P.add('S40-dialog-large-text', 'Large text (200%): everything scales, actions stack', frame_android(
    bg_s09_solo_large(),
    dialog('Delete “Trip ideas”?',
           '30 items, Round 1 and your decisions will be deleted from your account and this phone. trip-ideas.csv isn\'t changed.',
           'Cancel', 'Delete list', stacked=True, large=True, cancel_href='S09-list-overview.html#S09-default', confirm_href='S10-list-management.html#S10-deleted-snackbar', act='confirm-delete')),
    'Large text')

# ================================================================ SECTION: iOS
P.section('iOS dialogs',
          'Same copy as Android. Action sheets for destructive actions the person just chose in context (delete, remove, sign out, discard); alerts when the person must read before deciding or nothing is destroyed (end round, unsynced sign-out). Cancel is always the separate bottom button of an action sheet.')

P.add('S40-ios-delete-list', 'iOS: delete list (action sheet)', frame_ios(
    bg_s09_solo(ios=True),
    ios_sheet('Delete “Trip ideas”?', '30 items, Round 1 and your decisions will be deleted from your account and this iPhone. trip-ideas.csv isn\'t changed.',
              [('Delete list', True, 'S10-list-management.html#S10-deleted-snackbar', 'confirm-delete')], cancel_href='S09-list-overview.html#S09-ios')),
    'Delete list')

P.add('S40-ios-remove-member', 'iOS: remove member (action sheet)', frame_ios(
    bg_s34(ios=True),
    ios_sheet('Remove Selin from “Wedding guests”?', "Selin can't open the list anymore. Kept decisions still count toward Agreed, Pending and Conflict.",
              [("Remove and keep Selin's decisions", True, 'S34-members.html#S34-removed', 'confirm-remove'),
               ("Remove and discard Selin's decisions", True, 'S34-members.html#S34-removed', 'confirm-remove-discard')])),
    'Remove member')

P.add('S40-ios-sign-out', 'iOS: sign out (action sheet)', frame_ios(
    bg_s06(ios=True),
    ios_sheet(None, "Lists backed up to deniz.yilmaz@example.com are removed from this iPhone until you sign in again. “Frontend hiring, Q4” stays on this iPhone, hidden until you sign in again.",
              [('Sign out', True, 'S08-home.html#S08-ios-first-run', 'confirm-sign-out')])),
    'Sign out')

P.add('S40-ios-sign-out-unsynced', 'iOS: sign out, changes not backed up (alert)', frame_ios(
    bg_s06(ios=True, offline=True, paused=True),
    ios_alert('Sign out without backing up?', "12 changes haven't been backed up because you're offline. Signing out now removes them from this iPhone, and they can't be recovered.",
              [('Sign out anyway', 'destructive', 'S08-home.html#S08-ios-first-run', 'confirm-sign-out'), ('Cancel', 'cancel', None, 'cancel')], vertical=True)),
    'Sign out, unsynced')

P.add('S40-ios-end-round', 'iOS: end round for everyone (alert)', frame_ios(
    bg_s25(shared=True, ios=True),
    ios_alert('End Round 1 for everyone?', 'Mert and Selin are still sorting. Decisions made so far are kept, and items nobody decided stay undecided. Everyone sees the round summary.',
              [('Cancel', 'cancel', None, 'cancel'), ('End Round 1', 'default', 'S27-round-summary.html#S27-ended-early', 'confirm-end-round')])),
    'End round')

P.add('S40-ios-discard-import', 'iOS: discard import (action sheet)', frame_ios(
    bg_s13(),
    ios_sheet(None, 'Your selection of 88 contacts will be lost. Nothing has been added to SwipeSort yet.',
              [('Discard import', True, 'S08-home.html#S08-ios', 'discard')], cancel='Keep importing')),
    'Discard import')

# ================================================================ SECTION: snackbars
P.section('Snackbars',
          'Inverse surface, one line or two, one action at most. 16 above the bottom navigation on tab screens, 16 above the decision bar while sorting, 16 above a pinned bottom button elsewhere. 4 s without an action, 6 s with one, never under 10 s with a screen reader running. One at a time: a new snackbar replaces the current one.')

P.add('S40-snackbar', 'Snackbar, plain, above the bottom navigation', frame_android(
    bg_s06(), snackbar('Feedback sent. Thanks for helping improve SwipeSort.')), 'Plain')

P.add('S40-snackbar-undo', 'Snackbar with Undo (commits when it closes)', frame_android(
    bg_s08(fab='bottom-40', exclude=('Trip ideas',)), snackbar('List deleted', 'Undo', 'S08-home.html#S08-default')), 'With Undo')

P.add('S40-snackbar-error', 'Snackbar, error with Try again', frame_android(
    bg_s08(fab='bottom-48'), snackbar("Couldn't archive “Wedding guests”. Check your connection and try again.", 'Try again', None, kind='alert', ic='circle-alert')), 'Error')

P.add('S40-snackbar-success-action', 'Snackbar, success with an action (no bottom bar)', frame_android(
    bg_s09_solo(name='Desk setup', items=20, round_items=6, decided=6, cnt=(2, 1, 3), src='manual entry', src_icon='pencil-line', round_label='Round 2 complete',
                button=('Start a new round', 'play'), template='Product',
                rows=[row('list-checks', 'Results', '8 accepted, 11 rejected, 1 maybe'), row('history', 'Rounds', '2 rounds'), row('layout-template', 'Card template', 'Product'), row('file-down', 'Export', 'CSV, Excel, Google Sheets or a text summary')]),
    snackbar('Duplicated as “Desk setup (copy)”', 'Open', 'S09-list-overview.html#S09-default', ic='circle-check', pos='bottom-4')), 'Success with action')

P.add('S40-snackbar-sorting', 'Snackbar above the decision bar (S25)', frame_android(
    bg_s25(shared=True, decided=77, cnt=(17, 12, 48)),
    snackbar('Mert chose Maybe on Mia Andersson. This is now a conflict.', 'View', 'S36-conflicts.html#S36-default', ic='git-compare-arrows', pos='bottom-32')), 'Above decision bar')

P.add('S40-snackbar-large-text', 'Snackbar at 200% text: action below the text', frame_android(
    bg_s08(fab=None), snackbar("Couldn't archive “Wedding guests”. Check your connection and try again.", 'Try again', None, kind='alert', ic='circle-alert', large=True, two_line=True)), 'Large text')

# ================================================================ SECTION: banners and sync
P.section('Offline banner and sync notice',
          'The offline banner sits directly under the app bar, full width, and stays as long as the device is offline. The sync notice is a quiet line in the list header (or the progress row while sorting) and is the only place sync is visible.')

saved_line = f'<p class="mt-3 inline-flex items-center gap-1.5 text-body-sm text-muted-foreground" role="status">{icon("cloud-off", "size-4", "shrink-0")}Saved on this phone</p>'
P.add('S40-offline', 'Offline banner + “Saved on this phone”', frame_android(
    bg_s09_shared(banner=offline_banner("You're offline. Decisions are saved on this phone. Inviting needs a connection."), sync_html=saved_line, as_html=True)),
    'Offline')

sync_line = f'<p class="mt-3 inline-flex items-center gap-1.5 text-body-sm text-muted-foreground" role="status">{icon("refresh-cw", "size-4", "shrink-0 animate-spin")}Syncing 12 decisions…</p>'
P.add('S40-sync-syncing', 'Sync notice: syncing after reconnecting', frame_android(
    bg_s09_shared(sync_html=sync_line, as_html=True)), 'Syncing')

synced_line = f'<p class="mt-3 inline-flex items-center gap-1.5 text-body-sm text-muted-foreground" role="status">{icon("cloud-check", "size-4", "shrink-0")}Synced</p>'
P.add('S40-sync-synced', 'Sync notice: synced (shown 4 s, then hides)', frame_android(
    bg_s09_shared(sync_html=synced_line, as_html=True)), 'Synced')

fail_alert = f'<div class="flex items-center gap-2 rounded-control border border-destructive/40 bg-card py-1 pl-3 pr-1" role="alert">{icon("circle-alert", "size-4", "shrink-0 text-destructive")}<span class="min-w-0 flex-1 text-body-sm">Couldn\'t sync 12 decisions. They\'re safe on this phone.</span><button type="button" class="inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label text-primary" data-action="retry-sync">Try again</button></div>'
P.add('S40-sync-failed', 'Sync notice: failed, with Try again', frame_android(
    bg_s09_shared(alert_html=fail_alert, as_html=True)), 'Sync failed')

P.add('S40-offline-sorting', 'Offline while sorting: banner + compact count', frame_android(
    bg_s25(shared=True, banner=offline_banner("You're offline. Decisions are saved on this phone."),
           status_html=f'<span class="inline-flex items-center gap-1.5 text-caption text-muted-foreground">{icon("cloud-off", "size-4")}4 not synced</span>')),
    'Offline, sorting')

# ================================================================ SECTION: backup per list (D-33)
P.section('Backup per list',
          'A signed-in Owner can keep a solo list on this phone only (A-132). Turning backup off deletes the copy in the account, so it is confirmed with a destructive dialog and needs a connection (A-134); on iOS it is an alert, because the person must read the consequence first. Turning it back on is never confirmed. Other devices of the same account remove the list at their next sync and say so once.')


def switch_html(on=True, disabled=False):
    op = ' opacity-50' if disabled else ''
    if on:
        return f'<span class="flex h-8 w-13 shrink-0 items-center rounded-full bg-primary p-1{op}"><span class="ml-auto size-6 rounded-full bg-primary-foreground"></span></span>'
    return f'<span class="flex h-8 w-13 shrink-0 items-center rounded-full border-2 border-input bg-muted p-1{op}"><span class="size-5 rounded-full bg-muted-foreground"></span></span>'


def backup_group_bg(on=True):
    desc = 'Backed up to deniz.yilmaz@example.com' if on else 'On this phone only'
    ic = 'cloud-check' if on else 'cloud-off'
    return group([f'<li class="flex min-h-16 items-center gap-4 px-4 py-3">{icon(ic, "size-5", "shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">Back up this list</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span>{switch_html(on)}</li>'], 'Backup')


BACKUP_OFF_BODY = "The copy in your account is deleted and the list leaves your other devices. If you lose this phone or move to a new one, the list can't be recovered."
P.add('S40-backup-off', 'Turn backup off for one list (A-134)', frame_android(
    bg_s09_solo(extra=backup_group_bg(True), shift='-translate-y-40'),
    dialog('Keep “Trip ideas” on this phone only?', BACKUP_OFF_BODY,
           'Cancel', 'Keep on this phone only', cancel_href='S09-list-overview.html#S09-default', confirm_href='S10-list-management.html#S10-backup-off-done', act='confirm-backup-off')),
    'Turn backup off')

P.add('S40-ios-backup-off', 'iOS: turn backup off (alert, stacked)', frame_ios(
    bg_s09_solo(ios=True, extra=backup_group_bg(True), shift='-translate-y-40'),
    ios_alert('Keep “Trip ideas” on this phone only?', BACKUP_OFF_BODY.replace('this phone or', 'this iPhone or'),
              [('Keep on this phone only', 'destructive', 'S10-list-management.html#S10-backup-off-done', 'confirm-backup-off'), ('Cancel', 'cancel', None, 'cancel')], vertical=True)),
    'iOS: turn backup off')

P.add('S40-outcome-device-only-elsewhere', 'Another device kept a list on that device only', frame_android(
    bg_s08(fab='bottom-48', exclude=('Trip ideas', 'Frontend hiring, Q4')),
    snackbar("You kept “Trip ideas” on another device only. It's no longer on this one.", None, None, ic='cloud-off')),
    'Kept on another device')

# ================================================================ SECTION: sync outcomes (D-09)
P.section('Sync outcomes',
          'When the server applies a queued change differently than this phone expected (D-09), the person hears about it once. Nothing was lost, or it can be put back: a snackbar that says what happened and leads to where it can be changed. The person\'s own work was not applied: an inline alert on the screen where it would have been (Home when the list itself is gone), which stays until dismissed. Never a dialog: there is nothing to confirm.')


def outcome_alert(ic, title, body, extra=''):
    return (f'<div class="flex items-start gap-3 rounded-control border bg-card py-3 pl-4 pr-1 {extra}" role="status">{icon(ic, "size-5", "mt-0.5 shrink-0 text-muted-foreground")}'
            f'<div class="min-w-0 flex-1 pb-1"><p class="text-label">{title}</p><p class="mt-0.5 text-body-sm text-muted-foreground">{body}</p></div>'
            f'<button type="button" class="-my-2 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Dismiss" data-action="dismiss">{icon("x", "size-5")}</button></div>')


P.add('S40-outcome-edit-replaced', 'A later edit by another member replaced mine (D-09 row 1)', frame_android(
    bg_s09_shared(),
    snackbar("Mert changed City on Alper Turan after you, so your edit was replaced.", 'View', 'S26-item-detail.html#S26-edit-replaced', ic='pencil-line', pos='bottom-4')),
    'Edit replaced')

SELIN_HOME = [('Wedding guests', 'users', 'Shared with 2', None, (0, '0 / 6'), True, 'S09-list-overview.html#S09-shared-collaborator')]
P.add('S40-outcome-late-round', 'Round 1 decisions synced after Round 2 started (D-09 row 2)', frame_android(
    bg_s08(fab='bottom-48', rows=SELIN_HOME, archived=False),
    snackbar('Deniz started Round 2 of “Wedding guests”. Your 8 decisions from Round 1 were saved.', 'Open', 'S09-list-overview.html#S09-shared-collaborator', ic='list-restart')),
    'Late Round 1 decisions')

removed_home = f'''<div class="shrink-0"><div class="flex h-app-bar items-center justify-end gap-1 px-1">{ib("search")}</div><h1 class="px-gutter pb-2 text-title-1">Lists</h1></div>
  <div class="shrink-0 px-4 pt-2">{outcome_alert("user-x", "You were removed from “Wedding guests”", "Deniz removed you while you were offline, so the 6 decisions you made since 9:24 weren't saved. To join again, ask Deniz for a new invite.")}</div>
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center px-8 pb-10 text-center" aria-hidden="true" inert>
    {icon("layers", "size-8", "text-muted-foreground")}<p class="mt-4 text-title-2">No lists yet</p>
    <p class="mt-2 max-w-xs text-body text-muted-foreground">Import a list to start sorting, or join one when someone shares it with you.</p>
    <span class="mt-6 w-full max-w-xs">{fake_btn("Import a list", "primary", "download")}</span>
  </div>
  <div aria-hidden="true" inert>{nav('lists', badge=0)}</div>'''
P.add('S40-outcome-removed', 'Removed from a list while offline: lands on Home (D-09 row 4)', frame_android(removed_home), 'Removed while offline')

P.add('S40-outcome-already-agreed', 'Resolutions dropped: members agreed first (D-09 row 5)', frame_android(
    bg_s09_shared(role='Decision Maker'),
    snackbar('Members agreed on 2 conflicts before your resolutions synced. Their agreement is final.', 'View', 'S36-conflicts.html#S36-list', ic='check-check', pos='bottom-4')),
    'Already agreed')

role_alert = outcome_alert('gavel', "You're no longer the Decision Maker", "Deniz made Selin the Decision Maker while you were offline, so your 5 resolutions weren't applied. Those conflicts are still open.")
P.add('S40-outcome-dm-role-lost', 'Resolutions rejected: the Decision Maker role moved (D-09 row 6)', frame_android(
    bg_s09_shared(role='Collaborator', who='mert', alert_html=role_alert, as_html=True)),
    'Role moved')

# ================================================================ SECTION: errors and not found
P.section('Error and not-found screens',
          'ErrorState fills the content area under the normal app bar, so back or close still works. Always: what happened, how to fix it, one action that fixes it and one way out. No codes, no apologies.')


def state_screen(icon_name, title, body, primary, secondary=None, p_href=None, s_href=None, bar_html=None, p_act='try-again', s_act='back', body2=None):
    b2 = f'<p class="mt-3 max-w-xs text-body-sm text-muted-foreground">{body2}</p>' if body2 else ''
    p = f'<a href="{p_href}" class="mt-6 flex h-12 w-full max-w-xs items-center justify-center rounded-control bg-secondary text-label-lg text-secondary-foreground" data-action="{p_act}">{primary}</a>' if p_href else f'<button type="button" class="mt-6 flex h-12 w-full max-w-xs items-center justify-center rounded-control bg-secondary text-label-lg text-secondary-foreground" data-action="{p_act}">{primary}</button>'
    s = ''
    if secondary:
        s = f'<a href="{s_href}" class="mt-2 flex h-12 w-full max-w-xs items-center justify-center rounded-control text-label-lg" data-action="{s_act}">{secondary}</a>' if s_href else f'<button type="button" class="mt-2 flex h-12 w-full max-w-xs items-center justify-center rounded-control text-label-lg" data-action="{s_act}">{secondary}</button>'
    return f'''{bar_html or ''}
  <div class="flex flex-1 flex-col items-center justify-center px-8 pb-16 text-center">
    {icon(icon_name, "size-8", "text-muted-foreground")}
    <h1 class="mt-4 text-title-3">{title}</h1>
    <p class="mt-1 max-w-xs text-body text-muted-foreground">{body}</p>{b2}
    {p}{s}
  </div>'''


def real_bar(lead='arrow-left', label='Back to lists', href='S08-home.html#S08-default', title=None):
    t = f'<h2 class="min-w-0 flex-1 truncate px-1 text-title-3">{title}</h2>' if title else '<span class="flex-1"></span>'
    return f'<header class="flex h-app-bar shrink-0 items-center gap-1 px-1"><a href="{href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{label}" data-action="back">{icon(lead, "size-6")}</a>{t}</header>'


P.add('S40-error', 'Generic error: content couldn\'t load', frame_android(state_screen(
    'cloud-alert', 'Wedding guests couldn\'t be loaded', 'SwipeSort didn\'t respond. Check your connection and try again.',
    'Try again', 'Back to lists', None, 'S08-home.html#S08-default', real_bar(),
    body2='Your decisions are saved on this phone.')), 'Couldn\'t load')

P.add('S40-error-unknown', 'Generic error: unexpected, with a report', frame_android(state_screen(
    'triangle-alert', 'This screen couldn\'t be opened', 'Your lists and decisions are safe. Try again. If it keeps happening, restart SwipeSort or send us a report.',
    'Try again', 'Send a report', None, 'S06-settings.html#S06-feedback', real_bar(), s_act='report')), 'Unexpected error')

P.add('S40-not-found', 'Not found: list link you can\'t open', frame_android(state_screen(
    'link-2-off', 'This list isn\'t available', 'It may have been deleted, or it\'s shared with a different account. You\'re signed in as deniz.yilmaz@example.com.',
    'Back to lists', 'Switch account', 'S08-home.html#S08-default', 'S03-sign-in.html#S03-default', real_bar(), p_act='back', s_act='switch-account')), 'List not available')

P.add('S40-not-found-deleted', 'Not found: list was deleted (seen by a member)', frame_android(state_screen(
    'trash-2', 'This list was deleted', 'Deniz deleted “Wedding guests” for everyone today. Its items, decisions and notes were deleted with it.',
    'Back to lists', None, 'S08-home.html#S08-default', None, real_bar(), p_act='back')), 'List deleted')

P.add('S40-not-found-removed', 'Not found: you were removed from the list', frame_android(state_screen(
    'user-x', 'You\'re no longer on Wedding guests', 'Deniz removed you from the list, so you can\'t open it anymore. To join again, ask Deniz for a new invite.',
    'Back to lists', None, 'S08-home.html#S08-default', None, real_bar(), p_act='back')), 'Removed from list')

P.add('S40-item-gone', 'Not found: item no longer exists', frame_android(state_screen(
    'file-x', 'This item isn\'t in the list anymore', 'Mert removed it from Wedding guests. Its decisions and notes were removed with it.',
    'Open Wedding guests', None, 'S09-list-overview.html#S09-shared', None, real_bar('arrow-left', 'Back', 'S38-activity.html#S38-default'), p_act='open-list')), 'Item gone')

update_body = f'''<div class="flex flex-1 flex-col px-gutter pb-4">
    <div class="flex flex-1 flex-col items-center justify-center text-center">
      {icon("circle-arrow-up", "size-8", "text-muted-foreground")}
      <h1 class="mt-4 text-title-2">Update SwipeSort to keep syncing</h1>
      <p class="mt-2 max-w-xs text-body text-muted-foreground">This version can't sync with your account anymore. Your lists and decisions are saved on this phone and sync after you update.</p>
      <p class="mt-3 max-w-xs text-body-sm text-muted-foreground">Until then you can keep sorting. Shared lists and backup wait for the update.</p>
    </div>
    <a href="https://swipesort.app/get" class="flex h-14 w-full items-center justify-center gap-2 rounded-control bg-primary text-label-lg text-primary-foreground" data-action="update">Update on Google Play</a>
    <a href="S08-home.html#S08-default" class="mt-2 flex h-12 w-full items-center justify-center rounded-control text-label-lg" data-action="not-now">Not now</a>
  </div>'''
P.add('S40-update-required', 'App update required (sync version too old)', frame_android(update_body), 'Update required')

# ================================================================ SECTION: desktop
P.section('Desktop browser',
          'The phone layout runs in a 412-wide column centered on a muted page. Nothing is placed outside the column. The column fills the window height; app bars and bottom bars stay pinned and only the middle scrolls.')


def chrome(url):
    return f'<div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">{url}</span></div>'


NEW_LIST_BTN = f'<a href="S11-source-picker.html#S11-web-desktop" class="mr-2 inline-flex h-12 items-center gap-2 rounded-control bg-primary px-4 text-label-lg text-primary-foreground" data-action="new-list">{icon("plus", "size-5")}New list</a>'
SEARCH_BTN = f'<a href="S08-home.html#S08-search" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Search lists" data-action="search">{icon("search", "size-6")}</a>'


def home_live(focus=True):
    """Web desktop Home (A-124: no FAB, New list in the app bar), same rows as S08."""
    return f'''<header class="shrink-0"><div class="flex h-app-bar items-center justify-end gap-1 px-1">{SEARCH_BTN}{NEW_LIST_BTN}</div><h1 class="px-gutter pb-2 text-title-1">Lists</h1></header>
  <div class="min-h-0 flex-1 overflow-hidden px-4 pt-2">{home_rows(live=True, focus=focus, exclude=('Frontend hiring, Q4',))}</div>
  {live_nav()}'''


def live_nav(active='lists', badge=2):
    out = []
    for key, ic, lab, href in [('lists', 'list-checks', 'Lists', 'S08-home.html#S08-default'), ('activity', 'activity', 'Activity', 'S38-activity.html#S38-default'), ('settings', 'settings', 'Settings', 'S06-settings.html#S06-default')]:
        on = key == active
        b = f'<span class="absolute right-3 top-0 flex h-5 min-w-5 items-center justify-center rounded-full bg-primary px-1 text-caption leading-none text-primary-foreground">{badge}</span>' if key == 'activity' and badge else ''
        pill = 'bg-primary-soft text-primary-soft-foreground' if on else ''
        cur = ' aria-current="page"' if on else ''
        al = f' aria-label="Activity, {badge} unread"' if key == 'activity' and badge else ''
        lab_html = f'<span class="font-semibold">{lab}</span>' if on else lab
        out.append(f'<a href="{href}" class="flex flex-1 flex-col items-center justify-center gap-1 text-caption {"" if on else "text-muted-foreground"}"{cur}{al}><span class="relative flex h-8 w-16 items-center justify-center rounded-full {pill}">{icon(ic, "size-6")}{b}</span>{lab_html}</a>')
    return f'<nav class="flex h-bottom-nav shrink-0 border-t bg-card" aria-label="Main">{"".join(out)}</nav>'


toast = f'''<div class="absolute bottom-24 right-4 z-40 flex w-80 items-start gap-3 rounded-control bg-popover p-3 shadow-overlay" role="status">
    <span class="flex size-10 shrink-0 items-center justify-center rounded-full bg-conflict text-conflict-foreground">{icon("git-compare-arrows", "size-5")}</span>
    <a href="S36-conflicts.html#S36-non-dm" class="min-w-0 flex-1 py-1" data-action="open-notification"><span class="block text-label">15 conflicts in Wedding guests</span><span class="block text-body-sm text-muted-foreground">Mert decides them.</span></a>
    <button type="button" class="-m-1.5 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Dismiss" data-action="dismiss">{icon("x", "size-4")}</button>
  </div>'''

P.add('S40-desktop-frame', 'Desktop: centered column, keyboard focus ring', f'''<div class="desktop">
  {chrome("swipesort.app")}
  <div class="desktop-column">
  {home_live()}
  </div>
</div>''', 'Desktop frame')

P.add('S40-web-toast', 'Web: in-app notification toast (no push on web)', f'''<div class="desktop">
  {chrome("swipesort.app")}
  <div class="desktop-column">
  {home_live(focus=False)}
  {toast}
  </div>
</div>''', 'In-app toast')

desk_dialog = dialog('Delete “Trip ideas”?',
                     '30 items, Round 1 and your decisions will be deleted from your account and every device. trip-ideas.csv isn\'t changed.',
                     'Cancel', 'Delete list', cancel_href='S09-list-overview.html#S09-default', confirm_href='S10-list-management.html#S10-deleted-snackbar', act='confirm-delete', focus_cancel=True)
P.add('S40-web-dialog', 'Web, desktop: dialog, focus starts on Cancel', f'''<div class="desktop">
  {chrome("swipesort.app/l/3fP9aD")}
  <div class="relative flex min-h-0 flex-1 flex-col">
  <div class="desktop-column">
  {bg_s09_solo()}
  </div>
  {desk_dialog}
  </div>
</div>''', 'Dialog on desktop')

wide_spacer = '<div class="flex h-0 shrink-0" aria-hidden="true"><span class="w-[800px] shrink-0"></span><span class="w-[412px] shrink-0"></span><span class="w-[800px] shrink-0"></span></div>'
P.add('S40-desktop-wide', 'Very wide window (2,012 px): column stays 412', f'''<div class="desktop w-auto">
  {wide_spacer}
  {chrome("swipesort.app/l/7Hq2xK/sort")}
  <div class="desktop-column">
  {s25_body(shared=True, kbd=True)}
  </div>
</div>''', 'Very wide window')

short_home = f'''<header class="shrink-0"><div class="flex h-app-bar items-center gap-1 pl-gutter pr-1"><h1 class="min-w-0 flex-1 text-title-3">Lists</h1>{SEARCH_BTN}{NEW_LIST_BTN}</div></header>
  <div class="relative h-96 shrink-0 overflow-hidden px-4 pt-1">{home_rows(live=True, exclude=('Frontend hiring, Q4',))}</div>
  {live_nav()}'''
P.add('S40-desktop-short', 'Short window (568 px high): bars stay pinned', f'''<div class="desktop h-auto">
  {chrome("swipesort.app")}
  <div class="desktop-column flex-none">
  {short_home}
  </div>
</div>''', 'Short window')

web404 = state_screen('map-pin-off', 'This page doesn\'t exist', 'Check the address, or go to your lists.', 'Go to your lists', None, 'S08-home.html#S08-web-desktop', None, p_act='go-home')
P.add('S40-web-not-found', 'Web: unknown address', f'''<div class="desktop">
  {chrome("swipesort.app/l/7Hq2xK/sorting")}
  <div class="desktop-column">
  {web404}
  </div>
</div>''', 'Web 404')

P.write(OUT)
