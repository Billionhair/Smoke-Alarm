"""Report generation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

try:  # optional dependency
    from docxtpl import DocxTemplate
except Exception:  # pragma: no cover
    DocxTemplate = None  # type: ignore


def _env(template_dir: str) -> Environment:
    return Environment(loader=FileSystemLoader(template_dir))


def render_pdf(template_path: str, context: Dict, out_pdf: str) -> None:
    template_dir = str(Path(template_path).parent)
    env = _env(template_dir)
    tpl = env.get_template(Path(template_path).name)
    html = tpl.render(**context)
    HTML(string=html, base_url=template_dir).write_pdf(out_pdf)


def render_docx(template_path: str, context: Dict, out_docx: str) -> None:
    if not DocxTemplate:
        raise RuntimeError("docxtpl is not installed")
    tpl = DocxTemplate(template_path)
    tpl.render(context)
    tpl.save(out_docx)
