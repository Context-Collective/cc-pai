# Guide de Démarrage

Ce guide t'accompagne pour créer ta PAI personnelle.

## Qu'est-ce qu'une PAI ?

Une **Personal AI Infrastructure** (PAI) est une IA qui :
- **Te connaît** : ton rôle, tes projets, ta façon de travailler
- **Se souvient** : des sessions passées, des décisions
- **S'améliore** : avec des skills adaptés à tes besoins

Sans PAI, chaque session Claude repart de zéro. Avec une PAI, Claude est ton assistant personnalisé.

## Prérequis

- [Claude Code](https://claude.ai/code) installé
- Python 3.8+ (pour les scripts des skills)
- Git

## Installation

```bash
git clone https://github.com/Context-Collective/cc-pai.git
cd cc-pai
```

## Initialisation

### Option 1 : Onboarding assisté (recommandé)

Ouvre Claude Code dans le dossier cc-pai et dis :

> "Initialise ma PAI"

Claude va te poser des questions sur :
- Qui tu es (rôle, expertise)
- Tes objectifs
- Tes projets en cours
- Ta façon de travailler
- Tes conventions

Il génère ensuite tes fichiers de contexte personnalisés.

### Option 2 : Configuration manuelle

```bash
cp install/ME.template.md pai/context/ME.md
cp install/CURRENT.template.md pai/state/CURRENT.md
```

Édite `pai/context/ME.md` avec tes informations.

## Vérifier que ça marche

Ouvre une **nouvelle session** Claude Code et pose une question où ton contexte devrait influencer la réponse :

> "Comment structurer un nouveau projet ?"

Si Claude mentionne ta stack ou tes préférences, c'est bon. Sinon, vérifie que `pai/context/ME.md` existe.

## Structure de ta PAI

```
pai/
├── context/
│   └── ME.md           # Ton profil (qui tu es, comment tu travailles)
├── state/
│   └── CURRENT.md      # Ton focus actuel (optionnel)
├── memory/
│   └── ...             # Sessions passées (à venir)
└── skills/
    ├── skill-creator/  # Créer des skills
    ├── pai-init/       # Initialisation
    └── meeting-notes/  # Exemple de skill
```

## Créer ton premier skill

Dis à Claude :

> "Crée un skill pour [décris ton usage]"

Exemples :
- "Crée un skill pour générer des rapports de test"
- "Crée un skill pour formater mes commits git"
- "Crée un skill pour analyser des PDF"

Claude utilise le skill `skill-creator` pour générer la structure.

## Mettre à jour ton contexte

Quand tes projets ou objectifs changent, édite `pai/context/ME.md`.

**Bonnes pratiques** :
- Garde-le concis (50-100 lignes)
- Focus sur ce qui influence les réponses de Claude
- Mets à jour régulièrement

## Section critique : "Avec l'IA"

La section la plus importante de ton `ME.md` est comment tu veux que Claude interagisse avec toi :

```markdown
### Avec l'IA
- Challenge-moi sans m'abrutir de questions
- Quand je commence à m'énerver : on simplifie
- Ne JAMAIS me dire de me calmer
```

Ces instructions changent vraiment le comportement de Claude.

## Prochaines étapes

- Explore les [skills inclus](../reference/skills.md)
- Comprends le [système de contexte](../reference/context.md)
- Apprends comment fonctionnent les [hooks](../reference/hooks.md)
