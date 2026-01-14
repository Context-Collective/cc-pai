---
name: doc-manager
description: |
  Gere la documentation d'un projet : structure, coherence docs/code, liens internes.
  USE WHEN user says: "audit la doc", "verifie la doc", "doc manager", "organise la doc",
  "doc obsolete", "liens casses", "index manquant", "doc vs code".
---

# Doc Manager

Gestionnaire de documentation projet avec 3 modes : analyse structure, audit coherence, corrections.

Supporte les projets simples ET les monorepos.

## Modes

| Mode | Commande | Description |
|------|----------|-------------|
| **analyze** | `/doc-manager` | Structure des fichiers, detection type projet |
| **audit** | `/doc-manager audit` | Coherence docs↔code + docs↔docs |
| **fix** | `/doc-manager fix` | Applique les corrections proposees |

---

## Philosophie : Structure Flat

**Principe** : Une doc centralisee, plate, avec nommage intelligent.

### Projet simple

```
projet/
├── docs/
│   ├── INDEX.md              # Auto-genere
│   ├── architecture.md       # Type dans le nom
│   ├── api-reference.md
│   ├── devbook-fix-auth.md
│   └── spec-game-engine.md
├── CLAUDE.md
└── README.md
```

### Monorepo

```
monorepo/
├── docs/
│   ├── INDEX.md
│   ├── creator/              # Scope = sous-dossier
│   │   ├── architecture.md
│   │   └── api-reference.md
│   ├── storybook/
│   │   └── navigation.md
│   └── shared/
│       └── design-system.md
├── package-a/                # Code only
├── package-b/                # Code only
├── CLAUDE.md
└── README.md
```

### Convention de nommage

```
[prefixe-optionnel-]nom-descriptif.md

architecture.md          # Evident
api-users.md             # Reference API
devbook-fix-auth.md      # Investigation/debug
spec-game-engine.md      # Specification
research-perf-optim.md   # Analyse/recherche
```

Le type est dans le nom, pas dans l'arborescence.

---

## Aide contextuelle

Si l'utilisateur tape `/doc-manager` sans argument, afficher cette aide :

```markdown
## Doc Manager

Gestionnaire de documentation pour tes projets.

| Commande | Description |
|----------|-------------|
| `/doc-manager [path]` | Analyse structure (fichiers mal places) |
| `/doc-manager audit [path]` | Audit complet (code↔doc + liens) |
| `/doc-manager fix` | Applique les corrections de l'audit |

**Exemples :**
- `/doc-manager /Users/fabien/projets/biobreizh`
- `/doc-manager audit /Users/fabien/projets/jeofun25`

Quel projet veux-tu analyser ?
```

Puis demander le chemin avec AskUserQuestion.

---

## Detection du type de projet

Au lancement, detecter automatiquement :

### Indicateurs monorepo

- `package.json` avec `"workspaces"`
- `pnpm-workspace.yaml`
- `lerna.json`
- Plusieurs dossiers avec `package.json` enfants
- Patterns : `packages/`, `apps/`, `libs/`

### Si monorepo detecte

1. Lister les packages/scopes trouves
2. Verifier si `docs/` centralise existe
3. Detecter docs dispersees (dans chaque package)
4. Proposer centralisation si necessaire

### Flow interactif (monorepo)

```markdown
Monorepo detecte (3 packages: creator, storybook, engine)

Que veux-tu analyser ?
○ Vue globale (tout le monorepo)
○ Un scope specifique → [liste]
○ Docs dispersees uniquement (centralisation)
```

Utiliser AskUserQuestion pour le choix.

---

## Mode 1 : Analyze (par defaut)

**Declencheur** : `/doc-manager` ou `/doc-manager analyze`

### Workflow

1. Resoudre le chemin du projet
2. Detecter type (simple vs monorepo)
3. Si monorepo : demander le scope
4. Executer le script d'analyse :
   ```bash
   python3 pai/skills/doc-manager/scripts/analyze_docs.py "/path/to/project"
   ```
5. Afficher le rapport structure

### Output projet simple

```markdown
## Analyse Structure

**Projet**: [nom]
**Type**: Projet simple

### Fichiers a centraliser
| Source | Destination | Action |
|--------|-------------|--------|
| /FIX_BUG.md | docs/devbook-fix-bug.md | move+rename |
| /ARCHITECTURE.md | docs/architecture.md | move+rename |

### Nommage a corriger
| Fichier | Probleme | Suggestion |
|---------|----------|------------|
| docs/API_USERS.md | uppercase | api-users.md |

Tape `/doc-manager audit` pour verifier la coherence.
```

### Output monorepo

```markdown
## Analyse Structure

**Projet**: [nom]
**Type**: Monorepo (3 scopes: creator, storybook, shared)

### Vue globale
| Scope | Docs centralisees | Docs dispersees |
|-------|-------------------|-----------------|
| creator | 2 | 3 (a centraliser) |
| storybook | 0 | 1 (a centraliser) |
| shared | 5 | 0 |

### Docs dispersees a centraliser
| Source | Destination |
|--------|-------------|
| creator/docs/api.md | docs/creator/api.md |
| storybook/README-ARCH.md | docs/storybook/architecture.md |

### Docs sans scope clair
| Fichier | Suggestion |
|---------|------------|
| docs/old-notes.md | Archiver ou assigner scope |

Tape `/doc-manager audit` pour verifier la coherence.
```

---

## Mode 2 : Audit

**Declencheur** : `/doc-manager audit`

### Workflow

Lance 3 sous-agents en parallele via l'outil Task :

#### Agent 1 : doc-code-sync (Explore)

Compare la documentation avec le code source.

```
Analyse la coherence entre documentation et code du projet [PATH].

Pour un monorepo, analyser le scope [SCOPE] si specifie.

Cherche dans docs/ (ou docs/[scope]/) et compare avec src/ :
1. Endpoints API documentes mais absents du code
2. Endpoints dans le code mais non documentes
3. Signatures de fonctions incorrectes dans la doc
4. Composants documentes mais supprimes

Retourne un rapport JSON :
{
  "scope": "[scope ou null]",
  "undocumented": [{"type": "endpoint", "location": "src/api/users.ts:45", "signature": "POST /users"}],
  "obsolete": [{"doc": "docs/api-reference.md:120", "reason": "fonction supprimee"}],
  "incorrect": [{"doc": "docs/api-reference.md:50", "expected": "GET /users/:id", "actual": "GET /users/{id}"}]
}
```

#### Agent 2 : doc-coherence (Explore)

Verifie la coherence interne des docs.

```
Analyse la coherence interne de la documentation du projet [PATH].

Pour un monorepo, inclure les liens cross-scope.

Verifie :
1. Liens internes casses (docs/xxx.md → docs/yyy.md qui n'existe pas)
2. Liens cross-scope casses (docs/creator/x.md → docs/shared/y.md)
3. Doublons potentiels (fichiers avec contenu similaire >70%)
4. INDEX.md manquant ou incomplet
5. Fichiers orphelins (non references nulle part)
6. Docs dispersees (hors de docs/ centralisee)

Retourne un rapport JSON :
{
  "broken_links": [{"file": "docs/overview.md", "line": 42, "target": "docs/old-api.md"}],
  "cross_scope_issues": [{"file": "docs/creator/api.md", "target": "docs/storybook/types.md", "status": "missing"}],
  "duplicates": [{"files": ["docs/api.md", "docs/creator/api.md"], "similarity": 0.85}],
  "missing_index": true,
  "orphans": ["docs/old-notes.md"],
  "dispersed": ["creator/docs/local.md", "storybook/ARCHITECTURE.md"]
}
```

#### Agent 3 : structure-analyzer (script Python)

Reprend l'analyse de structure (mode analyze) via le script existant.

### Execution parallele

```python
# Lancer les 3 agents en parallele
Task(subagent_type="Explore", prompt="[doc-code-sync prompt]")
Task(subagent_type="Explore", prompt="[doc-coherence prompt]")
Bash("python3 .../analyze_docs.py [PATH]")
```

### Output combine

```markdown
## Audit Documentation

**Projet**: [nom]
**Type**: [simple|monorepo]
**Date**: [date]

### 1. Structure
- X fichiers a centraliser
- X fichiers a renommer
- Scopes detectes : [liste si monorepo]

### 2. Sync Code ↔ Docs
| Scope | Type | Details | Severite |
|-------|------|---------|----------|
| creator | Non documente | POST /api/users | haute |
| shared | Doc obsolete | docs/shared/old-api.md | moyenne |

### 3. Coherence Docs
| Type | Details |
|------|---------|
| Lien casse | docs/overview.md:42 → docs/old-api.md |
| Cross-scope | docs/creator/api.md → docs/storybook/types.md (missing) |
| Doublon | docs/api.md ≈ docs/creator/api.md (85%) |
| Dispersee | creator/docs/local.md (hors docs/) |

### Actions recommandees (par priorite)

**Haute**
1. Centraliser docs dispersees
2. Corriger liens casses

**Moyenne**
3. Fusionner doublons
4. Documenter APIs manquantes

**Basse**
5. Generer INDEX.md
6. Renommer fichiers (kebab-case)

Tape `/doc-manager fix` pour appliquer les corrections auto.
```

---

## Mode 3 : Fix

**Declencheur** : `/doc-manager fix`

**Prerequis** : Avoir execute `audit` avant.

### Ce qui est corrige automatiquement

| Action | Auto | Manuel |
|--------|------|--------|
| Centraliser docs dispersees | Oui | - |
| Renommer (kebab-case) | Oui | - |
| Corriger liens internes | Oui | - |
| Generer INDEX.md | Oui | - |
| Archiver doublons | Oui | - |
| Creer structure scopes | Oui | - |
| Documenter API manquante | - | Oui |
| Corriger signatures | - | Oui |
| Assigner scope ambigu | - | Oui |

### Workflow

1. Afficher les actions automatiques prevues
2. Demander confirmation globale
3. Executer les corrections
4. Mettre a jour les liens apres deplacements
5. Lister ce qui reste a faire manuellement

### Output

```markdown
## Corrections appliquees

### Auto (fait)
- 4 fichiers centralises vers docs/
- 2 scopes crees (creator/, storybook/)
- 3 liens corriges (apres deplacements)
- INDEX.md genere (15 entrees)
- 1 doublon archive

### Manuel (a faire)
- [ ] Documenter POST /api/users (src/api/users.ts:45)
- [ ] Assigner scope a docs/old-notes.md
- [ ] Verifier fusion docs/api.md + docs/creator/api.md

Log complet : docs/_archive/doc-manager-[date].md
```

---

## Generation INDEX.md

### Projet simple

```markdown
# Documentation

## Architecture
- [architecture.md](./architecture.md) - Vue d'ensemble du systeme

## API Reference
- [api-users.md](./api-users.md) - Endpoints utilisateurs
- [api-auth.md](./api-auth.md) - Authentification

## Devbooks
- [devbook-fix-auth.md](./devbook-fix-auth.md) - Resolution bug auth

---
*Genere automatiquement par doc-manager*
```

### Monorepo

```markdown
# Documentation

## Creator
- [creator/architecture.md](./creator/architecture.md) - Architecture web platform
- [creator/api-reference.md](./creator/api-reference.md) - API endpoints

## Storybook
- [storybook/navigation.md](./storybook/navigation.md) - Navigation mobile

## Shared
- [shared/design-system.md](./shared/design-system.md) - Composants partages
- [shared/types.md](./shared/types.md) - Types communs

---
*Genere automatiquement par doc-manager*
```

---

## Ce que cette skill NE FAIT PAS

- Rediger de la documentation
- Modifier le code source
- Supprimer sans archiver
- Forcer une structure si le projet en a deja une coherente
- Decider du scope a la place de l'utilisateur

---

## Fichiers ignores

**Toujours ignores** :
- `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`
- `package.json`, `tsconfig.json`, configs standard
- `README.md`, `CLAUDE.md`, `LICENSE.md` a la racine
- Fichiers dans `_archive/`
