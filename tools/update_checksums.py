#!/usr/bin/env python3
"""Refresh public package manifests; runtime evidence is intentionally excluded."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def public_files(base):
    for p in sorted(base.rglob('*')):
        rel = p.relative_to(base)
        if not p.is_file() or p.name == 'SHA256SUMS':
            continue
        if any(x in rel.parts for x in ('.git', '__pycache__', '.venv', 'dist')):
            continue
        if p.suffix in ('.pyc', '.pyo', '.log') or p.name == '.DS_Store':
            continue
        if 'evidence' in rel.parts and p.name != '.gitkeep':
            continue
        if p.name == 'images.lock.env' or p.name.startswith('.env'):
            continue
        yield p

def manifest(base):
    return ''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  '
                   + p.relative_to(base).as_posix() + '\n' for p in public_files(base))

if __name__ == '__main__':
    lab = ROOT / 'php2shell-lab'
    (lab / 'SHA256SUMS').write_text(manifest(lab))
    # Root list includes the lab manifest as well.
    lines = manifest(ROOT)
    path = lab / 'SHA256SUMS'
    lines += hashlib.sha256(path.read_bytes()).hexdigest() + '  php2shell-lab/SHA256SUMS\n'
    (ROOT / 'SHA256SUMS').write_text(lines)
    print('Updated repository and laboratory SHA256SUMS')
