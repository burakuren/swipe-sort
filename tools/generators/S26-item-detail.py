# Usage: python3 tools/generators/S26-item-detail.py design/03-screens/S26-item-detail.html
# Generates the S26 Item detail, editing and notes mockup frames. Helpers: group_e_common.py.
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from group_e_common import *  # noqa
import group_e_common as _c


def section_header(*a, **k):  # S26 aligns every text edge to the gutter (QA-092)
    return _c.section_header(*a, **k).replace('px-1 pb-2', 'pb-2')

OUT = sys.argv[1]
F = Frames('S26')

SRC_CONTACTS = "From Contacts on this phone. Edits stay in SwipeSort; your contacts aren't changed."


# ------------------------------------------------------------------ read-mode parts
def edited_block(original, by=None, field='City', revert_href='#S26-revert-confirm'):
    if not original:
        return ''
    who = f'Edited by {by}' if by else 'Edited'
    return f'''<div class="flex flex-wrap items-center gap-x-3 gap-y-1 pb-1 pl-32 pr-2">
            {badge('edited', who)}
            <p class="min-w-0 text-body-sm text-muted-foreground">Original: <span class="text-foreground">{original}</span></p>
            <a href="{revert_href}" class="-ml-2 inline-flex h-12 items-center gap-1.5 rounded-control px-2 text-label text-primary" data-action="revert" aria-label="Revert {field} to the original, {original}">{icon("undo-2", "size-4")}Revert to original</a>
          </div>'''


def frow(label, value=None, meta='', edited=None, edited_by=None, editable=True, missing=None, multi=None, link=False, edit_href='#S26-edit', mono=False):
    """One field row: label column + value. value=None + missing='phone' → 'Add phone' (editable) or '—' (read-only)."""
    lab = f'<span class="w-24 shrink-0 pt-0.5 text-body-sm text-muted-foreground">{label}</span>'
    if multi:
        vals = ''.join(f'<span class="flex items-baseline justify-between gap-3"><span class="tabular-nums">{n}</span><span class="text-caption text-muted-foreground">{l}</span></span>' for n, l in multi)
        val = f'<span class="block min-w-0 flex-1 space-y-1 text-body">{vals}</span>'
    elif value is None:
        if editable:
            return f'''<li><a href="{edit_href}" class="flex min-h-12 w-full items-start gap-3 px-4 py-3 text-left">{lab}<span class="inline-flex min-w-0 flex-1 items-center gap-1.5 text-body text-primary">{icon("plus", "size-4")}Add {missing}</span></a></li>'''
        val = '<span class="block min-w-0 flex-1 text-body text-muted-foreground" aria-label="No value">—</span>'
    elif link:
        val = f'<span class="block min-w-0 flex-1 break-words text-body text-primary">{value}</span>'
        meta = icon('external-link', 'size-4 text-primary')
    else:
        val = f'<span class="block min-w-0 flex-1 break-words text-body tabular-nums">{value}</span>'
    meta_html = f'<span class="shrink-0 pt-0.5 text-caption text-muted-foreground">{meta}</span>' if meta else ''
    inner = f'{lab}{val}{meta_html}'
    if editable:
        main = f'<a href="{edit_href}" class="flex min-h-12 w-full items-start gap-3 px-4 py-3 text-left" aria-label="{label}: {value or ""}{", edited" if edited is not None else ""}. Edit">{inner}</a>'
    else:
        main = f'<div class="flex min-h-12 w-full items-start gap-3 px-4 py-3">{inner}</div>'
    return f'<li>{main}{edited_block(edited, edited_by, label)}</li>'


def fields_group(rows, edit=True, edit_href='#S26-edit', title='Fields'):
    trailing = f'<a href="{edit_href}" class="-my-3 -mr-2 inline-flex h-12 items-center gap-1.5 rounded-control px-2 text-label text-primary" data-action="edit">{icon("pencil", "size-4")}Edit</a>' if edit else ''
    return f'''{section_header(title, "pt-6", trailing)}
    <ul class="divide-y overflow-hidden rounded-group bg-card">{''.join(rows)}</ul>'''


def source_line(text):
    return f'<p class="flex items-start gap-2 pt-3 text-body-sm text-muted-foreground">{icon("info", "size-4 mt-0.5 shrink-0")}<span>{text}</span></p>'


def my_decision(kind=None, label='My decision', trailing=''):
    b = badge(kind) if kind else badge('none')
    return f'''<div class="flex min-h-12 items-center justify-between gap-3 pt-4">
      <span class="text-label text-muted-foreground">{label}</span>
      <span class="flex items-center gap-2">{trailing}{b}</span>
    </div>'''


def decision_picker(selected, label='My decision', note=''):
    btns = ''
    for kind in ('reject', 'maybe', 'accept'):
        ic, verb, state, _ = DEC[kind]
        on = kind == selected
        cls = f'bg-{kind} text-{kind}-foreground' if on else f'border border-input bg-card'
        icn = icon(ic, 'size-5') if on else icon(ic, f'size-5 text-{kind}-soft-foreground')
        btns += f'<button type="button" role="radio" aria-checked="{"true" if on else "false"}" class="flex h-12 items-center justify-center gap-1.5 rounded-control text-label-lg {cls}" data-action="decide-{kind}">{icn}{verb}</button>'
    return f'''{section_header(label, "pt-5")}
    <div class="grid grid-cols-3 gap-2" role="radiogroup" aria-label="{label}">{btns}</div>{note}'''


def note_card(text, who='you', when='Sep 28', private=False, actions=True, solo=False, edit_href='#S26-note-edit', delete_href='#S26-note-delete'):
    if solo:
        head = f'<p class="flex items-center justify-between gap-2 text-caption text-muted-foreground"><span>My note</span><span>{when}</span></p>'
    elif who == 'you':
        lab = f'{avatar("deniz", "size-6")}You'
        pb = badge('private') if private else ''
        head = f'<div class="flex items-center gap-2 text-caption text-muted-foreground"><span class="flex flex-1 items-center gap-1.5">{lab}</span>{pb}<span>{when}</span></div>'
    else:
        name = PEOPLE_AV[who][2]
        head = f'<div class="flex items-center gap-2 text-caption text-muted-foreground"><span class="flex flex-1 items-center gap-1.5">{avatar(who, "size-6")}{name}</span><span>{when}</span></div>'
    box = 'border border-dashed border-input' if private else 'bg-muted'
    acts = ''
    if actions:
        acts = f'''<div class="-mb-2 -ml-3 mt-1 flex"><a href="{edit_href}" class="inline-flex h-12 items-center gap-1.5 rounded-control px-3 text-label" data-action="edit-note">{icon("pencil", "size-4")}Edit</a><a href="{delete_href}" class="inline-flex h-12 items-center gap-1.5 rounded-control px-3 text-label" data-action="delete-note">{icon("trash-2", "size-4")}Delete</a></div>'''
    return f'<div class="rounded-control {box} px-3.5 pt-2.5 {"pb-2.5" if not actions else "pb-2"}">{head}<p class="mt-1.5 text-body">{text}</p>{acts}</div>'


def notes_section(cards='', add=True, shared=False, add_href='#S26-add-note', empty=True):
    add_btn = btn('Add note', 'outline', add_href, 'add-note', ic='sticky-note', extra='mt-1') if add else ''
    empty_p = '<p class="pb-2 text-body-sm text-muted-foreground">No notes yet. Notes are visible to all members unless you make them private.</p>' if (empty and not cards and shared) else (
        '<p class="pb-2 text-body-sm text-muted-foreground">No notes yet.</p>' if (empty and not cards) else '')
    return f'''{section_header("Notes", "pt-6")}
    {empty_p}
    <div class="space-y-2">{cards}</div>
    <div class="{"pt-3" if cards else ""}">{add_btn}</div>'''


def who_decided(rows, status, final=None, foot=''):
    lis = ''
    for who, kind, role in rows:
        name = 'Deniz (you)' if who == 'deniz' else PEOPLE_AV[who][2]
        rl = f'<span class="block text-caption text-muted-foreground">{role}</span>' if role else ''
        lis += f'<li class="flex min-h-14 items-center gap-3 px-4 py-2">{avatar(who, "size-8")}<span class="min-w-0 flex-1"><span class="block text-body">{name}</span>{rl}</span>{badge(kind) if kind else badge("none", "Not decided")}</li>'
    fb = badge(final) if final else ''
    return f'''{section_header("Who decided what", "pt-6", f'<span class="flex items-center gap-2">{badge(status)}{fb}</span>')}
    <ul class="divide-y overflow-hidden rounded-group bg-card" aria-label="Decisions by member">{lis}</ul>{foot}'''


def item_head(title, sub, photo=None, initials='', image=None, size='size-16', h='text-title-2', image_h='h-44', alt=''):
    if image:
        fit = 'bg-muted object-contain p-3' if image.startswith('products/') else 'object-cover'
        return f'''<img src="{IMG}{image}" alt="{alt}" class="{image_h} w-full rounded-group {fit}">
    <div class="pt-4"><h2 class="break-words {h}">{title}</h2><p class="mt-0.5 text-body text-muted-foreground">{sub}</p></div>'''
    av = avatar((photo, initials), size)
    return f'''<div class="flex items-center gap-4">{av}<div class="min-w-0 flex-1"><h2 class="break-words {h}">{title}</h2><p class="mt-0.5 text-body text-muted-foreground">{sub}</p></div></div>'''


def decide_bar():
    b = ''
    for kind in ('reject', 'maybe', 'accept'):
        ic, verb, _, _ = DEC[kind]
        b += f'<button type="button" class="flex h-12 items-center justify-center gap-1.5 rounded-full bg-{kind}-soft text-label-lg text-{kind}-soft-foreground" data-action="{kind}">{icon(ic)}{verb}</button>'
    return f'<div class="grid shrink-0 grid-cols-3 gap-2 border-t bg-popover px-gutter pb-4 pt-3" role="group" aria-label="Decide this item">{b}</div>'


def edit_bar(save_href='#S26-saved', cancel_href='#S26-default', disabled=False):
    return f'''<div class="grid shrink-0 grid-cols-2 gap-3 border-t bg-popover px-gutter pb-4 pt-3">
    {btn("Cancel", "outline", cancel_href, "cancel-edit")}
    {btn("Save changes", "primary", None if disabled else save_href, "save-edit", disabled=disabled)}
  </div>'''


def sheet_detail(content, tid, bottom='', top='top-24', head_title='Item details', expand=True, close_href='S25-sorting.html#S25-default'):
    ex = icon_btn('maximize-2', 'Open full screen', '#S26-expanded', 'expand', '', 'size-5') if expand else ''
    return sheet(f'''<div class="flex shrink-0 items-center gap-1 pl-gutter pr-2"><h1 id="{tid}" class="min-w-0 flex-1 text-label text-muted-foreground">{head_title}</h1>{ex}{icon_btn("x", "Close details", close_href, "close", "", "size-5")}</div>
    <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">{content}</div>
    {bottom}''', tid, top=top)


def over_sorting(sheet_html, bg=None, ios=False, extra=''):
    return f'{bg or s25_background()}{scrim()}{sheet_html}{extra}'


# ------------------------------------------------------------------ edit-mode parts
def inp(fid, label, value, typ='text', focus=False, error=None, suffix=None, helper=None, trailing=None, mode=None):
    border = 'border-2 border-destructive' if error else ('border border-primary ring-2 ring-ring/30' if focus else 'border border-input')
    inv = f' aria-invalid="true" aria-describedby="{fid}-e"' if error else (f' aria-describedby="{fid}-h"' if helper else '')
    im = f' inputmode="{mode}"' if mode else ''
    if suffix or trailing:
        tail = f'<span class="pr-3.5 text-body text-muted-foreground">{suffix}</span>' if suffix else trailing
        field = f'<div class="mt-1.5 flex h-12 items-center rounded-control bg-card {border}"><input id="{fid}" type="{typ}"{im} value="{value}" class="h-full min-w-0 flex-1 rounded-control bg-transparent px-3.5 text-body"{inv}>{tail}</div>'
    else:
        field = f'<input id="{fid}" type="{typ}"{im} value="{value}" class="mt-1.5 h-12 w-full rounded-control bg-card px-3.5 text-body {border}"{inv}>'
    err = f'<p id="{fid}-e" class="mt-1.5 flex items-start gap-1.5 text-body-sm text-destructive">{icon("circle-alert", "size-4 mt-0.5 shrink-0")}{error}</p>' if error else ''
    hlp = f'<p id="{fid}-h" class="mt-1.5 flex items-start gap-1.5 text-body-sm text-muted-foreground">{helper}</p>' if helper else ''
    return f'<div><label for="{fid}" class="text-label">{label}</label>{field}{err}{hlp}</div>'


def photo_edit(photo, initials, label='Photo'):
    """Contact photo in edit mode (D-32, A-170): no photo picker or camera. A photo from the source can be removed
    (Revert to original brings it back); a contact without one shows its initials and no action."""
    av = avatar((photo, initials), 'size-16')
    if photo:
        return f'''<div><p class="text-label">{label}</p><div class="mt-1.5 flex items-center gap-3">{av}<button type="button" class="inline-flex h-12 items-center gap-2 rounded-control border border-input bg-card px-4 text-label-lg" data-action="remove-image">{icon("trash-2")}Remove</button></div><p class="mt-1.5 text-body-sm text-muted-foreground">From Contacts. Removing it here doesn't change your contacts.</p></div>'''
    return f'''<div><p class="text-label">{label}</p><div class="mt-1.5 flex items-center gap-3">{av}<p class="text-body-sm text-muted-foreground">No photo in Contacts.</p></div></div>'''


def image_link_edit(fid, img, link, label='Photo', focus=False, original=None, contain=False):
    """Image field from an image link (CSV, Google Sheets, manual entry; A-131, A-160, A-170): edited as the link,
    with a leading `link` icon (every state, A-160) and a 36 thumbnail once it loads. Same control as S17's item form."""
    border = 'border border-primary ring-2 ring-ring/30' if focus else 'border border-input'
    fit = 'bg-muted object-contain p-0.5' if contain else 'object-cover'
    orig = f'<p class="mt-1.5 flex items-start gap-1.5 text-body-sm text-muted-foreground">{icon("pencil-line", "size-4 mt-0.5 shrink-0")}<span class="min-w-0 break-all">Original: {original}</span></p>' if original else ''
    return f'''<div><label class="text-label" for="{fid}">{label}</label><div class="mt-1.5 flex h-12 items-center gap-2 rounded-control bg-card pl-3.5 pr-1.5 {border}">{icon("link", "size-5 shrink-0 text-muted-foreground")}<input id="{fid}" type="url" class="h-full min-w-0 flex-1 bg-transparent text-body" value="{link}" aria-describedby="{fid}-h"><img src="{IMG}{img}" alt="" class="size-9 shrink-0 rounded-sm {fit}"></div>{orig}<p id="{fid}-h" class="mt-1.5 text-body-sm text-muted-foreground">Paste a link to an image. Cards show the picture from this link.</p></div>'''


def edit_form(fields_html, title_note=''):
    return f'''<p class="pb-4 pt-2 text-body-sm text-muted-foreground">{title_note or "Changes stay in SwipeSort. The source isn't changed."}</p>
    <div class="space-y-5">{fields_html}</div>'''


# ------------------------------------------------------------------ people data
def mia_fields(editable=True):
    return [
        frow('Name', 'Mia Andersson', editable=editable),
        frow('Phone', '+46 8 0000 4021', 'Mobile', editable=editable),
        frow('Email', 'mia.andersson@example.com', editable=editable),
        frow('Side', "Bride's", editable=editable),
        frow('Relationship', 'Colleague', editable=editable),
        frow('City', 'Stockholm', editable=editable),
    ]


def mia_content(large=False):
    return f'''{item_head('Mia Andersson', 'Colleague', 'people/c077.svg', 'MA')}
    {my_decision(None)}
    {fields_group(mia_fields())}
    {notes_section()}
    {source_line(SRC_CONTACTS)}'''


# ------------------------------------------------------------------ section: sheet over sorting
F.section('Item detail over sorting (bottom sheet)', 'Tap the card in S25 (or Enter on desktop web, or the card action "Open details"). The sheet opens at about 85% height; drag it up or use the expand button for full screen. Deciding from the sheet closes it and runs the commit on the card.')

F.add('S26-default', 'Default: Mia Andersson (c077) over the sorting screen', phone(over_sorting(
    sheet_detail(mia_content(), 'sd1', decide_bar()))))

expanded = f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    {icon_btn("chevron-down", "Back to sorting", "#S26-default", "collapse")}
    <p class="min-w-0 flex-1 truncate px-1 text-label text-muted-foreground">Wedding guests, Round 1</p>
  </header>
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">
    <img src="{IMG}people/c077.svg" alt="Photo of Mia Andersson" class="h-56 w-full rounded-group object-cover">
    <h1 class="pt-4 text-title-1">Mia Andersson</h1>
    <p class="mt-0.5 text-body-lg text-muted-foreground">Colleague</p>
    {my_decision(None)}
    {fields_group(mia_fields())}
    {notes_section()}
    {source_line(SRC_CONTACTS)}
  </div>
  {decide_bar()}'''
F.add('S26-expanded', 'Expanded to full screen (dragged up)', phone(expanded))

# Trip ideas (D-32, A-130): tr13 Alfama, Lisbon on the Photo template; image from the CSV's image link.
TR13_LINK = 'https://images.example/trips/alfama-lisbon.jpg'
SRC_TRIPS = "From trip-ideas.csv. Edits stay in SwipeSort; the file isn't changed."
photo_bg_body = s25_photo_card('ph13', 'Alfama, Lisbon', 'Portugal', 'Apr to Jun', '€900')
photo_content = f'''{item_head('Alfama, Lisbon', 'Portugal', image='photos/ph13.svg', image_h='h-60', alt='Image for Alfama, Lisbon')}
    {my_decision(None)}
    {fields_group([frow('Place', 'Alfama, Lisbon', edit_href='#S26-edit-image-link'), frow('Country', 'Portugal', edit_href='#S26-edit-image-link'), frow('Best time', 'Apr to Jun', edit_href='#S26-edit-image-link'), frow('Budget (EUR)', '900', edit_href='#S26-edit-image-link')], edit_href='#S26-edit-image-link')}
    {notes_section()}
    {source_line(SRC_TRIPS)}'''
F.add('S26-photo', 'Photo template item (tr13, Trip ideas): image from a link, place details', phone(over_sorting(
    sheet_detail(photo_content, 'sd2', decide_bar(), close_href='S25-sorting.html#S25-photo'),
    s25_background(photo_bg_body, 'Trip ideas', 'Round 1', 12, 30, (6, 1, 5), nxt=s25_photo_card('ph12', 'Göreme, Cappadocia', 'Türkiye', 'Apr to May', '€700')))))

c014_bg = s25_person('Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein', 'Friend', 'people/c014.svg', [('Email', 'maximiliane.hohenberg-lichtenstein@example.net'), ('City', 'Berlin')], ["Bride's"])
c014_fields = [
    frow('Name', 'Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein'),
    frow('Phone', None, missing='phone'),
    frow('Email', 'maximiliane.hohenberg-lichtenstein@example.net'),
    frow('Side', "Bride's"),
    frow('Relationship', 'Friend'),
    frow('City', 'Berlin'),
]
c014_content = f'''{item_head('Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein', 'Friend', 'people/c014.svg', 'MH')}
    {my_decision(None)}
    {notes_section(note_card('Flying in from Berlin. Ask about dates first.', solo=True, when='Sep 28'), add=False)}
    {fields_group(c014_fields)}'''
F.add('S26-long-text', 'Long name and email wrap in full; missing phone shows "Add phone"; my note', phone(over_sorting(
    sheet_detail(c014_content, 'sd3', decide_bar(), close_href='S25-sorting.html#S25-long-text'),
    s25_background(c014_bg, done=13, counts=(2, 3, 8)))))

# ------------------------------------------------------------------ section: editing
F.section('Editing fields', 'Edit (or tap any field) switches the fields into inputs in place. Each field type gets its own keyboard and control. Save changes writes to the working copy; changed fields are marked Edited and keep their original value. Image fields have no photo library or camera (D-32): a contact photo can only be removed, an image from a link is edited as its link.')

c007_edit = f'''{edit_form(photo_edit(None, 'GD') + inp('e-name', 'Name', 'Gökhan Doğan') + inp('e-phone', 'Phone', '+90 500 000 97 41', 'tel', focus=True, helper=f'{icon("pencil-line", "size-4 mt-0.5 shrink-0")}<span>Original: +90 500 000 97 4</span>') + inp('e-email', 'Email', 'gokhan.dogan@example.com', 'email') + inp('e-side', 'Side', "Groom's") + inp('e-rel', 'Relationship', 'Friend') + inp('e-city', 'City', 'Bursa'))}'''
F.add('S26-edit', 'Editing fields in place (Gökhan Doğan c007: fixing a phone typo)', phone(over_sorting(
    sheet_detail(c007_edit, 'se1', edit_bar('#S26-saved', '#S26-default'), head_title='Edit Gökhan Doğan', expand=False),
    s25_background(s25_person('Gökhan Doğan', 'Friend', None, [('Phone', '+90 500 000 97 4'), ('Email', 'gokhan.dogan@example.com'), ('City', 'Bursa')], ["Groom's"], 'GD'), done=6, counts=(1, 2, 3)))))

c007_err = f'''{edit_form(inp('x-name', 'Name', 'Gökhan Doğan') + inp('x-phone', 'Phone', '+90 500 000 97 41', 'tel') + inp('x-email', 'Email', 'gokhan.dogan@example', 'email', error='Enter a full email address, like name@example.com.') + inp('x-side', 'Side', "Groom's") + inp('x-rel', 'Relationship', 'Friend'))}'''
F.add('S26-edit-error', 'Validation error: invalid email (Save keeps the form open, focus moves to the field)', phone(over_sorting(
    sheet_detail(c007_err, 'se2', edit_bar('#S26-edit-error', '#S26-default'), head_title='Edit Gökhan Doğan', expand=False),
    s25_background(s25_person('Gökhan Doğan', 'Friend', None, [('Phone', '+90 500 000 97 4')], ["Groom's"], 'GD'), done=6, counts=(1, 2, 3)))))

c007_saved_fields = [
    frow('Name', 'Gökhan Doğan'),
    frow('Phone', '+90 500 000 97 41', 'Mobile', edited='+90 500 000 97 4', edit_href='#S26-edit'),
    frow('Email', 'gokhan.dogan@example.com'),
    frow('Side', "Groom's"),
    frow('Relationship', 'Friend'),
    frow('City', 'Bursa'),
]
c007_saved = f'''{item_head('Gökhan Doğan', 'Friend', None, 'GD')}
    {my_decision(None)}
    {fields_group(c007_saved_fields)}'''
c007_saved_scrolled = f'<div class="-mt-16 pb-24">{c007_saved}</div>'
F.add('S26-saved', 'Saved: the field is marked Edited and keeps its original', phone(over_sorting(
    sheet_detail(c007_saved_scrolled, 'se3', decide_bar()),
    s25_background(s25_person('Gökhan Doğan', 'Friend', None, [('Phone', '+90 500 000 97 41', True)], ["Groom's"], 'GD'), done=6, counts=(1, 2, 3)),
    extra=snackbar('Changes saved', bottom='bottom-24'))))

multi_edit = f'''{back_bar('', 'S28-results.html#S28-shared', 'Back to results')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">
    <h1 class="text-title-2">Edit fields</h1>
    {edit_form(f"""<fieldset class="min-w-0"><legend class="text-label">Phone</legend>
        <div class="mt-1.5 space-y-2">
          <div class="flex items-center gap-2"><button type="button" class="inline-flex h-12 w-28 shrink-0 items-center justify-between rounded-control border border-input bg-card px-3 text-body" aria-label="Label: Mobile" aria-haspopup="listbox">Mobile{icon("chevron-down", "size-4 text-muted-foreground")}</button><input type="tel" aria-label="Mobile number" value="+90 500 000 96 91" class="h-12 min-w-0 flex-1 rounded-control border border-input bg-card px-3.5 text-body">{icon_btn("x", "Remove this number", None, None, "", "size-5")}</div>
          <div class="flex items-center gap-2"><button type="button" class="inline-flex h-12 w-28 shrink-0 items-center justify-between rounded-control border border-input bg-card px-3 text-body" aria-label="Label: Home" aria-haspopup="listbox">Home{icon("chevron-down", "size-4 text-muted-foreground")}</button><input type="tel" aria-label="Home number" value="+90 312 000 92 25" class="h-12 min-w-0 flex-1 rounded-control border border-primary bg-card px-3.5 text-body ring-2 ring-ring/30">{icon_btn("x", "Remove this number", None, None, "", "size-5")}</div>
        </div>
        <button type="button" class="mt-1 inline-flex h-12 items-center gap-2 rounded-control pr-3 text-label-lg text-primary">{icon("plus")}Add another phone</button>
        <p class="text-body-sm text-muted-foreground">The first number shows on the card.</p>
      </fieldset>""" + inp('m-email', 'Email', 'mehmet.yilmaz@example.com', 'email') + inp('m-city', 'City', 'İstanbul'))}
  </div>
  {edit_bar('S28-results.html#S28-shared', '#S26-shared-conflict')}'''
F.add('S26-edit-multi', 'Multi-value field: two phone numbers (Mehmet Yılmaz c002)', phone(multi_edit))

p03_edit = f'''{back_bar('', 'S28-results.html#S28-default', 'Back to results')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">
    <h1 class="text-title-2">Edit fields</h1>
    {edit_form(image_link_edit('p-photo', 'products/p03.svg', 'https://pixelhaus.example/img/4k-27.jpg', contain=True) +
              inp('p-name', 'Name', '27-inch 4K USB-C monitor') +
              inp('p-price', 'Price', '399', 'text', focus=True, suffix='EUR', mode='decimal', helper=f'{icon("pencil-line", "size-4 mt-0.5 shrink-0")}<span>Original: 429</span>') +
              '<div class="grid grid-cols-2 gap-3">' + inp('p-rating', 'Rating', '4.5', 'text', mode='decimal') + inp('p-reviews', 'Reviews', '2,870', 'text', mode='numeric') + '</div>' +
              inp('p-link', 'Link', 'https://pixelhaus.example/p/1074', 'url', trailing=icon_btn('external-link', 'Open link', None, None, '', 'size-5')))}
  </div>
  {edit_bar('#S26-product', '#S26-product')}'''
F.add('S26-edit-product', 'Product fields: image link, number with unit, link (p03)', phone(p03_edit))

link_edit = f'''{edit_form(image_link_edit('l-photo', 'photos/ph13.svg', TR13_LINK, focus=True) + inp('l-place', 'Place', 'Alfama, Lisbon') + inp('l-country', 'Country', 'Portugal') + inp('l-best', 'Best time', 'Apr to Jun') + inp('l-budget', 'Budget', '900', 'text', suffix='EUR', mode='decimal'))}'''
F.add('S26-edit-image-link', 'Image field from a link (tr13): edited as its link, no photo picker (D-32)', phone(over_sorting(
    sheet_detail(link_edit, 'se4', edit_bar('#S26-photo', '#S26-photo'), head_title='Edit Alfama, Lisbon', expand=False, close_href='S25-sorting.html#S25-photo'),
    s25_background(photo_bg_body, 'Trip ideas', 'Round 1', 12, 30, (6, 1, 5), nxt=s25_photo_card('ph12', 'Göreme, Cappadocia', 'Türkiye', 'Apr to May', '€700')))))

# ------------------------------------------------------------------ section: edited and revert
F.section('Edited fields and revert', 'Edited fields carry a pencil-line Edited badge, the original value and Revert to original (SAFE-03, SAFE-04). Revert asks first and offers Undo afterwards. When a later edit by another member replaced mine at sync, the item opened from the S40 snackbar asks Keep mine / Use Mert\'s (D-09 row 1, A-70).')
c045_bg = s25_person('Alper Turan', 'Friend', 'people/c045.svg', [('Phone', '+90 500 000 07 64'), ('Email', 'alper.turan@example.com'), ('City', 'Ankara', True)], ["Groom's"])


def c045(edited=True):
    rows = [frow('Name', 'Alper Turan'), frow('Phone', '+90 500 000 07 64', 'Mobile'), frow('Email', 'alper.turan@example.com'),
            frow('Side', "Groom's"), frow('Relationship', 'Friend'),
            frow('City', 'Ankara', edited='İstanbul') if edited else frow('City', 'İstanbul')]
    return f'''{item_head('Alper Turan', 'Friend', 'people/c045.svg', 'AT')}
    {my_decision(None)}
    {fields_group(rows)}
    {source_line(SRC_CONTACTS)}'''


F.add('S26-edited', 'Edited field with original value and Revert (Alper Turan c045, City)', phone(over_sorting(
    sheet_detail(c045(), 'sr1', decide_bar(), close_href='S25-sorting.html#S25-edited'), s25_background(c045_bg, done=44, counts=(8, 6, 30)))))
rv = dialog('rvd', 'Revert City to the original?', '<p>City goes back to “İstanbul”, the value from Contacts. Your edit “Ankara” is removed.</p>',
            btn('Cancel', 'ghost', '#S26-edited', 'cancel', full=False) + btn('Revert', 'destructive', '#S26-reverted', 'confirm-revert', full=False))
F.add('S26-revert-confirm', 'Revert confirmation', phone(over_sorting(
    sheet_detail(c045(), 'sr2', decide_bar(), close_href='S25-sorting.html#S25-edited'), s25_background(c045_bg, done=44, counts=(8, 6, 30)), extra=scrim('bg-scrim/50', 'z-20') + rv)))
F.add('S26-reverted', 'Reverted, with Undo', phone(over_sorting(
    sheet_detail(c045(False), 'sr3', decide_bar(), close_href='S25-sorting.html#S25-edited'), s25_background(c045_bg, done=44, counts=(8, 6, 30)),
    extra=snackbar('City reverted to İstanbul', 'Undo', bottom='bottom-24'))))

# D-09 row 1 (A-70, A-172): opened from the S40 snackbar "Mert changed City on Alper Turan after you…" (View),
# the inline "Keep mine / Use Mert's" choice waits above the fields until answered (not only in edit mode).
replaced_alert = f'''<div class="mt-6 rounded-control border bg-card p-4" role="region" aria-labelledby="er1">
      <div class="flex gap-3">{icon("pencil-line", "size-5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1">
        <p id="er1" class="text-label">Mert changed City after you</p>
        <p class="mt-0.5 text-body-sm text-muted-foreground">Your edit “Ankara” was replaced with Mert's “Eskişehir”. Keep your version or use Mert's?</p>
      </div></div>
      <div class="mt-3 grid grid-cols-2 gap-2">{btn("Keep mine", "outline", "#S26-edit-replaced-kept", "keep-mine")}{btn("Use Mert's", "outline", "#S26-edit-replaced-theirs", "use-theirs")}</div>
    </div>'''
replaced_rows = [frow('Name', 'Alper Turan'), frow('Phone', '+90 500 000 07 64', 'Mobile'), frow('Email', 'alper.turan@example.com'),
                 frow('Side', "Groom's"), frow('Relationship', 'Friend'), frow('City', 'Eskişehir', edited='İstanbul', edited_by='Mert')]
def replaced_screen(alert_html, rows, snack=''):
    return f'''{back_bar('', 'S09-list-overview.html#S09-shared', 'Back to Wedding guests', trailing=icon_btn("ellipsis-vertical", "More options", None, "menu"))}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">
    {item_head('Alper Turan', 'Friend', 'people/c045.svg', 'AT')}
    {alert_html}
    {fields_group(rows)}
  </div>
  {snack}'''


def alper_rows(city, by=None):
    return [frow('Name', 'Alper Turan'), frow('Phone', '+90 500 000 07 64', 'Mobile'), frow('Email', 'alper.turan@example.com'),
            frow('Side', "Groom's"), frow('Relationship', 'Friend'), frow('City', city, edited='İstanbul', edited_by=by)]


F.add('S26-edit-replaced', "Opened from the sync-outcome snackbar: my edit was replaced; Keep mine / Use Mert's waits (D-09 row 1)", phone(replaced_screen(replaced_alert, replaced_rows)))
F.add('S26-edit-replaced-kept', '"Keep mine": my value applies again as a new edit', phone(replaced_screen('', alper_rows('Ankara'), snackbar('Kept your edit', bottom='bottom-6'))))
F.add('S26-edit-replaced-theirs', '"Use Mert\'s": Mert\'s value stays, the choice closes', phone(replaced_screen('', alper_rows('Eskişehir', 'Mert'), snackbar("Using Mert's edit", bottom='bottom-6'))))

# ------------------------------------------------------------------ section: notes
F.section('Notes', 'One note per member per item. On shared lists notes are visible to all members by default; a private note shows a lock, "Only you" and a dashed outline (DM-18, DM-19). Solo lists have no private option.')

note_edit = f'''{item_head('Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein', 'Friend', 'people/c014.svg', 'MH')}
    {section_header("Notes", "pt-6")}
    <label for="ne1" class="sr-only">My note</label>
    <textarea id="ne1" rows="4" class="w-full resize-none rounded-control border border-primary bg-card px-3.5 py-3 text-body ring-2 ring-ring/30">Flying in from Berlin. Ask about dates first. She prefers the Saturday.</textarea>
    <div class="mt-1 flex justify-end"><span class="text-caption tabular-nums text-muted-foreground">69 / 1,000</span></div>
    <div class="mt-2 grid grid-cols-2 gap-3">{btn("Cancel", "outline", "#S26-long-text", "cancel-note")}{btn("Save note", "primary", "#S26-long-text", "save-note")}</div>'''
F.add('S26-note-edit', 'Editing my note (solo list: no private option)', phone(over_sorting(
    sheet_detail(note_edit, 'sn1', close_href='S25-sorting.html#S25-long-text'), s25_background(c014_bg, done=13, counts=(2, 3, 8)))))

nd = dialog('ndd', 'Delete your note?', '<p>“Flying in from Berlin. Ask about dates first.” will be deleted from this item.</p>',
            btn('Cancel', 'ghost', '#S26-long-text', 'cancel', full=False) + btn('Delete note', 'destructive', '#S26-long-text', 'confirm-delete-note', full=False))
F.add('S26-note-delete', 'Delete note confirmation', phone(over_sorting(
    sheet_detail(c014_content, 'sn2', decide_bar(), close_href='S25-sorting.html#S25-long-text'), s25_background(c014_bg, done=13, counts=(2, 3, 8)), extra=scrim('bg-scrim/50', 'z-20') + nd)))

c012_bg = s25_person('Gülşen Aydın', 'Family', None, [('Phone', '+90 500 000 26 84'), ('Email', 'gulsen.aydin@example.com'), ('City', 'Ankara')], ["Groom's"], 'GA')
add_note = f'''{item_head('Gülşen Aydın', 'Family', None, 'GA')}
    {section_header("Notes", "pt-6")}
    <div class="space-y-2">{note_card("Haven't seen her in years, maybe skip?", 'selin', 'Oct 3', actions=False)}</div>
    <div class="mt-4 rounded-control border border-dashed border-input p-3">
      <label for="an1" class="text-label">Your note</label>
      <textarea id="an1" rows="3" class="mt-1.5 w-full resize-none rounded-control border border-primary bg-card px-3.5 py-3 text-body ring-2 ring-ring/30">Ask Mert if his parents still see her.</textarea>
      <div class="mt-1 flex justify-end"><span class="text-caption tabular-nums text-muted-foreground">37 / 1,000</span></div>
      <div class="flex min-h-12 items-center gap-3"><span class="flex flex-1 items-center gap-2 text-body">{icon("lock", "size-5 text-muted-foreground")}Only visible to me</span>{switch(True, "Only visible to me")}</div>
      <p class="pb-1 text-body-sm text-muted-foreground">Mert and Selin won't see this note.</p>
      <div class="mt-2 grid grid-cols-2 gap-3">{btn("Cancel", "outline", "#S26-shared-hidden", "cancel-note")}{btn("Save note", "primary", "#S26-private-note", "save-note")}</div>
    </div>'''
F.add('S26-add-note', 'Add a note on a shared list, "Only visible to me" on (Gülşen Aydın c012)', phone(over_sorting(
    sheet_detail(add_note, 'sn3', close_href='S25-sorting.html#S25-shared'),
    s25_background(c012_bg, sub='Round 1, shared', done=76, counts=(17, 11, 48)))))

c006_rows = [frow('Name', 'Burak Arslan'), frow('Phone', '+90 500 000 95 92', 'Mobile'), frow('Email', 'burak.arslan@example.com'), frow('Side', "Groom's"), frow('Relationship', 'Colleague'), frow('City', 'İstanbul')]
private_note = f'''{back_bar('', 'S28-results.html#S28-shared', 'Back to results')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">
    {item_head('Burak Arslan', 'Colleague', 'people/c006.svg', 'BA', h='text-title-1')}
    {decision_picker('accept')}
    {who_decided([('deniz', 'accept', ''), ('mert', 'accept', 'Decision Maker'), ('selin', 'accept', '')], 'agreed', 'accept')}
    {notes_section(note_card('Only if we invite the whole team.', 'you', 'Sep 28', private=True), add=False)}
    {fields_group(c006_rows)}
  </div>'''
F.add('S26-private-note', 'My private note (lock, "Only you", dashed) on an Agreed item (Burak Arslan c006)', phone(private_note))

# ------------------------------------------------------------------ section: shared
F.section("Shared lists: who decided what", "Every item shows each member's decision with icon and label, the list status and the final decision (COL-16). While sorting with others' decisions hidden (SRT-12), the sheet keeps them hidden until I decide.")

c002_rows = [frow('Name', 'Mehmet Yılmaz'), frow('Phone', multi=[('+90 500 000 96 91', 'Mobile'), ('+90 312 000 92 25', 'Home')], edit_href='#S26-edit-multi'),
             frow('Email', 'mehmet.yilmaz@example.com'), frow('Side', "Bride's"), frow('Relationship', 'Family'), frow('City', 'İstanbul')]
conflict_foot = f'''<div class="flex flex-wrap items-center justify-between gap-x-3 pt-2"><p class="text-body-sm text-muted-foreground">Mert resolves conflicts as Decision Maker.</p><a href="S36-conflicts.html#S36-default" class="-mr-2 inline-flex h-12 items-center rounded-control px-2 text-label text-primary" data-action="review-conflicts">Review conflicts</a></div>'''
c002 = f'''{back_bar('', 'S28-results.html#S28-shared', 'Back to results', trailing=icon_btn("ellipsis-vertical", "More options", None, "menu"))}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">
    {item_head('Mehmet Yılmaz', 'Family', 'people/c002.svg', 'MY', h='text-title-1')}
    {decision_picker('accept', note='<p class="pt-2 text-body-sm text-muted-foreground">Changing your decision updates the list status for everyone.</p>')}
    {who_decided([('deniz', 'accept', ''), ('mert', 'reject', 'Decision Maker'), ('selin', 'accept', '')], 'conflict', None, conflict_foot)}
    {fields_group(c002_rows)}
    {notes_section(shared=True)}
  </div>'''
F.add('S26-shared-conflict', 'Shared item in Conflict, pushed from Results: who decided what, two phone numbers (c002)', phone(c002))

c079_bg = s25_person('Babaanne (Nermin Aydın)', 'Family', None, [('Phone', '+90 500 000 47 87'), ('City', 'Ankara')], ["Groom's"], 'BA')
c079_rows = [frow('Name', 'Babaanne (Nermin Aydın)', edited='Babaanne', edited_by='Mert', ),
             frow('Phone', '+90 500 000 47 87', 'Mobile'), frow('Email', None, missing='email'), frow('Side', "Groom's"), frow('Relationship', 'Family'), frow('City', 'Ankara')]
hidden_note = f'''<div class="flex items-start gap-3 rounded-control bg-muted p-3.5">{icon("eye-off", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="text-body-sm">Others' decisions stay hidden until you decide, so they don't sway you.</p><p class="mt-0.5 text-body-sm text-muted-foreground">To see them while sorting, turn on Show others' decisions in the sorting menu.</p></div></div>'''
c079 = f'''{item_head('Babaanne (Nermin Aydın)', 'Family', None, 'BA')}
    {my_decision(None)}
    {section_header("Who decided what", "pt-6", badge('pending', 'Pending'))}
    {hidden_note}
    {notes_section(note_card('Obviously yes.', 'mert', 'Sep 29', actions=False), shared=True)}
    {fields_group(c079_rows)}'''
F.add('S26-shared-hidden', "Shared list while sorting: others' decisions hidden, Mert's note and edit visible (c079)", phone(over_sorting(
    sheet_detail(c079, 'ss2', decide_bar(), close_href='S25-sorting.html#S25-shared'),
    s25_background(c079_bg, sub='Round 1, shared', done=76, counts=(17, 11, 48)))))

# ------------------------------------------------------------------ section: from results (change decision)
F.section('Opened from Results: change decision', 'Pushed from an S28 row. My decision becomes a segmented Reject, Maybe, Accept control (RES-06); a change shows a snackbar with Undo. Products and places use the same screen.')


def p03(selected='accept', snack=''):
    rows = [frow('Name', '27-inch 4K USB-C monitor', edit_href='#S26-edit-product'), frow('Price', '€429', edit_href='#S26-edit-product'),
            frow('Rating', '4.5', '2,870 reviews', edit_href='#S26-edit-product'), frow('Store', 'Pixelhaus', edit_href='#S26-edit-product'),
            frow('Category', 'Monitor', edit_href='#S26-edit-product'), frow('Link', 'pixelhaus.example/p/1074', link=True, edit_href='#S26-edit-product')]
    return f'''{back_bar('', 'S28-results.html#S28-default', 'Back to results', trailing=icon_btn("ellipsis-vertical", "More options", None, "menu"))}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">
    {item_head('27-inch 4K USB-C monitor', 'Pixelhaus', image='products/p03.svg', image_h='h-48', alt='27-inch 4K USB-C monitor', h='text-title-1')}
    {decision_picker(selected, note='<p class="pt-2 text-body-sm text-muted-foreground">Decided in Round 1, Oct 4.</p>' if selected == 'accept' else '<p class="pt-2 text-body-sm text-muted-foreground">Changed just now. Round 1 history keeps the original decision.</p>')}
    {fields_group(rows, edit_href='#S26-edit-product')}
    {notes_section()}
    {source_line("Added by hand on Oct 4.")}
  </div>
  {snack}'''


F.add('S26-product', 'Product item (p03, Desk setup) from Results with the decision control', phone(p03()))
F.add('S26-decision-changed', 'Decision changed to Maybe, with Undo', phone(p03('maybe', snackbar('Changed to Maybe', 'Undo'))))

# ------------------------------------------------------------------ section: states
F.section('States', 'Loading, offline save, an item removed by another member, and read-only archived lists.')
loading = f'''{back_bar('', 'S28-results.html#S28-default', 'Back to results')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6" role="status" aria-busy="true" aria-label="Loading item">
    <div class="h-48 animate-pulse rounded-group bg-muted"></div>
    <span class="mt-5 block h-7 w-3/4 animate-pulse rounded-full bg-muted"></span>
    <span class="mt-3 block h-4 w-1/3 animate-pulse rounded-full bg-muted"></span>
    <div class="mt-6 grid grid-cols-3 gap-2"><span class="h-12 animate-pulse rounded-control bg-muted"></span><span class="h-12 animate-pulse rounded-control bg-muted"></span><span class="h-12 animate-pulse rounded-control bg-muted"></span></div>
    <div class="mt-8 space-y-4 rounded-group bg-card p-4">{''.join('<div class="space-y-2"><span class="block h-3 w-16 animate-pulse rounded-full bg-muted"></span><span class="block h-4 w-2/3 animate-pulse rounded-full bg-muted"></span></div>' for _ in range(5))}</div>
  </div>'''
F.add('S26-loading', 'Loading (pushed from Results)', phone(loading))

offline = f'''{back_bar('', 'S28-results.html#S28-shared', 'Back to results')}
  {offline_banner()}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-4">
    {item_head('Gökhan Doğan', 'Friend', None, 'GD', h='text-title-1')}
    {decision_picker('accept')}
    {fields_group(c007_saved_fields)}
  </div>
  {snackbar("Saved on this phone. It will sync when you're back online.", ic='clock-arrow-up')}'''
F.add('S26-offline-saved', 'Saving offline: kept on this phone, syncs later', phone(offline))

nf = f'''{back_bar('', 'S28-results.html#S28-shared', 'Back to results')}
  <div class="flex flex-1 flex-col items-center justify-center px-8 pb-16 text-center">
    {icon("file-x", "size-8 text-muted-foreground")}
    <h1 class="mt-4 text-title-3">This item isn't in the list anymore</h1>
    <p class="mt-1 max-w-xs text-body text-muted-foreground">Mert removed it from Wedding guests. Its decisions and notes were removed with it.</p>
    <a href="S28-results.html#S28-shared" class="mt-6 flex h-12 w-full max-w-xs items-center justify-center rounded-control bg-secondary text-label-lg text-secondary-foreground" data-action="back">Back to results</a>
  </div>'''
F.add('S26-not-found', 'Item removed by another member', phone(nf))

a07_rows = [frow('Address', 'Türkali, Ihlamur Yolu 4', editable=False), frow('Rent', '39,500 TRY', editable=False), frow('Rooms', '1+1', editable=False),
            frow('Size', '58 m²', editable=False), frow('Viewing', None, missing='viewing', editable=False), frow('Link', 'listings.example/ist/48288', link=True, editable=False)]
ro = f'''{back_bar('', 'S28-results.html#S28-default', 'Back to results')}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">
    <div class="mb-4 flex items-start gap-3 rounded-control border bg-card p-4" role="note">{icon("archive", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1"><p class="text-label">Apartment viewings is archived</p><p class="mt-0.5 text-body-sm text-muted-foreground">Restore the list to edit fields, change decisions or add notes.</p><a href="S10-list-management.html#S10-default" class="-ml-2 mt-1 inline-flex h-12 items-center rounded-control px-2 text-label text-primary">Restore list</a></div></div>
    <h1 class="text-title-1">Türkali, Ihlamur Yolu 4</h1>
    <p class="mt-0.5 text-body-lg text-muted-foreground">1+1, 58 m²</p>
    {my_decision('maybe', 'Final decision')}
    {fields_group(a07_rows, edit=False)}
    {source_line("From Google Sheets: Flat hunt 2026, tab Beşiktaş.")}
  </div>'''
F.add('S26-read-only', 'Read-only (archived list): missing value shown as a dash', phone(ro))

# ------------------------------------------------------------------ section: accessibility
F.section('Accessibility', 'At 200% text, label and value stack, everything wraps and the decision buttons become full-width rows.')
big_rows = ''.join(f'<li class="px-4 py-3"><a href="#S26-edit" class="block min-h-16"><span class="block text-title-3 font-normal text-muted-foreground">{l}</span><span class="block break-words text-title-2 font-normal">{v}</span></a></li>' for l, v in [('Phone', '+46 8 0000 4021'), ('Email', 'mia.andersson@example.com'), ('Side', "Bride's"), ('Relationship', 'Colleague'), ('City', 'Stockholm')])
big = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    {icon_btn("chevron-down", "Back to sorting", "#S26-default", "collapse", "", "size-7")}
    <span class="flex-1"></span>
    <a href="#S26-edit" class="inline-flex h-14 items-center gap-2 rounded-control px-3 text-title-3 text-primary" data-action="edit">{icon("pencil", "size-6")}Edit</a>
  </header>
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-4">
    <h1 class="text-display">Mia Andersson</h1>
    <p class="mt-1 text-title-2 font-normal text-muted-foreground">Colleague</p>
    <p class="mt-4 inline-flex min-h-10 items-center gap-2 rounded-full bg-muted px-3 text-title-3 font-normal text-muted-foreground">{icon("circle-dashed", "size-6")}Not decided yet</p>
    <ul class="mt-5 divide-y overflow-hidden rounded-group bg-card">{big_rows}</ul>
  </div>
  <div class="shrink-0 space-y-2 border-t px-gutter pb-4 pt-3" role="group" aria-label="Decide this item">
    <div class="grid grid-cols-3 gap-2">{''.join(f'<button type="button" class="flex min-h-16 flex-col items-center justify-center gap-1 rounded-control bg-{k}-soft text-title-3 text-{k}-soft-foreground" data-action="{k}">{icon(DEC[k][0], "size-6")}{DEC[k][1]}</button>' for k in ('reject', 'maybe', 'accept'))}</div>
  </div>'''
F.add('S26-large-text', 'Large text (200%), expanded', phone(big))

# ------------------------------------------------------------------ section: iOS and web
F.section('iOS and web', 'iOS: a page sheet with medium and large detents, Edit and Done in the navigation bar; while editing, Cancel and Save replace them. Web desktop: Enter opens details from S25 as the same sheet inside the centered column, with keyboard hints.')
ios_content = f'''{item_head('Mia Andersson', 'Colleague', 'people/c077.svg', 'MA')}
    {my_decision(None)}
    {fields_group(mia_fields(), edit=False)}
    {notes_section()}'''
ios_sheet = f'''<div class="absolute inset-x-0 bottom-0 top-20 z-20 flex flex-col overflow-hidden rounded-t-sheet bg-popover shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="ios1">
    <div class="flex shrink-0 justify-center pt-1.5"><span class="h-1 w-9 rounded-full bg-muted-foreground/40"></span></div>
    {ios_bar(ios_text_btn("Edit", href="#S26-ios-edit", action="edit"), '<span id="ios1">Details</span>', ios_text_btn("Done", True, "S25-sorting.html#S25-ios", "close"))}
    <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">{ios_content}</div>
    {decide_bar()}
  </div>'''
F.add('S26-ios', 'iOS page sheet: Edit and Done in the bar', phone(s25_background(ios=True) + scrim('bg-scrim/40') + ios_sheet, ios=True))
ios_edit_sheet = f'''<div class="absolute inset-x-0 bottom-0 top-3 z-20 flex flex-col overflow-hidden rounded-t-sheet bg-popover shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="ios2">
    <div class="flex shrink-0 justify-center pt-1.5"><span class="h-1 w-9 rounded-full bg-muted-foreground/40"></span></div>
    {ios_bar(ios_text_btn("Cancel", href="#S26-ios", action="cancel-edit"), '<span id="ios2">Edit fields</span>', ios_text_btn("Save", True, "#S26-ios", "save-edit"))}
    <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6">{edit_form(photo_edit('people/c077.svg', 'MA') + inp('i-name', 'Name', 'Mia Andersson') + inp('i-phone', 'Phone', '+46 8 0000 4021', 'tel') + inp('i-email', 'Email', 'mia.andersson@example.com', 'email', focus=True) + inp('i-city', 'City', 'Stockholm'))}</div>
  </div>'''
F.add('S26-ios-edit', 'iOS editing: Cancel and Save in the bar, sheet at the large detent', phone('<div class="flex-1 bg-scrim/40" aria-hidden="true"></div>' + ios_edit_sheet, ios=True))

web_sheet = sheet_detail(mia_content(), 'sw1', decide_bar() + hints([('Esc', 'Close'), ('E', 'Edit'), ('← ↑ →', 'Decide')]), top='top-16', close_href='S25-sorting.html#S25-web-desktop')
F.add('S26-web-desktop', 'Web, desktop: Enter on the card opens details; keyboard hints', desktop(over_sorting(web_sheet), 'swipesort.app/l/7Hq2xK/sort'))

F.write(OUT, 'S26 Item detail, editing and notes', 'All fields of one item, my decision, who decided what on shared lists, notes, and editing in place with revert. Spec: <a href="S26-item-detail.md">S26-item-detail.md</a>. Opened from <a href="S25-sorting.html">S25</a> (sheet), S28 and S36 (pushed).')
