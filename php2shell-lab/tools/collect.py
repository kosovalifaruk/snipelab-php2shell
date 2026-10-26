#!/usr/bin/env python3
"""Collect evidence and generate digest overrides from already pulled images."""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = {'PHP_OLD_APACHE': 'php:8.5.11-apache',
          'PHP_FIXED_APACHE': 'php:8.5.12-apache',
          'PHP_OLD_FPM': 'php:8.5.11-fpm',
          'PHP_FIXED_FPM': 'php:8.5.12-fpm',
          'NGINX_IMAGE': 'nginx:1.28.0-alpine'}

def command(args):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=45)
    return {'argv': args, 'returncode': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', action='store_true')
    parser.add_argument('--fpm', action='store_true')
    args = parser.parse_args()
    records, locked = [], []
    selected = IMAGES if args.fpm else dict(list(IMAGES.items())[:2])
    for key, tag in selected.items():
        item = command(['docker', 'image', 'inspect', tag])
        records.append(item)
        if item['returncode'] != 0:
            raise RuntimeError('Image missing: ' + tag)
        digests = json.loads(item['stdout'])[0].get('RepoDigests', [])
        if not digests:
            raise RuntimeError('No registry digest for ' + tag)
        # Official repository expected; no arbitrary digest is manufactured.
        repo = tag.split(':')[0]
        matching = [x for x in digests if x.split('@')[0].split('/')[-1] == repo]
        if not matching:
            raise RuntimeError('No matching repository digest: ' + repo)
        locked.append(key + '=' + matching[0])
    if args.lock:
        (ROOT / 'images.lock.env').write_text('\n'.join(locked) + '\n')
    compose = ['docker', 'compose']
    if (ROOT / 'images.lock.env').exists():
        compose += ['--env-file', 'images.lock.env']
    for cmd in [['docker', 'version'], ['docker', 'compose', 'version'],
                compose + ['--profile', 'fpm', 'config'],
                compose + ['--profile', 'fpm', 'ps', '-a'],
                ['docker', 'network', 'inspect', 'php2shell-defense-lab_lab']]:
        records.append(command(cmd))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    directory = ROOT / 'evidence'
    directory.mkdir(exist_ok=True)
    path = directory / ('inventory-' + stamp + '.json')
    path.write_text(json.dumps({'time_utc': stamp, 'records': records}, indent=2))
    print(path)

if __name__ == '__main__':
    main()
