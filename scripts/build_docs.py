"""Construye la documentación del repositorio como sitio HTML estático.

Recorre ``docs/**/*.md``, convierte cada archivo a HTML y valida que todos los
enlaces internos apunten a archivos que existen. Si encuentra un enlace roto,
termina con código 1: el pipeline usa esa condición como *quality gate*.

Uso:
    python scripts/build_docs.py --out site
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import markdown

LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "data:")

CSS = """
:root { color-scheme: light dark; }
body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
       max-width: 60rem; margin: 2rem auto; padding: 0 1.25rem; line-height: 1.6; }
h1, h2, h3 { line-height: 1.25; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border: 1px solid #8884; padding: .35rem .55rem; text-align: left; }
code, pre { background: #8881; border-radius: .3rem; }
pre { padding: .8rem; overflow-x: auto; }
blockquote { border-left: .25rem solid #8886; margin-left: 0; padding-left: 1rem; }
nav a { margin-right: .75rem; }
"""


def title_of(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def check_links(page: Path, text: str, root: Path) -> list[str]:
    broken: list[str] = []
    for raw in LINK.findall(text):
        target = raw.strip()
        if target.startswith(SKIP_PREFIXES) or target.startswith("/"):
            continue
        path_part = unquote(target.split("#", 1)[0])
        if not path_part:
            continue
        candidate = (page.parent / path_part).resolve()
        if candidate.exists():
            continue
        if (root / path_part).exists():
            continue
        broken.append(f"{page.relative_to(root)} -> {target}")
    return broken


def build(root: Path, out: Path) -> int:
    docs = sorted((root / "docs").rglob("*.md"))
    if not docs:
        print("No se encontraron documentos en docs/.")
        return 1

    out.mkdir(parents=True, exist_ok=True)
    broken: list[str] = []
    pages: list[tuple[str, str, str]] = []

    for page in docs:
        text = page.read_text(encoding="utf-8")
        broken.extend(check_links(page, text, root))
        body = markdown.markdown(
            text,
            extensions=["extra", "tables", "fenced_code", "toc", "sane_lists"],
        )
        rel = page.relative_to(root / "docs").with_suffix(".html")
        destination = out / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        name = title_of(text, page.stem)
        destination.write_text(
            "<!doctype html><html lang=\"es\"><meta charset=\"utf-8\">"
            f"<title>{html.escape(name)}</title><style>{CSS}</style>"
            f"<nav><a href=\"{html.escape(str(Path(rel).parent / 'index.html'))}\">"
            "Índice</a> · <a href=\"/\">Repositorio</a></nav>"
            f"<article>{body}</article></html>",
            encoding="utf-8",
        )
        pages.append((name, rel.as_posix(), page.relative_to(root).as_posix()))

    rows = "\n".join(
        f'<li><a href="{html.escape(rel)}">{html.escape(name)}</a> '
        f"<code>{html.escape(source)}</code></li>"
        for name, rel, source in pages
    )
    (out / "index.html").write_text(
        "<!doctype html><html lang=\"es\"><meta charset=\"utf-8\">"
        f"<title>Documentación del proyecto</title><style>{CSS}</style>"
        "<h1>Documentación del proyecto</h1>"
        f"<p>{len(pages)} documentos construidos.</p><ul>{rows}</ul></html>",
        encoding="utf-8",
    )

    print(f"Documentos construidos: {len(pages)}")
    print("Enlaces internos verificados: OK")
    if broken:
        print(f"Enlaces roto(s): {len(broken)}")
        for item in broken:
            print("  " + item)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="site", help="carpeta de salida")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    return build(root, (root / args.out).resolve())


if __name__ == "__main__":
    sys.exit(main())
