# Prompts Sous-Agents

Prompts a utiliser avec l'outil Task pour le mode `audit`.

## Agent: doc-code-sync

**Type**: Explore
**But**: Detecter les incoherences entre documentation et code source

```
Analyse la coherence entre documentation et code du projet {PROJECT_PATH}.

## Ta mission

Compare les fichiers de documentation (docs/reference/, docs/architecture/) avec le code source (src/, lib/, api/).

## Ce que tu cherches

1. **Code non documente**
   - Endpoints API dans le code sans documentation
   - Fonctions/classes publiques exportees sans doc
   - Composants React principaux sans README

2. **Documentation obsolete**
   - Docs qui referent a des fichiers/fonctions supprimes
   - Endpoints documentes mais absents du code
   - Signatures de fonctions qui ne matchent plus

3. **Incoherences**
   - Noms de parametres differents doc vs code
   - Types differents
   - Valeurs par defaut incorrectes

## Comment chercher

1. Liste les fichiers dans docs/reference/ et docs/architecture/
2. Pour chaque doc, extrait les elements documentes (endpoints, fonctions, composants)
3. Cherche ces elements dans src/ avec Grep
4. Compare les signatures

## Format de sortie

Retourne un JSON structure :

```json
{
  "undocumented": [
    {
      "type": "endpoint|function|component",
      "location": "src/api/users.ts:45",
      "signature": "POST /api/users",
      "severity": "high|medium|low"
    }
  ],
  "obsolete": [
    {
      "doc": "docs/reference/api.md:120",
      "element": "GET /api/old-endpoint",
      "reason": "endpoint supprime du code"
    }
  ],
  "incorrect": [
    {
      "doc": "docs/reference/api.md:50",
      "line": 50,
      "documented": "GET /users/:id",
      "actual": "GET /users/{id}",
      "file": "src/api/users.ts:30"
    }
  ],
  "summary": {
    "total_docs_checked": 5,
    "undocumented_count": 3,
    "obsolete_count": 1,
    "incorrect_count": 2
  }
}
```

Ne retourne QUE le JSON, pas de texte autour.
```

---

## Agent: doc-coherence

**Type**: Explore
**But**: Verifier la coherence interne de la documentation

```
Analyse la coherence interne de la documentation du projet {PROJECT_PATH}.

## Ta mission

Verifie que les fichiers de documentation sont coherents entre eux.

## Ce que tu cherches

1. **Liens internes casses**
   - Liens markdown vers des fichiers qui n'existent pas
   - Ancres (#section) vers des titres inexistants
   - Chemins relatifs incorrects

2. **Doublons**
   - Fichiers avec contenu tres similaire (>70%)
   - Memes informations documentees a plusieurs endroits
   - Copies de fichiers avec noms differents

3. **INDEX.md**
   - Existe-t-il dans docs/ ?
   - Liste-t-il tous les fichiers du dossier ?
   - Les liens sont-ils corrects ?

4. **Tables des matieres**
   - Fichiers >200 lignes sans TOC
   - TOC presentes mais incompletes

5. **Fichiers orphelins**
   - Docs jamais referencees nulle part
   - Fichiers dans docs/ sans lien depuis INDEX ou autres docs

## Comment chercher

1. Liste tous les .md dans docs/
2. Pour chaque fichier, extrait les liens [text](path)
3. Verifie que chaque path existe
4. Compare les contenus pour detecter doublons
5. Verifie INDEX.md

## Format de sortie

Retourne un JSON structure :

```json
{
  "broken_links": [
    {
      "file": "docs/overview.md",
      "line": 42,
      "link_text": "voir API",
      "target": "docs/old-api.md",
      "reason": "fichier inexistant"
    }
  ],
  "duplicates": [
    {
      "files": ["docs/api.md", "docs/reference/api.md"],
      "similarity": 0.85,
      "recommendation": "fusionner ou supprimer un des deux"
    }
  ],
  "index": {
    "exists": false,
    "path": "docs/INDEX.md",
    "missing_entries": ["docs/devbooks/fix-bug.md"],
    "broken_entries": []
  },
  "missing_toc": [
    {
      "file": "docs/architecture/overview.md",
      "lines": 450,
      "recommendation": "ajouter table des matieres"
    }
  ],
  "orphans": [
    {
      "file": "docs/old-notes.md",
      "reason": "jamais reference dans aucun autre fichier"
    }
  ],
  "summary": {
    "total_docs": 15,
    "broken_links": 3,
    "duplicates": 1,
    "orphans": 2
  }
}
```

Ne retourne QUE le JSON, pas de texte autour.
```

---

## Usage dans la skill

```python
# Lancer les agents en parallele
results = []

# Agent 1: doc-code-sync
task1 = Task(
    subagent_type="Explore",
    prompt=DOC_CODE_SYNC_PROMPT.format(PROJECT_PATH=project_path),
    description="Audit doc-code sync"
)

# Agent 2: doc-coherence
task2 = Task(
    subagent_type="Explore",
    prompt=DOC_COHERENCE_PROMPT.format(PROJECT_PATH=project_path),
    description="Audit doc coherence"
)

# Agent 3: structure (script existant)
task3 = Bash(
    command=f"python3 pai/skills/doc-manager/scripts/analyze_docs.py {project_path}"
)

# Combiner les resultats
audit_report = combine_results(task1, task2, task3)
```
