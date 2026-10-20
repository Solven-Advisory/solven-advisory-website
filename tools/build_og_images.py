#!/usr/bin/env python3
"""Share images (Open Graph and Twitter cards) for site v5, 1200x630 PNG, in assets/og/:

    en.png, pt.png             each language's home card: the hero title; every page without its own card uses it
    en/<slug>.png, pt/<slug>.png   one card per insight: its title and topic

Design approved by the owner on 2026-10-20 (direction "Calcada"): the page ground under the hero's calcada
texture, the outlined wordmark, the title in the heading serif, a thin rule, then the address and the city.
All text comes from content/site-copy.md and the insights' front matter, read through build_site_v5.

Rendered with headless Chromium (CHROME_PATH, else the newest Playwright Chromium in ~/.cache/ms-playwright,
else chromium or google-chrome on PATH). Run it after changing the hero title or adding or retitling an insight,
then rebuild: python3 tools/build_og_images.py && python3 tools/build_site_v5.py --prod
The production build fails if a page names a card that does not exist.
"""
import base64
import html
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site_v5 as v5  # noqa: E402
import svg_paths  # noqa: E402

ROOT = v5.ROOT
OUT = ROOT / "assets/og"
W, H = 1200, 630


def chrome():
    found = [os.environ.get("CHROME_PATH")] + sorted(Path.home().glob(".cache/ms-playwright/chromium-*/chrome-linux64/chrome"), reverse=True)
    found += [shutil.which(n) for n in ("chromium", "chromium-browser", "google-chrome")]
    for c in found:
        if c and Path(c).is_file():
            return str(c)
    raise SystemExit("No Chromium found: set CHROME_PATH")


def data_uri(path, mime):
    return f"data:{mime};base64,{base64.b64encode(Path(path).read_bytes()).decode()}"


FONTS = "\n".join(
    f'@font-face {{ font-family: "{family}"; font-weight: 300 700; src: url({data_uri(ROOT / "assets/fonts" / f"{file}-{subset}.woff2", "font/woff2")}) format("woff2");'
    + (" unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+1E00-1E9F; }" if subset == "latin-ext" else " }")
    for family, file in (("Source Serif 4", "source-serif-4-v15"), ("Source Sans 3", "source-sans-3-v20"))
    for subset in ("latin", "latin-ext"))
CALCADA = "data:image/svg+xml;base64," + base64.b64encode(
    svg_paths.minify((ROOT / "explorations/site/img/calcada-wave.svg").read_text()).encode()).decode()
WORDMARK = re.sub(r"<svg ", '<svg style="height: 52px; width: auto; display: block; align-self: flex-start" ',
                  re.search(r'<svg class="logo__svg".*?</svg>', v5.v4.HEADER, re.S).group(0), count=1)

# The site's tokens (site.css): ground, anchor, muted text, rule, and the logo's two colour slots on light grounds
STYLE = FONTS + """
* { margin: 0; box-sizing: border-box; }
html, body { width: 1200px; height: 630px; overflow: hidden; }
body { position: relative; background: #FAF9F6; color: #2A2A28; font-family: "Source Sans 3", sans-serif; -webkit-font-smoothing: antialiased; }
.logo__word { fill: #2A2A28; } .logo__mark { fill: #6B8068; }
.texture { position: absolute; inset: 0; background: url(%s) center top / 200px 200px repeat; opacity: .12; }
.card { position: absolute; inset: 72px 96px 64px; display: flex; flex-direction: column; }
.main { margin: auto 0; }
h1 { font-family: "Source Serif 4", serif; font-weight: 400; font-optical-sizing: auto; font-size: 80px; line-height: 1.08;
     letter-spacing: -0.015em; text-wrap: balance; max-width: 13em; }
h1.long { font-size: 64px; }
.meta { margin-top: 20px; font-size: 26px; color: #5E6066; }
.foot { border-top: 1px solid #D9D6D0; padding-top: 20px; font-size: 24px; color: #5E6066; }
""" % CALCADA


def card(title, place, meta=None):
    e = html.escape
    long = ' class="long"' if len(title) > 40 else ""
    meta = f'<p class="meta">{e(meta)}</p>' if meta else ""
    return f"""<!doctype html><meta charset="utf-8"><style>{STYLE}</style>
<div class="texture"></div>
<div class="card">{WORDMARK}<div class="main"><h1{long}>{e(title)}</h1>{meta}</div><p class="foot">solvenadvisory.ai · {e(place)}</p></div>"""


def cards():
    for lang in ("en", "pt"):
        t = v5.COPY[lang]
        place = t.raw("footer.city")
        yield OUT / f"{lang}.png", card(t.raw("home.hero.title"), place)
        for a in v5.ARTICLES[lang]:
            yield OUT / lang / f"{a['slug']}.png", card(a["title"], place, f"{t.raw('nav.insights')} · {a['topic']}")


def render(browser, page, png, tmp):
    src = Path(tmp) / "card.html"
    src.write_text(page)
    png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={W},{H}", "--virtual-time-budget=10000", f"--screenshot={png}", src.as_uri()],
                   check=True, capture_output=True)
    w, h = struct.unpack(">II", png.read_bytes()[16:24])
    if (w, h) != (W, H):
        raise SystemExit(f"{png.relative_to(ROOT)} is {w}x{h}, not {W}x{H}")


if __name__ == "__main__":
    browser = chrome()
    if OUT.exists():
        shutil.rmtree(OUT)      # generated: start clean so a removed insight's card does not linger
    with tempfile.TemporaryDirectory() as tmp:
        for png, page in cards():
            render(browser, page, png, tmp)
            print(png.relative_to(ROOT), png.stat().st_size, "bytes")
