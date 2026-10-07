"""Builds the HabiVox site from src/ into plain HTML files in this folder.

Run:  python build.py

Shared header, footer and <head> live here so every page stays identical.
Icons are Lucide (https://lucide.dev), inlined from src/icons.json.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"

# Set this once the custom domain is connected, e.g. "https://habivox.app".
# Canonical URLs, the sitemap and social preview images need the full URL.
SITE_URL = "https://www.habivox.in"

PLAY = "https://play.google.com/store/apps/details?id=com.habivox.app"
EMAIL = "ebad7work@gmail.com"
UPDATED = "6 October 2026"

PAGES = {
    "index.html": "",
    "privacy.html": "privacy",
    "terms.html": "terms",
    "delete-account.html": "delete-account",
}

ICONS = json.loads((SRC / "icons.json").read_text(encoding="utf-8"))
# Changes whenever styles.css changes, so browsers never use a stale copy.
CSS_VERSION = hashlib.md5((ROOT / "styles.css").read_bytes()).hexdigest()[:8]


def head(title, description, path):
    url = f"{SITE_URL}/{path}" if SITE_URL else ""
    social = ""
    if SITE_URL:
        social = f"""
  <link rel="canonical" href="{url}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE_URL}/assets/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:image" content="{SITE_URL}/assets/og-image.jpg">"""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#ffffff">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="HabiVox">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta name="twitter:card" content="summary_large_image">{social}
  <link rel="icon" href="favicon.ico" sizes="48x48">
  <link rel="icon" href="assets/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="styles.css?v={CSS_VERSION}">
</head>"""


def header(home):
    base = "" if home else "index.html"
    links = "\n".join(
        f'          <li><a href="{base}#{anchor}">{label}</a></li>'
        for anchor, label in [("habits", "Habits"), ("insights", "Insights"), ("money", "Money"), ("ai", "AI Coach")]
    )
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="header">
  <div class="wrap header__inner">
    <a class="brand" href="{base or '#main'}" aria-label="HabiVox home">
      <img src="assets/logo-96.png" width="32" height="32" alt="">
      HabiVox
    </a>
    <nav class="nav" aria-label="Main">
      <ul class="nav__links">
{links}
      </ul>
      <a class="btn" href="{{{{PLAY}}}}">Get the app</a>
      <details class="menu">
        <summary aria-label="Menu"><span class="icon-open">{{{{icon:menu}}}}</span><span class="icon-close">{{{{icon:x}}}}</span></summary>
        <div class="menu__panel">
          <ul>
{links}
          </ul>
          <a class="btn" href="{{{{PLAY}}}}">Get the app</a>
        </div>
      </details>
    </nav>
  </div>
</header>"""


FOOTER = """<footer class="footer">
  <div class="wrap footer__inner">
    <small>&copy; 2026 Ebad Sayed</small>
    <ul class="footer__links">
      <li><a href="privacy.html">Privacy</a></li>
      <li><a href="terms.html">Terms</a></li>
      <li><a href="delete-account.html">Delete account</a></li>
      <li><a href="mailto:{{EMAIL}}">Contact</a></li>
    </ul>
  </div>
</footer>
<script>
  // Close the mobile menu after tapping a link in it.
  document.querySelectorAll('.menu__panel a').forEach(function (a) {
    a.addEventListener('click', function () { a.closest('details').removeAttribute('open'); });
  });
</script>
</body>
</html>
"""


def fill(html):
    def icon(m):
        name = m.group(1)
        if name not in ICONS:
            sys.exit(f"Unknown icon: {name}")
        return ICONS[name]

    html = re.sub(r"\{\{icon:([a-z0-9-]+)\}\}", icon, html)
    for key, value in {"PLAY": PLAY, "EMAIL": EMAIL, "UPDATED": UPDATED}.items():
        html = html.replace("{{" + key + "}}", value)
    return html


def check(name, html):
    problems = []
    if re.search(r"\{\{|\}\}", html):
        problems.append("unfilled placeholder")
    for ch, label in [("—", "em dash"), ("–", "en dash")]:
        if ch in html:
            problems.append(label)
    if problems:
        sys.exit(f"{name}: {', '.join(problems)}")


def build():
    for out, path in PAGES.items():
        src = (SRC / out).read_text(encoding="utf-8")
        title = re.search(r"<!--title: (.*?)-->", src).group(1)
        description = re.search(r"<!--description: (.*?)-->", src).group(1)
        body = re.sub(r"<!--(title|description): .*?-->\n", "", src)
        html = fill("\n".join([head(title, description, path), header(out == "index.html"), body, FOOTER]))
        check(out, html)
        (ROOT / out).write_text(html, encoding="utf-8", newline="\n")
        print(f"built {out}")

    if SITE_URL:
        urls = "\n".join(f"  <url><loc>{SITE_URL}/{p}</loc></url>" for p in PAGES.values())
        (ROOT / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
            encoding="utf-8",
        )
        (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
        print("built sitemap.xml, robots.txt")
    else:
        print("SITE_URL is empty: set it once the domain is connected, then rebuild.")


if __name__ == "__main__":
    build()
