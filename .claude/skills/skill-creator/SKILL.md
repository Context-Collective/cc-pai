---
name: skill-creator
description: |
  Guide for creating effective skills. Use this skill when users want to create
  a new skill (or update an existing skill) that extends Claude's capabilities
  with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities. Think of them as "onboarding guides" that transform Claude from a generalist into a specialist for specific domains or tasks.

**What skills provide:**
- Specialized workflows for specific domains
- Tool integrations (file formats, APIs)
- Domain expertise (company-specific knowledge, schemas)
- Bundled resources (scripts, references, assets)

## Core Principles

### Concise is Key
Context window is a shared public good. Claude is already intelligent - only add context Claude doesn't already have. Prefer concise examples over verbose explanations.

### Degrees of Freedom
- **High freedom**: Text instructions (multiple valid approaches)
- **Medium freedom**: Pseudocode/parameterized scripts (variation acceptable)
- **Low freedom**: Specific scripts (fragile operations, critical sequences)

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name + description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/     → Executable code (Python/Bash)
    ├── references/  → Documentation to load as needed
    └── assets/      → Files used in output (templates, images)
```

### SKILL.md Structure

**Frontmatter (required):**
```yaml
---
name: skill-name
description: |
  What the skill does + when to use it.
  Include all triggers HERE - the body loads AFTER triggering.
---
```

**Body:** Instructions in markdown, imperative form.

### Bundled Resources

| Directory | Purpose | Loaded into context? |
|-----------|---------|---------------------|
| `scripts/` | Executable code | No (runs directly) |
| `references/` | Documentation | Yes, on demand |
| `assets/` | Templates, images | No (used in output) |

## Skill Creation Process

### Step 1: Understand with Examples

Ask the user:
- What functionality should the skill support?
- Can you give concrete usage examples?
- What would a user say to trigger this skill?

### Step 2: Plan Reusable Contents

For each example, consider:
- How to execute it from scratch
- What scripts, references, assets would help with repeated workflows

### Step 3: Initialize the Skill

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

This creates:
- Skill directory with SKILL.md template
- Example resource directories: `scripts/`, `references/`, `assets/`

### Step 4: Edit the Skill

1. **Learn patterns**: See `references/workflows.md` and `references/output-patterns.md`
2. **Create resources**: Scripts, references, assets as needed
3. **Update SKILL.md**: Complete frontmatter and body

**Writing guidelines:**
- Use imperative/infinitive form
- Keep SKILL.md under 500 lines
- No duplication between SKILL.md and references

### Step 5: Package the Skill

```bash
python scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

This validates and creates a `.skill` file (zip format).

### Step 6: Iterate

1. Use the skill on real tasks
2. Note struggles or inefficiencies
3. Update SKILL.md or resources
4. Test again

## What NOT to Include

- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md
- Any auxiliary documentation not needed by the AI agent

**Principle:** A skill contains ONLY the information necessary for an AI agent to do the work.
