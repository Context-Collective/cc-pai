# Contribuer à cc-pai

cc-pai est un projet collaboratif ouvert. On valorise l'expérimentation et la diversité des approches.

## Rejoindre le projet

1. **Demande un accès** : Ouvre une [Issue](https://github.com/contexte-collectif/cc-pai/issues) ou contacte un membre
2. **Une fois accepté**, tu es ajouté comme collaborateur
3. **Clone le repo** :
   ```bash
   git clone https://github.com/contexte-collectif/cc-pai.git
   cd cc-pai
   ```
4. Tu peux maintenant créer et pousser tes branches directement

## Philosophie

- **Expérimenter librement** : Crée ta branche, teste tes idées
- **Partager tôt** : Pousse ta branche même si c'est en cours
- **Discuter ouvertement** : Les divergences sont normales et saines
- **Évoluer ensemble** : On trouve des compromis ou on accepte les différences

## Comment contribuer

### 1. Crée ta branche

```bash
git checkout -b ton-pseudo/ton-idee
# Exemples :
# madiane/memory-system
# mehdi/skill-pdf-analyzer
# pierre/approche-alternative-telos
```

### 2. Développe et pousse

```bash
git add .
git commit -m "Description de ton avancée"
git push origin ton-pseudo/ton-idee
```

Pousse régulièrement, même si c'est en work-in-progress.

### 3. Ouvre une discussion

- Crée une **Issue** ou une **Discussion** GitHub pour présenter ton approche
- Explique ce que tu explores, pourquoi, où tu en es
- Invite les autres à regarder ta branche

### 4. Ce qui peut arriver ensuite

| Scénario | Action |
|----------|--------|
| **Consensus** | On merge dans `main` |
| **Compromis** | On adapte et on merge |
| **Approches différentes** | Les branches coexistent |
| **Vision divergente** | Fork légitime du projet |

## Branches et versions

- `main` : Version stable, **protégée** (seul le gestionnaire peut merger)
- `pseudo/*` : Branches personnelles d'exploration
- `nom-de-code/*` : Branches collaboratives ou versions alternatives

## Comment ça fonctionne

```
main (stable)
  │
  ├── fabien/memory-system      ← expérimentation perso
  │     │
  │     └── ✓ ça marche, ça colle → merge dans main
  │
  ├── mehdi/skill-pdf           ← expérimentation perso
  │     │
  │     └── ✓ validé → merge dans main
  │
  └── phoenix/multi-provider    ← divergence assumée (pas que Claude)
        │
        └── devient une version alternative du projet
```

**Le cycle typique :**
1. Tu pars de `main`, tu crées `ton-pseudo/ton-idee`
2. Tu expérimentes, tu pousses, tu présentes tes idées
3. Discussion avec le groupe
4. **Si ça colle** → merge dans `main`
5. **Si ça diverge** (ex: approche multi-provider vs Claude only) → on crée une branche `nom-de-code/` qui devient une version alternative

## Règle simple

- Tu ne touches qu'à **tes** branches (`ton-pseudo/*`)
- Tu ne modifies **jamais** les branches des autres sans leur accord

**Travailler à plusieurs sur une branche ?** C'est possible !
- Créez une branche avec un nom de code (`phoenix/memory-system`, `aurora/nouvelle-archi`)
- Mettez-vous d'accord sur qui y contribue
- Communiquez pour éviter les conflits

## Conventions légères

- **Noms de branches** : `pseudo/description-courte`
- **Commits** : Messages clairs, en français ou anglais
- **Respect** : Bienveillance dans les discussions

## Pas de process lourd

On évite :
- Les PR obligatoires pour tout
- Les reviews bloquantes
- Les règles rigides

On préfère :
- La confiance
- La discussion
- L'expérimentation

---

L'important c'est de construire ensemble, pas de suivre un process.
