#!/usr/bin/env python3
"""Sync whitelisted files from learning-warehouse into learningWarehouse-public/site/."""

from __future__ import annotations

import argparse
import html
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Missing dependency: PyYAML. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "publish.config.yaml"
DEFAULT_SITE = ROOT / "site"
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


@dataclass
class SyncEntry:
    source: str
    target: str
    mode: str


@dataclass
class NavItem:
    title: str
    href: str
    mode: str


def load_config(config_path: Path) -> tuple[Path, list[SyncEntry]]:
    with config_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    source_root = (config_path.parent / data.get("source_root", "..")).resolve()
    raw_entries = data.get("entries") or []
    entries: list[SyncEntry] = []

    for item in raw_entries:
        if not isinstance(item, dict):
            continue
        source = str(item.get("source", "")).strip()
        target = str(item.get("target", "")).strip()
        mode = str(item.get("mode", "copy")).strip().lower()
        if not source or not target:
            continue
        entries.append(SyncEntry(source=source, target=target, mode=mode))

    return source_root, entries


def reset_site_dir(site_dir: Path) -> None:
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def render_md_viewer(title: str) -> str:
    template_path = TEMPLATE_DIR / "md-viewer.html"
    content = template_path.read_text(encoding="utf-8")
    return content.replace("{{TITLE}}", html.escape(title, quote=True))


def sync_html(src: Path, site_dir: Path, entry: SyncEntry) -> NavItem:
    dst = site_dir / entry.target / "index.html"
    copy_file(src, dst)
    title = Path(entry.target).name
    href = f"{entry.target}/"
    return NavItem(title=title, href=href, mode=entry.mode)


def sync_image(src: Path, site_dir: Path, entry: SyncEntry) -> NavItem:
    dst = site_dir / entry.target
    copy_file(src, dst)
    title = Path(entry.target).name
    href = entry.target
    return NavItem(title=title, href=href, mode=entry.mode)


def sync_markdown(src: Path, site_dir: Path, entry: SyncEntry) -> NavItem:
    target_dir = site_dir / entry.target
    target_dir.mkdir(parents=True, exist_ok=True)
    copy_file(src, target_dir / "content.md")
    title = Path(entry.target).name
    viewer = render_md_viewer(title)
    (target_dir / "index.html").write_text(viewer, encoding="utf-8")
    href = f"{entry.target}/"
    return NavItem(title=title, href=href, mode=entry.mode)


def sync_copy(src: Path, site_dir: Path, entry: SyncEntry) -> NavItem:
    dst = site_dir / entry.target
    copy_file(src, dst)
    title = Path(entry.target).name
    href = entry.target
    return NavItem(title=title, href=href, mode=entry.mode)


def sync_entry(source_root: Path, site_dir: Path, entry: SyncEntry) -> NavItem:
    src = source_root / entry.source
    if not src.is_file():
        raise FileNotFoundError(f"Source not found: {entry.source}")

    mode = entry.mode
    if mode == "html":
        return sync_html(src, site_dir, entry)
    if mode == "image":
        return sync_image(src, site_dir, entry)
    if mode == "markdown":
        return sync_markdown(src, site_dir, entry)
    if mode == "copy":
        return sync_copy(src, site_dir, entry)
    raise ValueError(f"Unsupported mode '{entry.mode}' for source: {entry.source}")


def build_nav_tree(items: list[NavItem]) -> dict[str, Any]:
    tree: dict[str, Any] = {}
    for item in items:
        parts = [p for p in item.href.replace("\\", "/").split("/") if p]
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        leaf_name = parts[-1] if parts else item.title
        node[leaf_name] = {"__item__": item}
    return tree


def render_nav_html(tree: dict[str, Any], prefix: str = "") -> str:
    parts: list[str] = ["<ul>"]
    for name in sorted(tree.keys(), key=str.lower):
        value = tree[name]
        if isinstance(value, dict) and "__item__" in value and len(value) == 1:
            item: NavItem = value["__item__"]
            href = prefix + item.href
            mode_label = html.escape(item.mode)
            title = html.escape(item.title)
            parts.append(
                f'<li><a href="{html.escape(href, quote=True)}">{title}</a>'
                f' <span class="mode">({mode_label})</span></li>'
            )
        elif isinstance(value, dict):
            parts.append(f"<li><span class=\"dir\">{html.escape(name)}</span>")
            parts.append(render_nav_html(value, prefix))
            parts.append("</li>")
    parts.append("</ul>")
    return "".join(parts)


def generate_index(site_dir: Path, nav_items: list[NavItem]) -> None:
    tree = build_nav_tree(nav_items)
    nav_html = render_nav_html(tree)
    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>learningWarehouse-public</title>
  <style>
    body {{
      font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.6;
      color: #1f2937;
      max-width: 960px;
      margin: 0 auto;
      padding: 32px 24px 64px;
    }}
    h1 {{ margin-bottom: 0.25em; }}
    .subtitle {{ color: #6b7280; margin-bottom: 1.5em; }}
    ul {{ list-style: none; padding-left: 0; }}
    ul ul {{ padding-left: 1.25em; margin-top: 0.35em; }}
    li {{ margin: 0.35em 0; }}
    a {{ color: #2563eb; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .dir {{ font-weight: 600; color: #374151; }}
    .mode {{ color: #9ca3af; font-size: 0.85em; }}
  </style>
</head>
<body>
  <h1>learningWarehouse-public</h1>
  <p class="subtitle">公开学习笔记目录 · 共 {len(nav_items)} 项</p>
  {nav_html}
</body>
</html>
"""
    (site_dir / "index.html").write_text(page, encoding="utf-8")


def run_sync(config_path: Path, site_dir: Path, strict: bool) -> int:
    source_root, entries = load_config(config_path)
    if not entries:
        print("No entries found in publish.config.yaml")
        return 1

    print(f"Config: {config_path}")
    print(f"Source root: {source_root}")
    print(f"Site output: {site_dir}")
    print(f"Entries: {len(entries)}")
    print()

    reset_site_dir(site_dir)

    nav_items: list[NavItem] = []
    ok = 0
    failed: list[str] = []

    for entry in entries:
        try:
            item = sync_entry(source_root, site_dir, entry)
            nav_items.append(item)
            ok += 1
            print(f"  OK  [{entry.mode}] {entry.source}")
        except Exception as exc:
            msg = f"  FAIL [{entry.mode}] {entry.source} -> {exc}"
            print(msg)
            failed.append(msg)
            if strict:
                return 1

    generate_index(site_dir, nav_items)

    print()
    print(f"Done: {ok} succeeded, {len(failed)} failed")
    if failed:
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync public content into site/")
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to publish.config.yaml",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_SITE,
        help="Output site directory",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error if any entry fails",
    )
    args = parser.parse_args()

    config_path = args.config.resolve()
    if not config_path.is_file():
        print(f"Config not found: {config_path}", file=sys.stderr)
        return 1

    return run_sync(config_path, args.output.resolve(), args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
