"""Smaller SVG drawings for the production build: the same shapes, written more compactly.

    import svg_paths
    small = svg_paths.minify(text)

Each path's d attribute is rewritten with relative commands (m, l, h, v, c, z), the command letter
only where it changes, and numbers in their shortest form. Coordinates are rounded to `decimals`
before the relative steps are taken, so the error never accumulates along a path. By default
`decimals` is the most the drawing itself uses, so nothing is rounded away: MAAT (whole numbers)
renders pixel for pixel the same, the calçada tile (one decimal) differs only in anti-aliasing.
Rounding the calçada to whole numbers visibly moves its stones; do not. Whitespace between tags
goes too. Handles the commands the site's drawings use (M, L, H, V, C, Z, absolute or relative);
anything else is left as it is.
"""
import re

TOKEN = re.compile(r"[MmLlHhVvCcZz]|-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
ARGS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "Z": 0}


def num(x, decimals):
    """Shortest text for a number: 3, -0.5 as -.5, 0.25 as .25."""
    s = f"{round(x, decimals):.{decimals}f}" if decimals else str(int(round(x)))
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s.replace("0.", ".", 1) if s.startswith(("0.", "-0.")) else s


def emit(out, prev, cmd, values, decimals):
    """Append one command: its letter only when it changes, and a space between two numbers
    only where the second does not start with a minus sign (which already separates them)."""
    if cmd != prev or cmd == "m":
        out.append(cmd)
    for v in values:
        s = num(v, decimals)
        if out and out[-1][-1] not in "mlhvcz" and not s.startswith("-"):
            out.append(" ")
        out.append(s)


def path(d, decimals):
    tokens = TOKEN.findall(d)
    if not tokens or any(t.isalpha() and t.upper() not in ARGS for t in tokens):
        return d
    out, prev = [], None
    x = y = sx = sy = 0.0          # the current point and the subpath start, both rounded
    r = lambda v: round(v, decimals)
    i, cmd = 0, None
    while i < len(tokens):
        if tokens[i].isalpha():
            cmd = tokens[i]
            i += 1
            if cmd in "Zz":
                if prev != "z":
                    out.append("z")
                prev, x, y = "z", sx, sy
                continue
        n = ARGS[cmd.upper()]
        vals = [float(v) for v in tokens[i:i + n]]
        i += n
        rel = cmd.islower()
        up = cmd.upper()
        if up == "H":
            ax = r(vals[0] + (x if rel else 0))
            step, letter, x = [ax - x], "h", ax
        elif up == "V":
            ay = r(vals[0] + (y if rel else 0))
            step, letter, y = [ay - y], "v", ay
        else:
            pts = [(r(vals[k] + (x if rel else 0)), r(vals[k + 1] + (y if rel else 0))) for k in range(0, n, 2)]
            step = [c for px, py in pts for c in (px - x, py - y)]
            x, y = pts[-1]
            letter = up.lower()
            if up == "M":
                sx, sy = x, y
                cmd = "l" if rel else "L"      # coordinates after a moveto are linetos
            elif up == "L" and step[0] == 0:
                step, letter = [step[1]], "v"
            elif up == "L" and step[1] == 0:
                step, letter = [step[0]], "h"
        emit(out, prev, letter, step, decimals)
        prev = letter
    return "".join(out)


def minify(text, decimals=None):
    if decimals is None:
        found = [len(n) for d in re.findall(r'\sd="([^"]*)"', text) for n in re.findall(r"\.(\d+)", d)]
        decimals = max(found, default=0)
    text = re.sub(r'\sd="([^"]*)"', lambda m: f' d="{path(m.group(1), decimals)}"', text)
    return re.sub(r">\s+<", "><", text).strip() + "\n"
