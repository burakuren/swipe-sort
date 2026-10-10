# Usage: python3 tools/generators/S05-sign-in-prompt.py  → design/03-screens/S05-sign-in-prompt.html
from groupa_common import *

P = Page('S05', 'Sign-in prompt and moving lists', 'A bottom sheet over the screen that needs an account: Share or Invite on a list (S09, S10), Back up (S06, S08 indicator). It explains why, signs in, then moves every list on this phone to the account and continues the original action. Backgrounds are simplified, non-interactive copies of S09 and S08.', 'S05-sign-in-prompt.md')

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


def bg_home(kind='android', web=False):
    """S08-guest (lists on this phone only; one indicator line under the Lists title)."""
    s = _B['home_guest'](web=web)
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


def prompt(sid, purpose='share', kind='android', state=None, large=False, web=False):
    off = state == 'offline'
    busy = state == 'busy'
    where = 'in this browser' if web else 'on this phone'
    if purpose == 'share':
        ic, title = 'users', 'Sign in to share this list'
        body = 'Sharing needs an account, so members can sort “Wedding guests” on their own devices and see where you agree.'
        points = [('cloud-upload', f'Your 4 lists {where} move to your account and are backed up.'),
                  ('wifi-off', 'Sorting keeps working offline, like now.')]
        not_now = ORIGIN_SHARE
        email_href = 'S03-sign-in.html#S03-context-share'
    else:
        ic, title = 'cloud-upload', 'Sign in to back up your lists'
        body = (f'Your lists are saved in this browser only. If you clear its data, they\'re gone. An account keeps them safe and on every device.' if web else
                'Your lists are saved on this phone only. If you lose it or remove the app, they\'re gone. An account keeps them safe and on every device.')
        points = [('cloud-upload', f'Your 4 lists {where} move to your account.'),
                  ('smartphone', 'Open them on other phones and in the browser.')]
        not_now = ORIGIN_BACKUP
        email_href = 'S03-sign-in.html#S03-context-backup'
    btns = []
    if kind == 'ios':
        btns.append(apple_btn(disabled=off or busy, href='#S05-moving'))
    if busy:
        btns.append(google_btn(busy=True))
    else:
        btns.append(google_btn(href='#S05-moving', action='continue-google', disabled=off))
    btns.append(email_btn(href=email_href, disabled=off or busy))
    btns.append(btn('Not now', 'ghost', href=not_now, action='not-now'))
    if large:
        btns = [b.replace('h-14', 'min-h-16 h-auto py-3').replace('text-label-lg', 'text-title-3') for b in btns]
    banner = ''
    if off:
        banner = f'<div class="mt-4 flex items-start gap-2 rounded-control bg-muted px-3 py-2.5 text-body-sm" role="status">{icon("wifi-off", "size-4 mt-0.5 shrink-0")}<span>You\'re offline. Signing in needs a connection. Your lists stay {where}.</span></div>'
    t = 'text-title-1' if large else 'text-title-2'
    b = 'text-title-3 font-normal' if large else 'text-body'
    pts = '' if large else why_points(points)
    return f'''<div class="pt-3">{round_icon(ic)}</div>
    <h2 id="{sid}-t" class="mt-4 {t}">{title}</h2>
    <p class="mt-2 {b} text-muted-foreground">{body}</p>
    {pts}
    {banner}
    <div class="mt-6 space-y-3">{"".join(btns)}</div>'''


STATUS = {
    'moved': ('circle-check', 'Moved', 'text-foreground'),
    'moving': ('loader-circle', 'Moving…', 'text-primary'),
    'waiting': ('clock', 'Waiting', 'text-muted-foreground'),
    'failed': ('circle-alert', 'Not moved', 'text-destructive'),
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


def moving(sid, web=False):
    where = 'this browser' if web else 'this phone'
    return f'''{signed_in_as()}
    <h2 id="{sid}-t" class="mt-5 text-title-2">Moving your lists to your account</h2>
    <p class="mt-2 text-body text-muted-foreground">Keep SwipeSort open. Each list stays on {where} until it\'s safely in your account.</p>
    <div class="mt-5" role="status">
      <div class="flex items-baseline justify-between"><span class="text-label tabular-nums">2 of 4 moved</span></div>
      <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="2" aria-valuemin="0" aria-valuemax="4" aria-label="2 of 4 lists moved"><div class="h-full w-1/2 rounded-full bg-primary"></div></div>
    </div>
    {list_rows(['moved', 'moved', 'moving', 'waiting'])}
    <a href="#S05-moved" class="sr-only focus:not-sr-only" data-action="next">Finish moving (prototype shortcut: the sheet moves on by itself)</a>'''


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


def partial(sid):
    return f'''<div class="pt-3">{round_icon('circle-alert', 'error')}</div>
    <h2 id="{sid}-t" class="mt-4 text-title-2">3 of 4 lists moved</h2>
    <p class="mt-2 text-body text-muted-foreground">“March photos clean-up” didn\'t move. It\'s still on this phone and nothing is lost. Try again now, or later from Settings › Backup.</p>
    {list_rows(['moved', 'moved', 'failed', 'moved'])}
    <div class="mt-5 space-y-2">{btn('Try again', href='#S05-moving', action='retry')}{btn('Continue to share', 'ghost', href='S31-invite.html#S31-default', action='continue')}</div>'''


def failed(sid):
    return f'''<div class="pt-3">{round_icon('wifi-off', 'error')}</div>
    <h2 id="{sid}-t" class="mt-4 text-title-2">Your lists didn\'t move</h2>
    <p class="mt-2 text-body text-muted-foreground">The connection dropped. You\'re signed in, and all 4 lists are safe on this phone. They move automatically when you\'re back online, or try again now.</p>
    {list_rows(['failed'] * 4)}
    <div class="mt-5 space-y-2">{btn('Try again', href='#S05-moving', action='retry')}{btn('Later', 'ghost', href=ORIGIN_SHARE, action='later')}</div>'''


def scene(bg, sid, content, kind='android', z_top=None):
    if kind == 'ios':
        return f'''{bg}
  {sheet(sid, content, ios=True, pad='pb-6')}'''
    return f'''{bg}
  {sheet(sid, content)}'''


# ---------------------------------------------------------------- frames
P.section('Why sign in', 'Opened when someone without an account taps Share, Invite or Back up. The sheet names the reason, says what happens to their lists, and offers Google and email (Apple first on iOS). "Not now" closes it; nothing changes. Continue with email opens S03 with the same context line.')
P.frame('S05-share', 'Share: why an account is needed', phone(scene(bg_list(), 's05s', prompt('s05s', 'share'))))
P.frame('S05-backup', 'Back up: why an account is needed', phone(scene(bg_home(), 's05b', prompt('s05b', 'backup'))))
P.frame('S05-signing-in', 'Signing in with Google', phone(scene(bg_list(), 's05g', prompt('s05g', 'share', state='busy'))))
P.frame('S05-offline', 'Offline: sign-in disabled with the reason', phone(scene(bg_list(), 's05o', prompt('s05o', 'share', state='offline'))))

P.section('Moving lists to the account', 'Right after sign-in, every list on this phone moves to the account, one by one, newest activity first. Each list stays usable locally the whole time. When the move finishes, the original action continues: Share opens the invite (S31); Back up returns to the backup page (S06).')
P.frame('S05-moving', 'Moving 4 lists (progress)', phone(scene(bg_list(), 's05m', moving('s05m'))))
P.frame('S05-moved', 'Moved: continue to share', phone(scene(bg_list(), 's05d', moved('s05d', 'share'))))
P.frame('S05-moved-backup', 'Moved: from Back up', phone(scene(bg_home(), 's05db', moved('s05db', 'backup'))))
P.frame('S05-moved-merge', 'Moved into an account that already has lists', phone(scene(bg_list(), 's05mm', moved('s05mm', 'share', merge=True))))

P.section('Move failures', 'Lists are never deleted from the phone until the account confirms them. A partial failure lets sharing continue when the shared list itself moved; a full failure retries automatically when the connection returns.')
P.frame('S05-move-partial', 'Partial failure: 3 of 4 moved', phone(scene(bg_list(), 's05p', partial('s05p'))))
P.frame('S05-move-failed', 'Failure: connection dropped', phone(scene(bg_list(), 's05f', failed('s05f'))))

P.section('Large text, iOS and web', 'Large text: the reasons list hides, buttons grow and the sheet becomes full height. iOS: a page sheet with grabber, Sign in with Apple first. Web: lists made without an account live in this browser only ("On this browser only"); Apple is not offered.')
P.frame('S05-share-large-text', 'Large text (200%)', phone(scene(bg_list(), 's05lt', prompt('s05lt', 'share', large=True))))
P.frame('S05-ios', 'iOS: page sheet, Apple first', phone(scene(bg_list('ios'), 's05i', prompt('s05i', 'share', kind='ios'), kind='ios'), kind='ios'))
P.frame('S05-ios-backup', 'iOS: back up', phone(scene(bg_home('ios'), 's05ib', prompt('s05ib', 'backup', kind='ios'), kind='ios'), kind='ios'))
web_bg = bg_list(web=True)
P.frame('S05-web', 'Web, mobile browser: lists live in this browser', phone(scene(web_bg, 's05w', prompt('s05w', 'share', web=True)), kind='web'))
P.frame('S05-web-backup', 'Web: back up from this browser', phone(scene(bg_home(web=True), 's05wb', prompt('s05wb', 'backup', web=True)), kind='web'))
P.frame('S05-web-moving', 'Web: moving lists from this browser', phone(scene(web_bg, 's05wm', moving('s05wm', web=True).replace('data-action="next"', 'data-action="next-web"')), kind='web'))

P.write('S05-sign-in-prompt.html')
