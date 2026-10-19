"""A small Markdown reader for the insights, so articles can be written as plain text.

No dependencies. It reads the part of Markdown an article needs and fails loudly on anything else,
so a typo never reaches the page as stray symbols.

  A header block between two --- lines, one "key: value" per line (see content/insights/README.md).

  ## Heading                a section heading (### for a smaller one; # is the page title, so not allowed)
  A paragraph               lines that follow each other join into one paragraph; a blank line ends it
  > A quotation             a pull quote; several > lines join into one
  - An item                 a bulleted list (or "* An item"); "1. An item" for a numbered one
  ![Alt text](image.jpg)    an image on its own line, with its description in the brackets

  Inside a paragraph: **bold**, *italic*, [a link](/book), `code`.
"""
import html
import re


def front_matter(text):
    """Split a file into its header block (a dict) and its body."""
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise ValueError("the file must start with a header block between two --- lines")
    meta = {}
    for n, line in enumerate(m.group(1).splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"header line {n} has no colon: {line!r}")
        meta[key.strip()] = value.strip()
    return meta, m.group(2)


def inline(text):
    text = html.escape(text, quote=False)
    codes = []

    def keep(m):
        codes.append(f"<code>{m.group(1)}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2).replace(chr(34), "&quot;")}">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*(?=\S)(.+?)(?<=\S)\*(?![*\w])", r"<em>\1</em>", text)
    if "*" in text:
        raise ValueError(f"unmatched * in: {text[:80]}")
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def to_html(text, image=None):
    """The article body as HTML. image(src, alt) renders a body image; by default a plain <img>."""
    blocks, para, quote, items, kind = [], [], [], [], None

    def flush():
        nonlocal para, quote, items, kind
        if para:
            blocks.append(f"<p>{inline(' '.join(para))}</p>")
        if quote:
            blocks.append(f"<blockquote>{inline(' '.join(quote))}</blockquote>")
        if items:
            lis = "\n".join(f"  <li>{inline(i)}</li>" for i in items)
            blocks.append(f"<{kind}>\n{lis}\n</{kind}>")
        para, quote, items, kind = [], [], [], None

    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        bullet = re.match(r"([-*]|\d+\.)\s+(.*)", s)
        if not s:
            flush()
        elif s.startswith("#"):
            m = re.match(r"(#{2,3})\s+(.+)", s)
            if not m:
                raise ValueError(f"line {n}: headings start with ## or ### (the # title comes from the header block)")
            flush()
            level = len(m.group(1))
            blocks.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
        elif s.startswith(">"):
            if para or items:
                flush()
            quote.append(s[1:].strip())
        elif bullet and not para:
            k = "ol" if bullet.group(1)[0].isdigit() else "ul"
            if quote or (items and k != kind):
                flush()
            kind = k
            items.append(bullet.group(2))
        elif re.fullmatch(r"!\[([^\]]*)\]\(([^)\s]+)\)", s):
            flush()
            alt, src = re.fullmatch(r"!\[([^\]]*)\]\(([^)\s]+)\)", s).groups()
            blocks.append(image(src, alt) if image else f'<img src="{html.escape(src)}" alt="{html.escape(alt)}">')
        elif items and line[:1] in " \t":
            items[-1] += " " + s          # an indented line continues the list item above
        elif quote:
            quote.append(s)
        else:
            if items:
                flush()
            para.append(s)
    flush()
    return "\n\n".join(blocks)


def words(text):
    return len(re.findall(r"[A-Za-z0-9À-ɏ'’-]+", re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)))
