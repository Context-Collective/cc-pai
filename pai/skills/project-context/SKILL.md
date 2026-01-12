---
name: project-context
description: |
  Charge le contexte d'un projet depuis la mémoire des sessions passées.
  USE WHEN user says: reprends [projet], contexte [projet], on en était où,
  qu'est-ce qu'on a fait sur [projet], résume le projet, project context.
---

# Project Context Loader

Charge et résume le contexte d'un projet depuis les sessions mémorisées.

## Workflow

### 1. Identifier le projet

**Si projet spécifié** : utiliser le nom donné
**Si non spécifié** : déduire du dossier courant ou demander

```bash
# Le projet peut être :
# - Un nom explicite ("Jeofun", "cc-pai", "Biobreizh")
# - Le dossier courant (basename du CLAUDE_PROJECT_DIR)
```

### 2. Rechercher les sessions liées

Chercher dans `pai/memory/sessions/` les fichiers mentionnant le projet :

```bash
# Recherche par nom de projet dans les fichiers de session
grep -l -i "$PROJECT_NAME" pai/memory/sessions/*.md 2>/dev/null | head -10
```

**Critères de pertinence :**
- Nom du projet dans le titre ou le résumé
- Mots-clés associés au projet
- Sessions les plus récentes en priorité

### 3. Charger le contexte

Pour chaque session pertinente (max 5 plus récentes) :
- Lire le fichier markdown
- Extraire : résumé, décisions, points clés, actions

### 4. Synthétiser et présenter

Produire un résumé structuré :

```markdown
## Contexte: [Nom du Projet]

### Dernière activité
[Date de la session la plus récente]

### État actuel
[Synthèse de où on en est]

### Décisions récentes
- [Liste des décisions importantes]

### Points clés à retenir
- [Informations importantes]

### Actions en suspens
- [ ] [Tâches non terminées]

### Sessions chargées
- [Liste des fichiers de session utilisés]
```

## Cas Particuliers

### Aucune session trouvée

```
Aucune session mémorisée pour "[projet]".

Options :
1. Vérifier le nom du projet
2. Lancer memory-manager pour capturer des sessions manquantes
3. Démarrer sans contexte historique
```

### Trop de sessions

Si > 10 sessions trouvées :
1. Prendre les 5 plus récentes
2. Mentionner qu'il y en a d'autres disponibles
3. Proposer de filtrer par période

### Projet nouveau

Si le projet existe mais pas de sessions :
```
Projet "[projet]" identifié mais aucune session en mémoire.
C'est un nouveau projet ou les sessions n'ont pas été capturées.
```

## Exemples d'Usage

**Reprise simple :**
> "reprends Jeofun"
→ Charge les dernières sessions Jeofun, résume l'état

**Contexte spécifique :**
> "on en était où sur le bug GPS de Jeofun ?"
→ Cherche sessions Jeofun + filtre sur "GPS" ou "bug"

**Sans nom de projet :**
> "on en était où ?"
→ Utilise le projet courant (déduit du dossier)

## Notes

- Les sessions sont dans `pai/memory/sessions/YYYY-MM-DD_HH-MM_SESSIONID.md`
- Le skill ne modifie rien, il lit seulement
- Pour capturer des sessions manquantes, utiliser `memory-manager`
