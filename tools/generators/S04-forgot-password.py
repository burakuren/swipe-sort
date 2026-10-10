# Usage: python3 tools/generators/S04-forgot-password.py  → design/03-screens/S04-forgot-password.html
from groupa_common import *

P = Page('S04', 'Forgot password', 'From S03 "Forgot password?". Request a reset link, then set a new password from the email link (in the app when installed, otherwise on the web). The "sent" message never reveals whether an account exists.', 'S04-forgot-password.md')

BACK = 'S03-sign-in.html#S03-email'
EMAIL = 'deniz.yilmaz@example.com'


def badge_icon(name, tone='primary'):
    cls = 'bg-primary-soft text-primary-soft-foreground' if tone == 'primary' else ('bg-muted text-muted-foreground' if tone == 'muted' else 'bg-secondary text-foreground')
    return f'<span class="flex size-14 items-center justify-center rounded-full {cls}">{icon(name, "size-6")}</span>'


def request(fid, kind='android', value=EMAIL, state='default', err=None, busy=False, offline=False, alert=''):
    top = ios_nav(back_text='Sign in', href=BACK) if kind == 'ios' else appbar('', href=BACK, label='Back to sign in')
    banner = offline_banner("You're offline. Sending a reset link needs a connection.") if offline else ''
    submit = btn('Sending…', busy=True) if busy else btn('Send reset link', href='#S04-sent', action='send-link', disabled=offline)
    return f'''{top}
  {banner}
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-2">
    <h1 class="text-title-1">Reset your password</h1>
    <p class="mt-2 text-body-lg text-muted-foreground">Enter the email you use for SwipeSort. We\'ll send a link to set a new password.</p>
    {alert}
    <div class="mt-6">{field(fid, 'Email', value=value, type='email', state=state, error=err, autocomplete='email')}</div>
    <div class="mt-6">{submit}</div>
  </div>'''


def sent(kind='android', large=False, snack='', cooldown=True):
    top = ios_nav(back_text='Sign in', href=BACK) if kind == 'ios' else appbar('', back='x', href=BACK, label='Close')
    t = 'text-display' if large else 'text-title-1'
    b = 'text-title-3 font-normal' if large else 'text-body-lg'
    again = (f'<button type="button" class="inline-flex min-h-touch items-center text-label-lg text-primary opacity-50" disabled>Send again in <span class="ml-1 tabular-nums">0:42</span></button>'
             if cooldown else link('Send again', '#S04-resent', 'send-again'))
    return f'''{top}
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-6">
    {badge_icon('mail-check')}
    <h1 class="mt-6 {t}">Check your email</h1>
    <p class="mt-2 {b} text-muted-foreground">If <span class="text-foreground">{EMAIL}</span> has a SwipeSort account, a link to reset its password is on the way. The link works for 1 hour.</p>
    <p class="mt-4 {"text-body-lg" if large else "text-body"} text-muted-foreground">No email after a few minutes? Check your spam folder, or check that the address is right.</p>
    <div class="mt-1">{again}</div>
  </div>
  <div class="shrink-0 space-y-2 px-gutter pb-4 pt-3">
    {btn('Open email app', href='#S04-new-password', action='open-email')}
    {btn('Back to sign in', 'ghost', href=BACK, action='back-to-sign-in')}
  </div>
  {snack}'''


RULES = [('At least 8 characters', 'met'), ('A number or symbol', 'met')]


def new_password(fid, kind='android', value='Sortitout2026', rules=RULES, state='focused', err=None, busy=False, shown=True, offline=False, alert=''):
    top = ios_nav(leading=ios_text_btn('Cancel', BACK)) if kind == 'ios' else appbar('', back='x', href=BACK, label='Close')
    if kind == 'desktop':
        top = f'<header class="flex h-app-bar shrink-0 items-center gap-2 px-gutter">{mark("size-8")}{wordmark("text-title-3")}</header>'
    banner = offline_banner("You're offline. Saving a new password needs a connection.") if offline else ''
    submit = btn('Saving…', busy=True) if busy else btn('Save password', href='#S04-success' if kind != 'desktop' else '#S04-web-desktop-success', action='save-password', disabled=offline)
    return f'''{top}
  {banner}
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-2">
    <h1 class="text-title-1">Set a new password</h1>
    <p class="mt-2 text-body-lg text-muted-foreground">For {EMAIL}</p>
    {alert}
    <div class="mt-6">
      {password_field(fid, 'New password', value=value, state=state, error=err, shown=shown, autocomplete='new-password')}
      {pw_rules(fid + '-rules', rules)}
    </div>
    <div class="mt-6">{submit}</div>
  </div>'''


def message(ic, title, body, primary, secondary=None, kind='android', tone='primary', close=BACK):
    top = ios_nav(leading=ios_text_btn('Close', close)) if kind == 'ios' else appbar('', back='x', href=close, label='Close')
    if kind == 'desktop':
        top = f'<header class="flex h-app-bar shrink-0 items-center gap-2 px-gutter">{mark("size-8")}{wordmark("text-title-3")}</header>'
    sec = secondary or ''
    return f'''{top}
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-6">
    {badge_icon(ic, tone)}
    <h1 class="mt-6 text-title-1">{title}</h1>
    <p class="mt-2 text-body-lg text-muted-foreground">{body}</p>
  </div>
  <div class="shrink-0 space-y-2 px-gutter pb-4 pt-3">{primary}{sec}</div>'''


# ---------------------------------------------------------------- frames
P.section('Request a reset link', 'The email field is prefilled from the sign-in form. Validation happens on submit; the button shows progress while sending.')
P.frame('S04-default', 'Default: enter email', phone(request('s04d')))
P.frame('S04-sending', 'Sending', phone(request('s04s', busy=True)))
P.frame('S04-invalid-email', 'Error: invalid email', phone(request('s04ie', value='deniz.yilmaz@', state='error', err='Enter a full email address, like name@example.com.')))
P.frame('S04-offline', 'Offline', phone(request('s04of', offline=True)))
P.frame('S04-send-failed', 'Error: connection lost while sending', phone(request('s04sf', alert='<div class="mt-6">' + alert_error("Couldn't send the link", 'No connection. Check your connection and try again.') + '</div>')))

P.section('Link sent', 'Same message whether or not the address has an account (no account enumeration). "Send again" unlocks after 60 seconds. "Open email app" opens the default mail app (Android intent, iOS mail URL); the prototype jumps to the new-password step.')
P.frame('S04-sent', 'Sent: check your email', phone(sent()))
P.frame('S04-resent', 'Sent again (after the cooldown)', phone(sent(cooldown=True, snack=snackbar('Sent again. Check your email.', bottom='bottom-40'))))

P.section('Set a new password', 'Opened from the email link: in the app when installed (App Link / Universal Link), otherwise in the browser. Same password rules as sign-up.')
P.frame('S04-new-password', 'New password (opened from the email link)', phone(new_password('s04np')))
P.frame('S04-new-password-weak', 'Error: password misses a rule', phone(new_password('s04wk', value='sortit', rules=[('At least 8 characters', 'fail'), ('A number or symbol', 'fail')], state='error',
    err='Use at least 8 characters, with a number or symbol.')))
P.frame('S04-saving', 'Saving', phone(new_password('s04sv', busy=True, state='default', shown=False)))
P.frame('S04-new-password-offline', 'Offline while setting a password', phone(new_password('s04npo', state='default', shown=False, offline=True)))
P.frame('S04-success', 'Password changed', phone(message('circle-check', 'Password changed',
    'Sign in with your new password. For your security, you\'re signed out on your other devices.',
    btn('Sign in', href=BACK, action='sign-in'), tone='secondary')))
P.frame('S04-expired', 'Error: link expired or already used', phone(message('hourglass', 'This link has expired',
    'Reset links work for 1 hour and only once. Request a new link to set your password.',
    btn('Send a new link', href='#S04-default', action='send-new-link'), btn('Back to sign in', 'ghost', href=BACK), tone='muted')))

P.section('iOS, web and large text', 'iOS: back chevron to Sign in; the new-password screen opens as a modal with Cancel. Web: the same steps in the phone column; after a reset on desktop the person can continue in the browser or on their phone.')
P.frame('S04-ios', 'iOS: enter email', phone(request('s04ios', kind='ios'), kind='ios'))
P.frame('S04-ios-new-password', 'iOS: new password', phone(new_password('s04iosnp', kind='ios'), kind='ios'))
P.frame('S04-web-desktop', 'Web, desktop browser: link opened without the app', desktop(new_password('s04wd', kind='desktop'), 'swipesort.app/reset?token=…'))
P.frame('S04-web-desktop-success', 'Web, desktop browser: password changed', desktop(message('circle-check', 'Password changed',
    'Sign in with your new password here, or in the SwipeSort app on your phone.',
    btn('Sign in', href=BACK, action='sign-in'), kind='desktop', tone='secondary'), 'swipesort.app/reset/done'))
P.frame('S04-large-text', 'Large text (200%): link sent', phone(sent(large=True)))

P.write('S04-forgot-password.html')
