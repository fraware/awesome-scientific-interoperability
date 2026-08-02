#!/usr/bin/env python3
"""Build the read-only GitHub Pages explorer from catalog exports and docs.

The site is a projection of the structured catalog and manually authored docs.
It never decides inclusion and never rewrites README.md.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from export_catalog import export_all  # noqa: E402

SITE_SRC = ROOT / "site"
ASSETS_SRC = SITE_SRC / "assets"
DEFAULT_OUT = SITE_SRC / "dist"
REPO_URL = "https://github.com/fraware/awesome-scientific-interoperability"
README_URL = f"{REPO_URL}/blob/main/README.md"

NAV = [
    ("Problems", "problems/index.html"),
    ("Guides", "guides/index.html"),
    ("Explore", "explore/index.html"),
    ("Compare", "compare/index.html"),
    ("Graph", "graph/index.html"),
    ("Downloads", "downloads/index.html"),
    ("About", "about/index.html"),
]

RESOURCE_MARKER_RE = re.compile(r"\[resource:([a-z0-9-]+)\]")
PROBLEM_LINE_RE = re.compile(r"^\[problem:([a-z0-9-]+)\]\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.MULTILINE)


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def load_json(path: Path) -> dict[str, Any]:
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def asset_prefix(depth: int) -> str:
    return "../" * depth if depth else "./"


def page_shell(
    *,
    title: str,
    body: str,
    depth: int,
    current: str | None,
    extra_head: str = "",
    include_app_js: bool = False,
) -> str:
    prefix = asset_prefix(depth)
    nav_items = []
    for label, href in NAV:
        current_attr = ' aria-current="page"' if current == label else ""
        nav_items.append(f'<a href="{prefix}{href}"{current_attr}>{esc(label)}</a>')
    app_js = f'<script src="{prefix}assets/app.js" defer></script>' if include_app_js else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} · Awesome Scientific Interoperability</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,550;9..144,700&family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/styles.css">
  {extra_head}
</head>
<body>
  <header class="site-header">
    <a class="brand" href="{prefix}index.html">Awesome Scientific Interoperability</a>
    <nav class="nav">{"".join(nav_items)}</nav>
  </header>
  <main>
    {body}
  </main>
  <footer class="site-footer">
    Read-only decision interface. The
    <a href="{README_URL}">manually curated README</a>
    remains authoritative for inclusion. Catalog dumps never auto-generate the list.
  </footer>
  {app_js}
</body>
</html>
"""


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def linkify_resources(text: str, *, depth: int) -> str:
    prefix = asset_prefix(depth)

    def repl(match: re.Match[str]) -> str:
        resource_id = match.group(1)
        return (
            f'<a class="mono" href="{prefix}resource/{esc(resource_id)}.html">'
            f"{esc(resource_id)}</a>"
        )

    return RESOURCE_MARKER_RE.sub(repl, esc(text)).replace("\n", "<br>\n")


def parse_problem_sections(doc: str) -> list[dict[str, str]]:
    matches = list(PROBLEM_LINE_RE.finditer(doc))
    headings = list(HEADING_RE.finditer(doc))
    problems: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(doc)
        block = doc[start:end].strip()
        title = match.group(1)
        for heading in headings:
            if heading.start() < match.start():
                title = heading.group(2).strip()
            else:
                break
        problems.append({"id": match.group(1), "title": title, "body": block})
    return problems


def simple_markdown(text: str, *, depth: int) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_ul = False
    in_table = False
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if in_table:
                out.append("</tbody></table>")
                in_table = False
            continue
        if set(line.strip()) <= {"|", "-", ":", " "} and "|" in line:
            continue
        if line.startswith("|") and "|" in line[1:]:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if not in_table:
                out.append("<table><tbody>")
                in_table = True
                out.append("<tr>" + "".join(f"<th>{linkify_resources(cell, depth=depth)}</th>" for cell in cells) + "</tr>")
            else:
                out.append("<tr>" + "".join(f"<td>{linkify_resources(cell, depth=depth)}</td>" for cell in cells) + "</tr>")
            continue
        if in_table:
            out.append("</tbody></table>")
            in_table = False
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            level = len(heading.group(1))
            out.append(f"<h{level}>{linkify_resources(heading.group(2), depth=depth)}</h{level}>")
            continue
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{linkify_resources(line[2:], depth=depth)}</li>")
            continue
        if in_ul:
            out.append("</ul>")
            in_ul = False
        out.append(f"<p>{linkify_resources(line, depth=depth)}</p>")
    if in_ul:
        out.append("</ul>")
    if in_table:
        out.append("</tbody></table>")
    return "\n".join(out)


def build_home(out_dir: Path) -> None:
    body = f"""
    <section class="hero">
      <h1>Awesome Scientific Interoperability</h1>
      <p>Find the strongest public interoperability mechanism for a concrete scientific integration problem—without starting a new landscape search.</p>
      <div class="cta-row">
        <a class="button" href="problems/index.html">Start from a problem</a>
        <a class="button-secondary" href="{README_URL}">Browse the Awesome list</a>
        <a class="button-secondary" href="downloads/index.html">Download data</a>
      </div>
    </section>
    """
    write_page(out_dir / "index.html", page_shell(title="Home", body=body, depth=0, current=None))


def build_problems(out_dir: Path, problems_index: dict[str, Any]) -> None:
    doc = (ROOT / "docs" / "integration-problems.md").read_text(encoding="utf-8")
    sections = {item["id"]: item for item in parse_problem_sections(doc)}
    cards = []
    for item in problems_index["problems"]:
        title = sections.get(item["id"], {}).get("title") or item["title"]
        cards.append(
            f'<a class="item-link" href="{esc(item["id"])}.html"><h3>{esc(title)}</h3>'
            f'<p class="mono">{esc(item["id"])}</p></a>'
        )
        body_md = sections.get(item["id"], {}).get("body", "")
        detail = f"""
        <h1 class="section-title">{esc(title)}</h1>
        <p class="lede mono">problem:{esc(item["id"])}</p>
        <div class="panel">{simple_markdown(body_md, depth=1)}</div>
        <p class="meta">Referenced resources:
        {" ".join(f'<a class="pill" href="../resource/{esc(rid)}.html">{esc(rid)}</a>' for rid in item["resource_ids"])}
        </p>
        """
        write_page(
            out_dir / "problems" / f"{item['id']}.html",
            page_shell(title=title, body=detail, depth=1, current="Problems"),
        )
    index_body = f"""
    <h1 class="section-title">Integration problems</h1>
    <p class="lede">Start from a concrete situation. Recommendations cite catalog boundary notes; no entry is a universal winner.</p>
    <div class="grid problems">{"".join(cards)}</div>
    """
    write_page(
        out_dir / "problems" / "index.html",
        page_shell(title="Problems", body=index_body, depth=1, current="Problems"),
    )


def build_guides(out_dir: Path, guides_index: dict[str, Any]) -> None:
    cards = []
    for guide in guides_index["guides"]:
        path = ROOT / guide["path"]
        text = path.read_text(encoding="utf-8") if path.is_file() else guide["title"]
        cards.append(
            f'<a class="item-link" href="{esc(guide["id"])}.html"><h3>{esc(guide["title"])}</h3>'
            f'<p>{esc(guide.get("scope") or "")}</p></a>'
        )
        detail = f"""
        <h1 class="section-title">{esc(guide["title"])}</h1>
        <p class="lede">{esc(guide.get("scope") or "")}</p>
        <p class="notice">Canonical markdown remains in the repository. This page is a read-only rendering for browser navigation.</p>
        <div class="panel">{simple_markdown(text, depth=1)}</div>
        """
        write_page(
            out_dir / "guides" / f"{guide['id']}.html",
            page_shell(title=guide["title"], body=detail, depth=1, current="Guides"),
        )
    index_body = f"""
    <h1 class="section-title">Decision guides</h1>
    <p class="lede">Side-by-side comparisons for overlapping mechanisms. Use them after you know the integration concern.</p>
    <div class="grid guides">{"".join(cards)}</div>
    """
    write_page(
        out_dir / "guides" / "index.html",
        page_shell(title="Guides", body=index_body, depth=1, current="Guides"),
    )


def build_resources(out_dir: Path, catalog: dict[str, Any], guides_index: dict[str, Any], problems_index: dict[str, Any]) -> None:
    guide_hits: dict[str, list[str]] = {}
    for guide in guides_index["guides"]:
        for rid in guide["resource_ids"]:
            guide_hits.setdefault(rid, []).append(guide["id"])
    problem_hits: dict[str, list[str]] = {}
    for problem in problems_index["problems"]:
        for rid in problem["resource_ids"]:
            problem_hits.setdefault(rid, []).append(problem["id"])

    for resource in catalog["resources"]:
        rid = resource["id"]
        relations = resource.get("relations") or []
        impls = resource.get("implementations") or []
        steward = resource.get("steward") or {}
        pills = "".join(f'<span class="pill">{esc(item)}</span>' for item in resource.get("evidence_types") or [])
        rel_rows = "".join(
            f"<tr><td class=\"mono\">{esc(item['type'])}</td>"
            f"<td><a href=\"{esc(item['resource_id'])}.html\">{esc(item['resource_id'])}</a></td></tr>"
            for item in relations
        ) or "<tr><td colspan='2'>No typed relations recorded.</td></tr>"
        impl_rows = "".join(
            f"<tr><td>{esc(item['name'])}</td><td class=\"mono\">{esc(item['relationship'])}</td>"
            f"<td><a href=\"{esc(item['url'])}\">{esc(item['url'])}</a></td></tr>"
            for item in impls
        ) or "<tr><td colspan='3'>No implementation records joined.</td></tr>"
        related_guides = "".join(
            f'<a class="pill" href="../guides/{esc(gid)}.html">{esc(gid)}</a>' for gid in guide_hits.get(rid, [])
        ) or "<span class=\"meta\">None indexed</span>"
        related_problems = "".join(
            f'<a class="pill" href="../problems/{esc(pid)}.html">{esc(pid)}</a>' for pid in problem_hits.get(rid, [])
        ) or "<span class=\"meta\">None indexed</span>"
        body = f"""
        <h1 class="section-title">{esc(resource["name"])}</h1>
        <p class="lede">{esc(resource["summary"])}</p>
        <p class="pill-row">{pills}<span class="pill">{esc(resource.get("review_type") or "unreviewed")}</span></p>
        <div class="panel">
          <p><strong>Mechanism:</strong> {esc(resource["mechanism"])}</p>
          <p><strong>Section:</strong> {esc(resource["section"])} · <strong>Kind:</strong> {esc(resource["resource_kind"])}</p>
          <p><strong>Primary URL:</strong> <a href="{esc(resource["url"])}">{esc(resource["url"])}</a></p>
          <p><strong>Steward:</strong> {esc(steward.get("name") or resource.get("steward_id") or "n/a")}
          ({esc(steward.get("type") or "unknown")})</p>
          <p><strong>Boundary note:</strong> {esc(resource.get("boundary_note") or "")}</p>
        </div>
        <h2>Typed relations</h2>
        <table><thead><tr><th>Type</th><th>Target</th></tr></thead><tbody>{rel_rows}</tbody></table>
        <h2>Implementations</h2>
        <table><thead><tr><th>Name</th><th>Relationship</th><th>URL</th></tr></thead><tbody>{impl_rows}</tbody></table>
        <h2>Decision paths</h2>
        <p>Guides: {related_guides}</p>
        <p>Problems: {related_problems}</p>
        """
        write_page(
            out_dir / "resource" / f"{rid}.html",
            page_shell(title=resource["name"], body=body, depth=1, current="Explore"),
        )


def build_explore(out_dir: Path) -> None:
    body = """
    <h1 class="section-title">Explore the catalog</h1>
    <p class="lede">Filter the structured catalog. Inclusion decisions stay in the manually curated README.</p>
    <div class="filters panel">
      <label>Search<input id="filter-query" type="search" placeholder="Name, id, mechanism…"></label>
      <label>Section<select id="filter-section"></select></label>
      <label>Layer<select id="filter-layer"></select></label>
      <label>Evidence<select id="filter-evidence"></select></label>
      <label>Resource kind<select id="filter-kind"></select></label>
      <label>Review type<select id="filter-review"></select></label>
    </div>
    <p id="result-count" class="meta">Loading…</p>
    <div class="panel" style="overflow-x:auto">
      <table>
        <thead>
          <tr><th>Resource</th><th>Section</th><th>Layers</th><th>Evidence</th><th>Review</th></tr>
        </thead>
        <tbody id="explore-body"></tbody>
      </table>
    </div>
    """
    write_page(
        out_dir / "explore" / "index.html",
        page_shell(title="Explore", body=body, depth=1, current="Explore", include_app_js=True),
    )


def build_compare(out_dir: Path) -> None:
    links = [
        ("Research object packaging", "research-object-packaging", "RO-Crate, BagIt, OCFL, Data Package, COMBINE/OMEX"),
        ("Neuroscience datasets", "neuroscience-data-standards", "BIDS, NWB, and related neurophysiology exchange"),
        ("Computational neuroscience models", "computational-neuroscience-model-exchange", "NeuroML, SONATA, and boundaries"),
        ("Astronomy / VO family", "astronomy-data-and-services", "FITS, ASDF, VOTable, TAP, ObsCore"),
        ("Repository preservation packaging", "repository-preservation-and-data-packaging", "OCFL vs BagIt vs RO-Crate vs Data Package"),
    ]
    cards = "".join(
        f'<a class="item-link" href="../guides/{esc(slug)}.html"><h3>{esc(title)}</h3><p>{esc(blurb)}</p></a>'
        for title, slug, blurb in links
    )
    body = f"""
    <h1 class="section-title">Compare</h1>
    <p class="lede">Curated deep-links into the decision guides that answer the most common “which standard?” questions.</p>
    <div class="grid guides">{cards}</div>
    <p class="notice">For typed relation neighborhoods, open the <a href="../graph/index.html">Graph</a> view.</p>
    """
    write_page(
        out_dir / "compare" / "index.html",
        page_shell(title="Compare", body=body, depth=1, current="Compare"),
    )


def build_graph(out_dir: Path) -> None:
    body = """
    <h1 class="section-title">Relation neighborhood</h1>
    <p class="lede">Inspect typed catalog relations around one resource. This is intentionally not a hairball of the full corpus.</p>
    <div class="graph-controls panel">
      <label style="min-width:16rem">Resource<select id="graph-root"></select></label>
      <p id="graph-meta" class="meta">Loading…</p>
    </div>
    <canvas id="graph-canvas" width="960" height="560" aria-label="Relation neighborhood graph"></canvas>
    """
    write_page(
        out_dir / "graph" / "index.html",
        page_shell(title="Graph", body=body, depth=1, current="Graph", include_app_js=True),
    )


def build_downloads(out_dir: Path) -> None:
    artifacts = [
        ("catalog.json", "Joined resources with steward and implementation summaries"),
        ("catalog.csv", "Flat table for spreadsheets"),
        ("relations.json", "Typed edge list"),
        ("catalog.jsonld", "Minimal JSON-LD projection"),
        ("problems.json", "Integration-problem navigation index"),
        ("guides-index.json", "Decision-guide navigation index"),
    ]
    rows = "".join(
        f'<tr><td><a href="../data/{esc(name)}">{esc(name)}</a></td><td>{esc(desc)}</td></tr>'
        for name, desc in artifacts
    )
    body = f"""
    <h1 class="section-title">Downloads</h1>
    <p class="lede">Machine-readable projections of the structured catalog. They do not decide inclusion.</p>
    <div class="panel">
      <table>
        <thead><tr><th>Artifact</th><th>Purpose</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p class="meta">Also published as the <code>catalog-exports</code> GitHub Actions artifact and as GitHub Release assets on tagged releases.</p>
    """
    write_page(
        out_dir / "downloads" / "index.html",
        page_shell(title="Downloads", body=body, depth=1, current="Downloads"),
    )


def build_about(out_dir: Path) -> None:
    body = f"""
    <h1 class="section-title">About this explorer</h1>
    <p class="lede">A browser projection of the Awesome Scientific Interoperability knowledge system.</p>
    <div class="panel">
      <p><strong>North Star:</strong> a technically competent user can identify the strongest available interoperability mechanism for a concrete scientific integration problem without conducting a new landscape search.</p>
      <p><strong>Canonical list:</strong> the <a href="{README_URL}">README on GitHub</a> is manually authored and authoritative for inclusion.</p>
      <p><strong>Governance limitation:</strong> until named domain section reviewers accept CODEOWNERS responsibility, this project remains under a single-maintainer limitation. See <a href="{REPO_URL}/blob/main/docs/governance.md">governance</a>.</p>
      <p><strong>Corrections:</strong> use repository issue forms to propose corrections or challenge evidence and guide recommendations.</p>
      <p><strong>Conflicts of interest:</strong> affiliated contributors do not sole-approve their own resources.</p>
    </div>
    """
    write_page(
        out_dir / "about" / "index.html",
        page_shell(title="About", body=body, depth=1, current="About"),
    )


def build_site(out_dir: Path, *, generated_on: str | None = None) -> None:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    data_dir = out_dir / "data"
    export_all(data_dir, generated_on=generated_on)
    assets_out = out_dir / "assets"
    shutil.copytree(ASSETS_SRC, assets_out)

    catalog = load_json(data_dir / "catalog.json")
    problems = load_json(data_dir / "problems.json")
    guides = load_json(data_dir / "guides-index.json")

    build_home(out_dir)
    build_problems(out_dir, problems)
    build_guides(out_dir, guides)
    build_resources(out_dir, catalog, guides, problems)
    build_explore(out_dir)
    build_compare(out_dir)
    build_graph(out_dir)
    build_downloads(out_dir)
    build_about(out_dir)

    # GitHub Pages project sites serve under /<repo>/; keep relative links only.
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--generated-on", help="Pin export_generated_on for deterministic builds")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    build_site(args.out_dir, generated_on=args.generated_on)
    print(f"Built site into {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
