# Convention Documentation Projets

Standard pour organiser la documentation dans tous les projets.

## Structure recommandée

```
project/
├── docs/
│   ├── README.md              # Index auto-généré
│   ├── architecture/          # Docs stables
│   │   ├── overview.md
│   │   └── data-model.md
│   ├── devbooks/              # Docs vivantes (investigations)
│   │   ├── 01_sujet.md
│   │   └── 02_autre.md
│   ├── research/              # Analyses, comparatifs, veille
│   │   └── analyse-X.md
│   └── reference/             # Docs de référence (API, config)
│       └── api.md
└── src/
```

## Catégories

### `architecture/`
Documentation stable sur l'architecture du projet.
- Choix techniques validés
- Modèles de données
- Diagrammes
- Ne change pas souvent

### `devbooks/`
Documentation vivante liée au développement en cours.
- Investigations (comme un devbook Biobreizh)
- Roadmaps techniques
- Options de résolution avec avantages/inconvénients
- Évolue fréquemment

**Convention nommage** : `{numero}_{sujet}.md` (ex: `11_Alignement_IDs_API.md`)

### `research/`
Analyses et recherches.
- Comparatifs d'outils/libs
- État de l'art
- Notes de veille
- Recherches ponctuelles

### `reference/`
Documentation de référence.
- API endpoints
- Configuration
- Conventions de code
- Guide de contribution

## Index auto-généré

Le `README.md` à la racine de `docs/` est généré automatiquement par un script.

**Format** :
```markdown
# Documentation

## Architecture
- [Overview](architecture/overview.md) - Vue d'ensemble du projet

## Devbooks
- [Alignement IDs API](devbooks/11_Alignement_IDs_API.md) - Investigation front/API

## Research
- [Hiérarchie tâches](research/hierarchie-taches.md) - Patterns de sous-tâches
```

Le script scanne les fichiers et extrait le titre (premier `#`) pour la description.

## Où stocker quoi ?

| Type de contenu | Emplacement | Exemple |
|-----------------|-------------|---------|
| Choix d'architecture validé | `architecture/` | Choix de Next.js vs Remix |
| Investigation en cours | `devbooks/` | Options pour aligner des IDs |
| Comparatif de libs | `research/` | Analyse ORM Drizzle vs Prisma |
| Doc API | `reference/` | Endpoints REST |
| Specs fonctionnelles | `architecture/` ou racine | PRD, specs |

## Relation avec PM

La documentation reste dans le projet (versionnée avec le code).

PM peut **référencer** un doc via son path :
```
task.doc_ref = "docs/devbooks/11_Alignement_IDs_API.md"
```

Pas de duplication, juste un lien.

## Relation avec Mémoire PAI

- **Mémoire PAI** : Capture le narratif des sessions (ce qui s'est passé, pourquoi)
- **Docs projet** : Capture le contenu structuré (comment, options, décisions)

Les deux sont complémentaires :
- La mémoire dit "on a investigué l'alignement des IDs et documenté dans un devbook"
- Le devbook contient l'analyse détaillée
