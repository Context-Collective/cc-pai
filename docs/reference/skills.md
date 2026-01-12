# Skills

Les skills étendent les capacités de Claude avec des connaissances spécialisées.

## Structure

```
pai/skills/{skill-name}/
├── SKILL.md            # Requis - Instructions
├── scripts/            # Optionnel - Scripts exécutables
├── references/         # Optionnel - Documentation complémentaire
└── assets/             # Optionnel - Fichiers utilisés en sortie
```

## SKILL.md

### Format

```yaml
---
name: skill-name
description: |
  Description en 3ème personne.
  Inclut CE QUE fait le skill et QUAND l'utiliser.
---

# Skill Name

[Instructions en markdown]
```

### Règles de validation

**Champ `name`** :
- hyphen-case (`pdf-analyzer`, pas `pdfAnalyzer`)
- ≤ 64 caractères
- Caractères autorisés : `a-z`, `0-9`, `-`

**Champ `description`** :
- Non vide, ≤ 1024 caractères
- 3ème personne ("Processes..." pas "I process...")
- Inclure les déclencheurs (quand utiliser le skill)

**Body** :
- < 500 lignes (performance)
- Références à 1 niveau max (pas d'imbrication)

## Routing automatique

Claude Code route automatiquement vers les skills selon la `description` du frontmatter. Pas besoin de routing manuel.

```yaml
description: |
  Extracts action items from meeting notes.
  USE WHEN user mentions meeting notes, résumer réunion, notes de réunion.
```

Les mots-clés dans la description servent de déclencheurs.

## Skills inclus

### skill-creator

Créer de nouveaux skills.

**Déclencheur** : "crée un skill", "nouveau skill"

### pai-init

Initialiser la PAI (onboarding).

**Déclencheur** : "initialise ma PAI", "configure ma PAI"

### meeting-notes

Extraire actions et décisions des notes de réunion.

**Déclencheur** : "notes de réunion", "résume la réunion"

## Créer un skill

```bash
python3 pai/skills/skill-creator/scripts/init_skill.py <nom-skill> --path pai/skills/
```

Ou demande simplement à Claude : "Crée un skill pour [usage]"

## Ressources

- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
