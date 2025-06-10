import http.server
import socketserver
import webbrowser
import pathlib
import sys

PORT = 8000
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        pass

DIR = pathlib.Path(__file__).resolve().parent / "rune_circle"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIR), **kwargs)


def main() -> None:
    url = f"http://localhost:{PORT}/index.html"
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Serving {DIR} at {url}")
            try:
                webbrowser.open(url)
            except Exception:
                pass
            httpd.serve_forever()
    except OSError as exc:
        print(f"Could not start server on port {PORT}: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
