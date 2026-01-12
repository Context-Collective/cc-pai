# Système de Contexte

Le contexte permet à Claude de te connaître et de personnaliser ses réponses.

## Structure

```
pai/
├── context/
│   └── ME.md           # Ton profil personnel
├── state/
│   └── CURRENT.md      # Ton état de travail actuel
└── memory/
    └── *.md            # Sessions passées, apprentissages
```

## ME.md - Profil Personnel

Contient qui tu es, tes objectifs, ta façon de travailler.

### Sections recommandées

| Section | Contenu |
|---------|---------|
| Qui je suis | Rôle, expertise, stack |
| Mes objectifs | Court/long terme |
| Mes projets | Projets actifs |
| Comment je travaille | Préférences, outils, style |
| Mes conventions | Code, langue, formats |

### Bonnes pratiques

- **Concis** : 50-100 lignes max
- **Actionnable** : des instructions, pas une bio
- **Évolutif** : mettre à jour régulièrement

### Exemple de section critique

```markdown
### Avec l'IA
- Challenge-moi sans m'abrutir de questions
- Quand je commence à insulter : on se pose, on simplifie
- Ne JAMAIS me dire de souffler ou de me calmer
```

Ce type d'instruction change vraiment le comportement de Claude.

## CURRENT.md - État Actuel

Contient sur quoi tu travailles maintenant.

### Sections recommandées

| Section | Contenu |
|---------|---------|
| Focus actuel | Tâche en cours |
| Tâches | Liste des tâches |
| Contexte | Ce qu'il faut savoir pour reprendre |
| Blocages | Ce qui bloque |

### Usage

Utile pour :
- Reprendre après une pause
- Garder le fil entre sessions
- Prioriser

## Memory - Mémoire (à venir)

Format et usage à définir. Prévu pour :
- Capture de sessions importantes
- Décisions clés
- Apprentissages

## Chargement du Contexte

Le contexte est injecté via un [hook SessionStart](./hooks.md) au démarrage de chaque session.

```
Session start → Hook → Lit ME.md → Injecte dans contexte → Claude te connaît
```
