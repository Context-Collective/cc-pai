# cc-pai

**Crée ta PAI (Personal AI Infrastructure) avec Claude Code.**

Une PAI est une IA qui te connaît, se souvient, et s'améliore avec toi.

## Installation

```bash
git clone https://github.com/Context-Collective/cc-pai.git
cd cc-pai
```

**Prérequis** : [Claude Code](https://claude.ai/code), Python 3.8+

## Démarrage

Lance Claude Code dans le projet et dis :

> "Initialise ma PAI"

Claude te pose les bonnes questions et configure ta PAI.

**Ou manuellement** :
```bash
cp install/ME.template.md pai/context/ME.md
cp install/CURRENT.template.md pai/state/CURRENT.md
# Édite les fichiers avec ton contexte
```

## Utilisation

Une fois initialisé, Claude te connaît. Il utilise ton contexte pour personnaliser ses réponses.

### Créer un skill

> "Crée un skill pour [ton usage]"

### Mettre à jour ton contexte

Édite `pai/context/ME.md` quand tes projets ou objectifs changent.

## Structure

```
pai/
├── context/ME.md      # Qui tu es
├── state/CURRENT.md   # Ce sur quoi tu travailles
├── memory/            # Sessions passées (à venir)
└── skills/            # Tes capacités
```

## Documentation

- [Guide de démarrage](docs/guides/getting-started.md)
- [Référence Skills](docs/reference/skills.md)
- [Référence Hooks](docs/reference/hooks.md)
- [Système de Contexte](docs/reference/context.md)
- [Système de Mémoire](docs/reference/memory.md)
- [Status Line](docs/reference/statusline.md)

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT - [Context Collective](https://github.com/Context-Collective)
