# Usage: python3 tools/generators/S01-splash.py  → design/03-screens/S01-splash.html
from groupa_common import *

P = Page('S01', 'Splash', 'Cold start only. Android uses the system splash screen (icon on the theme background, wordmark as the branding image); iOS uses a static launch screen; the web shows a brief loader only when loading takes longer than 300 ms.', 'S01-splash.md')


def splash(below='', link=None, link_label='', branding=True, mark_size='size-28'):
    brand = f'<div class="flex shrink-0 justify-center pb-12">{wordmark("text-title-2")}</div>' if branding else ''
    lk = ''
    if link:
        href, action = link
        lk = f'<a href="{href}" class="absolute inset-0 z-10" aria-label="{link_label}" data-action="{action}"></a>'
    return f'''<div class="relative flex flex-1 flex-col bg-background">
    {lk}
    <div class="flex flex-1 flex-col items-center justify-center px-8 text-center">
      {mark(mark_size)}
      {below}
    </div>
    {brand}
  </div>'''


P.section('Cold start', 'The splash stays only while the app opens its local database. Returning users go straight to Lists (S08); first launch goes to the introduction (S02); an invite link hands off to S32.')
P.frame('S01-default', 'Default (Android system splash)', phone(splash(
    link=('S02-onboarding.html#S02-welcome', 'next'),
    link_label='Open the introduction (the app moves on automatically)')))

slow = f'''<div class="mt-10 flex flex-col items-center gap-3" role="status">
        {icon("loader-circle", "size-6 animate-spin text-primary")}
        <p class="text-body text-muted-foreground">Opening your lists…</p>
      </div>'''
P.frame('S01-slow', 'Slow start (after 2 s): spinner and status', phone(splash(slow,
    link=('S08-home.html#S08-default', 'next'), link_label='Open Lists (the app moves on automatically)')))

updating = f'''<div class="mt-10 w-full max-w-xs" role="status">
        <p class="text-title-3">Updating your lists</p>
        <p class="mt-1 text-body text-muted-foreground">This takes a few seconds. Your lists and decisions are safe.</p>
        <div class="mt-5 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" aria-label="Updating your lists, 60%"><div class="h-full w-[60%] rounded-full bg-primary"></div></div>
      </div>'''
P.frame('S01-updating', 'First start after an app update (data upgrade)', phone(splash(updating)))

error = f'''<div class="relative flex flex-1 flex-col items-center justify-center bg-background px-8 text-center">
    {mark('size-16')}
    <h1 class="mt-8 text-title-2">SwipeSort couldn't open your lists</h1>
    <p class="mt-2 max-w-xs text-body text-muted-foreground">Nothing was deleted. Try again. If it keeps happening, restart your phone and send us a report.</p>
    <div class="mt-8 w-full max-w-xs space-y-2">
      {btn('Try again', 'primary', href='#S01-slow', action='retry')}
      {btn('Send a report', 'ghost', href='S06-settings.html#S06-feedback', action='report')}
    </div>
  </div>'''
P.frame('S01-error', 'Error: local data could not be opened', phone(error))

P.section('Opened from an invite link', 'App installed: the Android App Link or iOS Universal Link starts the app. The splash shows a status line while the invite is checked, then hands off to S32 (app) without showing onboarding first; onboarding is offered after joining.')
invite = f'''<div class="mt-10 flex flex-col items-center gap-3" role="status">
        {icon("loader-circle", "size-6 animate-spin text-primary")}
        <p class="text-body text-muted-foreground">Opening invite…</p>
      </div>'''
P.frame('S01-invite', 'Cold start from an invite link', phone(splash(invite,
    link=('S32-invite-link.html#S32-app', 'next'), link_label='Open the invite (the app moves on automatically)')))

P.section('iOS and web', 'iOS launch screens are static and carry no text (Apple HIG): the mark alone on the theme background. The in-app continuation (slow start, invite) is identical to Android. The web shows the mark with a thin loading bar only when the app takes more than 300 ms to load.')
P.frame('S01-ios', 'iOS launch screen (mark only, no text)', phone(splash(branding=False,
    link=('S02-onboarding.html#S02-welcome', 'next'), link_label='Open the introduction (the app moves on automatically)'), kind='ios'))
P.frame('S01-ios-slow', 'iOS slow start (in-app continuation)', phone(splash(slow, branding=False), kind='ios'))

web_bar = '<div class="absolute inset-x-0 top-0 h-1 overflow-hidden bg-muted" role="progressbar" aria-label="Loading SwipeSort"><div class="h-full w-1/3 rounded-full bg-primary"></div></div>'
web = f'''<div class="relative flex flex-1 flex-col items-center justify-center bg-background px-8 text-center">
    {web_bar}
    {mark('size-20')}
    <p class="mt-6 text-body text-muted-foreground" role="status">Loading SwipeSort…</p>
  </div>'''
P.frame('S01-web', 'Web, mobile browser: brief loader', phone(web, kind='web'))
P.frame('S01-web-desktop', 'Web, desktop browser: brief loader in the phone column', desktop(web, 'swipesort.app'))

P.write('S01-splash.html')
