#!/usr/bin/env python3
"""Regenerate legacy-site/llms-full.txt from the old site's pages.

The old site lives in legacy-site/ as a reference copy; site v5 writes its own
llms-full.txt (tools/build_site_v5.py --prod). Run:  python3 tools/build_llms_full.py
"""
import datetime
import html
import os
import re

os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "legacy-site"))

PAGES = [
    ("index.html", "Home", "https://solvenadvisory.ai/"),
    ("programmes.html", "Programmes", "https://solvenadvisory.ai/programmes"),
    ("approach.html", "Approach", "https://solvenadvisory.ai/approach"),
    ("work.html", "Work", "https://solvenadvisory.ai/work"),
    ("about.html", "About", "https://solvenadvisory.ai/about"),
    ("contact.html", "Contact", "https://solvenadvisory.ai/contact"),
    ("privacy.html", "Privacy", "https://solvenadvisory.ai/privacy"),
    ("pt/index.html", "Português", "https://solvenadvisory.ai/pt"),
    ("pt/programas.html", "Português: Programas", "https://solvenadvisory.ai/pt/programas"),
    ("pt/abordagem.html", "Português: Abordagem", "https://solvenadvisory.ai/pt/abordagem"),
    ("pt/trabalho.html", "Português: Trabalho", "https://solvenadvisory.ai/pt/trabalho"),
    ("pt/sobre.html", "Português: Sobre", "https://solvenadvisory.ai/pt/sobre"),
    ("pt/contacto.html", "Português: Contacto", "https://solvenadvisory.ai/pt/contacto"),
    ("ai-flix.html", "AI Flix", "https://solvenadvisory.ai/ai-flix"),
    ("blog/index.html", "Journal", "https://solvenadvisory.ai/blog"),
    ("blog/editors-of-drafts-they-cannot-defend.html",
     "Journal: Editors of drafts they cannot defend",
     "https://solvenadvisory.ai/blog/editors-of-drafts-they-cannot-defend"),
    ("blog/how-to-tell-whether-the-ai-is-real.html",
     "Journal: How to tell whether the AI is real",
     "https://solvenadvisory.ai/blog/how-to-tell-whether-the-ai-is-real"),
    ("blog/making-every-token-earn-its-place.html",
     "Journal: Making every token earn its place",
     "https://solvenadvisory.ai/blog/making-every-token-earn-its-place"),
]

PREFIX = {"h1": "## ", "h2": "### ", "h3": "#### ", "li": "- ",
          "blockquote": "> ", "summary": "**Q: ", "p": ""}


def page_text(fname):
    with open(fname, encoding="utf-8") as f:
        src = f.read()
    main = src[src.index('<main id="main">'):src.index("</main>")]
    main = re.sub(r"<script.*?</script>", "", main, flags=re.S)
    main = re.sub(r"<svg.*?</svg>", "", main, flags=re.S)
    main = re.sub(r'<[^>]*class="vh"[^>]*>.*?</[a-z]+>', "", main, flags=re.S)
    out = []
    for m in re.finditer(r"<(h1|h2|h3|p|li|summary|blockquote)\b[^>]*>(.*?)</\1>",
                         main, flags=re.S):
        tag, inner = m.group(1), m.group(2)
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", inner))).strip()
        if not text:
            continue
        out.append(PREFIX[tag] + text + ("**" if tag == "summary" else ""))
    return "\n\n".join(out)


def main():
    today = datetime.date.today().isoformat()
    parts = [
        "# Solven Advisory: full site text",
        "",
        "This file is the complete text of https://solvenadvisory.ai for AI systems "
        "and their users. A shorter index lives at /llms.txt. Generated from the "
        f"live pages on {today}.",
        "",
    ]
    for fname, title, url in PAGES:
        parts.append(f"\n---\n\n# {title}\n\n<{url}>\n")
        parts.append(page_text(fname))
    full = "\n".join(parts) + "\n"
    assert "—" not in full, "em dash found; fix the source page first"
    with open("llms-full.txt", "w", encoding="utf-8") as f:
        f.write(full)
    print(f"llms-full.txt: {len(full)} chars from {len(PAGES)} pages")


if __name__ == "__main__":
    main()
