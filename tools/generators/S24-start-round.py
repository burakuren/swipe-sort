# Usage: python3 tools/generators/S24-start-round.py design/03-screens/S24-start-round.html
# Generates the S24 Start a round mockup frames. Helpers: group_e_common.py.
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from group_e_common import *  # noqa

OUT = sys.argv[1]
F = Frames('S24')

# Shared piles use FINAL decisions (QA-134): counted from sample-data.json shared.items (Agreed or resolved items).
import json
_D = json.load(open(os.path.join(os.path.dirname(__file__), '../../design/02-data/sample-data.json')))
FINAL = {k: sum(1 for i in _D['shared']['items'] if i.get('finalDecision') == k) for k in ('accept', 'reject', 'maybe')}
SM, SA = FINAL['maybe'], FINAL['accept']

DEMO_DESK = '../04-prototype/swipe-demo.html?deck=desk-maybe&amp;next=S27-desk-round-2'

# ------------------------------------------------------------------ building blocks
def opt(key, title, desc, count=None, kind=None, disabled=False, loading=False):
    return dict(key=key, title=title, desc=desc, count=count, kind=kind, disabled=disabled, loading=loading)


def wedding_items(maybe=None, accepted=None, all_=100, shared=False, custom_count=None, loading=False):
    if maybe is None:
        maybe = SM if shared else 11
    if accepted is None:
        accepted = SA if shared else 48
    md = 'Final decision is Maybe' if shared else 'Items marked Maybe in Round 1'
    ad = 'Final decision is Accept' if shared else 'Narrow down what you accepted'
    return [
        opt('all', 'All items', 'Every item in the list, decided or not', all_, None, loading=loading),
        opt('maybe', 'Maybe pile', md, maybe, 'maybe', loading=loading),
        opt('accepted', 'Accepted items', ad, accepted, 'accept', loading=loading),
        opt('custom', 'Custom selection', 'Filter by a field or pick items by hand', custom_count, None, loading=loading),
    ]


def radio_row(o, selected, extra_html='', large=False):
    on = o['key'] == selected
    dis = o['disabled']
    title_cls = 'text-muted-foreground' if dis else ''
    t = 'text-title-1 font-medium' if large else 'text-body'
    d = 'text-title-2 font-normal' if large else 'text-body-sm'
    if o['loading']:
        cnt = '<span class="block h-7 w-10 shrink-0 animate-pulse rounded-full bg-muted" aria-hidden="true"></span>'
    elif o['count'] is None:
        cnt = ''
    elif dis:
        cnt = count_chip(None, o['count'])
    else:
        cnt = count_chip(o['kind'], o['count'])
    label_count = '' if o['count'] is None or o['loading'] else f', {o["count"]} items'
    dattr = ' disabled' if dis else ''
    if large:
        cnt = cnt.replace('h-7', 'h-10').replace('text-label', 'text-title-3').replace('size-4', 'size-6')
        body = f'''<span class="min-w-0 flex-1"><span class="block {t} {title_cls}">{o["title"]}</span><span class="mt-0.5 block {d} text-muted-foreground">{o["desc"]}</span>{f'<span class="mt-2 block">{cnt}</span>' if cnt else ''}</span>'''
    else:
        body = f'''<span class="min-w-0 flex-1"><span class="block {t} {title_cls}">{o["title"]}</span><span class="block {d} text-muted-foreground">{o["desc"]}</span></span>{cnt}'''
    return f'''<div>
        <button type="button" role="radio" aria-checked="{"true" if on else "false"}" aria-label="{o["title"]}{label_count}. {o["desc"]}" class="flex min-h-16 w-full items-center gap-4 px-4 py-3 text-left"{dattr}>{radio_dot(on, dis)}{body}</button>
        {extra_html}
      </div>'''


ORDERS = [
    ('original', 'Original order', 'As the items were imported'),
    ('shuffled', 'Shuffled', 'A new random order for this round'),
    ('sorted', 'Sorted by a field', 'Choose a field and a direction'),
]


def select_trigger(value, label='Field', href=None, open_=False, ring=False):
    ring_cls = ' border-primary ring-2 ring-ring/30' if ring or open_ else ' border-input'
    exp = 'true' if open_ else 'false'
    inner = f'<span class="flex min-w-0 flex-col items-start"><span class="text-caption text-muted-foreground">{label}</span><span class="truncate text-body">{value}</span></span>{icon("chevron-down", "size-5 shrink-0 text-muted-foreground")}'
    cls = f'flex min-h-14 w-full items-center justify-between gap-3 rounded-control border bg-card px-3.5 py-1.5 text-left{ring_cls}'
    if href:
        return f'<a href="{href}" class="{cls}" aria-haspopup="listbox" aria-expanded="{exp}" aria-label="{label}: {value}" data-action="choose-sort-field">{inner}</a>'
    return f'<button type="button" class="{cls}" aria-haspopup="listbox" aria-expanded="{exp}" aria-label="{label}: {value}" data-action="choose-sort-field">{inner}</button>'


def sorted_panel(field='City', direction='A to Z', dirs=('A to Z', 'Z to A'), open_=False, popover=''):
    return f'''<div class="relative space-y-3 px-4 pb-4 pl-14">
          {select_trigger(field, 'Field', '#S24-sort-field-sheet', open_)}
          {popover}
          {segmented([(dirs[0], 'arrow-down-a-z' if dirs[0] == 'A to Z' else 'arrow-down-0-1'), (dirs[1], 'arrow-up-z-a' if dirs[1] == 'Z to A' else 'arrow-up-1-0')], direction, 'Direction')}
        </div>'''


def filter_row(field, op, value):
    return f'''<li class="flex items-center gap-1 rounded-control border bg-background pl-3.5">
              <a href="#S24-add-filter" class="flex min-h-12 min-w-0 flex-1 items-center gap-1.5 text-left text-body" aria-label="Edit filter: {field} {op} {value}"><span class="text-muted-foreground">{field}</span><span>{op} {value}</span></a>
              {icon_btn("x", f"Remove filter: {field} {op} {value}", None, None, "", "size-5")}
            </li>'''


def custom_panel(filters, match_text, none=False):
    rows = ''.join(filter_row(*f) for f in filters)
    if none:
        res = f'<p class="flex items-start gap-2 text-body-sm" role="status">{icon("circle-alert", "size-4 mt-0.5 shrink-0 text-destructive")}<span>No items match these filters. Remove a filter or choose other values.</span></p>'
    else:
        res = f'<p class="flex items-center gap-2 text-body-sm" role="status">{icon("layers", "size-4 shrink-0 text-muted-foreground")}<span class="tabular-nums">{match_text}</span></p>'
    return f'''<div class="space-y-3 px-4 pb-4 pl-14">
          <p class="text-body-sm text-muted-foreground">Items that match every filter</p>
          <ul class="space-y-2">{rows}</ul>
          <a href="#S24-add-filter" class="inline-flex h-12 items-center gap-2 rounded-control pr-3 text-label-lg text-primary" data-action="add-filter">{icon("plus")}Add filter</a>
          {res}
          <a href="#S24-custom-pick" class="inline-flex h-12 items-center gap-2 rounded-control pr-3 text-label-lg text-primary" data-action="pick-items">{icon("list-checks")}Pick items by hand instead</a>
        </div>'''


def order_group(order='original', panel='', large=False, disabled=False):
    rows = ''
    for key, title, desc in ORDERS:
        o = opt(key, title, desc, None, None, disabled)
        rows += radio_row(o, order, panel if key == 'sorted' and order == 'sorted' else '', large)
    return rows


def summary_bar(n, round_no, detail, button, note=''):
    noun = 'item' if n == 1 else 'items'
    return f'''<div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">
    <p class="flex items-center justify-center gap-2 text-body" role="status">{icon("layers", "size-5 shrink-0 text-muted-foreground")}<span class="tabular-nums">Round {round_no} will have {n} {noun}</span></p>
    <p class="mt-0.5 text-center text-body-sm text-muted-foreground">{detail}</p>
    <div class="mt-3">{button}</div>
    {note}
  </div>'''


def screen(list_name, items, selected, order='original', round_no=2, custom_html='', order_panel='', notice='', bottom='', header=None, banner='', large=False, items_header='Items', order_disabled=False, items_trailing='', overlay='', close_href='S09-list-overview.html#S09-default', scroll=''):
    item_rows = ''.join(radio_row(o, selected, custom_html if o['key'] == 'custom' and selected == 'custom' else '', large) for o in items)
    hdr = header or modal_bar('Start a round', list_name, close_href, 'Close', action='close')
    return f'''{hdr}
  {banner}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-2">
    <div class="{scroll}">
    {notice}
    {section_header(items_header, "pt-2", items_trailing)}
    <div class="divide-y overflow-hidden rounded-group bg-card" role="radiogroup" aria-label="Items in Round {round_no}">{item_rows}</div>
    {section_header("Card order", "pt-6")}
    <div class="divide-y rounded-group bg-card" role="radiogroup" aria-label="Card order">{order_group(order, order_panel, large, order_disabled)}</div>
    </div>
  </div>
  {bottom}
  {overlay}'''


def start_btn(href=None, action='start-round', disabled=False, text='Start round'):
    return btn(text, 'primary', href, action, disabled=disabled)


# ------------------------------------------------------------------ frames: core
F.section('Choose items and card order', 'A full-screen modal from S09 (Start new round) or S27 (Re-sort Maybe, Start a new round). Items: All, Maybe pile, Accepted items, Custom selection, each with its count. Card order: Original, Shuffled, Sorted by a field. The summary above Start round always states the round size.')

F.add('S24-default', 'Default: Maybe pile chosen (Wedding guests after Round 1)', phone(screen(
    'Wedding guests', wedding_items(), 'maybe', 'original',
    bottom=summary_bar(11, 2, 'Maybe pile, in original order', start_btn('#S24-started')),
)))

desk_items = [
    opt('all', 'All items', 'Every item in the list, decided or not', 20),
    opt('maybe', 'Maybe pile', 'Items marked Maybe in Round 1', 6, 'maybe'),
    opt('accepted', 'Accepted items', 'Narrow down what you accepted', 5, 'accept'),
    opt('custom', 'Custom selection', 'Filter by a field or pick items by hand', None),
]
F.add('S24-maybe', 'Re-sort Maybe: Maybe pile preselected, shuffled (Desk setup)', phone(screen(
    'Desk setup', desk_items, 'maybe', 'shuffled', close_href='S09-list-overview.html#S09-solo-round-done',
    bottom=summary_bar(6, 2, 'Maybe pile, shuffled', start_btn(DEMO_DESK)),
)))

F.add('S24-sorted-by', 'Sorted by a field: Accepted items by City, A to Z', phone(screen(
    'Wedding guests', wedding_items(), 'accepted', 'sorted', order_panel=sorted_panel('City', 'A to Z'), scroll='-mt-48',
    bottom=summary_bar(48, 2, 'Accepted items, sorted by City from A to Z', start_btn()),
)))

field_rows = [('Name', 'type', 'Text', True), ('Phone', 'phone', 'Phone', False), ('Email', 'mail', 'Email', False),
              ('Side', 'type', 'Text', False), ('Relationship', 'type', 'Text', False), ('City', 'type', 'Text', False)]


def field_sheet(selected='City'):
    rows = ''.join(f'''<div><button type="button" role="radio" aria-checked="{"true" if f == selected else "false"}" class="flex min-h-14 w-full items-center gap-4 px-gutter py-2 text-left">{icon(ic, "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">{f}</span><span class="block text-body-sm text-muted-foreground">{t}</span></span>{icon("check", "size-5 text-primary") if f == selected else ""}</button></div>''' for f, ic, t, _ in field_rows)
    return sheet(f'''<div class="flex items-center justify-between px-gutter pt-1"><h2 id="sfs" class="text-title-3">Sort by</h2>{icon_btn("x", "Close", "#S24-sorted-by", None, "-mr-3", "size-5")}</div>
    <div class="mt-2 divide-y" role="radiogroup" aria-labelledby="sfs">{rows}</div>
    <p class="px-gutter pb-6 pt-3 text-body-sm text-muted-foreground">Text sorts A to Z, numbers from low to high and dates from oldest. Change the direction after choosing.</p>''', 'sfs', top=None)


F.add('S24-sort-field-sheet', 'Choosing the sort field (Select as a bottom sheet)', phone(screen(
    'Wedding guests', wedding_items(), 'accepted', 'sorted', order_panel=sorted_panel('City', 'A to Z', open_=True),
    bottom=summary_bar(48, 2, 'Accepted items, sorted by City from A to Z', start_btn()),
    overlay=scrim() + field_sheet('City'),
)))

# ------------------------------------------------------------------ custom selection
F.section('Custom selection', "Filter by any field (field, condition, value chips) with a live count, or pick items by hand. Pseudo-fields My decision (and List status on shared lists) are filterable too.")

F.add('S24-custom', 'Custom selection with two filters and the resulting count', phone(screen(
    'Wedding guests', wedding_items(custom_count=12), 'custom', 'original',
    custom_html=custom_panel([('Side', 'is', "Bride's"), ('Relationship', 'is', 'Family')], '12 items match'),
    bottom=summary_bar(12, 2, 'Custom selection, in original order', start_btn()),
)))

chips = [('Family', 25, True), ('Friend', 47, False), ('Colleague', 28, False)]
chip_html = ''.join(
    (f'<button type="button" aria-pressed="true" class="inline-flex h-9 items-center gap-1.5 rounded-full border border-primary bg-primary-soft px-3 text-label text-primary-soft-foreground">{icon("check", "size-4")}{t} <span class="tabular-nums">{n}</span></button>' if on
     else f'<button type="button" aria-pressed="false" class="inline-flex h-9 items-center gap-1.5 rounded-full border border-input px-3 text-label">{t} <span class="tabular-nums text-muted-foreground">{n}</span></button>')
    for t, n, on in chips)
add_filter_sheet = sheet(f'''<div class="flex items-center justify-between px-gutter pt-1"><h2 id="afs" class="text-title-3">Add filter</h2>{icon_btn("x", "Close", "#S24-custom", None, "-mr-3", "size-5")}</div>
    <div class="space-y-5 px-gutter pb-6 pt-3">
      {select_trigger('Relationship', 'Field')}
      <div><p class="pb-2 text-label">Condition</p>{segmented([('is', None), ('is not', None)], 'is', 'Condition')}</div>
      <div><p class="pb-1 text-label">Values</p><p class="pb-3 text-body-sm text-muted-foreground">Choose one or more. Counts are for the whole list.</p><div class="flex flex-wrap gap-x-2 gap-y-3">{chip_html}</div></div>
      <p class="flex items-center gap-2 text-body-sm" role="status">{icon("layers", "size-4 shrink-0 text-muted-foreground")}With this filter, 12 items match</p>
      {btn("Add filter", "primary", "#S24-custom", "confirm-filter")}
    </div>''', 'afs', top=None)
F.add('S24-add-filter', 'Filter builder: field, condition, value chips, live count', phone(screen(
    'Wedding guests', wedding_items(custom_count=51), 'custom', 'original',
    custom_html=custom_panel([('Side', 'is', "Bride's")], '51 items match'),
    bottom=summary_bar(51, 2, 'Custom selection, in original order', start_btn()),
    overlay=scrim() + add_filter_sheet,
)))

F.add('S24-custom-none', 'Filters match no items: Start round disabled', phone(screen(
    'Wedding guests', wedding_items(custom_count=0), 'custom', 'original',
    custom_html=custom_panel([('City', 'is', 'Tokyo'), ('Relationship', 'is', 'Family')], '', none=True),
    bottom=summary_bar(0, 2, 'Change the filters to include at least 1 item', start_btn(disabled=True)),
)))

PICK = [
    ('c001', 'Ayşe Demir', "Bride's, Family", 'people/c001.svg', 'AD', True, 'maybe'),
    ('c002', 'Mehmet Yılmaz', "Bride's, Family", 'people/c002.svg', 'MY', True, 'accept'),
    ('c003', 'Zeynep Kaya', "Groom's, Family", 'people/c003.svg', 'ZK', False, 'accept'),
    ('c004', 'Emre Çelik', "Groom's, Friend", 'people/c004.svg', 'EÇ', True, 'maybe'),
    ('c005', 'Elif Şahin', "Bride's, Friend", 'people/c005.svg', 'EŞ', True, 'maybe'),
    ('c006', 'Burak Arslan', "Groom's, Colleague", 'people/c006.svg', 'BA', False, 'accept'),
    ('c007', 'Gökhan Doğan', "Groom's, Friend", None, 'GD', False, 'accept'),
    ('c008', 'İrem Aksoy', "Bride's, Colleague", 'people/c008.svg', 'İA', False, 'reject'),
    ('c009', 'Oğuz Kılıç', "Groom's, Family", None, 'OK', True, 'accept'),
    ('c010', 'Şule Erdoğan', "Bride's, Family", 'people/c010.svg', 'ŞE', False, 'reject'),
]
pick_rows = ''.join(f'''<li><button type="button" role="checkbox" aria-checked="{"true" if on else "false"}" class="flex min-h-16 w-full items-center gap-3 px-4 py-2 text-left">{checkbox(on)}{avatar((ph, ini), "size-10")}<span class="min-w-0 flex-1"><span class="block truncate text-body">{n}</span><span class="block truncate text-body-sm text-muted-foreground">{meta}</span></span>{badge(dec)}</button></li>''' for _, n, meta, ph, ini, on, dec in PICK)
pick = f'''{back_bar('Pick items', '#S24-custom', 'Back to round options', sub='12 selected')}
  <div class="shrink-0 px-gutter pb-3 pt-1">
    <div class="relative">{icon("search", "pointer-events-none absolute left-3.5 top-3.5 size-5 text-muted-foreground")}<input type="search" aria-label="Search items" placeholder="Search 100 items" class="h-12 w-full rounded-full border-0 bg-secondary pl-11 pr-4 text-body placeholder:text-muted-foreground"></div>
  </div>
  <div class="flex shrink-0 items-center justify-between px-gutter pb-1"><p class="text-label text-muted-foreground">Your Round 1 decision is shown on the right</p></div>
  <div class="min-h-0 flex-1 overflow-hidden px-gutter"><ul class="divide-y overflow-hidden rounded-group bg-card">{pick_rows}</ul></div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">{btn("Use 12 items", "primary", "#S24-custom", "use-items")}</div>'''
F.add('S24-custom-pick', 'Pick items by hand (search, multi-select)', phone(pick))

# ------------------------------------------------------------------ availability
F.section('Unavailable options and loading', 'Options with nothing in them stay visible but disabled, with the reason in place of the description. Counts load from the working copy; while counting, Start round waits.')

hire_items = [
    opt('all', 'All items', 'Every item in the list, decided or not', 12),
    opt('maybe', 'Maybe pile', 'Nothing in Maybe. Items you swipe up wait here.', 0, 'maybe', disabled=True),
    opt('accepted', 'Accepted items', 'Narrow down what you accepted', 4, 'accept'),
    opt('custom', 'Custom selection', 'Filter by a field or pick items by hand', None),
]
F.add('S24-empty-option', 'Empty Maybe pile: option disabled with the reason (Frontend hiring, Q4)', phone(screen(
    'Frontend hiring, Q4', hire_items, 'accepted', 'original',
    bottom=summary_bar(4, 2, 'Accepted items, in original order', start_btn()),
)))

F.add('S24-loading', 'Loading counts', phone(screen(
    'Wedding guests', wedding_items(loading=True), 'maybe', 'original',
    bottom=f'''<div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3" aria-busy="true">
    <p class="flex items-center justify-center gap-2 text-body text-muted-foreground" role="status">{icon("loader-circle", "size-5 shrink-0 animate-spin text-primary")}Counting items…</p>
    <p class="mt-0.5 text-center text-body-sm text-muted-foreground">Maybe pile, in original order</p>
    <div class="mt-3">{start_btn(disabled=True)}</div>
  </div>''',
)))

# ------------------------------------------------------------------ shared lists
F.section('Shared lists', "Rounds on shared lists are started by the Owner and apply to every member (DM-15). Piles use final decisions. Collaborators and the Decision Maker can propose a round and ask the Owner.")

shared_notice = f'''<div class="mb-4 flex items-start gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground" role="note">
      {avatar_stack(['deniz', 'mert', 'selin'], 'Deniz, Mert and Selin', 'size-8')}
      <div class="min-w-0 flex-1"><p class="text-label">Starts Round 2 for Deniz, Mert and Selin</p><p class="mt-0.5 text-body-sm">Everyone sorts the same items from the start. Round 1 stays in round history.</p></div>
    </div>'''
F.add('S24-shared-owner', 'Shared list, Owner: starts the round for everyone', phone(screen(
    'Wedding guests', wedding_items(shared=True), 'maybe', 'original', close_href='S09-list-overview.html#S09-shared', notice=shared_notice,
    items_trailing='<span class="text-caption text-muted-foreground">Based on final decisions</span>',
    bottom=summary_bar(SM, 2, 'Maybe pile, in original order, for 3 members', start_btn()),
)))

progress_note = f'''<div class="mb-4 rounded-control border bg-card p-4" role="note">
      <div class="flex items-start gap-3">{icon("flag", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="text-label">Round 1 is still open</p><p class="mt-0.5 text-body-sm text-muted-foreground">Starting Round 2 ends Round 1 for everyone. Decisions made so far are kept.</p></div></div>
      <ul class="mt-3 space-y-2 pl-8 text-body-sm">
        <li class="flex items-center gap-2">{avatar('deniz', 'size-6')}<span class="flex-1">You</span><span class="tabular-nums text-muted-foreground">76 / 100 decided</span></li>
        <li class="flex items-center gap-2">{avatar('mert', 'size-6')}<span class="flex-1">Mert</span><span class="tabular-nums text-muted-foreground">85 / 100 decided</span></li>
        <li class="flex items-center gap-2">{avatar('selin', 'size-6')}<span class="flex-1">Selin</span><span class="tabular-nums text-muted-foreground">43 / 100 decided</span></li>
      </ul>
    </div>'''
in_progress = screen(
    'Wedding guests', wedding_items(shared=True), 'maybe', 'original', close_href='S09-list-overview.html#S09-shared', notice=progress_note,
    items_trailing='<span class="text-caption text-muted-foreground">Based on final decisions</span>',
    bottom=summary_bar(SM, 2, 'Maybe pile, in original order, for 3 members', start_btn('#S24-end-round-dialog', 'start-round')),
)
F.add('S24-round-in-progress', 'A round is in progress: inline warning before ending it', phone(in_progress))

end_dialog = dialog('erd', 'End Round 1 for everyone and start Round 2?',
                    f'<p>Mert and Selin are still sorting. Decisions made so far are kept, and items nobody decided stay undecided.</p><p>Round 2 starts for all 3 members with {SM} items.</p>',
                    btn('Cancel', 'ghost', '#S24-round-in-progress', 'cancel', full=False) + btn('End Round 1 and start', 'primary', 'S25-sorting.html#S25-shared', 'confirm-end-round', full=False))
F.add('S24-end-round-dialog', 'Confirm: end the open round for everyone, then start (shared variant of S40-new-round)', phone(in_progress.replace('data-action="start-round"', '') + scrim('bg-scrim/50', 'z-20') + end_dialog))

collab_notice = f'''<div class="mb-4 flex items-start gap-3 rounded-control border bg-card p-4" role="note">
      {icon("lock", "size-5 mt-0.5 shrink-0 text-muted-foreground")}
      <div class="min-w-0 flex-1"><p class="text-label">Only Deniz can start rounds</p><p class="mt-0.5 text-body-sm text-muted-foreground">Rounds apply to every member, so the Owner starts them. Choose the items and order you'd like, then ask Deniz.</p></div>
    </div>'''
collab = screen(
    'Wedding guests', wedding_items(shared=True), 'maybe', 'original', close_href='S09-list-overview.html#S09-shared', notice=collab_notice, header=modal_bar('Suggest a round', 'Wedding guests', 'S09-list-overview.html#S09-shared', 'Close'),
    items_trailing='<span class="text-caption text-muted-foreground">Based on final decisions</span>',
    bottom=summary_bar(SM, 2, 'Maybe pile, in original order', btn('Ask Deniz', 'primary', '#S24-collaborator-asked', 'ask-owner', ic='send')).replace('will have', 'would have'),
)
F.add('S24-collaborator', "Collaborator (Selin): can't start, asks the Owner instead", phone(collab))
F.add('S24-collaborator-asked', 'After asking: request sent to the Owner', phone(collab.replace('data-action="ask-owner"', '') + snackbar('Asked Deniz to start Round 2', bottom='bottom-36')))

F.add('S24-offline', 'Shared list offline: starting for everyone needs a connection', phone(screen(
    'Wedding guests', wedding_items(shared=True), 'maybe', 'original', close_href='S09-list-overview.html#S09-shared',
    banner=offline_banner("You're offline. Decisions are saved on this phone. Starting a round for everyone needs a connection."),
    items_trailing='<span class="text-caption text-muted-foreground">Based on final decisions</span>',
    bottom=summary_bar(SM, 2, 'Maybe pile, in original order, for 3 members', start_btn(disabled=True),
                       '<p class="mt-2 text-center text-body-sm text-muted-foreground">Try again when you\'re online.</p>'),
)))

F.add('S24-start-failed', "Couldn't start: error snackbar with Try again", phone(screen(
    'Wedding guests', wedding_items(shared=True), 'maybe', 'original', close_href='S09-list-overview.html#S09-shared',
    items_trailing='<span class="text-caption text-muted-foreground">Based on final decisions</span>',
    bottom=summary_bar(SM, 2, 'Maybe pile, in original order, for 3 members', start_btn()),
    overlay=snackbar("Couldn't start Round 2. Check your connection and try again.", 'Try again', bottom='bottom-36', role='alert', ic='circle-alert'),
)))

# ------------------------------------------------------------------ result
F.section('After Start round', 'Start round replaces this modal with S25 at the first card of the new round. The snackbar names the action.')
ayse = s25_person('Ayşe Demir', 'Family', 'people/c001.svg', [('Phone', '+90 500 000 97 62'), ('Email', 'ayse.demir@example.com'), ('City', 'İstanbul')], ["Bride's"], note=('Mum insists. Seat near the family table.', 'sticky-note'))
F.add('S24-started', 'Round 2 started: S25 opens at the first Maybe item', phone(s25_live(
    ayse, 'Wedding guests', 'Round 2', 0, 11, (0, 0, 0), snackbar('Round 2 started', bottom='bottom-32'), undo=False,
    card_label='Ayşe Demir, Family. Phone +90 500 000 97 62. Email ayse.demir@example.com. City İstanbul. Note: Mum insists. Seat near the family table.')))

# ------------------------------------------------------------------ accessibility
F.section('Accessibility', 'At 200% text the counts move under each option and the descriptions wrap; the screen scrolls and the summary with Start round stays pinned.')
F.add('S24-large-text', 'Large text (200%)', phone(f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    {icon_btn("x", "Close", "S09-list-overview.html#S09-default", "close", "", "size-7")}
    <h1 class="min-w-0 flex-1 px-1 text-title-1">Start a round</h1>
  </header>
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-2">
    <h2 class="px-1 pb-2 text-title-3 font-normal text-muted-foreground">Items</h2>
    <div class="divide-y overflow-hidden rounded-group bg-card" role="radiogroup" aria-label="Items in Round 2">{''.join(radio_row(o, 'maybe', '', True) for o in wedding_items())}</div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">
    <p class="text-center text-title-2 font-normal tabular-nums" role="status">Round 2 will have 11 items</p>
    <div class="mt-3">{btn("Start round", "primary", None, "start-round", h="min-h-16", extra="text-title-2")}</div>
  </div>'''))

# ------------------------------------------------------------------ iOS and web
F.section('iOS and web', 'iOS presents the modal as a page sheet with Cancel in the navigation bar, trailing checkmarks instead of radio buttons and a pull-down menu for the sort field. Web uses the Android layout; on desktop the Select opens as a popover.')


def ios_row(title, desc, on, count_html=''):
    return f'''<div><button type="button" role="radio" aria-checked="{"true" if on else "false"}" class="flex min-h-14 w-full items-center gap-3 px-4 py-2.5 text-left"><span class="min-w-0 flex-1"><span class="block text-body">{title}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span>{count_html}<span class="flex size-6 shrink-0 items-center justify-center text-primary">{icon("check", "size-5") if on else ""}</span></button></div>'''


def ios_screen(menu=''):
    items = [('All items', 'Every item in the list', False, count_chip(None, 20)), ('Maybe pile', 'Marked Maybe in Round 1', True, count_chip('maybe', 6)),
             ('Accepted items', 'Narrow down what you accepted', False, count_chip('accept', 5)), ('Custom selection', 'Filter or pick by hand', False, '')]
    irows = ''.join(ios_row(*i) for i in items)
    orows = ios_row('Original order', 'As imported', False) + ios_row('Shuffled', 'New random order', False) + f'''<div class="relative"><button type="button" role="radio" aria-checked="true" class="flex min-h-14 w-full items-center gap-3 px-4 py-2.5 text-left"><span class="min-w-0 flex-1"><span class="block text-body">Sorted by a field</span></span><span class="flex size-6 shrink-0 items-center justify-center text-primary">{icon("check", "size-5")}</span></button>
          <div class="flex items-center gap-2 px-4 pb-3"><button type="button" class="inline-flex h-12 min-w-0 flex-1 items-center justify-between gap-2 rounded-control bg-secondary px-3.5 text-body" aria-haspopup="menu" aria-expanded="{"true" if menu else "false"}" aria-label="Field: Price">Price{icon("chevrons-up-down", "size-4 text-muted-foreground")}</button><button type="button" class="inline-flex h-12 items-center gap-2 rounded-control bg-secondary px-3.5 text-body" aria-label="Direction: low to high">{icon("arrow-down-0-1", "size-4")}Low to high</button></div>
          {menu}
        </div>'''
    return f'''<div class="absolute inset-0 bg-scrim/40" aria-hidden="true"></div>
  <div class="absolute inset-x-0 bottom-0 top-2 flex flex-col overflow-hidden rounded-t-sheet bg-background" role="dialog" aria-modal="true" aria-labelledby="ios-t">
    <div class="flex shrink-0 justify-center pt-1.5"><span class="h-1 w-9 rounded-full bg-muted-foreground/40"></span></div>
    {ios_bar(ios_text_btn("Cancel", href="S09-list-overview.html#S09-default", action="close"), '<span id="ios-t">Start a round</span>', '', 'Desk setup')}
    <div class="min-h-0 flex-1 overflow-hidden px-4 pt-2">
      <h2 class="px-4 pb-1.5 text-body-sm text-muted-foreground">Items</h2>
      <div class="divide-y overflow-hidden rounded-group bg-card" role="radiogroup" aria-label="Items">{irows}</div>
      <h2 class="px-4 pb-1.5 pt-5 text-body-sm text-muted-foreground">Card order</h2>
      <div class="divide-y rounded-group bg-card" role="radiogroup" aria-label="Card order">{orows}</div>
    </div>
    <div class="shrink-0 px-4 pb-2 pt-3">
      <p class="text-center text-body tabular-nums" role="status">Round 2 will have 6 items</p>
      <div class="mt-3">{btn("Start round", "primary", DEMO_DESK, None, extra="rounded-full")}</div>
    </div>
  </div>'''


F.add('S24-ios', 'iOS: page sheet, Cancel, checkmarks (Desk setup, sorted by Price)', phone(ios_screen(), ios=True))
ios_menu = '''<div class="absolute bottom-full left-4 z-20 mb-1 w-64 overflow-hidden rounded-group bg-popover shadow-overlay" role="menu" aria-label="Sort by">''' + ''.join(
    f'<button type="button" role="menuitemradio" aria-checked="{"true" if f == "Price" else "false"}" class="flex h-12 w-full items-center gap-3 border-b px-4 text-left text-body"><span class="flex size-5 shrink-0 items-center justify-center">{icon("check", "size-4") if f == "Price" else ""}</span>{f}</button>'
    for f in ['Name', 'Price', 'Rating', 'Reviews', 'Store', 'Category']) + '</div>'
F.add('S24-ios-sort-menu', 'iOS: sort field as a pull-down menu', phone(ios_screen(ios_menu), ios=True))

pop = '''<div class="absolute inset-x-4 bottom-full z-20 mb-1 overflow-hidden rounded-control bg-popover py-1.5 shadow-overlay" role="listbox" aria-label="Field">''' + ''.join(
    f'<div role="option" aria-selected="{"true" if f == "City" else "false"}" class="flex h-12 items-center gap-3 px-4 text-body {"bg-accent" if f == "Relationship" else ""}"><span class="flex size-5 shrink-0 items-center justify-center text-primary">{icon("check", "size-4") if f == "City" else ""}</span>{f}</div>'
    for f, *_ in field_rows) + '</div>'
web_scr = screen('Wedding guests', wedding_items(shared=True), 'accepted', 'sorted', order_panel=sorted_panel('City', 'A to Z', open_=True, popover=pop), scroll='-mt-48',
                 header=modal_bar('Start a round', 'Wedding guests', 'S09-list-overview.html#S09-shared', 'Close'),
                 items_trailing='<span class="text-caption text-muted-foreground">Based on final decisions</span>',
                 bottom=summary_bar(SA, 2, 'Accepted items, sorted by City from A to Z, for 3 members', start_btn('#S24-round-in-progress')))
F.add('S24-web-desktop', 'Web, desktop: Select opens as a popover', desktop(web_scr, 'swipesort.app/l/7Hq2xK/rounds/new', hints([('Esc', 'Close'), ('Enter', 'Start round')])))

F.write(OUT, 'S24 Start a round', 'Choose which items go into the next round and the card order. Spec: <a href="S24-start-round.md">S24-start-round.md</a>. Next: <a href="S25-sorting.html">S25 Sorting</a>.')
