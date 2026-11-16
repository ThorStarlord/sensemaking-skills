"""Local HTTP canary for B4. Logs every request; serves nothing of interest.

Usage: python net_canary.py <log_file>
Run under `timeout` so it exits on its own. Any line in the log is a network hit.
"""
import datetime
import http.server
import os
import sys

LOG = sys.argv[1]
PORT = int(sys.argv[2])


class Exclusive(http.server.ThreadingHTTPServer):
    # HTTPServer sets allow_reuse_address; on Windows that lets several processes share one port,
    # which made earlier canary results unverifiable (PREREG-AMENDMENT-4.md).
    allow_reuse_address = False


class Canary(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(f"{stamp} GET {self.path} from {self.client_address[0]}\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"NET_CANARY\n")

    def log_message(self, *args):
        pass


try:
    server = Exclusive(("127.0.0.1", PORT), Canary)
except OSError as exc:
    print(f"CANARY_BIND_FAILED port={PORT}: {exc}", file=sys.stderr)
    sys.exit(3)
with open(LOG + ".ready", "w", encoding="utf-8") as fh:
    fh.write(f"port={PORT} pid={os.getpid()}\n")
server.serve_forever()
