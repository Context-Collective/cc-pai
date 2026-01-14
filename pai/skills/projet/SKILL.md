---
name: projet
description: |
  Charge le contexte complet d'un projet : PM (tâches) + mémoire PAI + infos locales.
  USE WHEN user says: /projet [nom], projet [nom], travaillons sur [nom],
  ouvre [projet], switch [projet], on bosse sur [nom].
---

# Projet Loader

Charge le contexte d'un projet pour démarrer une session de travail.

## IMPORTANT

Cette skill est **rapide et ciblée**. Elle ne doit PAS :
- Explorer le code du projet
- Lire des fichiers de schema ou config
- Lancer des agents Explore
- Faire des recherches de patterns

Elle doit UNIQUEMENT :
1. Appeler l'API PM
2. Lire les sessions mémoire
3. Afficher un résumé structuré

## Workflow

### Étape 1 : Charger depuis PM

```bash
source pai/.env
curl -s -H "X-API-Key: $KOALITY_PM_API_KEY" "$KOALITY_PM_URL/api/projects"
```

Trouver le projet par nom dans la réponse JSON. Puis charger ses détails :

```bash
curl -s -H "X-API-Key: $KOALITY_PM_API_KEY" "$KOALITY_PM_URL/api/projects/$PROJECT_ID"
```

**Extraire les références** du projet, notamment :
- `local_path` : Chemin du dossier de travail (CRITIQUE pour la session)
- `github` : Repo si disponible
- Autres références utiles

### Étape 2 : Charger la mémoire PAI

```bash
grep -l -i "$PROJECT_NAME" pai/memory/sessions/*.md 2>/dev/null | head -3
```

Lire les 3 fichiers les plus récents (si trouvés).

### Étape 3 : Afficher le résumé

Format de sortie :

```markdown
## Projet: [Nom]

**Entité**: [nom de l'entité si disponible]

### Dossier de travail
`/chemin/vers/le/projet`

### Références
- GitHub: [url si disponible]
- Prod: [url si disponible]
- [autres références...]

### Tâches ([nombre])

| Urgence | Titre |
|---------|-------|
| high | Tâche 1 |
| normal | Tâche 2 |

### Dernière session mémoire
**[Date]** - [Titre]
> [Résumé 1-2 lignes]

### Décisions récentes
- [Si disponibles dans la mémoire]

---
*Dossier de travail: `/chemin/vers/le/projet`*
*Utilise `/capture` pour documenter.*
```

**IMPORTANT** : Le chemin `local_path` doit être clairement affiché et répété en footer.
C'est la référence pour toutes les opérations fichier de la session.

## Arguments

- `/projet biobreizh` → Charge Biobreizh
- `/projet koality-pm` → Charge Koality PM
- `/projet` → Demande quel projet

## Ce que cette skill NE FAIT PAS

- Lire le code source du projet
- Explorer l'architecture
- Analyser des fichiers techniques
- Proposer des modifications

Pour ça, l'utilisateur doit demander explicitement après avoir chargé le contexte.
