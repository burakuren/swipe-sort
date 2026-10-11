# Usage: python3 tools/generators/S03-sign-in.py  → design/03-screens/S03-sign-in.html
from groupa_common import *

P = Page('S03', 'Sign up / sign in', 'Auth modal stack. Google, Apple and email on every platform (D-13): Apple first on iOS (HIG), Google first on Android and web (A-140). Email has a sign-in form and a create-account form; "Forgot password?" opens S04. Signing in is never required to use SwipeSort alone (ACC-01). Provider marks are stand-ins for the official assets (spec §8).', 'S03-sign-in.md')

CLOSE = 'S02-onboarding.html#S02-welcome'
TERMS = '<p class="text-center text-body-sm text-muted-foreground">By continuing, you agree to the <a href="https://swipesort.app/terms" class="text-primary underline underline-offset-4">Terms of Service</a> and <a href="https://swipesort.app/privacy" class="text-primary underline underline-offset-4">Privacy Policy</a>.</p>'

CONTEXT = {
    'share': ('users', 'Sign in to share “Wedding guests”', 'Members sort the same list on their own phones. Your 4 lists on this phone move to your account.'),
    'backup': ('cloud-upload', 'Sign in to back up your lists', 'Your 4 lists move to your account, so they are safe if you lose this phone.'),
}


def chooser(kind='android', context=None, state=None, large=False, web=False):
    """state: None | 'offline' | 'google-busy' | 'google-failed' | 'cancelled'."""
    off = state == 'offline'
    busy = state == 'google-busy'
    if kind == 'ios':
        top = ios_nav(leading=ios_text_btn('Cancel', CLOSE, action='close'))
    else:
        top = appbar('', back='x', href=CLOSE, label='Close', action='close')
    banner = offline_banner() if off else ''
    if context:
        ic, t, b = CONTEXT[context]
        intro = f'''<div class="mt-6">{alert_info(t, b, ic)}</div>'''
        head = '<h1 class="mt-6 text-title-1">Sign in or create an account</h1>'
    else:
        intro = ''
        tsz = 'text-display' if large else 'text-title-1'
        bsz = 'text-title-3 font-normal' if large else 'text-body-lg'
        head = f'<h1 class="mt-6 {tsz}">Sign in to SwipeSort</h1><p class="mt-2 {bsz} text-muted-foreground">Back up your lists, use them on other devices and decide together with others.</p>'
    err = ''
    if state == 'google-failed':
        err = '<div class="mt-6">' + alert_error("Google sign-in didn't work", 'Check your connection and try again, or continue with email.') + '</div>'
    bsize = 'lg'
    xtra = ' min-h-16 h-auto py-3 text-title-3' if large else ''
    # Apple links where Google does (Android/web: the busy pattern Apple shares, spec §4; iOS: the sheet itself)
    buttons = provider_buttons(kind, google_href='#S03-google-busy' if kind != 'ios' else '#S03-ios',
                               apple_href='#S03-google-busy' if kind != 'ios' else '#S03-ios',
                               email_href='#S03-email' if kind != 'ios' else '#S03-ios-email', off=off,
                               busy='google' if busy else None)
    if large:
        buttons = [b.replace('h-14', 'min-h-16 h-auto py-3').replace('text-label-lg', 'text-title-3') for b in buttons]
    note = ("Your lists stay on this phone. Try again when you're online." if off
            else ("Signing in is optional. Without an account, lists stay in this browser, and browsers can clear lists you haven't opened for a while." if web
                  else 'Signing in is optional. Without an account, lists stay on this phone.'))
    snack = snackbar('Google sign-in cancelled. Choose a way to continue.', bottom='bottom-24') if state == 'cancelled' else ''
    m = '' if large else mark('size-14')
    return f'''{top}
  {banner}
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-2">
    {m}
    {head}
    {intro}
    {err}
    <div class="mt-8 space-y-3">{"".join(buttons)}</div>
    <p class="mt-4 text-center {"text-body-lg" if large else "text-body-sm"} text-muted-foreground">{note}</p>
  </div>
  <div class="shrink-0 px-gutter pb-5 pt-3">{TERMS.replace("text-body-sm", "text-body-lg") if large else TERMS}</div>
  {snack}'''


# ---------------------------------------------------------------- email forms
def form_top(kind, back):
    if kind == 'ios':
        return ios_nav(back_text='Sign in', href=back)
    return appbar('', href=back, label='Back')


def sign_in_form(fid, kind='android', email='deniz.yilmaz@example.com', password='••••••••••', email_state='default',
                 email_err=None, pw_state='default', pw_err=None, alert='', busy=False, offline=False, mode='default'):
    """mode: default | locked (Sign in disabled, no duplicate reset link) | google (account uses Google: Google is the main action)."""
    pw_val = password
    submit = btn('Signing in…', busy=True) if busy else btn('Sign in', href='S08-home.html#S08-default', action='sign-in', disabled=offline or mode == 'locked')
    forgot = '' if mode == 'locked' else f'<div class="mt-1 flex justify-end">{link("Forgot password?", "S04-forgot-password.html#S04-default", "forgot-password")}</div>'
    pw_block = f'''<div>
        {password_field(fid + '-pw', value=pw_val, state=pw_state, error=pw_err)}
        {forgot}
      </div>'''
    if mode == 'google':
        pw_block = ''
        submit = google_btn(href='#S03-google-busy')
    banner = offline_banner() if offline else ''
    return f'''{form_top(kind, '#S03-default' if kind != 'ios' else '#S03-ios')}
  {banner}
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-2">
    <h1 class="text-title-1">Sign in with email</h1>
    {alert}
    <div class="mt-6 space-y-5">
      {field(fid + '-email', 'Email', value=email, type='email', state=email_state, error=email_err, autocomplete='email')}
      {pw_block}
    </div>
    <div class="mt-4">{submit}</div>
    <p class="mt-6 text-center text-body text-muted-foreground">New to SwipeSort? <a href="#S03-sign-up" class="inline-flex min-h-touch items-center text-label-lg text-primary underline underline-offset-4">Create an account</a></p>
  </div>'''


RULES_PARTIAL = [('At least 8 characters', 'met'), ('A number or symbol', 'todo')]
RULES_MET = [('At least 8 characters', 'met'), ('A number or symbol', 'met')]
RULES_FAIL = [('At least 8 characters', 'met'), ('A number or symbol', 'fail')]


def sign_up_form(fid, kind='android', name='Deniz Yılmaz', email='deniz.yilmaz@example.com', pw='sortitout', rules=RULES_PARTIAL,
                 alert='', busy=False, pw_state='focused', shown=True, email_state='default', email_err=None, pw_err=None):
    submit = btn('Creating account…', busy=True) if busy else btn('Create account', href='S08-home.html#S08-default', action='create-account')
    return f'''{form_top(kind, '#S03-email')}
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-2">
    <h1 class="text-title-1">Create an account</h1>
    {alert}
    <div class="mt-6 space-y-5">
      {field(fid + '-name', 'Name', value=name, autocomplete='name', helper='Shown to members of lists you share.')}
      {field(fid + '-email', 'Email', value=email, type='email', autocomplete='email', state=email_state, error=email_err)}
      <div>
        {password_field(fid + '-pw', value=pw, state=pw_state, shown=shown, autocomplete='new-password', error=pw_err)}
        {pw_rules(fid + '-rules', rules)}
      </div>
    </div>
    <div class="mt-6">{submit}</div>
    <p class="mt-4 text-center text-body text-muted-foreground">Already have an account? <a href="#S03-email" class="inline-flex min-h-touch items-center text-label-lg text-primary underline underline-offset-4">Sign in</a></p>
  </div>'''


# ---------------------------------------------------------------- frames
P.section('Choose a way to sign in', 'Android and web: Google, then Apple (Apple\'s outline style, a browser sign-in on these platforms, D-13), then email. The context line appears when S03 opens from a share or backup prompt (S05 › Continue with email).')
P.frame('S03-default', 'Default (Android)', phone(chooser()))
P.frame('S03-context-share', 'Opened from Share: context line', phone(chooser(context='share')))
P.frame('S03-context-backup', 'Opened from Back up: context line', phone(chooser(context='backup')))

P.section('Email', 'One sign-in form and one create-account form; each links to the other. Password rules are shown live while typing. Errors sit under the field they concern, or above the form when they concern the account.')
P.frame('S03-email', 'Sign in with email', phone(sign_in_form('s03e')))
P.frame('S03-signing-in', 'Signing in (loading)', phone(sign_in_form('s03si', busy=True)))
P.frame('S03-sign-up', 'Create an account: password rules update while typing', phone(sign_up_form('s03su')))
P.frame('S03-creating', 'Creating account (loading)', phone(sign_up_form('s03cr', pw='sortitout26', rules=RULES_MET, busy=True, pw_state='default', shown=False)))

P.section('Errors', 'What happened and how to fix it. No apologies, no error codes. Typed values are kept.')
P.frame('S03-error-wrong-password', 'Error: wrong password', phone(sign_in_form('s03wp', pw_state='error', pw_err='Wrong password. Try again or reset it.')))
P.frame('S03-error-invalid-email', 'Error: invalid email', phone(sign_in_form('s03ie', email='deniz.yilmaz@example', email_state='error', email_err='Enter a full email address, like name@example.com.', password='')))
P.frame('S03-error-account-exists', 'Error: account already exists (create account)', phone(sign_up_form('s03ae', pw='sortitout26', rules=RULES_MET, pw_state='default', shown=False,
    alert='<div class="mt-4">' + alert_error('An account with this email already exists', 'Sign in instead. If you forgot the password, you can reset it.', btn('Sign in instead', 'secondary', href='#S03-email', size='md', full=False, action='sign-in-instead')) + '</div>')))
P.frame('S03-error-uses-google', 'Error: this email signs in with Google', phone(sign_in_form('s03ug', password='', mode='google',
    alert='<div class="mt-4">' + alert_neutral('This email signs in with Google', 'Continue with Google to open your account. You can add a password later in Profile.', icon_name='info') + '</div>')))
P.frame('S03-error-weak-password', 'Error on submit: password misses a rule', phone(sign_up_form('s03wk', pw='sortitout', rules=RULES_FAIL, pw_state='error', pw_err='Add a number or symbol to your password.')))
P.frame('S03-error-locked', 'Error: too many attempts', phone(sign_in_form('s03lk', mode='locked',
    alert='<div class="mt-4">' + alert_error('Too many attempts', 'For your security, sign-in is paused for 15 minutes. You can reset your password now.', btn('Reset password', 'secondary', href='S04-forgot-password.html#S04-default', size='md', full=False)) + '</div>')))
P.frame('S03-error-no-connection', 'Error: connection lost while signing in', phone(sign_in_form('s03nc',
    alert='<div class="mt-4">' + alert_error("Couldn't sign in", 'No connection. Check your connection and try again. Your lists stay on this phone.') + '</div>')))

P.section('Google', 'Google opens the system account chooser (out of scope). While it returns, the Google button shows progress and the other options are disabled. Cancelling returns quietly; a failure explains what to do. Apple on Android and web follows the same pattern (busy, cancelled, failed) after its browser page.')
P.frame('S03-google-busy', 'Google: signing in', phone(chooser(state='google-busy')))
P.frame('S03-google-cancelled', 'Google: cancelled in the account chooser', phone(chooser(state='cancelled')))
P.frame('S03-google-failed', 'Google: failed', phone(chooser(state='google-failed')))

P.section('Offline and large text', 'Offline: sign-in buttons are disabled with the reason; the user can close and keep working without an account. Large text: the mark hides, buttons grow and wrap.')
P.frame('S03-offline', 'Offline', phone(chooser(state='offline')))
P.frame('S03-email-offline', 'Offline on the email form', phone(sign_in_form('s03of', offline=True)))
P.frame('S03-large-text', 'Large text (200%)', phone(chooser(large=True)))

P.section('iOS', 'Presented as a page sheet with Cancel. Sign in with Apple comes first (App Store guideline 4.8 and HIG), then Google, then email. The Apple button is the system AppleAuthenticationButton.')
P.frame('S03-ios', 'iOS: Apple first', phone(chooser('ios'), kind='ios'))
P.frame('S03-ios-context-share', 'iOS: opened from Share', phone(chooser('ios', context='share'), kind='ios'))
P.frame('S03-ios-email', 'iOS: sign in with email', phone(sign_in_form('s03ios', kind='ios'), kind='ios'))

P.section('Web', 'Mobile browsers: the Android layout, Apple included (Apple\'s sign-in page opens in a popup on desktop, a redirect on phones). Desktop browsers: the phone column, used by an invited member in prototype flow 3 (Mert opens Deniz\'s link and signs in to join).')
P.frame('S03-web', 'Web, mobile browser', phone(chooser(web=True), kind='web'))

inviter = f'''<div class="mt-6 flex items-center gap-3 rounded-group bg-card p-4 dark:border">
      {avatar(ME['avatar'], size='size-12')}
      <div class="min-w-0 flex-1"><p class="text-body"><span class="font-semibold">Deniz Yılmaz</span> invited you to</p><p class="truncate text-title-3">Wedding guests</p><p class="text-body-sm text-muted-foreground">100 items</p></div>
    </div>'''
web_desk = f'''<header class="flex h-app-bar shrink-0 items-center gap-2 px-gutter">{mark('size-8')}{wordmark('text-title-3')}</header>
  <div class="flex min-h-0 flex-1 flex-col px-gutter pt-4">
    <h1 class="text-title-1">Sign in to join</h1>
    <p class="mt-2 text-body-lg text-muted-foreground">No app needed. You can sort right here in your browser.</p>
    {inviter}
    <div class="mt-8 space-y-3">
      {"".join(provider_buttons('web', google_href='S33-join-list.html#S33-web-desktop', apple_href='S33-join-list.html#S33-web-desktop', email_href='#S03-web-desktop-email'))}
    </div>
    <p class="mt-4 text-center text-body-sm text-muted-foreground">Next, you\'ll see the list and your role before joining.</p>
  </div>
  <div class="shrink-0 px-gutter pb-5 pt-3">{TERMS}</div>'''
P.frame('S03-web-desktop', 'Web, desktop browser: invited member signs in to join', desktop(web_desk, 'swipesort.app/join/7Hq2xK'))

web_desk_email = sign_in_form('s03wde', email='mert.aydin@example.com', password='').replace('href="#S03-default"', 'href="#S03-web-desktop"').replace('S08-home.html#S08-default', 'S33-join-list.html#S33-web-desktop')
P.frame('S03-web-desktop-email', 'Web, desktop browser: email sign-in while joining', desktop(web_desk_email, 'swipesort.app/join/7Hq2xK'))

P.write('S03-sign-in.html')
