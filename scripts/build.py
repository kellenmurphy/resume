#!/usr/bin/env python3
"""Render resume.yaml into LaTeX, HTML, and Markdown.

Outputs (written to build/ by default):
  resume.tex   -- compiled to resume.pdf by CI (xu-cheng/latex-action)
  resume.html  -- Jekyll page for kellenmurphy.com/resume.html
  resume.md    -- Jekyll page served at kellenmurphy.com/resume.md
"""

import argparse
import datetime
import pathlib
import re

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).resolve().parent.parent


def tex_escape(value: str) -> str:
    """Escape the characters that actually occur in resume prose.

    Content is plain prose: backslashes, braces, ~, ^, $, #, _ never appear,
    so only the ampersand and typographic punctuation need mapping.
    """
    replacements = [
        ("&", r"\&"),
        ("%", r"\%"),
        ("—", "---"),  # em dash
        ("–", "--"),  # en dash
        ("’", "'"),  # right single quote
    ]
    result = str(value)
    for char, escaped in replacements:
        result = result.replace(char, escaped)
    return result


def html_escape(value: str) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bare_url(value: str) -> str:
    return re.sub(r"^https?://(www\.)?", "", str(value))


def make_env(**delimiters) -> Environment:
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        **delimiters,
    )
    env.filters.update(tex=tex_escape, h=html_escape, bare=bare_url)
    return env


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        default=datetime.date.today().isoformat(),
        help="last_modified_at date for the HTML front matter (YYYY-MM-DD)",
    )
    parser.add_argument("--outdir", type=pathlib.Path, default=ROOT / "build")
    args = parser.parse_args()

    data = yaml.safe_load((ROOT / "resume.yaml").read_text(encoding="utf-8"))
    data["date"] = args.date

    # LaTeX templates use <% %> / << >> delimiters so Jinja never collides
    # with TeX's braces; HTML and Markdown use the defaults.
    tex_env = make_env(
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="<<",
        variable_end_string=">>",
        comment_start_string="<#",
        comment_end_string="#>",
    )
    default_env = make_env()

    args.outdir.mkdir(parents=True, exist_ok=True)
    outputs = [
        (tex_env, "resume.tex.j2", "resume.tex"),
        (default_env, "resume.html.j2", "resume.html"),
        (default_env, "resume.md.j2", "resume.md"),
    ]
    for env, template, filename in outputs:
        rendered = env.get_template(template).render(data)
        (args.outdir / filename).write_text(rendered, encoding="utf-8")
        print(f"wrote {args.outdir / filename}")


if __name__ == "__main__":
    main()
