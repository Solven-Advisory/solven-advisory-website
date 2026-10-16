"""Padrão dos Descobrimentos for the wow lab 2 Padrão variants (HP1, HP2, KP1, KP2).

Reads the owner's traced image (docs/references/images/padrao-4-detailed.svg: eight sepia
tone layers and one outline) and writes explorations/wow/padrao.svg with the tones mapped,
light to dark, onto the site's warm greys (ledger.css and wow.css tokens). Coordinates are
rounded to whole units (the image is never shown above 1500px), which roughly halves the file.
Mirroring for the right-hand variants is done in CSS, so one file serves both sides.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs/references/images/padrao-4-detailed.svg"
OUT = ROOT / "explorations/wow/padrao.svg"

GREYS = {
    "#f3ebde": "#E8E6E1",   # stone in full light, a step darker than the band #EFEDE9
    "#e6dac7": "#D9D6D0",   # --c-rule
    "#cdbb9f": "#BAB8B1",   # --c-on-anchor-muted
    "#a99376": "#8E8C85",   # --tile-ink
    "#7c6a53": "#66645E",
    "#4f4336": "#46463F",   # --c-rule-on-anchor
    "#2a231e": "#2A2A28",   # --c-anchor
    "#1f1a16": "#1C1D20",   # --c-text (shadow ink and outline)
}


def build():
    s = SRC.read_text()
    s = re.sub(r"<title>.*?</title>", "<title>Padrão dos Descobrimentos, greyscale</title>", s)
    s = re.sub(r'(fill|stroke)="(#[0-9a-f]{6})"', lambda m: f'{m.group(1)}="{GREYS[m.group(2)]}"', s)
    s = re.sub(r'd="([^"]*)"', lambda m: 'd="' + re.sub(r"-?\d+\.\d+", lambda n: str(round(float(n.group(0)))), m.group(1)) + '"', s)
    assert chr(0x2014) not in s and chr(0x2013) not in s
    OUT.write_text(s)
    return OUT


if __name__ == "__main__":
    p = build()
    print(p.relative_to(ROOT), p.stat().st_size, "bytes")
