# Usage: python3 tools/generators/S18-photos-import.py
# Generates design/03-screens/S18-photos-import.html
import datetime
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from groupc2_common import *  # noqa

P = Page('S18', 'Photos import', 'Step 2 of the photos import: select photos from the gallery (Android, iOS) or upload photo files (web). Each photo becomes one item with fixed fields (Photo, Taken, Location, File name), so field mapping is skipped. Spec: <a href="S18-photos-import.md">S18-photos-import.md</a>.')

PHOTOS = DATA['photos']
CLOSE = 'S08-home.html#S08-default'
NEXT = 'S22-template-library.html#S22-import-pick'
GET_APP = 'https://swipesort.app/get'


def dt(p):
    return datetime.datetime.fromisoformat(p['takenAt'])


def day_label(d):
    return d.strftime('%A, %b ') + str(d.day)


def tile_label(p):
    d = dt(p)
    loc = f', {p["location"]}' if p['location'] else ''
    return f'Photo taken {d.strftime("%b")} {d.day}, {d.strftime("%H:%M")}{loc}'


def tile(p, selected):
    img = f'<img src="{IMG}photos/{p["id"]}.svg" alt="" class="size-full object-cover">'
    if selected:
        mark = f'<span class="pointer-events-none absolute inset-0 ring-2 ring-inset ring-primary"></span><span class="absolute right-1.5 top-1.5 flex size-6 items-center justify-center rounded-full bg-primary text-primary-foreground ring-2 ring-card">{icon("check", "size-4")}</span>'
    else:
        mark = '<span class="absolute right-1.5 top-1.5 size-6 rounded-full border-2 border-card bg-scrim/30"></span>'
    return f'<button role="checkbox" aria-checked="{"true" if selected else "false"}" aria-label="{tile_label(p)}" class="relative aspect-square overflow-hidden bg-muted">{img}{mark}</button>'


def skeleton_tile():
    return '<span class="aspect-square animate-pulse bg-muted" aria-hidden="true"></span>'


def days(photos):
    """Group photos by day, newest first. Days with fewer than 4 photos merge into their week (Monday to Sunday)."""
    by_day = {}
    for p in photos:
        by_day.setdefault(dt(p).date(), []).append(p)
    groups = {}
    for d, ps in by_day.items():
        key = ('day', d) if len(ps) >= 4 else ('week', d - datetime.timedelta(days=d.weekday()))
        groups.setdefault(key, []).extend(ps)
    out = []
    for key in sorted(groups, key=lambda k: max(dt(p) for p in groups[k]), reverse=True):
        ps = sorted(groups[key], key=dt, reverse=True)
        first, last = dt(ps[-1]).date(), dt(ps[0]).date()
        if first == last:
            label, short = day_label(datetime.datetime.combine(first, datetime.time())), f'{first.strftime("%b")} {first.day}'
        elif first.month == last.month:
            label = short = f'{first.strftime("%b")} {first.day} to {last.day}'
        else:
            label = short = f'{first.strftime("%b")} {first.day} to {last.strftime("%b")} {last.day}'
        out.append(((label, short), ps))
    return out


def day_section(d, ps, state='all', skeleton=False):
    """state: 'all' | 'none' | 'some'"""
    locs = []
    for p in ps:
        if p['location'] and p['location'] not in locs:
            locs.append(p['location'])
    loc = f'<p class="truncate text-caption text-muted-foreground">{", ".join(locs)}</p>' if locs else '<p class="text-caption text-muted-foreground">No location</p>'
    label, short = d
    box = checkbox_box(True if state == 'all' else ('mixed' if state == 'some' else False))
    checked = {'all': 'true', 'none': 'false', 'some': 'mixed'}[state]
    if skeleton:
        sel = '<span class="size-12"></span>'
        tiles = ''.join(skeleton_tile() for _ in ps)
    else:
        sel = f'<button role="checkbox" aria-checked="{checked}" aria-label="Select all photos from {short}" class="flex size-12 shrink-0 items-center justify-center rounded-full">{box}</button>'
        tiles = ''.join(tile(p, state == 'all' or (state == 'some' and j == 0)) for j, p in enumerate(ps))
    return f'''<section aria-label="{label}">
      <div class="flex h-14 items-center gap-3 pl-gutter pr-2"><div class="min-w-0 flex-1"><h2 class="text-label">{label}</h2>{loc}</div>{sel}</div>
      <div class="grid grid-cols-4 gap-0.5">{tiles}</div>
    </section>'''


def album_chip(name='All photos'):
    return f'<button class="inline-flex min-h-touch items-center" aria-haspopup="dialog" aria-label="Album: {name}. Change album"><span class="inline-flex h-9 items-center gap-1.5 rounded-full border border-input bg-card px-3 text-label">{icon("images", "size-4 text-muted-foreground")}{name}{icon("chevron-down", "size-4 text-muted-foreground")}</span></button>'


def toolbar(count_text, action='Clear', busy=False, album='All photos', status=True):
    role = ' role="status"' if status else ''
    spin = icon('loader-circle', 'size-4 animate-spin text-primary') if busy else ''
    act = f'<button class="inline-flex h-12 items-center rounded-control px-3 text-label-lg text-primary"{" disabled" if busy else ""}>{action}</button>' if action else ''
    return f'''<div class="flex shrink-0 flex-wrap items-center gap-x-2 border-b pb-1 pl-gutter {"pr-2" if action else "pr-gutter"}">
    <p class="inline-flex min-w-0 flex-1 items-center gap-2 text-label tabular-nums"{role}>{spin}{count_text}</p>
    {album_chip(album)}{act}
  </div>'''


def grid_screen(photos, states=None, count_text='30 selected', action='Clear', bar=None, top='', bottom_html=None, overlay='', skeleton_from=None, step=(2, 3), busy=False, album='All photos'):
    secs = ''
    for i, (d, ps) in enumerate(days(photos)):
        st = states[i] if states else 'all'
        sk = skeleton_from is not None and i >= skeleton_from
        secs += day_section(d, ps, st, sk)
    n, total = step
    return f'''{bar or modal_bar(close_href=CLOSE)}
  {stepper("Select items", n, total)}
  {toolbar(count_text, action, busy, album)}
  <div class="min-h-0 flex-1 overflow-hidden">
    {top}
    <div class="pb-6">{secs}</div>
  </div>
  {bottom_html or bottom("Continue", NEXT, "continue", note="Each photo becomes one item.")}
  {overlay}'''


# ------------------------------------------------------------------ gallery
P.section('Gallery selection (Android, iOS)', 'After photo access is granted (S12-photos), SwipeSort shows its own selection grid: grouped by day, newest first, 4 columns; days with fewer than 4 photos merge into their week so rows stay full. Tap a photo to select it; the day checkbox selects the whole day. Each photo becomes one item.')

P.frame('S18-default', 'Default: 30 photos selected', phone(grid_screen(PHOTOS)))

P.frame('S18-none-selected', 'First open: nothing selected yet', phone(grid_screen(
    PHOTOS, states=['none'] * 15, count_text='Select photos', action='Select all',
    bottom_html=bottom('Continue', disabled=True, note='Each photo becomes one item.'))))

P.frame('S18-loading', 'Loading thumbnails', phone(grid_screen(
    PHOTOS, states=['none'] * 15, count_text='Loading photos…', action=None, busy=True, skeleton_from=1,
    bottom_html=bottom('Continue', disabled=True, note='Each photo becomes one item.'))))

empty = f'''{modal_bar(close_href=CLOSE)}
  {stepper("Select items", 2, 3)}
  <div class="flex flex-1 flex-col items-center justify-center px-8 pb-16 text-center">
    {icon("images", "size-8 text-muted-foreground")}
    <h2 class="mt-4 text-title-3">No photos on this phone</h2>
    <p class="mt-1 max-w-xs text-body text-muted-foreground">Photos you take or save show up here. You can import from another source instead.</p>
    <a href="S11-source-picker.html#S11-default" class="mt-6 flex h-12 w-full max-w-xs items-center justify-center rounded-control bg-primary text-label-lg text-primary-foreground" data-action="choose-source">Choose another source</a>
  </div>'''
P.frame('S18-empty', 'Empty gallery', phone(empty))

albums = [('All photos', '30 photos', 'ph30', True), ('Camera', '26 photos', 'ph27', False), ('Lisbon', '8 photos', 'ph15', False), ('Downloads', '4 photos', 'ph05', False)]
ar = ''
for name, cnt, ph, sel in albums:
    ar += f'''<div><button role="radio" aria-checked="{"true" if sel else "false"}" class="flex min-h-16 w-full items-center gap-4 px-1 py-2 text-left">
        <img src="{IMG}photos/{ph}.svg" alt="" class="size-12 shrink-0 rounded-sm object-cover">
        <span class="min-w-0 flex-1"><span class="block text-body">{name}</span><span class="block text-body-sm tabular-nums text-muted-foreground">{cnt}</span></span>
        {radio_dot(sel)}</button></div>'''
P.frame('S18-albums', 'Album picker sheet', phone(grid_screen(
    PHOTOS, overlay=sheet('al1', 'Album', f'<div class="mt-2 divide-y" role="radiogroup" aria-label="Album">{ar}</div>', subtitle='Selected photos stay selected when you switch albums.').replace('class="-mr-3 flex size-12', 'class="-mr-3 flex size-12 shrink-0'))))

large_alert = f'<div class="px-gutter pb-1 pt-3">{alert("info", "1,248 photos make a long round", "You can import them all and sort in several sittings. Progress saves as you go.")}</div>'
P.frame('S18-large', 'Large selection: 1,248 photos (warning)', phone(grid_screen(
    PHOTOS[18:], count_text='1,248 selected', top=large_alert,
    bottom_html=bottom('Continue', NEXT, 'continue', note='Each photo becomes one item.'))))

P.frame('S18-limit', 'Limit reached: 5,000 photos', phone(grid_screen(
    PHOTOS[18:], states=['all', 'all', 'all', 'some', 'none', 'none'], count_text='5,000 selected',
    overlay=snackbar('Up to 5,000 photos can be imported at once. Unselect some to add others.', bottom='bottom-32', icon_name='info'),
    bottom_html=bottom('Continue', NEXT, 'continue', note='Each photo becomes one item.'))))

# ------------------------------------------------------------------ iOS
P.section('iOS', 'Same grid on iOS with full access (iOS bar: back chevron, centered title, close at the right). With limited access, the grid shows only the photos the person shared, with a way to share more.')
ios_bar = modal_bar(ios=True, back=('Choose source', 'S11-source-picker.html#S11-default'), close_href=CLOSE)
limited = PHOTOS[18:]
ios_banner = f'''<div class="px-gutter pb-1 pt-3">{alert("neutral", "SwipeSort can see 12 photos you chose", "", alert_button("Select more photos", "select-more") + alert_link("Allow access to all photos in Settings", "#S18-ios-limited"), ic="lock")}</div>'''
P.frame('S18-ios-limited', 'iOS: limited photo access', phone(grid_screen(
    limited, bar=ios_bar, count_text='12 selected', top=ios_banner), ios=True))

# ------------------------------------------------------------------ web
P.section('Web: upload photo files', "The gallery picker needs the Android or iOS app (PLT-08). On the web the same step uploads photo files instead: JPG, PNG, HEIC or WebP, up to 25 MB each, up to 5,000 per import. Format and size are checked before upload; files that can't be added are listed with the reason.")

web_note = alert('neutral', "Picking from your phone's gallery needs the Android or iOS app", 'You can upload photo files here instead.', alert_link('Get the app', GET_APP), ic='monitor-smartphone')
drop_mobile = f'''<div class="flex flex-col items-center rounded-tile border-2 border-dashed border-input bg-card px-6 py-10 text-center">
      {icon("upload", "size-8 text-muted-foreground")}
      <p class="mt-3 text-title-3">Upload photos from this device</p>
      <p class="mt-1 max-w-xs text-body-sm text-muted-foreground">JPG, PNG, HEIC or WebP, up to 25 MB each.</p>
      {btn("Choose photos", "outline", "image-plus", extra="mt-5", action="choose-photos")}
    </div>'''
P.frame('S18-web', 'Web, mobile browser: upload instead of the gallery', web_phone(f'''{modal_bar(close_href=CLOSE)}
  {stepper("Select items", 2, 3)}
  <div class="min-h-0 flex-1 space-y-4 overflow-hidden px-gutter pt-1">
    {web_note}
    {drop_mobile}
  </div>
  {bottom("Continue", disabled=True, note="Each photo becomes one item.")}'''))


def file_row(ph, name, size, state, pct=None):
    if ph:
        thumb = f'<img src="{IMG}photos/{ph}.svg" alt="" class="size-12 shrink-0 rounded-sm object-cover">'
    else:
        thumb = f'<span class="flex size-12 shrink-0 items-center justify-center rounded-sm bg-muted text-muted-foreground" aria-hidden="true">{icon("image-off")}</span>'
    trail = ''
    if state == 'uploaded':
        meta = f'<span class="inline-flex items-center gap-1">{icon("check", "size-4")}Uploaded</span>'
    elif state == 'uploading':
        meta = f'''<span class="flex items-center gap-2"><span class="tabular-nums">Uploading… {pct}%</span><span class="h-1.5 w-20 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="{pct}" aria-valuemin="0" aria-valuemax="100" aria-label="Uploading {name}, {pct}%"><span class="block h-full w-[{pct}%] rounded-full bg-primary"></span></span></span>'''
    elif state == 'waiting':
        meta = f'<span class="inline-flex items-center gap-1">{icon("clock", "size-4")}Waiting</span>'
    elif state == 'paused':
        meta = f'<span class="inline-flex items-center gap-1">{icon("pause", "size-4")}Paused</span>'
    else:  # error text
        meta = f'<span class="inline-flex items-start gap-1 text-destructive">{icon("circle-alert", "size-4 mt-0.5 shrink-0")}<span>{state}</span></span>'
        trail = icon_btn('x', f'Remove {name}')
    return f'''<li class="flex items-center gap-3 px-4 py-2.5">
        {thumb}
        <div class="min-w-0 flex-1"><p class="flex items-baseline gap-2"><span class="min-w-0 truncate text-body">{name}</span><span class="shrink-0 text-caption tabular-nums text-muted-foreground">{size}</span></p><div class="text-body-sm text-muted-foreground">{meta}</div></div>
        {trail}
      </li>'''


drop_compact = f'''<div class="flex items-center gap-3 rounded-tile border-2 border-dashed border-input bg-card py-2 pl-4 pr-2">
      {icon("upload", "size-5 shrink-0 text-muted-foreground")}
      <p class="min-w-0 flex-1 text-body text-muted-foreground">Drop to add more</p>
      {btn("Add photos", "ghost", size="h-12", extra="text-primary", action="choose-photos")}
    </div>'''
up_rows = (file_row('ph30', 'IMG_2070.JPG', '4.7 MB', 'uploaded')
           + file_row('ph29', 'IMG_2069.JPG', '4.0 MB', 'uploaded')
           + file_row('ph28', 'IMG_2068.JPG', '2.8 MB', 'uploading', 64)
           + file_row('ph27', 'IMG_2067.JPG', '4.6 MB', 'waiting')
           + file_row(None, 'IMG_2071.MOV', '48.2 MB', "Videos can't be imported.")
           + file_row('ph15', 'lisbon-panorama.jpg', '38.2 MB', 'Too large. The limit is 25 MB.'))
uploading = f'''{modal_bar(close_href=CLOSE)}
  {stepper("Select items", 2, 3)}
  <div class="min-h-0 flex-1 space-y-4 overflow-hidden px-gutter pt-1">
    {drop_compact}
    <div>
      <div class="flex items-baseline justify-between gap-3"><p class="text-label tabular-nums" role="status">Uploading 18 of 30 photos…</p><p class="text-caption text-destructive">2 can't be added</p></div>
      <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="18" aria-valuemin="0" aria-valuemax="30" aria-label="18 of 30 photos uploaded"><div class="h-full w-[60%] rounded-full bg-primary"></div></div>
    </div>
    <ul class="divide-y overflow-hidden rounded-group bg-card">{up_rows}</ul>
  </div>
  {bottom("Continue", disabled=True, note="You can continue when the upload finishes.")}'''
P.frame('S18-web-uploading', 'Web, desktop: uploading with format and size errors', desktop(uploading, 'swipesort.app/import/photos'))

fail_rows = (file_row(None, 'IMG_2071.MOV', '48.2 MB', "Videos can't be imported.")
             + file_row('ph15', 'lisbon-panorama.jpg', '38.2 MB', 'Too large. The limit is 25 MB.'))
strip = ''.join(f'<img src="{IMG}photos/{p}.svg" alt="" class="aspect-square w-full rounded-xs object-cover">' for p in ['ph30', 'ph29', 'ph28', 'ph27', 'ph26', 'ph25', 'ph24', 'ph23'])
partial_alert = alert('error', 'Uploaded 30 of 32 photos', "2 files couldn't be added. Save them as JPG, PNG, HEIC or WebP under 25 MB and choose them again, or continue without them.")
partial = f'''{modal_bar(close_href=CLOSE)}
  {stepper("Select items", 2, 3)}
  <div class="min-h-0 flex-1 space-y-5 overflow-hidden px-gutter pt-1">
    {partial_alert}
    <div><p class="px-1 pb-2 text-label text-muted-foreground">Couldn't be added (2)</p><ul class="divide-y overflow-hidden rounded-group bg-card">{fail_rows}</ul></div>
    <div><p class="px-1 pb-2 text-label text-muted-foreground">Ready to import (30)</p>
      <div class="rounded-group bg-card p-3"><div class="grid grid-cols-4 gap-1.5" role="img" aria-label="30 uploaded photos">{strip}</div><p class="mt-3 text-body-sm text-muted-foreground">And 22 more</p></div></div>
  </div>
  {bottom("Continue with 30 photos", NEXT, "continue", secondary=ghost_full("Choose more photos", "#S18-web", "choose-photos"))}'''
P.frame('S18-web-partial', 'Web: upload finished, 2 files not added', web_phone(partial))

off_rows = (file_row('ph30', 'IMG_2070.JPG', '4.7 MB', 'uploaded')
            + file_row('ph29', 'IMG_2069.JPG', '4.0 MB', 'uploaded')
            + file_row('ph28', 'IMG_2068.JPG', '2.8 MB', 'paused')
            + file_row('ph27', 'IMG_2067.JPG', '4.6 MB', 'paused')
            + file_row('ph26', 'IMG_2066.JPG', '4.1 MB', 'paused'))
offline = f'''{modal_bar(close_href=CLOSE)}
  {offline_banner("You're offline. Uploads continue when you're back online.")}
  {stepper("Select items", 2, 3)}
  <div class="min-h-0 flex-1 space-y-4 overflow-hidden px-gutter pt-1">
    <div>
      <p class="text-label tabular-nums" role="status">Uploaded 12 of 30 photos. Paused.</p>
      <div class="mt-2 h-1.5 overflow-hidden rounded-full bg-muted" role="progressbar" aria-valuenow="12" aria-valuemin="0" aria-valuemax="30" aria-label="12 of 30 photos uploaded, paused"><div class="h-full w-[40%] rounded-full bg-muted-foreground"></div></div>
    </div>
    <ul class="divide-y overflow-hidden rounded-group bg-card">{off_rows}</ul>
  </div>
  {bottom("Continue", disabled=True, note="You can continue when the upload finishes.")}'''
P.frame('S18-web-offline', 'Web, mobile browser: offline, uploads paused', web_phone(offline))

P.write('S18-photos-import.html')
