# Usage: python3 tools/generators/S02-onboarding.py  → design/03-screens/S02-onboarding.html
from groupa_common import *

P = Page('S02', 'Onboarding', 'First launch only (replay from Settings › Help). Three steps: welcome, a hands-on gesture demo with neutral sample cards, and a recap. No account is ever required (ACC-01). The demo uses the same drag feedback as S25 (tilt, tint, stamp, armed button); physics in motion.md §2 and live in <a href="../04-prototype/swipe-demo.html">swipe-demo.html</a>.', 'S02-onboarding.md')

SKIP = 'S08-home.html#S08-first-run'

# ---------------------------------------------------------------- demo cards (sample data p02, ph09, p05, ph05)
DESK = dict(kind='product', img='products/p02.svg', title='Walnut sit-stand desk, 140 × 70 cm', sub='Oakline', price='€649', rating='4.7', reviews='532', tag='Desk',
            label='Walnut sit-stand desk, 140 × 70 cm, Oakline, 649 euros, rated 4.7')
PHOTO = dict(kind='photo', img='photos/ph09.svg', title='Mar 5, 2026, 17:56', sub='Göreme, Cappadocia', meta='IMG_2049.JPG, 5.1 MB',
             label='Photo IMG_2049.JPG, taken Mar 5, 2026 in Göreme, Cappadocia')
LAMP = dict(kind='product', img='products/p05.svg', title='Ceramic desk lamp with dimmer', sub='Lumen & Co', price='€79', rating='4.2', reviews='211', tag='Lamp',
            label='Ceramic desk lamp with dimmer, Lumen & Co, 79 euros, rated 4.2')
CITY = dict(kind='photo', img='photos/ph05.svg', title='Mar 3, 2026, 13:28', sub='Kadıköy, İstanbul', meta='IMG_2045.JPG, 2 MB',
            label='Photo IMG_2045.JPG, taken Mar 3, 2026 in Kadıköy, İstanbul')


def card_body(c, large=False):
    if large:
        # A-125 sparse card: content block vertically centered, tags pinned to the bottom
        return f'''<div class="flex min-h-0 flex-1 flex-col px-6 pb-5 pt-6">
        <div class="my-auto">
          <h2 class="line-clamp-4 text-title-1">{c["title"]}</h2>
          <p class="mt-2 text-title-3 font-normal text-muted-foreground">{c["sub"]}</p>
          <dl class="mt-6 space-y-4">
            <div><dt class="text-body-lg text-muted-foreground">Price</dt><dd class="text-title-1 tabular-nums">{c.get("price", "")}</dd></div>
            <div><dt class="text-body-lg text-muted-foreground">Rating</dt><dd class="text-title-2 font-normal">{c.get("rating", "")} <span class="text-muted-foreground">({c.get("reviews", "")} reviews)</span></dd></div>
          </dl>
        </div>
        <div class="flex gap-2 pt-3"><span class="inline-flex min-h-9 items-center rounded-full bg-secondary px-3 text-body-lg text-secondary-foreground">{c.get("tag", "")}</span></div>
      </div>'''
    if c['kind'] == 'photo':
        return f'''<img src="{IMG}{c["img"]}" alt="" class="min-h-0 w-full flex-1 object-cover">
      <div class="px-5 pb-4 pt-3">
        <h2 class="text-title-2">{c["title"]}</h2>
        <p class="mt-0.5 text-body text-muted-foreground">{c["sub"]}</p>
      </div>'''
    return f'''<img src="{IMG}{c["img"]}" alt="" class="h-[44%] w-full object-cover">
      <div class="flex min-h-0 flex-1 flex-col px-5 pb-4 pt-4">
        <h2 class="line-clamp-2 text-title-1">{c["title"]}</h2>
        <p class="mt-1 text-body-lg text-muted-foreground">{c["sub"]}</p>
        <div class="mt-3 flex items-baseline justify-between"><span class="text-title-2 tabular-nums">{c["price"]}</span><span class="inline-flex items-center gap-1 text-body">{icon("star", "size-4")}{c["rating"]} <span class="text-muted-foreground">({c["reviews"]})</span></span></div>
        <div class="mt-auto flex gap-2 pt-3"><span class="inline-flex h-7 items-center rounded-full bg-secondary px-2.5 text-caption text-secondary-foreground">{c["tag"]}</span></div>
      </div>'''


STAMP = {
    'accept': ('left-5 top-5 -rotate-6', 'check', 'Accept'),
    'reject': ('right-5 top-5 rotate-6', 'x', 'Reject'),
    'maybe': ('bottom-12 left-1/2 -translate-x-1/2', 'circle-help', 'Maybe'),
}
MOVE = {'accept': 'translate-x-24 rotate-6', 'reject': '-translate-x-24 -rotate-6', 'maybe': '-translate-y-14'}


def card(c, drag=None, reduced=False, large=False):
    move = '' if not drag or reduced else MOVE[drag]
    if drag and reduced and drag != 'maybe':
        move = {'accept': 'translate-x-24', 'reject': '-translate-x-24'}[drag]
    if drag and reduced and drag == 'maybe':
        move = '-translate-y-14'
    shadow = 'shadow-hero-drag' if drag else 'shadow-hero'
    overlay = ''
    if drag:
        pos, ic, txt = STAMP[drag]
        overlay = f'''<div class="pointer-events-none absolute inset-0 bg-{drag} opacity-25"></div>
      <div class="pointer-events-none absolute {pos} inline-flex h-11 items-center gap-2 rounded-full bg-{drag} px-4 text-label-lg text-{drag}-foreground shadow-overlay">{icon(ic, "size-6")}{txt}</div>'''
    return f'''<article class="absolute inset-x-8 bottom-4 top-0 flex origin-bottom flex-col overflow-hidden rounded-hero bg-card {shadow} {move}" aria-label="{c["label"]}" aria-roledescription="card" tabindex="0">
      {card_body(c, large)}
      {overlay}
    </article>'''


def stack(top_card, nxt=None, promote=False, hint=None):
    behind = ''
    if nxt:
        pc = 'scale-[.975] translate-y-4' if promote else 'scale-95 translate-y-8'
        behind = f'<div class="absolute inset-x-8 bottom-4 top-0 flex origin-top {pc} flex-col overflow-hidden rounded-hero border bg-card shadow-raised" aria-hidden="true">{card_body(nxt)}</div>'
    h = ''
    if hint:
        pos = {'accept': 'right-3 top-[28%]', 'reject': 'left-3 top-[28%]', 'maybe': 'left-1/2 -top-1 -translate-x-1/2'}[hint]
        arrow = {'accept': 'arrow-right', 'reject': 'arrow-left', 'maybe': 'arrow-up'}[hint]
        h = f'<div class="pointer-events-none absolute {pos} z-10 flex size-14 items-center justify-center rounded-full bg-popover text-foreground shadow-overlay" aria-hidden="true">{icon(arrow, "size-7")}</div>'
    return f'''<div class="relative mt-4 min-h-0 flex-1">
    {behind}
    {top_card}
    {h}
  </div>'''


def dbtn(kind, state='rest', large=False, href=None):
    ic = {'accept': 'check', 'reject': 'x', 'maybe': 'circle-help'}[kind]
    lab = {'accept': 'Accept', 'reject': 'Reject', 'maybe': 'Maybe'}[kind]
    cls = {'rest': f'bg-{kind}-soft text-{kind}-soft-foreground',
           'armed': f'bg-{kind} text-{kind}-foreground ring-4 ring-{kind}/25'}[state]
    if large:
        return f'<button type="button" class="flex min-h-16 flex-col items-center justify-center gap-1 rounded-control bg-{kind}-soft px-2 py-2 text-{kind}-soft-foreground" data-action="{kind}">{icon(ic, "size-7")}<span class="text-title-3">{lab}</span></button>'
    inner = f'<span class="flex size-16 items-center justify-center rounded-full {cls}">{icon(ic, "size-7")}</span><span class="text-caption">{lab}</span>'
    if href:
        return f'<a href="{href}" class="flex min-w-touch flex-col items-center gap-1.5" data-action="{kind}">{inner}</a>'
    return f'<button type="button" class="flex min-w-touch flex-col items-center gap-1.5" data-action="{kind}">{inner}</button>'


def dbar(armed=None, large=False, links=None):
    st = lambda k: 'armed' if armed == k else 'rest'
    lk = links or {}
    if large:
        return f'<div class="grid shrink-0 grid-cols-3 gap-2 px-4 pb-4 pt-3">{dbtn("reject", large=True)}{dbtn("maybe", large=True)}{dbtn("accept", large=True)}</div>'
    return f'<div class="flex shrink-0 items-start justify-center gap-10 px-5 pb-5 pt-3">{dbtn("reject", st("reject"), href=lk.get("reject"))}{dbtn("maybe", st("maybe"), href=lk.get("maybe"))}{dbtn("accept", st("accept"), href=lk.get("accept"))}</div>'


def tried(done=()):
    """Checklist of the three gestures (Reject, Maybe, Accept order)."""
    out = []
    for kind, lab, ic in (('reject', 'Reject', 'x'), ('maybe', 'Maybe', 'circle-help'), ('accept', 'Accept', 'check')):
        if kind in done:
            out.append(f'<li class="inline-flex h-8 items-center gap-1.5 rounded-full bg-{kind}-soft px-3 text-caption text-{kind}-soft-foreground">{icon(ic, "size-4")}{lab}{icon("circle-check", "size-4")}<span class="sr-only">, tried</span></li>')
        else:
            out.append(f'<li class="inline-flex h-8 items-center gap-1.5 rounded-full border border-dashed border-input px-3 text-caption text-muted-foreground">{icon(ic, "size-4")}{lab}<span class="sr-only">, not tried yet</span></li>')
    n = len(done)
    return f'''<div class="mt-3 flex items-center justify-between gap-3">
      <ul class="flex flex-wrap gap-2" aria-label="Gestures tried">{"".join(out)}</ul>
      <span class="shrink-0 text-caption tabular-nums text-muted-foreground">{n} of 3</span>
    </div>'''


def demo_bar(kind='android', back='#S02-welcome'):
    if kind == 'ios':
        return ios_nav(back_text='Back', href=back, trailing=ios_text_btn('Skip', SKIP, action='skip'))
    return appbar('', href=back, label='Back to welcome', actions=text_action('Skip', SKIP, 'skip'))


# Prototype affordance (QA-019): clicking the card finishes the demo; in the app it moves on after the
# third gesture. The decision buttons step through the demo frames.
SHORTCUT = '<a href="#S02-demo-done" class="absolute inset-x-8 bottom-4 top-0 z-20 rounded-hero" data-action="next" aria-label="Finish the demo (prototype: click the card; the app moves on after the third gesture)"></a>'


def demo(title, body, top, nxt=None, drag=None, done=(), hint=None, kind='android', reduced=False, extra='', promote=None, shortcut=False, links=None, note=None):
    tc = card(top, drag, reduced) + (SHORTCUT if shortcut else '')
    sub = (f'<p class="mt-1 flex items-start gap-1.5 text-body text-foreground" role="status">{icon("info", "size-5 mt-0.5 shrink-0 text-primary")}<span>{note}</span></p>' if note
           else f'<p class="mt-1 text-body text-muted-foreground">{body}</p>')
    return f'''{demo_bar(kind)}
  <div class="shrink-0 px-gutter">
    <h1 class="text-title-2">{title}</h1>
    {sub}
    {tried(done)}
  </div>
  {stack(tc, nxt, promote if promote is not None else bool(drag), hint)}
  {dbar(drag, links=links)}
  {extra}'''


# ---------------------------------------------------------------- welcome
def hero(size='h-96'):
    return f'''<div class="relative mx-auto {size} w-72 shrink-0" aria-hidden="true">
      <div class="absolute left-0 top-8 h-72 w-52 origin-bottom -rotate-6 overflow-hidden rounded-hero border bg-card shadow-raised"><img src="{IMG}photos/ph09.svg" alt="" class="h-full w-full object-cover"></div>
      <div class="absolute right-0 top-8 h-72 w-52 origin-bottom rotate-6 overflow-hidden rounded-hero border bg-card shadow-raised"><img src="{IMG}products/p05.svg" alt="" class="h-1/2 w-full object-cover"></div>
      <div class="absolute left-1/2 top-2 flex h-80 w-56 -translate-x-1/2 rotate-3 flex-col overflow-hidden rounded-hero bg-card shadow-hero">
        <img src="{IMG}products/p02.svg" alt="" class="h-[52%] w-full object-cover">
        <div class="px-4 pt-3"><p class="line-clamp-2 text-title-3">Walnut sit-stand desk</p><p class="text-body-sm text-muted-foreground">Oakline</p><p class="mt-2 text-title-3 tabular-nums">€649</p></div>
        <div class="absolute left-3 top-3 inline-flex h-9 -rotate-6 items-center gap-1.5 rounded-full bg-accept px-3 text-label text-accept-foreground shadow-overlay">{icon("check", "size-5")}Accept</div>
      </div>
    </div>'''


def welcome(kind='android', web_note=False, replay=False):
    if replay:
        top = appbar('', back='x', href='S06-settings.html#S06-help', label='Close the introduction', action='close')
        return f'''{top}
  <div class="flex min-h-0 flex-1 flex-col justify-center">{hero()}</div>
  <div class="shrink-0 px-gutter text-center">
    <h1 class="text-balance text-title-1">Sort any list, one card at a time</h1>
    <p class="mx-auto mt-2 max-w-prose text-body-lg text-muted-foreground">Swipe right to accept, left to reject, up for maybe. Works for people, photos, things to buy and ideas, alone or with others.</p>
  </div>
  <div class="shrink-0 space-y-2 px-gutter pb-4 pt-6">
    {btn("Try the gestures", href="#S02-demo", action="next")}
    {btn("Done", "ghost", href="S06-settings.html#S06-help", action="done")}
  </div>'''
    if kind == 'ios':
        top = ios_nav(trailing=ios_text_btn('Skip', SKIP, action='skip'))
    else:
        top = f'<header class="flex h-app-bar shrink-0 items-center justify-end px-1">{text_action("Skip", SKIP, "skip")}</header>'
    note = ''
    if web_note:
        note = f'<div class="shrink-0 px-gutter pb-2 pt-4">{alert_neutral("Using SwipeSort in your browser", "Everything works here. Get the app to import phone contacts and photos from your gallery.", action=link("Get the app", "https://swipesort.app/get"))}</div>'
        top = ''
    return f'''{top}
  {note}
  <div class="flex min-h-0 flex-1 flex-col justify-center">{hero()}</div>
  <div class="shrink-0 px-gutter text-center">
    <h1 class="text-balance text-title-1">Sort any list, one card at a time</h1>
    <p class="mx-auto mt-2 max-w-prose text-body-lg text-muted-foreground">Swipe right to accept, left to reject, up for maybe. Works for people, photos, things to buy and ideas, alone or with others.</p>
  </div>
  <div class="shrink-0 space-y-2 px-gutter pb-4 pt-6">
    {btn("Get started", href="#S02-demo", action="next")}
    {btn("I have an account", "ghost", href="S03-sign-in.html#S03-default", action="sign-in")}
    <p class="flex items-center justify-center gap-1.5 pt-1 text-body-sm text-muted-foreground">{icon("smartphone", "size-4")}No account needed. Lists stay on this phone.</p>
  </div>'''


P.section('Welcome', 'What SwipeSort does in one sentence, shown with real sample cards. "Get started" opens the demo; "I have an account" opens S03. Skip goes straight to an empty Lists screen (S08 first run).')
P.frame('S02-default', 'Default entry: replayed from Settings › Help (close instead of Skip)', phone(welcome(replay=True)))
P.frame('S02-welcome', 'Welcome (first launch)', phone(welcome()))

# ---------------------------------------------------------------- demo
P.section('Gesture demo', 'A deck of four neutral sample cards (products and photos from sample data). The user tries all three gestures in any order; the checklist fills as each one is used, and the instruction always names the next untried gesture. Buttons count too. Nothing is saved. After the third gesture the recap opens automatically (700 ms after the commit).')
P.frame('S02-demo', 'Demo, step 1: swipe right to accept', phone(demo(
    'Swipe right to accept', 'Try it on these sample cards. Nothing is saved.', DESK, PHOTO, hint='accept', shortcut=True, links={'accept': '#S02-demo-step-2'})))
P.frame('S02-demo-drag-accept', 'Dragging right, armed: tint, stamp, Accept button fills', phone(demo(
    'Swipe right to accept', 'Try it on these sample cards. Nothing is saved.', DESK, PHOTO, drag='accept')))
P.frame('S02-demo-snap-back', 'Released too early: card snaps back, hint', phone(demo(
    'Swipe right to accept', 'Try it on these sample cards. Nothing is saved.', DESK, PHOTO,
    note='Drag a little further to decide. Let go early to cancel.')))
P.frame('S02-demo-step-2', 'Demo, step 2: swipe left to reject', phone(demo(
    'Swipe left to reject', 'Accepted. Now send this one the other way.', PHOTO, LAMP, done=('accept',), hint='reject', links={'reject': '#S02-demo-step-3'})))
P.frame('S02-demo-drag-reject', 'Dragging left, armed', phone(demo(
    'Swipe left to reject', 'Accepted. Now send this one the other way.', PHOTO, LAMP, drag='reject', done=('accept',))))
P.frame('S02-demo-step-3', 'Demo, step 3: swipe up for maybe', phone(demo(
    'Swipe up for maybe', 'Not sure? Maybe items wait in their own pile so you can sort them again later.', LAMP, CITY, done=('accept', 'reject'), hint='maybe', links={'maybe': '#S02-demo-done'})))
P.frame('S02-demo-drag-maybe', 'Dragging up, armed', phone(demo(
    'Swipe up for maybe', 'Not sure? Maybe items wait in their own pile so you can sort them again later.', LAMP, CITY, drag='maybe', done=('accept', 'reject'))))
P.frame('S02-demo-other-order', 'Any order works: left first, the hint moves on to the next untried gesture', phone(demo(
    'Swipe right to accept', 'Rejected. You can also accept: swipe right.', PHOTO, LAMP, done=('reject',), hint='accept')))


# ---------------------------------------------------------------- done
def recap_row(c, thumb_round, verb, kind):
    ic = {'accept': 'check', 'reject': 'x', 'maybe': 'circle-help'}[kind]
    badge = {'accept': 'Accepted', 'reject': 'Rejected', 'maybe': 'Maybe'}[kind]
    arrow = {'accept': 'arrow-right', 'reject': 'arrow-left', 'maybe': 'arrow-up'}[kind]
    return f'''<li class="flex min-h-16 items-center gap-3 px-4 py-2.5"><img src="{IMG}{c["img"]}" alt="" class="size-10 shrink-0 {thumb_round} object-cover"><div class="min-w-0 flex-1"><p class="truncate text-body">{c.get("short", c["title"])}</p><p class="flex items-center gap-1 text-body-sm text-muted-foreground">{icon(arrow, "size-4")}{verb}</p></div><span class="inline-flex h-7 shrink-0 items-center gap-1.5 rounded-full bg-{kind}-soft px-2.5 text-caption text-{kind}-soft-foreground">{icon(ic, "size-4")}{badge}</span></li>'''


DESK['short'] = 'Walnut sit-stand desk'
PHOTO['short'] = 'Göreme, Cappadocia'
LAMP['short'] = 'Ceramic desk lamp'


def done_screen(kind='android', large=False):
    top = ios_nav(back_text='Back', href='#S02-demo') if kind == 'ios' else appbar('', href='#S02-demo', label='Back to the demo')
    rows = recap_row(PHOTO, 'rounded-sm', 'Swiped left', 'reject') + recap_row(LAMP, 'rounded-sm', 'Swiped up', 'maybe') + recap_row(DESK, 'rounded-sm', 'Swiped right', 'accept')
    t = 'text-display' if large else 'text-title-1'
    b = 'text-title-3 font-normal' if large else 'text-body-lg'
    recap = '' if large else f'<ul class="mt-8 divide-y overflow-hidden rounded-group bg-card text-left dark:border" aria-label="Your demo decisions">{rows}</ul>'
    return f'''{top}
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-4">
    <h1 class="{t}">You know the three gestures</h1>
    <p class="mt-2 {b} text-muted-foreground">Right to accept, left to reject, up for maybe. Undo is always one tap away, and you can change any decision later.</p>
    {recap}
  </div>
  <div class="shrink-0 space-y-2 px-gutter pb-4 pt-4">
    {btn("Get started", href="S08-home.html#S08-first-run", action="get-started")}
    {btn("I have an account", "ghost", href="S03-sign-in.html#S03-default", action="sign-in")}
    <p class="flex items-center justify-center gap-1.5 pt-1 text-center text-body-sm text-muted-foreground">{icon("smartphone", "size-4 shrink-0")}No account needed. Lists stay on this phone.</p>
  </div>'''


P.section('Recap', 'The three sample decisions, shown as decision badges in the Reject, Maybe, Accept order, then into the app. "Get started" opens Lists in its first-run state (S08) without asking for an account.')
P.frame('S02-demo-done', 'Recap after the demo', phone(done_screen()))

# ---------------------------------------------------------------- accessibility
P.section('Accessibility', 'Reduced motion: the card follows the finger without tilt and the hint arrow is static; tint and stamp still show. Large text: the welcome illustration hides and the demo uses the labeled button grid from S25. Screen readers: the card exposes Accept, Reject and Maybe actions, and the instruction says so.')
P.frame('S02-demo-reduced-motion', 'Reduced motion: no tilt, static hint, tint and stamp kept', phone(demo(
    'Swipe right to accept', 'Try it on these sample cards. Nothing is saved.', DESK, PHOTO, drag='accept', reduced=True, promote=False)))

lt_welcome = f'''<header class="flex min-h-16 shrink-0 items-center justify-end px-1">{text_action("Skip", SKIP, "skip").replace("text-label-lg", "text-title-3")}</header>
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-2">
    {mark("size-16")}
    <h1 class="mt-6 text-display">Sort any list, one card at a time</h1>
    <p class="mt-4 text-title-2 font-normal text-muted-foreground">Swipe right to accept, left to reject, up for maybe. Works for people, photos, things to buy and ideas, alone or with others.</p>
  </div>
  <div class="shrink-0 space-y-2 px-gutter pb-4 pt-4">
    {btn("Get started", href="#S02-demo", extra="min-h-16 h-auto py-3 text-title-3")}
    {btn("I have an account", "ghost", href="S03-sign-in.html#S03-default", extra="min-h-16 h-auto py-3 text-title-3")}
    <p class="flex items-start gap-2 pt-1 text-body-lg text-muted-foreground">{icon("smartphone", "size-6 mt-0.5 shrink-0")}No account needed. Lists stay on this phone.</p>
  </div>'''
P.frame('S02-welcome-large-text', 'Large text (200%): illustration hidden, text wraps', phone(lt_welcome))

lt_demo = f'''{appbar('', href='#S02-welcome', label='Back to welcome', actions=text_action('Skip', SKIP, 'skip'))}
  <div class="shrink-0 px-gutter">
    <h1 class="text-title-1">Swipe right to accept</h1>
    <p class="mt-1 text-title-3 font-normal text-muted-foreground">Or use the buttons below.</p>
    <p class="mt-2 text-body-lg tabular-nums text-muted-foreground">0 of 3 gestures tried</p>
  </div>
  {stack(card(DESK, large=True), PHOTO)}
  {dbar(large=True)}'''
P.frame('S02-demo-large-text', 'Large text (200%): image hidden, labeled button grid', phone(lt_demo))

sr = f'''{scrim('z-20')}
  <div class="absolute inset-x-6 top-1/3 z-30 rounded-dialog bg-popover p-5 shadow-dialog" role="dialog" aria-labelledby="s02sr">
    <p class="text-caption text-muted-foreground">Screen reader (TalkBack actions menu, VoiceOver rotor)</p>
    <h2 id="s02sr" class="mt-1 text-title-3">Walnut sit-stand desk, 140 × 70 cm</h2>
    <ul class="mt-3 divide-y text-body">
      <li class="flex h-12 items-center gap-3">{icon("check", "size-5 text-accept-soft-foreground")}Accept</li>
      <li class="flex h-12 items-center gap-3">{icon("x", "size-5 text-reject-soft-foreground")}Reject</li>
      <li class="flex h-12 items-center gap-3">{icon("circle-help", "size-5 text-maybe-soft-foreground")}Maybe</li>
    </ul>
    <p class="mt-3 text-body-sm text-muted-foreground">Instruction read first: “Try the three decisions on these sample cards. Use the card's actions or the buttons below.” After an action: “Accepted. 1 of 3 tried.”</p>
  </div>'''
P.frame('S02-demo-screen-reader', 'Screen-reader actions on the demo card (annotation)', phone(demo(
    'Swipe right to accept', 'Try it on these sample cards. Nothing is saved.', DESK, PHOTO, extra=sr)))

# ---------------------------------------------------------------- platforms
P.section('iOS and web', 'iOS: navigation bar with a back chevron and Skip as a text button; edge swipe goes back a step. Web: same layout; mobile browsers show a short note about the app; desktop browsers add arrow-key hints (web only).')
P.frame('S02-welcome-ios', 'iOS welcome', phone(welcome('ios'), kind='ios'))
P.frame('S02-demo-ios', 'iOS demo, step 1', phone(demo('Swipe right to accept', 'Try it on these sample cards. Nothing is saved.', DESK, PHOTO, hint='accept', kind='ios'), kind='ios'))
P.frame('S02-web', 'Web, mobile browser: welcome with a note about the app', phone(welcome(web_note=True), kind='web'))

kbd = lambda k, t: f'<span class="inline-flex items-center gap-1.5"><kbd class="inline-flex h-6 min-w-6 items-center justify-center rounded-sm border border-b-2 bg-card px-1.5 text-caption text-foreground">{k}</kbd>{t}</span>'
hints = f'<div class="flex shrink-0 justify-center gap-4 pb-4 text-caption text-muted-foreground" aria-label="Keyboard shortcuts">{kbd("←", "Reject")}{kbd("↑", "Maybe")}{kbd("→", "Accept")}</div>'
desk_demo = demo('Press → or drag right to accept', 'Try it on these sample cards. Nothing is saved.', DESK, PHOTO, hint='accept')
P.frame('S02-web-desktop', 'Web, desktop browser: demo with keyboard hints', desktop(desk_demo + hints, 'swipesort.app/welcome'))

P.write('S02-onboarding.html')
