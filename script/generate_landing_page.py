#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [ "jinja2" ]
# ///
# Script to generate the landing page with links to all translated documents

import argparse
import re
from pathlib import Path
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

# Language codes to full names mapping
LANGUAGE_NAMES = {
    "de": "German (Deutsch)",
    # Add more languages as needed
}


def get_language_name(lang_code):
    """Get the full name of a language from its code."""
    return LANGUAGE_NAMES.get(lang_code, lang_code.upper())


def find_translations(srd_root):
    """Find all available translations in the SRD directory."""
    translations = defaultdict(list)

    # Walk through the SRD directory structure
    for version_dir in srd_root.iterdir():
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

            # Generate relative path from landing page to translation
            relative_path = f"srd/{version}/{lang_code}/index.html"

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
                {"version": version, "url": relative_path, "title": title}
            )

    return translations


def generate_landing_page(translations, template_file, output_file):
    """Generate the landing page using Jinja2 template."""
    # Set up Jinja2 environment
    template_path = Path(template_file)
    env = Environment(loader=FileSystemLoader(template_path.parent))
    env.globals["get_language_name"] = get_language_name

    # Load template
    template = env.get_template(template_path.name)

    # Sort translations for consistent output
    sorted_translations = dict(sorted(translations.items()))
    for lang_code in sorted_translations:
        sorted_translations[lang_code] = sorted(
            sorted_translations[lang_code],
            key=lambda v: [int(n) for n in v["version"].split(".") if n.isdigit()],
        )

    # Render template
    html_content = template.render(translations=sorted_translations)

    # Write output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated landing page at {output_file}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate landing page with links to all translated documents"
    )

    # Default paths based on script location
    script_dir = Path(__file__).parent
    default_srd_root = script_dir.parent / "srd"
    default_template = script_dir / "index.html.j2"
    default_output = script_dir / "index.html"

    parser.add_argument(
        "-s",
        "--source-dir",
        type=Path,
        default=default_srd_root,
        help=f"Path to the SRD directory (default: {default_srd_root})",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=script_dir,
        help=f"Output directory for the generated HTML file (default: {script_dir})",
    )

    parser.add_argument(
        "-t",
        "--template-file",
        type=Path,
        default=default_template,
        help=f"Path to the Jinja2 template file (default: {default_template})",
    )

    return parser.parse_args()


def main():
    """Main function to find translations and generate the landing page."""
    args = parse_arguments()

    srd_root = args.source_dir
    output_dir = args.output_dir
    template_file = args.template_file
    output_file = output_dir / "index.html"

    # Validate paths
    if not srd_root.exists():
        print(f"Error: Source directory '{srd_root}' does not exist.")
        return 1

    if not template_file.exists():
        print(f"Error: Template file '{template_file}' does not exist.")
        return 1

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Searching for translations in {srd_root}...")
    translations = find_translations(srd_root)

    if not translations:
        print("No translations found.")
        return 1

    print(f"Found translations for {len(translations)} languages:")
    for lang_code, versions in translations.items():
        print(f"  - {get_language_name(lang_code)}: {len(versions)} version(s)")

    generate_landing_page(translations, template_file, output_file)
    return 0


if __name__ == "__main__":
    exit(main())
