# Usage: python3 tools/generators/S16-plain-text.py
# Generates design/03-screens/S16-plain-text.html
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from groupc2_common import *  # noqa

P = Page('S16', 'Plain-text import', 'Step 2 of a plain-text import: paste a list or open a .txt file, one item per line. Parsed lines become items with one field, named in S19. Spec: <a href="S16-plain-text.md">S16-plain-text.md</a>.')

BOOKS = DATA['books']
CLOSE = 'S08-home.html#S08-default'
NEXT = 'S19-field-mapping.html#S19-text'


def tabs(active='text', count=12, large=False):
    txt = 'text-title-2 font-normal' if large else 'text-label'

    def tab(key, label):
        on = key == active
        cls = 'bg-card shadow-raised' if on else 'text-muted-foreground'
        return f'<button role="tab" aria-selected="{"true" if on else "false"}" class="{"min-h-14" if large else "min-h-touch"} flex-1 rounded-full px-3 {txt} {cls}">{label}</button>'
    return f'<div class="flex rounded-full bg-secondary p-1" role="tablist" aria-label="Show">{tab("text", "Text")}{tab("preview", f"Preview ({count})")}</div>'


_ta = [0]


def textarea(lines, rows=15, placeholder='', focused=False, extra='', large=False):
    _ta[0] += 1
    tid = f'ta{_ta[0]}'
    border = 'border-primary ring-2 ring-ring/30' if focused else 'border-input'
    txt = 'text-title-2 font-normal' if large else 'text-body'
    ph = f' placeholder="{placeholder}"' if placeholder else ''
    content = '\n'.join(lines)
    return f'<label for="{tid}" class="sr-only">Items, one per line</label><textarea id="{tid}" rows="{rows}" class="block w-full resize-none rounded-control border {border} bg-card px-3.5 py-3 {txt} placeholder:text-muted-foreground {extra}"{ph}>{content}</textarea>'


def count_line(main, sub='', main_cls='text-label', error=False):
    if error:
        m = f'<span class="inline-flex items-center gap-1.5 text-label tabular-nums text-destructive">{icon("circle-alert", "size-4")}{main}</span>'
    else:
        m = f'<span class="{main_cls} tabular-nums">{main}</span>'
    s = f'<span class="text-caption text-muted-foreground">{sub}</span>' if sub else ''
    return f'<div class="mt-2 flex items-baseline justify-between gap-3" role="status">{m}{s}</div>'


OPEN_FILE = btn('Open a .txt file', 'outline', 'file-up', extra='w-full')


def heading(large=False):
    t = 'text-display' if large else 'text-title-2'
    b = 'text-title-2 font-normal' if large else 'text-body'
    return f'<h2 class="{t}">Paste your list</h2><p class="mt-1 {b} text-muted-foreground">One item per line. Blank lines are skipped.</p>'


def screen(body, bottom_html, bar=None, overlay=''):
    return f'''{bar or modal_bar('Import', CLOSE)}
  {stepper("Select items", 2, 4)}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-4 px-gutter pb-6 pt-1">
    {body}
    </div>
  </div>
  {bottom_html}
  {overlay}'''


DEFAULT_LINES = BOOKS[:6] + [''] + BOOKS[6:]


def default_body(lines=DEFAULT_LINES, rows=15, extra_top='', count='12 items', sub='1 blank line skipped', tabs_html=None, after='', file_chip=''):
    return f'''<div>{heading()}</div>
    {tabs_html or tabs()}
    {extra_top}
    {file_chip}
    <div>{textarea(lines, rows)}{count_line(count, sub)}</div>
    {after or OPEN_FILE}'''


# ------------------------------------------------------------------ frames
P.section('Paste or open a file', 'One item per line. The live count updates as the user types; blank lines are skipped and counted separately. Opening a .txt file loads its text into the same box, where it stays editable.')

P.frame('S16-default', 'Default: 12 lines pasted', phone(screen(default_body(), bottom('Continue', NEXT, 'continue'))))

P.frame('S16-empty', 'Empty (first open)', phone(screen(
    f'''<div>{heading()}</div>
    {tabs(count=0)}
    <div>{textarea([], 15, placeholder='Type or paste, one item per line', focused=True)}{count_line('0 items', main_cls='text-label text-muted-foreground')}</div>
    {OPEN_FILE}''',
    bottom('Continue', disabled=True))))

rows = ''.join(f'<li class="flex min-h-12 items-center gap-3 px-4 py-2"><span class="w-6 shrink-0 text-caption tabular-nums text-muted-foreground" aria-hidden="true">{i + 1}</span><span class="min-w-0 flex-1 text-body">{b}</span></li>' for i, b in enumerate(BOOKS))
P.frame('S16-preview', 'Preview tab: parsed items in order', phone(screen(
    f'''<div>{heading()}</div>
    {tabs('preview')}
    <p class="text-body-sm text-muted-foreground">Each line becomes one item, in this order.</p>
    <ol class="divide-y overflow-hidden rounded-group bg-card" aria-label="12 items">{rows}</ol>''',
    bottom('Continue', NEXT, 'continue'))))

dup_lines = BOOKS[:3] + ['Piranesi'] + BOOKS[3:10] + ['Station Eleven'] + BOOKS[10:]
dup_alert = alert('info', '2 lines appear twice: Piranesi, Station Eleven.', 'Duplicates stay in the list unless you remove them.', alert_button('Remove duplicates', 'remove-duplicates'), ic='copy')
P.frame('S16-duplicates', 'Duplicate lines', phone(screen(
    default_body(dup_lines, rows=9, extra_top=dup_alert, count='14 items, 2 duplicates', sub='', tabs_html=tabs(count=14)),
    bottom('Continue', NEXT, 'continue'))))

many_lines = ['Ishiguro, The Buried Giant', 'Le Guin, The Dispossessed', 'Mandel, Sea of Tranquility', 'Pamuk, Kar', 'Pamuk, Masumiyet Müzesi', 'Atwood, The Testaments',
              'Kemal, Yer Demir Gök Bakır', 'Clarke, Jonathan Strange and Mr Norrell', 'von Arnim, Elizabeth and Her German Garden', 'Ali, Kürk Mantolu Madonna']
many_alert = alert('error', '6,214 lines', 'Up to 5,000 items can be imported at a time. Only the first 5,000 lines will be imported.', ic='circle-alert')
P.frame('S16-too-many', 'Too many lines (limit 5,000)', phone(screen(
    default_body(many_lines, rows=10, extra_top=many_alert, count='6,214 items', sub='', tabs_html=tabs(count='5,000')).replace(
        '<span class="text-label tabular-nums">6,214 items</span>',
        f'<span class="inline-flex items-center gap-1.5 text-label tabular-nums text-destructive">{icon("circle-alert", "size-4")}6,214 items, limit 5,000</span>'),
    bottom('Continue with 5,000 items', NEXT, 'continue'))))

file_chip = f'''<div class="flex min-h-14 items-center gap-3 rounded-control border bg-card py-1 pl-4 pr-1">
      {icon("file-text", "size-5 shrink-0 text-muted-foreground")}
      <div class="min-w-0 flex-1"><p class="truncate text-body">book-club.txt</p><p class="text-caption text-muted-foreground">12 lines, editable below</p></div>
      {btn('Clear', 'ghost', aria='Clear book-club.txt', extra='px-3')}
    </div>'''
P.frame('S16-file', 'Opened book-club.txt', phone(screen(
    default_body(BOOKS, rows=12, file_chip=file_chip, sub='', after=btn('Open another file', 'ghost', 'file-up', extra='w-full')),
    bottom('Continue', NEXT, 'continue'))))

# ------------------------------------------------------------------ states
P.section('Loading and errors', 'Reading a file is usually instant; the spinner shows for large files. File errors say what happened and how to fix it; the paste box stays available as a fallback.')

P.frame('S16-loading', 'Reading a file', phone(screen(
    f'''<div>{heading()}</div>
    {tabs(count=0)}
    <div class="flex h-80 items-center justify-center rounded-control border border-input bg-card" aria-busy="true">{spinner_line("Reading book-club.txt…")}</div>''',
    bottom('Continue', disabled=True))))


def error_body(title, body, ic):
    return f'''<div>{heading()}</div>
    {tabs(count=0)}
    {alert('error', title, body, '', ic=ic)}
    <div>{textarea([], 9, placeholder='Type or paste, one item per line')}{count_line('0 items', main_cls='text-label text-muted-foreground')}</div>
    {btn('Choose another file', 'secondary', 'file-up', extra='w-full', action='choose-file')}'''


P.frame('S16-error-empty-file', 'Error: the file is empty', phone(screen(
    error_body('reading-list.txt is empty', 'Choose another file or paste your list.', 'file-x'),
    bottom('Continue', disabled=True))))
P.frame('S16-error-unreadable', 'Error: the file can’t be read', phone(screen(
    error_body('book-club.docx can’t be read', 'Save it as plain text (.txt) and try again.', 'file-warning'),
    bottom('Continue', disabled=True))))

# ------------------------------------------------------------------ accessibility
P.section('Accessibility', 'At 200% text the box keeps at least 6 visible lines and the page scrolls; the count and the file button stay below the box.')
large_bar = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="{CLOSE}" class="flex size-12 items-center justify-center rounded-full" aria-label="Close import" data-action="close">{icon("x", "size-7")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">Import</h1>
  </header>
  <div class="shrink-0 px-gutter pb-3"><p class="text-title-3">Select items</p><p class="text-body-lg text-muted-foreground">Step 2 of 4</p>
    <div class="mt-2 flex gap-1" role="progressbar" aria-valuenow="2" aria-valuemin="1" aria-valuemax="4" aria-label="Step 2 of 4, Select items"><span class="h-1.5 flex-1 rounded-full bg-primary"></span><span class="h-1.5 flex-1 rounded-full bg-primary"></span><span class="h-1.5 flex-1 rounded-full bg-muted"></span><span class="h-1.5 flex-1 rounded-full bg-muted"></span></div></div>'''
P.frame('S16-large-text', 'Large text (200%)', phone(f'''{large_bar}
  <div class="min-h-0 flex-1 overflow-hidden">
    <div class="space-y-4 px-gutter pb-6 pt-1">
    <div>{heading(True)}</div>
    {tabs(large=True)}
    <div>{textarea(BOOKS[:7], 7, large=True)}<div class="mt-2" role="status"><span class="text-title-2 tabular-nums">12 items</span></div></div>
    {btn('Open a .txt file', 'outline', 'file-up', size='min-h-16', extra='w-full text-title-3 font-normal').replace(' text-label-lg ', ' ')}
    </div>
  </div>
  <div class="shrink-0 border-t bg-background px-gutter pb-4 pt-3"><a href="{NEXT}" class="flex min-h-16 w-full items-center justify-center rounded-control bg-primary px-6 text-title-3 text-primary-foreground" data-action="continue">Continue</a></div>'''))

# ------------------------------------------------------------------ platforms
P.section('iOS and web', 'iOS: 44 pt bar with a back chevron to the source picker (edge swipe goes back) and close at the right; “Open a .txt file” opens the Files app. Web: the file opens with the browser’s file picker; on desktop the user can also drop a file on the page.')
ios_bar = modal_bar('Import', CLOSE, ios=True, back=('Choose source', 'S11-source-picker.html#S11-default'))
P.frame('S16-ios', 'iOS', phone(screen(default_body(rows=13), bottom('Continue', NEXT, 'continue'), bar=ios_bar), ios=True))

drop = f'''<div class="flex flex-col items-center rounded-tile border-2 border-dashed border-input px-4 py-5 text-center">
      {icon("file-up", "size-6 text-muted-foreground")}
      <p class="mt-2 text-body">Drop a .txt file here, or <button class="inline-flex min-h-touch items-center text-primary underline underline-offset-4">browse</button></p>
      <p class="text-caption text-muted-foreground">Plain text, UTF-8, up to 5,000 lines</p>
    </div>'''
web_body = default_body(rows=8, after=drop)
P.frame('S16-web-desktop', 'Web, desktop: paste or drop a file', desktop(screen(web_body, bottom('Continue', NEXT, 'continue')), 'swipesort.app/import/text'))

P.write('S16-plain-text.html')
