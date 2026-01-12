# Plan de Test v1 - cc-pai

> Tests à effectuer avant merge vers main et tag v1.0

---

## Prérequis

- [ ] Claude Code installé et fonctionnel
- [ ] Python 3.8+ disponible
- [ ] `jq` installé (pour les hooks)

---

## 1. Tests de Structure

### 1.1 Vérifier le symlink

```bash
ls -la .claude/skills
# Attendu : skills -> ../pai/skills
```

- [ ] Le symlink pointe vers `../pai/skills`

### 1.2 Vérifier la structure pai/

```bash
ls -la pai/
```

- [ ] `context/` existe
- [ ] `memory/` existe
- [ ] `state/` existe
- [ ] `skills/` existe

### 1.3 Vérifier les templates

```bash
ls install/
```

- [ ] `ME.template.md` présent
- [ ] `CURRENT.template.md` présent

### 1.4 Vérifier le .gitignore

```bash
cat .gitignore | grep -A5 "PAI Instance"
```

- [ ] `pai/context/ME.md` ignoré
- [ ] `pai/state/CURRENT.md` ignoré
- [ ] `pai/memory/**/*` ignoré
- [ ] `.gitkeep` non ignoré

---

## 2. Tests des Hooks

### 2.1 Hook SessionStart (load-context.sh)

**Test :**
1. Lancer une nouvelle session Claude Code dans le projet
2. Observer le message de démarrage

- [ ] Le hook s'exécute sans erreur
- [ ] Le contexte personnel est mentionné (si ME.md existe)

### 2.2 Hook SessionEnd (memory-capture.sh)

**Test :**
1. Avoir une session avec ≥ 3 messages
2. Quitter proprement la session (pas /clear)
3. Vérifier `pai/memory/sessions/`

```bash
ls -la pai/memory/sessions/
```

- [ ] Un nouveau fichier `.md` est créé
- [ ] Le fichier contient un résumé structuré
- [ ] Format du nom : `YYYY-MM-DD_HH-MM_SESSIONID.md`

**Test échec attendu :**
1. Session avec < 3 messages
2. Quitter

- [ ] Aucun fichier créé (comportement normal)

---

## 3. Tests des Skills

### 3.1 Skill: pai-init

**Scénario A : Première initialisation**

1. Renommer temporairement `pai/context/ME.md` :
   ```bash
   mv pai/context/ME.md pai/context/ME.md.backup
   ```
2. Dire : "initialise ma PAI"
3. Répondre aux questions
4. Vérifier les fichiers créés

- [ ] Le skill détecte l'absence de ME.md
- [ ] Questions posées de manière conversationnelle
- [ ] `pai/context/ME.md` créé avec le contenu
- [ ] `pai/state/CURRENT.md` créé (si demandé)

5. Restaurer :
   ```bash
   mv pai/context/ME.md.backup pai/context/ME.md
   ```

**Scénario B : Mise à jour**

1. Avec ME.md existant, dire : "mets à jour ma PAI"

- [ ] Le skill détecte ME.md existant
- [ ] Propose une mise à jour (pas un écrasement)

### 3.2 Skill: skill-creator

**Test :**
1. Dire : "crée un skill pour analyser des logs"
2. Suivre le processus

- [ ] Le skill guide la création
- [ ] Structure créée dans `pai/skills/`
- [ ] SKILL.md généré avec frontmatter valide

**Validation :**
```bash
python3 pai/skills/skill-creator/scripts/quick_validate.py pai/skills/<nouveau-skill>/
```

- [ ] Validation passe sans erreur

### 3.3 Skill: memory-manager

**Prérequis :** Avoir des sessions Claude Code récentes.

**Test :**
1. Dire : "quelles sessions ne sont pas en mémoire ?"

- [ ] Liste des sessions récentes affichée
- [ ] Sessions déjà mémorisées identifiées
- [ ] Option de mémoriser proposée

**Test mémorisation :**
1. Choisir une session à mémoriser
2. Vérifier `pai/memory/sessions/`

- [ ] Fichier créé pour la session choisie

### 3.4 Skill: project-context

**Prérequis :** Avoir des sessions mémorisées mentionnant un projet.

**Test :**
1. Dire : "reprends cc-pai" (ou autre projet avec sessions)

- [ ] Sessions pertinentes trouvées
- [ ] Contexte synthétisé (état, décisions, actions)
- [ ] Sources listées

**Test sans sessions :**
1. Dire : "reprends ProjetInexistant"

- [ ] Message approprié (aucune session trouvée)

### 3.5 Skill: meeting-notes

**Test :**
1. Coller des notes de réunion brutes
2. Dire : "extrais les actions de cette réunion"

- [ ] Actions extraites
- [ ] Décisions identifiées
- [ ] Format structuré

---

## 4. Tests du Contexte

### 4.1 Chargement du contexte personnel

**Test :**
1. S'assurer que `pai/context/ME.md` contient des infos spécifiques
2. Nouvelle session, demander : "qui suis-je ?"

- [ ] Claude utilise les infos de ME.md
- [ ] Réponse personnalisée

### 4.2 Utilisation des préférences

**Test :**
1. ME.md mentionne une préférence (ex: "préfère les arrow functions")
2. Demander du code

- [ ] La préférence est respectée

---

## 5. Tests Clone Frais

Simuler l'expérience d'un nouvel utilisateur.

### 5.1 Setup

```bash
# Dans un dossier temporaire
git clone https://github.com/Context-Collective/cc-pai.git test-pai
cd test-pai
```

### 5.2 Vérifications initiales

- [ ] Symlink `.claude/skills` fonctionne
- [ ] Pas de `pai/context/ME.md` (gitignore)
- [ ] Pas de `pai/state/CURRENT.md` (gitignore)
- [ ] Templates présents dans `install/`

### 5.3 Onboarding

1. Lancer Claude Code
2. Dire : "initialise ma PAI"

- [ ] pai-init se déclenche
- [ ] Fichiers personnels créés
- [ ] Utilisable immédiatement après

### 5.4 Cleanup

```bash
cd ..
rm -rf test-pai
```

---

## 6. Tests de Robustesse

### 6.1 Session vide

1. Lancer Claude Code
2. Quitter immédiatement

- [ ] Pas d'erreur du hook
- [ ] Pas de fichier mémoire créé

### 6.2 Fichiers manquants

1. Supprimer temporairement `pai/context/ME.md`
2. Lancer une session

- [ ] Pas de crash
- [ ] Message approprié ou comportement dégradé gracieux

### 6.3 Permissions

```bash
ls -la .claude/hooks/
```

- [ ] `load-context.sh` exécutable (x)
- [ ] `memory-capture.sh` exécutable (x)

---

## 7. Tests de Documentation

### 7.1 README

1. Suivre les instructions du README

- [ ] Installation fonctionne
- [ ] Démarrage rapide fonctionne

### 7.2 Getting Started

1. Suivre `docs/guides/getting-started.md`

- [ ] Toutes les étapes fonctionnent
- [ ] Pas d'étape obsolète

### 7.3 Liens internes

```bash
# Vérifier les liens cassés (basique)
grep -r "](\./" docs/ | head -20
```

- [ ] Liens relatifs valides

---

## 8. Checklist Finale

### Avant merge

- [ ] Tous les tests ci-dessus passent
- [ ] Pas de fichiers personnels dans le repo (ME.md, sessions)
- [ ] PRD.md à jour avec la roadmap
- [ ] CHANGELOG ou notes de version prêtes

### Commandes de vérification

```bash
# Fichiers non trackés qui devraient l'être ?
git status

# Fichiers personnels qui seraient trackés par erreur ?
git ls-files | grep -E "(ME\.md|CURRENT\.md|sessions/)"
# Attendu : aucun résultat
```

---

## Résultats des Tests

| Section | Passé | Échoué | Notes |
|---------|-------|--------|-------|
| 1. Structure | | | |
| 2. Hooks | | | |
| 3. Skills | | | |
| 4. Contexte | | | |
| 5. Clone frais | | | |
| 6. Robustesse | | | |
| 7. Documentation | | | |

**Testeur :** _________________
**Date :** _________________
**Verdict :** ⬜ Prêt pour merge | ⬜ Corrections nécessaires
