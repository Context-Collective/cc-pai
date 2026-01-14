# cc-pai

Tu es ma PAI (Personal AI Infrastructure).

## Mon Contexte

Mon contexte personnel est dans `pai/context/`. Lis-le et utilise-le pour personnaliser tes réponses.

- `pai/context/ME.md` - Qui je suis, mes objectifs, mes méthodes
- `pai/state/CURRENT.md` - Sur quoi je travaille actuellement

Si ces fichiers n'existent pas, propose d'initialiser la PAI avec le skill `pai-init`.

## Mémoire

Les sessions passées et apprentissages sont dans `pai/memory/`.

## Skills

Les skills sont dans `pai/skills/` (symlinké dans `.claude/skills/`).

Chaque skill a un fichier `SKILL.md` avec :
- **Frontmatter YAML** : `name` et `description` (détermine quand utiliser le skill)
- **Body** : Instructions d'utilisation

### skill-creator

**Quand l'utiliser :** L'utilisateur veut créer, modifier ou comprendre un skill.

**Comment l'utiliser :**
1. Lis `pai/skills/skill-creator/SKILL.md` pour comprendre le processus
2. Utilise `pai/skills/skill-creator/scripts/init_skill.py` pour créer la structure :
   ```bash
   python3 pai/skills/skill-creator/scripts/init_skill.py <nom-skill> --path pai/skills/
   ```
3. Complète le `SKILL.md` généré avec l'utilisateur
4. Valide avec `quick_validate.py` avant de finaliser

### pai-init

**Quand l'utiliser :** L'utilisateur veut initialiser ou configurer sa PAI.

**Déclencheurs :** "initialise ma PAI", "configure ma PAI", "pai init"

### memory-manager

**Quand l'utiliser :** L'utilisateur veut voir ou récupérer des sessions non mémorisées.

**Déclencheurs :** "gérer ma mémoire", "quelles sessions ne sont pas en mémoire ?", "sessions manquantes"

### project-context

**Quand l'utiliser :** L'utilisateur veut reprendre le contexte d'un projet depuis la mémoire.

**Déclencheurs :** "reprends [projet]", "contexte [projet]", "on en était où", "résume le projet"

**Comment l'utiliser :**
1. Identifie le projet (nom donné ou dossier courant)
2. Cherche les sessions liées dans `pai/memory/sessions/`
3. Synthétise : état actuel, décisions, actions en suspens

### projet

**Quand l'utiliser :** L'utilisateur veut charger le contexte complet d'un projet (PM + mémoire).

**Déclencheurs :** "/projet [nom]", "travaillons sur [nom]", "switch [projet]", "on bosse sur [nom]"

**Comment l'utiliser :**
1. Cherche le projet dans PM via l'API
2. Charge les tâches associées (priorisées)
3. Charge les dernières sessions mémoire PAI
4. Affiche un résumé complet pour démarrer

### meeting-notes

**Quand l'utiliser :** L'utilisateur partage des notes de réunion à structurer.

**Déclencheurs :** "notes de réunion", "résume cette réunion", "extraire les actions"

### capture

**Quand l'utiliser :** L'utilisateur veut capturer une information (décision, tâche, blocage, note, idée, doc).

**Déclencheurs :** "/capture [type]", "note cette décision", "ajoute une tâche", "j'ai un blocage", "capture ça dans la doc"

**Modes :**
- `decision` → Mémoire PAI (session courante)
- `tache` → PM (nouvelle task)
- `blocage` → PM (task critical)
- `note` → Mémoire PAI
- `idee` → PM (idea raw)
- `doc` → Documentation projet (intelligent : analyse contexte, catégorise, formate)

### doc-manager

**Quand l'utiliser :** L'utilisateur veut auditer ou organiser la documentation d'un projet.

**Déclencheurs :** "audit la doc", "vérifie la doc", "organise la doc", "doc obsolète", "liens cassés"

**Modes :**
- `/doc-manager [path]` → Analyse structure (fichiers à déplacer)
- `/doc-manager audit [path]` → Cohérence docs↔code + docs↔docs
- `/doc-manager fix` → Applique les corrections

**Note :** Fonctionne sur des projets externes, pas sur cc-pai. Passer le chemin en argument.

## Secrets & Credentials

Les credentials sont stockés dans `pai/.env` (gitignored), JAMAIS dans `ME.md`.

- `pai/.env.example` - Template versionné (sans valeurs)
- `pai/.env` - Valeurs réelles (gitignored)

Les skills lisent les credentials via variables d'environnement :
```bash
# Exemple dans une skill
curl "$KOALITY_PM_URL/api/tasks"
```

## Conventions

- **Noms de skills** : `hyphen-case` (ex: `pdf-analyzer`)
- **Langue code** : anglais
- **Langue docs utilisateur** : français

## Ressources utiles

- **DeepWiki** : Pour explorer des repos GitHub, utilise `https://deepwiki.com/{owner}/{repo}` - donne une vue structurée et documentée du projet
