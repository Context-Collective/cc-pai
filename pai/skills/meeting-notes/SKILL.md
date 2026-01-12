---
name: meeting-notes
description: |
  Extracts action items, decisions, and key points from meeting notes.
  USE WHEN user mentions meeting notes, extraire actions, résumer réunion,
  notes de réunion, or pastes raw meeting notes asking for structure.
---

# Meeting Notes Processor

## Output Format

ALWAYS structure the output as:

```markdown
# Résumé Réunion

## Décisions
- [Liste des décisions prises]

## Actions
- [ ] Action (@responsable si mentionné)

## Points Clés
- [Points importants discutés]

## Prochaines Étapes
- [Si mentionnées]
```

## Guidelines

- Identifier les verbes d'action : "on va", "il faut", "décidé de", "doit"
- Extraire les responsables si mentionnés (noms propres)
- Distinguer décisions (actées) vs actions (à faire)
- Ignorer le bavardage, garder l'essentiel
- Si une deadline est mentionnée, l'inclure dans l'action
