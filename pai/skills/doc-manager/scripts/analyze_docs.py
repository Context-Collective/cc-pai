#!/usr/bin/env python3
"""
Analyze documentation structure in a project.
Supports both simple projects and monorepos.
Outputs JSON with structure analysis and recommendations.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Files to always ignore
IGNORE_FILES = {
    'README.md', 'CLAUDE.md', 'CONTRIBUTING.md', 'LICENSE.md',
    'CHANGELOG.md', 'CODE_OF_CONDUCT.md', '.env', '.env.example'
}

# Directories to always skip
SKIP_DIRS = {
    'node_modules', '.git', 'dist', 'build', '.next', '__pycache__',
    '.vscode', '.idea', 'vendor', 'coverage', '.cache', '.expo',
    '_archive', 'archives'
}

# Config files to ignore (not documentation)
CONFIG_FILES = {
    'package.json', 'package-lock.json', 'tsconfig.json', 'tsconfig.node.json',
    'tsconfig.app.json', 'vite.config.ts', 'vite.config.js',
    'tailwind.config.js', 'tailwind.config.ts', 'postcss.config.js', 'postcss.config.cjs',
    '.eslintrc.js', '.eslintrc.cjs', '.eslintrc.json',
    '.prettierrc', '.prettierrc.json', 'prettier.config.js',
    'jest.config.js', 'jest.config.ts', 'vitest.config.ts', 'vitest.config.js',
    'next.config.js', 'next.config.mjs', 'nuxt.config.ts',
    'composer.json', 'requirements.txt', 'pyproject.toml', 'Cargo.toml',
    'bun.lockb', 'yarn.lock', 'pnpm-lock.yaml', 'pnpm-workspace.yaml',
    'lerna.json', 'nx.json', 'turbo.json'
}

# Monorepo indicators
MONOREPO_INDICATORS = {
    'pnpm-workspace.yaml',
    'lerna.json',
    'nx.json',
    'turbo.json'
}

# Common monorepo package directories
MONOREPO_PATTERNS = {'packages', 'apps', 'libs', 'services', 'modules'}


def to_kebab_case(name: str) -> str:
    """Convert filename to kebab-case."""
    base = Path(name).stem
    ext = Path(name).suffix

    # Replace underscores and spaces with hyphens
    result = re.sub(r'[_\s]+', '-', base)
    # Handle camelCase
    result = re.sub(r'([a-z])([A-Z])', r'\1-\2', result)
    # Lowercase
    result = result.lower()
    # Remove multiple hyphens
    result = re.sub(r'-+', '-', result)
    # Remove leading/trailing hyphens
    result = result.strip('-')

    return result + ext.lower()


def detect_naming_issues(filename: str) -> list:
    """Detect naming convention issues."""
    issues = []
    base = Path(filename).stem

    # Check for uppercase
    if base.isupper() or re.search(r'[A-Z]{2,}', base):
        issues.append('uppercase')

    # Check for underscores (should use hyphens)
    if '_' in base:
        issues.append('underscore')

    # Check for spaces
    if ' ' in filename:
        issues.append('spaces')

    # Check for special characters
    if re.search(r'[àâäéèêëïîôùûüç]', base, re.IGNORECASE):
        issues.append('accents')

    return issues


def detect_doc_type(filename: str) -> str:
    """Detect document type from filename prefix/pattern."""
    base = Path(filename).stem.lower()

    # Architecture docs
    if base.startswith(('architecture', 'arch-', 'overview', 'design')):
        return 'architecture'

    # API/Reference docs
    if base.startswith(('api-', 'api_', 'reference', 'ref-')):
        return 'api-reference'

    # Devbooks/Investigations
    if base.startswith(('devbook-', 'fix-', 'bug-', 'debug-', 'investigation-')):
        return 'devbook'

    # Specifications
    if base.startswith(('spec-', 'prd-', 'rfc-', 'proposal-')):
        return 'spec'

    # Research
    if base.startswith(('research-', 'analyse-', 'analysis-', 'benchmark-')):
        return 'research'

    return 'general'


def detect_monorepo(project_path: Path) -> dict:
    """Detect if project is a monorepo and find packages."""
    result = {
        'is_monorepo': False,
        'indicator': None,
        'packages': [],
        'packages_dir': None,
        'has_workspaces': False
    }

    # Check for monorepo config files
    for indicator in MONOREPO_INDICATORS:
        if (project_path / indicator).exists():
            result['is_monorepo'] = True
            result['indicator'] = indicator
            break

    # Check package.json for workspaces
    package_json = project_path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json, 'r') as f:
                pkg = json.load(f)
                if 'workspaces' in pkg:
                    result['is_monorepo'] = True
                    result['has_workspaces'] = True
                    result['indicator'] = 'package.json workspaces'
        except (json.JSONDecodeError, IOError):
            pass

    # Find packages - check root level first
    if result['is_monorepo']:
        for item in project_path.iterdir():
            if item.is_dir() and item.name not in SKIP_DIRS:
                if (item / 'package.json').exists():
                    result['packages'].append(item.name)

    # If no packages found at root, check standard monorepo directories
    if result['is_monorepo'] and not result['packages']:
        packages_dirs = []
        for mono_dir in MONOREPO_PATTERNS:
            mono_path = project_path / mono_dir
            if mono_path.exists() and mono_path.is_dir():
                packages_dirs.append(mono_dir)
                for item in mono_path.iterdir():
                    if item.is_dir() and item.name not in SKIP_DIRS:
                        if (item / 'package.json').exists():
                            result['packages'].append(f"{mono_dir}/{item.name}")
                        elif any((item / f).exists() for f in ['src', 'lib', 'index.ts', 'index.js']):
                            # Package without package.json but looks like a package
                            result['packages'].append(f"{mono_dir}/{item.name}")
        if packages_dirs:
            result['packages_dir'] = packages_dirs if len(packages_dirs) > 1 else packages_dirs[0]

    # Also check for multiple package.json as indicator
    if not result['is_monorepo']:
        pkg_count = 0
        for item in project_path.iterdir():
            if item.is_dir() and item.name not in SKIP_DIRS:
                if (item / 'package.json').exists():
                    pkg_count += 1
                    result['packages'].append(item.name)
        if pkg_count >= 2:
            result['is_monorepo'] = True
            result['indicator'] = 'multiple package.json'

    return result


def find_docs_in_dir(dir_path: Path, base_path: Path) -> list:
    """Find all markdown files in a directory."""
    docs = []
    if not dir_path.exists():
        return docs

    for item in dir_path.rglob('*.md'):
        rel_path = str(item.relative_to(base_path))
        # Skip ignored files
        if item.name in IGNORE_FILES:
            continue
        # Skip files in skip dirs
        if any(skip in rel_path.split(os.sep) for skip in SKIP_DIRS):
            continue
        docs.append({
            'path': rel_path,
            'name': item.name,
            'dir': str(item.parent.relative_to(base_path))
        })

    return docs


def find_doc_like_dirs(project_path: Path, skip_dirs: set) -> list:
    """Find directories that look like documentation folders."""
    doc_patterns = {'docs', 'doc', 'documentation', 'wiki'}
    doc_like = []

    for item in project_path.iterdir():
        if item.is_dir() and item.name not in skip_dirs:
            name_lower = item.name.lower()
            # Check if name contains 'doc' pattern
            if any(pattern in name_lower for pattern in doc_patterns):
                if item.name != 'docs':  # Skip standard docs/
                    # Count markdown files inside
                    md_count = len(list(item.glob('*.md')))
                    if md_count > 0:
                        doc_like.append({
                            'name': item.name,
                            'path': str(item.relative_to(project_path)),
                            'md_count': md_count
                        })

    return doc_like


def analyze_project(project_path: str) -> dict:
    """Analyze a project's documentation structure."""
    project = Path(project_path)

    if not project.exists():
        return {'error': f'Path does not exist: {project_path}'}

    # Detect project type
    monorepo_info = detect_monorepo(project)

    # Find doc-like directories that aren't standard docs/
    doc_like_dirs = find_doc_like_dirs(project, SKIP_DIRS)

    result = {
        'project_path': str(project.absolute()),
        'project_name': project.name,
        'analysis_date': datetime.now().isoformat(),
        'project_type': 'monorepo' if monorepo_info['is_monorepo'] else 'simple',
        'monorepo_info': monorepo_info if monorepo_info['is_monorepo'] else None,
        'docs_centralized': [],
        'docs_dispersed': [],
        'docs_root': [],
        'docs_alternative': [],  # Non-standard doc directories
        'issues': {
            'naming': [],
            'dispersed_count': 0,
            'missing_index': False,
            'no_scope': [],
            'alternative_doc_dirs': doc_like_dirs
        },
        'recommendations': []
    }

    # Check for centralized docs/
    docs_path = project / 'docs'
    has_central_docs = docs_path.exists() and docs_path.is_dir()

    if has_central_docs:
        # Scan centralized docs
        for item in docs_path.rglob('*.md'):
            if item.name in IGNORE_FILES:
                continue
            rel_path = str(item.relative_to(project))
            rel_to_docs = str(item.relative_to(docs_path))

            # Determine scope (first directory level in docs/)
            parts = rel_to_docs.split(os.sep)
            scope = parts[0] if len(parts) > 1 and not parts[0].endswith('.md') else None

            doc_info = {
                'path': rel_path,
                'name': item.name,
                'scope': scope,
                'type': detect_doc_type(item.name),
                'naming_issues': detect_naming_issues(item.name),
                'suggested_name': to_kebab_case(item.name)
            }

            result['docs_centralized'].append(doc_info)

            if doc_info['naming_issues']:
                result['issues']['naming'].append({
                    'file': rel_path,
                    'issues': doc_info['naming_issues'],
                    'suggested': doc_info['suggested_name']
                })

        # Check for INDEX.md
        if not (docs_path / 'INDEX.md').exists():
            result['issues']['missing_index'] = True
    else:
        result['recommendations'].append({
            'priority': 'high',
            'action': 'create_docs_dir',
            'message': 'Creer un dossier docs/ centralise'
        })

    # Scan root for stray markdown files
    for item in project.iterdir():
        if item.is_file() and item.suffix == '.md':
            if item.name in IGNORE_FILES:
                continue

            doc_info = {
                'path': item.name,
                'name': item.name,
                'type': detect_doc_type(item.name),
                'naming_issues': detect_naming_issues(item.name),
                'suggested_name': to_kebab_case(item.name),
                'suggested_destination': f'docs/{to_kebab_case(item.name)}'
            }

            result['docs_root'].append(doc_info)

            if doc_info['naming_issues']:
                result['issues']['naming'].append({
                    'file': item.name,
                    'issues': doc_info['naming_issues'],
                    'suggested': doc_info['suggested_name']
                })

    # For monorepos, scan for dispersed docs in packages
    if monorepo_info['is_monorepo']:
        for pkg_name in monorepo_info['packages']:
            # Handle nested package paths (e.g., "apps/mobile")
            pkg_path = project / pkg_name
            # Extract simple name for scope suggestion
            simple_name = pkg_name.split('/')[-1] if '/' in pkg_name else pkg_name

            # Check for docs/ in package
            pkg_docs = pkg_path / 'docs'
            if pkg_docs.exists():
                for item in pkg_docs.rglob('*.md'):
                    if item.name in IGNORE_FILES:
                        continue
                    rel_path = str(item.relative_to(project))

                    doc_info = {
                        'path': rel_path,
                        'name': item.name,
                        'source_package': pkg_name,
                        'type': detect_doc_type(item.name),
                        'naming_issues': detect_naming_issues(item.name),
                        'suggested_name': to_kebab_case(item.name),
                        'suggested_destination': f'docs/{simple_name}/{to_kebab_case(item.name)}'
                    }

                    result['docs_dispersed'].append(doc_info)
                    result['issues']['dispersed_count'] += 1

            # Check for stray .md files in package root (except README)
            if pkg_path.exists():
                for item in pkg_path.iterdir():
                    if item.is_file() and item.suffix == '.md':
                        if item.name in IGNORE_FILES:
                            continue
                        rel_path = str(item.relative_to(project))

                        doc_info = {
                            'path': rel_path,
                            'name': item.name,
                            'source_package': pkg_name,
                            'type': detect_doc_type(item.name),
                            'naming_issues': detect_naming_issues(item.name),
                            'suggested_name': to_kebab_case(item.name),
                            'suggested_destination': f'docs/{simple_name}/{to_kebab_case(item.name)}'
                        }

                        result['docs_dispersed'].append(doc_info)
                        result['issues']['dispersed_count'] += 1

        # Check for docs without clear scope in centralized docs
        if has_central_docs:
            for doc in result['docs_centralized']:
                if doc['scope'] is None:
                    # Check if it should belong to a package
                    result['issues']['no_scope'].append(doc['path'])

    # Scan alternative doc directories (like jeofun-docs/)
    for alt_dir in doc_like_dirs:
        alt_path = project / alt_dir['name']
        for item in alt_path.rglob('*.md'):
            if item.name in IGNORE_FILES:
                continue
            rel_path = str(item.relative_to(project))

            doc_info = {
                'path': rel_path,
                'name': item.name,
                'source_dir': alt_dir['name'],
                'type': detect_doc_type(item.name),
                'naming_issues': detect_naming_issues(item.name),
                'suggested_name': to_kebab_case(item.name),
                'suggested_destination': f'docs/shared/{to_kebab_case(item.name)}'
            }

            result['docs_alternative'].append(doc_info)

            if doc_info['naming_issues']:
                result['issues']['naming'].append({
                    'file': rel_path,
                    'issues': doc_info['naming_issues'],
                    'suggested': doc_info['suggested_name']
                })

    # Generate recommendations
    if result['docs_root']:
        result['recommendations'].append({
            'priority': 'medium',
            'action': 'centralize_root',
            'message': f'{len(result["docs_root"])} fichiers MD a la racine a centraliser dans docs/',
            'files': [d['path'] for d in result['docs_root']]
        })

    if result['docs_dispersed']:
        result['recommendations'].append({
            'priority': 'high',
            'action': 'centralize_dispersed',
            'message': f'{len(result["docs_dispersed"])} fichiers disperses dans les packages a centraliser',
            'files': [d['path'] for d in result['docs_dispersed']]
        })

    if result['docs_alternative']:
        alt_dirs = list(set(d['source_dir'] for d in result['docs_alternative']))
        result['recommendations'].append({
            'priority': 'high',
            'action': 'consolidate_alternative',
            'message': f'{len(result["docs_alternative"])} fichiers dans dossier(s) non-standard: {", ".join(alt_dirs)}',
            'suggestion': 'Renommer en docs/ ou deplacer le contenu vers docs/',
            'files': [d['path'] for d in result['docs_alternative']]
        })

    if result['issues']['missing_index'] and has_central_docs:
        result['recommendations'].append({
            'priority': 'low',
            'action': 'generate_index',
            'message': 'INDEX.md manquant dans docs/'
        })

    if result['issues']['naming']:
        result['recommendations'].append({
            'priority': 'low',
            'action': 'fix_naming',
            'message': f'{len(result["issues"]["naming"])} fichiers avec nommage non standard',
            'files': [n['file'] for n in result['issues']['naming']]
        })

    # For monorepos, check which packages have no documentation
    if monorepo_info['is_monorepo'] and monorepo_info['packages']:
        # Get documented scopes
        documented_scopes = set()
        for doc in result['docs_centralized']:
            if doc['scope']:
                documented_scopes.add(doc['scope'])
        for doc in result['docs_dispersed']:
            simple_name = doc['source_package'].split('/')[-1]
            documented_scopes.add(simple_name)

        # Find undocumented packages
        undocumented = []
        for pkg in monorepo_info['packages']:
            simple_name = pkg.split('/')[-1]
            if simple_name not in documented_scopes:
                undocumented.append(pkg)

        if undocumented:
            result['issues']['undocumented_packages'] = undocumented
            result['recommendations'].append({
                'priority': 'medium',
                'action': 'document_packages',
                'message': f'{len(undocumented)} packages sans documentation',
                'packages': undocumented,
                'suggestion': 'Creer docs/[package]/ pour chaque package important'
            })

    # Summary stats
    result['summary'] = {
        'total_docs': len(result['docs_centralized']) + len(result['docs_dispersed']) + len(result['docs_root']) + len(result['docs_alternative']),
        'centralized': len(result['docs_centralized']),
        'dispersed': len(result['docs_dispersed']),
        'root': len(result['docs_root']),
        'alternative': len(result['docs_alternative']),
        'alternative_dirs': [d['name'] for d in doc_like_dirs],
        'scopes': list(set(d['scope'] for d in result['docs_centralized'] if d['scope'])) if monorepo_info['is_monorepo'] else [],
        'undocumented_packages': result['issues'].get('undocumented_packages', [])
    }

    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Usage: analyze_docs.py <project_path>'}))
        sys.exit(1)

    project_path = sys.argv[1]
    result = analyze_project(project_path)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
