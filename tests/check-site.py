#!/usr/bin/env python3
"""Check local HTML asset references without crawling external services."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import sys
ROOT=Path(__file__).resolve().parents[1]
errors=[];checked=0
class Check(HTMLParser):
    def __init__(self,source):super().__init__();self.source=source
    def handle_starttag(self,tag,attrs):
        global checked
        a=dict(attrs);value=a.get('src') if tag in {'img','script','source','video','audio'} else a.get('href') if tag=='link' and a.get('rel') in {'stylesheet','icon','preload'} else None
        if not value:return
        u=urlsplit(value)
        if u.scheme or u.netloc or not u.path:return
        p=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else self.source.parent/unquote(u.path)
        checked+=1
        if not p.is_file():errors.append(f'{self.source.relative_to(ROOT)}: missing asset {u.path}')
files=sorted(ROOT.glob('*.html'))
if not files:errors.append('No root HTML entry point')
for p in files:
    parser=Check(p);parser.feed(p.read_text());parser.close()
for error in errors:print(error)
print(f'HTML files: {len(files)}; local assets checked: {checked}; errors: {len(errors)}')
sys.exit(1 if errors else 0)
