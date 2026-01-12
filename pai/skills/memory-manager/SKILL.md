---
name: memory-manager
description: Gère la mémoire des sessions. Liste les sessions récentes non mémorisées et permet de les capturer manuellement. Utile après un /clear ou pour rattraper des sessions manquées.
---

# Memory Manager

Skill de gestion de la mémoire des sessions.

## Architecture

Le système de mémoire fonctionne ainsi :
1. **SessionStart** : Crée un fichier template `pai/memory/sessions/{SESSION_ID}.md`
2. **Ce skill** : Met à jour le fichier (snapshot en cours de session)
3. **SessionEnd** : Met à jour le fichier final (filet de sécurité)

**Un seul fichier par session**, nommé par son ID (8 premiers caractères).

## Déclencheurs

- "gérer ma mémoire", "memory manager"
- "quelles sessions ne sont pas en mémoire ?"
- "sessions manquantes", "rattraper les sessions"
- **"mémorise cette session"**, "snapshot session" → met à jour la session en cours

---

## Workflow 1 : Snapshot de la session en cours

Quand l'utilisateur dit "mémorise cette session" ou "snapshot".

### Étapes

1. **Identifier le fichier mémoire actuel**

```bash
# Le fichier a été créé au démarrage par le hook SessionStart
# Son nom est basé sur le session_id (8 premiers chars)
ls -la "$CLAUDE_PROJECT_DIR/pai/memory/sessions/"
```

2. **Lire le transcript actuel**

```bash
TRANSCRIPTS_DIR=~/.claude/projects/-$(echo "$CLAUDE_PROJECT_DIR" | sed 's/\//-/g')
# Le transcript le plus récent est la session en cours
CURRENT_TRANSCRIPT=$(ls -t "$TRANSCRIPTS_DIR"/*.jsonl 2>/dev/null | head -1)
```

3. **Analyser et mettre à jour** avec Claude headless (haiku)

Utilise le même prompt que le hook SessionEnd (voir `.claude/hooks/memory-capture.sh`).

Format de sortie enrichi :

```markdown
---
session_id: [full_id]
project: [nom_projet]
started: [date_debut]
updated: [maintenant]
status: active
messages: [count]
tags: [tags pertinents]
---

# Session: [Titre descriptif]

## Contexte
- **Projet**: [nom]
- **Branche**: [git branch]
- **Messages**: [count]

## Outils utilisés
- Read (Nx)
- Edit (Nx)
- Bash (Nx)
- Task (Nx)

## Fichiers touchés
- [liste des fichiers modifiés/créés]

## Résumé
[2-3 phrases]

## Décisions
[liste ou 'Aucune']

## Actions
[liste avec checkboxes]

---
*Transcript: [path]*
*Type: SNAPSHOT (session en cours)*
```

---

## Workflow 2 : Rattraper les sessions manquées

Pour les sessions terminées sans mémorisation (ex: après `/clear`).

### Étapes

1. **Lister les transcripts des 3 derniers jours**

```bash
TRANSCRIPTS_DIR=~/.claude/projects/-$(echo "$CLAUDE_PROJECT_DIR" | sed 's/\//-/g')
find "$TRANSCRIPTS_DIR" -name "*.jsonl" -mtime -3
```

2. **Comparer avec les fichiers mémoire existants**

```bash
# Une session est mémorisée si {SHORT_ID}.md existe
for jsonl in "$TRANSCRIPTS_DIR"/*.jsonl; do
  SESSION_ID=$(basename "$jsonl" .jsonl)
  SHORT_ID=${SESSION_ID:0:8}
  if [ ! -f "$CLAUDE_PROJECT_DIR/pai/memory/sessions/${SHORT_ID}.md" ]; then
    echo "Non mémorisée: $SHORT_ID"
  fi
done
```

3. **Afficher les candidates** avec aperçu

```
Sessions non mémorisées (3 derniers jours) :

1. [2026-01-11 14:30] abc12345 - 8 messages - "Discussion architecture..."
2. [2026-01-10 16:45] ghi11223 - 12 messages - "Implémentation memory..."

Lesquelles mémoriser ? (numéros, ou 'toutes')
```

4. **Générer les résumés** pour les sessions choisies

Même processus que le hook SessionEnd : appel haiku avec analyse du transcript.

---

## Commandes utiles

### Trouver le dossier transcripts

```bash
TRANSCRIPTS_DIR=~/.claude/projects/-$(echo "$CLAUDE_PROJECT_DIR" | sed 's/\//-/g')
```

### Compter les messages

```bash
grep -c '"type":"user"' "$TRANSCRIPT_FILE"
```

### Extraire un aperçu

```python
import json

def get_preview(filepath, max_len=60):
    with open(filepath, 'r') as f:
        for line in f:
            try:
                d = json.loads(line)
                if d.get('type') == 'summary':
                    return d.get('summary', '')[:max_len]
                if d.get('type') == 'user':
                    msg = d.get('message', {})
                    content = msg.get('content', '') if isinstance(msg, dict) else str(msg)
                    return content[:max_len]
            except:
                continue
    return "(session vide)"
```

---

## Notes importantes

- **Fichiers nommés par session_id** : `{SHORT_ID}.md` (pas de timestamp dans le nom)
- **Sessions < 3 messages** : ignorées (le template vide est supprimé)
- **Coût** : ~$0.001/session avec Haiku
- **Le skill et le hook utilisent la même mécanique** : update du fichier existant

## Voir aussi

- `.claude/hooks/load-context.sh` - Crée le template au démarrage
- `.claude/hooks/memory-capture.sh` - Met à jour à la fin de session
- `docs/reference/memory.md` - Documentation complète
