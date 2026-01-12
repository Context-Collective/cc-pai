# Comparaison cc-pai vs Miessler PAI

Analyse comparative des mécanismes entre cc-pai et la [PAI de Daniel Miessler](https://github.com/danielmiessler/Personal_AI_Infrastructure).

## Philosophies

| Miessler | cc-pai |
|----------|--------|
| Enterprise-grade, exhaustif | Accessible, minimaliste |
| 10 fichiers TELOS | 1 fichier ME.md |
| Sécurité avancée | Permissions basiques |
| Pack system custom | Skills natifs Claude Code |

## Architecture Globale

| Aspect | Miessler | cc-pai | Notes |
|--------|----------|--------|-------|
| **Hook SessionStart** | ✅ | ✅ | Mécanisme identique |
| **Routing skills** | Custom (CORE skill) | Natif Claude Code | Voir ⚠️ ci-dessous |
| **Séparation USER/SYSTEM** | Dossiers séparés | gitignore | Équivalent |
| **Multi-provider** | ❌ (tout dans .claude/) | ✅ (pai/ + symlink) | On anticipe |

### ⚠️ Routing et Multi-provider

cc-pai utilise le **routing natif de Claude Code** basé sur les `description` des skills. C'est un avantage aujourd'hui (simplicité, pas de maintenance) mais un **problème futur pour le multi-provider**.

**Pourquoi** : Le routing natif est spécifique à Claude Code. Si on veut supporter d'autres providers (Mistral, OpenAI), il faudra :
- Soit un système de routing orchestré (comme Miessler)
- Soit adapter le routing par provider
- Soit standardiser sur un format de routing universel

**À prévoir** : Un layer d'orchestration qui gère le routing indépendamment du provider.

## Contexte Personnel

### Miessler : TELOS Framework (10 fichiers)

| Fichier | Contenu |
|---------|---------|
| MISSION.md | But de vie |
| GOALS.md | Objectifs par domaine |
| PROJECTS.md | Projets actifs |
| BELIEFS.md | Convictions |
| MODELS.md | Modèles mentaux |
| STRATEGIES.md | Approches tactiques |
| NARRATIVES.md | Identité, histoire |
| LEARNED.md | Leçons apprises |
| CHALLENGES.md | Obstacles actuels |
| IDEAS.md | Idées notables |

### cc-pai : ME.md (1 fichier)

| Section | Équivalent TELOS |
|---------|------------------|
| Qui je suis | NARRATIVES |
| Mes objectifs | MISSION + GOALS |
| Mes projets | PROJECTS |
| Comment je travaille | STRATEGIES |
| Mes conventions | - |
| Avec l'IA | - |

### Ce qu'on ne couvre pas (volontairement)

- **BELIEFS** : Convictions profondes (pertinent pour life coaching, moins pour dev)
- **MODELS** : Modèles mentaux (idem)
- **LEARNED** : Leçons → pourrait aller dans Memory
- **IDEAS** : Idées → pourrait être un skill dédié

**Choix conscient** : Simplicité pour v1. On peut enrichir si besoin.

## Memory

| Aspect | Miessler | cc-pai |
|--------|----------|--------|
| Architecture | 3 tiers (hot/warm/cold) | À implémenter |
| Sous-dossiers | 11 (sessions, learnings, decisions...) | 1 (memory/) |
| Capture | Automatique | À définir |
| Injection | Dans le hook | À définir |

### Réflexion sur la mémoire

**Le problème** : Charger trop de mémoire = contexte surchargé = coût tokens + bruit.

**Options à explorer** :
1. Mémoire sélective (résumés vs détails)
2. Mémoire à la demande (skill qui va chercher)
3. Mémoire tiered comme Miessler (mais plus simple)

## Sécurité

| Aspect | Miessler | cc-pai |
|--------|----------|--------|
| PreToolUse validation | ✅ | ❌ |
| SecurityValidator hook | ✅ | ❌ |
| patterns.yaml | ✅ | ❌ |
| Permissions | settings.json | settings.local.json |

**Choix conscient** : La sécurité avancée est over-engineering pour un usage personnel. Les permissions Claude Code suffisent.

## Verdict

### ✅ Mécanismes corrects

- Hook SessionStart fonctionne
- Contexte injecté correctement
- Skills fonctionnels
- Architecture future-proof (symlink)

### ⚠️ À anticiper

- Routing multi-provider nécessitera orchestration
- Memory à concevoir sans surcharger le contexte

### 🎯 Différenciation

| Miessler | cc-pai |
|----------|--------|
| Exhaustif, complexe | Simple, accessible |
| Difficile à reprendre | Facile à démarrer |
| Spécifique Claude | Prêt multi-provider |
