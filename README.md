# Mystical

This repository contains a PostScript-based system for drawing magical circles and a small web prototype for experimenting with rune circles.

## Running the Rune Circle Demo

1. Install Python 3 (if not already installed).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. From the repository root, run:
   ```bash
   python3 run_server.py
   ```
   This starts a local web server and opens the demo in your browser. If port
   8000 is unavailable, you can pass a different port number, e.g.
   `python3 run_server.py 8080`.
4. Use the interface to add runes or nested circles. The interpretation of the spell is shown below the buttons.

The PostScript files for the original Mystical project are located under `mystical_ps/`. See `mystical_ps/README.md` for full documentation.
