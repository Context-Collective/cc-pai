# Système de Mémoire

La mémoire permet de conserver les sessions importantes et d'apprendre des interactions passées.

## Architecture

```
pai/memory/
├── sessions/           # Résumés de sessions auto-générés
│   └── 2026-01-11_22-30_abc123.md
└── .gitkeep
```

## Capture automatique

Chaque session est automatiquement résumée à la fin via un hook `SessionEnd`.

### Comment ça marche

```
Session se termine
    ↓
Hook SessionEnd s'exécute
    ↓
Claude Code headless (haiku) résume la session
    ↓
Fichier markdown créé dans pai/memory/sessions/
```

### Ce qui est capturé

| Élément | Description |
|---------|-------------|
| **Titre** | Sujet principal de la session |
| **Résumé** | 2-3 phrases |
| **Décisions** | Liste des décisions prises |
| **Points clés** | Informations importantes |
| **Actions** | Tâches à suivre |
| **Référence** | Lien vers le transcript complet |

### Conditions de capture

- Sessions avec **≥ 3 messages user** (évite les sessions vides)
- Résumé **> 50 caractères** (évite les erreurs)

## Configuration

### Hook SessionEnd

**Fichier** : `.claude/hooks/memory-capture.sh`

```bash
#!/bin/bash
# Lit le transcript de la session
# Appelle Claude headless pour résumer
# Sauvegarde dans pai/memory/sessions/
```

**Configuration** : `.claude/settings.json`

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/memory-capture.sh",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## Format des fichiers mémoire

```markdown
# Session: [Titre]

**Date**: 2026-01-11
**Messages**: 15

## Résumé
[Description courte de ce qui s'est passé]

## Décisions
- Décision 1
- Décision 2

## Points clés
- Point important 1
- Point important 2

## Actions
- [ ] Action à faire

---
*Transcript: ~/.claude/projects/.../session-id.jsonl*
```

## Coût

- **Modèle** : Haiku (économique)
- **Estimé** : ~$0.001 par session
- **Tokens** : ~2000 input, ~200 output

## Accès à la mémoire

La mémoire n'est **pas chargée automatiquement** au démarrage (évite de surcharger le contexte).

Pour accéder à la mémoire passée :
- Lis manuellement les fichiers dans `pai/memory/sessions/`
- Ou demande : "Qu'est-ce qu'on a fait la semaine dernière ?"

## Transcripts originaux

Les transcripts complets sont stockés par Claude Code dans :
```
~/.claude/projects/{project-path}/{session-id}.jsonl
```

Le fichier mémoire garde une référence vers le transcript original si tu as besoin de plus de détails.

## Rattrapage manuel

Si une session n'a pas été capturée (ex: `/clear` au lieu de quitter), utilise le skill `memory-manager` :

```
"quelles sessions ne sont pas en mémoire ?"
"gérer ma mémoire"
```

Le skill liste les sessions des 3 derniers jours non mémorisées et permet de les capturer manuellement.

## Limitations

- `/clear` ne déclenche pas la capture automatique (utiliser `memory-manager` pour rattraper)
- Dépend de Claude Code headless (doit être installé)
- Nécessite `jq` pour parser le JSON
- Timeout de 60 secondes pour le résumé
