# cc-pai - Framework PAI Open Source

> Spécification technique pour assistant IA de codage.
> Ce document définit cc-pai : un framework générique pour créer des PAI personnalisées.

---

## 1. OBJECTIF

### 1.1 Ce qu'est cc-pai

cc-pai est un **framework open source** permettant à quiconque de créer sa propre PAI (Personal AI Infrastructure).

**Workflow utilisateur :**
```
1. Clone cc-pai
2. Lance pai-init (ou remplit les templates manuellement)
3. Crée ses skills selon ses besoins
4. → C'est maintenant SA PAI
```

### 1.2 Principe Fondamental

> **L'architecture (scaffolding) compte plus que le modèle IA utilisé.**

### 1.3 Les 3 Composants Essentiels d'une PAI

| Composant | Rôle | Sans ça... |
|-----------|------|-----------|
| **CONTEXT** | Qui tu es (goals, projects, methods) | L'IA ne te connaît pas |
| **MEMORY** | Ce qui s'est passé (sessions, learnings) | Chaque session repart de zéro |
| **SKILLS** | Ce qu'elle sait faire (expertise domaine) | Juste un chatbot générique |

**+ STATE** : Sur quoi tu travailles maintenant

---

## 2. ARCHITECTURE

### 2.1 Structure du Projet

```
cc-pai/
├── pai/                              # Contenu PAI (AGNOSTIQUE PROVIDER)
│   ├── context/
│   │   └── ME.md                     # Profil utilisateur (gitignore)
│   ├── memory/
│   │   └── .gitkeep                  # Se remplit avec l'usage
│   ├── state/
│   │   └── CURRENT.md                # Travail en cours (gitignore)
│   └── skills/                       # Skills (format universel)
│       ├── skill-creator/
│       ├── pai-init/
│       └── meeting-notes/
│
├── install/                          # Templates pour initialisation
│   ├── ME.template.md
│   └── CURRENT.template.md
│
├── .claude/
│   ├── settings.local.json
│   └── skills -> ../pai/skills       # SYMLINK pour compatibilité Claude Code
│
├── docs/                             # Documentation projet
├── CLAUDE.md                         # Instructions pour Claude Code
├── PRD.md                            # Ce document
└── README.md                         # Guide utilisateur
```

### 2.2 Pourquoi cette structure ?

- `pai/` = contenu agnostique, prêt pour multi-provider futur
- `.claude/skills` = symlink pour que Claude Code reconnaisse les skills
- Séparation claire : config provider vs contenu PAI

### 2.3 Framework vs Instance

```
FRAMEWORK (versionné, distribué) :
├── install/ME.template.md
├── install/CURRENT.template.md
├── pai/skills/*
└── pai/memory/.gitkeep

INSTANCE (gitignore, personnel) :
├── pai/context/ME.md
├── pai/state/CURRENT.md
└── pai/memory/*.md
```

Permet de développer le framework ET d'utiliser sa PAI dans le même repo.

---

## 3. SPÉCIFICATION DES COMPOSANTS

### 3.1 Context (pai/context/)

**ME.md** - Profil de l'utilisateur

| Section | Contenu |
|---------|---------|
| Qui je suis | Rôle, domaine, expertise |
| Mes objectifs | Ce qu'on cherche à accomplir |
| Mes projets | Projets actifs |
| Comment je travaille | Préférences, méthodes, outils |
| Mes conventions | Style code, langue, formats |

### 3.2 State (pai/state/)

**CURRENT.md** - État de travail actuel

| Section | Contenu |
|---------|---------|
| Focus actuel | Tâche en cours |
| Tâches | Liste des tâches |
| Contexte | Ce qu'il faut savoir pour reprendre |
| Blocages | Ce qui bloque |

### 3.3 Memory (pai/memory/)

Format à définir. Capture des sessions, décisions, apprentissages.

### 3.4 Skills (pai/skills/)

Voir section 4.

---

## 4. SPÉCIFICATION DES SKILLS

### 4.1 Structure Minimale

```
{skill-name}/
└── SKILL.md    # Seul fichier requis
```

### 4.2 Structure Complète

```
{skill-name}/
├── SKILL.md                   # REQUIS
├── scripts/                   # Optionnel
│   └── {script}.py
├── references/                # Optionnel
│   └── {reference}.md
└── assets/                    # Optionnel
    └── {asset}.{ext}
```

### 4.3 SKILL.md - Spécification

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

### 4.4 Règles de Validation

#### Champ `name`

| Règle | Valide | Invalide |
|-------|--------|----------|
| hyphen-case | `pdf-analyzer` | `pdfAnalyzer` |
| ≤ 64 caractères | `my-skill` | (trop long) |
| `a-z`, `0-9`, `-` | `data-2024` | `data_2024` |

#### Champ `description`

| Règle | Détail |
|-------|--------|
| Non vide | Requis |
| ≤ 1024 caractères | Limite stricte |
| 3ème personne | "Processes..." pas "I process..." |

#### Body

| Règle | Détail |
|-------|--------|
| < 500 lignes | Performance optimale |
| Références à 1 niveau | SKILL.md → ref.md (pas d'imbrication) |

---

## 5. SKILLS DU FRAMEWORK

### 5.1 skill-creator

Skill méta pour créer d'autres skills.

**Déclencheur** : "crée un skill", "nouveau skill"

**Scripts** :
- `init_skill.py` - Initialise la structure
- `quick_validate.py` - Valide la structure

### 5.2 pai-init

Skill d'onboarding assisté.

**Déclencheur** : "initialise ma PAI", "configure ma PAI", "pai init"

**Workflow** :
1. Détecte si ME.md existe
2. Pose les questions clés (conversationnel)
3. Génère ME.md et CURRENT.md personnalisés
4. Confirme et explique la suite

### 5.3 meeting-notes

Skill exemple pour traiter des notes de réunion.

**Déclencheur** : "notes de réunion", "résume la réunion"

---

## 6. ROADMAP

### Étape 1 : Architecture PAI ✅
- [x] Structure `pai/` avec context, memory, state, skills
- [x] Symlink `.claude/skills -> ../pai/skills`
- [x] Templates ME.template.md et CURRENT.template.md
- [x] Séparation framework/instance avec .gitignore
- [x] Documentation (docs/guides/, docs/reference/)

### Étape 2 : Skills de base ✅
- [x] skill-creator fonctionnel
- [x] pai-init pour onboarding assisté
- [x] meeting-notes comme exemple
- [x] memory-manager (bonus - rattrapage manuel)

### Étape 3 : Memory ✅
- [x] Définir le format de capture (docs/reference/memory.md)
- [x] Hook SessionEnd pour capture automatique
- [x] Skill memory-manager pour rattrapage manuel

### Futures étapes (hors v1)
- Hooks d'automatisation
- Agents personnalisés
- Multi-provider

---

## 7. CONVENTIONS

### 7.1 Nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Skill | hyphen-case | `pdf-analyzer` |
| Script | snake_case | `extract_text.py` |

### 7.2 Langues

| Contexte | Langue |
|----------|--------|
| Code, frontmatter | Anglais |
| Documentation utilisateur | Français |

### 7.3 Anti-Patterns

- ❌ README.md dans les skills
- ❌ SKILL.md > 500 lignes
- ❌ Références imbriquées
- ❌ Description en 1ère personne

---

## 8. RÉFÉRENCES

- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Daniel Miessler PAI](https://github.com/danielmiessler/Personal_AI_Infrastructure)
