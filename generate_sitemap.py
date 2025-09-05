import os
from datetime import datetime

# Liste des dossiers clients (à adapter si nécessaire)
clients = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]

for client in clients:
    markdown_dir = os.path.join(client, "markdown")
    if os.path.exists(markdown_dir):
        urls = []
        for filename in os.listdir(markdown_dir):
            if filename.endswith(".md"):
                url = f"https://ia.{client}.com/markdown/{filename.replace('.md', '.html')}"
                urls.append(f"""
    <url>
      <loc>{url}</loc>
      <lastmod>{datetime.now().date()}</lastmod>
    </url>""")
        sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>"""
        with open(f"{client}/sitemap-ai.xml", "w") as f:
            f.write(sitemap)
        print(f"Generated sitemap for {client}")
