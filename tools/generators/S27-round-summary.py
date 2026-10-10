# Usage: python3 tools/generators/S27-round-summary.py design/03-screens/S27-round-summary.html
# Generates the S27 Round summary mockup frames. Helpers: group_e_common.py.
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from group_e_common import *  # noqa

OUT = sys.argv[1]
F = Frames('S27')

# ---- Shared summary data (QA-003): Deniz (Owner, me) finishes Round 1. Her decisions on items she had not
# decided (c077–c100) = Mert's decision where Mert decided, else Accept. List status recomputed from the
# sample data with those decisions.
import json
_D = json.load(open(os.path.join(os.path.dirname(__file__), '../../design/02-data/sample-data.json')))
_my = dict(_D['shared']['myDecisions'])
for _it in _D['shared']['items']:
    _my.setdefault(_it['itemId'], _it['decisions'].get('u-mert') or 'accept')
DENIZ = {k: sum(1 for v in _my.values() if v == k) for k in ('reject', 'maybe', 'accept')}
STATUS = {'agreed': 0, 'pending': 0, 'conflict': 0}
for _it in _D['shared']['items']:
    _ds = dict(_it['decisions'], **{'u-deniz': _my[_it['itemId']]})
    _vals = [v for v in _ds.values() if v]
    STATUS['conflict' if len(set(_vals)) > 1 else ('agreed' if len(_vals) == len(_ds) else 'pending')] += 1
MERT_DONE = sum(1 for _it in _D['shared']['items'] if _it['decisions'].get('u-mert'))
SELIN_DONE = sum(1 for _it in _D['shared']['items'] if _it['decisions'].get('u-selin'))
assert sum(DENIZ.values()) == 100 and sum(STATUS.values()) == 100


# ------------------------------------------------------------------ parts
def hero(title, list_name, line, large=False, ic=True):
    if large:
        return f'''<div class="px-gutter pt-2">
      <h1 class="text-display">{title}</h1>
      <p class="mt-1 text-title-2 font-normal text-muted-foreground">{list_name}</p>
      <p class="mt-1 text-title-3 font-normal tabular-nums text-muted-foreground">{line}</p>
    </div>'''
    return f'''<div class="px-gutter pt-1 text-center">
      {f'<span class="mx-auto mb-3 flex size-12 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon("flag", "size-6")}</span>' if ic else ''}
      <h1 class="text-title-1">{title}</h1>
      <p class="mt-1 text-body text-muted-foreground">{list_name}</p>
      <p class="text-body-sm tabular-nums text-muted-foreground">{line}</p>
    </div>'''


def counts(r, m, a, total=None, label_prefix='', animating=False):
    total = total or (r + m + a)
    cols = ''
    for kind, n in (('reject', r), ('maybe', m), ('accept', a)):
        ic, _, state, past = DEC[kind]
        cols += f'''<div class="flex flex-col items-center gap-1.5">
        <span class="flex size-10 items-center justify-center rounded-full bg-{kind}-soft text-{kind}-soft-foreground">{icon(ic)}</span>
        <span class="text-display tabular-nums">{n}</span>
        <span class="text-label text-muted-foreground">{state}</span>
      </div>'''
    def w(n):
        return f'w-[{round(n * 100 / total)}%]' if total else 'w-0'
    aria = f'{r} rejected, {m} maybe, {a} accepted'
    live = ' aria-live="off"' if animating else ''
    return f'''<div class="px-gutter pt-6"{live}>
      <div class="grid grid-cols-3 gap-2" role="img" aria-label="{label_prefix}{aria}">{cols}</div>
      <div class="mx-auto mt-4 flex h-2 max-w-xs gap-0.5 overflow-hidden rounded-full bg-muted" aria-hidden="true"><div class="{w(r)} bg-reject"></div><div class="{w(m)} bg-maybe"></div><div class="{w(a)} bg-accept"></div></div>
    </div>'''


def arow(ic, title, desc, href=None, action=None, disabled=False, icon_cls='text-muted-foreground'):
    inner = f'''{icon(ic, f"size-5 shrink-0 {icon_cls}")}<span class="min-w-0 flex-1"><span class="block text-body{" text-muted-foreground" if disabled else ""}">{title}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span>'''
    if disabled:
        return f'<li><div class="flex min-h-16 items-center gap-4 px-4 py-3" aria-disabled="true">{inner}</div></li>'
    da = f' data-action="{action}"' if action else ''
    return f'<li><a href="{href}" class="flex min-h-16 items-center gap-4 px-4 py-3"{da}>{inner}{icon("chevron-right", "size-5 shrink-0 text-muted-foreground")}</a></li>'


def actions(rows, header='Next'):
    return f'''<div class="px-gutter pt-8">{section_header(header)}<ul class="divide-y overflow-hidden rounded-group bg-card">{''.join(rows)}</ul></div>'''


def bottom(primary, done_href='S09-list-overview.html#S09-default', extra=''):
    return f'''<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3">
    {extra}
    {primary}
    {btn("Done", "ghost", done_href, "done")}
  </div>'''


def summary_screen(body, primary, done_href='S09-list-overview.html#S09-default', close_href=None, banner='', extra_bottom='', header=None):
    hdr = header or f'''<header class="flex h-app-bar shrink-0 items-center px-1">{icon_btn("x", "Close summary", close_href or done_href, "close")}</header>'''
    return f'''{hdr}
  {banner}
  <div class="min-h-0 flex-1 overflow-hidden pb-6{' pt-5' if banner else ''}">{body}</div>
  {bottom(primary, done_href, extra_bottom)}'''


def list_status(agreed=None, pending=None, conflict=None, trailing='', loading=False):
    """Same bar mapping and legend as S09-shared: Agreed = bg-foreground, Conflict = bg-foreground/50,
    Pending = muted track. Each legend row has a swatch matching its segment (QA-023)."""
    agreed = STATUS['agreed'] if agreed is None else agreed
    pending = STATUS['pending'] if pending is None else pending
    conflict = STATUS['conflict'] if conflict is None else conflict
    if loading:
        return f'''<div class="px-gutter pt-8" aria-busy="true">{section_header("List status")}
      <div class="rounded-group bg-card p-4" role="status" aria-label="Loading list status"><div class="h-2 animate-pulse rounded-full bg-muted"></div><div class="mt-4 space-y-3">{''.join('<div class="flex items-center gap-3"><span class="size-5 animate-pulse rounded-full bg-muted"></span><span class="h-4 flex-1 animate-pulse rounded-full bg-muted"></span><span class="h-5 w-8 animate-pulse rounded-full bg-muted"></span></div>' for _ in range(3))}</div></div></div>'''
    t = agreed + pending + conflict

    def leg(sw, ic, label, desc, n):
        return f'<li class="flex items-center gap-3 py-2"><span class="size-3 shrink-0 rounded-full {sw}" aria-hidden="true"></span>{icon(ic, "size-5 shrink-0")}<span class="min-w-0 flex-1"><span class="block text-body">{label}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span><span class="text-title-3 tabular-nums">{n}</span></li>'
    legend = (leg('bg-foreground', 'check-check', 'Agreed', 'Everyone chose the same', agreed)
              + leg('bg-foreground/50', 'git-compare-arrows', 'Conflict', 'Members chose differently', conflict)
              + leg('border border-input bg-muted', 'clock', 'Pending', 'Not everyone has decided', pending))
    return f'''<div class="px-gutter pt-8">{section_header("List status", "", trailing or '<span class="text-caption text-muted-foreground">All 3 members</span>')}
      <div class="rounded-group bg-card p-4">
        <div class="flex h-2 gap-0.5 overflow-hidden rounded-full bg-muted" role="img" aria-label="{agreed} agreed, {conflict} in conflict, {pending} pending"><div class="w-[{round(agreed * 100 / t)}%] bg-foreground"></div><div class="w-[{round(conflict * 100 / t)}%] bg-foreground/50"></div></div>
        <ul class="mt-2 divide-y">{legend}</ul>
      </div>
    </div>'''


def still_sorting(rows, loading=False):
    if loading:
        lis = ''.join(f'<li class="flex min-h-16 items-center gap-3 px-4 py-3"><span class="size-10 animate-pulse rounded-full bg-muted"></span><div class="flex-1 space-y-2"><span class="block h-3.5 w-1/3 animate-pulse rounded-full bg-muted"></span><span class="block h-1.5 w-2/3 animate-pulse rounded-full bg-muted"></span></div></li>' for _ in rows)
    else:
        lis = ''
        for who, name, done, role in rows:
            rl = f' <span class="text-muted-foreground">{role}</span>' if role else ''
            lis += f'''<li class="flex min-h-14 items-center gap-3 px-4 py-2.5">{avatar(who, "size-8")}<div class="min-w-0 flex-1"><p class="text-body">{name}{rl}</p><div class="mt-1.5 flex items-center gap-3"><div class="h-1.5 flex-1 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="{done}" aria-valuemin="0" aria-valuemax="100" aria-label="{name}: {done} of 100 decided"><div class="h-full w-[{done}%] rounded-full bg-primary"></div></div><span class="text-caption tabular-nums text-muted-foreground">{done} / 100</span></div></div></li>'''
    return f'''<div class="px-gutter pt-8">{section_header("Still sorting")}<ul class="divide-y overflow-hidden rounded-group bg-card">{lis}</ul></div>'''


backup_line = f'''<a href="S05-sign-in-prompt.html#S05-backup" class="flex min-h-12 items-center gap-2 rounded-control px-1 text-body-sm text-muted-foreground" data-action="back-up">{icon("cloud-off", "size-4 shrink-0")}<span class="flex-1">Saved on this phone only</span><span class="text-label text-primary">Back up</span></a>'''

REVIEW = lambda href='S28-results.html#S28-default': btn('Review results', 'primary', href, 'review-results')


def solo_rows(maybe_n, maybe_href='S24-start-round.html#S24-maybe', export='S39-export.html#S39-default', maybe_disabled=False):
    if maybe_disabled:
        mrow = arow('circle-help', 'Re-sort Maybe', 'Nothing in Maybe this round', disabled=True)
    else:
        mrow = arow('circle-help', f'Re-sort Maybe ({maybe_n})', f'Sort the {maybe_n} Maybe {"item" if maybe_n == 1 else "items"} again in a new round', maybe_href, 'resort-maybe', icon_cls='text-maybe-soft-foreground')
    return [mrow,
            arow('list-restart', 'Start a new round', 'Choose items and card order', 'S24-start-round.html#S24-default', 'new-round'),
            arow('file-down', 'Export', 'CSV, Excel, Google Sheets or a text summary', export, 'export')]


# ------------------------------------------------------------------ solo
F.section('Solo list', 'S27 replaces S25 after the last decision (500 ms after the commit, success haptic). One orchestrated moment: the three counts count up once (500 ms). Counts follow the decision order Reject, Maybe, Accept.')

default_body = f'''{hero('Round 1 complete', 'Wedding guests', '100 / 100 decided in 38 min')}
    {counts(24, 14, 62)}
    {actions(solo_rows(14))}'''
F.add('S27-default', 'Default: Wedding guests, solo, Round 1 complete', phone(summary_screen(default_body, REVIEW(), extra_bottom=backup_line)))

first_body = f'''{hero('Round 1 complete', 'Wedding guests', '85 / 85 decided in 31 min')}
    {counts(20, 12, 53)}
    {actions(solo_rows(12))}'''
F.add('S27-first-round', 'First round ever (end of flow 1): 85 imported contacts, not signed in', phone(summary_screen(first_body, REVIEW(), extra_bottom=backup_line)))

countup_body = f'''{hero('Round 1 complete', 'Wedding guests', '85 / 85 decided in 31 min')}
    {counts(10, 6, 27, 85, animating=True)}
    {actions(solo_rows(12))}'''
F.add('S27-count-up', 'Entrance: counts counting up (250 of 500 ms); reduced motion shows the final numbers at once', phone(summary_screen(countup_body, REVIEW(), extra_bottom=backup_line)))

desk_body = f'''{hero('Round 2 complete', 'Desk setup', '6 / 6 decided in 2 min')}
    {counts(2, 1, 3)}
    <div class="px-gutter pt-8">{section_header("List totals after 2 rounds")}
      <div class="rounded-group bg-card p-4">
        <div class="flex h-2 gap-0.5 overflow-hidden rounded-full bg-muted" role="img" aria-label="List totals: 11 rejected, 1 maybe, 8 accepted"><div class="w-[55%] bg-reject"></div><div class="w-[5%] bg-maybe"></div><div class="w-[40%] bg-accept"></div></div>
        <div class="mt-3 flex flex-wrap gap-2">{badge('reject', '11 rejected')}{badge('maybe', '1 maybe')}{badge('accept', '8 accepted')}</div>
      </div>
    </div>
    {actions(solo_rows(1))}'''
F.add('S27-desk-round-2', 'Desk setup, Round 2 (Maybe pile re-sorted)', phone(summary_screen(desk_body, REVIEW(), 'S09-list-overview.html#S09-solo-round-done')))

nomaybe_body = f'''{hero('Round 1 complete', 'Frontend hiring, Q4', '12 / 12 decided in 9 min')}
    {counts(8, 0, 4)}
    {actions(solo_rows(0, maybe_disabled=True))}'''
F.add('S27-no-maybe', 'Maybe pile empty: Re-sort Maybe unavailable with the reason', phone(summary_screen(nomaybe_body, REVIEW())))

early_body = f'''{hero('Round 1 ended', 'Wedding guests', '88 / 100 decided')}
    {counts(20, 13, 55, 100)}
    <div class="px-gutter pt-6">
      <div class="flex items-start gap-3 rounded-control border bg-card p-4" role="note">{icon("circle-dashed", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="text-label">12 items not decided</p><p class="mt-0.5 text-body-sm text-muted-foreground">They aren't in any pile. Continue Round 1 to decide them, or include them in a new round.</p><a href="S25-sorting.html#S25-default" class="-ml-2 mt-1 inline-flex h-12 items-center gap-1.5 rounded-control px-2 text-label text-primary" data-action="continue-round">{icon("play", "size-4")}Continue Round 1</a></div></div>
    </div>
    {actions(solo_rows(13))}'''
F.add('S27-ended-early', 'Round ended early: 12 items not decided, option to continue', phone(summary_screen(early_body, REVIEW())))

# ------------------------------------------------------------------ shared
F.section('Shared list', "My round is finished; the list is not. The summary shows my counts, the list status (Agreed, Pending, Conflict) and who is still sorting. The Decision Maker sees Review conflicts as the main action; only the Owner starts rounds.")

DR, DM, DA = DENIZ['reject'], DENIZ['maybe'], DENIZ['accept']
NC = STATUS['conflict']
owner_rows = [arow('git-compare-arrows', f'{NC} conflicts', 'Mert resolves them as Decision Maker', 'S36-conflicts.html#S36-default', 'review-conflicts'),
              arow('circle-help', f'Re-sort Maybe ({DM})', 'Ends Round 1 for everyone', 'S24-start-round.html#S24-round-in-progress', 'resort-maybe', icon_cls='text-maybe-soft-foreground'),
              arow('list-restart', 'Start a new round', 'Ends Round 1 for everyone', 'S24-start-round.html#S24-round-in-progress', 'new-round'),
              arow('file-down', 'Export', 'CSV, Excel, Google Sheets or a text summary', 'S39-export.html#S39-shared', 'export')]
SORTING = [('mert', 'Mert', MERT_DONE, 'Decision Maker'), ('selin', 'Selin', SELIN_DONE, '')]
owner_body = f'''{hero('Your Round 1 is done', 'Wedding guests', '100 / 100 decided', ic=False)}
    {counts(DR, DM, DA, label_prefix='My decisions: ')}
    {list_status()}
    {still_sorting(SORTING)}
    {actions(owner_rows)}'''
OWNER_PRIMARY = REVIEW('S28-results.html#S28-shared')
F.add('S27-shared', 'Shared, Owner (Deniz) finished; Mert and Selin still sorting', phone(summary_screen(owner_body, OWNER_PRIMARY, 'S09-list-overview.html#S09-shared')))

loading_body = f'''{hero('Your Round 1 is done', 'Wedding guests', '100 / 100 decided', ic=False)}
    {counts(DR, DM, DA, label_prefix='My decisions: ')}
    {list_status(loading=True)}
    {still_sorting([1, 2], loading=True)}'''
F.add('S27-shared-loading', 'Shared, loading the list status', phone(summary_screen(loading_body, OWNER_PRIMARY, 'S09-list-overview.html#S09-shared')))

offline_body = f'''{hero('Your Round 1 is done', 'Wedding guests', '100 / 100 decided', ic=False)}
    {counts(DR, DM, DA, label_prefix='My decisions: ')}
    {list_status(trailing='<span class="text-caption text-muted-foreground">As of 12 min ago</span>')}
    {actions(owner_rows)}'''
F.add('S27-offline', 'Shared, offline: decisions saved on this phone, status as of the last sync', phone(summary_screen(
    offline_body, OWNER_PRIMARY, 'S09-list-overview.html#S09-shared',
    banner=offline_banner("You're offline. Decisions are saved on this phone."))))

# ------------------------------------------------------------------ accessibility
F.section('Accessibility', 'At 200% text the counts become labeled rows and the title left-aligns. Screen readers hear one announcement: "Round 1 complete. 24 rejected, 14 maybe, 62 accepted." The count-up is not announced.')
big_counts = ''.join(f'<li class="flex min-h-16 items-center gap-4 px-4 py-3"><span class="flex size-12 shrink-0 items-center justify-center rounded-full bg-{k}-soft text-{k}-soft-foreground">{icon(DEC[k][0], "size-6")}</span><span class="flex-1 text-title-2 font-normal">{DEC[k][2]}</span><span class="text-title-1 tabular-nums">{n}</span></li>' for k, n in (('reject', 24), ('maybe', 14), ('accept', 62)))
big_body = f'''{hero('Round 1 complete', 'Wedding guests', '100 / 100 decided in 38 min', large=True)}
    <div class="px-gutter pt-6"><ul class="divide-y overflow-hidden rounded-group bg-card" aria-label="My decisions">{big_counts}</ul></div>
    <div class="px-gutter pt-6"><ul class="divide-y overflow-hidden rounded-group bg-card"><li><a href="S24-start-round.html#S24-maybe" class="flex min-h-16 items-center gap-4 px-4 py-3 text-title-2 font-normal" data-action="resort-maybe">{icon("circle-help", "size-6 shrink-0 text-maybe-soft-foreground")}<span class="flex-1">Re-sort Maybe (14)</span></a></li></ul></div>'''
big_bottom = f'''<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3">{btn("Review results", "primary", "S28-results.html#S28-default", "review-results", h="min-h-16", extra="text-title-2")}</div>'''
F.add('S27-large-text', 'Large text (200%)', phone(f'''<header class="flex min-h-16 shrink-0 items-center px-1">{icon_btn("x", "Close summary", "S09-list-overview.html#S09-default", "close", "", "size-7")}</header>
  <div class="min-h-0 flex-1 overflow-hidden pb-6">{big_body}</div>
  {big_bottom}'''))

# ------------------------------------------------------------------ iOS and web
F.section('iOS and web', 'iOS: Done sits in the navigation bar (no close icon); the summary replaces the sorting modal without a slide. Web: same layout; on desktop Enter runs the main action.')
ios = summary_screen(default_body, btn('Review results', 'primary', 'S28-results.html#S28-default', 'review-results', extra='rounded-full'),
                     header=ios_bar('', '<span class="sr-only">Round summary</span>', ios_text_btn('Done', True, 'S09-list-overview.html#S09-default', 'done')))
ios = ios.replace(btn("Done", "ghost", 'S09-list-overview.html#S09-default', "done"), '')
F.add('S27-ios', 'iOS', phone(ios, ios=True))

desk_owner = summary_screen(owner_body, OWNER_PRIMARY, 'S09-list-overview.html#S09-shared')
F.add('S27-web-desktop', 'Web, desktop: Deniz finished sorting in the browser', desktop(desk_owner, 'swipesort.app/l/7Hq2xK/summary', hints([('Enter', 'Review results'), ('Esc', 'Done')])))

F.write(OUT, 'S27 Round summary', 'The end of a round: my counts, what happened to the list and the next actions (review results, re-sort Maybe, start a new round, export). Spec: <a href="S27-round-summary.md">S27-round-summary.md</a>.')
