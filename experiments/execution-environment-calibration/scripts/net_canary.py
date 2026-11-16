"""Local HTTP canary for B4. Logs every request; serves nothing of interest.

Usage: python net_canary.py <log_file>
Run under `timeout` so it exits on its own. Any line in the log is a network hit.
"""
import datetime
import http.server
import sys

LOG = sys.argv[1]


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


http.server.ThreadingHTTPServer(("127.0.0.1", 8765), Canary).serve_forever()
