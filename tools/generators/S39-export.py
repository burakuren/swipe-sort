# Usage: python3 tools/generators/S39-export.py design/03-screens/S39-export.html
# Generates the S39 Export flow mockup frames (Group H). Helpers: group_e_common.py (shared markup
# for buttons, bars, badges, sheets, snackbars), mirroring S25-sorting.py and components.html.
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from group_e_common import *  # noqa
from group_e_common import _strip_interactive

OUT = sys.argv[1] if len(sys.argv) > 1 else 'design/03-screens/S39-export.html'
F = Frames('S39')

# ------------------------------------------------------------------ origins and data
S28 = 'S28-results.html#S28-default'          # Desk setup results (Flow 2 origin)
S37 = 'S37-bulk-resolve.html#S37-summary'      # Wedding guests after bulk resolve (Flow 3 origin)
S09 = 'S09-list-overview.html#S09-default'

ACCOUNT = 'deniz.yilmaz@example.com'
MERT = 'mert.aydin@example.com'  # Flow 3: Mert (Decision Maker) exports right after bulk resolve

# Desk setup (l-desk): latest decision per item after Round 1 and Round 2 (A-33)
DESK = dict(name='Desk setup', all=20, reject=11, maybe=1, accept=8, rounds=2,
            fields=['Name', 'Price', 'Rating', 'Reviews', 'Store', 'Category', 'Link'])
# Wedding guests (l-wedding) after Mert's bulk resolve (S37): 22+6 accepted, 4+6 rejected, 6 maybe,
# 3 conflicts stay open, 53 pending.
WED = dict(name='Wedding guests', all=100, reject=10, maybe=6, accept=28, conflict=3, pending=53,
           fields=['Name', 'Phone', 'Email', 'Side', 'Relationship', 'City'])
# Apartment viewings (l-apartments, archived, Google Sheets source Flat hunt 2026)
APT = dict(name='Apartment viewings', all=8, reject=4, maybe=1, accept=3,
           fields=['Tab', 'Address', 'Rent', 'Rooms', 'Size', 'Viewing', 'Link'])
# Frontend hiring, Q4 (l-candidates): 8 rejected, 0 maybe, 4 accepted (S27-no-maybe)
HIRE = dict(name='Frontend hiring, Q4', all=12, reject=8, maybe=0, accept=4)

ACCEPTED_DESK = [('Ergo Mesh task chair', '€389'), ('Walnut sit-stand desk, 140 × 70 cm', '€649'),
                 ('27-inch 4K USB-C monitor', '€429'), ('Low-profile mechanical keyboard', '€129'),
                 ('Wool felt desk mat, large', '€39'), ('Monitor arm with gas spring, single', '€99'),
                 ('Pothos plant in matte pot', '€24'), ('Pendant lamp, opal glass', '€149')]
MAYBE_DESK = [('Bookshelf speakers, pair', '€249')]


def plural(n, one, many=None):
    return f'{n} {one if n == 1 else (many or one + "s")}'


# ------------------------------------------------------------------ building blocks
CHIP_DEC = {'reject': ('x', 'Rejected'), 'maybe': ('circle-help', 'Maybe'), 'accept': ('check', 'Accepted'),
            'conflict': ('git-compare-arrows', 'Conflicts'), 'all': ('layers', 'All items')}


def chip(kind, n, selected, large=False):
    """Scope chip (DecisionSegments look): icon + label + count, selected = inverted fill. 48 hit area."""
    ic, label = CHIP_DEC[kind]
    h, t, isz = ('h-14', 'text-title-3', 'size-6') if large else ('h-9', 'text-label', 'size-4')
    if selected:
        vis = f'bg-foreground text-background'
        ic_cls, n_cls = '', ''
    else:
        vis = 'border border-input bg-card'
        ic_cls = '' if kind in ('all', 'conflict') else f'text-{kind}-soft-foreground'
        ic_cls = ic_cls or 'text-muted-foreground'
        n_cls = 'text-muted-foreground'
    noun = 'item' if n == 1 else 'items'
    return f'''<button type="button" role="radio" aria-checked="{"true" if selected else "false"}" aria-label="{label}, {n} {noun}" class="flex min-h-12 items-center" data-action="scope-{kind}"><span class="inline-flex {h} items-center gap-1.5 rounded-full px-3 {t} {vis}">{icon(CHIP_DEC[kind][0], isz, ic_cls)}{label}<span class="tabular-nums {n_cls}">{n}</span></span></button>'''


def chips(d, selected, shared=False, large=False):
    kinds = ['all', 'reject', 'maybe', 'accept'] + (['conflict'] if shared else [])
    inner = ''.join(chip(k, d[k], k == selected, large) for k in kinds)
    return f'<div class="flex flex-wrap gap-x-2" role="radiogroup" aria-label="Items to export">{inner}</div>'


def switch_row(title, desc, on, large=False):
    t, s = ('text-title-2 font-normal', 'text-title-3 font-normal') if large else ('text-body', 'text-body-sm')
    vis = ('<span class="flex h-8 w-13 shrink-0 items-center rounded-full bg-primary p-1" aria-hidden="true"><span class="ml-auto size-6 rounded-full bg-primary-foreground"></span></span>' if on else
           '<span class="flex h-8 w-13 shrink-0 items-center rounded-full border-2 border-input bg-muted p-1" aria-hidden="true"><span class="size-5 rounded-full bg-muted-foreground"></span></span>')
    return f'''<li><button type="button" role="switch" aria-checked="{"true" if on else "false"}" class="flex min-h-16 w-full items-center gap-4 px-4 py-3 text-left"><span class="min-w-0 flex-1"><span class="block {t}">{title}</span><span class="block {s} text-muted-foreground">{desc}</span></span>{vis}</button></li>'''


def fmt_row(ic, title, desc, href, action, nav=True, state='ok', large=False):
    """Export-as row. nav=True rows open a next step (chevron); file rows act at once (no chevron)."""
    t, s, isz = ('text-title-2 font-normal', 'text-title-3 font-normal', 'size-7') if large else ('text-body', 'text-body-sm', 'size-6')
    if state != 'ok':
        reason = 'Needs a connection' if state == 'offline' else desc
        tail = icon('wifi-off', 'size-5 shrink-0 text-muted-foreground') if state == 'offline' else ''
        return f'''<li><div class="flex min-h-16 items-center gap-4 px-4 py-3" aria-disabled="true">{icon(ic, f"{isz} shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block {t} text-muted-foreground">{title}</span><span class="block {s} text-muted-foreground">{reason}</span></span>{tail}</div></li>'''
    tail = icon('chevron-right', 'size-5 shrink-0 text-muted-foreground') if nav else ''
    return f'''<li><a href="{href}" class="flex min-h-16 items-center gap-4 px-4 py-3" data-action="{action}">{icon(ic, f"{isz} shrink-0 text-primary")}<span class="min-w-0 flex-1"><span class="block {t}">{title}</span><span class="block {s} text-muted-foreground">{desc}</span></span>{tail}</a></li>'''


def group(rows, extra=''):
    return f'<ul class="divide-y overflow-hidden rounded-group bg-card {extra}">{"".join(rows)}</ul>'


def footer(text, large=False):
    s = 'text-title-3 font-normal' if large else 'text-body-sm'
    return f'<p class="px-1 pt-2 {s} text-muted-foreground">{text}</p>'


def safety(text, large=False):
    s = 'text-title-3 font-normal' if large else 'text-body-sm'
    return f'<p class="flex gap-2 px-1 {s} text-muted-foreground">{icon("shield-check", "size-4 mt-0.5 shrink-0")}<span>{text}</span></p>'


def head(text, large=False, first=False):
    pt = '' if first else ('pt-8' if large else 'pt-6')
    cls = 'text-title-3' if large else 'text-label'
    return f'<h2 class="px-1 pb-2 {pt} {cls} text-muted-foreground">{text}</h2>'


# ------------------------------------------------------------------ step 1: choose what to export
def formats(kind='desk', web=False, offline=False, empty=False, large=False, csv_href='#S39-file-exporting'):
    st = 'empty' if empty else 'ok'
    dl = web
    rows = []
    csv_d = 'Downloads a .csv file' if dl else 'Opens in any spreadsheet app'
    xls_d = 'Downloads an .xlsx file' if dl else 'For Excel and Numbers'
    if kind == 'apt':
        g_d, g_href = 'Add to Flat hunt 2026, or a new spreadsheet', '#S39-apartments-destination'
    elif kind == 'shared':
        g_d, g_href = 'A new spreadsheet in Google Drive', '#S39-shared-google-destination'
    else:
        g_d, g_href = 'A new spreadsheet in Google Drive', '#S39-google-destination'
    if empty:
        rows = [fmt_row('file-text', 'CSV file', csv_d, '', '', state='empty', large=large),
                fmt_row('file-spreadsheet', 'Excel file', xls_d, '', '', state='empty', large=large),
                fmt_row('sheet', 'Google Sheets', g_d, '', '', state='empty', large=large),
                fmt_row('message-square-text', 'Text summary', 'Counts and accepted items as text', '', '', state='empty', large=large)]
    else:
        rows = [fmt_row('file-text', 'CSV file', csv_d, csv_href, 'format-csv', nav=False, large=large),
                fmt_row('file-spreadsheet', 'Excel file', xls_d, csv_href, 'format-excel', nav=False, large=large),
                fmt_row('sheet', 'Google Sheets', g_d, g_href, 'format-google', state='offline' if offline else st, large=large),
                fmt_row('message-square-text', 'Text summary', 'Counts and accepted items as text', '#S39-text-summary', 'format-text', large=large)]
    return group(rows)


def step1(d, selected='all', shared=False, kind='desk', close_href=S28, banner='', web=False, offline=False,
          empty_note='', large=False, ios=False, overlay='', csv_href='#S39-file-exporting', safety_line=True):
    if shared:
        columns = [switch_row("Each member's decision", 'Adds a column for Deniz, Mert and Selin', True, large),
                   switch_row('Notes', 'Shared notes with their author', True, large)]
        col_footer = 'All fields and a Final decision column are always included. Private notes are never exported.'
        latest = 'Counts are final decisions. Pending items are only in All items.'
    else:
        columns = [switch_row('Notes', 'Adds a Notes column', True, large)]
        if d.get('rounds', 1) > 1:
            columns.append(switch_row("Each round's decision", 'Adds Round 1 and Round 2 columns', False, large))
        col_footer = 'All fields and a Decision column are always included.'
        latest = f'Each item has its latest decision from {d.get("rounds", 1)} rounds.' if d.get('rounds', 1) > 1 else 'Decisions from Round 1.'
    if empty_note:
        helper = f'<p class="flex items-start gap-2 px-1 pt-1 {"text-title-3 font-normal" if large else "text-body-sm"}" role="status">{icon("circle-dashed", "size-4 mt-0.5 shrink-0 text-muted-foreground")}<span>{empty_note}</span></p>'
    else:
        helper = footer(latest, large).replace('pt-2', 'pt-1')
    src = {'desk': f'Exporting creates a copy. Nothing in {d["name"]} changes.',
           'apt': 'Exporting creates a copy. Flat hunt 2026 changes only if you choose it and confirm.',
           'shared': f'Exporting creates a copy. Nothing in {d["name"]} changes for anyone.'}[kind]
    if ios:
        bar = ios_bar(f'<a href="{close_href}" class="flex size-12 items-center justify-center rounded-full text-primary" aria-label="Close export" data-action="close">{icon("x", "size-6")}</a>', 'Export', '', d['name'])
    elif large:
        bar = f'''<header class="flex min-h-app-bar shrink-0 items-center gap-1 px-1">
    {icon_btn("x", "Close export", close_href, "close", "", "size-7")}
    <div class="min-w-0 flex-1 px-1"><h1 class="text-title-1">Export</h1><p class="text-title-3 font-normal text-muted-foreground">{d["name"]}</p></div>
  </header>'''
    else:
        bar = modal_bar('Export', d['name'], close_href, 'Close export')
    body = f'''<div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-2">
    {head("Items", large, first=True)}
    {chips(d, selected, shared, large)}
    {helper}
    {head("Columns", large)}
    {group(columns)}
    {footer(col_footer, large)}
    {head("Export as", large)}
    {formats(kind, web, offline, bool(empty_note), large, csv_href)}
    {f'<div class="pt-4">{safety(src, large)}</div>' if safety_line else ''}
  </div>'''
    return f'{bar}\n  {banner}\n  {body}\n  {overlay}'


def static(html):
    """Non-interactive copy of a screen behind a sheet: links and buttons become divs with the same classes."""
    import re

    def tag(m):
        cls = re.search(r'class="([^"]*)"', m.group(2))
        return f'<div class="{cls.group(1)}">' if cls else '<div>'
    html = re.sub(r'<(a|button)\b([^>]*)>', tag, html)
    html = re.sub(r'</(a|button)>', '</div>', html)
    html = re.sub(r' (data-action|aria-label|role|tabindex|aria-checked|aria-modal|aria-labelledby|aria-disabled|id|for)="[^"]*"', '', html)
    html = re.sub(r'<h([12]) ', r'<p ', html)
    html = re.sub(r'</h[12]>', '</p>', html)
    return f'<div class="flex min-h-0 flex-1 flex-col" aria-hidden="true">{html}</div>'


# ------------------------------------------------------------------ shared parts for later steps
def step_bar(title, sub, back_href, back_label='Back to Export', close=False, close_href=S28):
    if close:
        return modal_bar(title, sub, close_href, 'Close export')
    return back_bar(title, back_href, back_label, '', sub)


def bottom(primary, secondary=''):
    sec = f'<div class="mt-1">{secondary}</div>' if secondary else ''
    return f'''<div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">
    {primary}{sec}
  </div>'''


def P(text, href=None, action=None, ic=None, disabled=False):
    return btn(text, 'primary', href, action, ic, h='h-14', disabled=disabled)


def G(text, href=None, action=None, ic=None):
    return btn(text, 'ghost', href, action, ic)


def O(text, href=None, action=None, ic=None):
    return btn(text, 'outline', href, action, ic)


def account_row(email=ACCOUNT, photo='people/u-deniz.svg', sub='Google account', switch_href='S15-google-sheets.html#S15-account-switch'):
    return f'''<div class="flex min-h-16 items-center gap-3 rounded-group bg-card py-2 pl-4 pr-2"><img src="{IMG}{photo}" alt="" class="size-10 shrink-0 rounded-full"><div class="min-w-0 flex-1"><p class="truncate text-body">{email}</p><p class="text-body-sm text-muted-foreground">{sub}</p></div><a href="{switch_href}" class="inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label-lg text-primary" data-action="switch-account" aria-label="Switch Google account">Switch</a></div>'''


def col_chips(existing, added, rows_text):
    ex = ''.join(f'<li class="inline-flex h-8 items-center rounded-sm border border-input px-2.5 text-body-sm">{c}</li>' for c in existing)
    ad = ''.join(f'<li class="inline-flex h-8 items-center gap-1 rounded-sm bg-primary-soft px-2.5 text-body-sm text-primary-soft-foreground">{icon("plus", "size-4")}{c}</li>' for c in added)
    return f'''<div class="rounded-group bg-card p-4">
      <p class="text-label">Your fields</p>
      <ul class="mt-2 flex flex-wrap gap-1.5" aria-label="Your fields">{ex}</ul>
      <p class="mt-4 text-label">Added by SwipeSort</p>
      <ul class="mt-2 flex flex-wrap gap-1.5" aria-label="Added columns">{ad}</ul>
      <p class="mt-4 text-body-sm text-muted-foreground">{rows_text}</p>
    </div>'''


def info_alert(title, body, ic='info'):
    return f'<div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground" role="note">{icon(ic, "size-5 shrink-0")}<div class="min-w-0 flex-1"><p class="text-label">{title}</p><p class="mt-0.5 text-body-sm">{body}</p></div></div>'


def fact_rows(rows):
    """Confirmation facts: icon, label, value. Rows inside one group."""
    lis = ''
    for ic, label, value in rows:
        lis += f'<li class="flex gap-4 px-4 py-3.5">{icon(ic, "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="text-label">{label}</p><p class="mt-0.5 text-body text-muted-foreground">{value}</p></div></li>'
    return f'<ul class="divide-y overflow-hidden rounded-group bg-card">{lis}</ul>'


def state(ic, title, body, tone='muted', extra='', spin=False, role=None):
    cls = {'muted': 'bg-muted text-muted-foreground', 'primary': 'bg-primary-soft text-primary-soft-foreground',
           'error': 'bg-muted text-destructive'}[tone]
    ic_html = icon(ic, 'size-7 animate-spin' if spin else 'size-7')
    r = f' role="{role}"' if role else ''
    return f'''<div class="flex min-h-0 flex-1 flex-col items-center justify-center px-8 pb-8 text-center"{r}>
    <span class="flex size-14 items-center justify-center rounded-full {cls}">{ic_html}</span>
    <h2 class="mt-5 text-title-2">{title}</h2>
    <p class="mt-2 max-w-xs text-body text-muted-foreground">{body}</p>
    {extra}
  </div>'''


def file_card(name, meta, ic='file-text'):
    return f'''<div class="flex min-h-16 items-center gap-3 rounded-group bg-card px-4 py-2">
      <span class="flex size-10 shrink-0 items-center justify-center rounded-sm bg-primary-soft text-primary-soft-foreground">{icon(ic)}</span>
      <div class="min-w-0 flex-1"><p class="truncate text-body">{name}</p><p class="truncate text-body-sm text-muted-foreground">{meta}</p></div>
    </div>'''


def bsheet(title_id, title, inner, actions='', close=True):
    cl = icon_btn('x', 'Close', '#S39-accepted', 'close-sheet', '-mr-3', 'size-5') if close else ''
    return f'''{scrim()}
  <div class="absolute inset-x-0 bottom-0 z-20 rounded-t-sheet bg-popover px-gutter pb-5 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="{title_id}">
    <div class="flex justify-center py-1.5"><span class="h-1 w-8 rounded-full bg-muted-foreground/40"></span></div>
    <div class="flex min-h-12 items-center justify-between gap-3 pt-1"><h2 id="{title_id}" class="text-title-3">{title}</h2>{cl}</div>
    {inner}
    <div class="mt-5 space-y-1">{actions}</div>
  </div>'''


# ================================================================== frames
INTRO = ('Export decisions to CSV, Excel or Google Sheets, or share a text summary. One short modal stack: choose items, '
         'columns and a format; Google Sheets adds a destination and an explicit write confirmation. '
         'Spec: <a href="S39-export.md">S39-export.md</a>. Entry points: S27 round summary, S28 results, S37 bulk resolve summary, S09 list overview.')

# ---------------------------------------------------------------- 1 choose
F.section('Choose what to export',
          'One screen sets everything a file needs: items (latest decision per item), columns, then the format. Tapping CSV or Excel exports at once; Google Sheets and Text summary open one more step.')

F.add('S39-default', 'Default: Desk setup after Round 2, all items', phone(step1(DESK)))
F.add('S39-accepted', 'Accepted items chosen (8)', phone(step1(DESK, 'accept')))
F.add('S39-shared', 'Shared list: Wedding guests, Mert exports after bulk resolve (Flow 3)',
      phone(step1(WED, 'all', shared=True, kind='shared', close_href=S37)))
F.add('S39-apartments', 'List imported from Google Sheets: Apartment viewings (archived)',
      phone(step1(APT, 'all', kind='apt', close_href=S09)))
F.add('S39-empty-scope', 'Empty scope: Maybe has no items (Frontend hiring, Q4)',
      phone(step1(HIRE, 'maybe', close_href=S09, empty_note='No items in Maybe. Choose another group to export.')))
F.add('S39-offline', 'Offline: files and text work, Google Sheets needs a connection',
      phone(step1(DESK, 'all', offline=True, safety_line=False, banner=offline_banner("You're offline. Decisions are saved on this phone. Google Sheets needs a connection."))))
F.add('S39-large-text', 'Large text (200%): chips and rows grow and wrap, the screen scrolls',
      phone(step1(DESK, 'all', large=True)))

# ---------------------------------------------------------------- 2 files
F.section('File export (CSV and Excel)',
          'Tap CSV or Excel: the file is written on the phone (Exporting…), then a sheet offers Share or Save to device. The system share sheet and save dialog are native (out of scope). Excel works the same with .xlsx.')
bg_acc = static(step1(DESK, 'accept'))
exporting_sheet = f'''{scrim()}
  <div class="absolute inset-x-0 bottom-0 z-20 rounded-t-sheet bg-popover px-gutter pb-8 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="s39fx">
    <div class="flex justify-center py-1.5"><span class="h-1 w-8 rounded-full bg-muted-foreground/40"></span></div>
    <div class="flex items-center gap-4 pt-4" role="status">{icon("loader-circle", "size-6 shrink-0 animate-spin text-primary")}<div><h2 id="s39fx" class="text-title-3">Exporting…</h2><p class="text-body-sm text-muted-foreground">8 items to desk-setup-accepted.csv</p></div></div>
  </div>'''
F.add('S39-file-exporting', 'CSV: exporting (shown only after 300 ms)', phone(bg_acc + exporting_sheet))

ready_inner = f'''<div class="mt-2">{file_card("desk-setup-accepted.csv", "8 items, 1 KB")}</div>
    <p class="mt-3 text-body-sm text-muted-foreground">Columns: Name, Price, Rating, Reviews, Store, Category, Link, Decision and Notes.</p>'''
ready_actions = P('Share file', '#S39-success-file', 'share-file', 'share-2') + O('Save to device', '#S39-success-file', 'save-file', 'download', ).replace('w-full', 'w-full mt-2')
F.add('S39-file-ready', 'CSV: file ready, share or save', phone(bg_acc + bsheet('s39fr', 'Your file is ready', ready_inner, ready_actions)))
F.add('S39-success-file', 'CSV: exported (back from the share sheet)',
      phone(step1(DESK, 'accept', safety_line=False, overlay=snackbar('Exported 8 items to desk-setup-accepted.csv', ic='circle-check', bottom='bottom-4'))))
F.add('S39-error-file', 'CSV: file could not be written (storage full)',
      phone(bg_acc + bsheet('s39fe', "Couldn't export", f'''<div class="mt-1 flex gap-3" role="alert">{icon("circle-alert", "size-5 mt-0.5 shrink-0 text-destructive")}<p class="text-body text-muted-foreground">This phone is out of storage. Free up some space and try again.</p></div>''',
                            P('Try again', '#S39-file-exporting', 'retry'))))

# ---------------------------------------------------------------- 3 text
F.section('Text summary',
          'A readable summary to paste into a message: counts, then the accepted and Maybe items. Rejected items are counted but not listed, so a shared summary never lists who or what was turned down.')
lines_acc = ''.join(f'<li>- {n} ({p})</li>' for n, p in ACCEPTED_DESK)
lines_may = ''.join(f'<li>- {n} ({p})</li>' for n, p in MAYBE_DESK)
summary_text = f'''<div class="rounded-group bg-card p-4 text-body" aria-label="Summary text">
      <p class="font-semibold">Desk setup</p>
      <p>20 items after 2 rounds: 11 rejected, 1 maybe, 8 accepted.</p>
      <p class="mt-4 font-semibold">Accepted (8)</p>
      <ul>{lines_acc}</ul>
      <p class="mt-4 font-semibold">Maybe (1)</p>
      <ul>{lines_may}</ul>
    </div>'''


def text_screen(overlay='', ios=False):
    if ios:
        bar = ios_bar(f'<a href="#S39-ios" class="inline-flex h-12 items-center gap-0.5 pr-2 text-body text-primary" aria-label="Back to Export">{icon("chevron-left", "size-6")}Back</a>', 'Text summary', '', 'Desk setup')
    else:
        bar = step_bar('Text summary', 'Desk setup', '#S39-default')
    return f'''{bar}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pt-2">
    <h2 class="px-1 pb-2 text-label text-muted-foreground">Preview</h2>
    {summary_text}
    {footer("Lists accepted and Maybe items. Rejected items are counted, not listed.")}
  </div>
  {bottom(P("Share summary", None, "share-summary", "share-2"), O("Copy text", "#S39-text-copied", "copy-text", "copy"))}
  {overlay}'''


F.add('S39-text-summary', 'Text summary preview', phone(text_screen()))
F.add('S39-text-copied', 'Text copied', phone(text_screen(snackbar('Summary copied', ic='copy', bottom='bottom-36'))))

# ---------------------------------------------------------------- 4 google new spreadsheet
F.section('Google Sheets: new spreadsheet (Flows 2 and 3)',
          'Flow 2 is Deniz exporting Desk setup; Flow 3 is Mert exporting Wedding guests with his own Google account. Neither list came from Google Sheets, so the only destination is a new spreadsheet. Two short steps: where to write (name, columns, account), then an explicit confirmation. Google Sheets uses one narrow permission (drive.file, D-17): SwipeSort can open only files it creates or the person chose. Deniz allowed it when she imported Flat hunt 2026, so her export asks nothing more; Mert signed in with Google but never connected Google Sheets, so Google asks him once, after he confirms.')
dest = f'''{step_bar('Export to Google Sheets', 'Desk setup', '#S39-default')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-2">
    <h2 class="px-1 pb-2 text-label text-muted-foreground">New spreadsheet</h2>
    <div><label class="text-label" for="s39-name">Name</label><input id="s39-name" class="mt-1.5 h-12 w-full rounded-control border border-input bg-card px-3.5 text-body" value="Desk setup decisions"></div>
    {footer("Desk setup wasn't imported from Google Sheets, so SwipeSort creates a new spreadsheet.")}
    <h2 class="px-1 pb-2 pt-6 text-label text-muted-foreground">Google account</h2>
    {account_row()}
    <h2 class="px-1 pb-2 pt-6 text-label text-muted-foreground">Columns</h2>
    {col_chips(DESK["fields"], ["Decision", "Notes"], "20 rows, one per item. Decision says Accepted, Rejected or Maybe.")}
  </div>
  {bottom(P("Continue", "#S39-google-confirm", "continue"))}'''
F.add('S39-google-destination', 'Google Sheets: where to write (new spreadsheet)', phone(dest))

perm_new = info_alert('Google asks for permission next', 'Allow SwipeSort to create this spreadsheet. It can open only files it creates or you choose, not your other files.', 'shield-check')


def confirm_screen(title, lead, facts, alert, primary, back_href, sub='Desk setup', extra=''):
    return f'''{step_bar('Export to Google Sheets', sub, back_href, 'Back to destination')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-2">
    <h2 class="text-title-2">{title}</h2>
    <p class="mt-2 text-body text-muted-foreground">{lead}</p>
    <div class="mt-5">{fact_rows(facts)}</div>
    {f'<div class="mt-4">{alert}</div>' if alert else ''}
    {extra}
  </div>
  {bottom(primary, G("Back", back_href, "back"))}'''


conf = confirm_screen('Export 20 items to a new spreadsheet?', 'Nothing is written until you confirm.',
                      [('file-plus-2', 'Creates', f'Desk setup decisions, in the Google Drive of {ACCOUNT}'),
                       ('columns-3', 'Writes', '20 rows with your 7 fields, plus Decision and Notes'),
                       ('shield-check', "Doesn't change", 'Desk setup in SwipeSort, or any of your other spreadsheets')],
                      None, P('Export to Google Sheets', '#S39-success-google', 'confirm-write'), '#S39-google-destination')
F.add('S39-google-confirm', 'Google Sheets: explicit confirmation before writing', phone(conf))

exp_g = f'''{step_bar('Export to Google Sheets', 'Desk setup', None, close=True)}
  {state("loader-circle", "Exporting…", "Writing 20 rows to Desk setup decisions. This takes a few seconds.", "primary", spin=True, role="status")}'''
F.add('S39-google-exporting', 'Google Sheets: exporting', phone(exp_g))

succ = f'''<header class="flex h-app-bar shrink-0 items-center px-1">{icon_btn("x", "Close export", S28, "close")}</header>
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center px-gutter pb-10 text-center">
    <span class="flex size-14 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon("circle-check", "size-7")}</span>
    <h1 class="mt-5 text-title-1" role="status">Exported to Google Sheets</h1>
    <p class="mt-2 max-w-xs text-body text-muted-foreground">Desk setup decisions now has 20 rows with Decision and Notes columns.</p>
    <div class="mt-6 w-full text-left">{file_card("Desk setup decisions", ACCOUNT, "sheet")}</div>
  </div>
  {bottom(P("Open in Google Sheets", None, "open-sheet", "external-link"), G("Done", S28, "done"))}'''
F.add('S39-success-google', 'Google Sheets: exported', phone(succ))

WED_COLS = WED["fields"]
shared_dest = f'''{step_bar('Export to Google Sheets', 'Wedding guests', '#S39-shared')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-2">
    <h2 class="px-1 pb-2 text-label text-muted-foreground">New spreadsheet</h2>
    <div><label class="text-label" for="s39-name-shared">Name</label><input id="s39-name-shared" class="mt-1.5 h-12 w-full rounded-control border border-input bg-card px-3.5 text-body" value="Wedding guests decisions"></div>
    {footer("Wedding guests wasn't imported from Google Sheets, so SwipeSort creates a new spreadsheet.")}
    <h2 class="px-1 pb-2 pt-6 text-label text-muted-foreground">Google account</h2>
    {account_row(MERT, 'people/u-mert.svg')}
    <h2 class="px-1 pb-2 pt-6 text-label text-muted-foreground">Columns</h2>
    {col_chips(WED_COLS, ["Final decision", "Decision (Deniz Yılmaz)", "Decision (Mert Aydın)", "Decision (Selin Yılmaz)", "Notes"], "100 rows, one per item. Final decision says Accepted, Rejected, Maybe, Conflict or Pending.")}
  </div>
  {bottom(P("Continue", "#S39-shared-google-confirm", "continue"))}'''
F.add('S39-shared-google-destination', 'Shared list: where to write (Mert, new spreadsheet only)', phone(shared_dest))

shared_conf = confirm_screen('Export 100 items to a new spreadsheet?', 'Nothing is written until you confirm.',
                             [('file-plus-2', 'Creates', f'Wedding guests decisions, in the Google Drive of {MERT}'),
                              ('columns-3', 'Writes', "100 rows: your 6 fields, Final decision, a column per member and shared notes. Private notes aren't exported."),
                              ('users', 'Who sees it', 'Only people you share it with in Google Drive'),
                              ('shield-check', "Doesn't change", 'Wedding guests in SwipeSort')],
                             perm_new, P('Export to Google Sheets', '#S39-success-shared', 'confirm-write'), '#S39-shared-google-destination', 'Wedding guests')
F.add('S39-shared-google-confirm', 'Shared list: confirmation with member columns', phone(shared_conf))

S09S = 'S09-list-overview.html#S09-shared'
succ_shared = f'''<header class="flex h-app-bar shrink-0 items-center px-1">{icon_btn("x", "Close export", S09S, "close")}</header>
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center px-gutter pb-10 text-center">
    <span class="flex size-14 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon("circle-check", "size-7")}</span>
    <h1 class="mt-5 text-title-1" role="status">Exported to Google Sheets</h1>
    <p class="mt-2 max-w-xs text-body text-muted-foreground">Wedding guests decisions now has 100 rows with the final decision, each member's decision and notes.</p>
    <div class="mt-6 w-full text-left">{file_card("Wedding guests decisions", MERT, "sheet")}</div>
  </div>
  {bottom(P("Open in Google Sheets", None, "open-sheet", "external-link"), G("Done", S09S, "done"))}'''
F.add('S39-success-shared', 'Shared list: exported to Google Sheets (Flow 3 end)', phone(succ_shared))

# ---------------------------------------------------------------- 5 google original sheet
F.section('Google Sheets: the original sheet',
          'Lists imported from Google Sheets (Apartment viewings, from Flat hunt 2026) can also write to the original: a new tab (default, nothing existing moves) or new columns next to the rows. Existing cells are never overwritten. No new Google permission: the sheet was chosen in Google\'s file picker at import (D-17). When SwipeSort can\'t open it with this Google account (imported with another account, access removed), the destination asks to choose it again in the picker.')


def radio_opt(title, desc, on, nested=''):
    return f'''<div><button type="button" role="radio" aria-checked="{"true" if on else "false"}" class="flex min-h-16 w-full items-center gap-4 px-4 py-3 text-left" data-action="destination">{radio_dot(on)}<span class="min-w-0 flex-1"><span class="block text-body">{title}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span></button>{nested}</div>'''


def apt_dest(sel='tab', repick=False):
    tab_field = f'''<div class="px-4 pb-4 pl-14"><label class="text-label" for="s39-tab">Tab name</label><input id="s39-tab" class="mt-1.5 h-12 w-full rounded-control border border-input bg-card px-3.5 text-body" value="Decisions"></div>''' if sel == 'tab' else ''
    opts = [radio_opt('New tab in Flat hunt 2026', "All 8 items on their own tab. Your tabs don't change.", sel == 'tab', tab_field),
            radio_opt('New columns in Flat hunt 2026', 'Decision and Notes next to your rows in Kadıköy and Beşiktaş', sel == 'cols'),
            radio_opt('New spreadsheet', 'A separate copy in your Google Drive', sel == 'new')]
    nxt = '#S39-apartments-confirm-tab' if sel == 'tab' else '#S39-apartments-confirm-columns'
    # A-158: SwipeSort can't open the original with this Google account (drive.file grant missing): re-pick it
    top = (f'<div class="pb-5">{info_alert("Choose Flat hunt 2026 again", "SwipeSort can open only the files you choose in Google\'s file picker, and it can\'t open this one with this Google account yet. Choose it once more to write to it. A new spreadsheet works without it.", "file-search")}</div>'
           if repick else '')
    primary = P("Choose Flat hunt 2026", nxt, "repick-sheet") if repick else P("Continue", nxt, "continue")
    return f'''{step_bar('Export to Google Sheets', 'Apartment viewings', '#S39-apartments')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-2">
    {top}<h2 class="px-1 pb-2 text-label text-muted-foreground">Write to</h2>
    <div class="divide-y overflow-hidden rounded-group bg-card" role="radiogroup" aria-label="Write to">{"".join(opts)}</div>
    <h2 class="px-1 pb-2 pt-6 text-label text-muted-foreground">Google account</h2>
    {account_row()}
    <h2 class="px-1 pb-2 pt-6 text-label text-muted-foreground">Columns</h2>
    {col_chips(APT["fields"], ["Decision", "Notes"], "8 rows, one per item. The Tab column says which tab each item came from.")}
  </div>
  {bottom(primary)}'''


F.add('S39-apartments-destination', 'Original sheet: where to write (new tab selected)', phone(apt_dest('tab')))
F.add('S39-apartments-repick', 'Original sheet can\'t be opened with this Google account: choose it again in Google\'s picker', phone(apt_dest('tab', repick=True)))
F.add('S39-apartments-confirm-tab', 'Original sheet: confirm a new tab',
      phone(confirm_screen('Add a tab to Flat hunt 2026?', 'Nothing is written until you confirm.',
                           [('file-plus-2', 'Adds', 'A tab named Decisions with 8 rows: Tab, Address, Rent, Rooms, Size, Viewing, Link, Decision and Notes'),
                            ('shield-check', "Doesn't change", 'The tabs Kadıköy, Beşiktaş, Archive 2025 and Notes')],
                           None, P('Export to Flat hunt 2026', '#S39-success-tab', 'confirm-write'), '#S39-apartments-destination', 'Apartment viewings')))
succ_tab = f'''<header class="flex h-app-bar shrink-0 items-center px-1">{icon_btn("x", "Close export", S09, "close")}</header>
  <div class="flex min-h-0 flex-1 flex-col items-center justify-center px-gutter pb-10 text-center">
    <span class="flex size-14 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon("circle-check", "size-7")}</span>
    <h1 class="mt-5 text-title-1" role="status">Exported to Google Sheets</h1>
    <p class="mt-2 max-w-xs text-body text-muted-foreground">Flat hunt 2026 has a new tab, Decisions, with 8 rows. Your other tabs didn't change.</p>
    <div class="mt-6 w-full text-left">{file_card("Flat hunt 2026", "Tab Decisions", "sheet")}</div>
  </div>
  {bottom(P("Open in Google Sheets", None, "open-sheet", "external-link"), G("Done", S09, "done"))}'''
F.add('S39-success-tab', 'Original sheet: exported to a new tab', phone(succ_tab))
F.add('S39-apartments-confirm-columns', 'Original sheet: confirm new columns',
      phone(confirm_screen('Add 2 columns to Flat hunt 2026?', 'Nothing is written until you confirm. Existing cells are never overwritten.',
                           [('columns-3', 'Kadıköy', 'Decision in column G and Notes in column H, rows 1 to 5'),
                            ('columns-3', 'Beşiktaş', 'Decision in column G and Notes in column H, rows 1 to 5'),
                            ('shield-check', "Doesn't change", 'Columns A to F, the tabs Archive 2025 and Notes, and formatting'),
                            ('scan-search', 'Checked first', 'Each row still has the same address as when you imported it')],
                           None, P('Export to Flat hunt 2026', '#S39-error-partial', 'confirm-write'), '#S39-apartments-destination', 'Apartment viewings')))

# ---------------------------------------------------------------- 6 failures
F.section('Failures (EXP-09)',
          'Every failure says what happened and how to fix it, and keeps a way out: export a file instead. Error haptic on Android and iOS. Nothing is half-written silently: partial writes say exactly which tab changed.')
another = G('Export a file instead', '#S39-default', 'export-file')
pts = [('file-plus-2', 'Creates new spreadsheets', 'SwipeSort can open only files it creates or you choose. Your other files stay private.'),
       ('user-round', "Doesn't sign you in", "Connecting Google Sheets doesn't sign you in to SwipeSort or change your account."),
       ('unplug', 'Disconnect any time', 'In Settings, under Connected accounts.')]
pts_html = ''.join(f'<li class="flex gap-4"><span class="mt-0.5 shrink-0 text-muted-foreground">{icon(i, "size-6")}</span><div class="min-w-0"><p class="text-label-lg">{a}</p><p class="mt-0.5 text-body-sm text-muted-foreground">{b}</p></div></li>' for i, a, b in pts)
notconn = f'''{step_bar('Export to Google Sheets', 'Desk setup', '#S39-default')}
  <div class="flex min-h-0 flex-1 flex-col overflow-hidden px-gutter pt-3">
    <span class="flex size-14 shrink-0 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon("sheet", "size-7")}</span>
    <h2 class="mt-5 text-title-2">Connect Google Sheets</h2>
    <p class="mt-2 max-w-prose text-body-lg text-muted-foreground">Choose the Google account where SwipeSort creates the spreadsheet.</p>
    <ul class="mt-7 space-y-5">{pts_html}</ul>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">
    <p class="mb-3 text-body-sm text-muted-foreground">Next, Google asks you to choose an account and allow access.</p>
    {P("Connect Google account", "#S39-google-destination", "connect")}<div class="mt-1">{another}</div>
  </div>'''
F.add('S39-google-not-connected', 'Google Sheets not connected yet', phone(notconn))

F.add('S39-error-permission', 'Google permission not given',
      phone(f'''{step_bar('Export to Google Sheets', 'Desk setup', '#S39-google-confirm', 'Back to confirmation')}
  {state("shield-x", "SwipeSort can't write to Google Sheets", "Google didn't give SwipeSort permission to create the spreadsheet. Try again and choose Allow, or export a file instead.", "error", role="alert")}
  {bottom(P("Try again", "#S39-google-confirm", "retry"), another)}'''))

F.add('S39-error-network', 'Google Sheets didn\'t respond',
      phone(f'''{step_bar('Export to Google Sheets', 'Desk setup', '#S39-google-confirm', 'Back to confirmation')}
  {state("cloud-off", "Couldn't export to Google Sheets", "Google Sheets didn't respond. Check your connection and try again. Nothing was written.", "error", role="alert")}
  {bottom(P("Try again", "#S39-google-exporting", "retry"), another)}'''))

F.add('S39-error-sheet-missing', 'Original sheet deleted, moved or no longer shared',
      phone(f'''{step_bar('Export to Google Sheets', 'Apartment viewings', '#S39-apartments-destination', 'Back to destination')}
  {state("file-x-2", "Flat hunt 2026 can't be found", "It was deleted, or you no longer have access. Export to a new spreadsheet instead, or ask its owner to share it again.", "error", role="alert")}
  {bottom(P("Export to a new spreadsheet", "#S39-apartments-destination", "new-spreadsheet"), another)}'''))

F.add('S39-error-sheet-changed', 'Original rows changed since import: columns can\'t be matched',
      phone(f'''{step_bar('Export to Google Sheets', 'Apartment viewings', '#S39-apartments-destination', 'Back to destination')}
  {state("file-search", "Rows in Kadıköy have changed", "Rows were added, moved or deleted since you imported them, so SwipeSort can't match items to rows. Add a new tab instead. Nothing in Flat hunt 2026 was changed.", "error", role="alert")}
  {bottom(P("Add a new tab instead", "#S39-apartments-confirm-tab", "new-tab"), G("Back", "#S39-apartments-destination", "back"))}'''))

tabs_status = f'''<ul class="divide-y overflow-hidden rounded-group bg-card text-left">
      <li class="flex min-h-16 items-center gap-4 px-4 py-3">{icon("circle-check", "size-5 shrink-0 text-primary")}<div class="min-w-0 flex-1"><p class="text-body">Kadıköy</p><p class="text-body-sm text-muted-foreground">Decision and Notes added to 4 rows</p></div></li>
      <li class="flex min-h-16 items-center gap-4 px-4 py-3">{icon("circle-alert", "size-5 shrink-0 text-destructive")}<div class="min-w-0 flex-1"><p class="text-body">Beşiktaş</p><p class="text-body-sm text-muted-foreground">Protected tab. Nothing was added.</p></div></li>
    </ul>'''
partial = f'''{modal_bar('Export to Google Sheets', 'Apartment viewings', S09, 'Close export')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pt-6">
    <span class="flex size-14 items-center justify-center rounded-full bg-muted text-destructive">{icon("triangle-alert", "size-7")}</span>
    <h2 class="mt-5 text-title-2" role="alert">Exported 4 of 8 items</h2>
    <p class="mt-2 text-body text-muted-foreground">Beşiktaş is protected in Google Sheets. Ask the owner of Flat hunt 2026 to let you edit it, then try again. Kadıköy keeps its new columns.</p>
    <div class="mt-5">{tabs_status}</div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">
    {P("Try Beşiktaş again", "#S39-apartments-confirm-columns", "retry")}
    <div class="mt-2">{O("Open in Google Sheets", None, "open-sheet", "external-link")}</div>
    <div class="mt-1">{G("Done", S09, "done")}</div>
  </div>'''
F.add('S39-error-partial', 'Write partly failed: one tab protected', phone(partial))

# ---------------------------------------------------------------- 7 platforms
F.section('iOS and web',
          'iOS: CSV and Excel go straight to the iOS share sheet, which already has Save to Files. Web: CSV and Excel download in the browser; Google sign-in opens in a popup window.')
F.add('S39-ios', 'iOS: Export as a page sheet', phone(step1(DESK, 'all', ios=True), ios=True))
ios_bg = static(step1(DESK, 'accept', ios=True))
share_ph = f'''{scrim()}
  <div class="absolute inset-x-0 bottom-0 z-20 rounded-t-sheet bg-popover px-5 pb-10 pt-5 shadow-sheet" aria-hidden="true">
    <p class="text-caption text-muted-foreground">System share sheet (iOS, out of scope)</p>
    <div class="mt-3 flex items-center gap-3"><span class="flex size-10 items-center justify-center rounded-sm bg-muted text-muted-foreground">{icon("file-text")}</span><div><p class="text-body">desk-setup-accepted.csv</p><p class="text-caption text-muted-foreground">CSV file, 1 KB</p></div></div>
    <p class="mt-4 text-body-sm text-muted-foreground">AirDrop, Messages, Mail, Save to Files and other apps</p>
  </div>'''
F.add('S39-ios-share', 'iOS: CSV opens the share sheet directly (no file-ready step)', phone(ios_bg + share_ph, ios=True))
F.add('S39-ios-text', 'iOS: text summary', phone(text_screen(ios=True), ios=True))

web_col = step1(DESK, 'accept', web=True, csv_href='#S39-web-desktop')
toast = f'''<div class="absolute bottom-6 right-6 z-30 flex w-80 items-start gap-3 rounded-control bg-foreground px-4 py-3 text-background shadow-overlay" role="status">{icon("circle-check", "size-5 mt-0.5 shrink-0")}<span class="flex-1 text-body-sm">Exported 8 items to <span class="whitespace-nowrap">desk-setup-accepted.csv</span></span></div>'''
F.add('S39-web-desktop', 'Web, desktop: CSV downloaded, toast bottom-right', f'''<div class="desktop">
  <div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">swipesort.app/l/l-desk/export</span></div>
  <div class="desktop-column">
  {web_col}
  </div>
  {toast}
</div>''')

waiting = f'''{step_bar('Export to Google Sheets', 'Desk setup', '#S39-google-confirm', 'Back to confirmation')}
  {state("app-window", "Continue in the Google window", "Confirm your Google account so SwipeSort can create the spreadsheet. The export continues here when you're done.", "primary", role="status")}
  {bottom(O("Open the Google window again", None, "reopen-popup"), G("Cancel", "#S39-google-confirm", "cancel"))}'''
popup = f'''<div class="absolute right-10 top-24 z-20 flex h-96 w-96 flex-col overflow-hidden rounded-control border bg-card shadow-dialog" aria-hidden="true">
    <div class="flex h-9 shrink-0 items-center gap-2 border-b bg-secondary px-3 text-caption text-muted-foreground">{icon("lock", "size-3.5")}accounts.google.com</div>
    <div class="flex-1 space-y-3 p-6"><span class="block h-4 w-24 rounded-full bg-muted"></span><span class="block h-6 w-48 rounded-full bg-muted"></span><span class="block h-12 rounded-control bg-muted"></span><span class="block h-12 rounded-control bg-muted"></span><p class="pt-2 text-caption text-muted-foreground">Google sign-in (Google's UI, out of scope)</p></div>
  </div>'''
F.add('S39-web-google-popup', 'Web, desktop: Google sign-in popup open',
      f'''<div class="desktop">
  <div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">swipesort.app/l/l-desk/export</span></div>
  <div class="desktop-column">
  {waiting}
  </div>
  {popup}
</div>''')

F.write(OUT, 'S39 Export flow', INTRO)
