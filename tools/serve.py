#!/usr/bin/env python3
"""Serve the site locally the way Vercel serves it in production.

    python3 tools/serve.py           # http://127.0.0.1:8000
    python3 tools/serve.py 3000      # pick a port

Plain `python3 -m http.server` is not enough: internal links are
extensionless (`vercel.json` sets cleanUrls), so `/about` would 404.
This mirrors the production rules: clean URLs, no trailing slash,
`.html` redirects to the clean path, `/blog.html` to `/blog`, and the
custom `404.html` on misses. Nothing here is deployed; it is a
preview server only.
"""
import os
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = urlsplit(self.path).path

        # /blog.html -> /blog, /about.html -> /about
        if path.endswith(".html"):
            target = "/" if path == "/index.html" else path[: -len(".html")]
            return self.redirect(target)

        # /about/ -> /about  (trailingSlash: false)
        if len(path) > 1 and path.endswith("/"):
            return self.redirect(path.rstrip("/"))

        # /about -> about.html, /pt -> pt/index.html
        disk = os.path.join(ROOT, path.lstrip("/"))
        if not os.path.isfile(disk):
            for candidate in (disk + ".html", os.path.join(disk, "index.html")):
                if os.path.isfile(candidate):
                    self.path = "/" + os.path.relpath(candidate, ROOT)
                    break
            else:
                return self.not_found()

        return super().send_head()

    def redirect(self, location):
        self.send_response(308)
        self.send_header("Location", location)
        self.end_headers()
        return None

    def not_found(self):
        body = open(os.path.join(ROOT, "404.html"), "rb").read()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
        return None


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = partial(Handler, directory=ROOT)
    print(f"Solven Advisory on http://127.0.0.1:{port}  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", port), handler).serve_forever()
