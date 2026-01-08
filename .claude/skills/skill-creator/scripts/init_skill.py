#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
 init_skill.py <skill-name> --path <path>

Examples:
 init_skill.py my-new-skill --path skills/
 init_skill.py my-api-helper --path ../skills/
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: |
  [TODO: Complete and informative explanation of what the skill does and when to use it.
  Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Usage

[TODO: Describe how to use this skill]

## Resources

This skill includes example resource directories:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly.

### references/
Documentation and reference material to be loaded into context as needed.

### assets/
Files not intended to be loaded into context, but used within the output.

---

**Delete any unneeded directories.** Not every skill requires all three types of resources.
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

Replace with actual implementation or delete if not needed.
"""


def main():
    print("This is an example script for {skill_name}")
    # TODO: Add actual script logic here


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

## Common Asset Types

- Templates: .pptx, .docx, boilerplate directories
- Images: .png, .jpg, .svg
- Fonts: .ttf, .otf, .woff
- Data files: .csv, .json, .yaml
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created

    Returns:
        Path to created skill directory, or None if error
    """
    # Determine skill directory path
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("Created SKILL.md")
    except Exception as e:
        print(f"Error creating SKILL.md: {e}")
        return None

    # Create resource directories with example files
    try:
        # Create scripts/ directory with example script
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("Created scripts/example.py")

        # Create references/ directory with example reference doc
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("Created references/api_reference.md")

        # Create assets/ directory with example asset placeholder
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("Created assets/example_asset.txt")
    except Exception as e:
        print(f"Error creating resource directories: {e}")
        return None

    # Print next steps
    print(f"\nSkill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    print("2. Customize or delete the example files in scripts/, references/, and assets/")
    print("3. Run the validator when ready: python quick_validate.py <skill_dir>")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path>")
        print("\nSkill name requirements:")
        print(" - Hyphen-case identifier (e.g., 'data-analyzer')")
        print(" - Lowercase letters, digits, and hyphens only")
        print(" - Max 64 characters")
        print("\nExamples:")
        print(" init_skill.py my-new-skill --path skills/")
        print(" init_skill.py my-api-helper --path ../skills/")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"Initializing skill: {skill_name}")
    print(f"Location: {path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
