# Usage: python3 tools/generators/S27-round-summary.py design/03-screens/S27-round-summary.html
# Generates the S27 Round summary mockup frames. Helpers: group_e_common.py.
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from group_e_common import *  # noqa

OUT = sys.argv[1]
F = Frames('S27')


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


def list_status(agreed=32, pending=53, conflict=15, trailing='', loading=False):
    if loading:
        return f'''<div class="px-gutter pt-8" aria-busy="true">{section_header("List status")}
      <div class="rounded-group bg-card p-4" role="status" aria-label="Loading list status"><div class="h-2 animate-pulse rounded-full bg-muted"></div><div class="mt-4 flex gap-2"><span class="h-7 w-24 animate-pulse rounded-full bg-muted"></span><span class="h-7 w-28 animate-pulse rounded-full bg-muted"></span><span class="h-7 w-24 animate-pulse rounded-full bg-muted"></span></div></div></div>'''
    t = agreed + pending + conflict
    return f'''<div class="px-gutter pt-8">{section_header("List status", "", trailing)}
      <div class="rounded-group bg-card p-4">
        <div class="flex h-2 gap-0.5 overflow-hidden rounded-full" role="img" aria-label="{agreed} agreed, {conflict} in conflict, {pending} pending"><div class="w-[{round(agreed * 100 / t)}%] bg-foreground"></div><div class="w-[{round(conflict * 100 / t)}%] bg-foreground/50"></div><div class="flex-1 bg-muted"></div></div>
        <div class="mt-3 flex flex-wrap gap-2">{badge('agreed', f'{agreed} agreed')}{badge('conflict', f'{conflict} conflicts')}{badge('pending', f'{pending} pending')}</div>
        <p class="mt-3 text-body-sm text-muted-foreground">Pending items wait for members who are still sorting.</p>
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

first_body = f'''{hero('Round 1 complete', 'Wedding guests', '100 / 100 decided in 38 min')}
    {counts(9, 5, 23, 100, animating=True)}
    {actions(solo_rows(14))}'''
F.add('S27-first-round', 'First round ever: counts counting up (250 of 500 ms); reduced motion shows S27-default at once', phone(summary_screen(first_body, REVIEW(), extra_bottom=backup_line)))

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

mert_rows = [arow('chart-no-axes-column', 'Review results', 'Final decisions and my decisions', 'S28-results.html#S28-shared', 'review-results'),
             arow('file-down', 'Export', 'CSV, Excel, Google Sheets or a text summary', 'S39-export.html#S39-shared', 'export')]
mert_body = f'''{hero('Your Round 1 is done', 'Wedding guests', '100 / 100 decided', ic=False)}
    {counts(27, 15, 58, label_prefix='My decisions: ')}
    {list_status()}
    {still_sorting([('deniz', 'Deniz', 76, 'Owner'), ('selin', 'Selin', 43, '')])}
    {actions(mert_rows)}
    <p class="px-gutter pt-2 text-body-sm text-muted-foreground">Deniz, the Owner, starts new rounds.</p>'''
REVIEW_CONFLICTS = btn('Review 15 conflicts', 'primary', 'S36-conflicts.html#S36-default', 'review-conflicts', ic='git-compare-arrows')
F.add('S27-shared', 'Shared, Decision Maker (Mert): Review conflicts first', phone(summary_screen(mert_body, REVIEW_CONFLICTS, 'S09-list-overview.html#S09-shared')))

owner_rows = [arow('git-compare-arrows', '15 conflicts', 'Mert resolves them as Decision Maker', 'S36-conflicts.html#S36-default', 'review-conflicts'),
              arow('circle-help', 'Re-sort Maybe (14)', 'Ends Round 1 for everyone', 'S24-start-round.html#S24-round-in-progress', 'resort-maybe', icon_cls='text-maybe-soft-foreground'),
              arow('list-restart', 'Start a new round', 'Ends Round 1 for everyone', 'S24-start-round.html#S24-round-in-progress', 'new-round'),
              arow('file-down', 'Export', 'CSV, Excel, Google Sheets or a text summary', 'S39-export.html#S39-shared', 'export')]
owner_body = f'''{hero('Your Round 1 is done', 'Wedding guests', '100 / 100 decided', ic=False)}
    {counts(24, 14, 62, label_prefix='My decisions: ')}
    {list_status()}
    {still_sorting([('mert', 'Mert', 85, 'Decision Maker'), ('selin', 'Selin', 43, '')])}
    {actions(owner_rows)}'''
F.add('S27-shared-owner', 'Shared, Owner (Deniz): new rounds end Round 1 for everyone', phone(summary_screen(owner_body, REVIEW('S28-results.html#S28-shared'), 'S09-list-overview.html#S09-shared')))

loading_body = f'''{hero('Your Round 1 is done', 'Wedding guests', '100 / 100 decided', ic=False)}
    {counts(27, 15, 58, label_prefix='My decisions: ')}
    {list_status(loading=True)}
    {still_sorting([1, 2], loading=True)}'''
F.add('S27-shared-loading', 'Shared, loading the list status', phone(summary_screen(loading_body, btn('Review conflicts', 'primary', disabled=True, ic='git-compare-arrows'), 'S09-list-overview.html#S09-shared')))

offline_body = f'''{hero('Your Round 1 is done', 'Wedding guests', '100 / 100 decided', ic=False)}
    {counts(27, 15, 58, label_prefix='My decisions: ')}
    {list_status(trailing='<span class="text-caption text-muted-foreground">As of 12 min ago</span>')}
    {actions(mert_rows)}'''
F.add('S27-offline', 'Shared, offline: my decisions saved on this phone, status as of the last sync', phone(summary_screen(
    offline_body, REVIEW_CONFLICTS, 'S09-list-overview.html#S09-shared',
    banner=offline_banner("You're offline. 4 decisions are saved on this phone and will sync later."))))

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

desk_mert = summary_screen(mert_body, REVIEW_CONFLICTS, 'S09-list-overview.html#S09-shared')
F.add('S27-web-desktop', 'Web, desktop: Mert finished sorting in the browser', desktop(desk_mert, 'swipesort.app/l/7Hq2xK/summary', hints([('Enter', 'Review conflicts'), ('Esc', 'Done')])))

F.write(OUT, 'S27 Round summary', 'The end of a round: my counts, what happened to the list and the next actions (review results, re-sort Maybe, start a new round, export). Spec: <a href="S27-round-summary.md">S27-round-summary.md</a>.')
