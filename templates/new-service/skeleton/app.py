"""Tiny demo service (stdlib only): shows version, environment, feature flags and certificate status."""
import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

APP_NAME = os.environ.get("APP_NAME", "claims-api")
MESSAGE = "Claims intake API"
CERT_PATH = os.environ.get("CERT_PATH", "/etc/claims/tls/tls.crt")
COLORS = {"sit": "#0078D4", "uat": "#F0AB00", "preview": "#8A3FFC", "spike": "#EE0000"}


def status():
    try:
        with open(CERT_PATH, "rb") as f:
            cert = {"loaded": True, "sha256": hashlib.sha256(f.read()).hexdigest()[:12]}
    except OSError:
        cert = {"loaded": False}
    return {
        "app": APP_NAME,
        "message": MESSAGE,
        "version": os.environ.get("APP_VERSION", "dev"),
        "environment": os.environ.get("ENVIRONMENT", "local"),
        "features": os.environ.get("FEATURE_FLAGS", "none"),
        "certificate": cert,
        "pod": os.environ.get("HOSTNAME", "local"),
    }


PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>{app}</title>
<style>body{{font-family:Segoe UI,Arial;background:#141B2E;color:#E8EAF0;display:grid;place-items:center;height:100vh;margin:0}}
.c{{background:#24304E;border-top:8px solid {color};border-radius:10px;padding:32px 48px;min-width:420px}}
h1{{margin:0 0 4px;color:#fff}} td{{padding:4px 16px 4px 0}} .k{{color:#9AA3B8}}</style></head>
<body><div class="c"><h1>{app}</h1><div class="k">{message}</div><table>
<tr><td class="k">Environment</td><td><b>{environment}</b></td></tr>
<tr><td class="k">Version</td><td><b>{version}</b></td></tr>
<tr><td class="k">Feature flags</td><td>{features}</td></tr>
<tr><td class="k">Key Vault cert</td><td>{cert}</td></tr>
<tr><td class="k">Pod</td><td>{pod}</td></tr></table></div></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        if self.path.startswith("/healthz"):
            return self._send(200, "text/plain", "ok")
        s = status()
        if self.path.startswith("/api"):
            return self._send(200, "application/json", json.dumps(s, indent=2))
        env = s["environment"].split("-")[0]
        cert = "loaded (sha256 " + s["certificate"]["sha256"] + ")" if s["certificate"]["loaded"] else "not mounted"
        self._send(200, "text/html", PAGE.format(color=COLORS.get(env, "#3FB950"), cert=cert, **s))

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"{APP_NAME} listening on :8080")
    HTTPServer(("", 8080), Handler).serve_forever()
