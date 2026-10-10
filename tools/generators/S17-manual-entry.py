# Usage: python3 tools/generators/S17-manual-entry.py
# Generates design/03-screens/S17-manual-entry.html
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from groupc2_common import *  # noqa

P = Page('S17', 'Manual entry', 'A new list typed in by hand: define the fields first, then add items one after another. Field mapping and duplicate review are skipped. Spec: <a href="S17-manual-entry.md">S17-manual-entry.md</a>.')

CLOSE = 'S08-home.html#S08-default'
FINISH = 'S22-template-library.html#S22-import-pick'
PROD = {p['id']: p for p in DATA['products']}
FIELDS_SUMMARY = '5 fields: Name, Price (€), Store, Photo, Link'


def type_chip(t, label, locked=False):
    ic, name = TYPES[t]
    if locked:
        return f'<span class="inline-flex h-9 items-center gap-1.5 rounded-full bg-secondary px-3 text-label text-secondary-foreground">{icon(ic, "size-4")}{name}{icon("lock", "size-3.5")}<span class="sr-only">, the title is always text</span></span>'
    return f'<button class="inline-flex min-h-touch items-center" aria-haspopup="dialog" aria-label="Type: {name}. Change the type of {label}"><span class="inline-flex h-9 items-center gap-1.5 rounded-full border border-input bg-card px-3 text-label">{icon(ic, "size-4 text-muted-foreground")}{name}{icon("chevron-down", "size-4 text-muted-foreground")}</span></button>'


TITLE_BADGE = f'<span class="inline-flex h-6 shrink-0 items-center gap-1 rounded-full bg-primary-soft px-2 text-caption text-primary-soft-foreground">{icon("heading", "size-3.5")}Title</span>'

FIELDS = [('Name', 'text', True), ('Price (€)', 'number', False), ('Store', 'text', False), ('Photo', 'image', False), ('Link', 'link', False)]


def field_rows():
    out = ''
    for label, t, title in FIELDS:
        if title:
            head = f'<div class="flex items-center gap-2"><p class="text-body font-medium">{label}</p>{TITLE_BADGE}</div>'
            chip = f'<div class="mt-1.5 flex min-h-touch items-center">{type_chip(t, label, locked=True)}</div>'
            trail = icon_btn('pencil', f'Rename {label}', extra='text-muted-foreground')
        else:
            head = f'<p class="text-body font-medium">{label}</p>'
            chip = f'<div class="-mb-1 flex items-center">{type_chip(t, label)}</div>'
            trail = icon_btn('x', f'Remove {label}', extra='text-muted-foreground')
        out += f'<li class="flex items-center gap-2 py-2 pl-4 pr-1"><div class="min-w-0 flex-1">{head}{chip}</div>{trail}</li>'
    return out


def suggestion(label):
    return f'<button class="inline-flex min-h-touch items-center" aria-label="Add field {label}"><span class="inline-flex h-9 items-center gap-1.5 rounded-full border border-input bg-card px-3 text-label">{icon("plus", "size-4 text-muted-foreground")}{label}</span></button>'


def fields_screen(overlay='', bar=None):
    return f'''{bar or modal_bar('New list', CLOSE)}
  {stepper("Set up fields", 2, 4)}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-4 px-gutter pb-6 pt-1">
    <div><h2 class="text-title-2">Fields for your items</h2><p class="mt-1 text-body text-muted-foreground">Every item needs a title. Add fields you want to compare, like a price or a link.</p></div>
    <ul class="divide-y overflow-hidden rounded-group bg-card" aria-label="5 fields">{field_rows()}</ul>
    {btn('Add field', 'outline', 'plus', extra='w-full', action='add-field')}
    <div><p class="px-1 text-label text-muted-foreground">Suggestions</p><div class="flex flex-wrap gap-x-2">{suggestion('Rating')}{suggestion('Category')}{suggestion('Date')}</div></div>
    </div>
  </div>
  {bottom('Continue', '#S17-empty', 'continue')}
  {overlay}'''


# ------------------------------------------------------------------ items screen
def item_rows(ids, large=False):
    out = ''
    for pid in ids:
        p = PROD[pid]
        if large:
            out += f'''<li class="px-4 py-3"><div class="flex items-start gap-3"><img src="{IMG}products/{pid}.svg" alt="" class="size-14 shrink-0 rounded-sm object-cover"><div class="min-w-0 flex-1"><p class="text-title-3">{p["name"]}</p><p class="text-body-lg text-muted-foreground">{p["price"]}, {p["store"]}</p></div></div>
        <div class="mt-2 flex gap-2">{btn('Edit', 'outline', 'pencil', aria='Edit ' + p['name'], size='min-h-14', extra='flex-1 text-title-3 font-normal').replace(' text-label-lg ', ' ')}{btn('Delete', 'outline', 'trash-2', aria='Delete ' + p['name'], size='min-h-14', extra='flex-1 text-title-3 font-normal').replace(' text-label-lg ', ' ')}</div></li>'''
        else:
            out += f'''<li class="flex min-h-16 items-center gap-3 py-2 pl-4 pr-1"><img src="{IMG}products/{pid}.svg" alt="" class="size-10 shrink-0 rounded-sm object-cover"><div class="min-w-0 flex-1"><p class="truncate text-body">{p["name"]}</p><p class="truncate text-body-sm text-muted-foreground">{p["price"]}, {p["store"]}</p></div>{icon_btn('pencil', 'Edit ' + p['name'], href='#S17-edit-item' if pid == 'p02' else None, extra='text-muted-foreground')}{icon_btn('trash-2', 'Delete ' + p['name'], href='#S17-deleted' if pid == 'p01' else None, extra='text-muted-foreground')}</li>'''
    return out


def summary_line():
    return f'<div class="flex items-center justify-between gap-3"><p class="min-w-0 text-body-sm text-muted-foreground">{FIELDS_SUMMARY}</p><a href="#S17-fields" class="inline-flex min-h-touch shrink-0 items-center text-label text-primary underline underline-offset-4">Edit fields</a></div>'


def items_screen(ids, overlay='', bar=None, bottom_html=None):
    n = len(ids)
    return f'''{bar or modal_bar('New list', CLOSE)}
  {stepper("Add items", 3, 4)}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-4 px-gutter pb-6 pt-1">
    {summary_line()}
    <div class="flex items-center justify-between gap-3"><h2 class="text-title-3 tabular-nums">{n} items</h2>{btn('Add item', 'outline', 'plus', href='#S17-add-item', action='add-item')}</div>
    <ul class="divide-y overflow-hidden rounded-group bg-card" aria-label="{n} items">{item_rows(ids)}</ul>
    </div>
  </div>
  {bottom_html or bottom('Continue', FINISH, 'continue')}
  {overlay}'''


# ------------------------------------------------------------------ item form
def photo_tile(filled=None):
    if filled:
        return f'''<div><p class="text-label">Photo</p><div class="mt-1.5 flex items-center gap-3"><img src="{IMG}products/{filled}.svg" alt="Photo of the item" class="size-20 shrink-0 rounded-control object-cover">{btn('Change photo', 'ghost', extra='px-3')}</div></div>'''
    return f'''<div><p class="text-label">Photo</p><button class="mt-1.5 flex size-20 flex-col items-center justify-center gap-1 rounded-control border-2 border-dashed border-input bg-card text-caption text-muted-foreground" aria-label="Add photo">{icon("image-plus", "size-6")}Add photo</button></div>'''


def item_form(prefix, name='', price='', store='', link='', photo=None, name_err='', price_err='', focus_name=False):
    return f'''<div class="mt-3 min-h-0 flex-1 space-y-4 overflow-hidden">
      {label_input(prefix + 'n', 'Name', name, required=True, error=name_err, focused=focus_name and not name_err)}
      {label_input(prefix + 'p', 'Price (€)', price, error=price_err, ty='text')}
      {label_input(prefix + 's', 'Store', store)}
      {photo_tile(photo)}
      {label_input(prefix + 'l', 'Link', link, ty='url')}
    </div>'''


SECONDARY = 'flex h-14 flex-1 items-center justify-center rounded-control bg-secondary px-4 text-label-lg text-secondary-foreground'
PRIMARY_FLEX = 'flex h-14 flex-1 items-center justify-center rounded-control bg-primary px-4 text-label-lg text-primary-foreground'
ADD_ACTIONS = f'<div class="flex gap-3"><button class="{SECONDARY}" data-action="add-another">Add another</button><a href="#S17-default" class="{PRIMARY_FLEX}" data-action="add-item">Add item</a></div>'

P4 = PROD['p04']

# ------------------------------------------------------------------ frames
P.section('Set up fields', 'Manual entry has no source to map, so the user defines fields first. Name is the title and is always text; other fields can be added, retyped, renamed or removed.')
P.frame('S17-fields', 'Set up fields', phone(fields_screen()))

tr = ''
for t in ['text', 'number', 'phone', 'email', 'date', 'link', 'image']:
    sel = t == 'text'
    tr += f'<button role="radio" aria-checked="{"true" if sel else "false"}" class="flex min-h-12 w-full items-center gap-4 px-1 text-left">{icon(TYPES[t][0], "size-5 text-muted-foreground")}<span class="flex-1 text-body">{TYPES[t][1]}</span>{radio_dot(sel)}</button>'
fs_body = f'''<div class="mt-3 space-y-4">{label_input('fs-name', 'Field name', 'Category', focused=True)}
    <div><p class="text-label" id="fs-type">Type</p><div class="mt-1 divide-y" role="radiogroup" aria-labelledby="fs-type">{tr}</div></div></div>'''
P.frame('S17-field-sheet', 'Add field sheet', phone(fields_screen(overlay=sheet('fs1', 'Add field', fs_body, actions=f'<button class="{PRIMARY}">Add field</button>'))))

P.section('Add items', 'Items are added one at a time in a sheet. “Add another” saves and clears the form for fast entry; “Add item” saves and closes. Each added item can be edited or deleted (with undo).')

empty = f'''{modal_bar('New list', CLOSE)}
  {stepper("Add items", 3, 4)}
  <div class="flex min-h-0 flex-1 flex-col px-gutter pb-6 pt-1">
    {summary_line()}
    <div class="flex flex-1 flex-col items-center justify-center text-center">
      {icon("list-plus", "size-8 text-muted-foreground")}
      <h2 class="mt-4 text-title-3">No items yet</h2>
      <p class="mt-1 max-w-xs text-body text-muted-foreground">Add the first item. You can add more one after another.</p>
      <a href="#S17-add-item" class="mt-6 flex h-12 w-full max-w-xs items-center justify-center gap-2 rounded-control bg-primary text-label-lg text-primary-foreground" data-action="add-item">{icon("plus")}Add item</a>
    </div>
  </div>'''
P.frame('S17-empty', 'Empty: no items yet', phone(empty))
P.frame('S17-default', 'Default: 3 items added', phone(items_screen(['p01', 'p02', 'p03'])))

form = item_form('ai', P4['name'], str(P4['price']), P4['store'], 'keystone.example/p/1111', photo='p04')
P.frame('S17-add-item', 'New item sheet, filled', phone(items_screen(['p01', 'p02', 'p03'], overlay=sheet('ai1', 'New item', form, actions=ADD_ACTIONS, top='top-8'))))

added = f'<p class="mt-2 flex items-center gap-2 rounded-control bg-muted px-3 py-2 text-body-sm" role="status">{icon("check", "size-4 shrink-0")}Added Low-profile mechanical keyboard. 4 items.</p>'
form2 = added + item_form('aa', focus_name=True)
P.frame('S17-add-another', 'After “Add another”: form cleared for the next item', phone(items_screen(['p01', 'p02', 'p03', 'p04'], overlay=sheet('aa1', 'New item', form2, actions=ADD_ACTIONS, top='top-8'))))

form3 = item_form('va', '', '12o', 'Keystone', name_err='Enter a name. Every item needs a title.', price_err='Enter a number, like 389.')
P.frame('S17-validation', 'Validation: name missing, price not a number', phone(items_screen(['p01', 'p02', 'p03'], overlay=sheet('va1', 'New item', form3, actions=ADD_ACTIONS, top='top-8'))))

P2 = PROD['p02']
form4 = item_form('ed', P2['name'], str(P2['price']), P2['store'], 'oakline.example/p/1037', photo='p02')
EDIT_ACTIONS = f'<a href="#S17-default" class="{PRIMARY}" data-action="save">Save changes</a><a href="#S17-deleted" class="mt-1 flex h-12 w-full items-center justify-center gap-2 rounded-control text-label-lg text-destructive" data-action="delete">{icon("trash-2")}Delete item</a>'
P.frame('S17-edit-item', 'Edit an item', phone(items_screen(['p01', 'p02', 'p03'], overlay=sheet('ed1', 'Edit item', form4, actions=EDIT_ACTIONS, top='top-8'))))

P.frame('S17-deleted', 'Deleted, with undo', phone(items_screen(['p02', 'p03'], overlay=snackbar('Deleted Ergo Mesh task chair', 'Undo', bottom='bottom-28'))))

# ------------------------------------------------------------------ accessibility
P.section('Accessibility', 'At 200% text item titles wrap instead of truncating, and edit and delete become labeled buttons under each item.')
large = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="{CLOSE}" class="flex size-12 items-center justify-center rounded-full" aria-label="Close" data-action="close">{icon("x", "size-7")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">New list</h1>
  </header>
  <div class="shrink-0 px-gutter pb-3"><p class="text-title-3">Add items</p><p class="text-body-lg text-muted-foreground">Step 3 of 4</p>
    <div class="mt-2 flex gap-1" role="progressbar" aria-valuenow="3" aria-valuemin="1" aria-valuemax="4" aria-label="Step 3 of 4, Add items"><span class="h-1.5 flex-1 rounded-full bg-primary"></span><span class="h-1.5 flex-1 rounded-full bg-primary"></span><span class="h-1.5 flex-1 rounded-full bg-primary"></span><span class="h-1.5 flex-1 rounded-full bg-muted"></span></div></div>
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-4 px-gutter pb-6 pt-1">
    <div class="flex flex-wrap items-center justify-between gap-3"><h2 class="text-title-2 tabular-nums">3 items</h2>{btn('Add item', 'outline', 'plus', href='#S17-add-item', size='min-h-14', extra='text-title-3 font-normal').replace(' text-label-lg ', ' ')}</div>
    <ul class="divide-y overflow-hidden rounded-group bg-card" aria-label="3 items">{item_rows(['p01', 'p02', 'p03'], large=True)}</ul>
    </div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3"><a href="{FINISH}" class="flex min-h-16 w-full items-center justify-center rounded-control bg-primary px-6 text-title-3 text-primary-foreground" data-action="continue">Continue</a></div>'''
P.frame('S17-large-text', 'Large text (200%)', phone(large))

# ------------------------------------------------------------------ platforms
P.section('iOS', 'iOS: the item form is a page sheet with Cancel and Add in its own bar (Add = save and close); “Add another” sits under the form. The bar shows a back chevron to Set up fields. Web is the same as Android; the Photo field opens the browser’s file picker.')
ios_bar = modal_bar('New list', CLOSE, ios=True, back=('Set up fields', '#S17-fields'))
ios_form = item_form('io', P4['name'], str(P4['price']), P4['store'], 'keystone.example/p/1111', photo='p04').replace('mt-3 min-h-0 flex-1', 'mt-4 min-h-0 flex-1') + f'<div class="shrink-0 pb-8 pt-3"><button class="{SECONDARY} w-full" data-action="add-another">Add another</button></div>'
P.frame('S17-ios-add-item', 'iOS: new item as a page sheet', phone(items_screen(['p01', 'p02', 'p03'], bar=ios_bar, overlay=ios_sheet('io1', 'New item', ios_form, left='Cancel', right='Add')), ios=True))

P.write('S17-manual-entry.html')
