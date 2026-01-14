#!/usr/bin/env python3
"""
Génère automatiquement un README.md pour un dossier docs/.

Usage:
    python3 generate-docs-index.py /path/to/project/docs
    python3 generate-docs-index.py .  # utilise ./docs du dossier courant

Le script :
1. Scanne récursivement le dossier docs/
2. Extrait le titre (premier #) de chaque fichier .md
3. Génère un README.md organisé par sous-dossier
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime


def extract_title(filepath: Path) -> str:
    """Extrait le titre (premier # heading) d'un fichier markdown."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Cherche le premier heading
                if line.startswith("# "):
                    return line[2:].strip()
        # Pas de titre trouvé, utilise le nom du fichier
        return filepath.stem.replace("-", " ").replace("_", " ").title()
    except Exception:
        return filepath.stem


def scan_docs(docs_path: Path) -> dict:
    """
    Scanne le dossier docs et retourne une structure organisée.

    Returns:
        {
            "architecture": [
                {"path": "architecture/overview.md", "title": "Overview"},
                ...
            ],
            "devbooks": [...],
            ...
        }
    """
    result = {}

    for item in sorted(docs_path.iterdir()):
        # Ignorer les fichiers cachés et le README lui-même
        if item.name.startswith(".") or item.name.lower() == "readme.md":
            continue

        if item.is_dir():
            # Sous-dossier : scanner récursivement
            files = []
            for md_file in sorted(item.glob("**/*.md")):
                if md_file.name.lower() == "readme.md":
                    continue
                rel_path = md_file.relative_to(docs_path)
                files.append({
                    "path": str(rel_path),
                    "title": extract_title(md_file),
                    "name": md_file.stem
                })
            if files:
                result[item.name] = files

        elif item.suffix == ".md":
            # Fichier à la racine
            if "root" not in result:
                result["root"] = []
            result["root"].append({
                "path": item.name,
                "title": extract_title(item),
                "name": item.stem
            })

    return result


def generate_readme(docs_structure: dict, project_name: str = "") -> str:
    """Génère le contenu du README.md."""

    lines = [
        "# Documentation",
        "",
        f"*Index auto-généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
    ]

    # Ordre préféré des sections
    section_order = ["architecture", "reference", "devbooks", "research", "guides", "root"]
    section_titles = {
        "architecture": "Architecture",
        "reference": "Référence",
        "devbooks": "Devbooks",
        "research": "Recherche",
        "guides": "Guides",
        "root": "Autres"
    }

    # Trier les sections selon l'ordre préféré
    sorted_sections = []
    for section in section_order:
        if section in docs_structure:
            sorted_sections.append(section)
    # Ajouter les sections non prévues
    for section in docs_structure:
        if section not in sorted_sections:
            sorted_sections.append(section)

    for section in sorted_sections:
        files = docs_structure[section]
        title = section_titles.get(section, section.replace("-", " ").replace("_", " ").title())

        lines.append(f"## {title}")
        lines.append("")

        for file_info in files:
            # Format: - [Titre](path)
            lines.append(f"- [{file_info['title']}]({file_info['path']})")

        lines.append("")

    # Footer
    lines.extend([
        "---",
        "",
        "*Cet index est généré automatiquement par `scripts/generate-docs-index.py`*"
    ])

    return "\n".join(lines)


def main():
    # Déterminer le chemin docs/
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if target.name == "docs":
            docs_path = target
        else:
            docs_path = target / "docs"
    else:
        docs_path = Path.cwd() / "docs"

    if not docs_path.exists():
        print(f"Erreur: Le dossier {docs_path} n'existe pas.")
        sys.exit(1)

    if not docs_path.is_dir():
        print(f"Erreur: {docs_path} n'est pas un dossier.")
        sys.exit(1)

    # Scanner et générer
    print(f"Scanning {docs_path}...")
    structure = scan_docs(docs_path)

    if not structure:
        print("Aucun fichier markdown trouvé.")
        sys.exit(0)

    # Générer le README
    readme_content = generate_readme(structure)
    readme_path = docs_path / "README.md"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"✓ README.md généré: {readme_path}")

    # Afficher un résumé
    total_files = sum(len(files) for files in structure.values())
    print(f"  {len(structure)} sections, {total_files} fichiers indexés")


if __name__ == "__main__":
    main()
