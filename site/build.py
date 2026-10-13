#!/usr/bin/env python3
"""Generate the ZeroMatrixTech website into docs/ from site/content.json.

Usage:  python3 site/build.py          build all pages, then check links
        python3 site/build.py --check  only check links in docs/

Only the Python standard library is used. Pages are written to docs/ (Chinese)
and docs/en/ (English). Files this script does not own (CNAME, demos/, images,
site.css, site.js) are never touched.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
C = json.loads((ROOT / "site" / "content.json").read_text(encoding="utf-8"))
LANGS = ("zh", "en")
PAGES = ("index.html", "services.html", "projects.html", "about.html", "contact.html")


def esc(s):
    return html.escape(str(s), quote=True)


def tr(obj, lang):
    """Pick the language from a {"zh":..,"en":..} object; plain values pass through."""
    return obj[lang] if isinstance(obj, dict) and lang in obj else obj


def T(obj, lang):
    return esc(tr(obj, lang))


class Ctx:
    def __init__(self, lang, file):
        self.lang, self.file = lang, file
        self.up = "../" if lang == "en" else ""          # path back to docs/

    def page(self, f):                                   # page in the same language
        return f

    def res(self, p):                                    # shared resource under docs/
        return self.up + p

    def other(self):                                     # the same page in the other language
        return ("en/" + self.file) if self.lang == "zh" else ("../" + self.file)

    def url(self, lang=None):
        lang = lang or self.lang
        base = C["site"]["url"] + ("en/" if lang == "en" else "")
        return base + ("" if self.file == "index.html" else self.file)


ICONS = {
    "device": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    "server": '<rect x="4" y="3" width="16" height="7" rx="1.5"/><rect x="4" y="14" width="16" height="7" rx="1.5"/><path d="M8 6.5h.01M8 17.5h.01"/>',
    "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    "flask": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3"/><path d="M7.5 14h9"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "theme": '<circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def icon(name, size=20):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def mark():
    return '<span class="mark" aria-hidden="true">' + "<i></i>" * 9 + "</span>"


# ---------------------------------------------------------------- frame
def head(cx, title, desc):
    alt = "".join(f'<link rel="alternate" hreflang="{"zh-CN" if l == "zh" else "en"}" href="{cx.url(l)}">' for l in LANGS)
    return f"""<!doctype html>
<html lang="{'zh-CN' if cx.lang == 'zh' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{cx.url()}">
{alt}<link rel="alternate" hreflang="x-default" href="{cx.url('zh')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ZeroMatrixTech">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{cx.url()}">
<meta property="og:image" content="{C['site']['url']}assets/og.png">
<link rel="icon" href="{cx.res('assets/favicon.svg')}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@700;900&display=swap">
<link rel="stylesheet" href="{cx.res('assets/site.css')}">
<script>try{{var t=localStorage.getItem("zmt-theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
"""


def header(cx, current):
    ui = C["ui"]
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{cx.page(n["file"])}"{cur if n["id"] == current else ""}>{T(n, cx.lang)}</a>'
        for n in ui["nav"])
    other = "en" if cx.lang == "zh" else "zh-CN"
    return f"""<body>
<a class="skip" href="#main">{T(ui['skip'], cx.lang)}</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="{cx.page('index.html')}">{mark()}ZeroMatrixTech</a>
    <button class="menu" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">{icon('menu', 18)}</button>
    <nav class="nav" id="nav" aria-label="{'主导航' if cx.lang == 'zh' else 'Main'}">{links}</nav>
    <div class="tools">
      <a class="lang" href="{cx.other()}" hreflang="{other}" lang="{other}" title="{T(ui['lang_switch_label'], cx.lang)}">{T(ui['lang_switch'], cx.lang)}</a>
      <button class="theme" type="button" aria-label="{T(ui['theme'], cx.lang)}">{icon('theme', 16)}</button>
    </div>
  </div>
</header>
<main id="main">
"""


def cta(cx, h, text):
    ui, s = C["ui"], C["site"]
    return f"""<section><div class="wrap"><div class="cta">
  <div><h2>{T(h, cx.lang)}</h2><p>{T(text, cx.lang)}</p></div>
  <div class="row"><a class="btn" href="mailto:{s['email']}">{T(ui['email_us'], cx.lang)}</a><a class="btn ghost" href="{cx.page('contact.html')}">{esc(tr(C['ui']['nav'][4], cx.lang))} →</a></div>
</div></div></section>
"""


def footer(cx):
    ui, s, l = C["ui"], C["site"], cx.lang
    nav = "".join(f'<li><a href="{cx.page(n["file"])}">{T(n, l)}</a></li>' for n in ui["nav"])
    return f"""</main>
<footer>
  <div class="wrap">
    <div>
      <div class="brand">{mark()}ZeroMatrixTech</div>
      <p style="margin:0">{T(s['tagline'], l)}</p>
      <p style="margin:6px 0 0">{T(s['company'], l)}</p>
    </div>
    <div><h4>{T(ui['footer_sitemap'], l)}</h4><ul>{nav}</ul></div>
    <div><h4>{T(ui['footer_contact'], l)}</h4><ul><li><a href="mailto:{s['email']}">{esc(s['email'])}</a></li><li>{T(s['address'], l)}</li></ul></div>
    <div><h4>{T(ui['footer_open'], l)}</h4><ul><li><a href="{s['github']}" rel="noopener">{T(ui['footer_profile'], l)} ↗</a></li><li><a href="{s['repos']}" rel="noopener">{T(ui['footer_repos'], l)} ↗</a></li></ul></div>
    <div class="legal"><p>{T(s['ai_note'], l)}</p><p>© 2026 {T(s['company'], l)} · ZeroMatrixTech</p></div>
  </div>
</footer>
<script src="{cx.res('assets/site.js')}"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- components
def media(cx, p, link=True):
    href = cx.res(p["demo"]["href"]) if p.get("demo") else p.get("repo")
    if p.get("image"):
        inner = f'<img src="{cx.res(p["image"])}" alt="{T(p["image_alt"], cx.lang)}" loading="lazy" width="960" height="540">'
    else:
        lines = "".join(f'<div><span class="p">$ </span>{esc(c)}</div>' for c in p.get("terminal", []))
        inner = f'<div class="term" aria-hidden="true">{lines}<div><span class="p">$ </span><span class="c"></span></div></div>'
    play = f'<span class="play">▶ {T(C["ui"]["demo"], cx.lang)}</span>' if p.get("demo") else ""
    if link and href:
        ext = "" if href.startswith(("demos", "../")) else ' rel="noopener"'
        return f'<a class="media" href="{href}"{ext} aria-label="{esc(p["name"])}">{inner}{play}</a>'
    return f'<div class="media">{inner}{play}</div>'


def project_card(cx, p, compact=False):
    l, ui = cx.lang, C["ui"]
    cat = T(C["categories"][p["category"]], l)
    status = f'<span class="status tone-{p["status"]["tone"]}">{T(p["status"], l)}</span>'
    if compact:
        return f"""<article class="card" data-cat="{p['category']}">{media(cx, p)}
  <div class="body"><div class="meta"><span class="cat">{cat}</span>{status}</div><h3>{esc(p['name'])}</h3><p class="sum">{T(p['summary'], l)}</p></div>
</article>"""
    acts = []
    if p.get("repo"):
        acts.append(f'<a class="btn primary" href="{p["repo"]}" rel="noopener">{T(ui["repo"], l)} ↗</a>')
    else:
        acts.append(f'<span class="btn off">{T(p["repo_note"], l)}</span>')
    if p.get("demo"):
        acts.append(f'<a class="btn demo" href="{cx.res(p["demo"]["href"])}">▶ {T(p["demo"]["label"], l)}</a>')
    acts += [f'<a class="btn" href="{x["href"]}" rel="noopener">{T(x, l)} ↗</a>' for x in p.get("links", [])]
    tags = "".join(f"<li>{esc(t)}</li>" for t in tr(p["tags"], l))
    note = f'<p class="note">{T(p["note"], l)}</p>' if p.get("note") else ""
    return f"""<article class="card" data-cat="{p['category']}" id="{p['id']}">{media(cx, p)}
  <div class="body">
    <div class="meta"><span class="cat">{cat}</span>{status}<span class="lic">{T(p['license'], l)}</span></div>
    <h3>{esc(p['name'])}</h3>
    <p class="sum">{T(p['summary'], l)}</p>
    <ul class="tags">{tags}</ul>{note}
    <div class="actions">{''.join(acts)}</div>
  </div>
</article>"""


def steps(cx):
    items = "".join(f"<li><b>{esc(tr(s, cx.lang)[0])}</b><span>{esc(tr(s, cx.lang)[1])}</span></li>" for s in C["process"])
    return f'<ol class="steps">{items}</ol>'


def section_head(eyebrow, h, extra=""):
    return f'<div class="head"><h2><small>{esc(eyebrow)}</small>{h}</h2>{extra}</div>'


# ---------------------------------------------------------------- pages
def page_home(cx):
    h, l, ui = C["home"], cx.lang, C["ui"]
    doors = "".join(f'<a class="door" href="{cx.page(d["href"])}"><span class="k">{T(d["kicker"], l)}</span><b>{T(d["title"], l)}</b><span>{T(d["text"], l)}</span></a>' for d in h["doors"])
    tiles = "".join(f'<a class="tile" href="{cx.page("services.html")}#{s["id"]}" style="text-decoration:none"><span class="ico">{icon(s["icon"])}</span><h3>{T(s["title"], l)}</h3><p>{T(s["short"], l)}</p></a>' for s in C["services"])
    cards = "".join(project_card(cx, p, compact=True) for p in C["projects"])
    more = f'<a class="btn" href="{cx.page("projects.html")}">{T(h["projects_more"], l)} →</a>'
    return head(cx, tr(h["title"], l), tr(h["description"], l)) + header(cx, "home") + f"""
<div class="hero"><div class="wrap">
  <div>
    <p class="eyebrow">{T(h['eyebrow'], l)}</p>
    <h1>{tr(h['h1_html'], l)}</h1>
    <p class="lede">{T(h['lede'], l)}</p>
    <div class="doors">{doors}</div>
  </div>
  <canvas class="matrix" id="matrix" role="img" aria-label="{'ZM 点阵动画' if l == 'zh' else 'Animated ZM dot matrix'}"></canvas>
</div></div>
<section><div class="wrap">{section_head('SERVICES', T(h['services_h'], l))}<div class="tiles">{tiles}</div></div></section>
<section><div class="wrap">{section_head('PROJECTS', T(h['projects_h'], l), more)}<div class="grid compact">{cards}</div></div></section>
<section><div class="wrap">{section_head('PROCESS', T(h['process_h'], l), f'<p class="lede">{T(h["process_note"], l)}</p>')}{steps(cx)}</div></section>
""" + cta(cx, h["cta_h"], h["cta_text"]) + footer(cx)


def page_services(cx):
    sp, l = C["services_page"], cx.lang
    by_id = {p["id"]: p for p in C["projects"]}
    blocks = []
    for s in C["services"]:
        rel = ""
        if s["related"]:
            chips = "".join(f'<a class="chiplink" href="{cx.page("projects.html")}#{r}">{esc(by_id[r]["name"])}</a>' for r in s["related"])
            rel = f'<div class="rel"><span class="lbl">{T(sp["related_h"], l)}</span>{chips}</div>'
        blocks.append(f"""<div class="svc" id="{s['id']}">
  <div class="t"><span class="ico">{icon(s['icon'])}</span><div><h3>{T(s['title'], l)}</h3><p class="muted small" style="margin:2px 0 0">{T(s['short'], l)}</p></div></div>
  <div><p>{T(s['long'], l)}</p>{rel}</div>
</div>""")
    return head(cx, tr(sp["title"], l), tr(sp["description"], l)) + header(cx, "services") + f"""
<div class="pagehead"><div class="wrap"><p class="eyebrow">{T(sp['eyebrow'], l)}</p><h1>{T(sp['h1'], l)}</h1><p class="lede">{T(sp['lede'], l)}</p></div></div>
<section><div class="wrap">{''.join(blocks)}</div></section>
<section><div class="wrap">{section_head('PROCESS', T(sp['process_h'], l), f'<p class="lede">{T(C["home"]["process_note"], l)}</p>')}{steps(cx)}</div></section>
""" + cta(cx, sp["cta_h"], sp["cta_text"]) + footer(cx)


def page_projects(cx):
    pp, l, ui = C["projects_page"], cx.lang, C["ui"]
    counts = {}
    for p in C["projects"]:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    chips = f'<button class="chip" type="button" data-cat="all" aria-pressed="true">{T(ui["all"], l)}<em>{len(C["projects"])}</em></button>'
    chips += "".join(f'<button class="chip" type="button" data-cat="{k}" aria-pressed="false">{T(v, l)}<em>{counts[k]}</em></button>'
                     for k, v in C["categories"].items() if counts.get(k))
    cards = "".join(project_card(cx, p) for p in C["projects"])
    feat = next(p for p in C["projects"] if p["id"] == "aclt")
    steps_li = "".join(f"<li>{esc(x)}</li>" for x in tr(pp["featured_steps"], l))
    others = []
    for p in C["projects"]:
        if p["id"] == "aclt" or not p.get("demo"):
            continue
        d = p["demo"]
        others.append(f"""<article class="demo">{media(cx, p)}
  <div class="body"><div class="meta"><span class="cat">{esc(p['name'])}</span></div><h3>{T(d['label'], l)}</h3><p>{T(d['desc'], l)}</p>
  <div class="actions"><a class="btn demo" href="{cx.res(d['href'])}">▶ {T(ui['open_demo'], l)}</a></div></div>
</article>""")
    return head(cx, tr(pp["title"], l), tr(pp["description"], l)) + header(cx, "projects") + f"""
<div class="pagehead"><div class="wrap"><p class="eyebrow">{T(pp['eyebrow'], l)}</p><h1>{T(pp['h1'], l)}</h1><p class="lede">{T(pp['lede'], l)}</p></div></div>
<section><div class="wrap">
  <div class="head"><div class="chips" role="group" aria-label="{T(ui['filter'], l)}">{chips}</div></div>
  <div class="grid">{cards}</div>
</div></section>
<section id="demos"><div class="wrap">
  {section_head('DEMOS', T(pp['demos_h'], l), f'<p class="lede">{T(pp["demos_text"], l)}</p>')}
  <div class="feature">
    {media(cx, feat)}
    <div><h3>{T(pp['featured_title'], l)}</h3><p>{T(pp['featured_text'], l)}</p><ul>{steps_li}</ul>
    <div class="row"><a class="btn demo" href="{cx.res(feat['demo']['href'])}">▶ {T(ui['open_demo'], l)}</a></div></div>
  </div>
  <div class="demos">{''.join(others)}</div>
  <div class="callout"><b>{T(pp['oss_h'], l)}</b> · {T(pp['oss_text'], l)}</div>
</div></section>
""" + footer(cx)


def page_about(cx):
    ap, l, s = C["about_page"], cx.lang, C["site"]
    intro = "".join(f"<p>{esc(x)}</p>" for x in tr(ap["intro"], l))
    facts = "".join(f"<div><dt>{T(f['k'], l)}</dt><dd>{T(f['v'], l)}</dd></div>" for f in ap["facts"])
    team = "".join(f"""<div class="person"><span class="mono-av" aria-hidden="true">{esc(m['initial'])}</span><h3>{T(m['name'], l)}</h3><span class="role">{T(m['role'], l)}</span><p>{T(m['text'], l)}</p></div>""" for m in ap["team"])
    pa = ap["partner"]
    return head(cx, tr(ap["title"], l), tr(ap["description"], l)) + header(cx, "about") + f"""
<div class="pagehead"><div class="wrap"><p class="eyebrow">{T(ap['eyebrow'], l)}</p><h1>{T(ap['h1'], l)}</h1></div></div>
<section style="padding-top:20px"><div class="wrap about-intro"><div>{intro}</div><dl class="facts">{facts}</dl></div></section>
<section><div class="wrap">{section_head('TEAM', T(ap['team_h'], l))}<div class="team">{team}</div>
  <div class="partner"><span class="ico">{icon('server')}</span><div><p class="eyebrow" style="margin:0 0 2px">{T(ap['partner_h'], l)}</p><h3>{T(pa['name'], l)}</h3><p>{T(pa['text'], l)}</p></div></div>
</div></section>
<section><div class="wrap">{section_head('AI', T(ap['ai_h'], l))}<p class="prose">{T(s['ai_note'], l)}</p></div></section>
""" + cta(cx, C["home"]["cta_h"], C["home"]["cta_text"]) + footer(cx)


def page_contact(cx):
    cp, l, s, ui = C["contact_page"], cx.lang, C["site"], C["ui"]
    from urllib.parse import quote
    topics = "".join(f'<a class="topic" href="mailto:{s["email"]}?subject={quote("[ZeroMatrixTech] " + tr(t, l)[1])}"><b>{esc(tr(t, l)[0])}</b><span>{esc(tr(t, l)[1])}</span></a>' for t in cp["topics"])
    return head(cx, tr(cp["title"], l), tr(cp["description"], l)) + header(cx, "contact") + f"""
<div class="pagehead"><div class="wrap"><p class="eyebrow">{T(cp['eyebrow'], l)}</p><h1>{T(cp['h1'], l)}</h1><p class="lede">{T(cp['lede'], l)}</p></div></div>
<section style="padding-top:28px"><div class="wrap contact">
  <div>
    <div class="panel"><h3>{T(cp['email_h'], l)}</h3><p class="big"><span id="mail">{esc(s['email'])}</span></p>
      <div class="row" style="margin-top:10px"><a class="btn primary" href="mailto:{s['email']}">{icon('mail', 16)} {T(ui['email_us'], l)}</a><button class="btn" type="button" data-copy="mail" data-ok="{T(ui['copied'], l)}" data-fail="{T(ui['copy_fail'], l)}">{T(ui['copy'], l)}</button></div></div>
    <div class="panel"><h3>{T(cp['address_h'], l)}</h3><p>{T(s['address'], l)}</p></div>
  </div>
  <div>
    <div class="panel"><h3>{T(cp['topics_h'], l)}</h3><div class="topics">{topics}</div><p class="note">{T(cp['topics_note'], l)}</p></div>
    <div class="panel"><h3>{T(cp['oss_h'], l)}</h3><p>{T(cp['oss_text'], l)}</p><div class="row" style="margin-top:10px"><a class="btn" href="{s['repos']}" rel="noopener">{T(ui['footer_repos'], l)} ↗</a></div></div>
  </div>
</div></section>
""" + footer(cx)


def page_404():
    ui = C["ui"]
    css = '<link rel="stylesheet" href="/assets/site.css"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">'
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 · ZeroMatrixTech</title><meta name="robots" content="noindex">{css}
<script>try{{var t=localStorage.getItem("zmt-theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script></head>
<body><main class="nf"><div>
<p class="code">404</p>
<h1>{esc(ui['not_found_title']['zh'])} · {esc(ui['not_found_title']['en'])}</h1>
<p class="lede" style="margin-inline:auto">{esc(ui['not_found_text']['zh'])}<br>{esc(ui['not_found_text']['en'])}</p>
<div class="row" style="justify-content:center"><a class="btn primary" href="/">{esc(ui['not_found_home']['zh'])}</a><a class="btn" href="/en/">{esc(ui['not_found_home']['en'])}</a></div>
</div></main></body></html>
"""


RENDER = {"index.html": page_home, "services.html": page_services, "projects.html": page_projects,
          "about.html": page_about, "contact.html": page_contact}


def favicon():
    cells = []
    for i in range(9):
        x, y = 4 + (i % 3) * 9, 4 + (i // 3) * 9
        fill = "#0C7A69" if i == 4 else ("#5A6371" if i in (2, 6) else "#C9D0D8")
        cells.append(f'<rect x="{x}" y="{y}" width="7" height="7" rx="1.6" fill="{fill}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36">{"".join(cells)}</svg>\n'


def build():
    written = []
    for lang in LANGS:
        out = DOCS if lang == "zh" else DOCS / "en"
        out.mkdir(parents=True, exist_ok=True)
        for f in PAGES:
            (out / f).write_text(RENDER[f](Ctx(lang, f)), encoding="utf-8")
            written.append(out / f)
    (DOCS / "404.html").write_text(page_404(), encoding="utf-8")
    (DOCS / "assets" / "favicon.svg").write_text(favicon(), encoding="utf-8")
    urls = "".join(f"  <url><loc>{Ctx(l, f).url()}</loc></url>\n" for l in LANGS for f in PAGES)
    (DOCS / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {C['site']['url']}sitemap.xml\n", encoding="utf-8")
    print(f"built {len(written)} pages + 404, favicon, sitemap, robots")


def check():
    """Every relative href/src in docs/*.html and docs/en/*.html must point at an existing file."""
    bad = 0
    for page in sorted([*DOCS.glob("*.html"), *(DOCS / "en").glob("*.html")]):
        text = page.read_text(encoding="utf-8")
        for ref in re.findall(r'(?:href|src)="([^"]+)"', text):
            if re.match(r"^(https?:|mailto:|#|data:)", ref) or ref.startswith("/"):
                continue
            target = (page.parent / ref.split("#")[0].split("?")[0]).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                bad += 1
                print(f"BROKEN {page.relative_to(DOCS)} -> {ref}")
    print("links ok" if not bad else f"{bad} broken link(s)")
    return bad == 0


if __name__ == "__main__":
    if "--check" not in sys.argv:
        build()
    sys.exit(0 if check() else 1)
