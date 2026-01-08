# cc-pai

cc-pai est une PAI (Personal AI) open source développée par Context Collective.

## Skills

Les skills sont dans `.claude/skills/`. Chaque skill a un fichier `SKILL.md` avec :
- **Frontmatter YAML** : `name` et `description` (détermine quand utiliser le skill)
- **Body** : Instructions d'utilisation

### skill-creator

**Quand l'utiliser :** L'utilisateur veut créer, modifier ou comprendre un skill.

**Comment l'utiliser :**
1. Lis `.claude/skills/skill-creator/SKILL.md` pour comprendre le processus
2. Utilise `.claude/skills/skill-creator/scripts/init_skill.py` pour créer la structure :
   ```bash
   python3 .claude/skills/skill-creator/scripts/init_skill.py <nom-skill> --path .claude/skills/
   ```
3. Complète le `SKILL.md` généré avec l'utilisateur
4. Valide avec `quick_validate.py` avant de finaliser

**Références utiles :**
- `.claude/skills/skill-creator/references/workflows.md` : Patterns de workflows
- `.claude/skills/skill-creator/references/output-patterns.md` : Patterns de sortie

## Conventions

- **Noms de skills** : `hyphen-case` (ex: `pdf-analyzer`)
- **Langue code** : anglais
- **Langue docs utilisateur** : français
