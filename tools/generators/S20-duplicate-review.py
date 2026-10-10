# Usage: python3 tools/generators/S20-duplicate-review.py
# Generates design/03-screens/S20-duplicate-review.html
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from groupc2_common import *  # noqa

P = Page('S20', 'Duplicate review', 'Step 4 of the import: items that look alike are shown side by side with matching fields marked by icon and label. Merge, keep both or skip; anything not reviewed is kept. Also used when adding items to an existing list (S21). Spec: <a href="S20-duplicate-review.md">S20-duplicate-review.md</a>.')

C = CONTACTS
OPTS = [('merge', 'Merge', 'merge'), ('keep', 'Keep both', 'copy'), ('skip', 'Skip', 'skip-forward')]


def options(gid, choice, names, help_text=None, large=False, review=False):
    btns = ''
    for key, label, ic in OPTS:
        sel = key == choice
        if sel:
            cls = 'border-2 border-primary bg-primary-soft text-primary-soft-foreground'
            ic_html = icon('check', 'size-5 shrink-0')
        else:
            cls = 'border border-input bg-card'
            ic_html = icon(ic, 'size-5 shrink-0 text-muted-foreground')
        txt = 'text-title-3 font-normal' if large else 'text-label'
        layout = 'w-full justify-start px-4 min-h-14 gap-2' if large else 'min-h-14 flex-col justify-center px-1.5 gap-0.5 text-center'
        btns += f'<button role="radio" aria-checked="{"true" if sel else "false"}" class="flex {layout} items-center rounded-control py-1.5 {cls} {txt}">{ic_html}<span>{label}</span></button>'
    grid = 'flex flex-col gap-2' if large else 'grid grid-cols-3 gap-2'
    h = ''
    if help_text:
        hc = 'text-body-lg' if large else 'text-body-sm'
        h = f'<p class="mt-2 {hc} text-muted-foreground" role="status">{help_text}</p>'
    if review:
        h += f'<a href="#S20-merge" class="-ml-3 mt-1 inline-flex h-12 items-center gap-2 rounded-control px-3 text-label-lg text-primary" data-action="review-merge">{icon("git-merge", "size-5")}Review merge</a>'
    return f'<div role="radiogroup" aria-label="What to do with {names}" class="{grid}">{btns}</div>{h}'


def marker(kind):
    if kind == 'same':
        return f'<span class="ml-auto inline-flex items-center gap-1 text-caption text-foreground">{icon("equal", "size-3.5")}Same</span>'
    if kind == 'similar':
        return f'<span class="ml-auto inline-flex items-center gap-1 text-caption text-foreground">{icon("equal-approximately", "size-3.5")}Similar</span>'
    return ''


def comp_rows(rows):
    out = ''
    for label, v1, v2, kind in rows:
        band = 'rounded-sm bg-muted px-2 -mx-2' if kind else ''
        vcls = ''
        v1 = v1.replace('@', '@<wbr>')
        v2 = v2.replace('@', '@<wbr>')
        out += f'''<div class="border-t py-1.5"><div class="{band} py-1">
          <p class="flex items-center gap-1.5 text-caption text-muted-foreground">{label}{marker(kind)}</p>
          <p class="mt-0.5 grid grid-cols-2 gap-3 text-body-sm {vcls}"><span class="min-w-0 break-words">{v1}</span><span class="min-w-0 break-words">{v2}</span></p>
        </div></div>'''
    return out


def person_head(cid, name=None, extra=''):
    c = C[cid]
    return f'<div class="flex min-w-0 items-center gap-2.5">{avatar(cid, size="size-10")}<div class="min-w-0"><p class="break-words text-body font-medium">{name or c["name"]}</p>{extra}</div></div>'


def group(gid, reason_ic, reason, pos, left, right, rows, choice, help_text, col_labels=None, tag='', review=False):
    names = f'{left[1]} and {right[1]}'
    cols = ''
    if col_labels:
        cols = f'<div class="mt-3 grid grid-cols-2 gap-3 px-4 text-caption text-muted-foreground"><span>{col_labels[0]}</span><span>{col_labels[1]}</span></div>'
    return f'''<section class="rounded-group bg-card" aria-labelledby="{gid}">
      <div class="flex items-start gap-3 px-4 pt-4">
        {icon(reason_ic, "mt-0.5 size-5 shrink-0 text-muted-foreground")}
        <h3 id="{gid}" class="min-w-0 flex-1 text-label">{reason}</h3>{tag}
        <span class="shrink-0 text-caption tabular-nums text-muted-foreground">{pos}</span>
      </div>
      {cols}
      <div class="mt-2 grid grid-cols-2 gap-3 px-4">{left[0]}{right[0]}</div>
      <div class="mt-3 px-4">{comp_rows(rows)}</div>
      <div class="px-4 pb-4 pt-2">{options(gid, choice, names, help_text, review=review)}</div>
    </section>'''


IDENT = badge('Identical', 'copy-check', 'outline')

G1 = lambda choice='merge', help_text='One item with values from both.', review=True: group(
    'g1', 'phone', 'Same phone number, similar name', '1 of 4',
    (person_head('c001'), 'Ayşe Demir'), (person_head('c097'), 'Ayse Demir'),
    [('Name', 'Ayşe Demir', 'Ayse Demir', 'similar'), ('Phone', '+90 500 000 97 62', '+90 500 000 97 62', 'same'),
     ('Email', 'ayse.demir@example.com', 'ayse.demir@example.com', 'same'), ('City', 'İstanbul', 'İstanbul', 'same')],
    choice, help_text, review=review and choice == 'merge')
G2 = lambda choice='keep', help_text='Both are imported as separate items.': group(
    'g2', 'mail', 'Same email, similar name', '2 of 4',
    (person_head('c093'), 'Can Öztürk'), (person_head('c098'), 'Can Ozturk'),
    [('Name', 'Can Öztürk', 'Can Ozturk', 'similar'), ('Phone', '+90 500 000 75 94', '+90 500 000 49 08', None),
     ('Email', 'can.ozturk@example.com', 'can.ozturk@example.com', 'same'), ('City', 'İstanbul', 'İstanbul', 'same')],
    choice, help_text)
G3 = lambda choice=None, help_text=None, review=False: group(
    'g3', 'user', 'Same name', '3 of 4',
    (person_head('c005'), 'Elif Şahin'), (person_head('c099'), 'Elif Şahin'),
    [('Name', 'Elif Şahin', 'Elif Şahin', 'same'), ('Phone', '+90 500 000 45 82<span class="block text-muted-foreground">Mobile</span>', '+90 232 000 18 07<span class="block text-muted-foreground">Work</span>', None),
     ('Email', 'elif.sahin@example.com', 'elif.sahin@example.org', None), ('City', 'İzmir', 'İzmir', 'same')],
    choice, help_text, review=review)
G4 = lambda choice=None, help_text=None: group(
    'g4', 'copy-check', 'Identical name, phone and email', '4 of 4',
    (person_head('c058'), 'Jonas Weber'), (person_head('c100'), 'Jonas Weber'),
    [('Name', 'Jonas Weber', 'Jonas Weber', 'same'), ('Phone', '+49 30 0000 2868', '+49 30 0000 2868', 'same'),
     ('Email', 'jonas.weber@example.com', 'jonas.weber@example.com', 'same'), ('City', 'Berlin', 'Berlin', 'same')],
    choice, help_text)


def head(title, body, reviewed, total, bulk=None):
    pct = round(reviewed * 100 / total)
    b = bulk if bulk is not None else btn('Merge all identical (1)', 'outline', 'merge', extra='shrink-0')
    return f'''<div class="px-gutter">
      <h2 class="text-title-2">{title}</h2>
      <p class="mt-1 text-body text-muted-foreground">{body}</p>
      <div class="mt-4 flex flex-wrap items-center justify-between gap-x-3 gap-y-2"><span class="text-label tabular-nums">{reviewed} of {total} reviewed</span>{b}</div>
      <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="{reviewed}" aria-valuemin="0" aria-valuemax="{total}" aria-label="{reviewed} of {total} reviewed"><div class="h-full w-[{pct}%] rounded-full bg-primary"></div></div>
    </div>'''


INTRO = 'These items look alike. Merge them, keep both, or skip one. Anything you don\'t review is kept.'


def screen(content, note='', label='Continue', href='S22-template-library.html#S22-import-pick', bar=None, step=(4, 5), overlay='', title='Import', close='S08-home.html#S08-default', secondary=''):
    return f'''{bar or modal_bar(title, close)}
  {stepper("Review duplicates", *step)}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-4 pb-6 pt-1">
    {content}
    </div>
  </div>
  {bottom(label, href, "continue", note=note, secondary=secondary)}
  {overlay}'''


# ------------------------------------------------------------------ review
P.section('Review', 'Four groups from the sample data (c001/c097, c093/c098, c005/c099, c058/c100). Each group shows both items, marks matching fields with an icon and the word Same or Similar, and offers Merge, Keep both or Skip.')

default_content = f'''{head("4 possible duplicates", INTRO, 2, 4)}
    <div class="space-y-3 px-gutter">{G1()}{G2()}</div>'''
P.frame('S20-default', 'Default: 4 groups, 2 reviewed', phone(screen(default_content, note='2 not reviewed yet. They\'ll be imported as separate items.',
    secondary=ghost_full('Review the other 2', '#S20-reviewed-all', 'review'))))

scrolled = f'''<div class="space-y-3 px-gutter">{G3()}{G4()}</div>'''
P.frame('S20-scrolled', 'Scrolled: groups 3 and 4 not reviewed yet', phone(screen(scrolled, note='2 not reviewed yet. They\'ll be imported as separate items.')))

g4_merged = f'''{head("4 possible duplicates", INTRO, 4, 4, bulk='')}
    <div class="space-y-3 px-gutter">{G3("merge", "One item with values from both.", review=True)}{G4("merge", "One item. Nothing differs, so there's nothing to choose.")}</div>'''
P.frame('S20-reviewed-all', 'All 4 reviewed: 3 merged, 1 kept both (85 of 88)', phone(screen(g4_merged, note='All 4 reviewed: 3 merged, 1 kept both. 85 of 88 contacts will be imported.')))

# merge detail sheet
merge_body = f'''<div class="mt-4 min-h-0 flex-1 space-y-5 overflow-hidden pb-2">
      <div class="flex items-center gap-3">{avatar("c005", size="size-14")}<div><p class="text-title-3">Elif Şahin</p><p class="text-body-sm text-muted-foreground">Photo from the first item</p></div></div>
      <fieldset>
        <legend class="text-label">Phone</legend>
        <p class="text-caption text-muted-foreground">Both numbers are kept. The first one shows on cards.</p>
        <div class="mt-1 divide-y">
          <button role="checkbox" aria-checked="true" class="flex min-h-12 w-full items-center gap-3 py-1.5 text-left">{checkbox_box(True)}<span class="flex-1 text-body tabular-nums">+90 500 000 45 82</span><span class="text-body-sm text-muted-foreground">Mobile</span></button>
          <button role="checkbox" aria-checked="true" class="flex min-h-12 w-full items-center gap-3 py-1.5 text-left">{checkbox_box(True)}<span class="flex-1 text-body tabular-nums">+90 232 000 18 07</span><span class="text-body-sm text-muted-foreground">Work</span></button>
        </div>
      </fieldset>
      <fieldset>
        <legend class="text-label">Email</legend>
        <p class="text-caption text-muted-foreground">Choose one.</p>
        <div class="mt-1 divide-y" role="radiogroup" aria-label="Email">
          <button role="radio" aria-checked="true" class="flex min-h-12 w-full items-center gap-3 py-1.5 text-left">{radio_dot(True)}<span class="min-w-0 flex-1 break-words text-body">elif.sahin@example.com</span></button>
          <button role="radio" aria-checked="false" class="flex min-h-12 w-full items-center gap-3 py-1.5 text-left">{radio_dot(False)}<span class="min-w-0 flex-1 break-words text-body">elif.sahin@example.org</span></button>
        </div>
      </fieldset>
      <div class="flex items-start gap-3 rounded-control bg-muted px-4 py-3">{icon("equal", "mt-0.5 size-4 shrink-0")}<p class="text-body-sm">Name, Side, Relationship and City are the same in both.</p></div>
    </div>'''
merge_actions = f'<button class="{PRIMARY}">Merge</button><button class="mt-1 flex h-12 w-full items-center justify-center rounded-control text-label-lg">Cancel</button>'
P.frame('S20-merge', 'Merge detail: choose values, phones combined', phone(screen(scrolled, overlay=sheet('ms1', 'Merge 2 items', merge_body, merge_actions, subtitle='Choose which values to keep.'))))

summary_rows = [
    ('c001', 'Ayşe Demir', 'Merged', 'merge'),
    ('c093', 'Can Öztürk and Can Ozturk', 'Kept both', 'copy'),
    ('c005', 'Elif Şahin', 'Merged', 'merge'),
    ('c058', 'Jonas Weber', 'Merged', 'merge'),
]
sr = ''.join(f'''<li class="flex min-h-16 items-center gap-3 px-4 py-2">{avatar(cid, size="size-10")}<div class="min-w-0 flex-1"><p class="line-clamp-2 text-body">{name}</p><p class="flex items-center gap-1.5 text-body-sm text-muted-foreground">{icon(ic, "size-4")}{res}</p></div><a href="#S20-default" class="inline-flex min-h-touch items-center rounded-control px-3 text-label text-primary" aria-label="Change what happens to {name}">Change</a></li>''' for cid, name, res, ic in summary_rows)
summary = f'''<div class="px-gutter">
      <div class="flex items-center gap-3">{icon("circle-check", "size-6 shrink-0 text-muted-foreground")}<h2 class="text-title-2">All 4 reviewed</h2></div>
      <p class="mt-1 text-body text-muted-foreground">85 of 88 contacts will be imported: 3 pairs merged into one item each, 1 pair kept as two items.</p>
    </div>
    <div class="px-gutter"><ul class="divide-y overflow-hidden rounded-group bg-card">{sr}</ul></div>'''
P.frame('S20-summary', 'After review: summary', phone(screen(summary)))

# ------------------------------------------------------------------ none / loading
P.section('No duplicates and loading', 'Detection runs after mapping, because phone numbers and emails are compared in their mapped type. When nothing is found the step is skipped (A-23); this screen appears when the user steps back from Finish.')
none = f'''<div class="flex flex-1 flex-col items-center justify-center px-8 pb-16 text-center">
      {icon("copy-check", "size-8 text-muted-foreground")}
      <h2 class="mt-4 text-title-3">No duplicates found</h2>
      <p class="mt-1 max-w-xs text-body text-muted-foreground">All 12 items are different, so there\'s nothing to merge.</p>
    </div>'''
P.frame('S20-none', 'No duplicates found (candidates-q4.csv)', phone(f'''{modal_bar()}
  {stepper("Review duplicates", 4, 5)}
  {none}
  {bottom("Continue", "S22-template-library.html#S22-import-pick-csv", "continue")}'''))

sk = ''.join('''<div class="space-y-3 rounded-group bg-card p-4"><span class="block h-4 w-1/2 animate-pulse rounded-full bg-muted"></span><div class="grid grid-cols-2 gap-3"><div class="flex items-center gap-2"><span class="size-10 animate-pulse rounded-full bg-muted"></span><span class="h-3.5 flex-1 animate-pulse rounded-full bg-muted"></span></div><div class="flex items-center gap-2"><span class="size-10 animate-pulse rounded-full bg-muted"></span><span class="h-3.5 flex-1 animate-pulse rounded-full bg-muted"></span></div></div><span class="block h-3 w-full animate-pulse rounded-full bg-muted"></span><span class="block h-3 w-3/4 animate-pulse rounded-full bg-muted"></span></div>''' for _ in range(2))
P.frame('S20-loading', 'Looking for duplicates', phone(f'''{modal_bar()}
  {stepper("Review duplicates", 4, 5)}
  <div class="min-h-0 flex-1 space-y-4 overflow-hidden pt-1">
    <div class="px-gutter">{spinner_line("Looking for duplicates in 88 items…")}</div>
    <div class="space-y-3 px-gutter" aria-hidden="true">{sk}</div>
  </div>
  {bottom("Continue", disabled=True)}'''))

# ------------------------------------------------------------------ existing items (S21)
P.section('Against items already in the list', 'Used by S21 Add items: rows from the new source are compared with items already in the list. The left column is the existing item with its final decision; merging fills in values and keeps decisions and notes.')
accepted = f'<span class="mt-0.5 inline-flex items-center gap-1 text-caption text-accept-soft-foreground">{icon("check", "size-3.5")}Accepted</span>'


def ex_head(cid, decided=True):
    return person_head(cid, extra=accepted if decided else '')


E1 = group('e1', 'copy-check', 'Identical name, phone and email', '1 of 3',
           (ex_head('c003'), 'Zeynep Kaya'), (person_head('c003'), 'Zeynep Kaya in the file'),
           [('Name', 'Zeynep Kaya', 'Zeynep Kaya', 'same'), ('Phone', '+90 500 000 97 10', '+90 500 000 97 10', 'same'),
            ('Email', 'zeynep.kaya@example.com', 'zeynep.kaya@example.com', 'same')],
           'skip', 'Zeynep Kaya stays as it is. The row isn\'t added.', col_labels=('In the list', 'In mert-family.csv'))
E2 = group('e2', 'phone', 'Same name and phone number', '2 of 3',
           (ex_head('c009'), 'Oğuz Kılıç'), (person_head('c009'), 'Oğuz Kılıç in the file'),
           [('Name', 'Oğuz Kılıç', 'Oğuz Kılıç', 'same'), ('Phone', '+90 500 000 62 86 <span class="text-muted-foreground">+1</span>', '+90 500 000 62 86', 'same'),
            ('Address', '<span class="text-muted-foreground">Empty</span>', 'Çankaya, Ankara', None)],
           'merge', 'Oğuz Kılıç gets the Address from the file. Decisions and notes stay.', col_labels=('In the list', 'In mert-family.csv'))
existing = f'''{head("3 already in Wedding guests", "These rows in mert-family.csv match items in the list. Skip leaves the list as it is; Merge fills in new values and keeps decisions and notes.", 2, 3, btn("Skip all identical (1)", "outline", "skip-forward", extra="shrink-0"))}
    <div class="space-y-3 px-gutter">{E1}{E2}</div>'''
P.frame('S20-existing', 'Already in the list (used by S21)', phone(screen(
    existing, note='1 not reviewed yet. It will be added as a new item.', href='S21-add-items.html#S21-confirm',
    title='Add items', close='S09-list-overview.html#S09-shared')))

# ------------------------------------------------------------------ large number
P.section('Many duplicates', 'Large imports collapse groups into rows with a quick action each, a filter by match type and bulk actions. Tapping a row opens the full comparison.')
lg_rows = [
    ('c001', 'Ayşe Demir, Ayse Demir', 'Same phone number, similar name', 'Not reviewed'),
    ('c058', 'Jonas Weber (2)', 'Identical', 'Not reviewed'),
    ('c002', 'Mehmet Yılmaz (2)', 'Identical', 'Not reviewed'),
    ('c005', 'Elif Şahin (2)', 'Same name', 'Keep both'),
    ('c093', 'Can Öztürk, Can Ozturk', 'Same email, similar name', 'Not reviewed'),
    ('c010', 'Şule Erdoğan, Sule Erdogan', 'Same phone number, similar name', 'Not reviewed'),
    ('c006', 'Burak Arslan (2)', 'Identical', 'Not reviewed'),
]
lr = ''
for cid, names, reason, state in lg_rows:
    st_cls = 'text-muted-foreground' if state == 'Not reviewed' else ''
    lr += f'''<li class="flex min-h-16 items-center gap-3 px-4 py-2">{avatar(cid, size="size-10")}<a href="#S20-default" class="flex min-h-touch min-w-0 flex-1 flex-col justify-center"><span class="line-clamp-2 block text-body">{names}</span><span class="block truncate text-body-sm text-muted-foreground">{reason}</span></a>
      <button class="inline-flex min-h-touch shrink-0 items-center gap-1 rounded-control px-2 text-label {st_cls}" aria-haspopup="menu" aria-label="{names}: {state}. Choose what to do">{state}{icon("chevron-down", "size-4")}</button></li>'''
chips = f'''<div class="flex flex-wrap gap-2" role="tablist" aria-label="Filter duplicates">
      <button role="tab" aria-selected="true" class="inline-flex min-h-touch items-center"><span class="inline-flex h-9 items-center gap-1.5 rounded-full border border-primary bg-primary-soft px-3 text-label text-primary-soft-foreground">{icon("check", "size-4")}All 41</span></button>
      <button role="tab" aria-selected="false" class="inline-flex min-h-touch items-center"><span class="inline-flex h-9 items-center rounded-full border border-input px-3 text-label">Identical 26</span></button>
      <button role="tab" aria-selected="false" class="inline-flex min-h-touch items-center"><span class="inline-flex h-9 items-center rounded-full border border-input px-3 text-label">Similar 15</span></button>
    </div>'''
bulk = f'''<div class="flex flex-wrap gap-2">{btn("Merge all identical (26)", "secondary", "merge")}{btn("Keep both for the rest", "outline")}</div>'''
large_content = f'''{head("41 possible duplicates", "Your contacts have many repeated items. Merge the identical ones in one step, then check the rest.", 1, 41, bulk='')}
    <div class="space-y-3 px-gutter">{bulk}{chips}</div>
    <div class="px-gutter"><ul class="divide-y overflow-hidden rounded-group bg-card">{lr}</ul></div>'''
P.frame('S20-large', 'Many duplicates: bulk actions (1,204 contacts)', phone(screen(large_content, note='40 not reviewed yet. They\'ll be imported as separate items.')))

# ------------------------------------------------------------------ accessibility
P.section('Accessibility', 'At 200% text the two items no longer fit side by side: each field lists one value when both are the same, or both values numbered 1 and 2. Options stack as full-width buttons.')
big_fields = [
    ('Name', [('1', 'Ayşe Demir'), ('2', 'Ayse Demir')], 'similar'),
    ('Phone', [(None, '+90 500 000 97 62')], 'same'),
    ('Email', [(None, 'ayse.demir@example.com')], 'same'),
]
bf = ''
for label, vals, kind in big_fields:
    mk = f'<span class="inline-flex items-center gap-1.5 text-body-lg">{icon("equal" if kind == "same" else "equal-approximately", "size-5")}{"Same" if kind == "same" else "Similar"}</span>'
    vs = ''.join(f'<p class="text-title-2 font-normal break-words">{(n + ". ") if n else ""}{v}</p>' for n, v in vals)
    bf += f'<div class="border-t py-3"><div class="flex flex-wrap items-center justify-between gap-2"><p class="text-body-lg text-muted-foreground">{label}</p>{mk}</div>{vs}</div>'
big = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="S08-home.html#S08-default" class="flex size-12 items-center justify-center rounded-full" aria-label="Close import">{icon("x", "size-7")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">Import</h1>
  </header>
  <div class="shrink-0 px-gutter pb-3"><p class="text-title-3">Review duplicates</p><p class="text-body-lg text-muted-foreground">Step 4 of 5</p></div>
  <div class="min-h-0 flex-1 overflow-hidden px-gutter">
    <p class="text-title-3 font-normal tabular-nums">2 of 4 reviewed</p>
    <section class="mt-3 rounded-group bg-card px-4 pb-4 pt-4" aria-labelledby="lg1">
      <h3 id="lg1" class="text-title-2">Same phone number, similar name</h3>
      <div class="mt-2">{bf}</div>
      <div class="mt-2">{options("lg1", "merge", "Ayşe Demir and Ayse Demir", "One item with values from both.", large=True)}</div>
    </section>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3"><a href="S22-template-library.html#S22-import-pick" class="flex min-h-16 w-full items-center justify-center rounded-control bg-primary px-6 text-title-3 text-primary-foreground" data-action="continue">Continue</a></div>'''
P.frame('S20-large-text', 'Large text (200%)', phone(big))

# ------------------------------------------------------------------ iOS
P.section('iOS', 'Same review layout with the iOS bar (back chevron, edge swipe goes back to mapping). The merge detail is a page sheet with Cancel and Merge in its bar instead of bottom buttons.')
ios_bar = modal_bar(ios=True, back=('Map fields', 'S19-field-mapping.html#S19-contacts'))
P.frame('S20-ios', 'iOS', phone(screen(default_content, note='2 not reviewed yet. They\'ll be imported as separate items.', bar=ios_bar), ios=True))
P.frame('S20-ios-merge', 'iOS: merge detail as a page sheet', phone(screen(scrolled, bar=ios_bar, overlay=ios_sheet('ims', 'Merge 2 items', merge_body.replace('mt-4 min-h-0', 'mt-3 min-h-0'), right='Merge')), ios=True, overlay_full=True))

P.write('S20-duplicate-review.html')
