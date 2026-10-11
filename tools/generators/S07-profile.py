# Usage: python3 tools/generators/S07-profile.py  → design/03-screens/S07-profile.html
from groupa_common import *

_phone = phone


def phone(content, kind='android', screen_cls='', overlay_full=None):
    """Frames with a dialog or sheet: scrim and sheet run under the system bars (QA-053)."""
    if overlay_full is None:
        overlay_full = 'role="alertdialog"' in content or ('role="dialog"' in content and 'bg-scrim' in content)
    if overlay_full and kind != 'web':
        content = content.replace('rounded-t-sheet bg-popover px-gutter pb-6 pt-2', 'rounded-t-sheet bg-popover px-gutter pb-12 pt-2')
    return _phone(content, kind, screen_cls, overlay_full)

P = Page('S07', 'Profile, connected accounts and account deletion',
         'Pushed from Settings (S06) in the Settings tab stack. Edit name and photo, manage sign-in methods (Google, Apple and email and password on every platform, D-13) and delete the account with a clear account of what is deleted and what stays (lists on this phone only stay, A-138).',
         'S07-profile.md')

BACK = 'S06-settings.html#S06-default'
APPLE_EMAIL = 'deniz.yilmaz@example.net'


# ---------------------------------------------------------------- local helpers
def action_row(lead, title, desc, action_label, href='#', aria=None, action=None, disabled=False, primary=True):
    """Row with a trailing text button (Disconnect, Connect, Change)."""
    act = f' data-action="{action}"' if action else ''
    ar = f' aria-label="{aria}"' if aria else ''
    col = 'text-primary' if primary else ''
    if disabled:
        btn_html = f'<button type="button" class="inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label-lg {col} opacity-50" disabled{ar}>{action_label}</button>'
    else:
        btn_html = f'<a href="{href}" class="inline-flex h-12 shrink-0 items-center rounded-control px-3 text-label-lg {col}"{ar}{act}>{action_label}</a>'
    d = f'<span class="block truncate text-body-sm text-muted-foreground">{desc}</span>' if desc else ''
    return f'<li class="flex min-h-16 items-center gap-4 py-2 pl-4 pr-1">{lead}<span class="min-w-0 flex-1"><span class="block text-body">{title}</span>{d}</span>{btn_html}</li>'


def static_row(icon_name, title, desc=None, trailing=''):
    d = f'<span class="block text-body-sm text-muted-foreground">{desc}</span>' if desc else ''
    return f'<li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon(icon_name, "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">{title}</span>{d}</span>{trailing}</li>'


G_LEAD = '<span class="flex size-5 shrink-0 items-center justify-center rounded-full border border-input bg-card text-caption font-bold leading-none text-foreground" aria-hidden="true">G</span>'
APPLE_LEAD = icon('apple', 'size-5 shrink-0')
MAIL_LEAD = icon('key-round', 'size-5 shrink-0 text-muted-foreground')


def photo_block(photo=True, uploading=False, offline=False, href='#S07-change-photo', label='Change photo', size='size-24'):
    if photo:
        av = f'<img src="{ME["avatar"]}" alt="Profile photo of Deniz Yılmaz" class="{size} rounded-full object-cover">'
    else:
        av = avatar(initials='DY', size='size-24', text='text-title-1', alt='Deniz Yılmaz, no profile photo')
    over = ''
    if uploading:
        over = f'<span class="absolute inset-0 flex items-center justify-center rounded-full bg-scrim/50 text-primary-foreground dark:text-foreground" aria-hidden="true">{icon("loader-circle", "size-7 animate-spin")}</span>'
    if uploading:
        b = f'<p class="mt-2 flex h-12 items-center text-body-sm text-muted-foreground" role="status">Uploading photo…</p>'
    elif offline:
        b = f'<button type="button" class="mt-2 inline-flex h-12 items-center rounded-control px-4 text-label-lg text-primary opacity-50" disabled>{label}</button>'
    else:
        b = f'<a href="{href}" class="mt-2 inline-flex h-12 items-center gap-2 rounded-control px-4 text-label-lg text-primary" data-action="change-photo">{icon("camera")}{label}</a>'
    return f'<div class="flex flex-col items-center pb-2 pt-2"><span class="relative">{av}{over}</span>{b}</div>'


def apple_row(apple, d=False):
    """apple: not | connected (Sign in with Apple on every platform, D-13)."""
    if apple == 'connected':
        return action_row(APPLE_LEAD, 'Apple', APPLE_EMAIL, 'Disconnect', href='#S07-disconnect-apple', aria='Disconnect Apple', action='disconnect-apple', disabled=d)
    return action_row(APPLE_LEAD, 'Apple', 'Not connected', 'Connect', href='#S07-apple-connected', aria='Connect Apple', action='connect-apple', disabled=d)


def profile_groups(google='connected', password='set', offline=False, apple='not', ios=False, name='Deniz Yılmaz'):
    d = offline
    name_row = (f'<li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon("user-round", "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body-sm text-muted-foreground">Name</span><span class="block text-body">{name}</span></span>'
                + (f'<button type="button" class="flex size-12 shrink-0 items-center justify-center rounded-full opacity-50" aria-label="Edit name" disabled>{icon("pencil")}</button></li>' if d else
                   f'<a href="#S07-edit-name" class="-mr-3 flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Edit name" data-action="edit-name">{icon("pencil")}</a></li>'))
    email_row = f'<li class="flex min-h-14 items-center gap-4 px-4 py-3">{icon("mail", "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body-sm text-muted-foreground">Email</span><span class="block truncate text-body">{ME["email"]}</span></span></li>'
    personal = group([name_row, email_row], header='Personal info', footer=None if ios else 'Members of shared lists see your name and photo.', ios=ios)

    rows = []
    if google == 'connected' or google == 'only':
        rows.append(action_row(G_LEAD, 'Google', ME['email'], 'Disconnect',
                               href='#S07-disconnect-blocked' if google == 'only' else '#S07-disconnect-confirm',
                               aria='Disconnect Google', action='disconnect-google', disabled=d))
    else:
        rows.append(action_row(G_LEAD, 'Google', 'Not connected', 'Connect', href='#S07-default', aria='Connect Google', action='connect-google', disabled=d))
    # platform order as in S03 (A-140): Apple first on iOS, after Google on Android and web
    if ios:
        rows.insert(0, apple_row(apple, d))
    else:
        rows.append(apple_row(apple, d))
    if password == 'set':
        rows.append(action_row(MAIL_LEAD, 'Email and password', 'Password set', 'Change', href='#S07-change-password', aria='Change password', action='change-password', disabled=d))
    else:
        rows.append(action_row(MAIL_LEAD, 'Email and password', 'No password yet', 'Add', href='#S07-add-password', aria='Add a password', action='add-password', disabled=d))
    signin = group(rows, header='Sign-in methods', footer=None if ios else 'Sign in with any of these. Keep at least one.', ios=ios)

    if d:
        del_row = f'<li><button type="button" class="flex min-h-14 w-full items-center gap-4 px-4 py-3 text-left" disabled>{icon("trash-2", "size-5 shrink-0 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body text-muted-foreground">Delete account</span><span class="block text-body-sm text-muted-foreground">Connect to the internet to delete your account.</span></span></button></li>'
    else:
        del_row = f'<li><a href="#S07-delete" class="flex min-h-14 items-center gap-4 px-4 py-3 text-destructive" data-action="delete-account">{icon("trash-2", "size-5 shrink-0")}<span class="min-w-0 flex-1"><span class="block text-body">Delete account</span><span class="block text-body-sm text-muted-foreground">Delete your account, your backed-up lists and your notes</span></span>{icon("chevron-right", "size-5 shrink-0 text-muted-foreground")}</a></li>'
    danger = group([del_row], ios=ios)
    return personal + signin + danger


def profile(google='connected', password='set', photo=True, uploading=False, offline=False, overlay='', banner='', apple='not'):
    return f'''{appbar('Profile', href=BACK, label='Back to Settings', action='back')}
  {banner}
  <div class="min-h-0 flex-1 space-y-6 overflow-hidden px-gutter pb-6">
    {photo_block(photo, uploading, offline, label='Change photo' if photo else 'Add photo')}
    {profile_groups(google, password, offline, apple=apple)}
  </div>
  {overlay}'''


def page_sub(title, body, footer, back='#S07-default', label='Back to Profile', overlay='', banner=''):
    foot = f'<div class="shrink-0 space-y-2 border-t bg-background px-gutter pb-4 pt-3">{footer}</div>' if footer else ''
    return f'''{appbar(title, href=back, label=label, action='back')}
  {banner}
  <div class="min-h-0 flex-1 overflow-hidden px-gutter pb-6 pt-2">
    {body}
  </div>
  {foot}
  {overlay}'''


RULES_OK = [('At least 8 characters', 'met'), ('A number or symbol', 'met')]
RULES_HALF = [('At least 8 characters', 'met'), ('A number or symbol', 'todo')]

# ================================================================ Profile
P.section('Profile', 'Name and photo are what other members see. Email is the sign-in address and is read-only. Sign-in methods list every way into the account.')
P.frame('S07-default', 'Default (Google and password connected)', phone(profile()))

name_field = field('s07-name', 'Name', value='Deniz Yılmaz', state='focused', autocomplete='name', helper='Members of shared lists see this name.')
P.frame('S07-edit-name', 'Edit name (dialog)', phone(profile(overlay=dialog('s07en', 'Edit name', 'Use the name your partner, family or team will recognize.',
    dlg_btn('Cancel', href='#S07-default') + dlg_btn('Save', 'primary', href='#S07-default', action='save-name'), role='dialog',
    extra_body=f'<div class="mt-4">{name_field}</div>'))))
name_err = field('s07-name-e', 'Name', value='', state='error', autocomplete='name', error='Enter a name. Members see it on shared lists.')
P.frame('S07-edit-name-error', 'Edit name: empty name', phone(profile(overlay=dialog('s07ee', 'Edit name', 'Use the name your partner, family or team will recognize.',
    dlg_btn('Cancel', href='#S07-default') + dlg_btn('Save', 'primary', disabled=True), role='dialog',
    extra_body=f'<div class="mt-4">{name_err}</div>'))))

photo_sheet = sheet('s07ph', f'''<ul class="mt-2 divide-y">
      <li><a href="#S07-photo-uploading" class="flex min-h-14 items-center gap-4 py-3">{icon("camera", "size-5 text-muted-foreground")}<span class="text-body">Take photo</span></a></li>
      <li><a href="#S07-photo-uploading" class="flex min-h-14 items-center gap-4 py-3">{icon("images", "size-5 text-muted-foreground")}<span class="text-body">Choose from gallery</span></a></li>
      <li><a href="#S07-no-photo" class="flex min-h-14 items-center gap-4 py-3 text-destructive">{icon("trash-2", "size-5")}<span class="text-body">Remove photo</span></a></li>
    </ul>''', title='Profile photo', close_href='#S07-default')
P.frame('S07-change-photo', 'Change photo (bottom sheet)', phone(profile(overlay=photo_sheet)))
P.frame('S07-photo-uploading', 'Photo uploading', phone(profile(uploading=True)))
P.frame('S07-no-photo', 'No photo: initials, Add photo', phone(profile(photo=False, overlay=snackbar('Photo removed', 'Undo', action_href='#S07-default'))))

# ================================================================ Sign-in methods
P.section('Sign-in methods', 'Connect or disconnect Google and Apple on every platform (D-13; on Android and web Apple opens its sign-in page in the browser); add or change the password. A method can be disconnected only while another one remains (A-53).')
P.frame('S07-google-not-connected', 'Google not connected (email account): Connect', phone(profile(google='not', photo=False)))
P.frame('S07-disconnect-confirm', 'Disconnect Google: confirmation', phone(profile(overlay=dialog('s07dc', 'Disconnect Google?',
    f'You\'ll sign in with {ME["email"]} and your password instead. Your lists aren\'t affected.',
    dlg_btn('Cancel', href='#S07-default') + dlg_btn('Disconnect', 'destructive', href='#S07-google-disconnected', action='confirm-disconnect')))))
P.frame('S07-google-disconnected', 'Google disconnected (snackbar)', phone(profile(google='not', overlay=snackbar('Google disconnected'))))
P.frame('S07-google-only', 'Google is the only method (no password yet)', phone(profile(google='only', password='none')))
P.frame('S07-disconnect-blocked', 'Disconnect blocked: add a password first', phone(profile(google='only', password='none', overlay=dialog('s07db', 'Add a password first',
    'Google is your only way to sign in. Add a password or connect Apple first, so you can still sign in after disconnecting Google.',
    dlg_btn('Cancel', href='#S07-google-only') + dlg_btn('Add a password', 'primary', href='#S07-add-password', action='add-password')))))

P.frame('S07-apple-connected', 'Apple connected (back from Apple\'s sign-in page)', phone(profile(apple='connected', overlay=snackbar('Apple connected'))))
P.frame('S07-disconnect-apple', 'Disconnect Apple: confirmation', phone(profile(apple='connected', overlay=dialog('s07da', 'Disconnect Apple?',
    f'You\'ll sign in with Google or with {ME["email"]} and your password instead. Your lists aren\'t affected.',
    dlg_btn('Cancel', href='#S07-apple-connected') + dlg_btn('Disconnect', 'destructive', href='#S07-default', action='confirm-disconnect')))))

add_pw = f'''<p class="text-body text-muted-foreground">Add a password to sign in with your email address as well as with Google.</p>
    <div class="mt-6 space-y-5">
      {field('s07ap-email', 'Email', value=ME['email'], state='disabled', autocomplete='username')}
      <div>{password_field('s07ap-new', 'New password', value='lavender-27', shown=True, state='focused', autocomplete='new-password')}{pw_rules('s07ap-rules', RULES_OK)}</div>
    </div>'''
P.frame('S07-add-password', 'Add a password', phone(page_sub('Add a password', add_pw, btn('Save password', href='#S07-default', action='save-password'))))

change_pw = f'''<div class="space-y-5">
      {password_field('s07cp-cur', 'Current password', value='••••••••••')}
      {link('Forgot your current password?', 'S04-forgot-password.html#S04-default', action='forgot-password', extra='-mt-3')}
      <div>{password_field('s07cp-new', 'New password', value='lavender', state='focused', autocomplete='new-password')}{pw_rules('s07cp-rules', RULES_HALF)}</div>
    </div>
    <p class="mt-6 text-body-sm text-muted-foreground">After you change it, other phones and browsers signed in to your account are signed out.</p>'''
P.frame('S07-change-password', 'Change password (new password half valid)', phone(page_sub('Change password', change_pw, btn('Save password', disabled=True))))
change_pw_err = f'''<div class="space-y-5">
      {password_field('s07ce-cur', 'Current password', value='••••••••', state='error', error="That password isn't right. Try again or reset it.")}
      {link('Forgot your current password?', 'S04-forgot-password.html#S04-default', action='forgot-password', extra='-mt-3')}
      <div>{password_field('s07ce-new', 'New password', value='••••••••••••', autocomplete='new-password')}{pw_rules('s07ce-rules', RULES_OK)}</div>
    </div>'''
P.frame('S07-change-password-error', 'Change password: wrong current password', phone(page_sub('Change password', change_pw_err, btn('Save password', href='#S07-password-changed', action='save-password'))))
change_pw_ok = f'''<div class="space-y-5">
      {password_field('s07cs-cur', 'Current password', value='••••••••••')}
      <div>{password_field('s07cs-new', 'New password', value='••••••••••••', autocomplete='new-password')}{pw_rules('s07cs-rules', RULES_OK)}</div>
    </div>'''
P.frame('S07-change-password-saving', 'Change password: saving', phone(page_sub('Change password', change_pw_ok, btn('Saving…', busy=True))))
P.frame('S07-password-changed', 'Password changed (snackbar)', phone(profile(overlay=snackbar('Password changed. Other devices were signed out.'))))

reauth = sheet('s07ra', f'''<p class="mt-1 text-body text-muted-foreground">For your security, sign in again before you delete your account.</p>
    <div class="mt-5 space-y-3">
      {google_btn(href='#S07-delete-confirm', action='reauth-google', label='Continue with Google')}
      <div class="flex items-center gap-3 py-1 text-body-sm text-muted-foreground" aria-hidden="true"><span class="h-px flex-1 bg-border"></span>or<span class="h-px flex-1 bg-border"></span></div>
      {password_field('s07ra-pw', 'Password', value='', placeholder='Your SwipeSort password')}
      {btn('Confirm', href='#S07-delete-confirm', action='reauth-confirm')}
    </div>''', title="Confirm it's you", close_href='#S07-delete')

# ================================================================ Delete account
P.section('Delete account', 'Required by both app stores. Step 1 explains what is deleted and what stays and asks what happens to shared lists the user owns; step 2 asks to type "delete"; a final dialog confirms. Sensitive steps may ask to sign in again first.')


def delete_body(choice='transfer', owner='Mert Aydın', offline=False, scrolled=False):
    t = choice == 'transfer'
    radio = lambda on: ('<span class="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary" aria-hidden="true"><span class="size-3 rounded-full bg-primary"></span></span>' if on
                        else '<span class="mt-0.5 size-6 shrink-0 rounded-full border-2 border-input" aria-hidden="true"></span>')
    new_owner = (f'<a href="#S07-delete-transfer" class="ml-10 mt-1 flex min-h-12 items-center gap-3 rounded-control border border-input bg-card px-3 text-body" data-action="choose-owner" aria-label="New Owner: {owner}. Change">'
                 f'<img src="{MERT["avatar"] if owner == "Mert Aydın" else ""}" alt="" class="size-8 rounded-full"><span class="min-w-0 flex-1 truncate">{owner}</span>{icon("chevron-down", "size-5 text-muted-foreground")}</a>') if t else ''
    shared = f'''<section>
      <h2 class="px-1 pb-2 text-label text-muted-foreground">Shared list you own</h2>
      <div class="rounded-group bg-card p-4 dark:border">
        <div class="flex items-center gap-3"><span class="flex size-10 shrink-0 items-center justify-center rounded-full bg-muted">{icon("users", "size-5 text-muted-foreground")}</span><div class="min-w-0 flex-1"><p class="truncate text-body">Wedding guests</p><p class="text-body-sm text-muted-foreground">100 items, 3 members</p></div></div>
        <div class="mt-3" role="radiogroup" aria-label="What happens to Wedding guests">
          <button type="button" role="radio" aria-checked="{"true" if t else "false"}" class="flex min-h-14 w-full items-start gap-4 py-2 text-left">{radio(t)}<span><span class="block text-body">Transfer ownership</span><span class="block text-body-sm text-muted-foreground">Mert and Selin keep the list. Your decisions and notes on it are removed.</span></span></button>
          {new_owner}
          <button type="button" role="radio" aria-checked="{"false" if t else "true"}" class="mt-1 flex min-h-14 w-full items-start gap-4 py-2 text-left">{radio(not t)}<span><span class="block text-body">Delete for everyone</span><span class="block text-body-sm text-muted-foreground">Mert and Selin lose access to the list.</span></span></button>
        </div>
      </div>
    </section>'''
    deleted = group([
        static_row('user-round', 'Your profile and sign-in methods'),
        static_row('list-checks', '4 lists only you use', 'Desk setup, Trip ideas, and 2 archived: Apartment viewings, Book club picks'),
        static_row('sticky-note', 'Your decisions and notes', 'Including those on lists other people share with you'),
    ], header='Deleted for good')
    kept = group([
        static_row('cloud-off', 'Frontend hiring, Q4', 'On this phone only. It stays on this phone, without an account.'),
        static_row('file-check', "Files and Google Sheets you imported from", "SwipeSort never changed them"),
        static_row('download', 'Files you exported'),
    ], header='Not changed')
    export = f'<div><p class="text-body-sm text-muted-foreground">Want a copy first? Export a list before you delete your account.</p>{link("Export a list", "S39-export.html#S39-default", action="export")}</div>'
    if scrolled:
        return f'<div class="space-y-6">{deleted}{kept}{export}</div>'
    return f'''<div class="space-y-6">
      <p class="text-body text-muted-foreground">Deleting your account can't be undone. Here's what happens.</p>
      {shared}
      {deleted}
      {kept}
      {export}
    </div>'''


del_footer = btn('Continue', href='#S07-reauth', action='continue') + btn('Keep my account', 'ghost', size='md', href='#S07-default', action='cancel')
P.frame('S07-delete', 'Delete account, step 1: what is deleted and what stays', phone(page_sub('Delete account', delete_body(), del_footer)))
P.frame('S07-delete-scrolled', 'Step 1 scrolled: what is not changed, export first', phone(page_sub('Delete account', delete_body(scrolled=True), del_footer)))
P.frame('S07-delete-everyone', 'Step 1 with "Delete for everyone" chosen', phone(page_sub('Delete account', delete_body('delete'), del_footer)))

transfer_sheet = sheet('s07tr', f'''<p class="mt-1 text-body-sm text-muted-foreground">The new Owner can start rounds, manage members and change the conflict rule.</p>
    <div class="mt-3 divide-y" role="radiogroup" aria-label="New Owner">
      <button type="button" role="radio" aria-checked="true" class="flex min-h-16 w-full items-center gap-3 py-2 text-left"><img src="{MERT["avatar"]}" alt="" class="size-10 rounded-full"><span class="min-w-0 flex-1"><span class="block text-body">Mert Aydın</span><span class="block text-body-sm text-muted-foreground">Decision Maker, 85 / 100 decided</span></span><span class="flex size-6 shrink-0 items-center justify-center rounded-full border-2 border-primary" aria-hidden="true"><span class="size-3 rounded-full bg-primary"></span></span></button>
      <button type="button" role="radio" aria-checked="false" class="flex min-h-16 w-full items-center gap-3 py-2 text-left">{avatar(initials="SY")}<span class="min-w-0 flex-1"><span class="block text-body">Selin Yılmaz</span><span class="block text-body-sm text-muted-foreground">Collaborator, 43 / 100 decided</span></span><span class="size-6 shrink-0 rounded-full border-2 border-input" aria-hidden="true"></span></button>
    </div>
    <div class="mt-4">{btn('Choose Mert Aydın', href='#S07-delete', action='choose')}</div>''', title='New Owner of Wedding guests', close_href='#S07-delete')
P.frame('S07-delete-transfer', 'Choose the new Owner (bottom sheet)', phone(page_sub('Delete account', delete_body(), del_footer, overlay=transfer_sheet)))
P.frame('S07-reauth', "Re-authentication required (sheet)", phone(page_sub('Delete account', delete_body(), del_footer, overlay=reauth)))


def confirm_body(value='delete', state='default', error=None):
    summary = f'''<ul class="space-y-3 rounded-group bg-card p-4 text-body dark:border">
        <li class="flex gap-3">{icon("arrow-right-left", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<span>“Wedding guests” moves to Mert Aydın</span></li>
        <li class="flex gap-3">{icon("trash-2", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<span>Desk setup, Trip ideas and 2 archived lists (Apartment viewings, Book club picks) are deleted</span></li>
        <li class="flex gap-3">{icon("trash-2", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<span>Your profile, decisions and notes are deleted</span></li>
        <li class="flex gap-3">{icon("cloud-off", "size-5 mt-0.5 shrink-0 text-muted-foreground")}<span>“Frontend hiring, Q4” stays on this phone, without an account</span></li>
      </ul>'''
    f = field('s07dc-type', 'To confirm, type delete', value=value, state=state, error=error, autocomplete='off', helper=None if error else 'Lowercase is fine.')
    return f'''<div class="space-y-6">
      <p class="text-body text-muted-foreground">This is the last step. After this, your account can't be restored.</p>
      {summary}
      {f}
    </div>'''


confirm_footer = btn('Delete account', 'destructive', href='#S07-delete-dialog', action='delete-account') + btn('Keep my account', 'ghost', size='md', href='#S07-default', action='cancel')
P.frame('S07-delete-confirm', 'Step 2: type delete to confirm', phone(page_sub('Confirm deletion', confirm_body(state='focused'), confirm_footer, back='#S07-delete', label='Back')))
P.frame('S07-delete-confirm-empty', 'Step 2: nothing typed yet (button disabled)', phone(page_sub('Confirm deletion', confirm_body(value=''),
    btn('Delete account', 'destructive', disabled=True) + btn('Keep my account', 'ghost', size='md', href='#S07-default'), back='#S07-delete', label='Back')))
P.frame('S07-delete-dialog', 'Final confirmation dialog', phone(page_sub('Confirm deletion', confirm_body(), confirm_footer, back='#S07-delete', label='Back',
    overlay=dialog('s07fd', 'Delete your account?', "This can't be undone. “Wedding guests” moves to Mert Aydın. 4 lists (2 of them archived), your decisions and your notes are deleted. “Frontend hiring, Q4” stays on this phone.",
                   dlg_btn('Cancel', href='#S07-delete-confirm') + dlg_btn('Delete account', 'destructive', href='#S07-deleting', action='confirm-delete')))))

deleting = f'''<div class="relative flex flex-1 flex-col items-center justify-center px-8 text-center" role="status" aria-live="polite">
    {icon("loader-circle", "size-8 animate-spin text-primary")}
    <h1 class="mt-6 text-title-2">Deleting your account…</h1>
    <p class="mt-2 max-w-xs text-body text-muted-foreground">Keep SwipeSort open. This takes a few seconds.</p>
    <a href="#S07-deleted" class="absolute inset-0" data-action="next" aria-label="Show the result (prototype: click anywhere; the app moves on by itself)"></a>
  </div>'''
P.frame('S07-deleting', 'Deleting (no way back, no close button)', phone(deleting))

deleted = f'''<div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
    <span class="flex size-14 items-center justify-center rounded-full bg-muted text-foreground">{icon("check", "size-7")}</span>
    <h1 class="mt-6 text-title-2">Your account is deleted</h1>
    <p class="mt-2 max-w-xs text-body text-muted-foreground">Mert Aydın now owns Wedding guests. “Frontend hiring, Q4” is still on this phone. You can keep using SwipeSort without an account.</p>
  </div>
  <div class="shrink-0 px-gutter pb-4">{btn('Done', href='S08-home.html#S08-guest', action='done')}</div>'''
P.frame('S07-deleted', 'Deleted: signed out; the list on this phone only stays', phone(deleted))

failed_body = alert_error("Couldn't delete your account", 'Nothing was deleted. Check your connection and try again.') + '<div class="mt-6">' + confirm_body() + '</div>'
P.frame('S07-delete-failed', 'Deletion failed: nothing deleted, try again', phone(page_sub('Confirm deletion', failed_body,
    btn('Try again', 'destructive', href='#S07-deleting', action='retry') + btn('Keep my account', 'ghost', size='md', href='#S07-default'), back='#S07-delete', label='Back')))

# ================================================================ Offline, iOS, web, large text
P.section('Offline, iOS, web and large text', 'Offline: everything is readable, changes are disabled with the reason. iOS lists Apple first among sign-in methods (native Sign in with Apple) and uses grouped inset lists with a back chevron. Web uploads a photo file instead of camera or gallery; Apple connects through Apple\'s sign-in page.')
P.frame('S07-offline', 'Offline: changes disabled with the reason', phone(profile(offline=True, banner=offline_banner("You're offline. Profile changes need a connection."))))

ios_body = f'''{ios_nav('Profile', back_text='Settings', href=BACK, action='back')}
  <div class="min-h-0 flex-1 space-y-6 overflow-hidden px-4 pb-6">
    {photo_block(True, size='size-20')}
    {profile_groups(apple='connected', ios=True)}
  </div>'''
P.frame('S07-ios', 'iOS: Apple, Google and password; grouped inset lists', phone(ios_body, kind='ios'))
ios_alert = f'''{scrim('z-30', 'bg-scrim/40')}
  <div class="absolute inset-x-12 top-1/2 z-40 -translate-y-1/2 overflow-hidden rounded-dialog bg-popover text-center shadow-dialog" role="alertdialog" aria-modal="true" aria-labelledby="s07ia-t" aria-describedby="s07ia-d">
    <div class="px-4 pb-4 pt-5"><h2 id="s07ia-t" class="text-body font-semibold">Delete your account?</h2><p id="s07ia-d" class="mt-1 text-body-sm text-muted-foreground">This can't be undone. “Wedding guests” moves to Mert Aydın. 4 lists (2 of them archived), your decisions and your notes are deleted. “Frontend hiring, Q4” stays on this phone.</p></div>
    <a href="#S07-deleting" class="flex h-12 items-center justify-center border-t text-body text-destructive">Delete account</a>
    <a href="#S07-delete-confirm" class="flex h-12 items-center justify-center border-t text-body font-semibold text-primary">Cancel</a>
  </div>'''
ios_confirm = f'''{ios_nav('Confirm deletion', back_text='Back', href='#S07-delete')}
  <div class="min-h-0 flex-1 overflow-hidden px-4 pb-6 pt-2">{confirm_body()}</div>
  <div class="shrink-0 space-y-2 px-4 pb-2 pt-3">{btn('Delete account', 'destructive')}</div>
  {ios_alert}'''
P.frame('S07-ios-delete-alert', 'iOS: final confirmation as a system alert', phone(ios_confirm.replace('stays on this phone', 'stays on this iPhone'), kind='ios'))

web_sheet = sheet('s07wp', f'''<ul class="mt-2 divide-y">
      <li><a href="#S07-photo-uploading" class="flex min-h-14 items-center gap-4 py-3">{icon("upload", "size-5 text-muted-foreground")}<span class="min-w-0 flex-1"><span class="block text-body">Upload photo</span><span class="block text-body-sm text-muted-foreground">JPG or PNG, up to 10 MB</span></span></a></li>
      <li><a href="#S07-no-photo" class="flex min-h-14 items-center gap-4 py-3 text-destructive">{icon("trash-2", "size-5")}<span class="text-body">Remove photo</span></a></li>
    </ul>''', title='Profile photo', close_href='#S07-default')
P.frame('S07-web-change-photo', 'Web: upload a photo file', phone(profile(overlay=web_sheet), kind='web'))

big = f'''<header class="flex min-h-16 shrink-0 items-center gap-1 px-1">
    <a href="{BACK}" class="flex size-12 items-center justify-center rounded-full" aria-label="Back to Settings">{icon("arrow-left", "size-7")}</a>
    <h1 class="min-w-0 flex-1 truncate px-1 text-title-2">Profile</h1>
  </header>
  <div class="min-h-0 flex-1 space-y-6 overflow-hidden px-gutter pb-6">
    <div class="flex items-center gap-4"><img src="{ME["avatar"]}" alt="Profile photo of Deniz Yılmaz" class="size-20 rounded-full"><a href="#S07-change-photo" class="inline-flex min-h-touch items-center text-title-3 text-primary">Change photo</a></div>
    <section><h2 class="px-1 pb-2 text-body-lg text-muted-foreground">Personal info</h2>
      <ul class="divide-y overflow-hidden rounded-group bg-card dark:border">
        <li class="flex items-center gap-3 px-4 py-4"><span class="min-w-0 flex-1"><span class="block text-body-lg text-muted-foreground">Name</span><span class="block text-title-2 font-normal">Deniz Yılmaz</span></span><a href="#S07-edit-name" class="flex size-12 shrink-0 items-center justify-center rounded-full" aria-label="Edit name">{icon("pencil", "size-7")}</a></li>
        <li class="px-4 py-4"><span class="block text-body-lg text-muted-foreground">Email</span><span class="block break-all text-title-2 font-normal">{ME["email"]}</span></li>
      </ul></section>
    <section><h2 class="px-1 pb-2 text-body-lg text-muted-foreground">Sign-in methods</h2>
      <ul class="divide-y overflow-hidden rounded-group bg-card dark:border">
        <li class="px-4 py-4"><span class="block text-title-2 font-normal">Google</span><span class="block break-all text-body-lg text-muted-foreground">{ME["email"]}</span><a href="#S07-disconnect-confirm" class="mt-1 inline-flex min-h-touch items-center text-title-3 text-primary" aria-label="Disconnect Google">Disconnect</a></li>
        <li class="px-4 py-4"><span class="block text-title-2 font-normal">Apple</span><span class="block text-body-lg text-muted-foreground">Not connected</span><a href="#S07-apple-connected" class="mt-1 inline-flex min-h-touch items-center text-title-3 text-primary" aria-label="Connect Apple">Connect</a></li>
        <li class="px-4 py-4"><span class="block text-title-2 font-normal">Email and password</span><span class="block text-body-lg text-muted-foreground">Password set</span><a href="#S07-change-password" class="mt-1 inline-flex min-h-touch items-center text-title-3 text-primary" aria-label="Change password">Change</a></li>
      </ul></section>
    <section><ul class="overflow-hidden rounded-group bg-card dark:border"><li><a href="#S07-delete" class="flex min-h-16 items-center gap-4 px-4 py-4 text-destructive" data-action="delete-account">{icon("trash-2", "size-7 shrink-0")}<span class="text-title-2 font-normal">Delete account</span></a></li></ul></section>
  </div>'''
P.frame('S07-large-text', 'Large text (200%): rows stack, actions move below', phone(big))

P.write('S07-profile.html')
