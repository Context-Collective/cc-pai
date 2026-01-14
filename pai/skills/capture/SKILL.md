---
name: capture
description: |
  Capture manuelle d'informations vers PM, mémoire PAI, ou documentation projet.
  USE WHEN user says: /capture [type], capture ça, note cette décision,
  ajoute une tâche, j'ai un blocage, mémorise, capture dans la doc.
---

# Capture

Capture manuelle d'informations pendant une session de travail.

## Modes de capture

| Mode | Destination | Usage |
|------|-------------|-------|
| `decision` | Mémoire PAI | Décision prise pendant la session |
| `tache` | PM (task) | Nouvelle tâche à faire |
| `blocage` | PM (task) | Tâche bloquée avec contexte |
| `note` | Mémoire PAI | Note libre à retenir |
| `idee` | PM (idea) | Idée à évaluer plus tard |
| `doc` | Projet cible | Documentation du projet |

## Syntaxe

```
/capture decision [description]
/capture tache [titre] --urgency [low|normal|high|critical] --project [nom]
/capture blocage [description]
/capture note [contenu]
/capture idee [contenu]
```

## Workflows

### /capture decision

Enregistre une décision dans la session mémoire courante.

**Action :**
1. Identifier la session courante dans `pai/memory/sessions/`
2. Ajouter la décision à la section `## Décisions`

```markdown
## Décisions
- [Existantes...]
- [NOUVELLE] Description de la décision
```

**Exemple :**
```
/capture decision On utilise l'option A (parent_id) pour les sous-tâches
```

### /capture tache

Crée une tâche dans PM.

**Action :**
```bash
source pai/.env
curl -X POST -H "X-API-Key: $KOALITY_PM_API_KEY" \
  -H "Content-Type: application/json" \
  "$KOALITY_PM_URL/api/tasks" \
  -d '{
    "title": "[titre]",
    "urgency": "[urgency]",
    "status": "todo",
    "project_ids": ["[project_id]"]
  }'
```

**Exemple :**
```
/capture tache Implémenter le endpoint sous-tâches --urgency high --project koality-pm
```

### /capture blocage

Crée une tâche bloquée dans PM avec le contexte.

**Action :**
1. Créer une tâche avec description détaillée
2. Marquer comme `critical` ou `high`
3. Inclure le contexte du blocage

```bash
source pai/.env
curl -X POST -H "X-API-Key: $KOALITY_PM_API_KEY" \
  -H "Content-Type: application/json" \
  "$KOALITY_PM_URL/api/tasks" \
  -d '{
    "title": "BLOCAGE: [description courte]",
    "description": "[contexte détaillé du blocage]",
    "urgency": "critical",
    "status": "todo",
    "project_ids": ["[project_id]"]
  }'
```

**Exemple :**
```
/capture blocage Impossible de tester l'API - VirtualHost pas configuré
```

### /capture note

Ajoute une note libre à la session mémoire.

**Action :**
1. Identifier la session courante
2. Ajouter à une section `## Notes` (créer si n'existe pas)

**Exemple :**
```
/capture note Le client préfère l'option sans modification WordPress
```

### /capture idee

Crée une idée brute dans PM pour évaluation ultérieure.

**Action :**
```bash
source pai/.env
curl -X POST -H "X-API-Key: $KOALITY_PM_API_KEY" \
  -H "Content-Type: application/json" \
  "$KOALITY_PM_URL/api/ideas" \
  -d '{
    "content": "[contenu de l idée]",
    "status": "raw"
  }'
```

**Exemple :**
```
/capture idee Créer un dashboard temps réel des tâches avec websockets
```

### /capture doc

Capture intelligente vers la documentation du projet.

**Syntaxe :**
```
/capture doc [projet]
/capture doc                  # Demande le projet si non spécifié
"capture ça dans la doc"      # Déclencheur naturel
```

**Workflow intelligent :**

1. **Analyser le contexte** de la conversation récente
   - Quelles infos viennent d'être partagées ?
   - Commandes ? Config ? Architecture ? Investigation ?

2. **Catégoriser automatiquement**
   | Contenu détecté | Catégorie | Dossier |
   |-----------------|-----------|---------|
   | Commandes shell, SSH, Docker | reference | `docs/reference/` |
   | Endpoints API, config | reference | `docs/reference/` |
   | Choix technique validé | architecture | `docs/architecture/` |
   | Exploration d'options | devbook | `docs/devbooks/` |
   | Analyse, comparatif | research | `docs/research/` |

3. **Proposer un fichier** avec nom intelligent
   - Basé sur le contenu (ex: "server-commands.md", "api-endpoints.md")
   - Dans le bon dossier

4. **Formater selon la catégorie**
   - `reference/` → Factuel, listes, code blocks
   - `architecture/` → Contexte, décision, justification
   - `devbooks/` → Problème, options, pour/contre
   - `research/` → Analyse structurée

5. **Montrer le résultat** et demander confirmation simple

**Exemple :**

```
Utilisateur: "capture ça dans la doc de koality-pm"

Claude analyse la conversation et détecte : commandes serveur SSH/Docker

Claude:
┌─────────────────────────────────────────────────────┐
│ docs/reference/server-commands.md                   │
├─────────────────────────────────────────────────────┤
│ # Commandes Serveur                                 │
│                                                     │
│ ## Connexion                                        │
│ ```bash                                             │
│ ssh ssh_pm_koality@62.210.212.3                     │
│ cd /var/www/.../koality-pm                          │
│ ```                                                 │
│                                                     │
│ ## Logs                                             │
│ ```bash                                             │
│ docker compose logs app --tail=50                   │
│ ```                                                 │
│                                                     │
│ ## Maintenance                                      │
│ ```bash                                             │
│ docker compose restart                              │
│ docker exec koality-pm-app-1 bun run db:push        │
│ ```                                                 │
│                                                     │
│ ---                                                 │
│ *Source: session 2026-01-14*                        │
└─────────────────────────────────────────────────────┘

Créer ce fichier ? (oui/modifier/non)
```

**Si le fichier existe déjà :**
- Proposer de compléter (ajouter une section)
- Ou remplacer une section existante
- Montrer le diff

**Projet cible :**
- Si argument fourni : utiliser ce chemin
- Si `/projet` actif : utiliser ce projet
- Sinon : demander le chemin

**Action finale :**
```python
# Écrire dans le projet cible (PAS dans cc-pai)
Write(file_path=f"{project_path}/docs/{category}/{filename}")
```

## Contexte automatique

Si un projet est actif (via `/projet`), les captures héritent automatiquement :
- `project_id` pour les tâches
- Tag projet pour les notes mémoire

## Confirmation

Après chaque capture, confirmer :
```
✓ [Type] capturé : "[résumé]"
  → [Destination] : [fichier ou ID PM]
```

## Notes

- Cette skill **modifie** la mémoire PAI et/ou PM
- Les captures `decision` et `note` enrichissent la session courante
- Les captures `tache`, `blocage`, `idee` créent dans PM
- Sans projet actif, demander confirmation avant création PM
