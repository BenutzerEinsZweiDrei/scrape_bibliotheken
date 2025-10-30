import json

with open("bibliotheken.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("bibliotheken.md", "w", encoding="utf-8") as f:
    f.write("# Liste deutscher Stadtbibliotheken\n\n")
    for entry in data:
        name = entry.get("name", "Unbekannt")
        wiki = entry.get("wikipedia_url", "")
        site = entry.get("website", "")
        f.write(f"## [{name}]({wiki})\n")
        if site:
            f.write(f"- 🌐 Website: [{site}]({site})\n")
        f.write("\n")
