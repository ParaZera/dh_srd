#!/usr/bin/env python3
# Script to generate the landing page with links to all translated documents

import os
import re
from pathlib import Path
from collections import defaultdict

# Configuration
# Get the directory of the current script, then navigate to the srd directory
SRD_ROOT = Path(__file__).parent.parent / "srd"
LANDING_PAGE = SRD_ROOT.parent / "script" / "index.html"
PLACEHOLDER = "<!-- TRANSLATION_LINKS_PLACEHOLDER -->"

# Language codes to full names mapping
LANGUAGE_NAMES = {
    "de": "German (Deutsch)",
    # Add more languages as needed
}


def get_language_name(lang_code):
    """Get the full name of a language from its code."""
    return LANGUAGE_NAMES.get(lang_code, lang_code.upper())


def find_translations():
    """Find all available translations in the SRD directory."""
    translations = defaultdict(list)

    # Walk through the SRD directory structure
    for version_dir in SRD_ROOT.iterdir():
        if not version_dir.is_dir():
            continue

        version = version_dir.name

        # Find all language directories within this version
        for lang_dir in version_dir.iterdir():
            if not lang_dir.is_dir():
                continue

            lang_code = lang_dir.name

            # Check if this is a valid mdbook by looking for SUMMARY.md
            summary_path = lang_dir / "src" / "SUMMARY.md"
            if not summary_path.exists():
                continue

            # Find the index.html that corresponds to this translation
            index_path = lang_dir.relative_to(SRD_ROOT.parent) / "book" / "index.html"

            # Extract title from book.toml if available
            title = get_language_name(lang_code)
            book_toml_path = lang_dir / "book.toml"
            if book_toml_path.exists():
                with open(book_toml_path, "r", encoding="utf-8") as f:
                    toml_content = f.read()
                    title_match = re.search(r'title\s*=\s*"([^"]+)"', toml_content)
                    if title_match:
                        title = title_match.group(1)

            translations[lang_code].append(
                {"version": version, "path": f"/{index_path}", "title": title}
            )

    return translations


def generate_html_content(translations):
    """Generate HTML content for the language cards."""
    html_content = ""

    for lang_code, versions in sorted(translations.items()):
        language_name = get_language_name(lang_code)

        html_content += f"""
        <div class="language-card">
            <h2>{language_name}</h2>
            <ul>
"""

        # Sort versions by version number (assuming they're formatted as x.y)
        for version_info in sorted(
            versions,
            key=lambda v: [int(n) for n in v["version"].split(".") if n.isdigit()],
        ):
            version = version_info["version"]
            path = version_info["path"]
            title = version_info["title"]

            html_content += (
                f'                <li><a href="{path}">Version {version}</a></li>\n'
            )

        html_content += """            </ul>
        </div>
"""

    return html_content


def update_landing_page(html_content):
    """Update the landing page HTML with the generated content."""
    with open(LANDING_PAGE, "r", encoding="utf-8") as f:
        content = f.read()

    updated_content = content.replace(PLACEHOLDER, html_content)

    with open(LANDING_PAGE, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"Updated landing page at {LANDING_PAGE}")


def main():
    """Main function to find translations and update the landing page."""
    print("Searching for translations...")
    translations = find_translations()

    if not translations:
        print("No translations found.")
        return

    print(f"Found translations for {len(translations)} languages:")
    for lang_code, versions in translations.items():
        print(f"  - {get_language_name(lang_code)}: {len(versions)} version(s)")

    html_content = generate_html_content(translations)
    update_landing_page(html_content)


if __name__ == "__main__":
    main()
