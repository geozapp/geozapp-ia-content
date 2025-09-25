import os
from datetime import datetime
from urllib.parse import quote

# === Réglages simples ===
SUBDOMAIN_PREFIX = "ia"   # mettre "ai" si nécessaire
TLD = "com"               # "com", "fr", etc.
MARKDOWN_DIRNAME = "markdown"  # dossier où sont les .md dans chaque client

def iso_date_from_mtime(path: str) -> str:
    """Retourne la date ISO (YYYY-MM-DD) basée sur le mtime du fichier."""
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts).date().isoformat()

# Liste des dossiers clients (ignore dossiers cachés)
clients = [
    d for d in os.listdir(".")
    if os.path.isdir(d)
    and not d.startswith(".")
    and os.path.exists(os.path.join(d, MARKDOWN_DIRNAME))
]

for client in clients:
    markdown_dir = os.path.join(client, MARKDOWN_DIRNAME)
    if not os.path.exists(markdown_dir):
        print(f"Markdown directory not found for {client}")
        continue

    urls = []
    # tri pour un ordre stable
    for filename in sorted(os.listdir(markdown_dir)):
        # ne prendre que les .md (insensible à la casse) et ignorer fichiers cachés
        if filename.startswith("."):
            continue
        if not filename.lower().endswith(".md"):
            continue
        # URL = .../.md (pas de conversion en .html)
        url = f"https://{SUBDOMAIN_PREFIX}.{client}.{TLD}/{MARKDOWN_DIRNAME}/{quote(filename)}"
        file_path = os.path.join(markdown_dir, filename)
        lastmod = iso_date_from_mtime(file_path)

        urls.append(
            f"""  <url>
    <loc>{url}</loc>
    <lastmod>{lastmod}</lastmod>
  </url>"""
        )

    if urls:  # Ne générer que s'il y a des URLs
        sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{os.linesep.join(urls)}
</urlset>"""
        out_path = os.path.join(client, "sitemap-ai.xml")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(sitemap)
        print(f"Generated sitemap for {client} -> {out_path}")
    else:
        print(f"No Markdown files found in {client}/{MARKDOWN_DIRNAME}/")
