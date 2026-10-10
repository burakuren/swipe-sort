# Usage: python3 tools/generators/S06-settings.py  → design/03-screens/S06-settings.html
from groupa_common import *

P = Page('S06', 'Settings', 'The Settings tab and every sub-page: profile entry, backup, card templates, appearance, haptics, notifications, language, privacy, help and feedback, about, sign out. Signed-in and not-signed-in variants, offline, large text, iOS and web.', 'S06-settings.md')

S = '#S06-default'


def body(content, extra=''):
    return f'<div class="min-h-0 flex-1 space-y-6 overflow-hidden px-4 pb-6 pt-2 {extra}">{content}</div>'


def sub(title, content, back=S, actions='', top=''):
    return f'''{appbar(title, href=back, label='Back to Settings', action='back')}
  {top}
  {body(content)}'''


def profile_row(ios=False, href='S07-profile.html#S07-default'):
    av = avatar(ME['avatar'], size='size-14')
    return group([nav_row(ME['name'], href=href, avatar=av, desc=ME['email'], title_cls='text-title-3', action='profile',
                          aria=f"{ME['name']}, {ME['email']}. Profile and account")], ios=ios)


def textarea(fid, label, value='', placeholder='', counter='0 / 2,000', state='default', rows=5):
    b = 'border border-primary ring-2 ring-ring/30' if state == 'focused' else 'border border-input'
    ph = f' placeholder="{esc(placeholder)}"' if placeholder else ''
    return f'''<div><label for="{fid}" class="text-label">{label}</label>
      <textarea id="{fid}" rows="{rows}" class="mt-1.5 w-full resize-none rounded-control {b} bg-card px-3.5 py-3 text-body placeholder:text-muted-foreground"{ph} aria-describedby="{fid}-c">{esc(value)}</textarea>
      <div class="mt-1 flex justify-end"><span id="{fid}-c" class="text-caption tabular-nums text-muted-foreground">{counter}</span></div></div>'''


def segmented(label, options, selected):
    out = []
    for o in options:
        if o == selected:
            out.append(f'<button type="button" role="radio" aria-checked="true" class="h-10 flex-1 rounded-full bg-card text-label shadow-raised">{o}</button>')
        else:
            out.append(f'<button type="button" role="radio" aria-checked="false" class="h-10 flex-1 rounded-full text-label text-muted-foreground">{o}</button>')
    return f'<div><p id="seg-{label}" class="text-label">{label}</p><div class="mt-1.5 flex rounded-full bg-secondary p-1" role="radiogroup" aria-labelledby="seg-{label}">{"".join(out)}</div></div>'


def status_block(ic, tone, title, text, extra=''):
    tones = {'ok': 'bg-primary-soft text-primary-soft-foreground', 'muted': 'bg-muted text-muted-foreground',
             'error': 'bg-card text-destructive border border-destructive/40'}
    return f'''<div class="flex flex-col items-center px-4 pb-2 pt-4 text-center" role="status">
      <span class="flex size-14 items-center justify-center rounded-full {tones[tone]}">{icon(ic, "size-6 " + extra)}</span>
      <h2 class="mt-4 text-title-2">{title}</h2>
      <p class="mt-1 max-w-xs text-body text-muted-foreground">{text}</p>
    </div>'''


# ---------------------------------------------------------------- root
EVENTS = [
    ('Someone joins a list', 'user-plus'),
    ('Someone finishes sorting', 'flag'),
    ('New conflicts', 'git-compare-arrows'),
    ('Conflicts resolved', 'check-check'),
    ('A new round starts', 'play'),
    ('Your role changes', 'user-cog'),
]


def root_groups(state='signed-in', haptics_web=False, notif_value='On', ios=False, end=False):
    """state: signed-in | offline | guest"""
    g = []
    if state == 'guest':
        g.append(f'''<section class="rounded-group bg-card p-4 dark:border">
      <div class="flex gap-4">{icon("cloud-off", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1">
        <h2 class="text-title-3">Sign in to back up and share</h2>
        <p class="mt-1 text-body-sm text-muted-foreground">Your 4 lists are on this phone only. With an account they're backed up, and you can decide together with others.</p>
      </div></div>
      <div class="mt-4">{btn("Sign in", "primary", href="S05-sign-in-prompt.html#S05-backup", action="sign-in", size="md")}</div>
    </section>''')
    else:
        g.append(profile_row(ios))
    if state == 'guest':
        backup = nav_row('Backup', href='#S06-backup-guest', icon_name='cloud-off', desc='Not backed up. Lists are on this phone only.', action='backup')
    elif state == 'offline':
        backup = nav_row('Backup', href='#S06-backup-failed', icon_name='cloud-off', desc='Paused while offline', action='backup')
    else:
        backup = nav_row('Backup', href='#S06-backup', icon_name='cloud-check', desc='Backed up today at 09:12', action='backup')
    g.append(group([backup, nav_row('Card templates', href='S22-template-library.html#S22-default', icon_name='layout-template', desc='Built-in and your own', action='card-templates')], header='Lists', ios=ios))
    if haptics_web:
        hap = switch_row('Haptics', False, icon_name='vibrate', unavailable=('Haptics need the Android or iOS app.', '#S06-web-get-app'))
    else:
        hap = switch_row('Haptics', True, icon_name='vibrate', desc='Vibrate when you decide')
    notif_href = '#S06-notifications-web' if haptics_web else '#S06-notifications'
    g.append(group([
        nav_row('Appearance', href='#S06-appearance', icon_name='palette', value='System', action='appearance'),
        hap,
        nav_row('Notifications', href=notif_href, icon_name='bell', value=notif_value, action='notifications'),
        nav_row('Language', href='#S06-language', icon_name='languages', value='English', action='language'),
    ], header='Preferences', ios=ios))
    g.append(group([
        nav_row('Privacy', href='#S06-privacy', icon_name='shield-check', action='privacy'),
        nav_row('Help and feedback', href='#S06-help', icon_name='life-buoy', action='help'),
        nav_row('About', href='#S06-about', icon_name='info', value='1.0.0', action='about'),
    ], header='Support', ios=ios))
    if state != 'guest':
        g.append(group([button_row('Sign out', icon_name='log-out', href='#S06-sign-out', action='sign-out')], ios=ios))
    g.append('<p class="pb-2 text-center text-caption text-muted-foreground">SwipeSort 1.0.0 (142)</p>')
    return ''.join(g)


def root(state='signed-in', top='', haptics_web=False, notif_value='On', scrolled=False, nav=True, overlay=''):
    head = large_title('Settings') if not scrolled else appbar('Settings', back=None)
    content = root_groups(state, haptics_web, notif_value)
    # scrolled: content translated up to show the end of the page
    inner = f'<div class="space-y-6 {"-translate-y-96" if scrolled else ""}">{content}</div>'
    return f'''{head}
  {top}
  <div class="min-h-0 flex-1 overflow-hidden px-4 pb-6 {"pt-0" if state == "offline" and not scrolled else "pt-2"}">{inner}</div>
  {bottom_nav('settings') if nav else ''}
  {overlay}'''


P.section('Settings root', 'Top-level tab (bottom navigation: Lists, Activity, Settings). Groups are flat card surfaces with inset rows; the profile row opens S07. Haptics is a switch right on the root: one control does not need its own page.')
P.frame('S06-default', 'Default (signed in)', phone(root()))
P.frame('S06-default-end', 'Scrolled to the end: support and sign out', phone(root(scrolled=True)))
P.frame('S06-guest', 'Not signed in: sign-in row and not-backed-up indicator', phone(root('guest', notif_value='Off')))
P.frame('S06-offline', 'Offline: backup waits, everything else works', phone(root('offline', top=offline_banner("You're offline. Changes are saved on this phone."))))

# sign-out dialogs over the scrolled root
signout = dialog('so', 'Sign out?', f"Your lists are backed up to {ME['email']}. They'll be removed from this phone until you sign in again.",
                 dlg_btn('Cancel', href='#S06-default-end', action='cancel') + dlg_btn('Sign out', 'primary', href='S08-home.html#S08-first-run', action='confirm-sign-out'))
P.frame('S06-sign-out', 'Sign out: confirmation', phone(root(scrolled=True, overlay=signout)))
unsynced = dialog('su', 'Sign out without backing up?', "12 changes haven't been backed up because you're offline. Signing out now removes them from this phone, and they can't be recovered.",
                  dlg_btn('Cancel', href='#S06-offline', action='cancel') + dlg_btn('Sign out anyway', 'destructive', href='S08-home.html#S08-first-run', action='confirm-sign-out'))
P.frame('S06-sign-out-unsynced', 'Sign out with changes not backed up', phone(root('offline', top=offline_banner("You're offline. Changes are saved on this phone."), scrolled=True, overlay=unsynced)))

# ---------------------------------------------------------------- appearance, language
P.section('Preferences', 'Appearance (theme), notifications and language. Changes apply immediately; there is no Save button.')
P.frame('S06-appearance', 'Appearance: theme', phone(sub('Appearance', radio_group('theme', [
    ('System', "Match your phone's light or dark setting", True),
    ('Light', None, False),
    ('Dark', None, False)], 'Theme') + '<p class="px-1 text-body-sm text-muted-foreground">Applies right away on this device.</p>')))

lang = radio_group('lang', [('English', None, True)], 'Language') + alert_info('English only for now', 'More languages are coming, starting with Turkish. SwipeSort will switch automatically when your phone’s language is available.', icon_name='languages')
P.frame('S06-language', 'Language: English only for now', phone(sub('Language', lang)))


# ---------------------------------------------------------------- notifications
def event_rows(on=True, disabled=False):
    return [switch_row(t, on, icon_name=i, disabled=disabled) for t, i in EVENTS]


notif = (group([switch_row('Push notifications', True, icon_name='bell', desc='On this phone')])
         + group(event_rows(), header='Notify me when',
                 footer='Activity always shows every event, whatever you choose here.'))
P.frame('S06-notifications', 'Notifications: push on, per-event preferences', phone(sub('Notifications', notif)))

not_asked = (f'''<section class="rounded-group bg-card p-4 dark:border">
      <div class="flex gap-4">{icon("bell", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<div class="min-w-0 flex-1">
        <h2 class="text-title-3">Turn on push notifications</h2>
        <p class="mt-1 text-body-sm text-muted-foreground">Hear when someone joins, finishes sorting or a conflict needs you. Choose which events below.</p></div></div>
      <div class="mt-4">{btn("Turn on notifications", "primary", href="S12-permissions.html#S12-notifications", action="turn-on-notifications", size="md")}</div>
    </section>'''
             + group(event_rows(), header='Notify me when', footer='These apply once push notifications are on. Activity always shows every event.'))
P.frame('S06-notifications-not-asked', 'Notifications: permission not asked yet', phone(sub('Notifications', not_asked)))

denied = (alert_neutral("Notifications are off in your phone's settings",
                        "Turn them on for SwipeSort in Android settings to get push notifications. Activity still shows every event.",
                        icon_name='bell-off', action=link('Open phone settings', '#S06-notifications', action='open-system-settings'))
          + group(event_rows(disabled=True), header='Notify me when'))
P.frame('S06-notifications-denied', 'Notifications: blocked in system settings', phone(sub('Notifications', denied)))

notif_web = (alert_neutral('Push notifications need the app',
                           'In the browser, new events appear in Activity and as a badge while SwipeSort is open.',
                           action=link('Get the app', '#S06-web-get-app', action='get-app'))
             + group(event_rows(), header='Show in Activity with a badge',
                     footer="Events you turn off still appear in Activity, without a badge."))
P.frame('S06-notifications-web', 'Notifications on web: in-app only', phone(sub('Notifications', notif_web), kind='web'))

# ---------------------------------------------------------------- backup
P.section('Backup', 'Signed-in lists back up automatically whenever the phone is online. Backup states: backed up, backing up, paused (failed or offline), and not backed up (no account).')
acct_rows = [
    nav_row('Account', href='S07-profile.html#S07-default', icon_name='circle-user-round', desc=ME['email'], trailing=''),
]


def backup_page(status, rows, action_html):
    return sub('Backup', status + group(rows) + action_html)


P.frame('S06-backup', 'Backup: backed up', phone(backup_page(
    status_block('cloud-check', 'ok', 'Backed up', 'Last backup today at 09:12. Lists back up automatically whenever you’re online.'),
    acct_rows + [nav_row('Lists', href='S08-home.html#S08-default', icon_name='list-checks', value='4', trailing=''),
                 nav_row('Changes waiting', href='#S06-backup', icon_name='clock', value='None', trailing='')],
    btn('Back up now', 'secondary', size='md', action='back-up'))))

P.frame('S06-backup-syncing', 'Backup: backing up', phone(backup_page(
    status_block('refresh-cw', 'ok', 'Backing up…', 'Backing up 12 changes. You can keep using SwipeSort.', extra='animate-spin'),
    acct_rows + [nav_row('Lists', href='S08-home.html#S08-default', icon_name='list-checks', value='4', trailing=''),
                 nav_row('Changes waiting', href='#S06-backup-syncing', icon_name='clock', value='12', trailing='')],
    btn('Backing up…', 'secondary', size='md', busy=True))))

P.frame('S06-backup-failed', 'Backup: paused (failed)', phone(backup_page(
    status_block('cloud-alert', 'error', 'Backup paused', "SwipeSort couldn't reach its servers. Your 12 changes are saved on this phone and back up automatically when the connection works again."),
    acct_rows + [nav_row('Last backup', href='#S06-backup-failed', icon_name='history', value='Yesterday', trailing=''),
                 nav_row('Changes waiting', href='#S06-backup-failed', icon_name='clock', value='12', trailing='')],
    btn('Try again', 'secondary', size='md', action='retry'))))

device_rows = [f'<li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon(ic, "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block truncate text-body">{n}</span><span class="block text-body-sm text-muted-foreground">{c} items</span></span></li>' for n, c, ic in DEVICE_LISTS]
P.frame('S06-backup-guest', 'Backup: not signed in (not backed up)', phone(sub('Backup',
    status_block('cloud-off', 'muted', 'Not backed up', 'Your 4 lists are saved on this phone only. Sign in to back them up and open them on other devices.')
    + f'<div>{btn("Sign in to back up", "primary", href="S05-sign-in-prompt.html#S05-backup", action="sign-in")}</div>'
    + group(device_rows, header='On this phone only'))))

# ---------------------------------------------------------------- privacy
P.section('Privacy, help and about', 'Plain-language privacy information, help, feedback, version and licenses. External pages open in the in-app browser (marked with an external-link icon).')


def prose(items):
    return '<div class="space-y-5 px-1">' + ''.join(f'<section><h2 class="text-title-3">{h}</h2><p class="mt-1 max-w-prose text-body text-muted-foreground">{t}</p></section>' for h, t in items) + '</div>'


privacy = prose([
    ('What SwipeSort keeps', 'The lists you make: items, fields, decisions and notes. If you sign in, also your name, email and photo.'),
    ('Contacts and photos', 'SwipeSort reads only the contacts or photos you choose to import, and keeps only the fields you map.'),
    ('Shared lists', 'Members of a shared list see its items, everyone’s decisions and notes. Notes marked private are visible only to you.'),
    ('Your original files', 'Imported files and Google Sheets are never changed unless you confirm an export to them.'),
]) + group([
    nav_row('Privacy policy', href='#S06-privacy', icon_name='shield-check', external=True),
    nav_row('Terms of service', href='#S06-privacy', icon_name='file-text', external=True),
    nav_row('Delete account', href='S07-profile.html#S07-default', icon_name='trash-2', destructive=True, desc='From your profile', action='delete-account'),
])
P.frame('S06-privacy', 'Privacy', phone(sub('Privacy', privacy)))


def help_page(overlay=''):
    return sub('Help and feedback', group([
        nav_row('Replay the introduction', href='S02-onboarding.html#S02-welcome', icon_name='graduation-cap', desc='See the gesture demo again', action='replay-intro'),
        nav_row('Help center', href='#S06-help', icon_name='book-open', desc='Guides and answers', external=True),
    ]) + group([
        nav_row('Send feedback', href='#S06-feedback', icon_name='message-square-text', desc='Ideas and suggestions', action='send-feedback'),
        nav_row('Report a problem', href='#S06-feedback', icon_name='bug', desc='Something isn’t working', action='report-problem'),
        nav_row('Email support', href='#S06-help', icon_name='mail', desc='support@swipesort.app', external=True),
    ], header='Contact us')) + overlay


P.frame('S06-help', 'Help and feedback', phone(help_page()))


def feedback(top='', alert='', btn_html=None, value='Could the Maybe pile show how often I skipped an item? I keep going back and forth on the same ones.'):
    n = len(value)
    form = f'''{segmented('Type', ['Idea', 'Problem', 'Other'], 'Idea')}
    {textarea('fb-msg', 'Message', value=value, placeholder='What would make SwipeSort better?', counter=f'{n} / 2,000', state='focused')}
    {group([switch_row('Include device details', True, desc='App version, phone model and system version. No lists or contacts.')])}
    <p class="px-1 text-body-sm text-muted-foreground">We reply to {ME['email']}.</p>
    {alert}'''
    b = btn_html or btn('Send feedback', 'primary', href='#S06-feedback-sent', action='send')
    return f'''{appbar('Send feedback', href='#S06-help', label='Back to Help and feedback', action='back')}
  {top}
  {body(form, 'space-y-5')}
  <div class="shrink-0 px-gutter pb-4 pt-2">{b}</div>'''


P.frame('S06-feedback', 'Send feedback: form', phone(feedback()))
P.frame('S06-feedback-sent', 'Feedback sent (back on Help)', phone(help_page(snackbar('Feedback sent. Thanks for helping improve SwipeSort.', bottom='bottom-6')).replace('Help and feedback</h1>', 'Help and feedback</h1>', 1)))
P.frame('S06-feedback-error', "Feedback couldn't send: offline", phone(feedback(
    top=offline_banner("You're offline."),
    alert=alert_error("Couldn't send your feedback", "You're offline. Your message stays here; send it when you're back online."),
    btn_html=btn('Try again', 'primary', action='retry'))))

about = f'''<div class="flex flex-col items-center pb-2 pt-6 text-center">{mark('size-16')}<p class="mt-3 text-title-2">SwipeSort</p><p class="mt-1 text-body text-muted-foreground">Version 1.0.0 (142)</p></div>''' + group([
    nav_row('Terms of service', href='#S06-about', icon_name='file-text', external=True),
    nav_row('Privacy policy', href='#S06-about', icon_name='shield-check', external=True),
    nav_row('Open-source licenses', href='#S06-licenses', icon_name='scale', action='licenses'),
]) + group([nav_row('Rate SwipeSort', href='#S06-about', icon_name='star', desc='On Google Play', external=True)])
P.frame('S06-about', 'About', phone(sub('About', about)))

LIBS = [('Expo', 'MIT'), ('React Native', 'MIT'), ('React Native Reusables', 'MIT'), ('NativeWind', 'MIT'),
        ('react-native-gesture-handler', 'MIT'), ('react-native-reanimated', 'MIT'), ('expo-haptics', 'MIT'),
        ('Inter typeface', 'SIL Open Font License 1.1'), ('Lucide icons', 'ISC')]
licenses = '<p class="px-1 text-body text-muted-foreground">SwipeSort is built with these open-source projects. Tap one to read its license.</p>' + group(
    [nav_row(n, href='#S06-licenses', desc=l) for n, l in LIBS])
P.frame('S06-licenses', 'Open-source licenses', phone(f'''{appbar('Open-source licenses', href='#S06-about', label='Back to About', action='back')}
  {body(licenses)}'''))

# ---------------------------------------------------------------- accessibility
P.section('Accessibility', 'At 200% font size rows grow, values move under the title instead of beside it, and nothing truncates except the email address.')


def big_row(title, ic, value=None, href='#', switch_on=None):
    v = f'<span class="block text-body-lg text-muted-foreground">{value}</span>' if value else ''
    tr = switch(switch_on, title) if switch_on is not None else icon('chevron-right', 'size-6 shrink-0 text-muted-foreground')
    if switch_on is not None:
        return f'<li class="flex min-h-16 items-center gap-4 px-4 py-4">{icon(ic, "size-6 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-title-2 font-normal">{title}</span>{v}</span>{tr}</li>'
    return f'<li><a href="{href}" class="flex min-h-16 items-center gap-4 px-4 py-4">{icon(ic, "size-6 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-title-2 font-normal">{title}</span>{v}</span>{tr}</a></li>'


big = f'''<header class="shrink-0"><div class="h-6"></div><h1 class="px-gutter pb-3 text-display">Settings</h1></header>
  <div class="min-h-0 flex-1 space-y-6 overflow-hidden px-4 pb-6">
    <ul class="overflow-hidden rounded-group bg-card dark:border"><li><a href="S07-profile.html#S07-default" class="flex min-h-16 items-center gap-4 px-4 py-4">{avatar(ME['avatar'], size='size-14')}<span class="min-w-0 flex-1"><span class="block text-title-2">{ME['name']}</span><span class="block truncate text-body-lg text-muted-foreground">{ME['email']}</span></span>{icon('chevron-right', 'size-6 shrink-0 text-muted-foreground')}</a></li></ul>
    <section><h2 class="px-1 pb-2 text-title-3 text-muted-foreground">Lists</h2><ul class="divide-y overflow-hidden rounded-group bg-card dark:border">
      {big_row('Backup', 'cloud-check', 'Backed up today at 09:12', '#S06-backup')}
      {big_row('Card templates', 'layout-template', None, 'S22-template-library.html#S22-default')}
    </ul></section>
    <section><h2 class="px-1 pb-2 text-title-3 text-muted-foreground">Preferences</h2><ul class="divide-y overflow-hidden rounded-group bg-card dark:border">
      {big_row('Appearance', 'palette', 'System', '#S06-appearance')}
      {big_row('Haptics', 'vibrate', 'Vibrate when you decide', switch_on=True)}
    </ul></section>
  </div>
  <nav class="flex h-24 shrink-0 border-t bg-card" aria-label="Main">
    <a href="S08-home.html#S08-default" class="flex flex-1 flex-col items-center justify-center gap-1 text-label text-muted-foreground">{icon('list-checks', 'size-7')}Lists</a>
    <a href="S38-activity.html#S38-default" class="flex flex-1 flex-col items-center justify-center gap-1 text-label text-muted-foreground" aria-label="Activity, 3 unread">{icon('activity', 'size-7')}Activity</a>
    <a href="#S06-large-text" class="flex flex-1 flex-col items-center justify-center gap-1 text-label font-semibold" aria-current="page"><span class="flex h-9 w-16 items-center justify-center rounded-full bg-primary-soft text-primary-soft-foreground">{icon('settings', 'size-7')}</span>Settings</a>
  </nav>'''
P.frame('S06-large-text', 'Large text (200%)', phone(big))

# ---------------------------------------------------------------- iOS
P.section('iOS', 'Inset grouped lists, a large title that collapses on scroll, the iOS tab bar, and back chevrons with the previous title (edge swipe goes back). Sign out confirms with an action sheet.')


def ios_root(overlay=''):
    content = root_groups(ios=True).replace('Rate SwipeSort', 'Rate SwipeSort')
    return f'''{ios_nav(large='Settings')}
  <div class="min-h-0 flex-1 space-y-6 overflow-hidden px-4 pb-6 pt-2">{content}</div>
  {ios_tab_bar('settings')}
  {overlay}'''


P.frame('S06-ios', 'iOS settings root', phone(ios_root(), kind='ios'))
ios_notif = (group([switch_row('Push notifications', True, icon_name='bell', desc='On this iPhone')], ios=True)
             + group(event_rows(), header='Notify me when', footer='Activity always shows every event, whatever you choose here.', ios=True))
P.frame('S06-ios-notifications', 'iOS sub-page: notifications', phone(f'''{ios_nav('Notifications', back_text='Settings', href='#S06-ios', action='back')}
  <div class="min-h-0 flex-1 space-y-6 overflow-hidden px-4 pb-6 pt-2">{ios_notif}</div>''', kind='ios'))

ios_sheet = f'''{scrim('z-30')}
  <div class="absolute inset-x-2 bottom-2 z-40 space-y-2" role="alertdialog" aria-modal="true" aria-labelledby="ios-so-t">
    <div class="overflow-hidden rounded-dialog bg-popover shadow-dialog">
      <p id="ios-so-t" class="px-6 pb-3 pt-4 text-center text-body-sm text-muted-foreground">Your lists are backed up to {ME['email']}. They'll be removed from this iPhone until you sign in again.</p>
      <a href="S08-home.html#S08-first-run" class="flex h-14 items-center justify-center border-t text-title-3 font-normal text-destructive" data-action="confirm-sign-out">Sign out</a>
    </div>
    <a href="#S06-ios" class="flex h-14 items-center justify-center rounded-dialog bg-popover text-title-3 text-primary shadow-dialog" data-action="cancel">Cancel</a>
  </div>'''
P.frame('S06-ios-sign-out', 'iOS sign out: action sheet', phone(ios_root(ios_sheet), kind='ios'))

# ---------------------------------------------------------------- web
P.section('Web', 'Same layout in the browser. Haptics stay visible but unavailable, with the reason and Get the app. Notifications are in-app only. Desktop shows the phone layout centered.')
P.frame('S06-web', 'Web, mobile browser: haptics unavailable, in-app notifications', phone(root(haptics_web=True, notif_value='In-app only'), kind='web'))
get_app = sheet('ga', f'''<p class="mt-2 text-body text-muted-foreground">Haptics, push notifications and importing phone contacts need the app. Your lists come with you when you sign in.</p>
    <div class="mt-5 space-y-2">{btn('Get it on Google Play', 'primary', href='#S06-web', icon_name='smartphone', action='google-play')}{btn('Download on the App Store', 'outline', href='#S06-web', icon_name='smartphone', action='app-store')}</div>''',
                title='Get SwipeSort for your phone', close_href='#S06-web')
P.frame('S06-web-get-app', 'Web: Get the app sheet', phone(root(haptics_web=True, notif_value='In-app only', overlay=get_app), kind='web'))
P.frame('S06-web-desktop', 'Web, desktop browser', desktop(root(haptics_web=True, notif_value='In-app only'), 'swipesort.app/settings'))

P.write('S06-settings.html')
