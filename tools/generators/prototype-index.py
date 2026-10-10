# Usage: python3 tools/generators/prototype-index.py  → design/04-prototype/index.html
# Clickable prototype launcher: the four main flows as step lists. Every step opens the screen file in
# prototype mode (file.html#frame-id shows that frame only); inside a frame, tap the highlighted actions.
import os, glob

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
SCR = os.path.join(ROOT, 'design', '03-screens')
FILES = {os.path.basename(f)[:3]: os.path.basename(f) for f in glob.glob(os.path.join(SCR, 'S??-*.html'))}

def href(target):
    if target.startswith('demo:'):
        return 'swipe-demo.html?' + target[5:]
    return f'../03-screens/{FILES[target[:3]]}#{target}'

FLOWS = [
    ('flow-1', 'First launch to the first decision, without an account',
     'A new person installs the app, learns the gestures, imports phone contacts and sorts. No account is created. Covers SUC-04: the first decision is about 10 taps after the welcome screen.',
     [('S01-default', 'Splash'), ('S02-welcome', 'Welcome'), ('S02-demo', 'Try the gestures'), ('S02-demo-done', 'Gestures learned'),
      ('S08-first-run', 'Empty home'), ('S11-default', 'Choose a source'), ('S12-contacts', 'Why contacts access is needed'),
      ('S13-select-default', 'Select contacts'), ('S19-contacts', 'Map fields'), ('S20-default', 'Review duplicates'), ('S20-reviewed-all', '3 merged, 1 kept: 85 items'),
      ('S22-import-pick', 'Name the list and pick a card template'), ('S25-coach-1', 'Coach marks'),
      ('demo:deck=first&count=6&next=S27-first-round', 'Sort (live; the prototype stops after 6 cards)'), ('S27-first-round', 'Round summary')]),
    ('flow-2', 'Re-sort the Maybe pile, review results, export to Google Sheets',
     'A product shortlist, with no domain wording anywhere: the Maybe pile gets a second round, then results go to a new Google spreadsheet after an explicit confirmation.',
     [('S09-solo-round-done', 'Desk setup after Round 1'), ('S24-maybe', 'Start a round with the Maybe pile'),
      ('demo:deck=desk-maybe&next=S27-desk-round-2', 'Sort the Maybe pile (live)'), ('S27-desk-round-2', 'Round 2 summary'),
      ('S28-default', 'Results'), ('S39-default', 'Export: choose format'), ('S39-google-destination', 'Choose where to write'),
      ('S39-google-confirm', 'Confirm the write'), ('S39-success-google', 'Exported to Google Sheets')]),
    ('flow-3', 'Invite a partner who joins and sorts in a web browser',
     'Deniz shares a list made without an account: she signs in, her lists move to the account, and she invites Mert. Mert opens the link on a desktop browser, signs in, joins and sorts with the keyboard without installing anything (SUC-05). As the Decision Maker he resolves conflicts in bulk and exports.',
     [('S09-guest-wedding', 'Deniz: list on this phone only'), ('S05-share', 'Sign in to share'), ('S05-moving', 'Moving lists to the account'),
      ('S05-moved', 'Lists moved'), ('S31-default', 'Invite: copy the link'), ('S31-link-copied', 'Link copied'),
      ('S32-web-desktop', 'Mert opens the link in a browser'), ('S03-web-desktop', 'Mert signs in on the web'),
      ('S33-web-desktop', 'Join the list'), ('S34-dm-changed', 'Deniz makes Mert the Decision Maker'), ('S25-web-desktop', 'Mert sorts on the web'),
      ('demo:deck=mert&count=3&next=..%2F03-screens%2FS09-list-overview.html%23S09-shared-decision-maker', 'Mert sorts with the keyboard (live; stops after 3 cards)'),
      ('S25-shared', 'Meanwhile, Deniz sorts on her phone'), ('S09-shared-decision-maker', 'Mert sees 15 conflicts to resolve'), ('S36-default', 'Conflicts one by one'),
      ('S37-confirm', 'Resolve all with my decisions'), ('S37-summary', 'Resolved 12, 3 still open'),
      ('S39-shared', 'Export the shared list'), ('S39-shared-google-destination', 'New spreadsheet'),
      ('S39-shared-google-confirm', 'Confirm the write'), ('S39-success-shared', 'Exported to Google Sheets')]),
    ('flow-4', 'Create a list from a CSV file with a custom card template',
     'A hiring shortlist from candidates-q4.csv: map the columns, skip the empty duplicate step, customize the Candidate template and start sorting with it.',
     [('S08-default', 'Home'), ('S11-default', 'Choose a source'), ('S14-default', 'Choose a file'), ('S14-csv-preview', 'Preview the CSV'),
      ('S19-csv', 'Map fields'), ('S20-none', 'No duplicates found'), ('S22-import-pick-csv', 'Name the list and pick a template'),
      ('S23-default', 'Customize the card'), ('S23-save', 'Save the template'), ('S22-import-pick-custom', 'Custom template selected'),
      ('S25-candidate', 'Sorting with the custom template')]),
]

def flow_html(fid, title, desc, steps):
    lis = ''
    for i, (target, label) in enumerate(steps, 1):
        live = target.startswith('demo:')
        meta = 'Live swipe demo' if live else target
        lis += f'''
        <li><a href="{href(target)}" class="flex min-h-14 items-center gap-4 px-4 py-3" data-step="{target}">
          <span class="flex size-8 shrink-0 items-center justify-center rounded-full {'bg-primary text-primary-foreground' if live else 'bg-muted text-muted-foreground'} text-caption tabular-nums" aria-hidden="true">{i}</span>
          <span class="min-w-0 flex-1"><span class="block text-body">{label}</span><span class="block text-caption text-muted-foreground">{meta}</span></span>
          <i class="i-lucide-chevron-right size-5 text-muted-foreground" aria-hidden="true"></i></a></li>'''
    first = href(steps[0][0])
    return f'''
  <section id="{fid}" class="w-full max-w-2xl" aria-labelledby="{fid}-title">
    <div class="flex flex-wrap items-end justify-between gap-4">
      <div class="max-w-prose"><h2 id="{fid}-title" class="text-title-2">{title}</h2><p class="mt-1 text-body text-muted-foreground">{desc}</p></div>
      <a href="{first}" class="inline-flex h-12 items-center gap-2 rounded-control bg-primary px-5 text-label-lg text-primary-foreground" data-action="start-{fid}"><i class="i-lucide-play size-5" aria-hidden="true"></i>Start</a>
    </div>
    <ol class="mt-4 divide-y overflow-hidden rounded-group bg-card">{lis}
    </ol>
  </section>'''

html = f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SwipeSort prototype</title>
<link rel="icon" href="../01-foundations/brand/favicon.svg">
<link rel="stylesheet" href="../assets/css/app.css">
</head>
<body class="mock-page">
<header class="mock-doc">
  <div class="flex items-center gap-3"><img src="../01-foundations/brand/logo-mark.svg" alt="" class="size-10 dark:hidden"><img src="../01-foundations/brand/logo-mark-dark.svg" alt="" class="hidden size-10 dark:block"><h1>SwipeSort prototype</h1></div>
  <p>The four main flows, end to end. Each step opens one frame of the design. Inside a frame, use the buttons and links to move on, or come back here and pick the next step. Two steps are live: the swipe demo sorts real sample cards with touch, mouse or the keyboard (← Reject, ↑ Maybe, → Accept, Z Undo) and then continues to the round summary. To see a step in dark mode, set <code>data-theme="dark"</code> on the page, or add <code>&amp;theme=dark</code> to the swipe demo address. Everything else: <a href="../README.md">README</a>, <a href="../HANDOFF.md">handoff guide</a>, <a href="swipe-demo.html">swipe demo</a>.</p>
</header>
<main class="flex flex-col gap-section">
{''.join(flow_html(*f) for f in FLOWS)}
</main>
</body>
</html>
'''
out = os.path.join(ROOT, 'design', '04-prototype', 'index.html')
open(out, 'w').write(html)
print('prototype index:', sum(len(f[3]) for f in FLOWS), 'steps')
