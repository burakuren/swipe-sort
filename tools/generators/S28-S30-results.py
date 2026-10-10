# Usage: python3 tools/generators/S28-S30-results.py
# Generates Group F mockups: S28 Results, S29 Filter and sort sheet, S30 Round history
# (design/03-screens/S28-results.html, S29-filter-sort.html, S30-round-history.html).
# Helpers come from group_e_common.py (shared markup with S24/S26/S27); data from 02-data/sample-data.json.
import sys, os, json, re, itertools
sys.path.insert(0, os.path.dirname(__file__))
from group_e_common import *  # noqa
from group_e_common import _strip_interactive

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCR = os.path.join(ROOT, 'design', '03-screens')
D = json.load(open(os.path.join(ROOT, 'design', '02-data', 'sample-data.json')))

P = {p['id']: p for p in D['products']}
C = {c['id']: c for c in D['contacts']}
SI = {i['itemId']: i for i in D['shared']['items']}
MY = D['shared']['myDecisions']
NOTES = D['shared']['notes']
EDITS = {e['itemId'] for e in D['shared']['edits']}
# Notes Deniz can see: shared notes of anyone + Deniz's own private notes.
VISIBLE_NOTES = {n['itemId'] for n in NOTES if not n['private'] or n['author'] == 'u-deniz'}

_uid = itertools.count(1)


def uid(p='g'):
    return f'{p}{next(_uid)}'


def fmt(n):
    return f'{n:,}'


# ------------------------------------------------------------------ Desk setup (solo, products)
R1 = D['productDecisions']['round1']
R2 = D['productDecisions']['round2']
LATEST = {k: R2.get(k, v) for k, v in R1.items()}  # A-33: latest decision per item
R2_ORDER = ['p15', 'p04', 'p18', 'p13', 'p07', 'p16']  # shuffled order of Round 2 (stored with the round)
# Recently decided first: Round 2 (newest last decided first), then Round 1 in reverse original order.
RECENT = list(reversed(R2_ORDER)) + [k for k in reversed(list(R1.keys())) if k not in R2]


def desk(dec):
    return [k for k in RECENT if LATEST[k] == dec]


DESK_ACC, DESK_MAY, DESK_REJ = desk('accept'), desk('maybe'), desk('reject')
assert (len(DESK_ACC), len(DESK_MAY), len(DESK_REJ)) == (8, 1, 11)


def price(pid):
    return f'€{fmt(P[pid]["price"])}'


def pmeta(pid):
    return f'{price(pid)}, {P[pid]["store"]}'


def thumb(pid, size='size-12'):
    return f'<img src="{IMG}products/{pid}.svg" alt="" class="{size} shrink-0 rounded-sm bg-muted object-cover">'


# ------------------------------------------------------------------ Wedding guests (shared, contacts)
MEMBERS = (('u-deniz', 'deniz', 'You'), ('u-mert', 'mert', 'Mert'), ('u-selin', 'selin', 'Selin'))
PAST = {'accept': 'accepted', 'reject': 'rejected', 'maybe': 'chose Maybe'}


def initials(name):
    w = [t for t in re.sub(r'\([^)]*\)', '', name).split() if not t.endswith('.')]
    return w[0][0] + w[-1][0] if len(w) > 1 else w[0][0]


def cav(cid, size='size-10'):
    c = C[cid]
    ph = c['photo'].replace('images/', '') if c.get('photo') else None
    return avatar((ph, initials(c['name'])), size)


def cmeta(cid):
    c = C[cid]
    return f'{c["side"]}, {c["relationship"]}, {c["city"]}'


def who_text(decs):
    groups = {}
    for m, _, name in MEMBERS:
        groups.setdefault(decs[m] or 'none', []).append(name)
    parts = []
    for key, names in groups.items():
        n = ' and '.join(names) if len(names) < 3 else f'{names[0]}, {names[1]} and {names[2]}'
        if key == 'none':
            plural = len(names) > 1 or names == ['You']
            parts.append(f"{n} {'haven' if plural else 'hasn'}'t decided")
        else:
            parts.append(f'{n} {PAST[key]}')
    return ', '.join(parts)


def waiting_text(decs):
    names = [name.lower() if name == 'You' else name for m, _, name in MEMBERS if decs[m] is None]
    if len(names) == 1:
        return f'Waiting for {names[0]}'
    return f'Waiting for {", ".join(names[:-1])} and {names[-1]}'


def parts_html(parts):
    """parts: list of (icon name, icon color class, text). Each part stays together; parts wrap."""
    out = ''.join(f'<span class="inline-flex items-center gap-1">{icon(ic, f"size-4 shrink-0 {cls}")}{t}</span>' for ic, cls, t in parts)
    return f'<!-- Proposed component: MemberDecisionsText --><span class="flex flex-wrap gap-x-2.5 gap-y-0.5">{out}</span>'


def who_parts(decs, pending=False):
    groups = {}
    for m, _, name in MEMBERS:
        groups.setdefault(decs[m] or 'none', []).append(name)
    parts = []
    for key, names in groups.items():
        n = ' and '.join(names) if len(names) < 3 else f'{names[0]}, {names[1]} and {names[2]}'
        if key == 'none':
            if pending:
                parts.append(('clock', 'text-muted-foreground', waiting_text(decs)))
            else:
                plural = len(names) > 1 or names == ['You']
                parts.append(('circle-dashed', 'text-muted-foreground', f"{n} {'haven' if plural else 'hasn'}'t decided"))
        else:
            parts.append((DEC[key][0], f'text-{key}-soft-foreground', f'{n} {PAST[key]}'))
    return parts_html(parts)


def mdots(decs):
    out = ''
    for m, key, _ in MEMBERS:
        v = decs[m]
        if v:
            dot = f'<span class="absolute -bottom-0.5 -right-0.5 flex size-4 items-center justify-center rounded-full bg-{v} text-{v}-foreground ring-2 ring-background">{icon(DEC[v][0], "size-3")}</span>'
        else:
            dot = f'<span class="absolute -bottom-0.5 -right-0.5 flex size-4 items-center justify-center rounded-full bg-background text-muted-foreground ring-2 ring-background">{icon("circle-dashed", "size-3")}</span>'
        out += f'<span class="relative shrink-0">{avatar(key, "size-8", "ring-2 ring-background")}{dot}</span>'
    return f'<span class="flex shrink-0 -space-x-2" aria-hidden="true">{out}</span>'


ORDER = 'ABCÇDEFGĞHIİJKLMNOÖPQRSŞTUÜVWXYZ'


def trkey(s):
    out = []
    for ch in s:
        u = {'i': 'İ', 'ı': 'I'}.get(ch, ch.upper())
        out.append(ORDER.index(u) if u in ORDER else 100 + ord(u))
    return out


ALL_IDS = [i['itemId'] for i in D['shared']['items']]
MY_ACC = [k for k in reversed(ALL_IDS) if MY.get(k) == 'accept']  # recently decided first
FINAL = {k: SI[k]['finalDecision'] for k in ALL_IDS}
STATUS = {k: SI[k]['status'] for k in ALL_IDS}
F_ACC = [k for k in reversed(ALL_IDS) if STATUS[k] == 'agreed' and FINAL[k] == 'accept']
CONF = [k for k in reversed(ALL_IDS) if STATUS[k] == 'conflict']
PEND = [k for k in ALL_IDS if STATUS[k] == 'pending']
PEND_ME = [k for k in PEND if SI[k]['decisions']['u-deniz'] is None]
PEND_SORTED = PEND_ME + [k for k in PEND if k not in PEND_ME]  # "Waiting for you" first
assert (len(MY_ACC), len(F_ACC), len(CONF), len(PEND)) == (48, 22, 15, 53)
# After Mert's bulk resolve (S37): Mert's own decision becomes final on the conflicts he decided.
RESOLVED = {k: SI[k]['decisions']['u-mert'] for k in CONF if SI[k]['decisions']['u-mert']}
assert len(RESOLVED) == 12
RES_ACC = [k for k in CONF if RESOLVED.get(k) == 'accept']
RES_REJ = [k for k in CONF if RESOLVED.get(k) == 'reject']


def cval(k, field):
    c, s = C[k], SI[k]
    return {
        'side': c['side'], 'rel': c['relationship'], 'city': c['city'], 'status': s['status'],
        'mert': s['decisions']['u-mert'] or 'none', 'selin': s['decisions']['u-selin'] or 'none',
        'note': k in VISIBLE_NOTES, 'edited': k in EDITS,
    }[field]


def facet(items, filters, field, value, getter):
    """Count of items matching every filter except `field`, plus field == value."""
    n = 0
    for k in items:
        if all(getter(k, f) in vs for f, vs in filters.items() if f != field) and getter(k, field) == value:
            n += 1
    return n


def matching(items, filters, getter):
    return [k for k in items if all(getter(k, f) in vs for f, vs in filters.items())]


WED_FILTER = {'side': {"Groom's"}, 'rel': {'Friend'}}
WED_12 = matching(MY_ACC, WED_FILTER, cval)
assert len(WED_12) == 12


# ------------------------------------------------------------------ shared building blocks
SEG_IC = {'accept': 'check', 'maybe': 'circle-help', 'reject': 'x', 'conflict': 'git-compare-arrows', 'pending': 'clock', 'none': 'circle-dashed'}
DESK_SEGS = [('accept', 'Accept', 8), ('maybe', 'Maybe', 1), ('reject', 'Reject', 11)]
FINAL_SEGS = [('accept', 'Accept', 22), ('maybe', 'Maybe', 6), ('reject', 'Reject', 4), ('conflict', 'Conflicts', 15), ('pending', 'Pending', 53)]
MINE_SEGS = [('accept', 'Accept', 48), ('maybe', 'Maybe', 11), ('reject', 'Reject', 17), ('none', 'Not decided', 24)]


def seg_bar(segs, selected, shift='', links=None, large=False, label='Decisions', pinned=False):
    links = links or {}
    tabs = ''
    for key, lab, n in segs:
        on = key == selected
        cls = 'bg-foreground text-background' if on else 'bg-secondary text-secondary-foreground'
        cnt = 'tabular-nums' if on else 'tabular-nums text-muted-foreground'
        h = 'h-12 px-4 text-title-3 font-normal' if large else 'h-10 px-3 text-label'
        inner = f'{icon(SEG_IC[key], "size-5" if large else "size-4")}{lab} <span class="{cnt}">{fmt(n)}</span>'
        attrs = f'role="tab" aria-selected="{"true" if on else "false"}" class="inline-flex shrink-0 items-center gap-1.5 rounded-full {h} {cls}"'
        href = links.get(key)
        tabs += f'<a href="{href}" {attrs}>{inner}</a>' if href else f'<button type="button" {attrs}>{inner}</button>'
    pin = ' relative z-10 border-b bg-background' if pinned else ''
    return f'<div class="shrink-0 overflow-hidden py-1{pin}"><div class="flex gap-2 px-gutter {shift}" role="tablist" aria-label="{label}">{tabs}</div></div>'


def search_field(placeholder, query=None, label='Search', focused=False, large=False, clear_href=None):
    ring = ' ring-2 ring-ring/30' if focused else ''
    val = f' value="{query}"' if query else ''
    h = 'h-14 text-title-3 font-normal' if large else 'h-12 text-body'
    clear = ''
    if query:
        cl = f'href="{clear_href}"' if clear_href else ''
        tag = 'a' if clear_href else 'button'
        typ = '' if clear_href else ' type="button"'
        clear = f'<{tag} {cl}{typ} class="absolute right-0 top-0 flex size-12 items-center justify-center rounded-full" aria-label="Clear search" data-action="clear-search">{icon("x", "size-5 text-muted-foreground")}</{tag}>'
    top = 'top-4' if large else 'top-3.5'
    return f'<div class="relative">{icon("search", f"pointer-events-none absolute left-3.5 {top} size-5 text-muted-foreground")}<input type="search" aria-label="{label}" placeholder="{placeholder}"{val} class="{h} w-full rounded-full border-0 bg-secondary pl-11 pr-12 placeholder:text-muted-foreground{ring}">{clear}</div>'


def tool_chip(text, ic, href, action, active=False, count=None, trailing=None, large=False):
    if active:
        cls = 'border border-primary bg-primary-soft text-primary-soft-foreground'
    else:
        cls = 'border border-input'
    h = 'h-12 px-4 text-title-3 font-normal' if large else 'h-9 px-3 text-label'
    cnt = f'<span class="flex h-5 min-w-5 items-center justify-center rounded-full bg-primary px-1.5 text-caption tabular-nums text-primary-foreground">{count}</span>' if count else ''
    tr = icon(trailing, 'size-4') if trailing else ''
    return f'<a href="{href}" class="inline-flex shrink-0 items-center gap-1.5 rounded-full {h} {cls}" data-action="{action}">{icon(ic, "size-4")}{text}{cnt}{tr}</a>'


def applied_chip(text, aria, large=False):
    h = 'h-12 pl-4 pr-3 text-title-3 font-normal' if large else 'h-9 pl-3 pr-2 text-label'
    return f'<!-- Proposed component: AppliedFilterChip --><button type="button" class="inline-flex shrink-0 items-center gap-1.5 rounded-full bg-secondary {h} text-secondary-foreground" aria-label="Remove filter: {aria}" data-action="remove-filter">{text}{icon("x", "size-4")}</button>'


def toolbar(placeholder, query=None, filter_href='S29-filter-sort.html#S29-products', sort_href='S29-filter-sort.html#S29-sort',
            sort_label='Recently decided', n_filters=0, applied=(), focused=False, chips=True, label='Search', clear_href=None):
    chip_row = ''
    if chips:
        fc = tool_chip('Filter', 'sliders-horizontal', filter_href, 'filter', active=n_filters > 0, count=n_filters or None)
        sc = tool_chip(sort_label, 'arrow-up-down', sort_href, 'sort', trailing='chevron-down')
        ap = ''.join(applied_chip(t, a) for t, a in applied)
        wrap = ' flex-wrap gap-y-3' if ap else ''
        chip_row = f'<div class="overflow-hidden"><div class="flex gap-2 px-gutter pb-3 pt-3{wrap}">{fc}{sc}{ap}</div></div>'
    return f'''<div class="shrink-0 pt-2">
    <div class="px-gutter">{search_field(placeholder, query, label, focused, clear_href=clear_href)}</div>
    {chip_row}
  </div>'''


def count_line(text):
    return f'<p class="shrink-0 px-gutter pb-1 pt-1 text-body-sm tabular-nums text-muted-foreground" role="status">{text}</p>'


def menu_btn(title, href=None, extra=''):
    return icon_btn('ellipsis-vertical', f'More options for {title}', href, 'row-menu', f'text-muted-foreground {extra}', 'size-5')


def row(lead, title, meta, trailing='', href='S26-item-detail.html#S26-product', menu='#S28-row-menu', last=False, bg='',
        title_html=None, action='open-item', meta_cls='line-clamp-2', large=False, tint=''):
    bb = '' if last else ' border-b'
    menu_html = f'<span class="flex shrink-0 items-center pr-1{bb}">{menu_btn(title, menu)}</span>' if menu is not None else ''
    t = title_html or title
    if large:
        body = f'<span class="flex min-w-0 flex-1 flex-col items-start gap-2 self-stretch py-4{bb}"><span class="text-title-2 font-normal">{t}</span><span class="text-title-3 font-normal text-muted-foreground">{meta}</span>{trailing}</span>'
        return f'''<li class="flex items-stretch {bg}">
      <a href="{href}" class="flex min-w-0 flex-1 items-start gap-4 pl-gutter" data-action="{action}"><span class="shrink-0 pt-4">{lead}</span>{body}</a>{menu_html}
    </li>'''
    pr = ' pr-1' if menu is not None else ' pr-gutter'
    return f'''<li class="flex items-stretch {bg}">
      <a href="{href}" class="flex min-w-0 flex-1 items-center gap-3 pl-gutter" data-action="{action}">{lead}<span class="flex min-w-0 flex-1 items-center gap-3 self-stretch py-3{pr}{bb}"><span class="min-w-0 flex-1"><span class="line-clamp-2 text-body {tint}">{t}</span><span class="mt-0.5 text-body-sm text-muted-foreground {meta_cls}">{meta}</span></span>{trailing}</span></a>{menu_html}
    </li>'''


def rows(items):
    return f'<ul aria-label="Items">{"".join(items)}</ul>'


def desk_rows(ids, menu='#S28-row-menu', bg_for=None, badge_for=None, title_html=None, href='S26-item-detail.html#S26-product'):
    out = []
    for i, pid in enumerate(ids):
        b = badge(badge_for.get(pid) if badge_for and pid in badge_for else LATEST[pid])
        out.append(row(thumb(pid), P[pid]['name'], pmeta(pid), b, href, menu, last=i == len(ids) - 1,
                       bg=(bg_for or {}).get(pid, ''), title_html=(title_html or {}).get(pid)))
    return out


def results_bar(list_name, back_href, back_label, hist_href, export_href='S39-export.html#S39-default', title='Results', export=True, history=True):
    tr = ''
    if history:
        tr += icon_btn('history', 'Round history', hist_href, 'round-history')
    if export:
        tr += f'<a href="{export_href}" class="inline-flex h-12 min-w-touch items-center justify-center rounded-full px-3 text-label-lg text-primary" data-action="export">Export</a>'
    return back_bar(title, back_href, back_label, tr, sub=list_name)


def desk_bar(**kw):
    return results_bar('Desk setup', 'S09-list-overview.html#S09-solo-round-done', 'Back to Desk setup', 'S30-round-history.html#S30-default', **kw)


def wed_bar(**kw):
    return results_bar('Wedding guests', 'S09-list-overview.html#S09-shared', 'Back to Wedding guests', 'S30-round-history.html#S30-in-progress', 'S39-export.html#S39-shared', **kw)


def view_toggle(selected, links=None):
    links = links or {}
    btns = ''
    for text in ('Final decisions', 'My decisions'):
        on = text == selected
        cls = 'bg-card text-foreground shadow-raised' if on else 'text-muted-foreground'
        href = links.get(text)
        attrs = f'role="radio" aria-checked="{"true" if on else "false"}" class="inline-flex h-10 flex-1 items-center justify-center gap-1.5 rounded-full px-3 text-label {cls}"'
        btns += f'<a href="{href}" {attrs} data-action="view-{"final" if text.startswith("F") else "mine"}">{text}</a>' if href else f'<button type="button" {attrs}>{text}</button>'
    return f'<div class="shrink-0 px-gutter pb-2"><div class="flex rounded-full bg-secondary p-1" role="radiogroup" aria-label="Show decisions">{btns}</div></div>'


VIEW_LINKS = {'Final decisions': '#S28-shared-accept', 'My decisions': '#S28-shared-mine'}


def screen(*parts, body='', overlay=''):
    top = ''.join(parts)
    return f'''{top}
  <div class="relative min-h-0 flex-1 overflow-hidden">{body}</div>
  {overlay}'''


def strip(html):
    """Inert backdrop copy: same layout classes, no interactive elements, no ids."""
    html = re.sub(r'<(a|button)\b', '<span', html)
    html = re.sub(r'</(a|button)>', '</span>', html)
    html = re.sub(r'<input\b[^>]*class="([^"]*)"[^>]*>', r'<span class="block \1"></span>', html)
    html = re.sub(r' (id|href|type|disabled|data-action|role|tabindex|aria-[a-z]+)(="[^"]*")?(?=[\s>])', '', html)
    html = re.sub(r'<h([12]) ', r'<p ', html)
    html = re.sub(r'</h[12]>', '</p>', html)
    return f'<div class="flex min-h-0 flex-1 flex-col" aria-hidden="true">{html}</div>'


def dropdown(items, top, label, right='right-3'):
    out = ''
    for ic, text, href, action in items:
        if text == '-':
            out += '<div class="my-1 border-t" role="separator"></div>'
            continue
        h = f'href="{href}" ' if href else ''
        tag = 'a' if href else 'button'
        typ = '' if href else 'type="button" '
        out += f'<{tag} {h}{typ}role="menuitem" class="flex h-12 w-full items-center gap-3 px-4 text-left text-body" data-action="{action}">{icon(ic, "size-5 text-muted-foreground")}{text}</{tag}>'
    return f'<div class="absolute {right} {top} z-30 w-60 overflow-hidden rounded-control bg-popover py-1 shadow-overlay" role="menu" aria-label="{label}">{out}</div>'


def decision_picker(selected, label, links=None, large=False):
    links = links or {}
    btns = ''
    for kind in ('reject', 'maybe', 'accept'):
        ic, verb, _, _ = DEC[kind]
        on = kind == selected
        cls = f'bg-{kind} text-{kind}-foreground' if on else 'border border-input bg-card'
        icn = icon(ic, 'size-5') if on else icon(ic, f'size-5 text-{kind}-soft-foreground')
        h = 'min-h-16 flex-col text-title-3 font-normal' if large else 'h-12'
        attrs = f'role="radio" aria-checked="{"true" if on else "false"}" class="flex {h} items-center justify-center gap-1.5 rounded-control text-label-lg {cls}" data-action="decide-{kind}"'
        href = links.get(kind)
        btns += f'<a href="{href}" {attrs}>{icn}{verb}</a>' if href else f'<button type="button" {attrs}>{icn}{verb}</button>'
    return f'<div class="grid grid-cols-3 gap-2" role="radiogroup" aria-label="{label}">{btns}</div>'


def sheet_head(title, hid, close_href, sub=None, back=None):
    s = f'<p class="text-body-sm text-muted-foreground">{sub}</p>' if sub else ''
    lead = icon_btn('arrow-left', back[1], back[0], 'back', '-ml-3', 'size-5') if back else ''
    close = icon_btn('x', 'Close', close_href, 'close', '-mr-3', 'size-5') if close_href else ''
    return f'<div class="flex shrink-0 items-center gap-1 px-gutter pt-1">{lead}<div class="min-w-0 flex-1"><h2 id="{hid}" class="text-title-3">{title}</h2>{s}</div>{close}</div>'


def change_sheet(title, lead, meta, selected, note, close_href, links=None, heading='Change decision', extra=''):
    hid = uid('cs')
    inner = f'''{sheet_head(heading, hid, close_href)}
    <div class="space-y-4 px-gutter pb-6 pt-3">
      <div class="flex items-center gap-3">{lead}<div class="min-w-0 flex-1"><p class="line-clamp-2 text-body">{title}</p><p class="truncate text-body-sm text-muted-foreground">{meta}</p></div></div>
      {decision_picker(selected, f"Decision for {title}", links)}
      {extra}
      <p class="text-body-sm text-muted-foreground">{note}</p>
    </div>'''
    return '<!-- Proposed component: ChangeDecisionSheet (BottomSheet + S26 decision control) -->' + sheet(inner, hid, top=None)


IOS_GRAB = '<div class="flex shrink-0 justify-center pt-2"><span class="h-1.5 w-9 rounded-full bg-muted-foreground/40"></span></div>'


# ==================================================================================== S28
F = Frames('S28')

desk_tools = toolbar('Search 8 items in Accept', label='Search in Accept')
DESK_SEG_LINKS = {'accept': '#S28-default', 'maybe': '#S28-maybe', 'reject': '#S28-default'}

F.section('Solo list: Desk setup after Round 2', 'Results show the latest decision per item across rounds (A-33): Round 2 re-sorted the 6 Maybe items, so Desk setup now has 8 accepted, 1 maybe and 11 rejected. Segments lead with Accept (the result people come for) and keep icon, label and count. Rows are full-bleed: thumbnail, title, price and store, decision badge, overflow menu.')

F.add('S28-default', 'Default: Desk setup, Accept segment', phone(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'accept', links=DESK_SEG_LINKS), desk_tools,
    body=rows(desk_rows(DESK_ACC)),
)))

maybe_body = rows(desk_rows(DESK_MAY)) + f'''<div class="px-gutter pt-6"><p class="text-body-sm text-muted-foreground">Still undecided after Round 2. Sort it again with a fresh look.</p>
    <a href="S24-start-round.html#S24-maybe" class="mt-3 inline-flex h-12 items-center gap-2 rounded-control border border-input bg-card px-4 text-label-lg" data-action="resort-maybe">{icon("circle-help", "size-5 text-maybe-soft-foreground")}Re-sort Maybe (1)</a></div>'''
F.add('S28-maybe', 'Maybe segment: 1 item left after two rounds', phone(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'maybe', links=DESK_SEG_LINKS), toolbar('Search 1 item in Maybe', label='Search in Maybe'),
    body=maybe_body,
)))

ROW_MENU = [('info', 'Open details', 'S26-item-detail.html#S26-product', 'open-details'),
            ('arrow-right-left', 'Change decision', '#S28-change-decision', 'change-decision'),
            ('sticky-note', 'Add note', '#S28-add-note', 'add-note')]
F.add('S28-row-menu', 'Row overflow menu: Open details, Change decision, Add note', phone(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'maybe', links=DESK_SEG_LINKS), toolbar('Search 1 item in Maybe', label='Search in Maybe'),
    body=rows(desk_rows(DESK_MAY, bg_for={'p18': 'bg-accent'})),
    overlay=dropdown(ROW_MENU, 'top-72', 'Options for Bookshelf speakers, pair'),
)))

p18_meta = f'{pmeta("p18")}'
F.add('S28-change-decision', 'Change decision sheet (RES-06): tap a decision to apply it', phone(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'maybe', links=DESK_SEG_LINKS), toolbar('Search 1 item in Maybe', label='Search in Maybe'),
    body=rows(desk_rows(DESK_MAY)),
    overlay=scrim() + change_sheet(P['p18']['name'], thumb('p18'), p18_meta, 'maybe',
                                   'Maybe in Round 1 and Round 2. The change applies at once and round history keeps both rounds as they were.',
                                   '#S28-maybe', links={'accept': '#S28-changed', 'reject': '#S28-changed'}),
)))

SEGS_AFTER = [('accept', 'Accept', 9), ('maybe', 'Maybe', 0), ('reject', 'Reject', 11)]
F.add('S28-changed', 'Changed to Accept: row stays with its new badge until the snackbar closes', phone(screen(
    desk_bar(), seg_bar(SEGS_AFTER, 'maybe', links={'accept': '#S28-default', 'maybe': '#S28-empty-segment'}), toolbar('Search in Maybe', label='Search in Maybe'),
    body=rows(desk_rows(DESK_MAY, badge_for={'p18': 'accept'}, bg_for={'p18': 'bg-accent'})),
    overlay=snackbar('Changed to Accept', 'Undo', 'bottom-4', href='#S28-maybe'),
)))

F.add('S28-empty-segment', 'Empty segment: nothing in Maybe', phone(screen(
    desk_bar(), seg_bar(SEGS_AFTER, 'maybe', links={'accept': '#S28-default'}),
    body=f'''<div class="flex h-full flex-col items-center px-gutter pt-20 text-center">
      {icon("circle-help", "size-8 text-muted-foreground")}
      <h2 class="mt-3 text-title-3">Nothing in Maybe</h2>
      <p class="mt-1 max-w-xs text-body text-muted-foreground">Items you swipe up will wait here.</p>
      <a href="S24-start-round.html#S24-default" class="mt-6 inline-flex h-12 items-center justify-center rounded-control border border-input bg-card px-5 text-label-lg" data-action="new-round">Start a new round</a>
    </div>''',
)))

note_hid = uid('ns')
note_sheet = sheet(f'''{sheet_head("Note on Bookshelf speakers, pair", note_hid, "#S28-maybe")}
    <div class="px-gutter pb-6 pt-3">
      <label for="{note_hid}t" class="text-label">Note</label>
      <textarea id="{note_hid}t" rows="3" class="mt-1.5 w-full resize-none rounded-control border border-primary bg-card px-3.5 py-3 text-body ring-2 ring-ring/30">Check if they fit on the shelf above the desk.</textarea>
      <p class="mt-1.5 text-right text-caption tabular-nums text-muted-foreground">47 / 1,000</p>
      <div class="mt-4">{btn("Save note", "primary", "#S28-maybe", "save-note")}</div>
    </div>''', note_hid, top=None)
F.add('S28-add-note', 'Add note from the row menu (same note sheet as S25)', phone(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'maybe', links=DESK_SEG_LINKS), toolbar('Search 1 item in Maybe', label='Search in Maybe'),
    body=rows(desk_rows(DESK_MAY)), overlay=scrim() + note_sheet,
)))

# ---------------------------------------------------------------- search, filter, sort
F.section('Search, filter and sort', 'Every segment has its own search (RES-02), filters (RES-03) and sorting (RES-04); they apply to the segment shown. Filter and Sort open the S29 sheet; applied filters appear as removable chips. Search matches the title, every visible field and notes.')

hl = {'p15': 'Pendant <span class="font-semibold">lamp</span>, opal glass'}
F.add('S28-search', 'Search with results, plus matches in other segments', phone(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'accept', links=DESK_SEG_LINKS),
    toolbar('Search 8 items in Accept', 'lamp', label='Search in Accept', focused=True, clear_href='#S28-default'),
    count_line('1 of 8 items'),
    body=rows(desk_rows(['p15'], title_html=hl)) + f'''<div class="px-gutter pt-5"><p class="text-label text-muted-foreground">In other segments</p>
      <a href="#S28-default" class="mt-1 flex min-h-12 items-center gap-3 text-body" data-action="search-other-segment">{icon("x", "size-5 text-reject-soft-foreground")}<span class="flex-1">1 match in Reject</span><span class="text-label text-primary">Show</span></a></div>''',
)))

F.add('S28-search-none', 'Search with no results in this segment', phone(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'accept', links=DESK_SEG_LINKS),
    toolbar('Search 8 items in Accept', 'headphones', label='Search in Accept', focused=True, clear_href='#S28-default'),
    body=f'''<div class="flex flex-col items-center px-gutter pt-16 text-center">
      {icon("search-x", "size-8 text-muted-foreground")}
      <h2 class="mt-3 text-title-3">No matches in Accept</h2>
      <p class="mt-1 max-w-xs text-body text-muted-foreground">Nothing in Accept matches “headphones”. It matches 1 item in Reject.</p>
      <a href="#S28-default" class="mt-6 inline-flex h-12 items-center justify-center rounded-control border border-input bg-card px-5 text-label-lg" data-action="search-other-segment">Show 1 match in Reject</a>
      <a href="#S28-default" class="mt-2 inline-flex h-12 items-center justify-center rounded-control px-5 text-label-lg" data-action="clear-search">Clear search</a>
    </div>''',
)))


def mine_row(k, last=False, menu='#S28-shared-change', href='S26-item-detail.html#S26-shared-conflict'):
    st = STATUS[k]
    meta = cmeta(k)
    if st == 'conflict':
        others = {m: v for m, v in SI[k]['decisions'].items() if m != 'u-deniz'}
        meta = parts_html([(DEC[v][0], f'text-{v}-soft-foreground', f'{dict((a, n) for a, _, n in MEMBERS)[m]} {PAST[v]}') for m, v in others.items() if v and v != MY[k]])
    elif st == 'pending':
        meta = parts_html([('clock', 'text-muted-foreground', waiting_text(SI[k]["decisions"]))])
    return row(cav(k), C[k]['name'], meta, badge(st), href, menu, last, meta_cls='block')


F.add('S28-filtered', 'Filters applied from S29 (Side, Relationship): chips can be removed one by one', phone(screen(
    wed_bar(), view_toggle('My decisions', VIEW_LINKS), seg_bar(MINE_SEGS, 'accept'),
    toolbar('Search 48 items in Accept', label='Search in Accept', filter_href='S29-filter-sort.html#S29-default', n_filters=2,
            applied=[("Side: Groom's", "Side is Groom's"), ('Relationship: Friend', 'Relationship is Friend')]),
    count_line('12 of 48 items'),
    body=rows([mine_row(k, i == 11) for i, k in enumerate(WED_12)]),
)))

by_price = sorted(DESK_ACC, key=lambda k: -P[k]['price'])
F.add('S28-sorted', 'Sorted by Price, high to low (chosen in S29)', phone(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'accept', links=DESK_SEG_LINKS),
    toolbar('Search 8 items in Accept', label='Search in Accept', sort_label='Price, high to low'),
    body=rows(desk_rows(by_price)),
)))

# ---------------------------------------------------------------- shared
F.section('Shared list: Wedding guests (Round 1 in progress)', 'Final decisions (RES-05) show the list-level result: Agreed items in Accept, Maybe and Reject; Conflicts (15) and Pending (53) are not final yet and get their own segments, so no item is hidden. My decisions show only my own choices, with the list status on every row so the difference from the final decision is visible. Rows show who decided what (COL-16).')

CONF_SHIFT = '-translate-x-32'
PEND_SHIFT = '-translate-x-60'
FINAL_LINKS = {'accept': '#S28-shared-accept', 'conflict': '#S28-shared', 'pending': '#S28-shared-pending'}


def conf_row(k, last=False, bg=''):
    d = SI[k]['decisions']
    return row(cav(k), C[k]['name'], who_parts(d), '', 'S26-item-detail.html#S26-shared-conflict', '#S28-shared-change', last, bg=bg, meta_cls='block')


conf_note = '<p class="px-gutter pb-2 pt-1 text-body-sm text-muted-foreground">Members chose differently. Mert resolves conflicts as Decision Maker.</p>'
F.add('S28-shared', 'Shared list, Final decisions: Conflicts segment with who decided what', phone(screen(
    wed_bar(), view_toggle('Final decisions', VIEW_LINKS), seg_bar(FINAL_SEGS, 'conflict', CONF_SHIFT, FINAL_LINKS),
    toolbar('Search 15 conflicts', label='Search in Conflicts', filter_href='S29-filter-sort.html#S29-default'),
    body=conf_note + rows([conf_row(k) for k in CONF[:7]]),
    overlay=f'<div class="absolute inset-x-0 bottom-0 z-10 border-t bg-background px-gutter pb-4 pt-3">{btn("Review 15 conflicts", "primary", "S36-conflicts.html#S36-default", "review-conflicts", ic="git-compare-arrows")}</div>',
)))


def agreed_row(k, last=False):
    return row(cav(k), C[k]['name'], cmeta(k), badge('agreed'), 'S26-item-detail.html#S26-shared-conflict', '#S28-shared-change', last)


F.add('S28-shared-accept', 'Final decisions, Accept: 22 items everyone accepted', phone(screen(
    wed_bar(), view_toggle('Final decisions', VIEW_LINKS), seg_bar(FINAL_SEGS, 'accept', links=FINAL_LINKS),
    toolbar('Search 22 items in Accept', label='Search in Accept', filter_href='S29-filter-sort.html#S29-default'),
    body=rows([agreed_row(k) for k in F_ACC[:8]]),
)))


def pend_row(k, last=False):
    d = SI[k]['decisions']
    return row(cav(k), C[k]['name'], who_parts(d, pending=True), '', 'S26-item-detail.html#S26-shared-conflict', '#S28-shared-change', last, meta_cls='block')


pend_note = f'''<div class="mx-gutter mb-2 mt-1 rounded-control bg-muted p-4" role="note">
      <p class="flex items-center gap-2 text-label">{icon("clock", "size-4 shrink-0")}Not final yet</p>
      <p class="mt-1 text-body-sm">These items get a final decision once every member has decided them. Waiting for Selin on 53, for you on 24 and for Mert on 12.</p>
      <a href="S25-sorting.html#S25-shared" class="-mb-2 mt-1 inline-flex h-12 items-center text-label-lg text-primary" data-action="continue-sorting">Continue sorting</a>
    </div>'''
F.add('S28-shared-pending', 'Final decisions, Pending: not final yet, items waiting for me listed first', phone(screen(
    wed_bar(), view_toggle('Final decisions', VIEW_LINKS), seg_bar(FINAL_SEGS, 'pending', PEND_SHIFT, FINAL_LINKS),
    toolbar('Search 53 pending items', label='Search in Pending', sort_label='Waiting for you first', filter_href='S29-filter-sort.html#S29-default'),
    body=pend_note + rows([pend_row(k) for k in PEND_SORTED[:6]]),
)))

F.add('S28-shared-mine', 'My decisions, Accept: my 48, each with its list status (differs from final on conflicts)', phone(screen(
    wed_bar(), view_toggle('My decisions', VIEW_LINKS), seg_bar(MINE_SEGS, 'accept'),
    toolbar('Search 48 items in Accept', label='Search in Accept', filter_href='S29-filter-sort.html#S29-default'),
    body=rows([mine_row(k) for k in MY_ACC[:8]]),
)))

ROLE_IC = {'Owner': 'crown', 'Decision Maker': 'gavel', 'Collaborator': None}


def role_line(role, extra=''):
    ic = ROLE_IC.get(role)
    r = f'<span class="inline-flex items-center gap-1 whitespace-nowrap">{icon(ic, "size-4 shrink-0")}{role}</span>' if ic else f'<span class="whitespace-nowrap">{role}</span>'
    return f'<span class="mt-0.5 flex min-w-0 flex-wrap items-center gap-x-3 text-body-sm text-muted-foreground">{r}{extra}</span>'


k69 = 'c069'
who69 = f'''<ul class="divide-y overflow-hidden rounded-group bg-card" aria-label="Decisions by member">
        <li class="flex min-h-12 items-center gap-3 px-4 py-2">{avatar("mert", "size-8")}<span class="min-w-0 flex-1"><span class="block text-body">Mert</span>{role_line("Decision Maker")}</span>{badge("reject")}</li>
        <li class="flex min-h-12 items-center gap-3 px-4 py-2">{avatar("selin", "size-8")}<span class="min-w-0 flex-1"><span class="block text-body">Selin</span>{role_line("Collaborator")}</span>{badge("accept")}</li>
      </ul>'''
F.add('S28-shared-change', 'Change my decision on a shared list: others stay visible, status recomputes', phone(screen(
    wed_bar(), view_toggle('Final decisions', VIEW_LINKS), seg_bar(FINAL_SEGS, 'conflict', CONF_SHIFT, FINAL_LINKS),
    toolbar('Search 15 conflicts', label='Search in Conflicts'),
    body=conf_note + rows([conf_row(k) for k in CONF[:7]]),
    overlay=scrim() + change_sheet(C[k69]['name'], cav(k69), cmeta(k69), 'accept',
                                   'Changing your decision updates the list status for everyone. Choosing Reject keeps this item in Conflict: Selin chose Accept.',
                                   '#S28-shared', links={'reject': '#S28-shared', 'maybe': '#S28-shared'}, heading='Change my decision', extra=who69),
)))


def resolved_row(k, last=False):
    final = RESOLVED[k]
    mine = SI[k]['decisions']['u-deniz']
    if mine != final:
        ic = DEC[mine][0]
        meta = parts_html([(ic, f'text-{mine}-soft-foreground', f'You chose {DEC[mine][1]}')])
    else:
        others = [(n, SI[k]['decisions'][m]) for m, _, n in MEMBERS[1:] if SI[k]['decisions'][m] and SI[k]['decisions'][m] != final]
        meta = parts_html([(DEC[v][0], f'text-{v}-soft-foreground', f'{n} chose {DEC[v][1]}') for n, v in others])
    return row(cav(k), C[k]['name'], meta, badge('resolved', 'Resolved'), 'S26-item-detail.html#S26-shared-conflict', '#S28-shared-change', last, meta_cls='block')


RES_SEGS = [('accept', 'Accept', 28), ('maybe', 'Maybe', 6), ('reject', 'Reject', 10), ('conflict', 'Conflicts', 3), ('pending', 'Pending', 53)]
res_note = f'<p class="flex items-start gap-2 px-gutter pb-2 pt-1 text-body-sm text-muted-foreground">{icon("gavel", "mt-0.5 size-4 shrink-0")}<span>Mert resolved 12 conflicts. 3 stay open because he hasn\'t decided them.</span></p>'
F.add('S28-shared-resolved', 'After bulk resolve (S37): final decision differs from mine on some rows', phone(screen(
    wed_bar(), view_toggle('Final decisions', VIEW_LINKS), seg_bar(RES_SEGS, 'accept', links=FINAL_LINKS),
    toolbar('Search 28 items in Accept', label='Search in Accept'),
    body=res_note + rows([resolved_row(k) for k in RES_ACC] + [agreed_row(k) for k in F_ACC[:2]]),
)))

# ---------------------------------------------------------------- round results (from S30)
F.section('Round results (opened from S30)', 'Tapping a round in history opens Results for that round: the decisions as they were when the round ended. Rows say what changed later. Search, filters and sorting work the same; Export always uses the latest results.')


def round_rows(ids, round_dec, later):
    out = []
    for i, pid in enumerate(ids):
        lt = later.get(pid)
        meta = pmeta(pid)
        if lt:
            meta = f'{meta}<span class="mt-0.5 flex items-start gap-1">{lt}</span>'
        out.append(row(thumb(pid), P[pid]['name'], meta, badge(round_dec[pid]), 'S26-item-detail.html#S26-product', '#S28-row-menu', i == len(ids) - 1, meta_cls='block'))
    return out


def later_text(pid):
    v = R2[pid]
    if v == 'maybe':
        return f'{icon("circle-help", "mt-0.5 size-4 shrink-0 text-maybe-soft-foreground")}<span>Still Maybe in Round 2</span>'
    return f'{icon(DEC[v][0], f"mt-0.5 size-4 shrink-0 text-{v}-soft-foreground")}<span>Changed to {DEC[v][1]} in Round 2</span>'


r1_maybe = [k for k in R1 if R1[k] == 'maybe']
round_banner = lambda text, href: f'''<div class="mx-gutter mb-1 mt-1 flex items-start gap-3 rounded-control bg-primary-soft p-3 text-primary-soft-foreground" role="note">{icon("history", "mt-0.5 size-5 shrink-0")}<div class="min-w-0 flex-1 text-body-sm"><p>{text}</p><a href="{href}" class="-mb-2 inline-flex h-12 items-center text-label underline underline-offset-4" data-action="latest-results">See latest results</a></div></div>'''
R1_SEGS = [('accept', 'Accept', 5), ('maybe', 'Maybe', 6), ('reject', 'Reject', 9)]
F.add('S28-round-1', 'Round 1 results (Desk setup): Maybe segment shows what Round 2 changed', phone(screen(
    results_bar('Desk setup', 'S30-round-history.html#S30-default', 'Back to round history', None, title='Round 1 results', export=False, history=False),
    round_banner('Decisions as they were when Round 1 ended on Oct 4. 6 items were sorted again in Round 2.', '#S28-default'),
    seg_bar(R1_SEGS, 'maybe'), toolbar('Search 6 items in Maybe', label='Search in Maybe'),
    body=rows(round_rows(r1_maybe, R1, {k: later_text(k) for k in r1_maybe})),
)))

R2_SEGS = [('accept', 'Accept', 3), ('maybe', 'Maybe', 1), ('reject', 'Reject', 2)]
F.add('S28-round-2', 'Round 2 results: only the 6 items in that round', phone(screen(
    results_bar('Desk setup', 'S30-round-history.html#S30-default', 'Back to round history', None, title='Round 2 results', export=False, history=False),
    round_banner('Round 2 sorted the 6 Maybe items from Round 1 on Oct 6. These are also the latest decisions for them.', '#S28-default'),
    seg_bar(R2_SEGS, 'accept'), toolbar('Search 3 items in Accept', label='Search in Accept'),
    body=rows(round_rows([k for k in reversed(R2_ORDER) if R2[k] == 'accept'], R2, {})),
)))

APT = {a['id']: a for a in D['apartments']}
APT_DEC = {'a01': 'accept', 'a02': 'reject', 'a03': 'accept', 'a04': 'reject', 'a05': 'accept', 'a06': 'reject', 'a07': 'maybe', 'a08': 'reject'}  # illustrative (r-a1: 3 / 1 / 4)
apt_rows = [row('', APT[k]['address'], f"{APT[k]['rooms']}, {APT[k]['sizeM2']} m², {fmt(APT[k]['rent'])} TRY", badge('accept'), 'S26-item-detail.html#S26-read-only', None, i == 2)
            for i, k in enumerate([k for k in APT_DEC if APT_DEC[k] == 'accept'])]
F.add('S28-archived', 'Archived list (Apartment viewings): read-only results, no row menu', phone(screen(
    results_bar('Apartment viewings', 'S09-list-overview.html#S09-archived', 'Back to Apartment viewings', 'S30-round-history.html#S30-single-round', 'S39-export.html#S39-apartments'),
    f'<div class="mx-gutter mb-1 mt-1 flex items-start gap-3 rounded-control border bg-card p-3" role="note">{icon("archive", "mt-0.5 size-5 shrink-0 text-muted-foreground")}<p class="text-body-sm">Apartment viewings is archived. Restore it to change decisions or add notes. Export still works.</p></div>',
    seg_bar([('accept', 'Accept', 3), ('maybe', 'Maybe', 1), ('reject', 'Reject', 4)], 'accept'),
    toolbar('Search 3 items in Accept', label='Search in Accept'),
    body=rows(apt_rows),
)))

# ---------------------------------------------------------------- states
F.section('Loading, offline, error and long lists', 'Results come from the working copy on the phone, so loading is short and offline still works; shared statuses update after sync. Long lists keep the segment bar pinned and add a fast-scroll handle.')

sk_rows = ''.join(f'''<li class="flex items-center gap-3 py-3 pl-gutter pr-gutter"><span class="size-12 shrink-0 animate-pulse rounded-sm bg-muted"></span><span class="flex-1 space-y-2"><span class="block h-4 w-{w} animate-pulse rounded-xs bg-muted"></span><span class="block h-3 w-24 animate-pulse rounded-xs bg-muted"></span></span><span class="h-7 w-20 animate-pulse rounded-full bg-muted"></span></li>''' for w in ('48', '40', '56', '36', '44', '52', '40'))
F.add('S28-loading', 'Loading: skeleton rows, controls wait for counts', phone(screen(
    desk_bar(export=False),
    f'<div class="flex shrink-0 gap-2 px-gutter py-1" aria-hidden="true"><span class="h-10 w-28 animate-pulse rounded-full bg-muted"></span><span class="h-10 w-24 animate-pulse rounded-full bg-muted"></span><span class="h-10 w-24 animate-pulse rounded-full bg-muted"></span></div>',
    f'<div class="shrink-0 px-gutter pt-2" aria-hidden="true"><span class="block h-12 w-full rounded-full bg-secondary"></span></div>',
    body=f'<p class="sr-only" role="status">Loading results</p><ul class="pt-3" aria-hidden="true">{sk_rows}</ul>',
)))

F.add('S28-offline', 'Offline (shared): everything works on the phone; statuses update after sync', phone(screen(
    wed_bar(), offline_banner(), view_toggle('Final decisions', VIEW_LINKS), seg_bar(FINAL_SEGS, 'conflict', CONF_SHIFT, FINAL_LINKS),
    toolbar('Search 15 conflicts', label='Search in Conflicts', filter_href='S29-filter-sort.html#S29-default'),
    body=f'<p class="flex items-center gap-2 px-gutter pb-2 pt-1 text-body-sm text-muted-foreground">{icon("cloud-off", "size-4 shrink-0")}List statuses from 12 min ago. They update when you\'re back online.</p>' + rows([conf_row(k) for k in CONF[:7]]),
)))

F.add('S28-error', 'Error: the working copy could not be read', phone(screen(
    desk_bar(export=False, history=False),
    body=f'''<div class="flex h-full flex-col items-center justify-center px-8 pb-16 text-center">
      {icon("triangle-alert", "size-8 text-muted-foreground")}
      <h2 class="mt-4 text-title-3">Results couldn't be opened</h2>
      <p class="mt-1 max-w-xs text-body text-muted-foreground">Your decisions are safe. Try again, or go back and open Results from the list.</p>
      <a href="#S28-default" class="mt-6 flex h-12 w-full max-w-xs items-center justify-center rounded-control bg-secondary text-label-lg text-secondary-foreground" data-action="try-again">Try again</a><a href="S09-list-overview.html#S09-solo-round-done" class="mt-2 flex h-12 w-full max-w-xs items-center justify-center rounded-control text-label-lg" data-action="back">Back to list</a>
    </div>''',
)))

az = sorted(MY_ACC, key=lambda k: trkey(C[k]['name']))
mi = next(i for i, k in enumerate(az) if C[k]['name'].startswith('M'))
long_rows = rows([mine_row(k) for k in az[mi - 1:mi + 11]])
fast = '''<!-- Proposed component: FastScroller -->
    <div class="absolute inset-y-2 right-0 z-10 w-6" role="scrollbar" aria-orientation="vertical" aria-controls="ll" aria-valuenow="58" aria-valuemin="0" aria-valuemax="100" aria-label="Fast scroll" tabindex="-1"><span class="absolute right-1 top-[52%] h-12 w-1.5 rounded-full bg-muted-foreground"></span></div>
    <span class="absolute right-40 top-[48%] z-10 flex size-14 items-center justify-center rounded-full bg-primary text-title-2 text-primary-foreground shadow-overlay" aria-hidden="true">M</span>'''
F.add('S28-large-list', 'Long list scrolled: segments pinned under the bar, fast scroll with letter (Name, A to Z)', phone(screen(
    wed_bar(), seg_bar(MINE_SEGS, 'accept', pinned=True),
    body=long_rows.replace('<ul ', '<ul id="ll" ', 1).replace('<ul id="ll" aria-label="Items">', '<ul id="ll" aria-label="Items" class="-mt-6">', 1) + fast,
)))

# ---------------------------------------------------------------- platforms
F.section('iOS, web and large text', 'iOS: native back with the list name, swipe actions on rows (trailing: the other two decisions; leading: Note), context menu on long press. Web: same layout; desktop shows keyboard hints and opens the row menu as a popover. Large text: rows reflow, the badge moves under the title.')

ios_rows = []
for i, pid in enumerate(DESK_ACC[:7]):
    if pid == 'p09':
        ios_rows.append(f'''<!-- Proposed component: RowSwipeActions (iOS) --><li class="relative flex items-stretch overflow-hidden">
      <div class="absolute inset-y-0 right-0 flex" role="group" aria-label="Actions for {P[pid]["name"]}">
        <a href="#S28-ios" class="flex w-24 flex-col items-center justify-center gap-1 bg-maybe text-label text-maybe-foreground" data-action="swipe-maybe">{icon("circle-help", "size-5")}Maybe</a>
        <a href="#S28-ios" class="flex w-24 flex-col items-center justify-center gap-1 bg-reject text-label text-reject-foreground" data-action="swipe-reject">{icon("x", "size-5")}Reject</a>
      </div>
      <div class="flex min-w-0 flex-1 -translate-x-48 items-center gap-3 bg-background pl-gutter">{thumb(pid)}<span class="flex min-w-0 flex-1 items-center gap-3 self-stretch border-b py-3 pr-gutter"><span class="min-w-0 flex-1"><span class="line-clamp-2 text-body">{P[pid]["name"]}</span><span class="mt-0.5 block truncate text-body-sm text-muted-foreground">{pmeta(pid)}</span></span>{badge("accept")}</span></div>
    </li>''')
    else:
        ios_rows.append(row(thumb(pid), P[pid]['name'], pmeta(pid), badge('accept'), 'S26-item-detail.html#S26-product', None, i == 6))
ios_bar_html = ios_bar(f'<a href="S09-list-overview.html#S09-ios" class="-ml-2 inline-flex h-12 items-center text-body text-primary" data-action="back">{icon("chevron-left", "size-6")}Desk setup</a>',
                       'Results', f'<span class="flex items-center">{icon_btn("history", "Round history", "S30-round-history.html#S30-ios", "round-history", "text-primary")}{ios_text_btn("Export", href="S39-export.html#S39-ios", action="export")}</span>')
F.add('S28-ios', 'iOS: row swiped left shows Maybe and Reject (the other decisions)', phone(screen(
    ios_bar_html, seg_bar(DESK_SEGS, 'accept'), toolbar('Search 8 items in Accept', label='Search in Accept'),
    body=rows(ios_rows),
), ios=True))

desk_menu = dropdown(ROW_MENU, 'top-96', 'Options for Low-profile mechanical keyboard', right='right-14')
F.add('S28-web-desktop', 'Web, desktop: row menu as a popover, keyboard hints', desktop(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'accept', links=DESK_SEG_LINKS), desk_tools,
    body=rows(desk_rows(DESK_ACC[:6], bg_for={'p04': 'bg-accent'})), overlay=desk_menu,
), 'swipesort.app/l/desk-setup/results', hints([('/', 'Search'), ('F', 'Filter'), ('↑ ↓', 'Move'), ('Enter', 'Open')])))

lt_rows = []
for i, pid in enumerate(DESK_ACC[:4]):
    lt_rows.append(row(thumb(pid, 'size-14'), P[pid]['name'], pmeta(pid), badge('accept').replace('h-7', 'min-h-10 py-1').replace('px-2.5 text-caption', 'px-3.5 text-title-3 font-normal').replace('size-4', 'size-5'), 'S26-item-detail.html#S26-product', '#S28-row-menu', large=True))
lt_bar = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    {icon_btn("arrow-left", "Back to Desk setup", "S09-list-overview.html#S09-solo-round-done", "back", "", "size-7")}
    <div class="min-w-0 flex-1 px-1"><h1 class="text-title-1">Results</h1></div>
    {icon_btn("ellipsis-vertical", "More options: Export, Round history", "#S28-large-text-menu", "menu", "", "size-7")}
  </header>'''
lt_tools = f'''<div class="shrink-0 space-y-3 px-gutter pt-2">
    {search_field("Search in Accept", label="Search in Accept", large=True)}
    <div class="flex gap-2">{tool_chip("Filter", "sliders-horizontal", "S29-filter-sort.html#S29-large-text", "filter", large=True)}{tool_chip("Sort", "arrow-up-down", "S29-filter-sort.html#S29-sort", "sort", large=True)}</div>
  </div>'''
F.add('S28-large-text', 'Large text (200%): badge under the title, Export moves into the menu', phone(screen(
    lt_bar, seg_bar(DESK_SEGS, 'accept', large=True), lt_tools,
    body=rows(lt_rows),
)))

lt_menu = f'''<div class="absolute right-3 top-16 z-30 w-72 overflow-hidden rounded-control bg-popover py-1 shadow-overlay" role="menu" aria-label="More options">
      <a href="S39-export.html#S39-large-text" role="menuitem" class="flex min-h-16 items-center gap-4 px-4 text-title-2 font-normal" data-action="export">{icon("file-down", "size-6 text-muted-foreground")}Export</a>
      <a href="S30-round-history.html#S30-large-text" role="menuitem" class="flex min-h-16 items-center gap-4 px-4 text-title-2 font-normal" data-action="round-history">{icon("history", "size-6 text-muted-foreground")}Round history</a>
    </div>'''
F.add('S28-large-text-menu', 'Large text: Export and Round history in the overflow menu', phone(screen(
    lt_bar, seg_bar(DESK_SEGS, 'accept', large=True), lt_tools,
    body=rows(lt_rows), overlay=lt_menu,
)))

F.write(os.path.join(SCR, 'S28-results.html'), 'S28 Results',
        'Results per decision with counts, search, filters and sorting in every segment; shared lists switch between final decisions and my decisions; any decision can be changed from here. Spec: <a href="S28-results.md">S28-results.md</a>. Opened from <a href="S27-round-summary.html#S27-desk-round-2">S27</a>, S09 and <a href="S30-round-history.html">S30</a>; filters in <a href="S29-filter-sort.html">S29</a>.')


# ==================================================================================== S29
G = Frames('S29')


def fchip(text, n=None, on=False, ic=None, role=None, href=None, large=False):
    disabled = n == 0 and not on
    if on:
        cls = 'border border-primary bg-primary-soft text-primary-soft-foreground'
        lead = icon('check', 'size-4')
    else:
        cls = 'border border-input'
        lead = icon(ic, 'size-4 text-muted-foreground') if ic else ''
    if disabled:
        cls += ' opacity-50'
    cnt = f' <span class="tabular-nums{"" if on else " text-muted-foreground"}">{fmt(n)}</span>' if n is not None else ''
    h = 'min-h-12 px-4 py-2 text-title-3 font-normal' if large else 'h-9 px-3 text-label'
    state = f'role="{role}" aria-checked="{"true" if on else "false"}"' if role else f'aria-pressed="{"true" if on else "false"}"'
    dis = ' disabled' if disabled else ''
    if href and not disabled:
        return f'<a href="{href}" {state} class="inline-flex items-center gap-1.5 rounded-full {h} {cls}">{lead}{text}{cnt}</a>'
    return f'<button type="button" {state} class="inline-flex items-center gap-1.5 rounded-full {h} {cls}"{dis}>{lead}{text}{cnt}</button>'


def fgroup(label, chips, trailing='', note='', large=False, role='group'):
    gid = uid('fg')
    nt = f'<p class="mt-1 text-body-sm text-muted-foreground">{note}</p>' if note else ''
    tl = 'text-title-2' if large else 'text-label'
    return f'''<div role="{role}" aria-labelledby="{gid}">
        <div class="flex min-h-6 items-center justify-between gap-3"><h3 id="{gid}" class="{tl}">{label}</h3>{trailing}</div>{nt}
        <div class="mt-2 flex flex-wrap gap-x-2 gap-y-3">{chips}</div>
      </div>'''


def sort_trigger(value, href='#S29-sort', large=False):
    t = 'text-title-3 font-normal' if large else 'text-body'
    return f'<a href="{href}" class="flex min-h-14 w-full items-center justify-between gap-3 rounded-control border border-input bg-card px-3.5 py-1.5" aria-haspopup="dialog" data-action="sort-field"><span><span class="block text-caption text-muted-foreground">Sort by</span><span class="block {t}">{value}</span></span>{icon("chevron-down", "size-5 text-muted-foreground")}</a>'


def footer(count, reset=True, apply_href='S28-results.html#S28-filtered', zero=False, large=False, ios=False):
    label = f'Show {fmt(count)} item{"" if count == 1 else "s"}'
    if zero:
        primary = f'<button type="button" class="inline-flex h-12 flex-1 items-center justify-center rounded-control bg-primary px-4 text-label-lg text-primary-foreground opacity-50" disabled>{label}</button>'
    else:
        primary = f'<a href="{apply_href}" class="inline-flex h-12 flex-1 items-center justify-center rounded-control bg-primary px-4 text-label-lg text-primary-foreground" data-action="apply">{label}</a>'
    if ios:
        return f'<div class="shrink-0 border-t bg-popover px-gutter pb-2 pt-3"><div class="flex">{primary}</div></div>'
    rd = '' if reset else ' disabled'
    rop = '' if reset else ' opacity-50'
    if large:
        return f'''<div class="shrink-0 space-y-2 border-t bg-popover px-gutter pb-4 pt-3">{primary.replace("h-12 flex-1", "min-h-16 w-full text-title-2")}<button type="button" class="inline-flex min-h-14 w-full items-center justify-center rounded-control text-title-2{rop}" data-action="reset"{rd}>Reset</button></div>'''
    return f'<div class="flex shrink-0 gap-3 border-t bg-popover px-gutter pb-4 pt-3"><button type="button" class="inline-flex h-12 items-center justify-center rounded-control border border-input bg-card px-5 text-label-lg{rop}" data-action="reset"{rd}>Reset</button>{primary}</div>'


def fs_sheet(sub, body, foot, close_href='S28-results.html#S28-shared-mine', head=None, top='top-12', extra='', handle=True, scrolled=False):
    hid = uid('fs')
    h = head(hid) if head else sheet_head('Filter and sort', hid, close_href, sub)
    if scrolled:
        h = f'<div class="shrink-0 border-b pb-2">{h}</div>'
    inner = f'''{h}
    <div class="min-h-0 flex-1 overflow-hidden px-gutter pt-4"><div class="space-y-6 {extra}">{body}</div></div>
    {foot}'''
    return sheet(inner, hid, top=top, handle=handle)


# -------- Wedding guests, My decisions, Accept (48)
def wchips(field, values, filters, on=(), ic=None, items=MY_ACC, label_map=None, large=False, href=None):
    out = ''
    for v in values:
        n = facet(items, filters, field, v, cval)
        out += fchip((label_map or {}).get(v, v), n, v in on, (ic or {}).get(v) if isinstance(ic, dict) else ic, large=large, href=href)
    return out


def city_values(items, filters):
    cnt = {}
    for k in items:
        if all(cval(k, f) in vs for f, vs in filters.items() if f != 'city'):
            cnt[cval(k, 'city')] = cnt.get(cval(k, 'city'), 0) + 1
    allc = sorted({cval(k, 'city') for k in items}, key=lambda c: (-cnt.get(c, 0), trkey(c)))
    return allc, cnt


wf = WED_FILTER
cities, ccount = city_values(MY_ACC, wf)
STATUS_IC = {'agreed': 'check-check', 'pending': 'clock', 'conflict': 'git-compare-arrows'}
STATUS_LB = {'agreed': 'Agreed', 'pending': 'Pending', 'conflict': 'Conflict'}
MEMBER_LB = {'accept': 'Accepted', 'reject': 'Rejected', 'maybe': 'Maybe', 'none': 'Not decided'}
MEMBER_IC = {'accept': 'check', 'reject': 'x', 'maybe': 'circle-help', 'none': 'circle-dashed'}


def wed_body(filters, large=False, part='top', city_on=()):
    groups = []
    if part in ('top', 'all'):
        groups.append(sort_trigger('Recently decided', large=large))
        groups.append(f'<div><h3 class="{"text-title-2" if large else "text-title-3"}">Filters</h3><p class="mt-0.5 text-body-sm text-muted-foreground">Items must match every filter. Counts update as you choose.</p></div>')
        groups.append(fgroup('Side', wchips('side', ["Bride's", "Groom's"], filters, filters.get('side', ()), large=large), large=large))
        groups.append(fgroup('Relationship', wchips('rel', ['Friend', 'Colleague', 'Family'], filters, filters.get('rel', ()), large=large), large=large))
        if not large:
            top6 = cities[:6]
            groups.append(fgroup('City', wchips('city', top6, filters, city_on), f'<a href="#S29-value-picker" class="-my-3 inline-flex h-12 items-center text-label text-primary" data-action="all-values">Show all {len(cities)}</a>'))
    if part in ('bottom', 'all'):
        groups.append(fgroup('List status', wchips('status', ['agreed', 'pending', 'conflict'], filters, (), STATUS_IC, label_map=STATUS_LB)))
        member_sel = f'<a href="#S29-shared-scrolled" class="-my-3 inline-flex h-12 items-center gap-1 text-label text-primary" aria-haspopup="listbox" data-action="choose-member">Mert Aydın{icon("chevron-down", "size-4")}</a>'
        groups.append(fgroup('Decided by a member', wchips('mert', ['accept', 'reject', 'maybe', 'none'], filters, (), MEMBER_IC, label_map=MEMBER_LB), member_sel, 'Filter by what another member chose.'))
        notes_chips = fchip('Has a note', facet(MY_ACC, filters, 'note', True, cval), False, 'sticky-note') + fchip('Edited', facet(MY_ACC, filters, 'edited', True, cval), False, 'pencil-line')
        groups.append(fgroup('Notes and edits', notes_chips))
    return ''.join(groups)


wed_bg = strip(screen(wed_bar(), view_toggle('My decisions'), seg_bar(MINE_SEGS, 'accept'),
                      toolbar('Search 48 items in Accept', label='Search in Accept'), body=rows([mine_row(k) for k in MY_ACC[:8]])))
WSUB = 'My decisions in Accept, 48 items'

G.section('Filter and sort sheet', 'A bottom sheet over S28 for the segment on screen. Sort first (one choice), then filters by field values: AND across fields, OR within a field, the same vocabulary as S24. Chips show how many items each value would leave. "Show 12 items" applies; Reset clears everything back to Recently decided with no filters.')

G.add('S29-default', 'Default: Wedding guests, Side and Relationship chosen, Show 12 items', phone(wed_bg + scrim() + fs_sheet(WSUB, wed_body(wf), footer(12))))

G.add('S29-shared-scrolled', 'Scrolled: list status, decided by a member, notes and edits (shared lists)', phone(wed_bg + scrim() + fs_sheet(WSUB, wed_body(wf, part='bottom'), footer(12), scrolled=True)))

# value picker for City
city_filters = dict(wf)
city_sel = ('İstanbul', 'Ankara')
city_filters['city'] = set(city_sel)
n_city = len(matching(MY_ACC, city_filters, cval))
picker_chips = ''.join(fchip(c, ccount.get(c, 0), c in city_sel) for c in cities)


def picker_head(hid):
    return f'''<div class="flex shrink-0 items-center gap-1 px-gutter pt-1">{icon_btn("arrow-left", "Back to filters", "#S29-default", "back", "-ml-3", "size-5")}<div class="min-w-0 flex-1"><h2 id="{hid}" class="text-title-3">City</h2><p class="text-body-sm text-muted-foreground">2 selected</p></div></div>'''


G.add('S29-value-picker', 'Field with many values: search and multi-select chips (City)', phone(wed_bg + scrim() + fs_sheet(WSUB,
    f'''{search_field(f"Search {len(cities)} cities", label="Search cities")}
      <div role="group" aria-label="Cities"><p class="text-body-sm text-muted-foreground">Choose one or more. Values that would leave no items are dimmed.</p><div class="mt-3 flex flex-wrap gap-x-2 gap-y-3">{picker_chips}</div></div>''',
    footer(n_city), head=picker_head)))

# -------- Desk setup (products), Accept (8)


def pval(k, field):
    p = P[k]
    return {'store': p['store'], 'category': p['category'], 'price': p['price'], 'rating': p['rating']}[field]


def pmatch(k, f):
    if 'store' in f and P[k]['store'] not in f['store']:
        return False
    if 'category' in f and P[k]['category'] not in f['category']:
        return False
    if 'price' in f and not (f['price'][0] <= P[k]['price'] <= f['price'][1]):
        return False
    if 'rating' in f and (P[k]['rating'] is None or P[k]['rating'] < f['rating']):
        return False
    return True


def pfacet(field, value, f):
    g = {k: v for k, v in f.items() if k != field}
    g[field] = {value} if field in ('store', 'category') else value
    return sum(1 for k in DESK_ACC if pmatch(k, g))


STORES = ['Nordhaus', 'Oakline', 'Pixelhaus', 'Keystone', 'Greenroom', 'Lumen & Co']
CATS = ['Chair', 'Desk', 'Monitor', 'Keyboard', 'Accessory', 'Plant', 'Lamp']


def price_inputs(lo=None, hi=None, focus_hi=False, large=False):
    a, b = uid('pf'), uid('pt')

    def inp(i, lab, val, ph, focus):
        f = ' border-primary ring-2 ring-ring/30' if focus else ' border-input'
        v = f' value="{val}"' if val is not None else ''
        return f'<div><label for="{i}" class="text-body-sm text-muted-foreground">{lab}</label><div class="mt-1 flex h-12 items-center rounded-control border bg-card{f}"><input id="{i}" inputmode="decimal" placeholder="{ph}"{v} class="h-full min-w-0 flex-1 rounded-control bg-transparent px-3.5 text-body placeholder:text-muted-foreground"><span class="pr-3.5 text-body text-muted-foreground">EUR</span></div></div>'
    return f'<div class="grid grid-cols-2 gap-3">{inp(a, "From", lo, "24", False)}{inp(b, "To", hi, "649", focus_hi)}</div>'


def desk_body(f, focus_hi=False, sort='Recently decided'):
    lo, hi = f.get('price', (None, None))
    rating_on = f.get('rating')
    rchips = fchip('Any', None, rating_on is None, role='radio') + fchip('4 and up', pfacet('rating', 4.0, f), rating_on == 4.0, 'star', role='radio') + fchip('4.5 and up', pfacet('rating', 4.5, f), rating_on == 4.5, 'star', role='radio')
    groups = [
        sort_trigger(sort),
        '<div><h3 class="text-title-3">Filters</h3><p class="mt-0.5 text-body-sm text-muted-foreground">Items must match every filter. Counts update as you choose.</p></div>',
        fgroup('Store', ''.join(fchip(s, pfacet('store', s, f), s in f.get('store', ())) for s in STORES)),
        fgroup('Category', ''.join(fchip(c, pfacet('category', c, f), c in f.get('category', ())) for c in CATS)),
        f'''<div role="group" aria-label="Price"><h3 class="text-label">Price</h3><div class="mt-2">{price_inputs(lo, hi, focus_hi)}</div><p class="mt-2 text-body-sm text-muted-foreground">Prices in Accept go from €24 to €649.</p></div>''',
        fgroup('Rating', rchips, note='Items without a rating are left out when you choose one.', role='radiogroup'),
    ]
    return ''.join(groups)


desk_bg = strip(screen(desk_bar(), seg_bar(DESK_SEGS, 'accept'), desk_tools, body=rows(desk_rows(DESK_ACC))))
DSUB = 'Accept, 8 items'


def dcount(f):
    return sum(1 for k in DESK_ACC if pmatch(k, f))


G.add('S29-products', 'Products (Desk setup): store, category, price range, rating; nothing chosen yet', phone(desk_bg + scrim() + fs_sheet(DSUB, desk_body({}), footer(8, reset=False, apply_href='S28-results.html#S28-default'), close_href='S28-results.html#S28-default')))

f_price = {'price': (50, 500)}
assert dcount(f_price) == 5
G.add('S29-number-range', 'Number range: Price from 50 to 500 EUR, To field focused', phone(desk_bg + scrim() + fs_sheet(DSUB, desk_body(f_price, focus_hi=True), footer(5, apply_href='#S29-applied'), close_href='S28-results.html#S28-default', extra='-mt-56', scrolled=True)))

SORT_ROWS = [('calendar-clock', 'Recently decided', 'Decision time'), ('list-ordered', 'Original order', 'As imported'), ('type', 'Name', 'Text'),
             ('hash', 'Price', 'Number'), ('star', 'Rating', 'Number'), ('hash', 'Reviews', 'Number'), ('type', 'Store', 'Text'), ('type', 'Category', 'Text')]


def sort_list(selected='Price', direction='High to low', dirs=('Low to high', 'High to low'), large=False):
    out = ''
    for ic, name, typ in SORT_ROWS:
        on = name == selected
        panel = ''
        if on and dirs:
            panel = f'<div class="pb-3 pl-9">{segmented([(d, None) for d in dirs], direction, "Direction")}</div>'
        out += f'''<div><button type="button" role="radio" aria-checked="{"true" if on else "false"}" class="flex min-h-12 w-full items-center gap-4 py-2 text-left">{icon(ic, "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">{name}</span><span class="block text-body-sm text-muted-foreground">{typ}</span></span>{icon("check", "size-5 text-primary") if on else ""}</button>{panel}</div>'''
    return f'<div class="-mt-2 divide-y" role="radiogroup" aria-label="Sort by">{out}</div>'


def sort_head(hid):
    return f'''<div class="flex shrink-0 items-center gap-1 px-gutter pt-1">{icon_btn("arrow-left", "Back to filters", "#S29-products", "back", "-ml-3", "size-5")}<div class="min-w-0 flex-1"><h2 id="{hid}" class="text-title-3">Sort by</h2><p class="text-body-sm text-muted-foreground">Empty values always go last.</p></div></div>'''


G.add('S29-sort', 'Sort field: radio list with direction for the chosen field', phone(desk_bg + scrim() + fs_sheet(DSUB, sort_list(), footer(8, apply_href='S28-results.html#S28-sorted'), head=sort_head)))

f_none = {'store': {'Oakline'}, 'price': (100, 500)}
assert dcount(f_none) == 0
none_alert = f'''<div class="rounded-control border bg-card p-4" role="status">
      <p class="flex items-center gap-2 text-label">{icon("search-x", "size-5 shrink-0 text-muted-foreground")}No items match these filters</p>
      <p class="mt-1 text-body-sm text-muted-foreground">Remove a filter or choose other values. Oakline items in Accept cost €39 and €649.</p>
      <button type="button" class="-mb-2 mt-1 inline-flex h-12 items-center text-label-lg text-primary" data-action="reset">Reset filters</button>
    </div>'''
G.add('S29-no-results', 'No results preview: Show button disabled, reason and Reset', phone(desk_bg + scrim() + fs_sheet(DSUB, none_alert + desk_body(f_none), footer(0, zero=True), close_href='S28-results.html#S28-default')))

applied_ids = [k for k in DESK_ACC if pmatch(k, f_price)]
G.add('S29-applied', 'Applied: S28 shows the filter chip, the count and the 5 matching items', phone(screen(
    desk_bar(), seg_bar(DESK_SEGS, 'accept', links=DESK_SEG_LINKS),
    toolbar('Search 8 items in Accept', label='Search in Accept', filter_href='#S29-number-range', n_filters=1,
            applied=[('Price: €50 to €500', 'Price from 50 to 500 EUR')]),
    count_line('5 of 8 items'),
    body=rows(desk_rows(applied_ids)),
    overlay=snackbar('Filters applied', None, 'bottom-4'),
)))

G.section('States, platforms and large text', 'Counts are computed on the phone from the working copy, so there is no loading or offline state for this sheet (lists over 5,000 items show "Counting…" in the button for up to a second). iOS uses a page sheet with Cancel and Reset in the bar; desktop web keeps the sheet inside the centered column.')


def ios_head(hid):
    return f'''<div class="grid shrink-0 grid-cols-[1fr_auto_1fr] items-center gap-2 px-3">
      <div class="justify-self-start">{ios_text_btn("Cancel", href="S28-results.html#S28-ios", action="cancel")}</div>
      <h2 id="{hid}" class="text-body font-semibold">Filter and sort</h2>
      <div class="justify-self-end">{ios_text_btn("Reset", action="reset")}</div>
    </div>'''


ios_bg = strip(screen(ios_bar_html, seg_bar(DESK_SEGS, 'accept'), toolbar('Search 8 items in Accept', label='Search in Accept'), body=rows(desk_rows(DESK_ACC))))
G.add('S29-ios', 'iOS page sheet: Cancel and Reset in the bar, one button at the bottom', phone(ios_bg + scrim() + fs_sheet(DSUB, desk_body(f_price), footer(5, ios=True, apply_href='#S29-applied'), head=lambda h: IOS_GRAB + ios_head(h), top='top-3', handle=False), ios=True))

G.add('S29-web-desktop', 'Web, desktop: sheet in the column, Esc closes, Enter applies', desktop(desk_bg + scrim() + fs_sheet(DSUB, desk_body({}), footer(8, reset=False, apply_href='S28-results.html#S28-default') + hints([('Esc', 'Close'), ('Enter', 'Show items'), ('Tab', 'Next control')]), close_href='S28-results.html#S28-web-desktop', top='top-16'),
                                                                                               'swipesort.app/l/desk-setup/results'))


def lt_head(hid):
    return f'''<div class="flex shrink-0 items-center gap-1 px-gutter pt-1"><div class="min-w-0 flex-1"><h2 id="{hid}" class="text-title-1">Filter and sort</h2></div>{icon_btn("x", "Close", "S28-results.html#S28-large-text", "close", "-mr-3", "size-7")}</div>'''


lt_body = f'''{sort_trigger("Recently decided", large=True)}
      {fgroup("Side", wchips("side", ["Bride's", "Groom's"], wf, wf["side"], large=True), large=True)}
      {fgroup("Relationship", wchips("rel", ["Friend", "Colleague", "Family"], wf, wf["rel"], large=True), large=True)}
      {fgroup("City", wchips("city", cities[:3], wf, (), large=True), '<a href="#S29-value-picker" class="inline-flex min-h-12 items-center text-title-3 font-normal text-primary" data-action="all-values">Show all 14</a>', large=True)}'''
G.add('S29-large-text', 'Large text (200%): full-screen sheet, chips wrap, buttons stack', phone(fs_sheet(WSUB, lt_body, footer(12, large=True), head=lt_head, top='top-0', handle=False)))

# Background S28 markup inside S29 frames links back to S28's file, not to local anchors.
G.items = [f.replace('href="#S28-', 'href="S28-results.html#S28-') for f in G.items]
G.write(os.path.join(SCR, 'S29-filter-sort.html'), 'S29 Filter and sort',
        'The filter and sort sheet for a Results segment: field value chips with live counts, number ranges, many-value search, sort field and direction, Reset and "Show 12 items". Spec: <a href="S29-filter-sort.md">S29-filter-sort.md</a>. Opened from <a href="S28-results.html">S28</a>.')


# ==================================================================================== S30
H = Frames('S30')


def split(a, m, r, total=None, label=None):
    total = total or (a + m + r)

    def w(n):
        return f'w-[{round(n * 100 / total)}%]'
    parts = ''.join(f'<div class="{w(n)} bg-{k}"></div>' for k, n in (('reject', r), ('maybe', m), ('accept', a)) if n)
    return f'<div class="flex h-2 gap-0.5 overflow-hidden rounded-full bg-muted" aria-hidden="true">{parts}</div>'


def legend(a, m, r, trailing='', large=False):
    t = 'text-title-3 font-normal' if large else 'text-caption'
    items = ''.join(f'<span class="inline-flex items-center gap-1 text-{k}-soft-foreground">{icon(DEC[k][0], "size-4")}<span class="tabular-nums">{n}</span> {DEC[k][3]}</span>' for k, n in (('reject', r), ('maybe', m), ('accept', a)))
    lay = 'flex flex-col items-start gap-1' if large else 'flex flex-wrap items-center gap-x-3 gap-y-1'
    return f'<span class="{lay} {t}">{items}{trailing}</span>'


def dur(text):
    return f'<span class="ml-auto inline-flex items-center gap-1 text-muted-foreground">{icon("timer", "size-4")}{text}</span>'


def round_row(name, date, include, a, m, r, duration, href, info_href, info_label, last=False, badge_html='', large=False, extra='', info_cls='text-muted-foreground'):
    bb = '' if last else ' border-b'
    tt = 'text-title-1' if large else 'text-title-3'
    st = 'text-title-3 font-normal' if large else 'text-body-sm'
    info = f'<span class="flex shrink-0 items-start pr-1 pt-3">{icon_btn("info", info_label, info_href, "round-details", info_cls, "size-5")}</span>' if info_href else ''
    return f'''<!-- Proposed component: RoundRow --><li class="flex items-stretch">
      <a href="{href}" class="flex min-w-0 flex-1 flex-col gap-2 py-4 pl-4{"" if info_href else " pr-4"}" data-action="open-round">
        <span class="flex flex-wrap items-center gap-x-3 gap-y-1"><span class="{tt}">{name}</span>{badge_html}</span>
        <span class="{st} text-muted-foreground">{date}{f", sorted in {duration}" if duration else ""}<br>{include}</span>
        {split(a, m, r)}
        {legend(a, m, r, '', large)}
        {extra}
      </a>{info}
    </li>'''


def hist_bar(list_name, back_href, back_label):
    return back_bar('Round history', back_href, back_label, '', sub=list_name)


latest = f'''<div class="px-gutter pt-2">
    <ul class="overflow-hidden rounded-group bg-card"><li><a href="S28-results.html#S28-default" class="flex items-center gap-4 px-4 py-4" data-action="latest-results">
      <span class="min-w-0 flex-1 space-y-2"><span class="block text-title-3">Latest results</span><span class="block text-body-sm text-muted-foreground">The latest decision on each of the 20 items</span>{split(8, 1, 11)}{legend(8, 1, 11)}</span>
      {icon("chevron-right", "size-5 shrink-0 text-muted-foreground")}</a></li></ul>
  </div>'''
desk_rounds = f'''<div class="px-gutter pt-8">{section_header("Rounds, newest first")}
    <ul class="overflow-hidden rounded-group bg-card" aria-label="Rounds">
      {round_row("Round 2", "Oct 6", "Maybe pile from Round 1, 6 items, shuffled", 3, 1, 2, "2 min", "S28-results.html#S28-round-2", "#S30-round-2-detail", "Round 2 details")}
      {round_row("Round 1", "Oct 4", "All 20 items, original order", 5, 6, 9, "6 min", "S28-results.html#S28-round-1", "#S30-round-detail", "Round 1 details", last=True)}
    </ul>
  </div>'''
start_bar = f'<div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">{btn("Start a new round", "primary", "S24-start-round.html#S24-default", "new-round")}</div>'

H.section('Round history', 'Every round of a list, newest first, with the decision split, counts, what was included, card order, date and sorting time. Tapping a round opens S28 with that round\'s results; the info button opens the round details. "Latest results" on top is what Results and Export use (A-33).')

H.add('S30-default', 'Default: Desk setup, two finished rounds', phone(f'''{hist_bar("Desk setup", "S09-list-overview.html#S09-solo-round-done", "Back to Desk setup")}
  <div class="min-h-0 flex-1 overflow-hidden pb-6">{latest}{desk_rounds}</div>
  {start_bar}'''))


def detail_rows(pairs):
    return ''.join(f'<li class="flex min-h-12 items-start gap-4 px-4 py-3"><span class="w-28 shrink-0 text-body-sm text-muted-foreground">{k}</span><span class="min-w-0 flex-1 text-body">{v}</span></li>' for k, v in pairs)


def items_in_order(ids, decs, total, href):
    li = ''.join(f'<li class="flex min-h-14 items-center gap-3 px-4 py-2"><span class="w-5 shrink-0 text-right text-body-sm tabular-nums text-muted-foreground">{i + 1}</span>{thumb(k, "size-10")}<span class="line-clamp-2 min-w-0 flex-1 text-body">{P[k]["name"]}</span>{badge(decs[k])}</li>' for i, k in enumerate(ids))
    return f'''<ol class="divide-y overflow-hidden rounded-group bg-card" aria-label="Items in card order">{li}</ol>
      <a href="{href}" class="mt-1 inline-flex h-12 items-center px-1 text-label-lg text-primary" data-action="round-results">See all {total} items</a>'''


def round_detail(title, back, include, order, started, finished, duration, a, m, r, later, ids, decs, total, results_href):
    return f'''{back_bar(title, back, "Back to round history", "", sub="Desk setup")}
  <div class="min-h-0 flex-1 overflow-hidden pb-6">
    <div class="px-gutter pt-2"><div class="rounded-group bg-card p-4">
      <p class="text-label text-muted-foreground">Result</p>
      <div class="mt-3">{split(a, m, r)}</div>
      <div class="mt-3 flex flex-wrap gap-2" role="img" aria-label="{r} rejected, {m} maybe, {a} accepted">{badge("reject", f"{r} rejected")}{badge("maybe", f"{m} maybe")}{badge("accept", f"{a} accepted")}</div>
    </div></div>
    <div class="px-gutter pt-6">{section_header("Details")}<ul class="divide-y overflow-hidden rounded-group bg-card">{detail_rows([("Items", include), ("Card order", order), ("Started", started), ("Finished", finished), ("Sorting time", duration)])}</ul></div>
    {later}
    <div class="px-gutter pt-6">{section_header("Items in card order")}{items_in_order(ids, decs, total, results_href)}</div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">{btn(f"See {title} results", "primary", results_href, "round-results")}</div>'''


later1 = f'''<div class="px-gutter pt-6">{section_header("Changed in a later round")}<a href="S28-results.html#S28-round-2" class="flex items-center gap-4 rounded-group bg-card px-4 py-3" data-action="round-2">{icon("history", "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">Round 2 sorted the 6 Maybe items again</span><span class="block text-body-sm text-muted-foreground">3 accepted, 2 rejected, 1 still Maybe</span></span>{icon("chevron-right", "size-5 shrink-0 text-muted-foreground")}</a></div>'''
H.add('S30-round-detail', 'Round detail: included items, order, time, what changed later, items in card order', phone(round_detail(
    'Round 1', '#S30-default', 'All items (20)', 'Original order', 'Oct 4, 10:00', 'Oct 4, 10:06', '6 min', 5, 6, 9, later1,
    ['p01', 'p02', 'p03', 'p04', 'p05'], R1, 20, 'S28-results.html#S28-round-1')))

H.add('S30-round-2-detail', 'Round 2 detail: Maybe pile, shuffled order', phone(round_detail(
    'Round 2', '#S30-default', 'Maybe pile from Round 1 (6)', 'Shuffled', 'Oct 6, 12:30', 'Oct 6, 12:33', '2 min', 3, 1, 2, '',
    R2_ORDER[:5], R2, 6, 'S28-results.html#S28-round-2')))

# ---------------------------------------------------------------- shared, in progress
H.section('Shared lists and rounds in progress', 'On shared lists a round belongs to everyone: the Owner starts it (DM-15), the split shows list status (Agreed, Pending, Conflict) while it runs, and the detail lists each member\'s results. Sorting time is not shown on shared lists (A-71).')


def status_split(ag, co, pe):
    t = ag + co + pe
    return f'<div class="flex h-2 gap-0.5 overflow-hidden rounded-full bg-muted" aria-hidden="true"><div class="w-[{round(ag * 100 / t)}%] bg-foreground"></div><div class="w-[{round(co * 100 / t)}%] bg-foreground/50"></div></div>'


SW = {'agreed': 'bg-foreground', 'conflict': 'bg-foreground/50', 'pending': 'border border-input bg-muted'}


def status_legend(ag, co, pe, full=False):
    """Legend with a swatch per bar segment (same mapping as S09-shared) plus the status icon."""
    items = (('agreed', 'check-check', 'Agreed', 'Everyone chose the same', ag), ('conflict', 'git-compare-arrows', 'Conflict', 'Members chose differently', co), ('pending', 'clock', 'Pending', 'Not everyone has decided', pe))
    if full:
        li = ''.join(f'<li class="flex items-center gap-3 py-2"><span class="size-3 shrink-0 rounded-xs {SW[k]}" aria-hidden="true"></span>{icon(ic, "size-5 shrink-0")}<span class="min-w-0 flex-1"><span class="block text-body">{lab}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span><span class="text-title-3 tabular-nums">{n}</span></li>' for k, ic, lab, desc, n in items)
        return f'<!-- Proposed component: ListStatusLegend (S09) --><ul class="divide-y">{li}</ul>'
    return f'<span class="flex flex-wrap gap-x-3 gap-y-1 text-caption">' + ''.join(f'<span class="inline-flex items-center gap-1.5"><span class="size-2.5 shrink-0 rounded-xs {SW[k]}" aria-hidden="true"></span>{icon(ic, "size-4")}<span class="tabular-nums">{n}</span> {lab.lower() if k != "conflict" else ("conflicts" if n != 1 else "conflict")}</span>' for k, ic, lab, desc, n in items) + '</span>'


def _old_status_legend(ag, co, pe):
    return f'<span class="flex flex-wrap gap-x-3 gap-y-1 text-caption"><span class="inline-flex items-center gap-1">{icon("check-check", "size-4")}<span class="tabular-nums">{ag}</span> agreed</span><span class="inline-flex items-center gap-1">{icon("git-compare-arrows", "size-4")}<span class="tabular-nums">{co}</span> conflicts</span><span class="inline-flex items-center gap-1 text-muted-foreground">{icon("clock", "size-4")}<span class="tabular-nums">{pe}</span> pending</span></span>'


def member_progress(rows_):
    out = ''
    for who, name, done in rows_:
        out += f'<span class="flex items-center gap-3">{avatar(who, "size-6")}<span class="w-12 shrink-0 text-body-sm">{name}</span><span class="h-1.5 flex-1 overflow-hidden rounded-full bg-muted"><span class="block h-full w-[{done}%] rounded-full bg-primary"></span></span><span class="w-16 shrink-0 text-right text-caption tabular-nums text-muted-foreground">{done} / 100</span></span>'
    return f'<span class="mt-1 flex flex-col gap-2" role="img" aria-label="You 76 of 100 decided, Mert 85 of 100, Selin 43 of 100">{out}</span>'


progress_badge = badge('pending', 'In progress').replace('i-lucide-clock', 'i-lucide-hourglass')
w_round = f'''<li class="flex items-stretch">
      <a href="S28-results.html#S28-shared" class="flex min-w-0 flex-1 flex-col gap-2 py-4 pl-4" data-action="open-round">
        <span class="flex flex-wrap items-center gap-x-3 gap-y-1"><span class="text-title-3">Round 1</span>{progress_badge}</span>
        <span class="text-body-sm text-muted-foreground">All 100 items, original order. You started it on Sep 28.</span>
        <span class="text-label">List status</span>
        {status_split(32, 15, 53)}
        {status_legend(32, 15, 53)}
        <span class="mt-2 text-label">Members</span>
        {member_progress([("deniz", "You", 76), ("mert", "Mert", 85), ("selin", "Selin", 43)])}
      </a><span class="flex shrink-0 items-start pr-1 pt-3">{icon_btn("info", "Round 1 details", "#S30-shared-detail", "round-details", "text-muted-foreground", "size-5")}</span>
    </li>'''
H.add('S30-in-progress', 'In progress, shared (Wedding guests Round 1): list status and member progress', phone(f'''{hist_bar("Wedding guests", "S09-list-overview.html#S09-shared", "Back to Wedding guests")}
  <div class="min-h-0 flex-1 overflow-hidden pb-6">
    <div class="px-gutter pt-2">{section_header("Rounds, newest first")}<ul class="overflow-hidden rounded-group bg-card" aria-label="Rounds">{w_round}</ul>
    <p class="mt-3 px-1 text-body-sm text-muted-foreground">Finished rounds stay here with their results. As the Owner, you start new rounds for everyone.</p></div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">{btn("Continue sorting", "primary", "S25-sorting.html#S25-shared", "continue-sorting")}</div>'''))

mrows = ''
for who, name, role, done, a, m, r in (('deniz', 'Deniz (you)', 'Owner', 76, 48, 11, 17), ('mert', 'Mert', 'Decision Maker', 85, 50, 14, 21), ('selin', 'Selin', 'Collaborator', 43, 25, 10, 8)):
    mrows += f'''<li class="flex items-start gap-3 px-4 py-3">{avatar(who, "size-10")}<div class="min-w-0 flex-1 space-y-2">
        <div><p class="text-body">{name}</p>{role_line(role, f'<span class="tabular-nums">{done} / 100 decided</span>')}</div>
        {split(a, m, r, 100)}
        {legend(a, m, r)}
      </div></li>'''
H.add('S30-shared-detail', 'Shared round detail: who started it, rule, list status, per-member results', phone(f'''{back_bar("Round 1", "#S30-in-progress", "Back to round history", "", sub="Wedding guests")}
  <div class="min-h-0 flex-1 overflow-hidden pb-6">
    <div class="px-gutter pt-2"><div class="rounded-group bg-card p-4">
      <p class="flex items-center justify-between gap-3"><span class="text-label text-muted-foreground">List status</span>{progress_badge}</p>
      <div class="mt-3">{status_split(32, 15, 53)}</div>
      <div class="mt-2">{status_legend(32, 15, 53, full=True)}</div>
    </div></div>
    <div class="px-gutter pt-6">{section_header("Details")}<ul class="divide-y overflow-hidden rounded-group bg-card">{detail_rows([("Items", "All items (100)"), ("Card order", "Original order"), ("Started by", "You, Sep 28, 19:05"), ("Conflict rule", "Decision Maker decides (Mert)")])}</ul></div>
    <div class="px-gutter pt-6">{section_header("Members")}<ul class="divide-y overflow-hidden rounded-group bg-card" aria-label="Results by member">{mrows}</ul></div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">{btn("See Round 1 results", "primary", "S28-results.html#S28-shared", "round-results")}</div>'''))

# ---------------------------------------------------------------- single round, never sorted, loading
H.section('Single round, never sorted and loading', 'A list with one finished round (here archived, so read-only), a list that was never sorted (the empty state invites the first sort) and the loading skeleton.')

H.add('S30-single-round', 'Single finished round (Apartment viewings, archived: read-only)', phone(f'''{hist_bar("Apartment viewings", "S09-list-overview.html#S09-archived", "Back to Apartment viewings")}
  <div class="min-h-0 flex-1 overflow-hidden pb-6">
    <div class="mx-gutter mt-2 flex items-start gap-3 rounded-control border bg-card p-3" role="note">{icon("archive", "mt-0.5 size-5 shrink-0 text-muted-foreground")}<p class="text-body-sm">Apartment viewings is archived. Restore it from the list to start a new round.</p></div>
    <div class="px-gutter pt-6">{section_header("Rounds")}<ul class="overflow-hidden rounded-group bg-card" aria-label="Rounds">
      {round_row("Round 1", "Jul 21", "All 8 items, original order", 3, 1, 4, None, "S28-results.html#S28-archived", None, None, last=True)}
    </ul>
    <p class="mt-3 px-1 text-body-sm text-muted-foreground">Each new round adds its results here. Earlier rounds never change.</p></div>
  </div>'''))

H.add('S30-never-sorted', 'Never sorted (Frontend hiring, Q4): empty state with Start sorting', phone(f'''{hist_bar("Frontend hiring, Q4", "S09-list-overview.html#S09-default", "Back to Frontend hiring, Q4")}
  <div class="flex min-h-0 flex-1 flex-col items-center px-gutter pt-32 text-center">
    {icon("history", "size-8 text-muted-foreground")}
    <h2 class="mt-3 text-title-3">No rounds yet</h2>
    <p class="mt-1 max-w-xs text-body text-muted-foreground">Sort the list once and the results of each round will be kept here.</p>
    <div class="mt-6 w-full max-w-xs">{btn("Start sorting", "primary", "S25-sorting.html#S25-candidate", "start-sorting")}</div>
  </div>'''))

sk = ''.join(f'''<li class="space-y-3 px-4 py-4"><span class="block h-5 w-24 animate-pulse rounded-xs bg-muted"></span><span class="block h-4 w-56 animate-pulse rounded-xs bg-muted"></span><span class="block h-2 w-full animate-pulse rounded-full bg-muted"></span><span class="block h-4 w-48 animate-pulse rounded-xs bg-muted"></span></li>''' for _ in range(2))
H.add('S30-loading', 'Loading: skeleton rounds', phone(f'''{hist_bar("Desk setup", "S09-list-overview.html#S09-solo-round-done", "Back to Desk setup")}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pt-2"><p class="sr-only" role="status">Loading rounds</p><ul class="divide-y overflow-hidden rounded-group bg-card" aria-hidden="true">{sk}</ul></div>'''))

# ---------------------------------------------------------------- platforms
H.section('iOS and large text', 'iOS: back chevron with the list name, inset grouped list, the info button is the native detail disclosure (separate tap target from the row). Large text: the split bar stays full width, legend items wrap one per line.')

ios_hist = f'''{ios_bar(f'<a href="S09-list-overview.html#S09-ios" class="-ml-2 inline-flex h-12 items-center text-body text-primary" data-action="back">{icon("chevron-left", "size-6")}Desk setup</a>', 'Round history')}
  <div class="min-h-0 flex-1 overflow-hidden pb-6">{latest.replace("S28-results.html#S28-default", "S28-results.html#S28-ios")}<div class="px-gutter pt-8">{section_header("Rounds, newest first")}
    <ul class="overflow-hidden rounded-group bg-card" aria-label="Rounds">
      {round_row("Round 2", "Oct 6", "Maybe pile from Round 1, 6 items, shuffled", 3, 1, 2, "2 min", "S28-results.html#S28-round-2", "#S30-round-2-detail", "Round 2 details", info_cls="text-primary")}
      {round_row("Round 1", "Oct 4", "All 20 items, original order", 5, 6, 9, "6 min", "S28-results.html#S28-round-1", "#S30-round-detail", "Round 1 details", last=True, info_cls="text-primary")}
    </ul></div></div>
  <div class="shrink-0 px-gutter pb-2 pt-3">{btn("Start a new round", "primary", "S24-start-round.html#S24-ios", "new-round")}</div>'''
H.add('S30-ios', 'iOS', phone(ios_hist, ios=True))

lt_hist = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    {icon_btn("arrow-left", "Back to Desk setup", "S09-list-overview.html#S09-solo-round-done", "back", "", "size-7")}
    <div class="min-w-0 flex-1 px-1"><h1 class="text-title-1">Round history</h1></div>
  </header>
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-2">
    <ul class="overflow-hidden rounded-group bg-card"><li><a href="S28-results.html#S28-large-text" class="flex items-start gap-4 px-4 py-4" data-action="latest-results">
      <span class="min-w-0 flex-1 space-y-2"><span class="block text-title-1">Latest results</span><span class="block text-title-3 font-normal text-muted-foreground">The latest decision on each of the 20 items</span>{split(8, 1, 11)}{legend(8, 1, 11, large=True)}</span>
      {icon("chevron-right", "mt-2 size-6 shrink-0 text-muted-foreground")}</a></li></ul>
    <h2 class="px-1 pb-2 pt-8 text-title-3 font-normal text-muted-foreground">Rounds, newest first</h2>
    <ul class="overflow-hidden rounded-group bg-card" aria-label="Rounds">
    {round_row("Round 2", "Oct 6", "Maybe pile from Round 1, 6 items, shuffled", 3, 1, 2, "2 min", "S28-results.html#S28-round-2", "#S30-round-2-detail", "Round 2 details", large=True)}
    {round_row("Round 1", "Oct 4", "All 20 items, original order", 5, 6, 9, "6 min", "S28-results.html#S28-round-1", "#S30-round-detail", "Round 1 details", last=True, large=True)}
  </ul></div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3"><a href="S24-start-round.html#S24-large-text" class="inline-flex min-h-16 w-full items-center justify-center rounded-control bg-primary px-4 text-title-2 text-primary-foreground" data-action="new-round">Start a new round</a></div>'''
H.add('S30-large-text', 'Large text (200%): Latest results kept, legend one item per line', phone(lt_hist))

H.write(os.path.join(SCR, 'S30-round-history.html'), 'S30 Round history',
        'Each round of a list with its results: decision split, counts, what was included, card order, date and sorting time; round details; shared rounds in progress. Spec: <a href="S30-round-history.md">S30-round-history.md</a>. Opens <a href="S28-results.html#S28-round-1">S28</a> filtered to a round.')
