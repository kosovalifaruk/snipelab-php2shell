#!/usr/bin/env python3
"""Verify public package integrity, local Markdown links and source appendix."""
import hashlib
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'php2shell-lab'
STEM = 'SnipeLab_PHP2Shell_Teknik_Analiz_ve_Kurumsal_Savunma_Raporu'


def verify_hashes(base):
    count = 0
    for line in (base / 'SHA256SUMS').read_text().splitlines():
        digest, rel = line.split('  ', 1)
        path = (base / rel).resolve()
        if not path.is_relative_to(base.resolve()):
            raise ValueError('Manifest path outside package: ' + rel)
        if not path.is_file():
            raise ValueError('Missing file: ' + rel)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Hash mismatch: ' + rel)
        count += 1
    return count


def verify_links():
    checked = 0
    for doc in ROOT.rglob('*.md'):
        if '.git' in doc.parts:
            continue
        # Do not mistake source-code examples for prose links.
        text = re.sub(r'```.*?```', '', doc.read_text(), flags=re.S)
        for target in re.findall(r'\]\(([^\s)]+)\)', text):
            if target.startswith(('http:', 'https:', 'mailto:', '#')):
                continue
            rel = unquote(target.split('#', 1)[0])
            path = (doc.parent / rel).resolve()
            if not path.is_relative_to(ROOT.resolve()) or not path.exists():
                raise ValueError('Broken local link in %s: %s' % (doc.name, target))
            checked += 1
    return checked


def verify_sources():
    report = (ROOT / 'docs' / (STEM + '.md')).read_text()
    paths = list((LAB / 'app').glob('*.php'))
    paths += list((LAB / 'config').iterdir())
    paths += list((LAB / 'tools').glob('*.py'))
    paths += list((LAB / 'tests').glob('*.py'))
    paths += [LAB / 'compose.yaml']
    for path in paths:
        if path.read_text().rstrip() not in report:
            raise ValueError('Source differs from report appendix: ' + str(path))
    for ext in ('pdf',):
        if not (ROOT / 'docs' / (STEM + '.' + ext)).is_file():
            raise ValueError('Missing report format: ' + ext)
    return len(paths)


def main():
    total = verify_hashes(ROOT)
    lab = verify_hashes(LAB)
    links = verify_links()
    sources = verify_sources()
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts:
            continue
        if path.name in ('images.lock.env', '.env'):
            raise ValueError('Local runtime configuration must not ship: ' + str(path))
        if path.stat().st_size > 25 * 1024 * 1024:
            raise ValueError('File exceeds browser upload size: ' + str(path))
    print('PASS: %d repository hashes, %d lab hashes, %d local links, %d source files'
          % (total, lab, links, sources))
    print('Scope: publication integrity; not Docker/PHP runtime or CVE exploitation')

if __name__ == '__main__':
    main()
