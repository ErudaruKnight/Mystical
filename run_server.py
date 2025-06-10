import http.server
import socketserver
import webbrowser
import pathlib

PORT = 8000
DIR = pathlib.Path(__file__).resolve().parent / "rune_circle"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIR), **kwargs)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    url = f"http://localhost:{PORT}/index.html"
    print(f"Serving {DIR} at {url}")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    httpd.serve_forever()
