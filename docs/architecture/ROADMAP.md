# Roadmap cc-pai

Suivi du développement du framework cc-pai.

## Étape 1 : Architecture PAI ✅

- [x] Structure `pai/` avec context, memory, state, skills
- [x] Symlink `.claude/skills -> ../pai/skills`
- [x] Templates dans `install/`
- [x] Séparation framework/instance avec .gitignore
- [x] Hook SessionStart pour injection du contexte

## Étape 2 : Skills de base ✅

- [x] skill-creator fonctionnel
- [x] pai-init pour onboarding assisté
- [x] meeting-notes comme exemple

## Étape 3 : Documentation ✅

- [x] Structure docs/ organisée (architecture, reference, guides)
- [x] README user-facing
- [x] Guide getting-started
- [x] Référence hooks, skills, context

## Étape 4 : Memory ✅

- [x] Hook SessionEnd avec Claude headless (haiku) pour résumer
- [x] Format markdown structuré (décisions, points clés, actions)
- [x] Capture automatique des sessions ≥ 3 messages
- [x] Référence vers transcript original

## Étape 5 : State

- [ ] Intégrer CURRENT.md dans le hook
- [ ] Skill pour mettre à jour l'état

## Futures étapes (hors v1)

| Étape | Fonctionnalité |
|-------|----------------|
| 6 | Hooks d'automatisation avancés |
| 7 | Agents personnalisés |
| 8 | Multi-provider (pas que Claude) |
| 9 | Partage de skills entre PAI |

## Historique

| Date | Milestone |
|------|-----------|
| Jan 2026 | Architecture PAI v1 |
| Jan 2026 | Hook SessionStart |
| Jan 2026 | Documentation complète |
| Jan 2026 | Système de mémoire (auto-capture) |
