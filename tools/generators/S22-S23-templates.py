# Usage: python3 tools/generators/S22-S23-templates.py
# Generates design/03-screens/S22-template-library.html and S23-template-editor.html (group D).
# Card bodies mirror tools/generators/S25-sorting.py exactly (same classes, same structure), so the preview
# is the real SwipeCard rendered at 50% (`origin-top scale-50`) on a card box with the Android sort-card
# proportions (372 x 620, `aspect-card`).
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from groupc2_common import *  # noqa
from groupc2_common import phone as _phone


def phone(content, ios=False):
    """Frames with a modal overlay: the scrim and sheets extend under the system bars (screen is static, bars on top)."""
    html = _phone(content, ios)
    if 'aria-modal="true"' in content and 'id="pf1"' not in content:
        html = (html.replace('<div class="screen">', '<div class="screen static">', 1)
                .replace('class="sysbar-top"', 'class="sysbar-top relative z-50"', 1)
                .replace('class="sysbar-nav"', 'class="sysbar-nav relative z-50"', 1))
    return html

# ------------------------------------------------------------------ data
CANDS = {c['id']: c for c in DATA['candidates']}
CLABEL = {f['key']: f['label'] for f in DATA['fields']['candidates']}
TPL = {t['id']: t['layout'] for t in DATA['templates']}
PROD = {p['id']: p for p in DATA['products']}
TRIPS = {t['id']: t for t in DATA['trips']}  # "Trip ideas" (D-32, A-130); the photos dataset is only for the retired S18
ACCOUNT = DATA['me']['signedIn']['email']


def cand(k):
    c = CANDS[k]
    return dict(name=c['name'], role=c['role'], yearsExperience=str(c['yearsExperience']), location=c['location'],
                expectedSalary=(f"€{c['expectedSalary']:,}" if c['expectedSalary'] else None),
                portfolio=(c['portfolio'].replace('https://', '') if c['portfolio'] else None),
                email=c['email'], source=c['source'])


def contact(cid):
    c = CONTACTS[cid]
    ph = c['phones'][0]['number'] if c['phones'] else None
    extra = len(c['phones']) - 1
    if ph and extra:
        ph = f'{ph} <span class="text-muted-foreground">+{extra}</span>'
    return dict(name=c['name'], phone=ph, email=c['email'], side=c['side'], relationship=c['relationship'], city=c['city'])


PLABEL = {'phone': 'Phone', 'email': 'Email', 'city': 'City', 'side': 'Side', 'relationship': 'Relationship', 'name': 'Name'}
HIDDEN_CSV = ('role',)  # auto-hidden in S19-csv (same value in all 12 rows)
COMPACT = TPL['t-candidate-compact']
CANDIDATE = TPL['t-candidate']
PERSON = TPL['t-person']
TABLE = TPL['t-wedding-table']
GENERIC_BOOK = dict(image='none', title='book', subtitle=None, rows=[], tags=[])
PRODUCT = TPL['t-product']
PHOTO = TPL['t-photo']  # title Place, subtitle Country, rows Best time and Budget (A-131)
TRIP_LABEL = {'bestTime': 'Best time', 'budget': 'Budget'}

TAG = '<span class="inline-flex h-7 items-center rounded-full bg-secondary px-2.5 text-caption text-secondary-foreground">{}</span>'


# ------------------------------------------------------------------ the card (same markup as S25)
def inline_row(label, value):
    return f'<div class="flex gap-3"><dt class="w-16 shrink-0 text-muted-foreground">{label}</dt><dd class="min-w-0 truncate tabular-nums">{value}</dd></div>'


def stacked_row(label, value, big=False):
    vcls = 'text-title-2' if big else 'text-title-3'
    return f'<div class="flex flex-col"><dt class="text-body-sm text-muted-foreground">{label}</dt><dd class="truncate {vcls} tabular-nums">{value}</dd></div>'


def card_body(layout, vals, labels, photo=None, hidden=(), kind=None, no_title=False):
    image = layout['image']
    t = None if no_title else vals.get(layout['title'])
    sk = layout.get('subtitle')
    sub = vals.get(sk) if sk and sk not in hidden else None
    rows = [(labels.get(k, k), vals[k]) for k in layout['rows'] if k not in hidden and vals.get(k)]
    tags = [vals[k] for k in layout['tags'] if k not in hidden and vals.get(k)]
    if image == 'full':
        # Photo (A-131, A-166): caption panel under the image, title + subtitle, then the rows as label/value pairs
        # (same markup as S25-photo and S40's Trip ideas card).
        sub_h = f'<p class="mt-0.5 text-body text-muted-foreground">{sub}</p>' if sub else ''
        rows_h = ''.join(f'<div class="flex gap-3"><dt class="w-24 shrink-0 text-muted-foreground">{l}</dt><dd class="min-w-0 truncate tabular-nums">{v}</dd></div>' for l, v in rows)
        dl_h = f'<dl class="mt-3 flex flex-col gap-1.5 text-body-sm">{rows_h}</dl>' if rows else ''
        return f'''<img src="{IMG}{photo}" alt="" class="min-h-0 w-full flex-1 object-cover">
      <div class="shrink-0 px-6 pb-5 pt-4">
        <h2 class="text-title-2">{t}</h2>{sub_h}{dl_h}
      </div>'''
    # Sparse rule (image area None): the title/subtitle/rows block is vertically centred above the tags;
    # templates with up to 3 rows use larger values (title-2, 20 apart); a title-only card uses text-display.
    sparse = image == 'none'
    big = sparse and len(layout['rows']) <= 3
    title_only = sparse and not sk and not layout['rows']
    if t:
        tcls = 'line-clamp-3 text-display' if title_only else ('line-clamp-4 text-title-1' if len(t) > 36 else 'line-clamp-3 text-card-title')
        title_h = f'<h2 class="{tcls}">{t}</h2>'
    else:  # validation preview only: the slot is outlined, never shown on a real card
        title_h = f'<div class="flex h-12 items-center gap-2 rounded-control border-2 border-dashed border-destructive px-3 text-body-lg text-destructive">{icon("circle-alert", "size-5 shrink-0")}No title</div>'
    sub_h = f'<p class="mt-1 text-body-lg text-muted-foreground">{sub}</p>' if sub else ''
    if kind == 'product':
        price = vals.get('price')
        rating = vals.get('rating')
        r_h = f'<span class="inline-flex items-center gap-1 text-body">{icon("star", "size-4")}{rating} <span class="text-muted-foreground">({vals.get("reviews")})</span></span>' if rating else ''
        body_rows = f'<div class="mt-4 flex items-baseline justify-between"><span class="text-title-1 tabular-nums">{price}</span>{r_h}</div>' if price else ''
    else:
        stacked = image == 'none' or any(len(l) > 8 for l, _ in rows)
        if not rows:
            body_rows = ''
        elif stacked:
            mt = 'mt-6' if image == 'none' else 'mt-4'
            sp = 'space-y-5' if big else 'space-y-3'
            body_rows = f'<dl class="{mt} {sp} text-body">{"".join(stacked_row(l, v, big) for l, v in rows)}</dl>'
        else:
            body_rows = f'<dl class="mt-4 space-y-2 text-body">{"".join(inline_row(l, v) for l, v in rows)}</dl>'
    tags_h = f'<div class="mt-auto flex flex-wrap gap-2 pt-3">{"".join(TAG.format(x) for x in tags)}</div>' if tags else ''
    if image == 'avatar' and not photo:
        ini = f'<div class="mb-5"><span class="flex size-24 items-center justify-center rounded-full bg-muted text-title-1 text-muted-foreground" aria-hidden="true">{initials(t or "")}</span></div>'
        tg = tags_h.replace('mt-auto ', '')
        return f'''<div class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-7">
        <div class="my-auto">{ini}{title_h}{sub_h}
        {body_rows}</div>
        {tg}
      </div>'''
    if image in ('avatar', 'cover'):
        if photo:
            top = f'<img src="{IMG}{photo}" alt="" class="h-[46%] w-full object-cover">'
        elif image == 'avatar':
            top = f'<div class="px-6 pt-7"><span class="flex size-24 items-center justify-center rounded-full bg-muted text-title-1 text-muted-foreground" aria-hidden="true">{initials(t or "")}</span></div>'
        else:
            top = f'<div class="flex h-[46%] w-full items-center justify-center bg-muted text-muted-foreground">{icon("image-off", "size-8")}</div>'
        pt = 'pt-5'
    else:
        tg = tags_h.replace('mt-auto ', '')
        return f'''<div class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-7">
        <div class="my-auto">{title_h}{sub_h}
        {body_rows}</div>
        {tg}
      </div>'''
    return f'''{top}
      <div class="flex min-h-0 flex-1 flex-col px-6 pb-5 {pt}">
        {title_h}{sub_h}
        {body_rows}
        {tags_h}
      </div>'''


def card_label(layout, vals, labels, hidden=()):
    t = vals.get(layout['title']) or 'No title'
    sk = layout.get('subtitle')
    parts = [t]
    if sk and sk not in hidden and vals.get(sk):
        parts[0] += f', {vals[sk]}'
    for k in layout['rows']:
        if k not in hidden and vals.get(k):
            v = vals[k].split(' <span')[0]
            parts.append(f'{labels[k]} {v}')
    for k in layout['tags']:
        if k not in hidden and vals.get(k):
            parts.append(f'Tag {vals[k]}')
    return '. '.join(parts) + '.'


def stage(body, label, h='h-80', prevnext=False, expand_href=None, extra_cls='', scale='scale-50'):
    """The live preview: the real SwipeCard (S25 markup) on the 372 x 620 card box, shown at 50%."""
    card = f'<div class="absolute inset-x-gutter top-0 flex aspect-card origin-top {scale} flex-col overflow-hidden rounded-hero bg-card shadow-hero" role="img" aria-label="Card preview: {label}">{body}</div>'
    pn = ''
    if prevnext:
        pn = (f'<button class="absolute left-4 top-1/2 flex size-12 -translate-y-1/2 items-center justify-center rounded-full border border-input bg-card" aria-label="Previous item" data-action="preview-previous">{icon("chevron-left")}</button>'
              f'<button class="absolute right-4 top-1/2 flex size-12 -translate-y-1/2 items-center justify-center rounded-full border border-input bg-card" aria-label="Next item" data-action="preview-next">{icon("chevron-right")}</button>')
    ex = ''
    if expand_href:
        ex = f'<a href="{expand_href}" class="absolute right-2 top-0 flex size-12 items-center justify-center rounded-full text-muted-foreground" aria-label="See card at full size" data-action="preview-full">{icon("maximize-2")}</a>'
    return f'<div class="relative {h} shrink-0 {extra_cls}">{card}{pn}{ex}</div>'


# ------------------------------------------------------------------ template tiles
def schematic(image, h='h-12'):
    bar = lambda w, o='40', mt='mt-1.5', hh='h-1.5': f'<span class="{mt} block {hh} {w} rounded-full bg-muted-foreground/{o}"></span>'
    if image == 'avatar':
        inner = f'<div class="flex items-center gap-2"><span class="size-5 shrink-0 rounded-full bg-muted-foreground/30"></span><span class="h-2 flex-1 rounded-full bg-muted-foreground/40"></span></div>{bar("w-2/3", "25", "mt-2")}{bar("w-1/2", "25")}'
    elif image == 'cover':
        inner = f'<span class="block h-5 rounded-xs bg-muted-foreground/25"></span>{bar("w-3/4", "40", "mt-1.5", "h-2")}{bar("w-1/3", "25")}'
    elif image == 'full':
        inner = f'<span class="block min-h-0 flex-1 rounded-xs bg-muted-foreground/25"></span>{bar("w-1/2", "40", "mt-1.5", "h-2")}'
    else:
        inner = f'{bar("w-3/4", "40", "", "h-2")}{bar("w-1/2", "25")}{bar("w-2/3", "25", "mt-2")}{bar("w-1/2", "25")}'
    return f'<div class="flex {h} flex-col overflow-hidden rounded-sm bg-muted p-2" aria-hidden="true">{inner}</div>'


def pick_tile(name, image, caption='', selected=False, href=None, large=False):
    border = 'border-2 border-primary' if selected else 'border'
    pad = 'p-2.5' if selected else 'p-3'
    chk = icon('circle-check', 'size-5 shrink-0 text-primary') if selected else ''
    cap = f'<span class="mt-auto block pt-0.5 text-caption text-muted-foreground">{caption}</span>' if caption else ''
    inner = f'{schematic(image)}<span class="mt-2 flex items-start justify-between gap-1"><span class="text-label">{name}</span>{chk}</span>{cap}'
    cls = f'flex w-32 shrink-0 flex-col rounded-tile {border} bg-card {pad} text-left'
    aria = f'role="radio" aria-checked="{"true" if selected else "false"}"'
    if href:
        return f'<a href="{href}" {aria} class="{cls}">{inner}</a>'
    return f'<button {aria} class="{cls}">{inner}</button>'


def carousel(tiles, label='Card template'):
    return f'<div class="flex gap-3 overflow-hidden px-gutter" role="radiogroup" aria-label="{label}">{"".join(tiles)}</div>'


ALL = [('Person', 'avatar'), ('Product', 'cover'), ('Photo', 'full'), ('Task', 'none'), ('Candidate', 'avatar'), ('Generic', 'none')]
CUSTOM = [('Guest with table side', 'avatar'), ('Candidate, compact', 'none')]


def tiles_for(recommended, selected=None, caption_sel='Recommended', current=None, first_custom=None, sel_href=None):
    """Order: recommended (or current) first, then your templates, then the other built-ins."""
    selected = selected or recommended
    out = []
    order = [recommended]
    customs = [c for c, _ in CUSTOM]
    if first_custom and first_custom in customs:
        customs.remove(first_custom)
        customs.insert(0, first_custom)
    order += customs + [n for n, _ in ALL if n != recommended]
    imgs = dict(ALL + CUSTOM)
    for n in order:
        cap = ''
        if n == recommended:
            cap = caption_sel
        elif n in dict(CUSTOM):
            cap = 'Custom'
        else:
            cap = 'Built-in'
        out.append(pick_tile(n, imgs[n], cap, n == selected, href=sel_href.get(n) if sel_href else None))
    return out


# ------------------------------------------------------------------ small building blocks
def sec_head(text, right=''):
    r = f'<span class="text-caption tabular-nums text-muted-foreground">{right}</span>' if right else ''
    return f'<div class="flex items-baseline justify-between gap-3 px-1 pb-2"><h3 class="text-label text-muted-foreground">{text}</h3>{r}</div>'


GROUP = 'divide-y overflow-hidden rounded-group bg-card dark:border'


def back_bar(title, href, label, caption='', trailing='', action='back'):
    cap = f'<p class="truncate text-caption text-muted-foreground">{caption}</p>' if caption else ''
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    <a href="{href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{label}" data-action="{action}">{icon("arrow-left", "size-6")}</a>
    <div class="min-w-0 flex-1 px-1"><h1 class="truncate text-title-3">{title}</h1>{cap}</div>
    {trailing}
  </header>'''


def ios_bar(title, back_text, back_href, right='', caption=''):
    cap = f'<p class="truncate text-caption text-muted-foreground">{caption}</p>' if caption else ''
    return f'''<header class="grid h-11 shrink-0 grid-cols-[1fr_auto_1fr] items-center px-2">
    <a href="{back_href}" class="inline-flex h-12 items-center gap-0.5 justify-self-start pr-2 text-body text-primary" aria-label="Back to {back_text}">{icon("chevron-left", "size-6")}{back_text}</a>
    <div class="min-w-0 text-center"><h1 class="truncate text-body font-semibold">{title}</h1>{cap}</div>
    <div class="flex justify-end">{right}</div>
  </header>'''


def overflow_btn(label='More options', href=None, action='menu'):
    if href:
        return f'<a href="{href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{label}" data-action="{action}">{icon("ellipsis-vertical", "size-6")}</a>'
    return f'<button class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="{label}" data-action="{action}">{icon("ellipsis-vertical", "size-6")}</button>'


def dlg(did, title, body, actions, role='alertdialog', top=None):
    """S40 dialog: vertically centred, max width 384, no icon (A-112)."""
    return f'''{scrim()}
  <div class="absolute inset-0 z-20 flex items-center justify-center px-6">
    <div class="w-full max-w-sm rounded-dialog bg-popover p-6 shadow-dialog" role="{role}" aria-modal="true" aria-labelledby="{did}">
      <h2 id="{did}" class="text-title-3">{title}</h2>
      {body}
      <div class="mt-6 flex flex-wrap justify-end gap-2">{actions}</div>
    </div>
  </div>'''


def dbtn(label, variant='ghost', href=None, action=None, disabled=False):
    return btn(label, variant, href=href, action=action, disabled=disabled)


def menu(items, top='top-14'):
    out = ''
    for it in items:
        if it == '-':
            out += '<div class="my-1.5 h-px bg-border"></div>'
            continue
        ic, text, href, destr = it
        cls = 'text-destructive' if destr else ''
        icls = 'size-5' if destr else 'size-5 text-muted-foreground'
        tag_open = f'<a href="{href}"' if href else '<button'
        tag_close = '</a>' if href else '</button>'
        out += f'{tag_open} role="menuitem" class="flex h-12 w-full items-center gap-3 px-4 text-body {cls}">{icon(ic, icls)}{text}{tag_close}'
    return f'<div class="absolute right-2 {top} z-20 w-64 overflow-hidden rounded-control bg-popover py-1.5 shadow-overlay" role="menu" aria-label="Template options">{out}</div>'


SNACK_BAND = '<div class="h-16 shrink-0" aria-hidden="true"></div>'  # content ends above the snackbar band


def bg(content, overlay):
    """Background under a modal overlay is inert (as in the app: focus and touch stay in the sheet or dialog)."""
    if 'aria-modal="true"' in overlay:
        return f'<div class="contents" inert>{content}</div>'
    return content


def p_muted(text, extra=''):
    return f'<p class="text-body-sm text-muted-foreground {extra}">{text}</p>'


# ================================================================== S22
P = Page('S22', 'Template library', 'One screen, three modes: <b>manage</b> (Settings › Card templates), <b>pick</b> (the last import step: name the list, choose a card template, start sorting) and <b>change</b> (a list\'s Card template, applied immediately). Previews render the real SwipeCard from S25 with the list\'s own items. Spec: <a href="S22-template-library.md">S22-template-library.md</a>. Editor: <a href="S23-template-editor.html">S23-template-editor.html</a>.')

DESC = {
    'Person': 'Photo, name and contact details',
    'Product': 'Image, price and rating',
    'Photo': 'The image fills the card',
    'Task': 'Title, due date and owner',
    'Candidate': 'Role, experience and salary',
    'Generic': 'The first fields of any list',
}


def lib_tile(name, image, href=None, large=False):
    inner = f'{schematic(image)}<span class="mt-2 block text-label-lg">{name}</span><span class="block text-caption text-muted-foreground">{DESC[name]}</span>'
    cls = 'flex flex-col rounded-tile border bg-card p-3 text-left'
    if href:
        return f'<a href="{href}" class="{cls}" aria-label="{name}, built-in. {DESC[name]}">{inner}</a>'
    return f'<button class="{cls}" aria-label="{name}, built-in. {DESC[name]}">{inner}</button>'


def custom_row(name, image, meta, href='#', more_href='#S22-actions', more_action='template-options'):
    return f'''<li class="flex items-center gap-1 pr-1">
      <a href="{href}" class="flex min-h-touch min-w-0 flex-1 items-center gap-4 py-3 pl-4">
        <span class="w-14 shrink-0">{schematic(image, 'h-12')}</span>
        <span class="min-w-0 flex-1"><span class="block text-body">{name}</span><span class="block text-body-sm text-muted-foreground">{meta}</span></span>
      </a>
      <a href="{more_href}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="More options for {name}" data-action="{more_action}">{icon("ellipsis-vertical")}</a>
    </li>'''


CUSTOM_ROWS = [
    ('Candidate, compact', 'none', 'Used by Frontend hiring, Q4', 'S23-template-editor.html#S23-edit-saved'),
    ('Guest with table side', 'avatar', 'Used by Wedding guests', 'S23-template-editor.html#S23-edit-saved'),
]


def manage(custom_rows=CUSTOM_ROWS, empty=False, overlay='', bar=None, extra_rows='', scroll='', band=False):
    tiles = ''.join(lib_tile(n, im, 'S23-template-editor.html#S23-built-in' if n == 'Candidate' else None) for n, im in ALL)
    if empty:
        yours = f'''<div class="flex flex-col items-center rounded-group bg-card px-6 py-6 text-center dark:border">
        {icon("layout-template", "size-8 text-muted-foreground")}
        <p class="mt-3 text-title-3">No templates of your own yet</p>
        <p class="mt-1 max-w-xs text-body text-muted-foreground">Duplicate a built-in template or start a new one to choose your own fields.</p>
        {btn("New template", "outline", "plus", href="#S22-new", extra="mt-4", action="new-template")}
      </div>'''
    else:
        rows = ''.join(custom_row(*r) for r in custom_rows) + extra_rows
        yours = f'''<ul class="{GROUP}">{rows}</ul>
      {btn("New template", "outline", "plus", href="#S22-new", extra="mt-3 w-full", action="new-template")}'''
    content = f'''{bar or back_bar("Card templates", "S06-settings.html#S06-default", "Back to Settings")}
  <div class="min-h-0 flex-1 overflow-y-auto px-gutter pb-6">
    <p class="px-1 text-body-sm text-muted-foreground {scroll}">Templates decide which fields show on a list's cards. Any list can switch templates at any time.</p>
    <div class="mt-5">{sec_head("Built-in")}<div class="grid grid-cols-2 gap-3">{tiles}</div></div>
    <div class="mt-6">{sec_head("Your templates")}{yours}</div>
  </div>{SNACK_BAND if band else ''}'''
    return f'''{bg(content, overlay)}
  {overlay}'''


# ----- sheet with the template's actions
def actions_sheet(name, meta, items, sid, note=''):
    rows = ''
    for ic, text, href, destr, action in items:
        cls = 'text-destructive' if destr else ''
        icls = 'size-5 shrink-0' if destr else 'size-5 shrink-0 text-muted-foreground'
        rows += f'<li><a href="{href}" class="flex min-h-14 items-center gap-4 px-1 text-body {cls}" data-action="{action}">{icon(ic, icls)}{text}</a></li>'
    n = f'<p class="mt-3 text-body-sm text-muted-foreground">{note}</p>' if note else ''
    body = f'<ul class="mt-2">{rows}</ul>{n}'
    return sheet(sid, name, body, subtitle=meta)


P.section('Manage mode', 'From Settings › Card templates. Built-in templates on top as tiles with a layout schematic; your templates below with the lists that use them. Tapping a template opens it in the editor (S23); built-ins open read-only and can be duplicated.')
P.frame('S22-default', 'Default: manage mode (Settings › Card templates)', phone(manage()))
P.frame('S22-actions', 'Template actions sheet (custom template)', phone(manage(overlay=actions_sheet(
    'Candidate, compact', 'Used by Frontend hiring, Q4',
    [('pencil', 'Edit', 'S23-template-editor.html#S23-edit-saved', False, 'edit-template'),
     ('text-cursor-input', 'Rename', '#S22-rename', False, 'rename-template'),
     ('copy', 'Duplicate', '#S22-duplicated', False, 'duplicate-template'),
     ('trash-2', 'Delete template', '#S22-delete', True, 'delete-template')], 'sa1'))))
P.frame('S22-actions-built-in', 'Long-press on a built-in: duplicate only', phone(manage(overlay=actions_sheet(
    'Person', 'Built-in template',
    [('eye', 'View layout', 'S23-template-editor.html#S23-built-in', False, 'view-template'),
     ('copy', 'Duplicate', '#S22-duplicated', False, 'duplicate-template')], 'sa2',
    note='Built-in templates can\'t be changed or deleted. Duplicate one to make your own version.'))))

rename_body = f'''<div class="mt-4">{label_input("rn1", "Template name", value="Candidate, compact", focused=True)}</div>'''
P.frame('S22-rename', 'Rename dialog', phone(manage(overlay=dlg('rd1', 'Rename template', rename_body,
    dbtn('Cancel', href='#S22-default') + btn('Rename', 'primary', href='#S22-renamed', action='confirm-rename'), role='dialog'))))
renamed_rows = [('Candidate, short', 'none', 'Used by Frontend hiring, Q4', 'S23-template-editor.html#S23-edit-saved'), CUSTOM_ROWS[1]]
P.frame('S22-renamed', 'Renamed: snackbar confirms', phone(manage(custom_rows=renamed_rows, scroll='-mt-24', band=True, overlay=snackbar('Template renamed', bottom='bottom-3'))))
rename_err = f'''<div class="mt-4">{label_input("rn2", "Template name", value="Guest with table side", error="You already have a template with this name. Choose another name.")}</div>'''
P.frame('S22-rename-error', 'Rename: name already used', phone(manage(overlay=dlg('rd2', 'Rename template', rename_err,
    dbtn('Cancel', href='#S22-default') + btn('Rename', 'primary'), role='dialog'))))
dup_row = custom_row('Candidate, compact (copy)', 'none', 'Not used by any list', 'S23-template-editor.html#S23-duplicated')
P.frame('S22-duplicated', 'Duplicated: the copy appears first in Your templates (newest first)', phone(manage(
    custom_rows=[], extra_rows=dup_row + ''.join(custom_row(*r) for r in CUSTOM_ROWS), scroll='-mt-40', band=True,
    overlay=snackbar('Duplicated as “Candidate, compact (copy)”', 'Edit', bottom='bottom-3', action_href='S23-template-editor.html#S23-duplicated'))))

del_body = f'''<p id="dd1-d" class="mt-2 text-body text-muted-foreground">Wedding guests uses this template. Its cards switch to the template you choose, for every member of the list.</p>
    <div class="mt-4"><p class="text-label" id="dd1-l">Card template for Wedding guests</p><div class="mt-1.5">{select_trigger("Person", "Card template for Wedding guests: Person")}</div><p class="mt-1.5 text-caption text-muted-foreground">Person is the template it was based on.</p></div>'''
P.frame('S22-delete', 'Delete a template in use: choose a replacement', phone(manage(overlay=dlg('dd1', 'Delete “Guest with table side”?', del_body,
    dbtn('Cancel', href='#S22-default') + btn('Delete template', 'destructive', href='#S22-deleted', action='confirm-delete'), top='top-1/4'))))
P.frame('S22-deleted', 'Deleted: Undo restores the template and the list\'s choice', phone(manage(
    custom_rows=[CUSTOM_ROWS[0]], scroll='-mt-12', band=True, overlay=snackbar('Template deleted', 'Undo', bottom='bottom-3'))))

new_body = f'''<div class="mt-4 space-y-5">
      <div><p class="text-label">Use fields from</p><div class="mt-1.5">{select_trigger("Frontend hiring, Q4", "Use fields from: Frontend hiring, Q4", ic="list-checks")}</div><p class="mt-1.5 text-caption text-muted-foreground">The preview shows this list's items. You can use the template on any list.</p></div>
      <div><p class="text-label" id="nt-start">Start from</p>
        <div class="mt-1 grid grid-cols-2 gap-x-3" role="radiogroup" aria-labelledby="nt-start">
          {"".join(f'<button role="radio" aria-checked="{"true" if n == "Candidate" else "false"}" class="flex min-h-12 items-center gap-3 text-left text-body">{radio_dot(n == "Candidate")}{n}</button>' for n, _ in ALL)}
        </div></div>
    </div>'''
P.frame('S22-new', 'New template sheet: fields from a list, start from a built-in', phone(manage(overlay=sheet('ns1', 'New template', new_body,
    actions=f'<a href="S23-template-editor.html#S23-start" class="{PRIMARY}" data-action="continue">Continue</a>'))))

P.section('Manage mode: other states', 'No templates of your own yet, and loading.')
P.frame('S22-empty', 'Empty: no templates of your own yet', phone(manage(empty=True)))
sk_tile = '<div class="rounded-tile border bg-card p-3"><span class="block h-12 animate-pulse rounded-sm bg-muted"></span><span class="mt-3 block h-4 w-2/3 animate-pulse rounded-full bg-muted"></span><span class="mt-2 block h-3 w-full animate-pulse rounded-full bg-muted"></span></div>'
loading = f'''{back_bar("Card templates", "S06-settings.html#S06-default", "Back to Settings")}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter" role="status" aria-busy="true" aria-label="Loading templates">
    <span class="block h-4 w-5/6 animate-pulse rounded-full bg-muted"></span>
    <div class="mt-8 grid grid-cols-2 gap-3" aria-hidden="true">{sk_tile * 6}</div>
    <div class="mt-8 space-y-px overflow-hidden rounded-group" aria-hidden="true"><div class="h-16 animate-pulse bg-card"></div><div class="h-16 animate-pulse bg-card"></div></div>
  </div>'''
P.frame('S22-loading', 'Loading (synced templates after sign-in)', phone(loading))

# ------------------------------------------------------------------ pick mode
SUM_CONTACTS = '85 items from Contacts. 3 duplicate pairs merged, 1 pair kept as separate items.'
C001 = contact('c001')
AYSE = card_body(PERSON, C001, PLABEL, photo='people/c001.svg')
AYSE_L = card_label(PERSON, C001, PLABEL)
LENA = cand('k01')
LENA_CAND = card_body(CANDIDATE, LENA, CLABEL, hidden=HIDDEN_CSV)
LENA_CAND_L = card_label(CANDIDATE, LENA, CLABEL, HIDDEN_CSV)
LENA_COMPACT = card_body(COMPACT, LENA, CLABEL)
LENA_COMPACT_L = card_label(COMPACT, LENA, CLABEL)


BACKUP_DESC = {
    'on': ('cloud-check', f'Backed up to {ACCOUNT}'),
    'off': ('cloud-off', 'It stays on this phone only. You can back it up later.'),
    'web-on': ('cloud-check', f'Backed up to {ACCOUNT}'),
    'web-off': ('cloud-off', "It stays in this browser only. Browsers can clear lists you haven't opened for a while."),
}


def backup_row(state, href=None):
    """Import finish, signed in only (D-33, A-132, A-168): BackupSwitchRow, on by default. Same row as S09's Backup group."""
    ic, desc = BACKUP_DESC[state]
    on = state in ('on', 'web-on')
    return (f'<!-- Proposed component: BackupSwitchRow (same as S09) --><div class="mt-3 flex min-h-16 items-center gap-4 rounded-group bg-card px-4 py-3 dark:border">'
            f'{icon(ic, "size-5 shrink-0 text-muted-foreground")}'
            f'<span class="min-w-0 flex-1"><span class="block text-body">Back up this list</span><span class="block break-words text-body-sm text-muted-foreground" aria-live="polite">{desc}</span></span>'
            f'{_backup_switch(on, href)}</div>')


def _backup_switch(on, href=None):
    """The Switch; in the prototype it is a link to the other state's frame (flow 4: csv <-> device-only)."""
    sw = switch(on, "Back up this list").replace('<button role="switch"', '<button role="switch" data-action="toggle-backup"', 1)
    if href:
        sw = sw.replace('<button role="switch"', f'<a href="{href}" role="switch"', 1).replace('</button>', '</a>').replace(' disabled', '')
    return sw


def pick(fid, name, summary, body, label, tiles, step=(5, 5), title='Import', customize='S23-template-editor.html#S23-default',
         start='S25-sorting.html#S25-coach-1', start_label='Start sorting', name_kw=None, overlay='', bottom_html=None,
         sum_icon='list-checks', ios=False, back=None, start_action='start-sorting', scroll='', stage_h='h-72', stage_scale='scale-[.46]',
         backup=None, backup_href=None):
    kw = dict(value=name)
    kw.update(name_kw or {})
    if backup and stage_h == 'h-72':  # the switch row takes ~88 dp: a smaller preview keeps the template row in view
        stage_h, stage_scale = 'h-56', 'scale-[.36]'
    bar = modal_bar(title, close_label='Close import', ios=ios, back=back)
    return bg(f'''{bar}
  {stepper("Finish", *step)}
  <div class="min-h-0 flex-1 overflow-y-auto">
    <div class="px-gutter pt-1 {scroll}">
      {label_input(fid + "-name", "List name", **kw)}
      <p class="mt-3 flex items-start gap-2 text-body-sm text-muted-foreground">{icon(sum_icon, "size-4 mt-0.5 shrink-0")}<span>{summary}</span></p>
      {backup_row(backup, backup_href) if backup else ''}
    </div>
    <div class="mt-4 flex items-center justify-between gap-2 pl-gutter pr-2"><h2 class="text-title-3">Card template</h2><a href="{customize}" class="inline-flex h-12 items-center gap-2 rounded-control px-3 text-label-lg text-primary" data-action="customize-template">{icon("pencil")}Customize</a></div>
    {stage(body, label, h=stage_h, scale=stage_scale)}
    <div class="mt-3">{carousel(tiles)}</div>
  </div>
  {bottom_html if bottom_html is not None else bottom(start_label, start, start_action)}''', overlay) + overlay


P.section('Pick mode: the import finish step', 'The last import step (A-22): name the list, choose a card template and start sorting. The recommended template is preselected from the source and its fields; the preview is the first imported item on the real card. "Customize" opens the editor on a copy. When the duplicate step was skipped, the summary says "No duplicates found" (A-23). Signed in, a "Back up this list" switch (on by default) sits under the summary, so a private list never has to reach the server (D-33, A-132); without an account it is not shown (flow 1).')
P.frame('S22-import-pick', 'Pick mode: contacts, Person recommended (Step 5 of 5)', phone(pick(
    'ip1', 'Wedding guests', SUM_CONTACTS, AYSE, AYSE_L, tiles_for('Person'))))
P.frame('S22-import-pick-prefilled', 'Arriving: name prefilled from the source and selected', phone(pick(
    'ip2', 'Contacts', SUM_CONTACTS, AYSE, AYSE_L, tiles_for('Person'),
    name_kw=dict(focused=True, helper='Prefilled from the source. Type to rename it.'))))
SUM_CSV = '12 items from candidates-q4.csv. No duplicates found.'
P.frame('S22-import-pick-csv', 'Pick mode: CSV, signed in: Candidate recommended, "Back up this list" on (default)', phone(pick(
    'ip3', 'Frontend hiring, Q4', SUM_CSV, LENA_CAND, LENA_CAND_L,
    tiles_for('Candidate'), sum_icon='copy-check', start='S25-sorting.html#S25-candidate', backup='on', backup_href='#S22-import-pick-device-only')))
P.frame('S22-import-pick-device-only', 'Signed in: "Back up this list" turned off, the list stays on this phone only', phone(pick(
    'ip12', 'Frontend hiring, Q4', SUM_CSV, LENA_CAND, LENA_CAND_L,
    tiles_for('Candidate'), sum_icon='copy-check', start='S25-sorting.html#S25-candidate', backup='off', backup_href='#S22-import-pick-csv')))
P.frame('S22-import-pick-custom', 'Pick mode: back from Save, scrolled to the just-saved template (flow 4)', phone(pick(
    'ip4', 'Frontend hiring, Q4', SUM_CSV, LENA_COMPACT, LENA_COMPACT_L,
    tiles_for('Candidate', selected='Candidate, compact', first_custom='Candidate, compact'), sum_icon='copy-check',
    start='S25-sorting.html#S25-candidate', customize='S23-template-editor.html#S23-edit-saved', scroll='-mt-24', backup='off',
    overlay=snackbar('Template saved', bottom='bottom-28'))))

BOOK = dict(book='The Remains of the Day')
BOOK_BODY = card_body(GENERIC_BOOK, BOOK, {})
P.frame('S22-import-pick-text', 'Plain text: Step 4 of 4, Generic recommended (one field)', phone(pick(
    'ip5', 'Book club picks', '12 items from pasted text.', BOOK_BODY, 'The Remains of the Day.',
    tiles_for('Generic'), step=(4, 4), sum_icon='file-text', start='S25-sorting.html#S25-default')))
P01 = PROD['p01']
P01V = dict(name=P01['name'], store=P01['store'], price=f"€{P01['price']}")
P01_BODY = card_body(PRODUCT, P01V, {}, photo='products/p01.svg', kind='product')
P.frame('S22-import-pick-manual', 'Manual entry: Step 4 of 4, Product recommended', phone(pick(
    'ip6', 'Desk setup', '3 items you added.', P01_BODY, 'Ergo Mesh task chair, Nordhaus. Price €389.',
    tiles_for('Product'), step=(4, 4), title='New list', sum_icon='list-checks', start='S25-sorting.html#S25-product')))
TR01 = TRIPS['tr01']
TR01V = dict(place=TR01['place'], country=TR01['country'], bestTime=TR01['bestTime'], budget=f"€{TR01['budget']:,}")
TR_BODY = card_body(PHOTO, TR01V, TRIP_LABEL, photo=TR01['photo'].replace('images/', ''))
TR_L = card_label(PHOTO, TR01V, TRIP_LABEL)
SUM_TRIPS = '30 items from trip-ideas.csv. No duplicates found.'
P.frame('S22-import-pick-trips', 'CSV with an image link per row (Trip ideas): Photo recommended', phone(pick(
    'ip7', 'Trip ideas', SUM_TRIPS, TR_BODY, TR_L,
    tiles_for('Photo'), sum_icon='copy-check', start='S25-sorting.html#S25-photo', backup='on')))

P.section('Pick mode: states', 'Name validation, importing, image links that did not download. Data was already read in the earlier steps, so this step works offline; images from links download when a connection returns.')
P.frame('S22-import-pick-error', 'List name cleared: error on Start sorting', phone(pick(
    'ip8', '', SUM_CONTACTS, AYSE, AYSE_L, tiles_for('Person'),
    name_kw=dict(error='Enter a name for the list.', placeholder='e.g. Desk setup'))))
P.frame('S22-import-pick-importing', 'Start sorting pressed: importing', phone(pick(
    'ip9', 'Wedding guests', SUM_CONTACTS, AYSE, AYSE_L, tiles_for('Person'),
    bottom_html=bottom('Importing 85 items…', busy=True))))
partial = f'''<div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">
    {alert("neutral", "2 images couldn\'t be downloaded", "The image links in rows 14 and 27 don\'t open an image. Those 2 cards show without one. You can change a link in item details.", ic="image-off", role="status")}
    <a href="S25-sorting.html#S25-photo" class="{PRIMARY} mt-3" data-action="start-sorting">Start sorting</a>
  </div>'''
P.frame('S22-import-pick-partial', 'Images partly downloaded: 2 image links didn\'t open, all 30 items are in the list', phone(pick(
    'ip10', 'Trip ideas', '30 items from trip-ideas.csv. 28 of 30 images downloaded.', TR_BODY, TR_L,
    tiles_for('Photo'), sum_icon='copy-check', bottom_html=partial, scroll='-mt-20', backup='on')))

# ------------------------------------------------------------------ change mode
P03 = PROD['p03']
P03V = dict(name=P03['name'], store=P03['store'], price=f"€{P03['price']}", rating=P03['rating'], reviews=f"{P03['reviews']:,}")
P03_BODY = card_body(PRODUCT, P03V, {}, photo='products/p03.svg', kind='product')


def product_with_tag(body, tag):
    return body.replace('        \n      </div>', f'        <div class="mt-auto flex flex-wrap gap-2 pt-3">{TAG.format(tag)}</div>\n      </div>')


P03_BODY = product_with_tag(P03_BODY, P03['category'])
AYSE_TABLE = card_body(TABLE, C001, PLABEL, photo='people/c001.svg')
AYSE_TABLE_L = card_label(TABLE, C001, PLABEL)


def change(list_name, back, body, label, tiles, notice='', overlay='', edit_label='Customize', edit_href='S23-template-editor.html#S23-start', ios=False, bar=None):
    nb = f'<div class="px-gutter pb-3">{notice}</div>' if notice else ''
    b = bar or back_bar('Card template', back, f'Back to {list_name}', caption=list_name)
    return f'''{b}
  <div class="min-h-0 flex-1 overflow-y-auto pt-1">
    {nb}
    {stage(body, label)}
    <div class="mt-4 flex items-center justify-between gap-2 pl-gutter pr-2"><h2 class="text-label text-muted-foreground">Templates</h2><a href="{edit_href}" class="inline-flex h-12 items-center gap-2 rounded-control px-3 text-label-lg text-primary" data-action="customize-template">{icon("pencil")}{edit_label}</a></div>
    <div class="mt-1">{carousel(tiles, "Card template for " + list_name)}</div>
    <p class="mt-4 px-gutter text-body-sm text-muted-foreground">Choosing a template changes the cards right away. Decisions, notes and fields stay as they are.</p>
  </div>
  {overlay}'''


shared_notice = alert('info', 'Shared list', 'A new template changes the cards for all 3 members.', ic='users')
P.section('Change mode: a list\'s card template', 'From S09 › Card template or the S25 menu. The current template is marked; choosing another applies immediately with Undo (TPL-13). On a shared list the change applies to every member, and the screen says so.')
P.frame('S22-change', 'Change mode, solo list (Desk setup): current template marked', phone(change(
    'Desk setup', 'S09-list-overview.html#S09-default', P03_BODY, '27-inch 4K USB-C monitor, Pixelhaus. Price €429. Rating 4.5. Tag Monitor.',
    tiles_for('Product', caption_sel='Current'))))
P.frame('S22-change-shared', 'Change mode, shared list (Wedding guests): applies to everyone', phone(change(
    'Wedding guests', 'S09-list-overview.html#S09-shared', AYSE, AYSE_L, tiles_for('Person', caption_sel='Current'), notice=shared_notice)))
cur_tiles = tiles_for('Person', selected='Guest with table side', caption_sel='')
cur_tiles[1] = cur_tiles[1].replace('>Custom</span>', '>Current</span>')
cur_tiles[0] = cur_tiles[0].replace('<span class="text-label">Person</span></span>', '<span class="text-label">Person</span></span><span class="mt-auto block pt-0.5 text-caption text-muted-foreground">Built-in</span>')
P.frame('S22-change-applied', 'Applied immediately: snackbar with Undo', phone(change(
    'Wedding guests', 'S09-list-overview.html#S09-shared', AYSE_TABLE, AYSE_TABLE_L, cur_tiles, notice=shared_notice,
    edit_label='Edit template', edit_href='S23-template-editor.html#S23-edit-saved',
    overlay=snackbar('Card template changed to Guest with table side', 'Undo', bottom='bottom-3'))))
off_bar = back_bar('Card template', 'S09-list-overview.html#S09-shared', 'Back to Wedding guests', caption='Wedding guests')
offline_notice = alert('info', 'Shared list', 'The new template applies on this phone now. All 3 members see it once it\'s synced.', ic='users')
P.frame('S22-change-offline', 'Offline on a shared list: queued, not blocked (D-05). Applied on this phone, members see it after sync', phone(change(
    'Wedding guests', 'S09-list-overview.html#S09-shared', AYSE_TABLE, AYSE_TABLE_L, cur_tiles, notice=offline_notice,
    bar=off_bar + offline_banner("You're offline. Changes are saved on this phone.") + '<div class="h-3 shrink-0"></div>',
    edit_label='Edit template', edit_href='S23-template-editor.html#S23-edit-saved',
    overlay=snackbar('Card template changed. Saved on this phone until it syncs.', 'Undo', bottom='bottom-3'))))

# ------------------------------------------------------------------ iOS, web, large text
P.section('iOS, web and large text', 'iOS: back chevron with the previous title, page sheets and an action sheet for template actions. Web: same layout as Android; on desktop the actions open as a menu next to the row. Large text: the preview becomes a button that opens it at full size and the carousel becomes a list.')
ios_manage_bar = ios_bar('Card templates', 'Settings', 'S06-settings.html#S06-default')
P.frame('S22-ios', 'iOS: manage mode', phone(manage(bar=ios_manage_bar), ios=True))
ios_as = f'''{scrim(op='bg-scrim/40')}
  <div class="absolute inset-x-2 bottom-9 z-20 space-y-2" role="dialog" aria-modal="true" aria-labelledby="ias">
    <div class="divide-y overflow-hidden rounded-tile bg-popover">
      <div class="px-4 py-3 text-center"><p id="ias" class="text-label text-muted-foreground">Candidate, compact</p><p class="text-caption text-muted-foreground">Used by Frontend hiring, Q4</p></div>
      <a href="S23-template-editor.html#S23-edit-saved" class="flex h-14 items-center justify-center text-title-3 font-normal text-primary">Edit</a>
      <a href="#S22-rename" class="flex h-14 items-center justify-center text-title-3 font-normal text-primary">Rename</a>
      <a href="#S22-duplicated" class="flex h-14 items-center justify-center text-title-3 font-normal text-primary">Duplicate</a>
      <a href="#S22-delete" class="flex h-14 items-center justify-center text-title-3 font-normal text-destructive">Delete template</a>
    </div>
    <button class="flex h-14 w-full items-center justify-center rounded-tile bg-popover text-title-3 text-primary">Cancel</button>
  </div>'''
P.frame('S22-ios-actions', 'iOS: template actions as an action sheet', phone(manage(bar=ios_manage_bar, overlay=ios_as), ios=True))
P.frame('S22-import-pick-ios', 'iOS: import finish step', phone(pick(
    'ip11', 'Wedding guests', SUM_CONTACTS, AYSE, AYSE_L, tiles_for('Person'),
    ios=True, back=('Review duplicates', 'S20-duplicate-review.html#S20-default'), stage_h='h-56', stage_scale='scale-[.36]'), ios=True))
web_menu = menu([('pencil', 'Edit', 'S23-template-editor.html#S23-edit-saved', False), ('text-cursor-input', 'Rename', '#S22-rename', False),
                 ('copy', 'Duplicate', '#S22-duplicated', False), '-', ('trash-2', 'Delete template', '#S22-delete', True)], top='bottom-32')
web_manage = manage(overlay=web_menu).replace('aria-label="More options for Candidate, compact" data-action="template-options"', 'aria-label="More options for Candidate, compact" aria-expanded="true" data-action="template-options"')
P.frame('S22-web-desktop', 'Web, desktop browser: actions open as a menu', desktop(web_manage, 'swipesort.app/settings/templates'))
P.frame('S22-import-pick-web-device-only', 'Web, signed in: backup off keeps the list in this browser only (D-08 line)', web_phone(pick(
    'ip13', 'Frontend hiring, Q4', SUM_CSV, LENA_CAND, LENA_CAND_L,
    tiles_for('Candidate'), sum_icon='copy-check', start='S25-sorting.html#S25-candidate', backup='web-off')))


def big_backup(state):
    ic, desc = BACKUP_DESC[state]
    sw = switch(state in ('on', 'web-on'), 'Back up this list').replace('h-8 w-13', 'h-10 w-16').replace('size-6 rounded-full bg-primary-foreground', 'size-8 rounded-full bg-primary-foreground').replace('size-5 rounded-full bg-muted-foreground', 'size-7 rounded-full bg-muted-foreground')
    return (f'<div class="mt-4 rounded-group bg-card px-4 py-3 dark:border"><div class="flex items-center gap-4">{icon(ic, "size-6 shrink-0 text-muted-foreground")}'
            f'<span class="min-w-0 flex-1 text-title-3 font-normal">Back up this list</span>{sw}</div>'
            f'<p class="mt-1 break-words text-body-lg text-muted-foreground" aria-live="polite">{desc}</p></div>')


def big_pick(name='Wedding guests', summary='85 items from Contacts. 3 duplicate pairs merged, 1 pair kept as separate items.', rec='Person',
             opts=None, backup=None, start='S25-sorting.html#S25-coach-1'):
    radios = ''
    opts = opts or [('Person', 'Recommended'), ('Guest with table side', 'Custom'), ('Candidate, compact', 'Custom'), ('Product', ''), ('Photo', ''), ('Task', '')]
    for n, cap in opts:
        sel = n == rec
        c = f'<span class="block text-body-lg text-muted-foreground">{cap}</span>' if cap else ''
        radios += f'<button role="radio" aria-checked="{"true" if sel else "false"}" class="flex min-h-16 w-full items-center gap-4 px-4 py-3 text-left">{radio_dot(sel)}<span class="min-w-0 flex-1"><span class="block text-title-3 font-normal">{n}</span>{c}</span></button>'
    return f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="S08-home.html#S08-default" class="flex size-12 items-center justify-center rounded-full" aria-label="Close import">{icon("x", "size-7")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">Import</h1>
  </header>
  <div class="shrink-0 px-gutter pb-3"><div class="flex flex-wrap items-baseline justify-between gap-x-3"><p class="text-title-3">Finish</p><p class="text-body-lg tabular-nums text-muted-foreground">Step 5 of 5</p></div>
    <div class="mt-2 flex gap-1" role="progressbar" aria-valuenow="5" aria-valuemin="1" aria-valuemax="5" aria-label="Step 5 of 5, Finish">{'<span class="h-1.5 flex-1 rounded-full bg-primary"></span>' * 5}</div></div>
  <div class="min-h-0 flex-1 overflow-y-auto px-gutter">
    <label for="lt1" class="text-title-3">List name</label>
    <input id="lt1" class="mt-2 h-16 w-full rounded-control border border-input bg-card px-4 text-title-3 font-normal" value="{name}">
    <p class="mt-3 text-body-lg text-muted-foreground">{summary}</p>{big_backup(backup) if backup else ''}
    <h2 class="mt-6 text-title-2">Card template</h2>
    <div class="mt-3 flex flex-col gap-2">
      <button class="flex min-h-16 items-center justify-center gap-3 rounded-control border border-input bg-card px-4 text-title-3 font-normal" aria-haspopup="dialog" data-action="preview-full">{icon("eye", "size-6")}See card preview</button>
      <a href="S23-template-editor.html#S23-default" class="flex min-h-16 items-center justify-center gap-3 rounded-control px-4 text-title-3 font-normal text-primary" data-action="customize-template">{icon("pencil", "size-6")}Customize</a>
    </div>
    <div class="mt-4 {GROUP}" role="radiogroup" aria-label="Card template">{radios}</div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3"><a href="{start}" class="flex min-h-16 w-full items-center justify-center rounded-control bg-primary px-6 text-title-3 text-primary-foreground" data-action="start-sorting">Start sorting</a></div>'''


P.frame('S22-large-text', 'Large text (200%): preview behind a button, templates as a list', phone(big_pick()))
P.frame('S22-import-pick-device-only-large-text', 'Large text (200%), signed in: the backup switch row wraps under its label', phone(big_pick(
    'Frontend hiring, Q4', SUM_CSV, 'Candidate', [('Candidate', 'Recommended'), ('Candidate, compact', 'Custom'), ('Guest with table side', 'Custom'), ('Person', ''), ('Product', '')],
    backup='off', start='S25-sorting.html#S25-candidate')))
P.write('S22-template-library.html')

# ================================================================== S23
E = Page('S23', 'Template editor', 'Choose which fields appear on cards and in what order: image area, title, subtitle, up to 6 field rows and up to 3 tags. Fonts and colors are fixed (TPL-04). The preview on top is the real card with the list\'s own items; previous and next cycle through them. Spec: <a href="S23-template-editor.md">S23-template-editor.md</a>. Library: <a href="S22-template-library.html">S22-template-library.html</a>.')

IMAGE_LABEL = {'none': 'None', 'avatar': 'Photo or initials', 'cover': 'Image on top', 'full': 'Full image'}
TYPE_ICON = {'name': 'type', 'role': 'type', 'yearsExperience': 'hash', 'location': 'type', 'expectedSalary': 'hash', 'portfolio': 'link', 'email': 'mail', 'source': 'type'}


def ibtn(ic, label, disabled=False, action=None, focus=False):
    d = ' disabled' if disabled else ''
    op = ' opacity-50' if disabled else ''
    da = f' data-action="{action}"' if action else ''
    f = ' ring-2 ring-ring ring-offset-2 ring-offset-card' if focus else ''
    return f'<button class="flex size-12 shrink-0 items-center justify-center rounded-full{op}{f}" aria-label="{label}"{d}{da}>{icon(ic)}</button>'


def sample_line(v, item_name):
    if v:
        return f'<span class="block truncate text-body-sm text-muted-foreground">{v}</span>'
    return f'<span class="flex items-center gap-1.5 text-body-sm text-muted-foreground">{icon("circle-dashed", "size-4 shrink-0")}No value for {item_name}</span>'


def reorder_row(key, idx, n, vals, kind='row', focus_up=False, readonly=False):
    name = CLABEL[key]
    item = vals['name']
    noun = 'field rows' if kind == 'row' else 'tags'
    if readonly:
        return f'<li class="flex min-h-14 items-center gap-4 px-4 py-2"><span class="min-w-0 flex-1"><span class="block text-body">{name}</span>{sample_line(vals.get(key), item)}</span></li>'
    return f'''<li class="flex min-h-14 items-center py-1 pl-1 pr-0.5">
        <span class="flex h-12 w-7 shrink-0 cursor-grab items-center justify-center text-muted-foreground" aria-hidden="true">{icon("grip-vertical")}</span>
        <span class="min-w-0 flex-1 pl-1"><span class="block text-body">{name}</span>{sample_line(vals.get(key), item)}</span>
        {ibtn("arrow-up", f"Move {name} up", idx == 0, "move-up", focus_up)}{ibtn("arrow-down", f"Move {name} down", idx == n - 1, "move-down")}{ibtn("x", f"Remove {name} from {noun}", action="remove")}
      </li>'''


def layout_row(label, value, sub='', warn='', href=None, error='', readonly=False):
    s = ''
    if error:
        s = f'<span class="mt-0.5 flex items-start gap-1.5 text-body-sm text-destructive">{icon("circle-alert", "size-4 mt-0.5 shrink-0")}{error}</span>'
    elif warn:
        s = f'<span class="mt-0.5 flex items-start gap-1.5 text-body-sm text-muted-foreground">{icon("eye-off", "size-4 mt-0.5 shrink-0")}{warn}</span>'
    elif sub:
        s = f'<span class="block text-body-sm text-muted-foreground">{sub}</span>'
    chev = '' if readonly else icon('chevron-right', 'size-5 shrink-0 text-muted-foreground')
    inner = f'<span class="min-w-0 flex-1"><span class="block text-body">{label}</span>{s}</span><span class="max-w-[50%] text-right text-body text-muted-foreground">{value}</span>{chev}'
    ring = ' ring-2 ring-inset ring-destructive' if error else ''
    if readonly:
        return f'<li class="flex min-h-14 items-center gap-3 px-4 py-3">{inner}</li>'
    tag = f'<a href="{href}"' if href else '<button'
    end = '</a>' if href else '</button>'
    return f'<li>{tag} class="flex min-h-14 w-full items-center gap-3 px-4 py-3 text-left{ring}" aria-haspopup="dialog">{inner}{end}</li>'


def add_row(text, href='#S23-field-picker', disabled=False, reason=''):
    if disabled:
        return f'<li class="px-4 py-3"><button class="flex min-h-touch items-center gap-3 text-label-lg text-primary opacity-50" disabled>{icon("plus")}{text}</button><p class="text-body-sm text-muted-foreground">{reason}</p></li>'
    return f'<li><a href="{href}" class="flex min-h-14 w-full items-center gap-3 px-4 text-label-lg text-primary" data-action="add-field">{icon("plus")}{text}</a></li>'


def not_on_card(keys, vals, readonly=False):
    out = ''
    for k in keys:
        name = CLABEL[k]
        if k == 'role':
            out += f'<li class="flex min-h-14 items-center gap-3 py-2 pl-4 pr-4">{icon(TYPE_ICON[k], "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">{name}</span><span class="flex items-center gap-1.5 text-body-sm text-muted-foreground">{icon("eye-off", "size-4 shrink-0")}Hidden in this list</span></span></li>'
            continue
        add = '' if readonly else f'<button class="inline-flex h-12 shrink-0 items-center gap-1.5 rounded-control px-3 text-label text-primary" aria-label="Add {name} as a field row" data-action="add-row">{icon("plus", "size-4")}Add</button>'
        out += f'<li class="flex min-h-14 items-center gap-3 py-1 pl-4 pr-2">{icon(TYPE_ICON[k], "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">{name}</span>{sample_line(vals.get(k), vals["name"])}</span>{add}</li>'
    return out


def editor_body(layout, vals, hidden=HIDDEN_CSV, part='top', focus_up_row=None, title_error=False, readonly=False, sub_warn=False, extra_top='', pt='pt-4'):
    allk = [k for k, _ in CLABEL.items()]
    used = {layout['title'], layout.get('subtitle')} | set(layout['rows']) | set(layout['tags'])
    rest = [k for k in allk if k not in used and k != 'role'] + (['role'] if 'role' not in used else [])  # hidden last
    title_val = '' if title_error else CLABEL[layout['title']]
    sub_key = layout.get('subtitle')
    sub_val = CLABEL[sub_key] if sub_key else 'None'
    lay = f'''<div>{sec_head("Layout")}<ul class="{GROUP}">
      {layout_row("Image area", IMAGE_LABEL[layout["image"]], href="#S23-image-sheet", readonly=readonly)}
      {layout_row("Title", title_val or "Not set", sub="Required", href="#S23-field-picker", error="Choose a title field. Every card needs one." if title_error else "", readonly=readonly)}
      {layout_row("Subtitle", sub_val, href="#S23-field-picker", warn="Hidden in this list, so cards leave it out" if sub_warn else "", readonly=readonly)}
    </ul></div>'''
    nrows = len(layout['rows'])
    rows = ''.join(reorder_row(k, i, nrows, vals, 'row', focus_up=(k == focus_up_row), readonly=readonly) for i, k in enumerate(layout['rows']))
    rows_add = '' if readonly else add_row('Add field row')
    rws = f'<div>{sec_head("Field rows", f"{nrows} of 6")}<ul class="{GROUP}">{rows}{rows_add}</ul></div>'
    ntags = len(layout['tags'])
    tg = ''.join(reorder_row(k, i, ntags, vals, 'tag', readonly=readonly) for i, k in enumerate(layout['tags']))
    tg_add = '' if readonly else add_row('Add tag')
    tgs = f'<div>{sec_head("Tags", f"{ntags} of 3")}<ul class="{GROUP}">{tg}{tg_add}</ul></div>'
    noc = f'<div>{sec_head("Not on the card")}<ul class="{GROUP}">{not_on_card(rest, vals, readonly)}</ul><p class="mt-2 px-1 text-body-sm text-muted-foreground">Fields that aren\'t on the card still show in item details and exports.</p></div>'
    if part == 'top':
        parts = lay + rws + tgs
    elif part == 'rows':
        parts = rws + tgs + noc
    else:
        parts = tgs + noc
    focus = ' tabindex="0" role="region" aria-label="Template layout"' if readonly else ''
    return f'<div class="min-h-0 flex-1 space-y-6 overflow-y-auto px-gutter pb-6 {pt}"{focus}>{extra_top}{parts}</div>'


def editor(layout, vals, idx, title='New template', caption='Copy of Candidate, not saved', back='#S23-discard', back_label='Back to Finish',
           part='top', overlay='', bottom_html=None, helper='', trailing='', ios=False, readonly=False, notice='', title_error=False,
           sub_warn=False, focus_up_row=None, preview_with='', bar=None, no_title=False, label_override=None, pt='pt-4', band=False):
    body = card_body(layout, vals, CLABEL, hidden=HIDDEN_CSV, no_title=no_title)
    label = label_override or card_label(layout, vals, CLABEL, HIDDEN_CSV)
    if bar is None:
        bar = back_bar(title, back, back_label, caption=caption, trailing=trailing)
    pw = f'<div class="px-gutter pb-2">{select_trigger(preview_with, "Preview with " + preview_with, ic="list-checks")}</div>' if preview_with else ''
    hp = f'<p class="px-gutter pb-2 text-center text-body-sm text-muted-foreground" role="status">{helper}</p>' if helper else ''
    nt = f'<div class="px-gutter pb-3">{notice}</div>' if notice else ''
    prev = f'''<div class="shrink-0 border-b bg-background">
    {nt}{pw}
    {stage(body, label, prevnext=True, expand_href="#S23-preview-full", extra_cls="mt-3" if ios else "")}
    <p class="pb-2 pt-1 text-center text-caption tabular-nums text-muted-foreground" aria-live="polite">Item {idx} of 12</p>
    {hp}
  </div>'''
    eb = editor_body(layout, vals, part=part, focus_up_row=focus_up_row, title_error=title_error, readonly=readonly, sub_warn=sub_warn, pt=pt)
    bot = bottom_html if bottom_html is not None else bottom('Save template', '#S23-save', 'save-template')
    return bg(f'''{bar}
  {prev}
  {eb}{'<div class="h-20 shrink-0" aria-hidden="true"></div>' if band else ''}
  {bot}''', overlay) + overlay


L01, L04, L09 = cand('k01'), cand('k04'), cand('k09')
COMPACT_PLUS = dict(COMPACT, rows=['yearsExperience', 'expectedSalary', 'portfolio'])
COMPACT_4 = dict(COMPACT, rows=['expectedSalary', 'yearsExperience', 'portfolio', 'email'])

E.section('Editor', 'Flow 4: "Customize" in the import finish step opens a copy of the recommended template (Candidate) for the list Frontend hiring, Q4. The preview is pinned on top; the layout slots scroll below it in card order.')
E.frame('S23-default', 'Default: editing a copy of Candidate (changed, not saved yet)', phone(editor(COMPACT, L01, 1)))
E.frame('S23-scrolled', 'Scrolled: field rows, tags and fields not on the card', phone(editor(COMPACT, L01, 1, part='rows')))
E.frame('S23-start', 'Just opened: unchanged copy of Candidate (Role hidden in this list)', phone(editor(
    CANDIDATE, L01, 1, caption='Copy of Candidate', back='S22-template-library.html#S22-import-pick-csv', sub_warn=True)))
save_body = f'''<div class="mt-4">{label_input("sv1", "Template name", value="Candidate, compact", focused=True, helper="You can use it on any list.")}</div>'''
E.frame('S23-save', 'Save template: name dialog', phone(editor(COMPACT, L01, 1, overlay=dlg('sd1', 'Save template', save_body,
    dbtn('Cancel', href='#S23-default') + btn('Save', 'primary', href='S22-template-library.html#S22-import-pick-custom', action='confirm-save'), role='dialog'))))
save_err = f'''<div class="mt-4">{label_input("sv2", "Template name", value="", error="Enter a name for the template.")}</div>'''
E.frame('S23-save-error', 'Save dialog: name required', phone(editor(COMPACT, L01, 1, overlay=dlg('sd2', 'Save template', save_err,
    dbtn('Cancel', href='#S23-default') + btn('Save', 'primary'), role='dialog'))))

E.section('Live preview', 'Previous and next cycle through the list\'s items (wrapping at the ends). The preview shows exactly what the sort card will show: empty values are left out, long text wraps and truncates (TPL-05, TPL-06, TPL-07).')
E.frame('S23-preview-missing', 'Missing values: Marco Bianchi has no salary and no portfolio', phone(editor(
    COMPACT_PLUS, L04, 4, part='rows', helper='2 empty fields are left out of this card.')))
E.frame('S23-preview-long', 'Long name (k09, 36 characters): the title wraps to 2 lines; rows truncate to 1 line', phone(editor(
    COMPACT, L09, 9, helper='Long titles wrap to 3 lines; very long ones get a smaller size and up to 4. Values end with … and show in full in item details.')))
full_body = card_body(COMPACT, L01, CLABEL)
full = f'''<div class="absolute inset-0 z-20 flex flex-col bg-background" role="dialog" aria-modal="true" aria-labelledby="pf1">
    <header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
      <a href="#S23-default" class="flex size-12 items-center justify-center rounded-full" aria-label="Close preview" data-action="close">{icon("x", "size-6")}</a>
      <h2 id="pf1" class="min-w-0 flex-1 truncate px-1 text-title-3">Card preview</h2>
    </header>
    <div class="relative mt-2 min-h-0 flex-1">
      <article class="absolute inset-x-gutter top-0 flex aspect-card flex-col overflow-hidden rounded-hero bg-card shadow-hero" aria-label="{LENA_COMPACT_L}" aria-roledescription="card">{full_body}</article>
    </div>
    <div class="flex shrink-0 items-center justify-center gap-6 px-gutter pb-5 pt-3">
      <button class="flex size-12 items-center justify-center rounded-full border border-input bg-card" aria-label="Previous item">{icon("chevron-left")}</button>
      <span class="text-label tabular-nums" aria-live="polite">Item 1 of 12</span>
      <button class="flex size-12 items-center justify-center rounded-full border border-input bg-card" aria-label="Next item">{icon("chevron-right")}</button>
    </div>
  </div>'''
E.frame('S23-preview-full', 'Preview at full size (same size as the sort card)', phone(editor(COMPACT, L01, 1, overlay=full)))
sk_card = '<div class="absolute inset-x-gutter top-0 flex aspect-card origin-top scale-50 flex-col overflow-hidden rounded-hero bg-card shadow-hero"><div class="space-y-6 px-6 pt-7"><span class="block h-9 w-3/4 animate-pulse rounded-full bg-muted"></span><span class="block h-6 w-1/3 animate-pulse rounded-full bg-muted"></span><span class="block h-10 w-1/2 animate-pulse rounded-full bg-muted"></span><span class="block h-10 w-2/3 animate-pulse rounded-full bg-muted"></span></div></div>'
loading_ed = f'''{back_bar("New template", "S22-template-library.html#S22-import-pick-csv", "Back to Finish", caption="Copy of Candidate")}
  <div class="shrink-0 border-b bg-background" role="status" aria-busy="true" aria-label="Loading preview items"><div class="relative h-80" aria-hidden="true">{sk_card}</div><p class="pb-2 pt-1 text-center text-caption text-muted-foreground">Loading items…</p></div>
  <div class="min-h-0 flex-1 space-y-3 overflow-hidden px-gutter pt-4" aria-hidden="true"><span class="block h-4 w-1/4 animate-pulse rounded-full bg-muted"></span><div class="h-44 animate-pulse rounded-group bg-card"></div></div>
  {bottom('Save template', disabled=True)}'''
E.frame('S23-loading', 'Loading preview items', phone(loading_ed))

E.section('Editing the layout', 'Pickers open as bottom sheets. Rows reorder by dragging the handle or with the up and down buttons (accessible alternative).')


def picker_sheet():
    def opt(k, where=None, disabled=False):
        name = CLABEL[k]
        v = LENA.get(k)
        right = f'<span class="shrink-0 text-body-sm text-muted-foreground">{where}</span>' if where else ''
        if disabled:
            return f'<li><div class="flex min-h-14 items-center gap-3 py-2" aria-disabled="true">{icon(TYPE_ICON[k], "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body text-muted-foreground">{name}</span><span class="flex items-center gap-1.5 text-body-sm text-muted-foreground">{icon("eye-off", "size-4 shrink-0")}Hidden in this list</span></span></div></li>'
        return f'<li><a href="#S23-default" class="flex min-h-14 items-center gap-3 py-2" data-action="pick-field">{icon(TYPE_ICON[k], "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">{name}</span><span class="block truncate text-body-sm text-muted-foreground">{v}</span></span>{right}</a></li>'
    body = f'''<div class="mt-2">
      <ul class="divide-y">{opt("portfolio")}{opt("email")}</ul>
      <p class="pb-1 pt-4 text-label text-muted-foreground">On the card already: choosing one moves it here</p>
      <ul class="divide-y">{opt("name", "Title")}{opt("location", "Subtitle")}{opt("yearsExperience", "Field row")}{opt("expectedSalary", "Field row")}{opt("source", "Tag")}{opt("role", disabled=True)}</ul>
    </div>'''
    return sheet('fp1', 'Add field row', body, subtitle='Values from Lena Hoffmann')


E.frame('S23-field-picker', 'Field picker sheet (Add field row)', phone(editor(COMPACT, L01, 1, part='rows', overlay=picker_sheet())))


def image_sheet():
    def opt(key, desc, sel=False, disabled=False):
        dis = ' disabled' if disabled else ''
        op = ' opacity-50' if disabled else ''
        name_cls = 'text-muted-foreground' if disabled else ''
        return f'''<button role="radio" aria-checked="{"true" if sel else "false"}" class="flex min-h-16 w-full items-center gap-4 py-2 text-left"{dis}>
          <span class="flex shrink-0 items-center{op}">{radio_dot(sel)}</span>
          <span class="w-12 shrink-0{op}">{schematic(key, "h-14")}</span>
          <span class="min-w-0 flex-1"><span class="block text-body {name_cls}">{IMAGE_LABEL[key]}</span><span class="block text-body-sm text-muted-foreground">{desc}</span></span>
        </button>'''
    body = f'''<div class="mt-2 divide-y" role="radiogroup" aria-label="Image area">
      {opt("none", "Text only. Rows get more room.", sel=True)}
      {opt("avatar", "Shows initials: this list has no Image field.")}
      {opt("cover", "Needs an Image field. This list has none.", disabled=True)}
      {opt("full", "Needs an Image field. This list has none.", disabled=True)}
    </div>'''
    return sheet('is1', 'Image area', body)


E.frame('S23-image-sheet', 'Image area sheet: options without an Image field are unavailable', phone(editor(COMPACT, L01, 1, overlay=image_sheet())))


def reorder_frame():
    vals = L01
    rows = COMPACT_4['rows']
    items = ''
    # Expected salary is being dragged above Years of experience (lifted copy + gap)
    items += f'<li class="flex h-14 items-center px-2" aria-hidden="true"><span class="h-12 w-full rounded-control border-2 border-dashed border-primary"></span></li>'
    for i, k in enumerate(['yearsExperience', 'portfolio', 'email']):
        items += reorder_row(k, i + 1, 4, vals)
    lifted = f'''<div class="pointer-events-none absolute -left-1 -right-1 top-2 z-10 flex min-h-14 scale-[1.02] items-center gap-1 rounded-control bg-popover py-1 pl-1 pr-1 shadow-overlay ring-2 ring-primary" aria-hidden="true">
        <span class="flex h-12 w-9 shrink-0 items-center justify-center text-primary">{icon("grip-vertical")}</span>
        <span class="min-w-0 flex-1"><span class="block text-body">Expected salary</span><span class="block text-body-sm text-muted-foreground">€78,000</span></span>
        <span class="flex size-12 items-center justify-center">{icon("arrow-up")}</span><span class="flex size-12 items-center justify-center">{icon("arrow-down")}</span><span class="flex size-12 items-center justify-center">{icon("x")}</span>
      </div>'''
    rws = f'<div>{sec_head("Field rows", "4 of 6")}<div class="relative"><ul class="{GROUP}">{items}{add_row("Add field row")}</ul>{lifted}</div></div>'
    tg = f'<div>{sec_head("Tags", "1 of 3")}<ul class="{GROUP}">{reorder_row("source", 0, 1, vals, "tag")}{add_row("Add tag")}</ul></div>'
    body = card_body(COMPACT_4, vals, CLABEL)
    label = card_label(COMPACT_4, vals, CLABEL)
    live = '<p class="sr-only" role="status">Expected salary, row 1 of 4.</p>'
    return f'''{back_bar("New template", "#S23-discard", "Back to Finish", caption="Copy of Candidate, not saved")}
  <div class="shrink-0 border-b bg-background">{stage(body, label, prevnext=True, expand_href="#S23-preview-full")}<p class="pb-2 pt-1 text-center text-caption tabular-nums text-muted-foreground">Item 1 of 12</p></div>
  <div class="min-h-0 flex-1 space-y-6 overflow-y-auto px-gutter pb-6 pt-4">{rws}{tg}{live}</div>
  {bottom('Save template', '#S23-save', 'save-template')}'''


E.frame('S23-reorder', 'Reorder in progress: dragging Expected salary to the top, preview follows', phone(reorder_frame()))
E.frame('S23-validation', 'Validation: Name moved to field rows, title is empty', phone(editor(
    dict(COMPACT, title=None, rows=['name', 'yearsExperience', 'expectedSalary']),
    L01, 1, title_error=True, no_title=True, label_override='No title. Berlin. Name Lena Hoffmann. Years of experience 6. Expected salary €78,000. Tag Referral.')))
discard = dlg('dc1', 'Discard this new template?', '<p class="mt-2 text-body text-muted-foreground">It hasn\'t been saved. The list keeps the template selected in the finish step.</p>',
              btn('Keep editing', 'ghost', href='#S23-default', action='cancel') + btn('Discard template', 'destructive', href='S22-template-library.html#S22-import-pick-csv', action='discard'))
E.frame('S23-discard', 'Back from a new, unsaved template: discard dialog', phone(editor(COMPACT, L01, 1, overlay=discard)))
discard2 = dlg('dc2', 'Discard changes to “Candidate, compact”?', '<p class="mt-2 text-body text-muted-foreground">Your layout changes won\'t be saved. Frontend hiring, Q4 keeps the current layout.</p>',
               btn('Keep editing', 'ghost', href='#S23-edit-saved', action='cancel') + btn('Discard changes', 'destructive', href='S22-template-library.html#S22-default', action='discard'))
E.frame('S23-discard-changes', 'Back from a saved template with unsaved changes (same as S40-discard-template)', phone(editor(
    COMPACT_PLUS, L01, 1, title='Candidate, compact', caption='Custom template, unsaved changes', back='#S23-discard-changes', back_label='Back to Card templates',
    trailing=overflow_btn(href='#S23-menu'), notice=alert('info', 'Used by Frontend hiring, Q4', 'Changes apply to that list too.', ic='layers'), overlay=discard2)))

E.section('Built-in and saved templates', 'Built-ins are read-only: duplicate first. A saved template opened from Settings or a list shows which lists use it; changes apply to all of them. Rename, Duplicate and Delete live in the overflow menu.')
bi_notice = alert('info', 'Built-in templates can\'t be changed', 'Duplicate this one to choose your own fields.', ic='lock')
E.frame('S23-built-in', 'Built-in template (Candidate): read-only, duplicate to edit', phone(editor(
    CANDIDATE, L01, 1, title='Candidate', caption='Built-in template', back='S22-template-library.html#S22-default', back_label='Back to Card templates',
    readonly=True, sub_warn=True, preview_with='Frontend hiring, Q4',
    bottom_html=bottom('Duplicate and edit', 'S23-template-editor.html#S23-start', 'duplicate-template'), part='top')))
used_notice = alert('info', 'Used by Frontend hiring, Q4', 'Changes apply to that list too.', ic='layers')
saved_trailing = overflow_btn(href='#S23-menu')
E.frame('S23-edit-saved', 'Saved template from Settings: used-by notice, no changes yet', phone(editor(
    COMPACT, L01, 1, title='Candidate, compact', caption='Custom template', back='S22-template-library.html#S22-default', back_label='Back to Card templates',
    trailing=saved_trailing, notice=used_notice, bottom_html=bottom('Save template', disabled=True))))
menu_html = menu([('text-cursor-input', 'Rename', '#S23-rename', False), ('copy', 'Duplicate', '#S23-duplicated', False), '-', ('trash-2', 'Delete template', '#S23-delete', True)])
E.frame('S23-menu', 'Overflow menu: rename, duplicate, delete', phone(editor(
    COMPACT, L01, 1, title='Candidate, compact', caption='Custom template', back='S22-template-library.html#S22-default', back_label='Back to Card templates',
    trailing=saved_trailing, notice=used_notice, bottom_html=bottom('Save template', disabled=True), overlay=menu_html)))
rn = f'''<div class="mt-4">{label_input("rn3", "Template name", value="Candidate, compact", focused=True)}</div>'''
E.frame('S23-rename', 'Rename dialog', phone(editor(
    COMPACT, L01, 1, title='Candidate, compact', caption='Custom template', trailing=saved_trailing, notice=used_notice,
    bottom_html=bottom('Save template', disabled=True),
    overlay=dlg('rd3', 'Rename template', rn, dbtn('Cancel', href='#S23-edit-saved') + btn('Rename', 'primary', href='#S23-edit-saved', action='confirm-rename'), role='dialog'))))
E.frame('S23-duplicated', 'Duplicated: now editing the copy', phone(editor(
    COMPACT, L01, 1, title='Candidate, compact (copy)', caption='Custom template, not used by any list', back='S22-template-library.html#S22-duplicated',
    back_label='Back to Card templates', trailing=saved_trailing, bottom_html=bottom('Save template', disabled=True), part='rows', band=True, pt='pt-10',
    overlay=snackbar('Duplicated as “Candidate, compact (copy)”', bottom='bottom-28'))))
del_body2 = f'''<p class="mt-2 text-body text-muted-foreground">Frontend hiring, Q4 uses this template. Its cards switch to the template you choose.</p>
    <div class="mt-4"><p class="text-label">Card template for Frontend hiring, Q4</p><div class="mt-1.5">{select_trigger("Candidate", "Card template for Frontend hiring, Q4: Candidate")}</div><p class="mt-1.5 text-caption text-muted-foreground">Candidate is the template it was based on.</p></div>'''
E.frame('S23-delete', 'Delete from the editor: choose a replacement', phone(editor(
    COMPACT, L01, 1, title='Candidate, compact', caption='Custom template', trailing=saved_trailing, notice=used_notice,
    bottom_html=bottom('Save template', disabled=True),
    overlay=dlg('dd3', 'Delete “Candidate, compact”?', del_body2, dbtn('Cancel', href='#S23-edit-saved') + btn('Delete template', 'destructive', href='S22-template-library.html#S22-deleted', action='confirm-delete'), top='top-1/4'))))

E.section('iOS, web and large text', 'iOS: Cancel and Save in the navigation bar, pickers as page sheets. Web desktop: drag with the mouse, keyboard reorder with Alt and the arrow keys. Large text: the preview opens from a button and row controls move below the field name.')
ios_ed_bar = f'''<header class="grid h-11 shrink-0 grid-cols-[1fr_auto_1fr] items-center px-2">
    <a href="#S23-discard" class="inline-flex h-12 items-center justify-self-start px-2 text-body text-primary">Cancel</a>
    <div class="min-w-0 text-center"><h1 class="truncate text-body font-semibold">New template</h1><p class="text-caption text-muted-foreground">Copy of Candidate</p></div>
    <a href="#S23-save" class="inline-flex h-12 items-center justify-self-end px-2 text-body font-semibold text-primary" data-action="save-template">Save</a>
  </header>'''
E.frame('S23-ios', 'iOS: Cancel and Save in the navigation bar', phone(editor(COMPACT, L01, 1, bar=ios_ed_bar, bottom_html='', ios=True), ios=True))
kb = lambda k: f'<kbd class="inline-flex h-6 min-w-6 items-center justify-center rounded-sm border border-b-2 bg-card px-1.5 text-caption text-foreground">{k}</kbd>'
web_hint = f'<div class="flex shrink-0 flex-wrap items-center justify-center gap-x-1.5 gap-y-1 border-t bg-background px-gutter py-2 text-caption text-muted-foreground" aria-label="Keyboard shortcuts">{kb("Alt")}+{kb("↑")}{kb("↓")}<span>moves the focused row</span></div>'
web_ed = editor(COMPACT, L01, 1, part='rows', focus_up_row='expectedSalary').replace('<div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">', web_hint + '<div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3">', 1)
E.frame('S23-web-desktop', 'Web, desktop browser: keyboard reorder, focus visible', desktop(web_ed, 'swipesort.app/import/template'))


def big_editor():
    def brow(name, sample, first=False, last=False):
        b = lambda ic, t, aria, dis=False: f'<button class="inline-flex min-h-touch items-center gap-2 rounded-control border border-input bg-card px-3 text-body-lg{" opacity-50" if dis else ""}"{" disabled" if dis else ""} aria-label="{aria}">{icon(ic, "size-6")}{t}</button>'
        return f'''<li class="px-4 py-3"><p class="text-title-3 font-normal">{name}</p><p class="text-body-lg text-muted-foreground">{sample}</p>
        <div class="mt-2 flex flex-wrap gap-2">{b("arrow-up", "Up", f"Move {name} up", first)}{b("arrow-down", "Down", f"Move {name} down", last)}{b("x", "Remove", f"Remove {name} from field rows")}</div></li>'''
    lrow = lambda l, v: f'<li><button class="flex min-h-16 w-full items-center gap-3 px-4 py-3 text-left" aria-haspopup="dialog"><span class="min-w-0 flex-1"><span class="block text-title-3 font-normal">{l}</span><span class="block text-body-lg text-muted-foreground">{v}</span></span>{icon("chevron-right", "size-6 shrink-0 text-muted-foreground")}</button></li>'
    return f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="#S23-discard" class="flex size-12 items-center justify-center rounded-full" aria-label="Back to Finish">{icon("arrow-left", "size-7")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">New template</h1>
  </header>
  <div class="min-h-0 flex-1 space-y-5 overflow-y-auto px-gutter pt-2">
    <a href="#S23-preview-full" class="flex min-h-16 items-center justify-center gap-3 rounded-control border border-input bg-card px-4 text-title-3 font-normal" data-action="preview-full">{icon("eye", "size-6")}See card preview</a>
    <ul class="{GROUP}">{lrow("Image area", "None")}{lrow("Title", "Name")}{lrow("Subtitle", "Location")}</ul>
    <div><h2 class="px-1 pb-2 text-title-3">Field rows <span class="font-normal text-muted-foreground">2 of 6</span></h2>
    <ul class="{GROUP}">{brow("Years of experience", "6", first=True)}{brow("Expected salary", "€78,000", last=True)}</ul></div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3"><a href="#S23-save" class="flex min-h-16 w-full items-center justify-center rounded-control bg-primary px-6 text-title-3 text-primary-foreground" data-action="save-template">Save template</a></div>'''


E.frame('S23-large-text', 'Large text (200%): preview behind a button, labeled row controls', phone(big_editor()))
E.write('S23-template-editor.html')
