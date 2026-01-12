# Hooks

Les hooks permettent d'exécuter du code en réponse aux événements de Claude Code.

## Hook SessionStart

Injecte automatiquement le contexte personnel (`ME.md`) au démarrage de chaque session.

### Configuration

**Fichier** : `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

### Script

**Fichier** : `.claude/hooks/load-context.sh`

```bash
#!/bin/bash
# Hook SessionStart : injecte le contexte personnel au démarrage

CONTEXT_FILE="$CLAUDE_PROJECT_DIR/pai/context/ME.md"

if [ -f "$CONTEXT_FILE" ]; then
  echo "=== CONTEXTE PERSONNEL ==="
  cat "$CONTEXT_FILE"
  echo "=== FIN CONTEXTE ==="
fi

exit 0
```

### Fonctionnement

1. Claude Code démarre une session
2. Le hook `SessionStart` s'exécute
3. Le script lit `pai/context/ME.md`
4. Le contenu est injecté dans le contexte de Claude
5. Claude te connaît dès le départ

### Variables disponibles

| Variable | Description |
|----------|-------------|
| `$CLAUDE_PROJECT_DIR` | Racine du projet |
| `$CLAUDE_ENV_FILE` | Fichier pour persister des variables d'env |

### Matchers SessionStart

Le hook peut être déclenché selon le type de démarrage :

| Matcher | Déclencheur |
|---------|-------------|
| `startup` | Nouvelle session |
| `resume` | `--resume`, `--continue`, `/resume` |
| `clear` | `/clear` |
| `compact` | Compaction auto ou manuelle |

### Sortie du hook

- **stdout** avec exit 0 → injecté comme contexte
- **JSON** avec `additionalContext` → injecté comme contexte
- **exit != 0** → erreur, hook ignoré

## Ressources

- [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
