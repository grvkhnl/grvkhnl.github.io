#!/usr/bin/env python3
"""Render the two diagram-based social cards (requires librsvg and ImageMagick)."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
for post, name in [('the-asymmetry-of-information', 'forward-reverse-kl'),
                   ('the-bridge', 'bridge-paths')]:
    figures = root/'posts'/post/'figures'
    with tempfile.TemporaryDirectory() as tmp:
        rendered = Path(tmp)/'figure.png'
        subprocess.run(['rsvg-convert', '-w', '1160', '-h', '590', '-a',
                        str(figures/(name+'.svg')), '-o', str(rendered)], check=True)
        subprocess.run(['magick', str(rendered), '-background', '#fff1dc',
                        '-gravity', 'center', '-extent', '1200x630',
                        str(figures/'social-preview.png')], check=True)
    print(figures/'social-preview.png')
