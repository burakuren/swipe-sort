#!/usr/bin/env python3
"""python3 tools/qa/dialogs.py [frame-regex]
Lists every dialog (role=dialog|alertdialog) in frames: title/body text, buttons with variant (destructive /
primary / other), whether it contains an icon, and whether its wrapper centers it vertically."""
import re, glob, os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'design', '03-screens')
fre = re.compile(sys.argv[1]) if len(sys.argv) > 1 else None
def text(s):
    s = re.sub(r'<[^>]+>', '\n', s).replace('&#39;', "'").replace('&amp;', '&')
    return ' | '.join(x.strip() for x in s.split('\n') if x.strip())
for f in sorted(glob.glob(os.path.join(ROOT, 'S*.html'))):
    html = open(f, encoding='utf8').read()
    for p in re.split(r'(?=<[a-z]+[^>]*\sdata-frame=")', html):
        m = re.match(r'<[a-z]+[^>]*\sdata-frame="([^"]+)"', p)
        if not m: continue
        fid = m.group(1)
        if fre and not fre.search(fid): continue
        for d in re.finditer(r'<(div|section)([^>]*role="(?:alert)?dialog"[^>]*)>', p):
            start = d.start()
            # crude: take until 3000 chars or next data-frame
            chunk = p[start:start + 6000]
            # balance divs
            depth = 0; end = None
            for t in re.finditer(r'<(/?)(div|section)\b', chunk):
                depth += -1 if t.group(1) else 1
                if depth == 0: end = t.end(); break
            body = chunk[:end] if end else chunk
            attrs = d.group(2)
            wrapper = p[max(0, start - 400):start]
            centered = 'items-center' in wrapper.split('<')[-1] or 'justify-center' in wrapper.split('<')[-1] or 'my-auto' in attrs or 'top-1/2' in attrs
            icon = bool(re.search(r'i-lucide-', body))
            if 'sheet' in attrs or 'rounded-t-sheet' in attrs: continue
            btns = []
            for b in re.finditer(r'<(button|a)\b([^>]*)>(.*?)</\1>', body, re.S):
                cls = re.search(r'class="([^"]*)"', b.group(2)); cls = cls.group(1) if cls else ''
                v = 'DESTRUCTIVE' if 'bg-destructive' in cls or 'text-destructive' in cls else ('PRIMARY' if 'bg-primary ' in cls + ' ' else '')
                btns.append(f"{text(b.group(3))}{'['+v+']' if v else ''}")
            print(f"{fid}: centered={centered} icon={icon} :: {text(body)[:400]} :: BUTTONS {btns}")
