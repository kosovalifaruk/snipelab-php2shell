"""Real local HTTP fixtures. They do not run PHP or reproduce either CVE."""
import hashlib
import importlib.util
import json
import threading
import unittest
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check', ROOT / 'tools/check.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
spec2 = importlib.util.spec_from_file_location('model', ROOT / 'tools/lifecycle_model.py')
model = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(model)

class Fixture(BaseHTTPRequestHandler):
    wrong_version = False
    corrupt_upload = False
    redirect = False
    def log_message(self, *args):
        pass
    def send_json(self, payload, code=200):
        raw = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
    def do_GET(self):
        if self.redirect:
            self.send_response(302)
            self.send_header('Location', 'http://example.invalid/no-follow')
            self.end_headers()
            return
        target = next(t for t in check.TARGETS if t[1] == self.server.server_port)
        name, port, version, sapi, progress = target
        self.send_json({'lab': 'SnipeLab-PHP2Shell',
                        'php_version': '0.0.0' if self.wrong_version else version,
                        'sapi': sapi, 'pid': port,
                        'upload_progress': progress, 'fatal_backtraces': progress,
                        'ini_scanned': '00-lab.ini;99-mitigation.ini'})
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        if self.path == '/oom.php':
            self.send_json({'fixture': True}, 500)
            return
        message = BytesParser(policy=policy.default).parsebytes(
            ('Content-Type: ' + self.headers['Content-Type'] + '\r\n\r\n').encode() + body)
        parts = list(message.iter_parts())
        data = parts[0].get_payload(decode=True)
        self.send_json({'accepted': True, 'persisted': False, 'size': len(data),
                        'sha256': 'bad' if self.corrupt_upload
                        else hashlib.sha256(data).hexdigest()})

class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servers = []
        try:
            for _, port, *_ in check.TARGETS:
                s = ThreadingHTTPServer(('127.0.0.1', port), Fixture)
                cls.servers.append(s)
                threading.Thread(target=s.serve_forever, daemon=True).start()
        except Exception:
            cls.tearDownClass()
            raise
    @classmethod
    def tearDownClass(cls):
        for s in cls.servers:
            s.shutdown()
            s.server_close()
    def tearDown(self):
        Fixture.wrong_version = Fixture.corrupt_upload = Fixture.redirect = False
    def test_all_five_http_fixtures_pass(self):
        result = check.run(fpm=True)
        self.assertTrue(result['pass'])
        self.assertEqual(len(result['results']), 5)
        self.assertFalse(result['cve_exploitation_tested'])
    def test_wrong_version_fails(self):
        Fixture.wrong_version = True
        self.assertFalse(check.run()['pass'])
    def test_upload_corruption_fails(self):
        Fixture.corrupt_upload = True
        self.assertFalse(check.run()['pass'])
    def test_redirect_not_followed(self):
        Fixture.redirect = True
        code, _ = check.fetch(18081, '/status.php')
        self.assertEqual(code, 302)
    def test_oom_500_is_not_exploit_proof(self):
        result = check.run(oom=True)
        self.assertTrue(result['pass'])
        for item in result['results']:
            self.assertFalse(item['oom_observation']['oom_confirmed'])
    def test_unknown_target_is_rejected(self):
        with self.assertRaises(ValueError):
            check.fetch(80, '/status.php')
    def test_bad_endpoint_is_rejected(self):
        with self.assertRaises(ValueError):
            check.fetch(18081, '/other')
    def test_lifecycle_invariants(self):
        self.assertFalse(model.simulate(False)['invariant_ok'])
        self.assertTrue(model.simulate(True)['invariant_ok'])

if __name__ == '__main__':
    unittest.main()
