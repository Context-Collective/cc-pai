# Notes de Conception : Système de Mémoire

> Document de travail - Janvier 2026
> Statut : Réflexion en cours, implémentation v1 simple

---

## Contexte

La mémoire est le centre de la PAI. Sans elle, chaque session repart de zéro.

**Cas d'usage prioritaires identifiés :**
1. **Reprise de contexte projet** : "On en était où sur Jeofun ?"
2. **Décisions passées** : "Pourquoi on a choisi Zustand ?"

---

## État Actuel (v1)

### Ce qui existe

| Composant | Implémentation | Statut |
|-----------|----------------|--------|
| **Capture** | Hook SessionEnd → résumé Haiku | ✅ Fonctionnel |
| **Stockage** | `pai/memory/sessions/*.md` | ✅ Fonctionnel |
| **Retrieval manuel** | Skill `memory-manager` | ✅ Fonctionnel |
| **Retrieval projet** | Skill `project-context` | ✅ Créé (non testé) |

### Approche Actuelle

```
Capture : Automatique (tout capturer)
Retrieval : Manuel (skill déclenché par l'utilisateur)
Sélection : Bourrine (grep + 5 dernières sessions)
```

**Limites connues :**
- Pas de filtrage intelligent
- Charge potentiellement trop de contexte
- Pas d'économie de tokens

---

## Points en Suspens

### 1. Économie de Tokens (Critique pour Multi-Provider)

**Problème :** Charger 5 sessions complètes = beaucoup de tokens.

**Contexte multi-provider :**
- Claude Code : contexte "gratuit" (abonnement)
- API directe : chaque token coûte
- Providers tiers : limites de contexte variables

**Pistes à explorer :**

| Approche | Description | Complexité |
|----------|-------------|------------|
| **Résumés multi-niveaux** | Session → Résumé court → Mots-clés | Moyenne |
| **Chargement progressif** | D'abord titres, puis détails si besoin | Moyenne |
| **Index/métadonnées** | Fichier index.json avec metadata par session | Simple |
| **Embeddings locaux** | Recherche sémantique sans charger le contenu | Complexe |

### 2. Pertinence du Retrieval

**Problème :** Comment savoir quelles sessions sont pertinentes ?

**Approche actuelle :** Grep sur le nom du projet → naïf.

**Limites :**
- "Jeofun" doit apparaître textuellement
- Pas de liens sémantiques ("GPS" lié à "géolocalisation")
- Pas de contexte croisé (session A mentionne décision utile pour projet B)

**Pistes à explorer :**

| Approche | Description | Complexité |
|----------|-------------|------------|
| **Tags manuels** | L'utilisateur tagge les sessions importantes | Simple |
| **Tags auto** | Le résumé inclut des tags générés | Moyenne |
| **Graphe de liens** | Sessions liées entre elles | Complexe |
| **RAG léger** | Embeddings + recherche sémantique | Complexe |

### 3. Obsolescence

**Problème :** Une décision de janvier peut être obsolète en mars.

**Approche Miessler :** Pas de gestion automatique. Curation humaine.

**Nos options :**

| Approche | Description | Complexité |
|----------|-------------|------------|
| **Rien** | L'humain sait ce qui est récent | Simple |
| **Decay visuel** | Afficher l'âge des sessions | Simple |
| **Archivage manuel** | Déplacer les vieilles sessions | Simple |
| **Versioning** | Tracker l'évolution des décisions | Complexe |

### 4. Conflits d'Information

**Problème :** Session A dit "on utilise Redux", Session B dit "on migre vers Zustand".

**Approche Miessler :** Pas de gestion. L'humain résout.

**Nos options :**

| Approche | Description | Complexité |
|----------|-------------|------------|
| **Rien** | Afficher les deux, l'humain tranche | Simple |
| **Priorité récent** | Session plus récente = vérité | Simple |
| **Détection** | Alerter sur contradictions potentielles | Complexe |

### 5. Granularité de la Mémoire

**Question :** Une seule mémoire globale ou par projet ?

**Réflexion actuelle :**

```
pai/memory/
├── sessions/           # Toutes les sessions (global)
└── projects/           # Mémoire par projet (futur ?)
    ├── jeofun/
    └── cc-pai/
```

**Trade-offs :**

| Approche | Avantage | Inconvénient |
|----------|----------|--------------|
| **Globale** | Simple, cross-projet possible | Bruit, recherche moins ciblée |
| **Par projet** | Ciblée, moins de bruit | Silos, duplication possible |
| **Hybride** | Best of both | Complexité |

---

## Comparaison des Approches de Retrieval

### Approche 1 : Tout Charger (actuel)

```
grep "projet" sessions/*.md → charger les 5 premiers
```

| + | - |
|---|---|
| Ultra simple | Coûteux en tokens |
| Fonctionne | Pas de pertinence |
| Pas de dépendances | Ne scale pas |

**Viable pour :** Usage personnel, Claude Code (tokens "gratuits")

### Approche 2 : Index + Chargement Sélectif

```
1. Maintenir un index.json avec métadonnées
2. Chercher dans l'index (léger)
3. Charger uniquement les sessions sélectionnées
```

```json
// pai/memory/index.json
{
  "sessions": [
    {
      "id": "2026-01-11_14-30_abc123",
      "date": "2026-01-11",
      "title": "Architecture PAI v2",
      "projects": ["cc-pai"],
      "tags": ["architecture", "memory", "design"],
      "summary_short": "Réflexion sur le système de mémoire..."
    }
  ]
}
```

| + | - |
|---|---|
| Recherche rapide | Index à maintenir |
| Économe en tokens | Sync index/fichiers |
| Extensible | Plus de code |

**Viable pour :** Multi-provider, usage intensif

### Approche 3 : RAG Léger (Embeddings Locaux)

```
1. Générer embeddings des sessions (une fois)
2. Recherche sémantique sur la question
3. Charger les K plus pertinentes
```

| + | - |
|---|---|
| Recherche sémantique | Dépendance externe |
| Cross-projet intelligent | Complexité |
| Scale bien | Coût génération embeddings |

**Viable pour :** Grosse base de mémoire, besoins avancés

---

## Recommandations

### Court Terme (v1 - maintenant)

**Garder l'approche simple :**
- Capture automatique (hook)
- Retrieval par skill (grep + N sessions)
- Pas d'optimisation tokens

**Pourquoi :** On utilise Claude Code, les tokens sont "gratuits". Mieux vaut un système simple qui marche qu'un système complexe qui bugge.

### Moyen Terme (v1.5)

**Ajouter un index léger :**
- Générer `index.json` à chaque capture
- Modifier `project-context` pour chercher dans l'index d'abord
- Charger seulement les sessions pertinentes

**Trigger :** Quand on aura assez de sessions pour que le grep devienne lent.

### Long Terme (v2)

**Si besoin multi-provider avec économie de tokens :**
- Résumés à 2 niveaux (court/complet)
- Potentiellement embeddings locaux
- Ou solution externe (Mem0, etc.)

---

## Questions Ouvertes

1. **Quel seuil de sessions justifie un index ?** (10 ? 50 ? 100 ?)

2. **Comment gérer les sessions multi-projets ?** (Une session touche Jeofun ET cc-pai)

3. **Faut-il un niveau "learnings" séparé des sessions ?** (Comme Miessler)

4. **Comment intégrer avec les autres providers ?** (Format universel ?)

5. **Quid de la mémoire "globale" vs "projet" ?** (ME.md = global, sessions = projet ?)

---

## Références

- [Analyse Miessler](./miessler-memory-analysis.md) - Comment il gère sa mémoire
- [PRD](../architecture/PRD.md) - Spécification du projet
- [Memory Reference](../reference/memory.md) - Documentation utilisateur

---

## Historique

| Date | Changement |
|------|------------|
| 2026-01-11 | Création du document, réflexion initiale |
| 2026-01-11 | Analyse Miessler, création skill project-context |
