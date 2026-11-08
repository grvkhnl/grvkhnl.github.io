#!/usr/bin/env python3
"""Compile the canonical TikZ sources into light/dark, desktop/mobile SVGs.

Requires XeLaTeX and pdftocairo. Numerical data are tracked; regenerate them
separately with generate-diagram-data.py (NumPy/SciPy) when changing examples.
"""
import argparse
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--figure', action='append', help='Stem of a figure to rebuild (repeatable)')
args = parser.parse_args()
sources = sorted(ROOT.glob('posts/*/figures/source/*.tex'))
sources = [p for p in sources if not p.name.startswith('chapter') and
           (not args.figure or p.stem in args.figure)]
if not sources:
    parser.error('No matching figures')
for source in sources:
    build = source.parent.parent / 'build'
    build.mkdir(exist_ok=True)
    for suffix, defines in [('', ''), ('-dark', r'\def\darkmode{1}'),
                            ('-mobile', r'\def\mobile{1}'),
                            ('-mobile-dark', r'\def\mobile{1}\def\darkmode{1}')]:
        stem = source.stem + suffix
        command = ['xelatex', '-interaction=nonstopmode', '-halt-on-error',
                   '-output-directory=../build', '-jobname=' + stem,
                   defines + r'\input{' + source.name + '}']
        result = subprocess.run(command, cwd=source.parent, text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stdout[-6000:] + result.stderr)
        svg = source.parent.parent / (stem + '.svg')
        subprocess.run(['pdftocairo', '-svg', str(build / (stem + '.pdf')), str(svg)], check=True)
        # pdftocairo omits the PDF page color. Give every standalone SVG an
        # explicit background, including when opened or shared outside the blog.
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
        tree = ET.parse(svg)
        root = tree.getroot()
        width, height = root.attrib['viewBox'].split()[2:]
        background = ET.Element('{http://www.w3.org/2000/svg}rect', {
            'width': width, 'height': height,
            'fill': '#0d1117' if 'dark' in suffix else '#fff1dc'})
        root.insert(0, background)
        tree.write(svg, encoding='utf-8', xml_declaration=True)
        print(svg.relative_to(ROOT), flush=True)
