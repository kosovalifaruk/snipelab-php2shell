#!/usr/bin/env python3
"""Fixed-loopback functional controls. No claim of CVE exploitation."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import (Request, build_opener, ProxyHandler,
                            HTTPRedirectHandler)

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = b'SnipeLab normal upload\n'
TARGETS = [
    ('apache-old', 18081, '8.5.11', 'apache2handler', True),
    ('apache-fixed', 18082, '8.5.12', 'apache2handler', True),
    ('apache-mitigated', 18083, '8.5.11', 'apache2handler', False),
    ('fpm-old', 18084, '8.5.11', 'fpm-fcgi', True),
    ('fpm-fixed', 18085, '8.5.12', 'fpm-fcgi', True),
]

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

OPENER = build_opener(ProxyHandler({}), NoRedirect())

def fetch(port, path, data=None, headers=None):
    if port not in {t[1] for t in TARGETS}:
        raise ValueError('Port is not an authorized fixed lab port')
    if path not in ('/status.php', '/upload.php', '/oom.php'):
        raise ValueError('Unknown lab endpoint')
    req = Request('http://127.0.0.1:%d%s' % (port, path),
                  data=data, headers=headers or {})
    try:
        with OPENER.open(req, timeout=10) as response:
            raw = response.read(65537)
            if len(raw) > 65536:
                raise ValueError('Response exceeds evidence size limit')
            parsed = json.loads(raw)
            if not isinstance(parsed, dict):
                raise ValueError('Expected a JSON object')
            return response.status, parsed
    except HTTPError as exc:
        exc.close()
        return exc.code, {'http_error': True}

def multipart():
    boundary = 'SnipeLabBoundary01'
    body = ('--' + boundary + '\r\n'
            'Content-Disposition: form-data; name="probe"; '
            'filename="probe.txt"\r\n'
            'Content-Type: text/plain\r\n\r\n').encode()
    body += PAYLOAD + ('\r\n--' + boundary + '--\r\n').encode()
    return body, {'Content-Type': 'multipart/form-data; boundary=' + boundary}

def inspect_target(target, oom=False):
    name, port, version, sapi, progress = target
    item = {'target': name, 'checks': {}, 'scope': 'functional_baseline',
            'security_posture': ('patched_for_two_cves_only' if 'fixed' in name
                                 else 'known_affected_partial_mitigation'
                                 if 'mitigated' in name else 'known_affected_comparison')}
    try:
        code, status = fetch(port, '/status.php')
        checks = item['checks']
        checks['status_http'] = code == 200
        checks['identity'] = status.get('lab') == 'SnipeLab-PHP2Shell'
        checks['version'] = status.get('php_version') == version
        checks['sapi'] = status.get('sapi') == sapi
        checks['upload_progress'] = status.get('upload_progress') is progress
        checks['fatal_backtraces'] = status.get('fatal_backtraces') is progress
        checks['baseline_ini'] = '00-lab.ini' in str(status.get('ini_scanned'))
        if not progress:
            checks['mitigation_ini'] = '99-mitigation.ini' in str(status.get('ini_scanned'))
        item['status'] = status
        body, headers = multipart()
        code, upload = fetch(port, '/upload.php', body, headers)
        checks['normal_upload'] = (
            code == 200 and upload.get('accepted') is True
            and upload.get('size') == len(PAYLOAD)
            and upload.get('persisted') is False
            and upload.get('sha256') == hashlib.sha256(PAYLOAD).hexdigest())
        if oom:
            observation = {'scope': 'bounded_oom_observation',
                           'oom_confirmed': False,
                           'requires': 'Correlate LAB_BOUNDED_OOM_DEMO with runtime logs'}
            try:
                code, reply = fetch(port, '/oom.php', b'')
                observation.update(http_status=code, reply=reply)
            except (OSError, ValueError, URLError) as exc:
                observation['transport_error'] = str(exc)
            # A disconnected request/500 is observation, never exploit evidence.
            code, after = fetch(port, '/status.php')
            checks['healthy_after_oom_request'] = (
                code == 200 and after.get('lab') == 'SnipeLab-PHP2Shell')
            observation['after'] = after
            item['oom_observation'] = observation
    except (OSError, ValueError, URLError) as exc:
        item['error'] = str(exc)
        item['checks']['reachable_and_parseable'] = False
    item['pass'] = bool(item['checks']) and all(item['checks'].values())
    return item

def run(fpm=False, oom=False):
    targets = TARGETS if fpm else TARGETS[:3]
    results = [inspect_target(t, oom) for t in targets]
    return {'schema': 'snipelab-controls-v1',
            'time_utc': datetime.now(timezone.utc).isoformat(),
            'scope': 'version_configuration_upload_only',
            'cve_exploitation_tested': False,
            'results': results, 'pass': all(x['pass'] for x in results)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fpm', action='store_true')
    parser.add_argument('--oom-demo', action='store_true')
    args = parser.parse_args()
    result = run(args.fpm, args.oom_demo)
    evidence = ROOT / 'evidence'
    evidence.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    dest = evidence / ('checks-' + stamp + '.json')
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({'pass': result['pass'], 'evidence': str(dest),
                      'scope': result['scope']}, ensure_ascii=False))
    return 0 if result['pass'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
