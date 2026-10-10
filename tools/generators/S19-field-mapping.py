# Usage: python3 tools/generators/S19-field-mapping.py
# Generates design/03-screens/S19-field-mapping.html
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from groupc2_common import *  # noqa

P = Page('S19', 'Field mapping', 'Step 3 of the import: detected fields with sample values from the real records; rename, set the type, hide, choose the title field, handle several values. Spec: <a href="S19-field-mapping.md">S19-field-mapping.md</a>. Shared stepper and app bar: <a href="../01-foundations/components.html#C-navigation">components › Navigation</a>.')

# ------------------------------------------------------------------ field data (real records)
CONTACT_FIELDS = [
    dict(key='name', label='Name', type='text', title=True, samples='Ayşe Demir, Mehmet Yılmaz, Zeynep Kaya, Emre Çelik'),
    dict(key='phone', label='Phone', type='phone', samples='+90 500 000 97 62, +90 500 000 96 91, +90 500 000 97 10', multi='All numbers', note='8 items have 2 or more numbers. Empty in 5 items.'),
    dict(key='email', label='Email', type='email', samples='ayse.demir@example.com, mehmet.yilmaz@example.com', note='Empty in 5 items'),
    dict(key='photo', label='Photo', type='image', imgs=['c001', 'c002', 'c003', 'c004'], samples='35 of 88 items have a photo'),
    dict(key='side', label='Side', type='text', samples="Bride's, Groom's"),
    dict(key='rel', label='Relationship', type='text', samples='Family, Friend, Colleague'),
    dict(key='city', label='City', type='text', samples='İstanbul, Ankara, İzmir, Berlin, Lisbon'),
]
CSV_FIELDS = [
    dict(key='name', label='Name', type='text', title=True, samples='Lena Hoffmann, Kaan Yurt, Aisha Bello, Marco Bianchi'),
    dict(key='years', label='Years of experience', type='number', samples='6, 4, 8, 3, 5, 10'),
    dict(key='loc', label='Location', type='text', samples='Berlin, İstanbul, London, Milan'),
    dict(key='salary', label='Expected salary', type='number', samples='78,000, 62,000, 92,000', note='Empty in 1 item'),
    dict(key='portfolio', label='Portfolio', type='link', samples='lenahoffmann.example, kaanyurt.example, aisha.example', note='Empty in 2 items'),
    dict(key='email', label='Email', type='email', samples='lena.hoffmann@example.com, kaan.yurt@example.com'),
    dict(key='source', label='Source', type='text', samples='Referral, LinkedIn, Careers page, Agency'),
]
CSV_AUTO_HIDDEN = [dict(key='role', label='Role', type='text', samples='Frontend engineer', shown=False, note='Same value in all 12 items')]
APT_FIELDS = [
    dict(key='address', label='Address', type='text', title=True, samples='Moda Cd. 112, Kadıköy; Bahariye Cd. 48, Kadıköy'),
    dict(key='rent', label='Rent (TRY)', type='number', samples='42,000, 38,500, 31,000, 48,000'),
    dict(key='rooms', label='Rooms', type='text', samples='2+1, 1+1, 3+1'),
    dict(key='size', label='Size (m²)', type='number', samples='95, 88, 62, 120'),
    dict(key='viewing', label='Viewing', type='date', samples='Oct 12, 11:00; Oct 12, 13:30; Oct 13, 10:00', note='Empty in 1 item'),
    dict(key='link', label='Link', type='link', samples='listings.example/ist/48210, listings.example/ist/48223'),
    dict(key='tab', label='Tab', type='text', samples='Kadıköy, Beşiktaş', note='Added from the tab names, so you can tell the tabs apart'),
]


def type_chip(t, label, large=False):
    ic, name = TYPES[t]
    txt = 'text-title-3' if large else 'text-label'
    h = 'h-12' if large else 'h-9'
    return f'<button class="inline-flex min-h-touch items-center" aria-haspopup="dialog" aria-label="Type: {name}. Change the type of {label}"><span class="inline-flex {h} items-center gap-1.5 rounded-full border border-input bg-card px-3 {txt}">{icon(ic, "size-4 text-muted-foreground")}{name}{icon("chevron-down", "size-4 text-muted-foreground")}</span></button>'


def multi_chip(value, label, large=False):
    txt = 'text-title-3' if large else 'text-label'
    h = 'h-12' if large else 'h-9'
    return f'<button class="inline-flex min-h-touch items-center" aria-haspopup="dialog" aria-label="Several values: {value}. Change how {label} handles several values"><span class="inline-flex {h} items-center gap-1.5 rounded-full border border-input bg-card px-3 {txt}">{icon("list", "size-4 text-muted-foreground")}{value}{icon("chevron-down", "size-4 text-muted-foreground")}</span></button>'


TITLE_BADGE = f'<span class="inline-flex h-6 shrink-0 items-center gap-1 rounded-full bg-primary-soft px-2 text-caption text-primary-soft-foreground">{icon("heading", "size-3.5")}Title</span>'


TITLE_BADGE_LG = f'<span class="inline-flex h-9 shrink-0 items-center gap-1.5 rounded-full bg-primary-soft px-3 text-body-lg text-primary-soft-foreground">{icon("heading", "size-5")}Title</span>'


def field_row(f, large=False, renaming=None, error=None, hide_switch=False):
    ic, tname = TYPES[f['type']]
    label = f['label']
    shown = f.get('shown', True)
    lab_cls = 'text-title-2' if large else 'text-body font-medium'
    smp_cls = 'text-title-3 font-normal' if large else 'text-body-sm'
    title = (TITLE_BADGE_LG if large else TITLE_BADGE) if f.get('title') else ''
    if renaming is not None:
        head = f'''<div class="flex items-center gap-2">
          <label for="ren-{f['key']}" class="sr-only">Field name</label>
          <input id="ren-{f['key']}" class="h-12 min-w-0 flex-1 rounded-control border border-primary bg-card px-3.5 text-body ring-2 ring-ring/30" value="{renaming}">
          <button class="flex size-12 shrink-0 items-center justify-center rounded-full bg-secondary text-secondary-foreground" aria-label="Save name">{icon("check")}</button>
        </div>
        <p class="mt-1 text-caption text-muted-foreground">Original name in the source: {label}</p>'''
    else:
        ren = f'<button class="-my-3 flex size-12 shrink-0 items-center justify-center rounded-full text-muted-foreground" aria-label="Rename {label}">{icon("pencil", "size-4")}</button>'
        frm = f'<p class="text-caption text-muted-foreground">From: {f["from"]}</p>' if f.get('from') else ''
        head = f'<div class="flex min-h-6 flex-wrap items-center gap-x-2"><p class="{lab_cls}">{label}</p>{title}{ren}</div>{frm}'
    if f.get('imgs'):
        thumbs = ''.join(avatar(c, size='size-7') for c in f['imgs'])
        samples = f'<div class="mt-1 flex items-center gap-2"><span class="flex -space-x-1.5">{thumbs}</span><span class="{smp_cls} text-muted-foreground">{f["samples"]}</span></div>'
    else:
        trunc = '' if large else 'truncate'
        samples = f'<p class="mt-0.5 {trunc} {smp_cls} text-muted-foreground"><span class="sr-only">Sample values: </span>{f["samples"]}</p>'
    chips = type_chip(f['type'], label, large)
    if f.get('multi'):
        chips += multi_chip(f['multi'], label, large)
    note = ''
    if f.get('note'):
        ncls = 'text-body-lg' if large else 'text-caption'
        note = f'<p class="{ncls} text-muted-foreground">{f["note"]}</p>'
    if not shown:
        note += f'<p class="flex items-center gap-1.5 text-caption text-muted-foreground">{icon("eye-off", "size-3.5")}Hidden on cards. Kept for details and export.</p>'
    err = ''
    if error:
        err = f'<p class="mt-1 flex items-start gap-1.5 text-caption text-destructive">{icon("circle-alert", "size-4 shrink-0")}<span>{error}</span></p>'
    sw = '' if hide_switch else switch(shown, f'Show {label} on cards', extra='-mr-1')
    icon_box = ''
    if large:
        return f'''<li class="px-4 py-4">
        {head}
        {samples}
        <div class="mt-1 flex flex-wrap items-center gap-x-2">{chips}</div>
        {note}{err}
        <div class="mt-2 flex items-center justify-between gap-3"><span class="text-title-3 font-normal">Show on cards</span>{sw}</div>
      </li>'''
    return f'''<li class="flex gap-3 px-4 py-3">
        {icon_box}
        <div class="min-w-0 flex-1">
          {head}
          {samples}
          <div class="-mb-1 flex flex-wrap items-center gap-x-2">{chips}</div>
          {note}{err}
        </div>
        {sw}
      </li>'''


def fields_group(fields, count_label, renaming=None, error_key=None, error=None, extra_rows='', large=False):
    rows = ''.join(field_row(f, large=large, renaming=renaming.get(f['key']) if renaming else None,
                             error=error if f['key'] == error_key else None) for f in fields)
    right = '' if large else '<p class="text-label text-muted-foreground">On cards</p>'
    return f'''<div class="px-gutter">
      <div class="flex items-end justify-between px-1 pb-2"><p class="text-label text-muted-foreground">{count_label}</p>{right}</div>
      <ul class="divide-y overflow-hidden rounded-group bg-card">{rows}{extra_rows}</ul>
    </div>'''


def title_select(value, error=None, placeholder=False, large=False):
    if error:
        helper = f'<p id="ts-e" class="mt-1.5 flex items-start gap-1.5 text-caption text-destructive">{icon("circle-alert", "size-4 shrink-0")}<span>{error}</span></p>'
    else:
        helper = '<p class="mt-1.5 text-caption text-muted-foreground">The largest text on each card. Every item needs a value here.</p>'
    lab = 'text-title-3' if large else 'text-label'
    return f'''<div class="px-gutter">
      <p class="{lab}">Card title</p>
      <div class="mt-1.5">{select_trigger(value, "Card title: " + value + ". Choose the title field", ic="heading", error=bool(error), placeholder=placeholder)}</div>
      {helper}
    </div>'''


def intro(text, large=False):
    cls = 'text-body-lg' if large else 'text-body'
    return f'<p class="px-gutter {cls} text-muted-foreground">{text}</p>'


def hidden_group(n, names, expanded=False, rows=''):
    chevron = 'chevron-up' if expanded else 'chevron-down'
    head = f'''<li><button class="flex min-h-14 w-full items-center gap-3 px-4 py-3 text-left" aria-expanded="{"true" if expanded else "false"}">
        {icon("eye-off", "size-5 shrink-0 text-muted-foreground")}
        <span class="min-w-0 flex-1"><span class="block text-body font-medium">Hidden by SwipeSort ({n})</span><span class="block truncate text-body-sm text-muted-foreground">{names}</span></span>
        {icon(chevron, "size-5 text-muted-foreground")}</button></li>'''
    return head + (rows if expanded else '')


def mapping_screen(fields, intro_text, step=(3, 5), title_value='Name', continue_href=None, action='continue', overlay='', bar=None,
                   top_extra='', renaming=None, error_key=None, error=None, title_error=None, title_placeholder=False, extra_rows='',
                   count_label=None, scrolled=False, bottom_html=None, continue_label='Continue'):
    n, total = step
    count_label = count_label or f'{len(fields)} fields'
    parts = []
    if not scrolled:
        parts.append(intro(intro_text))
        if top_extra:
            parts.append(f'<div class="px-gutter">{top_extra}</div>')
        parts.append(title_select(title_value, title_error, title_placeholder))
    else:
        if top_extra:
            parts.append(f'<div class="px-gutter">{top_extra}</div>')
    parts.append(fields_group(fields, count_label, renaming, error_key, error, extra_rows))
    body = '\n    '.join(parts)
    return f'''{bar or modal_bar()}
  {stepper("Map fields", n, total)}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-5 pb-6 pt-1">
    {body}
    </div>
  </div>
  {bottom_html or bottom(continue_label, continue_href, action)}
  {overlay}'''


# ------------------------------------------------------------------ frames
P.section('Field mapping by source', 'One layout for every source. Each row: detected field name, sample values from real records, type, show on cards, rename. The title field is chosen at the top. Steps without mapping (photos, manual entry) never show this screen.')

P.frame('S19-default', 'Default: Google Sheets (Flat hunt 2026, two tabs)', phone(mapping_screen(
    APT_FIELDS, '8 rows from Flat hunt 2026, tabs Kadıköy and Beşiktaş. Rename fields, set their type and choose what shows on cards.',
    title_value='Address', continue_href='S22-template-library.html#S22-import-pick')))

P.frame('S19-contacts', 'Contacts (88 selected)', phone(mapping_screen(
    CONTACT_FIELDS, '88 contacts with 7 fields. Rename fields, set their type and choose what shows on cards.',
    continue_href='S20-duplicate-review.html#S20-default')))

P.frame('S19-csv', 'CSV (candidates-q4.csv)', phone(mapping_screen(
    CSV_FIELDS, '12 rows and 8 columns from candidates-q4.csv. Rename fields, set their type and choose what shows on cards.',
    continue_href='S20-duplicate-review.html#S20-none', count_label='8 fields, 1 hidden by SwipeSort')))

TEXT_FIELD = dict(key='text', label='Text', type='text', title=True, samples='The Remains of the Day, Piranesi, Kürk Mantolu Madonna, Klara and the Sun')
text_tip = alert('info', 'Give the field a name', 'Cards and exports use it. For this list, Book or Title reads better than Text.', alert_button('Rename Text'))
P.frame('S19-text', 'Plain text: one field', phone(f'''{modal_bar()}
  {stepper("Map fields", 3, 4)}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-5 pb-6 pt-1">
    {intro("12 lines from your text become 12 items with one field. It is the title of every card.")}
    <div class="px-gutter">{text_tip}</div>
    {fields_group([TEXT_FIELD], "1 field", extra_rows="")}
    </div>
  </div>
  {bottom("Continue", "S22-template-library.html#S22-import-pick", "continue")}'''.replace(switch(True, 'Show Text on cards', extra='-mr-1'), '').replace('<p class="text-label text-muted-foreground">On cards</p>', '')))

# ------------------------------------------------------------------ editing
P.section('Editing a field', 'Rename inline. Type, title field and several values open bottom sheets (Select). Fields SwipeSort hides on its own sit in a collapsed group at the end.')

ren_fields = [dict(f) for f in CONTACT_FIELDS]
P.frame('S19-rename', 'Rename inline: Side becomes Family side', phone(mapping_screen(
    ren_fields[3:], '', renaming={'side': 'Family side'}, scrolled=True, count_label='7 fields',
    continue_href='S20-duplicate-review.html#S20-default')))

csv_by_key = {f['key']: f for f in CSV_FIELDS}
type_rows = [
    ('text', 'Text', '78000', None),
    ('number', 'Number', '78,000', None),
    ('phone', 'Phone', None, "Doesn't fit 11 values"),
    ('email', 'Email', None, "Doesn't fit 11 values"),
    ('date', 'Date', None, "Doesn't fit 11 values"),
    ('link', 'Link', None, "Doesn't fit 11 values"),
    ('image', 'Image', None, "Doesn't fit 11 values"),
]
tr = ''
for t, name, ex, warn in type_rows:
    sel = t == 'number'
    desc = f'Example: {ex}' if ex else warn
    tr += f'''<div><button role="radio" aria-checked="{"true" if sel else "false"}" class="flex min-h-14 w-full items-center gap-4 px-1 py-2 text-left">
        {icon(TYPES[t][0], "size-5 text-muted-foreground")}
        <span class="min-w-0 flex-1"><span class="block text-body">{name}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span>
        {radio_dot(sel)}</button></div>'''
type_sheet = sheet('ts1', 'Type of Expected salary', f'<div class="mt-2 divide-y" role="radiogroup" aria-label="Field type">{tr}</div>',
                   subtitle='The type changes how values look, sort and filter.')
P.frame('S19-type-sheet', 'Type picker sheet (Select)', phone(mapping_screen(
    CSV_FIELDS, '12 rows and 8 columns from candidates-q4.csv. Rename fields, set their type and choose what shows on cards.',
    continue_href='S20-duplicate-review.html#S20-none', overlay=type_sheet, count_label='8 fields, 1 hidden by SwipeSort')))

title_opts = [
    ('Name', 'type', 'Ayşe Demir, Mehmet Yılmaz', None, True),
    ('Phone', 'phone', '+90 500 000 97 62', 'Empty in 5 items', False),
    ('Email', 'mail', 'ayse.demir@example.com', 'Empty in 5 items', False),
    ('Side', 'type', "Bride's, Groom's", None, False),
    ('Relationship', 'type', 'Family, Friend', None, False),
    ('City', 'type', 'İstanbul, Ankara', None, False),
]
to = ''
for name, ic, smp, warn, sel in title_opts:
    w = f'<span class="block text-caption text-muted-foreground">{warn}</span>' if warn else ''
    to += f'''<div><button role="radio" aria-checked="{"true" if sel else "false"}" class="flex min-h-14 w-full items-center gap-4 px-1 py-2 text-left">
        {icon(ic, "size-5 text-muted-foreground")}
        <span class="min-w-0 flex-1"><span class="block text-body">{name}</span><span class="block truncate text-body-sm text-muted-foreground">{smp}</span>{w}</span>
        {radio_dot(sel)}</button></div>'''
title_sheet = sheet('tp1', 'Card title', f'<div class="mt-2 divide-y" role="radiogroup" aria-label="Title field">{to}</div><p class="mt-3 text-body-sm text-muted-foreground">Photo can\'t be the title. Image fields show in the card\'s image area.</p>',
                    subtitle='Choose the field shown as the largest text on each card.')
P.frame('S19-title-picker', 'Title field picker', phone(mapping_screen(
    CONTACT_FIELDS, '88 contacts with 7 fields. Rename fields, set their type and choose what shows on cards.',
    continue_href='S20-duplicate-review.html#S20-default', overlay=title_sheet)))

mv_opts = [
    ('All numbers in one field', 'Cards show the first number and how many more. Item details show all of them.', True, '+90 500 000 96 91 <span class="text-muted-foreground">+1</span>'),
    ('First number only', 'Other numbers are left out of this list. Your contacts aren\'t changed.', False, '+90 500 000 96 91'),
    ('One field per label', 'Creates Mobile, Home and Work fields, each with one number.', False, 'Mobile +90 500 000 96 91, Home +90 312 000 92 25'),
]
mo = ''
for name, desc, sel, prev in mv_opts:
    ring = 'border-2 border-primary' if sel else 'border'
    mo += f'''<div><button role="radio" aria-checked="{"true" if sel else "false"}" class="flex w-full items-start gap-3 rounded-control {ring} bg-card p-4 text-left">
        {radio_dot(sel)}
        <span class="min-w-0 flex-1"><span class="block text-body font-medium">{name}</span><span class="mt-0.5 block text-body-sm text-muted-foreground">{desc}</span>
        <span class="mt-2 block rounded-sm bg-muted px-3 py-2 text-body-sm tabular-nums"><span class="text-muted-foreground">Mehmet Yılmaz:</span> {prev}</span></span></button></div>'''
mv_sheet = sheet('mv1', 'Several phone numbers', f'<div class="mt-4 space-y-3" role="radiogroup" aria-label="How to handle several phone numbers">{mo}</div>',
                 actions=f'<button class="{PRIMARY}">Done</button>', subtitle='8 items have 2 or more numbers, like Mehmet Yılmaz.')
P.frame('S19-multi-value', 'Several values: phone numbers', phone(mapping_screen(
    CONTACT_FIELDS, '88 contacts with 7 fields. Rename fields, set their type and choose what shows on cards.',
    continue_href='S20-duplicate-review.html#S20-default', overlay=mv_sheet)))

role_row = field_row(CSV_AUTO_HIDDEN[0])
P.frame('S19-hidden-collapsed', 'Hidden by SwipeSort, collapsed (scrolled to the end)', phone(mapping_screen(
    CSV_FIELDS[3:], '', scrolled=True, count_label='8 fields, 1 hidden by SwipeSort',
    extra_rows=hidden_group(1, 'Role: same value in all 12 items'), continue_href='S20-duplicate-review.html#S20-none')))
P.frame('S19-hidden', 'Hidden by SwipeSort, expanded', phone(mapping_screen(
    CSV_FIELDS[4:], '', scrolled=True, count_label='8 fields, 1 hidden by SwipeSort',
    extra_rows=hidden_group(1, 'Role: same value in all 12 items', True, role_row), continue_href='S20-duplicate-review.html#S20-none')))

# ------------------------------------------------------------------ validation and limits
P.section('Validation and limits', 'Every card needs a title. Errors appear after Continue, at the field, with icon and text. Sources with more than 50 columns import the first 50 until the user chooses.')

no_title = [dict(f) for f in CONTACT_FIELDS]
no_title[0] = dict(no_title[0], title=False, shown=False)
P.frame('S19-error-no-title', 'Error: no title field (Name was hidden)', phone(mapping_screen(
    no_title, '88 contacts with 7 fields. Rename fields, set their type and choose what shows on cards.',
    title_value='Choose a field', title_placeholder=True, title_error='Choose a title field. Every card needs a title, and hiding Name removed it.',
    continue_href='#S19-error-no-title')))

csv_port = [dict(f) for f in CSV_FIELDS]
csv_port[0] = dict(csv_port[0], title=False)
csv_port[4] = dict(csv_port[4], title=True)
port_alert = alert('error', '2 items have no Portfolio', 'Marco Bianchi and Jakub Nowak would have cards without a title.',
                   alert_link('Choose another field', '#S19-title-picker') + alert_button('Skip 2 items'))
P.frame('S19-error-title-empty', 'Error: title field empty for some items', phone(mapping_screen(
    csv_port, '12 rows and 8 columns from candidates-q4.csv. Rename fields, set their type and choose what shows on cards.',
    title_value='Portfolio', title_error='Empty in 2 of 12 items.', top_extra='',
    continue_href='#S19-error-title-empty', count_label='8 fields, 1 hidden by SwipeSort').replace(
    '<div class="px-gutter">\n      <div class="flex items-end', f'<div class="px-gutter">{port_alert}</div>\n    <div class="px-gutter">\n      <div class="flex items-end', 1)))

ATS = [
    dict(key='name', label='Name', type='text', title=True, samples='Lena Hoffmann, Kaan Yurt, Aisha Bello'),
    dict(key='email', label='Email', type='email', samples='lena.hoffmann@example.com, kaan.yurt@example.com'),
    dict(key='stage', label='Stage', type='text', samples='Applied, Phone screen, Interview'),
    dict(key='applied', label='Applied on', type='date', samples='Sep 14, Sep 21, Oct 2'),
]
many_alert = alert('info', '64 columns found', 'Up to 50 fields can be imported. The first 50 columns are selected.', alert_link('Choose columns', '#S19-choose-columns'), ic='columns-3')
P.frame('S19-too-many', 'Too many columns: first 50 imported', phone(mapping_screen(
    ATS, '214 rows and 64 columns from applicants-export.xlsx.', top_extra=many_alert,
    continue_href='S20-duplicate-review.html#S20-none', count_label='50 fields')))

cols = [('Name', True), ('Email', True), ('Phone', True), ('Role', True), ('Location', True), ('Stage', True), ('Recruiter', True),
        ('Interview 3 score', True), ('Offer sent on', True), ('UTM campaign', False), ('UTM source', False), ('Referral bonus', False), ('Internal ID', False)]
cr = ''
for i, (name, on) in enumerate(cols):
    num = [1, 2, 3, 4, 5, 6, 7, 49, 50, 51, 52, 53, 54][i]
    dis = '' if on else ' disabled'
    op = '' if on else ' opacity-50'
    sep = '<li class="px-1 py-2 text-caption text-muted-foreground">Columns 8 to 48 selected</li>' if i == 7 else ''
    cr += f'''{sep}<li><button role="checkbox" aria-checked="{"true" if on else "false"}" class="flex min-h-12 w-full items-center gap-4 px-1 py-1.5 text-left{op}"{dis}>
        {checkbox_box(on)}<span class="min-w-0 flex-1 text-body">{name}</span><span class="text-caption tabular-nums text-muted-foreground">Column {num}</span></button></li>'''
cc_body = f'''<div class="relative mt-3 shrink-0"><label for="cs1" class="sr-only">Search columns</label>{icon("search", "pointer-events-none absolute left-3.5 top-3.5 size-5 text-muted-foreground")}<input id="cs1" type="search" class="h-12 w-full rounded-full border-0 bg-secondary pl-11 pr-4 text-body placeholder:text-muted-foreground" placeholder="Search columns"></div>
    <p class="mt-3 shrink-0 text-body-sm text-muted-foreground" role="status">50 of 50 selected. Unselect a column to choose another.</p>
    <ul class="mt-1 min-h-0 flex-1 divide-y overflow-hidden">{cr}</ul>'''
cc_sheet = sheet('cc1', 'Choose columns', cc_body, actions=f'<button class="{PRIMARY}">Done</button>', top='top-10', subtitle='applicants-export.xlsx, 64 columns')
P.frame('S19-choose-columns', 'Choose columns (limit 50)', phone(mapping_screen(
    ATS, '214 rows and 64 columns from applicants-export.xlsx.', top_extra=many_alert, overlay=cc_sheet,
    continue_href='S20-duplicate-review.html#S20-none', count_label='50 fields')))

# ------------------------------------------------------------------ loading
P.section('Loading', 'Fields and sample values are read from the selected items. Large files show a skeleton for up to a few seconds.')
sk_rows = ''.join(f'''<li class="flex items-center gap-3 px-4 py-4"><span class="flex-1 space-y-2"><span class="block h-3.5 w-{w} animate-pulse rounded-full bg-muted"></span><span class="block h-3 w-2/3 animate-pulse rounded-full bg-muted"></span></span><span class="h-8 w-13 animate-pulse rounded-full bg-muted"></span></li>''' for w in ['1/3', '1/2', '2/5', '1/3', '1/2'])
P.frame('S19-loading', 'Loading fields', phone(f'''{modal_bar()}
  {stepper("Map fields", 3, 5)}
  <div class="min-h-0 flex-1 space-y-5 overflow-hidden pt-1">
    <div class="px-gutter">{spinner_line("Reading fields from candidates-q4.csv…")}</div>
    <div class="px-gutter" aria-hidden="true"><ul class="divide-y overflow-hidden rounded-group bg-card">{sk_rows}</ul></div>
  </div>
  {bottom("Continue", disabled=True)}'''))

# ------------------------------------------------------------------ accessibility
P.section('Accessibility', 'At 200% text the row stacks: name, samples (wrapping), type and several-values selects, then a labeled switch row. The type icon box is dropped to give the text room.')
large = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="S08-home.html#S08-default" class="flex size-12 items-center justify-center rounded-full" aria-label="Close import">{icon("x", "size-7")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">Import</h1>
  </header>
  <div class="shrink-0 px-gutter pb-3"><p class="text-title-3">Map fields</p><p class="text-body-lg text-muted-foreground">Step 3 of 5</p>
    <div class="mt-2 flex gap-1" role="progressbar" aria-valuenow="3" aria-valuemin="1" aria-valuemax="5" aria-label="Step 3 of 5, Map fields"><span class="h-1.5 flex-1 rounded-full bg-primary"></span><span class="h-1.5 flex-1 rounded-full bg-primary"></span><span class="h-1.5 flex-1 rounded-full bg-primary"></span><span class="h-1.5 flex-1 rounded-full bg-muted"></span><span class="h-1.5 flex-1 rounded-full bg-muted"></span></div></div>
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-5 pb-6 pt-1">
    {fields_group(CONTACT_FIELDS[:4], "7 fields", large=True).replace('text-label text-muted-foreground">7 fields', 'text-title-3 font-normal text-muted-foreground">7 fields')}
    </div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3"><a href="S20-duplicate-review.html#S20-default" class="flex min-h-16 w-full items-center justify-center rounded-control bg-primary px-6 text-title-3 text-primary-foreground" data-action="continue">Continue</a></div>'''
P.frame('S19-large-text', 'Large text (200%)', phone(large))

# ------------------------------------------------------------------ platforms
P.section('iOS and web', 'iOS: 44 pt bar with a back chevron (edge swipe goes back a step) and close at the right; the type select is a pull-down menu; other choices open page sheets. Web: same as Android; selects open as popovers on desktop.')
ios_bar = modal_bar(ios=True, back=('Select items', 'S13-contacts-import.html#S13-select-default'))
P.frame('S19-ios', 'iOS', phone(mapping_screen(
    CONTACT_FIELDS, '88 contacts with 7 fields. Rename fields, set their type and choose what shows on cards.',
    bar=ios_bar, continue_href='S20-duplicate-review.html#S20-default'), ios=True))

menu_items = ''
for t in ['text', 'number', 'phone', 'email', 'date', 'link', 'image']:
    sel = t == 'phone'
    chk = icon('check', 'size-5 text-primary') if sel else '<span class="size-5"></span>'
    menu_items += f'<button role="menuitemradio" aria-checked="{"true" if sel else "false"}" class="flex h-12 w-full items-center gap-3 px-4 text-body">{chk}<span class="flex-1 text-left">{TYPES[t][1]}</span>{icon(TYPES[t][0], "size-5 text-muted-foreground")}</button>'
ios_menu = f'''<div class="absolute inset-0 z-10 bg-scrim/20"></div>
  <div class="absolute left-16 top-96 z-20 w-60 overflow-hidden rounded-control bg-popover py-1 shadow-overlay" role="menu" aria-label="Type of Phone">{menu_items}</div>'''
P.frame('S19-ios-type-menu', 'iOS: type as a pull-down menu', phone(mapping_screen(
    CONTACT_FIELDS, '88 contacts with 7 fields. Rename fields, set their type and choose what shows on cards.',
    bar=ios_bar, continue_href='S20-duplicate-review.html#S20-default', overlay=ios_menu), ios=True))

ios_mv_body = f'''<p class="mt-4 text-body-sm text-muted-foreground">8 items have 2 or more numbers, like Mehmet Yılmaz.</p>
    <div class="mt-4 space-y-3" role="radiogroup" aria-label="How to handle several phone numbers">{mo}</div>'''
P.frame('S19-ios-multi-value', 'iOS: several values as a page sheet', phone(mapping_screen(
    CONTACT_FIELDS, '88 contacts with 7 fields. Rename fields, set their type and choose what shows on cards.',
    bar=ios_bar, continue_href='S20-duplicate-review.html#S20-default',
    overlay=ios_sheet('imv', 'Several phone numbers', ios_mv_body)), ios=True))

pop_items = ''
for t, name, ex, warn in type_rows:
    sel = t == 'link'
    desc = 'Example: lenahoffmann.example' if t == 'link' else ("Doesn't fit 10 values" if t not in ('text',) else 'Example: https://lenahoffmann.example')
    pop_items += f'<button role="option" aria-selected="{"true" if sel else "false"}" class="flex min-h-12 w-full items-center gap-3 px-3 py-1.5 text-left {"bg-accent" if sel else ""}">{icon(TYPES[t][0], "size-5 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">{name}</span><span class="block text-caption text-muted-foreground">{desc}</span></span>{icon("check", "size-5 text-primary") if sel else ""}</button>'
popover = f'<div class="absolute left-9 top-60 z-20 w-64 overflow-hidden rounded-control bg-popover py-1 shadow-overlay" role="listbox" aria-label="Type of Portfolio">{pop_items}</div>'
web_screen = mapping_screen(CSV_FIELDS[4:], '', scrolled=True, count_label='8 fields, 1 hidden by SwipeSort',
                            continue_href='S20-duplicate-review.html#S20-none', overlay=popover)
P.frame('S19-web-desktop', 'Web, desktop: type select as a popover', desktop(web_screen, 'swipesort.app/import/fields'))

P.write('S19-field-mapping.html')
