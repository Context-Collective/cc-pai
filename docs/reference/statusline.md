# Status Line PAI

La status line affiche des informations contextuelles en bas du terminal Claude Code.

## Aperçu

```
[PAI:Opus] main | 23% | 15s
```

| Élément | Description |
|---------|-------------|
| `[PAI:Opus]` | Indicateur PAI + modèle actif |
| `main` | Branche git courante |
| `23%` | Utilisation du contexte |
| `15s` | Nombre de sessions en mémoire |

## Couleurs

| Élément | Couleur | Condition |
|---------|---------|-----------|
| `[PAI]` | Cyan bold | Toujours |
| Modèle | Magenta | Toujours |
| Branche | Vert | Toujours |
| Context | Vert | < 50% |
| Context | Jaune | 50-80% |
| Context | Rouge | > 80% |
| Sessions | Jaune | Toujours |

## Configuration

**Fichier :** `.claude/settings.json`

```json
{
  "statusLine": {
    "type": "command",
    "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/statusline.sh"
  }
}
```

**Script :** `.claude/hooks/statusline.sh`

## Données Disponibles

Le script reçoit un JSON via stdin avec :

```json
{
  "model": {
    "display_name": "Opus",
    "id": "claude-opus-4-5-20251101"
  },
  "workspace": {
    "current_dir": "/path/to/project",
    "project_dir": "/path/to/project"
  },
  "context_window": {
    "context_window_size": 200000,
    "current_usage": {
      "input_tokens": 15000,
      "cache_creation_input_tokens": 5000,
      "cache_read_input_tokens": 2000
    }
  }
}
```

## Personnalisation

Pour modifier l'affichage, éditer `.claude/hooks/statusline.sh`.

**Ajouter une info :**
1. Extraire la donnée avec `jq`
2. L'ajouter à la variable `OUTPUT`

**Changer les couleurs :**
```bash
# Codes ANSI disponibles
RESET="\033[0m"
BOLD="\033[1m"
DIM="\033[2m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
```

## Dépendances

- `jq` - Parser JSON
- `git` - Pour la branche (optionnel)

## Dépannage

**La statusline ne s'affiche pas :**
1. Vérifier que le script est exécutable : `chmod +x .claude/hooks/statusline.sh`
2. Tester manuellement : `echo '{}' | .claude/hooks/statusline.sh`
3. Vérifier `jq` installé : `which jq`

**Erreur de parsing :**
- Le script doit produire exactement une ligne en sortie
- Pas de retour à la ligne supplémentaire
