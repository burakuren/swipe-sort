# Usage: python3 tools/generators/S21-add-items.py
# Generates design/03-screens/S21-add-items.html
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from groupc2_common import *  # noqa

P = Page('S21', 'Add items to an existing list', 'From S09 “Add items”: the same import steps with list context. Columns are matched to the list\'s existing fields, rows are checked against items already in the list (S20-existing), and new items join the current round. Sample: mert-family.csv added to Wedding guests (shared with Mert and Selin). Spec: <a href="S21-add-items.md">S21-add-items.md</a>.')

CLOSE = 'S09-list-overview.html#S09-shared'
LIST = 'Wedding guests'
OFFLINE_TEXT = "You're offline. Items you add are saved on this phone. Google Sheets needs a connection."  # S40 offline banner pattern


def bar(ios=False, back=None):
    return modal_bar('Add items', CLOSE, 'Close adding items', ios=ios, back=back)


SOURCES = [
    ('contact', 'Contacts', 'From this phone', 'S13-contacts-import.html#S13-select-default', 'source-contacts'),
    ('file-spreadsheet', 'CSV or Excel', 'A .csv or .xlsx file', '#S21-file', 'source-csv'),
    ('sheet', 'Google Sheets', 'From Google Drive', 'S15-google-sheets.html#S15-default', 'source-google'),
    ('text', 'Plain text', 'Paste a list or a .txt file', 'S16-plain-text.html#S16-empty', 'source-text'),
    ('square-pen', 'Manual entry', 'Type items one by one', 'S17-manual-entry.html#S17-empty', 'source-manual'),
]
# Photos left with D-32 (A-129). Five tiles: the last one spans both columns, as in S11 (A-150).
# Contacts: Android 16 and lower (reference) go straight to the full list (permission already granted);
# Android 17 and later and iOS open the contact picker intro (D-18).


def tile(ic, name, desc, href, action, wide=False):
    span = 'col-span-2 ' if wide else ''
    return f'<a href="{href}" class="{span}flex min-h-28 flex-col justify-start gap-3 rounded-tile border bg-card p-4" data-action="{action}">{icon(ic, "size-6 text-primary")}<span><span class="block text-label-lg">{name}</span><span class="block text-caption text-muted-foreground">{desc}</span></span></a>'


def tile_off(ic, name, desc, badge_ic, aria, wide=False):
    span = 'col-span-2 ' if wide else ''
    return f'<button class="{span}flex min-h-28 flex-col justify-start gap-3 rounded-tile border border-dashed border-input bg-transparent p-4 text-left" aria-label="{aria}"><span class="flex w-full items-start justify-between">{icon(ic, "size-6 text-muted-foreground")}{icon(badge_ic, "size-4 text-muted-foreground")}</span><span><span class="block text-label-lg text-muted-foreground">{name}</span><span class="block text-caption text-muted-foreground">{desc}</span></span></button>'


def picker(overrides=None, banner='', note_extra=''):
    overrides = overrides or {}
    tiles = ''
    for i, s in enumerate(SOURCES):
        wide = len(SOURCES) % 2 == 1 and i == len(SOURCES) - 1
        tiles += overrides.get(s[1], tile(*s, wide=wide))
    return f'''{banner}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-5 pb-6 pt-1">
    <div class="px-gutter">
      <h2 class="text-title-2">Add items to {LIST}</h2>
      <p class="mt-1 text-body text-muted-foreground">New items join Round 1, so every member sorts them. Decisions already made stay as they are.</p>
    </div>
    <div class="px-gutter">
      <p class="px-1 pb-2 text-label text-muted-foreground">In this list now</p>
      <ul class="overflow-hidden rounded-group bg-card"><li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon("contact", "size-5 text-muted-foreground")}<span class="flex-1 text-body">Contacts</span><span class="text-body tabular-nums text-muted-foreground">88 items</span></li></ul>
    </div>
    <div class="px-gutter">
      <p class="px-1 pb-2 text-label text-muted-foreground">Add from</p>
      <div class="grid grid-cols-2 gap-3">{tiles}</div>
      <p class="mt-3 px-1 text-body-sm text-muted-foreground">A list can combine items from any of these sources.{note_extra}</p>
    </div>
    </div>
  </div>'''


# ------------------------------------------------------------------ flow
P.section('Flow', 'Choose source (with list context) → select the file → match columns to the list\'s fields → duplicates against existing items (S20-existing) → confirm → adding → back to the list with a snackbar.')

P.frame('S21-default', 'Default: choose a source for Wedding guests', phone(f'''{bar()}
  {stepper("Choose source", 1, 5)}
  {picker()}'''))

preview_rows = [
    ('c089', 'Begüm Sağlam', 'begum.saglam@example.com'),
    ('c090', 'Tarık Kalkan', '+90 500 000 52 74'),
    ('c091', 'Canan Eren', '+90 500 000 15 86'),
    ('c092', 'Levent Öğüt', '+90 500 000 54 34'),
]
pr = ''.join(f'<li class="flex min-h-14 items-center gap-3 px-4 py-2">{avatar(name=n, size="size-10")}<div class="min-w-0 flex-1"><p class="truncate text-body">{n}</p><p class="truncate text-body-sm text-muted-foreground">{m}</p></div></li>' for cid, n, m in preview_rows)
file_card = f'''<div class="flex items-center gap-3 rounded-group bg-card px-4 py-3">
      <span class="flex size-10 shrink-0 items-center justify-center rounded-control bg-primary-soft text-primary-soft-foreground">{icon("file-spreadsheet")}</span>
      <div class="min-w-0 flex-1"><p class="truncate text-body font-medium">mert-family.csv</p><p class="text-body-sm text-muted-foreground">15 rows, 7 columns</p></div>
      <button class="inline-flex min-h-touch shrink-0 items-center rounded-control px-3 text-label text-primary">Change</button>
    </div>'''
P.frame('S21-file', 'File chosen: mert-family.csv', phone(f'''{bar()}
  {stepper("Select items", 2, 5)}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-5 pb-6 pt-1">
    <div class="px-gutter">{file_card}</div>
    <div class="px-gutter">
      <p class="px-1 pb-2 text-label text-muted-foreground">First rows</p>
      <ul class="divide-y overflow-hidden rounded-group bg-card">{pr}</ul>
      <p class="mt-2 px-1 text-body-sm text-muted-foreground">Showing 4 of 15 rows. Every row is added; you can review matches in the next steps.</p>
    </div>
    </div>
  </div>
  {bottom("Continue", "#S21-mapping", "continue")}'''))

MAP = [
    ('Name', 'Begüm Sağlam, Tarık Kalkan', 'Name', 'heading', 'Title'),
    ('Phone', '+90 500 000 52 74, +90 500 000 15 86', 'Phone', 'phone', None),
    ('E-mail', 'begum.saglam@example.com', 'Email', 'mail', None),
    ('Side', "Bride's, Groom's", 'Side', 'type', None),
    ('Relationship', 'Friend, Colleague, Family', 'Relationship', 'type', None),
    ('City', 'İstanbul, Ankara, İzmir', 'City', 'type', None),
    ('Address', 'Çankaya, Ankara; Moda, İstanbul', 'New field', 'circle-plus', 'New'),
]


def map_row(col, samples, field, ic, tag, error=False, placeholder=False):
    t = ''
    if tag == 'New':
        t = f'<span class="inline-flex h-6 items-center gap-1 rounded-full bg-primary-soft px-2 text-caption text-primary-soft-foreground">{icon("plus", "size-3.5")}New</span>'
    sel = select_trigger(field, f'{col} goes to: {field}. Change', ic=ic, error=error, placeholder=placeholder)
    extra = '<p class="mt-1.5 text-caption text-muted-foreground">Items already in the list leave it empty.</p>' if tag == 'New' else ''
    return f'''<li class="px-4 py-3">
        <div class="flex items-center gap-3">
          <div class="w-2/5 min-w-0 shrink-0"><p class="flex items-center gap-1.5 truncate text-body font-medium">{col}</p><p class="truncate text-body-sm text-muted-foreground">{samples}</p></div>
          <div class="min-w-0 flex-1">{sel}</div>
        </div>{t and f'<div class="mt-1.5">{t}</div>'}{extra}
      </li>'''


def mapping(rows, top='', overlay='', ios=False):
    rws = ''.join(map_row(*r) for r in rows)
    return f'''{bar(ios=ios, back=('Select items', '#S21-file') if ios else None)}
  {stepper("Map fields", 3, 5)}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-4 pb-6 pt-1">
    <p class="px-gutter text-body text-muted-foreground">Match the 7 columns in mert-family.csv to fields in {LIST}.</p>
    {top}
    <div class="px-gutter">
      <div class="flex items-end justify-between px-1 pb-2"><p class="w-2/5 text-label text-muted-foreground">Column in the file</p><p class="flex-1 pl-3 text-label text-muted-foreground">Field in the list</p></div>
      <ul class="divide-y overflow-hidden rounded-group bg-card">{rws}</ul>
      <p class="mt-2 flex items-start gap-2 px-1 text-body-sm text-muted-foreground">{icon("info", "mt-0.5 size-4 shrink-0")}Photo has no column in this file. New items show initials instead.</p>
    </div>
    </div>
  </div>
  {bottom("Continue", "S20-duplicate-review.html#S20-existing", "continue")}
  {overlay}'''


P.frame('S21-mapping', 'Map columns to the list\'s fields (one new field)', phone(mapping(MAP)))

opts = [
    ('circle-plus', 'New field: Address', 'Added to every item; existing items leave it empty', True),
    ('circle-slash', 'Don\'t import', 'The column is left out', False),
    ('heading', 'Name', 'Title. Already filled by Name', False),
    ('phone', 'Phone', 'Already filled by Phone', False),
    ('mail', 'Email', 'Already filled by E-mail', False),
    ('image', 'Photo', 'No column yet', False),
    ('type', 'City', 'Already filled by City', False),
]
ol = ''.join(f'''<div><button role="radio" aria-checked="{"true" if sel else "false"}" class="flex min-h-14 w-full items-center gap-4 px-1 py-2 text-left">{icon(ic, "size-5 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">{n}</span><span class="block text-body-sm text-muted-foreground">{d}</span></span>{radio_dot(sel)}</button></div>''' for ic, n, d, sel in opts)
fs = sheet('fs1', 'Address goes to', f'<div class="mt-2 divide-y" role="radiogroup" aria-label="Field for the Address column">{ol}</div>', subtitle='Column in mert-family.csv')
P.frame('S21-field-select', 'New column: add as a field or leave out', phone(mapping(MAP, overlay=fs)))

err_rows = [('Ad Soyad', 'Begüm Sağlam, Tarık Kalkan', 'New field', 'circle-plus', 'New')] + MAP[1:6]
err_alert = alert('error', 'Name has no column', 'Every item needs a title. Choose the column that holds the names.', alert_button('Use Ad Soyad for Name'))
P.frame('S21-mapping-error', 'Error: the title field has no column', phone(mapping(err_rows, top=f'<div class="px-gutter">{err_alert}</div>').replace(
    'S20-duplicate-review.html#S20-existing" class', '#S21-mapping-error" class', 1)))

# confirm
summary_items = [
    ('file-spreadsheet', '12 new items', 'From mert-family.csv'),
    ('merge', '3 rows match items already in the list', '2 merged, 1 skipped. Their decisions and notes stay.'),
    ('circle-plus', '1 new field: Address', 'Items already in the list leave it empty.'),
    ('layers', 'New items join Round 1', 'Every member sorts them. Decisions already made don\'t change.'),
    ('layout-template', 'Cards use the Person template', 'Address shows in item details. Add it to cards in Card template.'),
]


def summary_list(large=False):
    t = 'text-title-3 font-normal' if large else 'text-body'
    d = 'text-body-lg' if large else 'text-body-sm'
    return ''.join(f'<li class="flex items-start gap-4 px-4 py-3">{icon(ic, "mt-0.5 size-5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="{t}">{a}</p><p class="{d} text-muted-foreground">{b}</p></div></li>' for ic, a, b in summary_items)


members = f'<span class="flex shrink-0 -space-x-2">{avatar(photo="images/people/u-mert.svg", size="size-8")}<span class="flex size-8 items-center justify-center rounded-full bg-muted text-caption text-muted-foreground ring-2 ring-primary-soft">SY</span></span>'
shared_notice = f'''<div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground" role="note">{members}<div class="min-w-0 flex-1"><p class="text-label">Mert and Selin will see 12 new items to sort</p><p class="mt-0.5 text-body-sm">They get a notification. Their progress counts the new items.</p></div></div>'''
# D-05: adding items to a shared list offline is queued, not blocked (A-159)
shared_notice_offline = f'''<div class="flex gap-3 rounded-control bg-primary-soft p-4 text-primary-soft-foreground" role="note">{members}<div class="min-w-0 flex-1"><p class="text-label">Mert and Selin see the 12 new items when you\'re back online</p><p class="mt-0.5 text-body-sm">Until then they\'re saved on this phone. Members get a notification once the items sync.</p></div></div>'''


def confirm(busy=False, ios=False, offline=False):
    if busy:
        btn_html = bottom('Adding 12 items…', busy=True)
    else:
        btn_html = bottom('Add to list', '#S21-offline-success' if offline else '#S21-success', 'add-to-list')
    banner = f'{offline_banner(OFFLINE_TEXT)}<div class="h-3 shrink-0"></div>' if offline else ''
    prog = ''
    if busy:
        prog = '<div class="px-gutter"><div class="h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="7" aria-valuemin="0" aria-valuemax="12" aria-label="Adding items, 7 of 12"><div class="h-full w-[58%] rounded-full bg-primary"></div></div><p class="mt-2 text-body-sm tabular-nums text-muted-foreground" role="status">7 of 12 added. You can leave; adding continues.</p></div>'
    return f'''{bar(ios=ios, back=('Review duplicates', 'S20-duplicate-review.html#S20-existing') if ios else None)}
  {banner}{stepper("Add to list", 5, 5)}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-4 pb-6 pt-1">
    <h2 class="px-gutter text-title-2">Add 12 items to {LIST}</h2>
    {prog}
    <div class="px-gutter"><ul class="divide-y overflow-hidden rounded-group bg-card">{summary_list()}</ul></div>
    <div class="px-gutter">{shared_notice_offline if offline else shared_notice}</div>
    </div>
  </div>
  {btn_html}'''


P.frame('S21-confirm', 'Confirm: Add 12 items to Wedding guests (shared list)', phone(confirm()))
P.frame('S21-adding', 'Adding progress', phone(confirm(busy=True)))

# success on S09: the real S09-shared screen (Group B) embedded from S09-list-overview.html
import re as _re
_S09 = open(os.path.join(SCREENS, 'S09-list-overview.html'), encoding='utf-8').read()


def s09_screen(frame_id, suffix):
    i = _S09.index(f'data-frame="{frame_id}"')
    i = _S09.index('<div class="screen', i)
    i = _S09.index('>', i) + 1
    j = _S09.index('<div class="sysbar-nav"', i)
    inner = _S09[i:j].rstrip()
    assert inner.endswith('</div>')
    inner = inner[:-len('</div>')]
    for fid in set(_re.findall(r' id="([^"]+)"', inner)):
        inner = inner.replace(f'"{fid}"', f'"{fid}-{suffix}"')
    return f'<!-- Embedded from S09-list-overview.html#{frame_id} (Group B) -->\n' + inner


added_event = f'<li class="flex items-center gap-3 px-4 py-3">{avatar(photo="images/people/u-deniz.svg", size="size-8")}<span class="min-w-0 flex-1"><span class="block text-body">You added 12 items from mert-family.csv</span><span class="block text-body-sm text-muted-foreground">Just now</span></span></li>'
ACT_UL = '<ul class="mt-1 divide-y overflow-hidden rounded-group bg-card dark:border">'
P.frame('S21-success', 'Back on S09: snackbar “Added 12 items” with Undo', phone(s09_screen('S09-shared', 's21a') + snackbar('Added 12 items', 'Undo', bottom='bottom-2')))
P.frame('S21-success-activity', 'S09 scrolled: the addition in Recent activity', phone(s09_screen('S09-shared-scrolled', 's21b').replace(ACT_UL, ACT_UL + added_event, 1)))

# ------------------------------------------------------------------ errors and states
P.section('Errors, offline and platforms', 'Partial add, offline (local sources work; Google Sheets needs a connection; on a shared list the added items are saved on this phone and reach members when the connection is back, D-05), web (contacts need the app) and iOS.')

skipped = [
    ('Row 9', 'Has 9 values but the file has 7 columns.'),
    ('Row 14', 'Has characters that can\'t be read. Save the file as UTF-8.'),
]
sk = ''.join(f'<li class="flex items-start gap-4 px-4 py-3">{icon("file-x", "mt-0.5 size-5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="text-body">{a}</p><p class="text-body-sm text-muted-foreground">{b}</p></div></li>' for a, b in skipped)
partial = f'''{bar()}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-5 px-gutter pb-6 pt-4">
    <div class="flex items-start gap-3">{icon("circle-alert", "mt-1 size-6 shrink-0 text-destructive")}<div><h2 class="text-title-2">Added 10 of 12 items</h2><p class="mt-1 text-body text-muted-foreground">2 rows in mert-family.csv couldn\'t be added. The other 10 are in {LIST} and join Round 1.</p></div></div>
    <div><p class="px-1 pb-2 text-label text-muted-foreground">Not added</p><ul class="divide-y overflow-hidden rounded-group bg-card">{sk}</ul>
    <p class="mt-2 px-1 text-body-sm text-muted-foreground">Fix these rows in the file and add it again. Rows already in the list show up as duplicates, so nothing is added twice.</p></div>
    </div>
  </div>
  {bottom("Done", CLOSE, "done", secondary=ghost_full("Add the file again", "#S21-file"))}'''
P.frame('S21-partial', 'Partial: 10 of 12 added', phone(partial))

off_tile = tile_off('sheet', 'Google Sheets', 'Needs a connection', 'wifi-off', 'Google Sheets, needs a connection')
P.frame('S21-offline', 'Offline: local sources work, Google Sheets doesn\'t', phone(f'''{bar()}
  {offline_banner(OFFLINE_TEXT)}<div class="h-3 shrink-0"></div>
  {stepper("Choose source", 1, 5)}
  {picker({"Google Sheets": off_tile})}'''))

P.frame('S21-offline-confirm', 'Offline, shared list: Add to list still works (queued)', phone(confirm(offline=True)))
# S40 SyncNotice under the S09 header meta: the 12 queued items stay visible after the snackbar (A-159)
SYNC_NOTICE = f'<p class="mt-3 inline-flex items-center gap-1.5 text-body-sm text-muted-foreground" role="status">{icon("cloud-off", "size-4 shrink-0")}Saved on this phone<span class="sr-only">, 12 new items not synced yet</span></p>'


def with_sync_notice(html):
    if 'Saved on this phone' in html:  # S09-offline draws the S40 sync notice itself (group C, QA round)
        return html
    anchor = 'Owner</span></div></div>'
    assert html.count(anchor) >= 1, 'S09-offline header meta changed'
    return html.replace(anchor, 'Owner</span></div>' + SYNC_NOTICE + '</div>', 1)


P.frame('S21-offline-success', 'Offline, shared list: added and saved on this phone (sync notice stays after the snackbar)', phone(with_sync_notice(s09_screen('S09-offline', 's21o')) + snackbar("Added 12 items. Members see them when you're back online.", 'Undo', bottom='bottom-2')))

web_contacts = tile_off('contact', 'Contacts', 'Needs the Android or iOS app', 'monitor-smartphone', 'Contacts, needs the Android or iOS app')
web_note = ' Contacts import needs the Android or iOS app. <a href="https://swipesort.app/get" class="text-primary underline underline-offset-4">Get the app</a>'
P.frame('S21-web', 'Web: contacts unavailable', web_phone(f'''{bar()}
  {stepper("Choose source", 1, 5)}
  {picker({"Contacts": web_contacts}, note_extra=web_note)}'''))

P.frame('S21-ios', 'iOS: choose a source', phone(f'''{bar(ios=True)}
  {stepper("Choose source", 1, 5)}
  {picker({"Contacts": tile('contact', 'Contacts', 'From this iPhone', 'S13-contacts-import.html#S13-picker-intro-ios', 'source-contacts')})}''', ios=True))
P.frame('S21-ios-confirm', 'iOS: confirm', phone(confirm(ios=True), ios=True))

big = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="{CLOSE}" class="flex size-12 items-center justify-center rounded-full" aria-label="Close adding items">{icon("x", "size-7")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">Add items</h1>
  </header>
  <div class="shrink-0 px-gutter pb-3"><p class="text-title-3">Add to list</p><p class="text-body-lg text-muted-foreground">Step 5 of 5</p></div>
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-4 pb-6 pt-1">
    <h2 class="px-gutter text-title-1">Add 12 items to {LIST}</h2>
    <div class="px-gutter"><ul class="divide-y overflow-hidden rounded-group bg-card">{summary_list(large=True)}</ul></div>
    </div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3"><a href="#S21-success" class="flex min-h-16 w-full items-center justify-center rounded-control bg-primary px-6 text-title-3 text-primary-foreground" data-action="add-to-list">Add to list</a></div>'''
P.frame('S21-large-text', 'Large text (200%): confirm', phone(big))

P.write('S21-add-items.html')
