# Usage: python3 tools/generators/S25-sorting.py design/03-screens/S25-sorting.html
# Generates design/03-screens/S25-sorting.html (static mockup frames).
import sys
OUT = sys.argv[1]
IMG = '../02-data/images/'

def icon(name, size='size-5', extra=''):
    return f'<i class="i-lucide-{name} {size} {extra}" aria-hidden="true"></i>'.replace('  ', ' ')

# ---------- card content per template ----------
def row(label, value, edited=False, wrap=False):
    ed = f'<span class="ml-1.5 inline-flex items-center align-middle text-muted-foreground" title="Edited">{icon("pencil-line", "size-3.5")}<span class="sr-only">, edited</span></span>' if edited else ''
    return f'<div class="flex gap-3"><dt class="w-16 shrink-0 text-muted-foreground">{label}</dt><dd class="min-w-0 {"" if wrap else "truncate"} tabular-nums">{value}{ed}</dd></div>'

PEOPLE = {
    'c077': dict(name='Mia Andersson', sub='Colleague', photo='people/c077.svg', rows=[('Phone', '+46 8 0000 4021'), ('Email', 'mia.andersson@example.com'), ('City', 'Stockholm')], tags=["Bride's"]),
    'c078': dict(name='Anna-Katharina Rosenthal-Brückner', sub='Colleague', photo='people/c078.svg', rows=[('Phone', '+43 1 0000 4117'), ('Email', 'anna-katharina.rosenthal-bruckner@example.com'), ('City', 'Vienna')], tags=["Bride's"]),
    'c081': dict(name='Fatma Güler', sub='Family', photo=None, initials='FG', rows=[('Phone', '+90 500 000 51 38'), ('Email', 'fatma.guler@example.com'), ('City', 'Ankara')], tags=["Groom's"]),
    'c080': dict(name='Dr. Hülya Öztürk (dentist)', sub='Friend', photo=None, initials='HÖ', rows=[('Phone', '+90 500 000 97 25', False, 2), ('City', 'İstanbul')], tags=["Bride's"], note=('Dentist, not sure why she is in my contacts list.', True)),
    'c014': dict(name='Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein', sub='Friend', photo='people/c014.svg', rows=[('Email', 'maximiliane.hohenberg-lichtenstein@example.net'), ('City', 'Berlin')], tags=["Bride's"], note=('Flying in from Berlin. Ask about dates first.', False)),
    'c045': dict(name='Alper Turan', sub='Friend', photo='people/c045.svg', rows=[('Phone', '+90 500 000 07 64'), ('Email', 'alper.turan@example.com'), ('City', 'Ankara', True)], tags=["Groom's"]),
}

def initials_block(txt, h=None):
    return f'<div class="px-6 pt-7"><span class="flex size-24 items-center justify-center rounded-full bg-muted text-title-1 text-muted-foreground" aria-hidden="true">{txt}</span></div>'

def person_body(p, note=None, compact=False):
    img = f'<img src="{IMG}{p["photo"]}" alt="" class="h-[46%] w-full object-cover">' if p.get('photo') else initials_block(p['initials'])
    rows = ''
    for r in p['rows']:
        label, value = r[0], r[1]
        edited = len(r) > 2 and r[2] is True
        extra = r[3] if len(r) > 3 else 0
        if extra:
            value = f'{value} <span class="text-muted-foreground">+{extra - 1}</span>'
        rows += row(label, value, edited)
    n = note or p.get('note')
    note_html = ''
    if n:
        text, private = n
        note_html = f'<p class="flex items-center gap-2 text-body-sm text-muted-foreground">{icon("lock" if private else "sticky-note", "size-4 shrink-0")}<span class="truncate">{text}</span></p>'
    tags = ''.join(f'<span class="inline-flex h-7 items-center rounded-full bg-secondary px-2.5 text-caption text-secondary-foreground">{t}</span>' for t in p['tags'])
    return f'''{img}
      <div class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-5">
        <h2 class="line-clamp-4 text-card-title">{p["name"]}</h2>
        <p class="mt-1 text-body-lg text-muted-foreground">{p["sub"]}</p>
        <dl class="mt-4 space-y-2 text-body">{rows}</dl>
        <div class="mt-auto space-y-3 pt-3">{note_html}<div class="flex gap-2">{tags}</div></div>
      </div>'''

def product_body():
    return f'''<img src="{IMG}products/p03.svg" alt="" class="h-[46%] w-full object-cover">
      <div class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-5">
        <h2 class="line-clamp-3 text-card-title">27-inch 4K USB-C monitor</h2>
        <p class="mt-1 text-body-lg text-muted-foreground">Pixelhaus</p>
        <div class="mt-4 flex items-baseline justify-between"><span class="text-title-1 tabular-nums">€429</span><span class="inline-flex items-center gap-1 text-body">{icon("star", "size-4")}4.5 <span class="text-muted-foreground">(2,870)</span></span></div>
        <div class="mt-auto flex gap-2 pt-3"><span class="inline-flex h-7 items-center rounded-full bg-secondary px-2.5 text-caption text-secondary-foreground">Monitor</span></div>
      </div>'''

def photo_body():
    return f'''<img src="{IMG}photos/ph13.svg" alt="Photo IMG_2053.JPG" class="min-h-0 w-full flex-1 object-cover">
      <div class="px-6 pb-5 pt-4">
        <h2 class="text-title-2">Mar 7, 2026, 10:24</h2>
        <p class="mt-1 text-body text-muted-foreground">Alfama, Lisbon</p>
        <p class="mt-1 text-body-sm text-muted-foreground">IMG_2053.JPG, 3.3 MB</p>
      </div>'''

def candidate_body():
    # Sparse-card rule (S23 §3, D-S23-8): no image area -> title, subtitle and rows form one block,
    # vertically centered above the pinned tags; templates with up to 3 rows use text-title-2 values.
    return f'''<div class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-7">
        <div class="my-auto">
          <h2 class="line-clamp-3 text-card-title">Lena Hoffmann</h2>
          <p class="mt-1 text-body-lg text-muted-foreground">Berlin</p>
          <dl class="mt-6 space-y-5">
            <div class="flex flex-col"><dt class="text-body-sm text-muted-foreground">Years of experience</dt><dd class="text-title-2 tabular-nums">6</dd></div>
            <div class="flex flex-col"><dt class="text-body-sm text-muted-foreground">Expected salary</dt><dd class="text-title-2 tabular-nums">€78,000</dd></div>
          </dl>
        </div>
        <div class="flex gap-2 pt-3"><span class="inline-flex h-7 items-center rounded-full bg-secondary px-2.5 text-caption text-secondary-foreground">Referral</span></div>
      </div>'''

STAMP = {
    'accept': ('left-5 top-6 -rotate-6', 'check', 'Accept'),
    'reject': ('right-5 top-6 rotate-6', 'x', 'Reject'),
    'maybe': ('bottom-16 left-1/2 -translate-x-1/2', 'circle-help', 'Maybe'),
}
MOVE = {
    ('accept', 'half'): 'translate-x-12 rotate-3', ('accept', 'armed'): 'translate-x-28 rotate-6',
    ('reject', 'half'): '-translate-x-12 -rotate-3', ('reject', 'armed'): '-translate-x-28 -rotate-6',
    ('maybe', 'half'): '-translate-y-5', ('maybe', 'armed'): '-translate-y-10',
}

def card(body, label, drag=None, level='armed', others=None, reduced=False):
    move = '' if not drag or reduced else MOVE[(drag, level)]
    shadow = 'shadow-hero-drag' if drag else 'shadow-hero'
    overlay = ''
    if drag:
        pos, ic, txt = STAMP[drag]
        op = 'opacity-25' if level == 'armed' else 'opacity-10'
        sop = '' if level == 'armed' else 'scale-90'
        overlay = f'''<div class="pointer-events-none absolute inset-0 bg-{drag} {op}"></div>
      <div class="pointer-events-none absolute {pos} {sop} inline-flex h-11 items-center gap-2 rounded-full bg-{drag} px-4 text-label-lg text-{drag}-foreground shadow-overlay">{icon(ic, "size-6")}{txt}</div>'''
    oth = ''
    if others:
        oth = f'<div class="absolute right-4 top-4 w-48 rounded-control bg-card px-2.5 py-2 shadow-raised">{others}</div>'
    return f'''<article class="absolute inset-x-gutter bottom-5 top-0 flex origin-bottom flex-col overflow-hidden rounded-hero bg-card {shadow} {move}" aria-label="{label}" aria-roledescription="card" tabindex="0">
      {body}
      {oth}
      {overlay}
    </article>'''

NEXT_BODY = None
def stack(top, nxt=True, promote=False, nxt_body=None, z=''):
    nc = 'inset-x-gutter bottom-5 top-0 origin-top scale-95 translate-y-10' if not promote else 'inset-x-gutter bottom-5 top-0 origin-top scale-[.975] translate-y-5'
    body = nxt_body or NEXT_BODY or ''
    behind = f'<div class="absolute {nc} flex flex-col overflow-hidden rounded-hero border bg-card shadow-raised" aria-hidden="true">{body}</div>' if nxt else ''
    return f'''<div class="relative mx-0 mt-2 min-h-0 flex-1 {z}">
    {behind}
    {top}
  </div>'''

def header(title='Wedding guests', sub='Round 1', close_label='Close sorting', ios=False):
    if ios:
        return f'''<header class="grid h-11 shrink-0 grid-cols-[auto_1fr_auto] items-center px-2">
    <button class="flex size-12 items-center justify-center rounded-full text-primary" aria-label="{close_label}">{icon("x", "size-6")}</button>
    <div class="min-w-0 text-center"><h1 class="truncate text-body font-semibold">{title}</h1><p class="text-caption text-muted-foreground">{sub}</p></div>
    <button class="flex size-12 items-center justify-center rounded-full text-primary" aria-label="More options">{icon("ellipsis", "size-6")}</button>
  </header>'''
    return f'''<header class="flex h-app-bar shrink-0 items-center gap-1 px-1">
    <a href="S09-list-overview.html#S09-default" class="flex size-12 items-center justify-center rounded-full" aria-label="{close_label}" data-action="close">{icon("x", "size-6")}</a>
    <div class="min-w-0 flex-1 px-1"><h1 class="truncate text-title-3">{title}</h1><p class="text-caption text-muted-foreground">{sub}</p></div>
    <button class="flex size-12 items-center justify-center rounded-full" aria-label="More options" data-action="menu">{icon("ellipsis-vertical", "size-6")}</button>
  </header>'''

def progress(done=76, total=100, extra=''):
    pct = round(done * 100 / total)
    return f'''<div class="shrink-0 px-gutter pb-1">
    <div class="flex items-center justify-between gap-3"><span class="text-label tabular-nums">{done} / {total} decided</span>{extra}</div>
    <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="{done}" aria-valuemin="0" aria-valuemax="{total}" aria-label="{done} of {total} decided"><div class="h-full w-[{pct}%] rounded-full bg-primary"></div></div>
  </div>'''

def dbtn(kind, count, state='rest', large=False):
    ic = {'accept': 'check', 'reject': 'x', 'maybe': 'circle-help'}[kind]
    lab = {'accept': 'Accept', 'reject': 'Reject', 'maybe': 'Maybe'}[kind]
    past = {'accept': 'accepted', 'reject': 'rejected', 'maybe': 'maybe'}[kind]
    cls = {
        'rest': f'bg-{kind}-soft text-{kind}-soft-foreground',
        'half': f'bg-{kind}-soft text-{kind}-soft-foreground ring-2 ring-{kind}/40',
        'armed': f'bg-{kind} text-{kind}-foreground ring-4 ring-{kind}/25',
    }[state]
    cnt = f' <span class="tabular-nums text-muted-foreground">{count}</span>' if count is not None else ''
    lbl = 'text-label' if large else 'text-caption'
    return f'<button class="flex min-w-touch flex-col items-center gap-1.5" aria-label="{lab}, {count} {past}" data-action="{kind}"><span class="flex size-16 items-center justify-center rounded-full {cls}">{icon(ic, "size-7")}</span><span class="{lbl} text-center">{lab}{cnt}</span></button>'

def bar(counts=(17, 11, 48), armed=None, level='armed', undo=True, large=False, note_label='Note', undo_label='Undo last decision (Accept on Ayşe Demir)'):
    r, m, a = counts
    st = lambda k: (level if armed == k else 'rest')
    lbl = 'text-label' if large else 'text-caption'
    uattr = '' if undo else ' disabled'
    uop = '' if undo else ' opacity-40'
    return f'''<div class="flex shrink-0 items-start justify-between px-5 pb-4 pt-2">
    <button class="flex min-w-touch flex-col items-center gap-1.5{uop}" aria-label="{undo_label if undo else "Nothing to undo"}" data-action="undo"{uattr}><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("undo-2")}</span><span class="{lbl} text-muted-foreground">Undo</span></button>
    {dbtn('reject', r, st('reject'), large)}
    {dbtn('maybe', m, st('maybe'), large)}
    {dbtn('accept', a, st('accept'), large)}
    <button class="flex min-w-touch flex-col items-center gap-1.5" aria-label="Add note" data-action="note"><span class="flex size-12 items-center justify-center rounded-full border border-input bg-card">{icon("sticky-note")}</span><span class="{lbl} text-muted-foreground">{note_label}</span></button>
  </div>'''

def snackbar(text, action=None, bottom='bottom-32', role='status', icon_name=None):
    act = f'<button class="-my-1 inline-flex h-12 items-center rounded-sm px-3 text-label text-primary-inverse">{action}</button>' if action else ''
    ic = icon(icon_name, 'size-5 shrink-0') if icon_name else ''
    pad = 'py-1.5 pl-4 pr-1.5' if action else 'px-4 py-3'
    return f'<div class="absolute inset-x-4 {bottom} z-10 flex min-h-12 items-center gap-3 rounded-control bg-foreground {pad} text-background shadow-overlay" role="{role}">{ic}<span class="flex-1 text-body-sm">{text}</span>{act}</div>'

def phone(content, ios=False):
    cls = 'phone-ios' if ios else 'phone'
    return f'''<div class="{cls}">
  <div class="sysbar-top" aria-hidden="true"><span>9:41</span><span class="sysbar-icons"></span></div>
  <div class="screen">
  {content}
  </div>
  <div class="sysbar-nav" aria-hidden="true"></div>
</div>'''

def web_phone(content):
    return f'''<div class="phone">
  <div class="screen">
  {content}
  </div>
</div>'''

def frame(fid, label, inner):
    return f'''
<figure class="frame" data-frame="{fid}" id="{fid}">
  <figcaption class="frame-label">S25 · {label} · <span class="theme-name"></span></figcaption>
  {inner}
</figure>'''

def section(title, desc):
    return f'</main>\n<h2 class="mock-section">{title}</h2>\n<p>{desc}</p>\n<main class="mock-canvas">'

MIA = person_body(PEOPLE['c077'])
annak = person_body(PEOPLE['c078'])
NEXT_BODY = annak
MIA_L = 'Mia Andersson, Colleague. Phone +46 8 0000 4021. Email mia.andersson@example.com. City Stockholm.'

def sorting(body=MIA, label=MIA_L, drag=None, level='armed', counts=(17, 11, 48), done=76, others=None, extra_top='', overlay='', hdr=None, prog=None, promote=False, reduced=False, undo=True, nxt=True, barhtml=None, nxt_body=None, undo_label='Undo last decision (Accept on Ayşe Demir)'):
    return f'''{hdr or header()}
  {extra_top}
  {prog or progress(done)}
  {stack(card(body, label, drag, level, others, reduced), nxt, promote, nxt_body=nxt_body)}
  {barhtml or bar(counts, drag, level, undo, undo_label=undo_label)}
  {overlay}'''

frames = []
F = lambda *a: frames.append(frame(*a))

# ----- Core -----
frames.append(section('Sorting', 'The card stack with progress, decision buttons and counts. Gestures: right Accept, left Reject, up Maybe. Values in motion.md §2.'))
F('S25-default', 'Default (solo list)', phone(sorting()))
F('S25-drag-accept-start', 'Dragging right, below threshold', phone(sorting(drag='accept', level='half', promote=False)))
F('S25-drag-accept', 'Dragging right, armed: release to accept', phone(sorting(drag='accept', promote=True)))
F('S25-drag-reject', 'Dragging left, armed: release to reject', phone(sorting(drag='reject', promote=True)))
F('S25-drag-maybe', 'Dragging up, armed: release for maybe', phone(sorting(drag='maybe', promote=True)))
# commit: top card flying out right, next card promoted (Anna-Katharina), counts updated
annak = person_body(PEOPLE['c078'])
commit_card = f'''<div class="relative mt-2 min-h-0 flex-1">
    <div class="absolute inset-x-gutter bottom-5 top-0 flex origin-top scale-95 translate-y-10 flex-col overflow-hidden rounded-hero border bg-card shadow-raised" aria-hidden="true">{person_body(PEOPLE['c081'])}</div>
    {card(annak, 'Anna-Katharina Rosenthal-Brückner, Colleague. Phone +43 1 0000 4117. City Vienna.')}
    <div class="pointer-events-none absolute inset-x-gutter bottom-12 top-0 translate-x-full rotate-12 overflow-hidden rounded-hero bg-card opacity-90 shadow-hero-drag" aria-hidden="true"><img src="{IMG}people/c077.svg" alt="" class="h-[46%] w-full object-cover"><div class="absolute inset-0 bg-accept opacity-25"></div></div>
  </div>'''
F('S25-commit', 'Committed: card leaves, next card rises, count ticks', phone(f'''{header()}
  {progress(77)}
  {commit_card}
  {bar((17, 11, 49), 'accept', 'armed', undo_label='Undo last decision (Accept on Mia Andersson)')}'''))
F('S25-undo', 'Undo: last card returns, snackbar confirms', phone(sorting(overlay=snackbar('Undid Accept on Mia Andersson'), undo_label=None) if False else sorting(overlay=snackbar('Undid Accept on Mia Andersson'))))

# ----- Coach marks -----
frames.append(section('First-time coach marks', 'Shown on the first sort only. The card demonstrates each gesture (static arrows with reduced motion). Skip ends the tutorial; it can be replayed from the menu.'))
def coach(step, title, body, ic, tone, drag, last=False):
    dots = ''.join(f'<span class="size-2 rounded-full {"bg-primary" if i == step else "bg-muted-foreground/30"}"></span>' for i in range(1, 5))
    nxt_btn = (f'<a href="../04-prototype/swipe-demo.html?deck=first&amp;count=6&amp;next=S27-first-round" class="inline-flex h-12 items-center rounded-control bg-primary px-5 text-label-lg text-primary-foreground" data-action="done">Start sorting</a>' if last
               else f'<a href="#S25-coach-{step + 1}" class="inline-flex h-12 items-center rounded-control bg-primary px-5 text-label-lg text-primary-foreground" data-action="next">Next</a>')
    skip = '' if last else '<a href="#S25-default" class="inline-flex h-12 items-center rounded-control px-4 text-label-lg" data-action="skip">Skip</a>'
    hand = ''
    if drag:
        pos = {'accept': 'right-10 top-1/2', 'reject': 'left-10 top-1/2', 'maybe': 'left-1/2 top-24 -translate-x-1/2'}[drag]
        arrow = {'accept': 'arrow-right', 'reject': 'arrow-left', 'maybe': 'arrow-up'}[drag]
        hand = f'<div class="pointer-events-none absolute {pos} z-30 flex size-14 items-center justify-center rounded-full bg-popover text-foreground shadow-overlay" aria-hidden="true">{icon(arrow, "size-7")}</div>'
    tone_cls = f'bg-{tone}-soft text-{tone}-soft-foreground' if tone else 'bg-primary-soft text-primary-soft-foreground'
    bubble = f'''<div class="absolute inset-x-4 bottom-6 z-30 rounded-dialog bg-popover p-5 shadow-dialog" role="dialog" aria-modal="true" aria-labelledby="cm{step}">
      <div class="flex items-center gap-3"><span class="flex size-10 shrink-0 items-center justify-center rounded-full {tone_cls}">{icon(ic)}</span><p id="cm{step}" class="text-title-3">{title}</p></div>
      <p class="mt-2 text-body text-muted-foreground">{body}</p>
      <div class="mt-4 flex items-center justify-between"><span class="flex gap-1.5" role="img" aria-label="Step {step} of 4">{dots}</span><span class="flex gap-1">{skip}{nxt_btn}</span></div>
    </div>'''
    scrim = '<div class="absolute inset-0 z-10 bg-scrim/60"></div>'
    return phone(f'''{header()}
  {progress(0, 85)}
  {stack(card(MIA, MIA_L, drag, 'half' if drag else 'armed'), True, z='z-20')}
  {bar((0, 0, 0), drag, 'half', undo=False)}
  {scrim}{hand}{bubble}''')
F('S25-coach-1', 'Coach mark 1 of 4: accept', coach(1, 'Swipe right to accept', 'Or tap the check button below the card.', 'arrow-right', 'accept', 'accept'))
F('S25-coach-2', 'Coach mark 2 of 4: reject', coach(2, 'Swipe left to reject', 'Or tap the cross button.', 'arrow-left', 'reject', 'reject'))
F('S25-coach-3', 'Coach mark 3 of 4: maybe', coach(3, 'Swipe up for maybe', 'Not sure yet? Maybe items wait in their own pile, so you can sort them again later.', 'arrow-up', 'maybe', 'maybe'))
F('S25-coach-4', 'Coach mark 4 of 4: details and undo', coach(4, 'Tap the card for details', 'Undo is always one tap away. Your progress saves as you go.', 'hand', None, None, last=True))

# ----- Notes, menu -----
frames.append(section('Notes and menu', 'Add or edit a note without leaving the stack. Tap the card to open item details (S26).'))
note_sheet = f'''<div class="absolute inset-0 z-10 bg-scrim/50"></div>
  <div class="absolute inset-x-0 bottom-0 z-20 rounded-t-sheet bg-popover px-gutter pb-6 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="ns1">
    <div class="flex justify-center py-1.5"><span class="h-1 w-8 rounded-full bg-muted-foreground/40"></span></div>
    <div class="flex items-center justify-between pt-2"><h2 id="ns1" class="text-title-3">Note on Mia Andersson</h2><button class="-mr-3 flex size-12 items-center justify-center rounded-full" aria-label="Close">{icon("x")}</button></div>
    <label for="note-mia" class="sr-only">Note</label>
    <textarea id="note-mia" rows="4" class="mt-3 w-full resize-none rounded-control border border-primary bg-card px-3.5 py-3 text-body ring-2 ring-ring/30">Met her at the Stockholm offsite. Ask if she can travel in June.</textarea>
    <div class="mt-1 flex justify-end"><span class="text-caption tabular-nums text-muted-foreground">62 / 1,000</span></div>
    <button class="mt-4 flex h-12 w-full items-center justify-center rounded-control bg-primary text-label-lg text-primary-foreground" data-action="save-note">Save note</button>
  </div>'''
F('S25-note', 'Note sheet (solo list)', phone(sorting(overlay=note_sheet)))
mia_noted = person_body(PEOPLE['c077'], note=('Met her at the Stockholm offsite. Ask if she can travel in June.', False))
F('S25-note-saved', 'Note saved and shown on the card', phone(sorting(body=mia_noted, overlay=snackbar('Note saved'))))
menu = f'''<div class="absolute right-2 top-14 z-20 w-72 overflow-hidden rounded-control bg-popover py-1.5 shadow-overlay" role="menu" aria-label="Sorting options">
    <a href="S22-template-library.html#S22-change" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body">{icon("layout-template", "size-5 text-muted-foreground")}Card template</a>
    <a href="#S25-coach-1" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body">{icon("graduation-cap", "size-5 text-muted-foreground")}Show the tutorial again</a>
    <a href="S26-item-detail.html#S26-default" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body">{icon("panel-bottom-open", "size-5 text-muted-foreground")}Open item details</a>
    <div class="my-1.5 h-px bg-border"></div>
    <a href="S40-global-patterns.html#S40-end-round" role="menuitem" class="flex h-12 items-center gap-3 px-4 text-body">{icon("flag", "size-5 text-muted-foreground")}End round</a>
  </div>'''
F('S25-menu', 'Overflow menu (solo list)', phone(sorting(overlay=menu)))

# ----- Shared -----
frames.append(section('Shared list', "Every member decides independently. Others' decisions are hidden by default to avoid bias; each member can turn them on from the menu."))
members = f'''<div class="flex -space-x-2" role="img" aria-label="3 members: Deniz, Mert, Selin"><img src="{IMG}people/u-deniz.svg" alt="" class="size-6 rounded-full ring-2 ring-background"><img src="{IMG}people/u-mert.svg" alt="" class="size-6 rounded-full ring-2 ring-background"><span class="flex size-6 items-center justify-center rounded-full bg-muted text-caption text-muted-foreground ring-2 ring-background">S</span></div>'''
shared_hdr = header('Wedding guests', 'Round 1, shared')
F('S25-shared', "Shared list, others' decisions hidden (default)", phone(sorting(hdr=shared_hdr, prog=progress(76, 100, members))))
others = f'''<div class="space-y-1.5" role="img" aria-label="Mert: Maybe. Selin: not decided yet.">
    <div class="flex items-center gap-2"><img src="{IMG}people/u-mert.svg" alt="" class="size-6 rounded-full"><span class="text-caption">Mert</span><span class="ml-auto inline-flex h-6 items-center gap-1 rounded-full bg-maybe-soft px-2 text-caption text-maybe-soft-foreground">{icon("circle-help", "size-3.5")}Maybe</span></div>
    <div class="flex items-center gap-2"><span class="flex size-6 items-center justify-center rounded-full bg-muted text-caption text-muted-foreground">SY</span><span class="text-caption">Selin</span><span class="ml-auto inline-flex h-6 items-center gap-1 rounded-full bg-muted px-2 text-caption text-muted-foreground">{icon("circle-dashed", "size-3.5")}Not decided</span></div>
  </div>'''
F('S25-shared-others', "Shared list, others' decisions shown on the card", phone(sorting(hdr=shared_hdr, prog=progress(76, 100, members), others=others)))
shared_menu = menu.replace('<a href="S22-template-library.html#S22-change"', f'''<div role="menuitemcheckbox" aria-checked="true" class="flex min-h-12 items-center gap-3 px-4 py-2 text-body">{icon("eye", "size-5 shrink-0 text-muted-foreground")}<span class="flex-1">Show others' decisions</span><span class="flex h-8 w-13 shrink-0 items-center rounded-full bg-primary p-1" aria-hidden="true"><span class="ml-auto size-6 rounded-full bg-primary-foreground"></span></span></div>
    <a href="S22-template-library.html#S22-change"''', 1).replace('S40-global-patterns.html#S40-end-round"', 'S40-global-patterns.html#S40-end-round-shared"')
F('S25-shared-menu', "Shared list menu with the others' decisions switch", phone(sorting(hdr=shared_hdr, prog=progress(76, 100, members), overlay=shared_menu)))
F('S25-shared-conflict', 'After deciding: new conflict revealed', phone(sorting(body=annak, label='Anna-Katharina Rosenthal-Brückner', hdr=shared_hdr, prog=progress(77, 100, members), counts=(18, 11, 48), nxt_body=person_body(PEOPLE['c081']), undo_label='Undo last decision (Reject on Mia Andersson)',
    overlay=snackbar('Mert chose Maybe on Mia Andersson. This is now a conflict.', 'View', icon_name='git-compare-arrows'))))
F('S25-web-desktop-shared', 'placeholder', '')  # replaced below (kept for ID order)
frames.pop()

# ----- Templates (any kind of list) -----
frames.append(section('Any kind of list', 'The card follows the list\'s card template. No domain words in the interface: the same screen sorts products, photos and candidates.'))
F('S25-product', 'Product template (Desk setup)', phone(sorting(body=product_body(), label='27-inch 4K USB-C monitor, Pixelhaus, 429 euros, rated 4.5', hdr=header('Desk setup', 'Round 1'), prog=progress(2, 20), counts=(0, 0, 2))))
F('S25-photo', 'Photo template (March photos clean-up)', phone(sorting(body=photo_body(), label='Photo IMG_2053.JPG, taken Mar 7, 2026 in Alfama, Lisbon', hdr=header('March photos clean-up', 'Round 1'), prog=progress(12, 30), counts=(6, 1, 5))))
F('S25-candidate', 'Custom template "Candidate, compact"', phone(sorting(body=candidate_body(), label='Lena Hoffmann, Berlin. 6 years of experience. Expected salary 78,000 euros.', hdr=header('Frontend hiring, Q4', 'Round 1'), prog=progress(0, 12), counts=(0, 0, 0), undo=False)))

# ----- Content edge cases -----
frames.append(section('Content edge cases', 'Long text clamps on the card and shows in full in details. Missing values are left out. Edited values carry a marker.'))
F('S25-long-text', 'Very long name, missing phone, note', phone(sorting(body=person_body(PEOPLE['c014']), label='Maximiliane Alexandra Charlotte von Hohenberg-Lichtenstein, Friend', done=13, counts=(2, 3, 8))))
F('S25-no-photo', 'No photo: initials', phone(sorting(body=person_body(PEOPLE['c081']), label='Fatma Güler, Family. Phone +90 500 000 51 38. City Ankara.', done=80, counts=(18, 12, 50))))
F('S25-edited', 'Edited field (city changed from İstanbul)', phone(sorting(body=person_body(PEOPLE['c045']), label='Alper Turan, Friend. Phone +90 500 000 07 64. City Ankara, edited.', done=44, counts=(8, 6, 30))))

# ----- States -----
frames.append(section('States', 'Loading, offline, errors, the last card and resuming.'))
loading = f'''{header()}
  <div class="shrink-0 px-gutter pb-1" aria-busy="true"><span class="block h-4 w-32 animate-pulse rounded-full bg-muted"></span><div class="mt-2 h-1.5 rounded-full bg-muted"></div></div>
  <div class="relative mt-2 min-h-0 flex-1" role="status" aria-busy="true" aria-label="Loading cards">
    <div class="absolute inset-x-gutter bottom-4 top-0 flex flex-col overflow-hidden rounded-hero bg-card shadow-hero">
      <div class="h-[46%] animate-pulse bg-muted"></div>
      <div class="space-y-3 px-6 pt-6"><span class="block h-7 w-3/4 animate-pulse rounded-full bg-muted"></span><span class="block h-4 w-1/3 animate-pulse rounded-full bg-muted"></span><span class="block h-4 w-2/3 animate-pulse rounded-full bg-muted"></span><span class="block h-4 w-1/2 animate-pulse rounded-full bg-muted"></span></div>
    </div>
  </div>
  {bar((0, 0, 0), undo=False).replace('<button class="flex min-w-touch', '<button disabled class="opacity-40 flex min-w-touch')}'''
F('S25-loading', 'Loading', phone(loading))
offline_banner = f'<div class="flex shrink-0 items-center gap-2 bg-muted px-gutter py-2 text-body-sm" role="status">{icon("wifi-off", "size-4 shrink-0")}<span class="flex-1">You\'re offline. Decisions are saved on this phone.</span></div>'
F('S25-offline', 'Offline: sorting continues, saved locally', phone(sorting(hdr=shared_hdr, extra_top=offline_banner, prog=progress(76, 100, f'<span class="inline-flex items-center gap-1.5 text-caption text-muted-foreground">{icon("cloud-off", "size-4")}4 not synced</span>'))))
F('S25-syncing', 'Back online: syncing', phone(sorting(hdr=shared_hdr, prog=progress(80, 100, f'<span class="inline-flex items-center gap-1.5 text-caption text-muted-foreground" role="status">{icon("refresh-cw", "size-4 animate-spin")}Syncing 4 decisions…</span>'), counts=(18, 12, 50))))
error = f'''{header()}
  <div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
    {icon("triangle-alert", "size-8 text-muted-foreground")}
    <h2 class="mt-4 text-balance text-title-3">This list couldn't be opened</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">Your decisions are safe. Close the list and open it again. If it keeps happening, restart SwipeSort.</p>
    <button class="mt-6 flex h-12 w-full max-w-xs items-center justify-center rounded-control bg-secondary text-label-lg text-secondary-foreground">Try again</button>
    <a href="S09-list-overview.html#S09-default" class="mt-2 flex h-12 w-full max-w-xs items-center justify-center rounded-control text-label-lg">Back to list</a>
  </div>'''
F('S25-error', 'Error: list could not be opened', phone(error))
last = person_body(PEOPLE['c080'])
F('S25-last-card', 'Last card, several phone numbers, private note', phone(sorting(body=last, label='Dr. Hülya Öztürk (dentist), Friend. Phone +90 500 000 97 25 and 1 more. City İstanbul. Private note.', done=99, counts=(23, 13, 63), nxt=False)))
resume = f'''{header()}
  {progress(76)}
  <div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
    <span class="flex size-14 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon("play", "size-6")}</span>
    <h2 class="mt-4 text-balance text-title-2">Pick up where you left off</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">76 of 100 decided. 24 items left in Round 1.</p>
    <a href="#S25-default" class="mt-6 flex h-12 w-full max-w-xs items-center justify-center rounded-control bg-primary text-label-lg text-primary-foreground" data-action="continue">Continue sorting</a>
  </div>'''
F('S25-resume', 'Resume prompt (only after an app update or a sync from another device)', phone(resume))
done_state = f'''{header()}
  {progress(100)}
  <div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
    <span class="flex size-14 items-center justify-center rounded-full bg-accept-soft text-accept-soft-foreground">{icon("check-check", "size-6")}</span>
    <h2 class="mt-4 text-balance text-title-2">Every item is decided</h2>
    <p class="mt-1 max-w-xs text-balance text-body text-muted-foreground">Round 1 is complete. See the summary or change any decision in Results.</p>
    <a href="S27-round-summary.html#S27-default" class="mt-6 flex h-12 w-full max-w-xs items-center justify-center rounded-control bg-primary text-label-lg text-primary-foreground" data-action="summary">See summary</a>
  </div>'''
F('S25-nothing-left', 'Opening a round with nothing left to sort', phone(done_state))

# ----- Accessibility -----
frames.append(section('Accessibility', 'Large text, reduced motion and screen-reader actions. Every gesture has a visible button and a named action.'))
big_body = f'''<div class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-6">
        <h2 class="line-clamp-4 text-display">Mia Andersson</h2>
        <p class="mt-2 text-title-2 font-normal text-muted-foreground">Colleague</p>
        <dl class="mt-5 space-y-3 text-title-3 font-normal"><div><dt class="text-body-lg text-muted-foreground">Phone</dt><dd class="tabular-nums">+46 8 0000 4021</dd></div><div><dt class="text-body-lg text-muted-foreground">Email</dt><dd class="break-all">mia.andersson@example.com</dd></div><div><dt class="text-body-lg text-muted-foreground">City</dt><dd>Stockholm</dd></div></dl>
        <p class="mt-auto text-body-lg text-primary">1 more field in details</p>
      </div>'''
big_bar = f'''<div class="grid shrink-0 grid-cols-3 gap-2 px-4 pb-3 pt-2">
    <button class="flex min-h-16 flex-col items-center justify-center gap-1 rounded-control bg-reject-soft px-2 py-2 text-reject-soft-foreground" aria-label="Reject, 17 rejected" data-action="reject">{icon("x", "size-7")}<span class="text-title-3">Reject <span class="tabular-nums">17</span></span></button>
    <button class="flex min-h-16 flex-col items-center justify-center gap-1 rounded-control bg-maybe-soft px-2 py-2 text-maybe-soft-foreground" aria-label="Maybe, 11 maybe" data-action="maybe">{icon("circle-help", "size-7")}<span class="text-title-3">Maybe <span class="tabular-nums">11</span></span></button>
    <button class="flex min-h-16 flex-col items-center justify-center gap-1 rounded-control bg-accept-soft px-2 py-2 text-accept-soft-foreground" aria-label="Accept, 48 accepted" data-action="accept">{icon("check", "size-7")}<span class="text-title-3">Accept <span class="tabular-nums">48</span></span></button>
    <button class="col-span-3 flex h-12 items-center justify-center gap-2 rounded-control border border-input text-title-3 font-normal" aria-label="Undo last decision" data-action="undo">{icon("undo-2")}Undo</button>
  </div>'''
big_hdr = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <button class="flex size-12 items-center justify-center rounded-full" aria-label="Close sorting">{icon("x", "size-7")}</button>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">Wedding guests</h1>
    <button class="flex size-12 items-center justify-center rounded-full" aria-label="More options, including Add note">{icon("ellipsis-vertical", "size-7")}</button>
  </header>'''
big_prog = f'''<div class="shrink-0 px-gutter pb-1"><span class="text-title-3 tabular-nums">76 / 100 decided</span><div class="mt-2 h-2 overflow-hidden rounded-full bg-muted"><div class="h-full w-[76%] rounded-full bg-primary"></div></div></div>'''
F('S25-large-text', 'Large text (200%): image hidden, buttons become a labeled grid', phone(f'''{big_hdr}{big_prog}
  {stack(card(big_body, MIA_L), True)}
  {big_bar}'''))
F('S25-reduced-motion', 'Reduced motion: no tilt or fly-out, tint and stamp still show', phone(sorting(drag='accept', reduced=True)))
sr = f'''<div class="absolute inset-0 z-10 bg-scrim/50"></div>
  <div class="absolute inset-x-6 top-1/3 z-20 rounded-dialog bg-popover p-5 shadow-dialog" role="dialog" aria-labelledby="sr1">
    <p class="text-caption text-muted-foreground">Screen reader actions on the card (TalkBack: actions menu; VoiceOver: rotor)</p>
    <h2 id="sr1" class="mt-1 text-title-3">Mia Andersson</h2>
    <ul class="mt-3 divide-y text-body">
      <li class="flex h-12 items-center gap-3">{icon("check", "size-5 text-accept-soft-foreground")}Accept</li>
      <li class="flex h-12 items-center gap-3">{icon("x", "size-5 text-reject-soft-foreground")}Reject</li>
      <li class="flex h-12 items-center gap-3">{icon("circle-help", "size-5 text-maybe-soft-foreground")}Maybe</li>
      <li class="flex h-12 items-center gap-3">{icon("undo-2", "size-5")}Undo</li>
      <li class="flex h-12 items-center gap-3">{icon("sticky-note", "size-5")}Add note</li>
      <li class="flex h-12 items-center gap-3">{icon("panel-bottom-open", "size-5")}Open details</li>
    </ul>
    <p class="mt-3 text-body-sm text-muted-foreground">After an action: “Accepted Mia Andersson. 77 of 100 decided.”</p>
  </div>'''
F('S25-screen-reader', 'Screen-reader actions (annotation)', phone(sorting(overlay=sr, hdr=header().replace('class="flex h-app-bar', 'class="flex h-app-bar ring-2 ring-ring'))))

# ----- Platforms -----
frames.append(section('iOS and web', 'iOS: modal with a top bar and an iOS page sheet for notes; swipe-down to dismiss is off while sorting. Web: no haptics; desktop shows the phone layout centered with keyboard hints.'))
ios_screen = sorting(hdr=header(ios=True))
F('S25-ios', 'iOS', phone(ios_screen, ios=True))
ios_sheet = f'''<div class="absolute inset-0 z-10 bg-scrim/40"></div>
  <div class="absolute inset-x-0 bottom-0 top-16 z-20 rounded-t-sheet bg-popover px-5 pt-2 shadow-sheet" role="dialog" aria-modal="true" aria-labelledby="ins">
    <div class="flex justify-center py-1.5"><span class="h-1 w-9 rounded-full bg-muted-foreground/40"></span></div>
    <div class="grid grid-cols-[1fr_auto_1fr] items-center pt-1"><button class="inline-flex h-12 items-center justify-self-start px-1 text-body text-primary">Cancel</button><h2 id="ins" class="text-body font-semibold">Note</h2><button class="inline-flex h-12 min-w-12 items-center justify-end justify-self-end px-1 text-body font-semibold text-primary">Save</button></div>
    <p class="mt-5 text-label text-muted-foreground">Mia Andersson</p>
    <label for="note-ios" class="sr-only">Note</label>
    <textarea id="note-ios" rows="5" class="mt-2 w-full resize-none rounded-control border border-input bg-card px-3.5 py-3 text-body">Met her at the Stockholm offsite. Ask if she can travel in June.</textarea>
  </div>'''
F('S25-ios-note', 'iOS note as a page sheet', phone(sorting(hdr=header(ios=True), overlay=ios_sheet), ios=True))
F('S25-web', 'Web, mobile browser', web_phone(sorting(hdr=shared_hdr, prog=progress(76, 100, members))))
kbd = lambda k, t: f'<span class="inline-flex items-center gap-1.5"><kbd class="inline-flex h-6 min-w-6 items-center justify-center rounded-sm border border-b-2 bg-card px-1.5 text-caption text-foreground">{k}</kbd>{t}</span>'
hints = f'<div class="flex shrink-0 justify-center gap-4 pb-3 text-caption text-muted-foreground" aria-label="Keyboard shortcuts">{kbd("←", "Reject")}{kbd("↑", "Maybe")}{kbd("→", "Accept")}{kbd("Z", "Undo")}{kbd("N", "Note")}</div>'
mert_hdr = header('Wedding guests', 'Round 1, shared').replace('S09-list-overview.html#S09-default', 'S09-list-overview.html#S09-shared-decision-maker').replace('data-action="close"', 'data-action="finish"')
LIVE = '../04-prototype/swipe-demo.html?deck=mert&amp;next=..%2F03-screens%2FS09-list-overview.html%23S09-shared-decision-maker'
desk_screen = sorting(hdr=mert_hdr, prog=progress(85, 100, members), counts=(21, 14, 50), undo=True, undo_label='Undo last decision (Accept on Mehmet Yılmaz)')
# Prototype: on the desktop frame the decision buttons open the live demo with Mert's undecided items.
_bar_at = desk_screen.index('<div class="flex shrink-0 items-start justify-between px-5 pb-4 pt-2">')
desk_screen = desk_screen[:_bar_at] + desk_screen[_bar_at:].replace('<button class="flex min-w-touch', f'<a href="{LIVE}" class="flex min-w-touch').replace('</span></button>', '</span></a>')
finish = ''
desktop = f'''<div class="desktop">
  <div class="desktop-chrome" aria-hidden="true"><span class="flex gap-1.5"><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span><span class="size-3 rounded-full bg-muted-foreground/30"></span></span><span class="desktop-url">swipesort.app/l/7Hq2xK/sort</span></div>
  <div class="desktop-column">
  {desk_screen}
  {hints}
  {finish}
  </div>
</div>'''
F('S25-web-desktop', 'Web, desktop browser: Mert sorting with keyboard hints', desktop)

html = f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>S25 Sorting screen</title>
<link rel="stylesheet" href="../assets/css/app.css">
</head>
<body class="mock-page">
<header class="mock-doc">
  <h1>S25 Sorting screen</h1>
  <p>The heart of the product and the quality reference for every other screen. Spec: <a href="S25-sorting.md">S25-sorting.md</a>. Live interaction: <a href="../04-prototype/swipe-demo.html">swipe-demo.html</a>. Motion values: <a href="../01-foundations/motion.md">motion.md</a>.</p>
</header>
<main class="mock-canvas">
{''.join(frames)}
</main>
</body>
</html>
'''
# drop empty leading </main> from the first section
html = html.replace('<main class="mock-canvas">\n</main>\n', '', 1)
open(OUT, 'w').write(html)
print('frames:', html.count('data-frame='))
