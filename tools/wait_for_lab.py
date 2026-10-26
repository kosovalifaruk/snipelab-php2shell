#!/usr/bin/env python3
"""Bounded readiness wait for the five fixed loopback laboratory endpoints."""
import argparse
import importlib.util
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lab_check', ROOT / 'php2shell-lab/tools/check.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fpm', action='store_true')
    args = parser.parse_args()
    targets = check.TARGETS if args.fpm else check.TARGETS[:3]
    deadline = time.monotonic() + 45
    pending = {t[1] for t in targets}
    while pending and time.monotonic() < deadline:
        for port in list(pending):
            try:
                code, status = check.fetch(port, '/status.php')
                if code == 200 and status.get('lab') == 'SnipeLab-PHP2Shell':
                    pending.remove(port)
            except (OSError, ValueError):
                pass
        if pending:
            time.sleep(0.5)
    if pending:
        raise SystemExit('Laboratory readiness failed for ports: ' + str(sorted(pending)))
    print('Fixed loopback endpoints are ready; run functional checks next')
