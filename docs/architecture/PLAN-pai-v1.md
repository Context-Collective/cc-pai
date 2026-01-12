# Plan : cc-pai - Framework PAI Générique

> Plan d'implémentation approuvé - Janvier 2026

## Vision Clarifiée

**cc-pai n'est PAS une PAI expurgée comme Miessler.**
**cc-pai EST un framework conçu dès le départ pour être générique.**

```
cc-pai = Structure + Outils + Processus pour créer SA propre PAI
```

---

## Les 3 Composants Essentiels d'une PAI

| Composant | Rôle | Sans ça... |
|-----------|------|-----------|
| **CONTEXT** | Qui tu es (goals, projects, methods) | L'IA ne te connaît pas |
| **MEMORY** | Ce qui s'est passé (sessions, learnings) | Chaque session repart de zéro |
| **SKILLS** | Ce qu'elle sait faire (expertise domaine) | Juste un chatbot générique |

**+ STATE** (optionnel mais utile) : Sur quoi tu travailles maintenant

---

## Architecture Future-Proof

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
│       └── pai-init/
│
├── install/                          # Templates pour initialisation
│   ├── ME.template.md
│   └── CURRENT.template.md
│
├── .claude/
│   ├── settings.json
│   └── skills -> ../pai/skills       # SYMLINK pour compatibilité Claude Code
│
├── CLAUDE.md                         # Instructions (lit pai/context/)
├── PRD.md                            # Spécification technique
└── README.md                         # Guide utilisateur
```

### Pourquoi cette structure ?

- `pai/` = contenu agnostique, prêt pour multi-provider futur
- `.claude/skills` = symlink pour que Claude Code reconnaisse les skills
- Séparation claire : config provider vs contenu PAI

### Séparation Framework vs Instance

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

**.gitignore** :
```gitignore
# PAI Instance (personnel)
pai/context/ME.md
pai/state/CURRENT.md
pai/memory/*
!pai/memory/.gitkeep
```

Permet de développer le framework ET d'utiliser sa PAI dans le même repo.

---

## Ce que cc-pai FOURNIT (générique)

| Élément | Description |
|---------|-------------|
| **Structure `pai/`** | Les bons dossiers au bon endroit |
| **Templates** | `ME.template.md`, `CURRENT.template.md` avec les bonnes questions |
| **skill-creator** | Outil pour créer ses skills |
| **pai-init** | Skill d'onboarding pour initialiser sa PAI |
| **CLAUDE.md** | Instructions qui utilisent le contexte |
| **Documentation** | Guide pour transformer cc-pai en SA PAI |

## Ce que l'UTILISATEUR fait (personnel)

1. Clone cc-pai
2. Lance `pai-init` ou remplit les templates manuellement
3. `ME.template.md` devient `ME.md` avec SON contenu
4. Crée SES skills selon ses besoins
5. → C'est maintenant SA PAI

---

## Templates

### pai/context/ME.template.md

```markdown
# Mon Contexte Personnel

## Qui je suis
<!-- Ton rôle, ton domaine, ton expertise -->

## Mes objectifs actuels
<!-- Ce que tu cherches à accomplir -->

## Mes projets en cours
<!-- Liste des projets actifs -->

## Comment je travaille
<!-- Tes préférences, méthodes, outils -->

## Mes conventions
<!-- Style de code, langue, formats préférés -->
```

### pai/state/CURRENT.template.md

```markdown
# État Actuel

## Focus actuel
<!-- Sur quoi tu travailles maintenant -->

## Tâches en cours
- [ ] ...

## Contexte de travail
<!-- Ce qu'il faut savoir pour reprendre -->

## Blocages / Questions
<!-- Ce qui te bloque -->
```

---

## Plan d'Implémentation

### Étape 1 : Restructurer l'architecture

| Action | Détail |
|--------|--------|
| Créer `pai/context/` | + `ME.template.md` |
| Créer `pai/memory/` | + `.gitkeep` |
| Créer `pai/state/` | + `CURRENT.template.md` |
| Déplacer `skills/` | De `.claude/skills/` vers `pai/skills/` |
| Créer symlink | `.claude/skills -> ../pai/skills` |
| Mettre à jour CLAUDE.md | Pointer vers `pai/context/` |

### Étape 2 : Créer le skill pai-init

Skill d'onboarding assisté par Claude :

**Déclencheur** : "initialise ma PAI", "configure ma PAI", "pai init"

**Workflow** :
```
1. Détecte si ME.md existe
   ├── Oui → propose mise à jour
   └── Non → lance onboarding complet

2. Pose les questions clés (conversationnel) :
   - Qui es-tu ? Ton rôle, domaine, expertise
   - Quels sont tes objectifs actuels ?
   - Sur quels projets tu travailles ?
   - Comment tu aimes travailler ? Préférences, outils
   - Conventions ? Style code, langue, formats

3. Génère les fichiers personnels :
   - pai/context/ME.md (à partir des réponses)
   - pai/state/CURRENT.md (état initial)

4. Confirme et explique la suite
```

**Output** : Fichiers `ME.md` et `CURRENT.md` personnalisés, prêts à l'emploi

### Étape 3 : Mettre à jour la documentation

- PRD.md avec la nouvelle architecture
- README.md avec le nouveau processus d'onboarding

### Étape 4 : Memory basique

- Définir le format de capture
- Créer un skill `memory-capture` (optionnel)

---

## Vérification

### Test de la structure
```bash
# Vérifier le symlink
ls -la .claude/skills
# Doit afficher: skills -> ../pai/skills
```

### Test fonctionnel
1. Remplir `pai/context/ME.md` avec du contenu test
2. Demander à Claude quelque chose qui utilise le contexte
3. Vérifier qu'il utilise bien les infos de ME.md

### Test d'onboarding
1. Partir d'un clone frais
2. Lancer le skill `pai-init`
3. Vérifier que ME.md est créé correctement

---

## Différence avec Miessler

| Miessler | cc-pai |
|----------|--------|
| PAI complète expurgée | Framework conçu générique |
| Structure complexe (6+ systèmes) | 3 composants essentiels |
| Difficile à reprendre | Facile à démarrer |
| Spécifique Claude | Future-proof (symlink) |
