# Usage: python3 tools/generators/S05-sign-in-prompt.py  → design/03-screens/S05-sign-in-prompt.html
import re
from groupa_common import *

P = Page('S05', 'Sign-in prompt and moving lists', 'A bottom sheet over the screen that needs an account: Share or Invite on a list (S09, S10), Back up (S06, S08 indicator). It explains why, signs in, then moves the lists on this phone to the account (all by default; Choose lists keeps some on this phone only, D-33) and continues the original action. The sample list never moves (D-10). Backgrounds are simplified, non-interactive copies of S09 and S08.', 'S05-sign-in-prompt.md')

ORIGIN_SHARE = 'S09-list-overview.html#S09-guest-wedding'
ORIGIN_BACKUP = 'S08-home.html#S08-guest'


# ---------------------------------------------------------------- backgrounds (inert copies of the origin screens)
# Reuses Group B's markup (tools/generators/S08-S10-lists.py) without running its page writers: only the
# helper definitions above its first `P = Page(` are executed.
_B = {}
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'S08-S10-lists.py')).read()
exec(_src[:_src.index("\nP = Page('S08'")], _B)


def bg_list(kind='android', web=False):
    """S09-guest-wedding (Wedding guests before sharing, not signed in)."""
    s = _B['ov_guest_wedding'](web=web)
    if kind == 'ios':
        s = s.replace(_B['ov_bar'](share=('S05-sign-in-prompt.html#S05-share', 'Share list', None)),
                      _B['ov_ios_bar'](share=('S05-sign-in-prompt.html#S05-share', 'Share list')))
    return _B['inert'](s)


_S6 = {}
_src6 = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'S06-settings.py')).read()
exec(_src6[:_src6.index("P.section('Settings root'")], _S6)


def bg_settings():
    """S06-guest (Settings while not signed in)."""
    return _B['inert'](_S6['root']('guest', notif_value='Off'))


def bg_home(kind='android', web=False):
    """S08-guest (lists on this phone only; one indicator line under the Lists title)."""
    s = _B['home_guest'](web=web)
    if not web:  # frames use overlay_full: absolute offsets count from the phone edge, past the 24 dp nav bar
        s = s.replace('absolute bottom-24 right-4', 'absolute bottom-32 right-4')
    if kind == 'ios':
        s = s.replace(large_title('Lists', _B['search_btn']()), ios_nav(large='Lists'))
        s = s.replace(bottom_nav('lists', badge=0), ios_tab_bar('lists', badge=0))
        s = s.replace(_B['fab'](), '')
    return _B['inert'](s)


# ---------------------------------------------------------------- sheet content
def why_points(points):
    return '<ul class="mt-4 space-y-3">' + ''.join(
        f'<li class="flex gap-3 text-body">{icon(ic, "size-5 mt-0.5 shrink-0 text-muted-foreground")}<span>{t}</span></li>' for ic, t in points) + '</ul>'


def round_icon(name, tone='primary'):
    cls = {'primary': 'bg-primary-soft text-primary-soft-foreground', 'neutral': 'bg-secondary text-foreground', 'error': 'bg-secondary text-destructive'}[tone]
    return f'<span class="flex size-12 shrink-0 items-center justify-center rounded-full {cls}">{icon(name, "size-6")}</span>'


def choose_link(kind='android', web=False, purpose='share'):
    if purpose == 'backup':
        href = '#S05-backup-choose-lists'
    else:
        href = '#S05-ios-choose-lists' if kind == 'ios' else ('#S05-web-choose-lists' if web else '#S05-choose-lists')
    return f'<a href="{href}" class="-my-1 inline-flex min-h-touch items-center text-label-lg text-primary underline underline-offset-4" data-action="choose-lists">Choose lists</a>'


def prompt(sid, purpose='share', kind='android', state=None, large=False, web=False, chosen=False):
    """chosen: the person used Choose lists and left one list unchecked (A-135)."""
    off = state == 'offline'
    busy = state == 'busy'
    where = 'in this browser' if web else 'on this phone'
    if chosen:
        move_line = f'3 of your 4 lists {where} move to your account. 1 stays {where} only.'
    elif purpose == 'share':
        move_line = f'Your 4 lists {where} move to your account and are backed up.'
    else:
        move_line = f'Your 4 lists {where} move to your account.'
    move_point = f'<span class="block">{move_line}</span>{choose_link(kind, web, purpose)}'
    if purpose == 'share':
        ic, title = 'users', 'Sign in to share this list'
        body = 'Sharing needs an account, so members can sort “Wedding guests” on their own devices and see where you agree.'
        points = [('cloud-upload', move_point),
                  ('wifi-off', 'Sorting keeps working offline, like now.')]
        not_now = ORIGIN_SHARE
        email_href = 'S03-sign-in.html#S03-context-share'
    else:
        ic, title = 'cloud-upload', 'Sign in to back up your lists'
        body = ('Your lists are saved in this browser only. Browsers can clear lists you haven\'t opened for a while. Signing in keeps them safe and on every device.' if web else
                'Your lists are saved on this phone only. If you lose it or remove the app, they\'re gone. An account keeps them safe and on every device.')
        points = [('cloud-upload', move_point),
                  ('smartphone', 'Open them on other phones and in the browser.')]
        not_now = ORIGIN_BACKUP
        email_href = 'S03-sign-in.html#S03-context-backup'
    nxt = '#S05-moving-some-kept' if chosen else '#S05-moving'
    btns = provider_buttons(kind, google_href=nxt, apple_href=nxt, email_href=email_href, off=off,
                            busy='google' if busy else None)
    btns.append(btn('Not now', 'ghost', href=not_now, action='not-now'))
    if large:
        btns = [b.replace('h-14', 'min-h-16 h-auto py-3').replace('text-label-lg', 'text-title-3') for b in btns]
    banner = ''
    if off:
        banner = f'<div class="mt-4 flex items-start gap-2 rounded-control bg-muted px-3 py-2.5 text-body-sm" role="status">{icon("wifi-off", "size-4 mt-0.5 shrink-0")}<span>You\'re offline. Signing in needs a connection. Your lists stay {where}.</span></div>'
    t = 'text-title-1' if large else 'text-title-2'
    b = 'text-title-3 font-normal' if large else 'text-body'
    pts = why_points(points).replace('text-body', 'text-title-3 font-normal').replace('text-label-lg', 'text-title-3') if large else why_points(points)
    if large:
        return f'''<div class="min-h-0 flex-1 overflow-hidden pb-3">
    <div class="pt-3">{round_icon(ic)}</div>
    <h2 id="{sid}-t" class="mt-4 {t}">{title}</h2>
    <p class="mt-2 {b} text-muted-foreground">{body}</p>
    {pts}
    {banner}
    </div>
    <div class="shrink-0 space-y-3 border-t pt-4">{"".join(btns)}</div>'''
    return f'''<div class="pt-3">{round_icon(ic)}</div>
    <h2 id="{sid}-t" class="mt-4 {t}">{title}</h2>
    <p class="mt-2 {b} text-muted-foreground">{body}</p>
    {pts}
    {banner}
    <div class="mt-6 space-y-3">{"".join(btns)}</div>'''


# ---------------------------------------------------------------- Choose lists (D-33, A-135)
def check_box(on, ios=False):
    if ios:
        if on:
            return f'<span class="flex size-6 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground" aria-hidden="true">{icon("check", "size-4")}</span>'
        return '<span class="size-6 shrink-0 rounded-full border-2 border-input" aria-hidden="true"></span>'
    if on:
        return f'<span class="flex size-6 shrink-0 items-center justify-center rounded-sm bg-primary text-primary-foreground" aria-hidden="true">{icon("check", "size-4")}</span>'
    return '<span class="size-6 shrink-0 rounded-sm border-2 border-input bg-popover" aria-hidden="true"></span>'


def choose_rows(sid, purpose='share', ios=False, large=False, kept=('Frontend hiring, Q4',)):
    out = []
    tsz = 'text-title-3 font-normal' if large else 'text-body'
    dsz = 'text-body-lg' if large else 'text-body-sm'
    for i, (name, count, ic) in enumerate(DEVICE_LISTS):
        locked = purpose == 'share' and name == 'Wedding guests'
        on = name not in kept
        tile = f'<span class="flex size-10 shrink-0 items-center justify-center rounded-control bg-secondary text-muted-foreground">{icon(ic)}</span>'
        if locked:
            box = check_box(True, ios).replace('aria-hidden="true"', 'aria-hidden="true"', 1).replace('class="flex', 'class="opacity-50 flex', 1)
            desc = f'<span id="{sid}-l{i}" class="flex items-center gap-1.5 {dsz} text-muted-foreground">{icon("lock", "size-4 shrink-0")}Needed to share</span>'
            out.append(f'<li><div role="checkbox" aria-checked="true" aria-disabled="true" aria-describedby="{sid}-l{i}" tabindex="0" class="flex min-h-16 w-full items-center gap-3 py-2 text-left">{box}{tile}<span class="min-w-0 flex-1"><span class="block {"" if large else "truncate "}{tsz}">{name}</span>{desc}</span></div></li>')
        else:
            desc = f'<span class="block {dsz} tabular-nums text-muted-foreground">{count} items</span>'
            out.append(f'<li><button type="button" role="checkbox" aria-checked="{"true" if on else "false"}" class="flex min-h-16 w-full items-center gap-3 py-2 text-left">{check_box(on, ios)}{tile}<span class="min-w-0 flex-1"><span class="block {"" if large else "truncate "}{tsz}">{name}</span>{desc}</span></button></li>')
    return f'<ul class="mt-3 divide-y" aria-label="Lists to move">{"".join(out)}</ul>'


def choose_lists(sid, purpose='share', kind='android', web=False, large=False):
    """Checklist step inside the S05 sheet: every list starts checked; the shared list is locked on; the sample
    list is never listed (D-10). Frames show "Frontend hiring, Q4" unchecked."""
    ios = kind == 'ios'
    only = 'in this browser only' if web else 'on this phone only'
    if purpose == 'share':
        back = '#S05-ios' if ios else ('#S05-web' if web else '#S05-share')
        done = '#S05-ios' if ios else ('#S05-web' if web else '#S05-share-chosen')
    else:
        back = done = '#S05-backup'
    extra = ' Browsers can clear lists you haven\'t opened for a while.' if web else ''
    lead = f'Checked lists move to your account and are backed up. The others stay {only}.{extra} You can back them up later in Settings › Backup.'
    count = 3 if purpose == 'share' else 3
    summary = f'<p class="text-body-sm tabular-nums text-muted-foreground" role="status">{count} of 4 lists move</p>'
    if ios:
        head = f'''<div class="-mx-3 grid grid-cols-[1fr_auto_1fr] items-center gap-2">
      <a href="{back}" class="inline-flex h-12 items-center gap-0.5 justify-self-start pr-2 text-body text-primary" data-action="back">{icon("chevron-left", "size-6")}Back</a>
      <h2 id="{sid}-t" class="text-body font-semibold">Choose lists</h2>
      <a href="{done}" class="inline-flex h-12 items-center justify-self-end px-2 text-body font-semibold text-primary" data-action="done">Done</a>
    </div>'''
        return f'''{head}
    <p class="mt-2 text-body text-muted-foreground">{lead}</p>
    {choose_rows(sid, purpose, ios=True)}
    <div class="mt-3">{summary}</div>'''
    tsz = 'text-title-1' if large else 'text-title-2'
    bsz = 'text-title-3 font-normal' if large else 'text-body'
    head = f'''<div class="-ml-3 flex items-center gap-1 pt-1">
      <a href="{back}" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Back" data-action="back">{icon("arrow-left", "size-6")}</a>
      <h2 id="{sid}-t" class="min-w-0 flex-1 {tsz}">Choose lists to move</h2>
    </div>'''
    done_btn = btn('Done', href=done, action='done')
    if large:
        done_btn = done_btn.replace('h-14', 'min-h-16 h-auto py-3').replace('text-label-lg', 'text-title-3')
        return f'''<div class="min-h-0 flex-1 overflow-hidden pb-3">
    {head}
    <p class="mt-2 {bsz} text-muted-foreground">{lead}</p>
    {choose_rows(sid, purpose, large=True)}
    </div>
    <div class="shrink-0 space-y-3 border-t pt-4">{summary.replace("text-body-sm", "text-body-lg")}{done_btn}</div>'''
    return f'''{head}
    <p class="mt-2 {bsz} text-muted-foreground">{lead}</p>
    {choose_rows(sid, purpose)}
    <div class="mt-5 space-y-3">{summary}{done_btn}</div>'''


STATUS = {
    'moved': ('circle-check', 'Moved', 'text-foreground'),
    'moving': ('loader-circle', 'Moving…', 'text-primary'),
    'waiting': ('clock', 'Waiting', 'text-muted-foreground'),
    'failed': ('circle-alert', 'Not moved', 'text-destructive'),
    'kept': ('cloud-off', 'On this phone only', 'text-muted-foreground'),
    'kept-web': ('cloud-off', 'On this browser only', 'text-muted-foreground'),
}


def list_rows(statuses):
    out = []
    for (name, count, ic), st in zip(DEVICE_LISTS, statuses):
        sic, lab, col = STATUS[st]
        spin = ' animate-spin' if st == 'moving' else ''
        out.append(f'<li class="flex min-h-14 items-center gap-3 py-2"><span class="flex size-10 shrink-0 items-center justify-center rounded-control bg-secondary text-muted-foreground">{icon(ic)}</span><div class="min-w-0 flex-1"><p class="truncate text-body">{name}</p><p class="text-body-sm tabular-nums text-muted-foreground">{count} items</p></div><span class="inline-flex shrink-0 items-center gap-1.5 text-body-sm {col}">{icon(sic, "size-4" + spin)}{lab}</span></li>')
    return f'<ul class="mt-4 divide-y" aria-label="Lists">{"".join(out)}</ul>'


def signed_in_as():
    return f'<div class="flex items-center gap-3 pt-3">{avatar(ME["avatar"], size="size-8")}<p class="min-w-0 flex-1 truncate text-body-sm text-muted-foreground">Signed in as <span class="text-foreground">{ME["email"]}</span></p></div>'


def moving(sid, web=False, kept=False):
    """kept: one list was left unchecked in Choose lists; it shows as staying on this phone (A-135)."""
    where = 'this browser' if web else 'this phone'
    total = 3 if kept else 4
    w = 'w-2/3' if kept else 'w-1/2'
    rows = ['moved', 'moved', 'moving', 'kept-web' if web else 'kept'] if kept else ['moved', 'moved', 'moving', 'waiting']
    nxt = '#S05-moved-some-kept' if kept else '#S05-moved'
    return f'''{signed_in_as()}
    <h2 id="{sid}-t" class="mt-5 text-title-2">Moving your lists to your account</h2>
    <p class="mt-2 text-body text-muted-foreground">Keep SwipeSort open. Each list stays on {where} until it\'s safely in your account.</p>
    <div class="relative">
    <div class="mt-5" role="status">
      <div class="flex items-baseline justify-between"><span class="text-label tabular-nums">2 of {total} moved</span></div>
      <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="2" aria-valuemin="0" aria-valuemax="{total}" aria-label="2 of {total} lists moved"><div class="h-full {w} rounded-full bg-primary"></div></div>
    </div>
    {list_rows(rows)}
    <a href="{nxt}" class="absolute inset-0 rounded-control" data-action="next" aria-label="Finish moving (prototype: click the progress; the sheet moves on by itself)"></a>
    </div>'''


def moved(sid, purpose='share', merge=False):
    if purpose == 'share':
        tail = 'Now you can share “Wedding guests”.'
        action = btn('Share list', href='S31-invite.html#S31-default', action='continue')
    else:
        tail = 'Changes back up automatically from now on.'
        action = btn('Done', href='S06-settings.html#S06-backup', action='done')
    title = '4 lists added to your account' if merge else '4 lists moved to your account'
    body = (f'Your account now has 6 lists: the 4 from this phone and the 2 that were already there. Nothing was replaced. {tail}' if merge
            else f'They\'re backed up to {ME["email"]} and stay on this phone too. {tail}')
    return f'''<div class="pt-3">{round_icon('cloud-check', 'neutral')}</div>
    <h2 id="{sid}-t" class="mt-4 text-title-2" role="status">{title}</h2>
    <p class="mt-2 text-body text-muted-foreground">{body}</p>
    {list_rows(['moved'] * 4)}
    <div class="mt-5">{action}</div>'''


def moved_some_kept(sid):
    return f'''<div class="pt-3">{round_icon('cloud-check', 'neutral')}</div>
    <h2 id="{sid}-t" class="mt-4 text-title-2" role="status">3 lists moved to your account</h2>
    <p class="mt-2 text-body text-muted-foreground">1 stays on this phone only. You can back it up anytime in Settings › Backup. Now you can share “Wedding guests”.</p>
    {list_rows(['moved', 'moved', 'moved', 'kept'])}
    <div class="mt-5">{btn('Share list', href='S31-invite.html#S31-default', action='continue')}</div>'''


def partial(sid):
    return f'''<div class="pt-3">{round_icon('circle-alert', 'error')}</div>
    <h2 id="{sid}-t" class="mt-4 text-title-2">3 of 4 lists moved</h2>
    <p class="mt-2 text-body text-muted-foreground">“Trip ideas” didn\'t move. It\'s still on this phone and nothing is lost. Try again now, or later from Settings › Backup.</p>
    {list_rows(['moved', 'moved', 'failed', 'moved'])}
    <div class="mt-5 space-y-2">{btn('Try again', href='#S05-moving', action='retry')}{btn('Continue to share', 'ghost', href='S31-invite.html#S31-default', action='continue')}</div>'''


def failed(sid):
    return f'''<div class="pt-3">{round_icon('wifi-off', 'error')}</div>
    <h2 id="{sid}-t" class="mt-4 text-title-2">Your lists didn\'t move</h2>
    <p class="mt-2 text-body text-muted-foreground">The connection dropped. You\'re signed in, and all 4 lists are safe on this phone. They move automatically when you\'re back online, or try again now.</p>
    {list_rows(['failed'] * 4)}
    <div class="mt-5 space-y-2">{btn('Try again', href='#S05-moving', action='retry')}{btn('Later', 'ghost', href=ORIGIN_SHARE, action='later')}</div>'''


def scene(bg, sid, content, kind='android', z_top=None):
    """Sheet over the origin screen. Use with phone(..., overlay_full=True) so scrim and sheet run under the
    system bars; bottom padding keeps the content above the gesture bar (24 Android, 34 iOS)."""
    pad = {'ios': 'pb-14', 'android': 'pb-12', 'web': 'pb-6'}[kind]
    return f'''{bg}
  {sheet(sid, content, ios=kind == 'ios', pad=pad)}'''


def backed_up(bg):
    """Host screen after the move (QA-054): lists are backed up, the not-backed-up indicator is gone."""
    bg = re.sub(r'<span class="mx-4 flex min-h-touch[^"]*">(?:(?!</span>).)*</i><span class="flex-1">Lists are on this phone only</span><span class="text-label text-primary">Back up</span></span>', '', bg)
    bg = re.sub(r'<span class="(ml-1 )?text-label text-primary">Back up</span>', '', bg)
    bg = bg.replace('i-lucide-cloud-off', 'i-lucide-cloud-check')
    return bg.replace('Lists are on this phone only', 'Lists are backed up').replace('On this phone only', 'Backed up')


# ---------------------------------------------------------------- frames
P.section('Why sign in', 'Opened when someone without an account taps Share, Invite or Back up. The sheet names the reason, says what happens to their lists (with "Choose lists" to keep some on this phone), and offers Google, Apple and email (Apple first on iOS, Google first on Android and web, A-140). "Not now" closes it; nothing changes. Continue with email opens S03 with the same context line.')
P.frame('S05-default', 'Default entry: Back up from Settings (not signed in)', phone(scene(bg_settings(), 's05df', prompt('s05df', 'backup')), overlay_full=True))
P.frame('S05-share', 'Share: why an account is needed', phone(scene(bg_list(), 's05s', prompt('s05s', 'share')), overlay_full=True))
P.frame('S05-backup', 'Back up: why an account is needed', phone(scene(bg_home(), 's05b', prompt('s05b', 'backup')), overlay_full=True))
P.frame('S05-signing-in', 'Signing in with Google', phone(scene(bg_list(), 's05g', prompt('s05g', 'share', state='busy')), overlay_full=True))
P.frame('S05-offline', 'Offline: sign-in disabled with the reason', phone(scene(bg_list(), 's05o', prompt('s05o', 'share', state='offline')), overlay_full=True))

P.section('Choose lists', 'Every list on this phone moves by default. "Choose lists" opens a checklist inside the same sheet: all lists start checked, the list being shared is locked on ("Needed to share"), and the sample list is never listed (D-10). Unchecked lists stay on this phone only and belong to the account (D-33, A-135). The frames show "Frontend hiring, Q4" unchecked.')
P.frame('S05-choose-lists', 'Choose lists: checklist, shared list locked on', phone(scene(bg_list(), 's05cl', choose_lists('s05cl')), overlay_full=True))
P.frame('S05-share-chosen', 'Share prompt after choosing: 3 of 4 lists move', phone(scene(bg_list(), 's05sc', prompt('s05sc', 'share', chosen=True)), overlay_full=True))
P.frame('S05-backup-choose-lists', 'Choose lists from Back up: nothing locked', phone(scene(bg_home(), 's05bcl', choose_lists('s05bcl', 'backup')), overlay_full=True))
P.frame('S05-choose-lists-large-text', 'Choose lists, large text (200%)', phone(bg_list() + sheet('s05cll', choose_lists('s05cll', large=True), pad='pb-12'), overlay_full=True))

P.section('Moving lists to the account', 'Right after sign-in, the lists on this phone move to the account, one by one, the shared list first, then newest activity. Lists left unchecked in Choose lists show "On this phone only" and never upload. Each list stays usable locally the whole time. When the move finishes, the original action continues: Share opens the invite (S31); Back up returns to the backup page (S06).')
P.frame('S05-moving', 'Moving 4 lists (progress)', phone(scene(bg_list(), 's05m', moving('s05m')), overlay_full=True))
P.frame('S05-moved', 'Moved: continue to share', phone(scene(backed_up(bg_list()), 's05d', moved('s05d', 'share')), overlay_full=True))
P.frame('S05-moved-backup', 'Moved: from Back up', phone(scene(backed_up(bg_home()), 's05db', moved('s05db', 'backup')), overlay_full=True))
P.frame('S05-moved-merge', 'Moved into an account that already has lists', phone(scene(backed_up(bg_list()), 's05mm', moved('s05mm', 'share', merge=True)), overlay_full=True))
P.frame('S05-moving-some-kept', 'Moving 3 lists; 1 stays on this phone', phone(scene(bg_list(), 's05mk', moving('s05mk', kept=True)), overlay_full=True))
P.frame('S05-moved-some-kept', 'Moved 3 lists; 1 stays on this phone only', phone(scene(backed_up(bg_list()), 's05dk', moved_some_kept('s05dk')), overlay_full=True))

P.section('Move failures', 'Lists are never deleted from the phone until the account confirms them. A partial failure lets sharing continue when the shared list itself moved; a full failure retries automatically when the connection returns.')
P.frame('S05-move-partial', 'Partial failure: 3 of 4 moved', phone(scene(backed_up(bg_list()), 's05p', partial('s05p')), overlay_full=True))
P.frame('S05-move-failed', 'Failure: connection dropped', phone(scene(bg_list(), 's05f', failed('s05f')), overlay_full=True))

P.section('Large text, iOS and web', 'Large text: the sheet becomes full height; the reasons stay and the text scrolls above pinned buttons. iOS: a page sheet with grabber, Sign in with Apple first; Choose lists uses a navigation bar with Back and Done and round iOS checkmarks. Web: lists made without an account live in this browser only ("On this browser only"), and the copy says browsers can clear lists not opened for a while (D-08); Apple is offered through Apple\'s sign-in page (D-13).')
P.frame('S05-share-large-text', 'Large text (200%)', phone(bg_list() + sheet('s05lt', prompt('s05lt', 'share', large=True), pad='pb-12'), overlay_full=True))
P.frame('S05-ios', 'iOS: page sheet, Apple first', phone(scene(bg_list('ios'), 's05i', prompt('s05i', 'share', kind='ios'), kind='ios'), kind='ios', overlay_full=True))
P.frame('S05-ios-choose-lists', 'iOS: Choose lists (Back, Done, round checkmarks)', phone(scene(bg_list('ios'), 's05icl', choose_lists('s05icl', kind='ios'), kind='ios'), kind='ios', overlay_full=True))
P.frame('S05-ios-backup', 'iOS: back up', phone(scene(bg_home('ios'), 's05ib', prompt('s05ib', 'backup', kind='ios'), kind='ios'), kind='ios', overlay_full=True))
web_bg = bg_list(web=True)
P.frame('S05-web', 'Web, mobile browser: lists live in this browser', phone(scene(web_bg, 's05w', prompt('s05w', 'share', web=True), kind='web'), kind='web'))
P.frame('S05-web-backup', 'Web: back up from this browser', phone(scene(bg_home(web=True), 's05wb', prompt('s05wb', 'backup', web=True), kind='web'), kind='web'))
P.frame('S05-web-choose-lists', 'Web: Choose lists (browsers can clear lists)', phone(scene(web_bg, 's05wcl', choose_lists('s05wcl', web=True), kind='web'), kind='web'))
P.frame('S05-web-moving', 'Web: moving lists from this browser', phone(scene(web_bg, 's05wm', moving('s05wm', web=True).replace('data-action="next"', 'data-action="next-web"'), kind='web'), kind='web'))

P.write('S05-sign-in-prompt.html')
