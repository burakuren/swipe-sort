#!/usr/bin/env python3
"""python3 tools/qa/frame-text.py [regex-for-frame-id] [--grep REGEX]
Prints the visible text of frames (one line per text node, joined with ' | ') for QA review."""
import re, glob, sys, os
ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'design', '03-screens')
args = sys.argv[1:]
grep = None
if '--grep' in args:
    i = args.index('--grep'); grep = re.compile(args[i+1], re.I); args = args[:i] + args[i+2:]
fre = re.compile(args[0]) if args else None
for f in sorted(glob.glob(os.path.join(ROOT, 'S*.html'))):
    html = open(f, encoding='utf8').read()
    for p in re.split(r'(?=<[a-z]+[^>]*\sdata-frame=")', html):
        m = re.match(r'<[a-z]+[^>]*\sdata-frame="([^"]+)"', p)
        if not m: continue
        fid = m.group(1)
        if fre and not fre.search(fid): continue
        t = re.sub(r'<script.*?</script>', ' ', p, flags=re.S)
        t = re.sub(r'<figcaption.*?</figcaption>', ' ', t, flags=re.S)
        t = re.sub(r'aria-label="([^"]*)"', r'>[aria: \1]<', t)
        t = re.sub(r'<[^>]+>', '\n', t)
        t = t.replace('&#39;', "'").replace('&amp;', '&').replace('&nbsp;', ' ')
        lines = [x.strip() for x in t.split('\n') if x.strip()]
        if grep:
            hits = [x for x in lines if grep.search(x)]
            if hits: print(f'{fid}: ' + ' | '.join(hits))
        else:
            print(f'===== {fid}\n' + ' | '.join(lines))
