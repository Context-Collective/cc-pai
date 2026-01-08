# cc-pai

**PAI (Personal AI) open source par Contexte Collectif**

Une infrastructure d'IA personnelle simple, modulaire et évolutive, conçue pour [Claude Code](https://claude.ai/code).

## Vision

cc-pai s'inspire des travaux de [Daniel Miessler](https://danielmiessler.com/blog/personal-ai-maturity-model) sur l'IA personnelle, avec une approche simplifiée adaptée aux besoins de notre communauté.

**Philosophie :** Skills d'abord, complexité ensuite.

## Installation

```bash
git clone https://github.com/contexte-collectif/cc-pai.git
cd cc-pai
```

**Prérequis :**
- [Claude Code](https://claude.ai/code)
- Python 3.8+ (pour les scripts des skills)
- PyYAML (`pip install pyyaml`)

## Utilisation

cc-pai fonctionne avec **Claude Code**. Tu interagis en langage naturel.

### Créer un nouveau skill

Demande simplement à Claude Code :

> "Crée un skill pour analyser des PDF"

ou

> "J'ai besoin d'un skill qui résume des articles"

Claude Code utilise le `skill-creator` et génère automatiquement la structure :

```
skills/mon-skill/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

### Valider un skill

> "Valide le skill pdf-analyzer"

### Packager un skill

> "Package le skill pdf-analyzer"

## Structure du projet

```
cc-pai/
├── skills/                    # Skills disponibles
│   └── skill-creator/         # Skill pour créer des skills
├── CLAUDE.md                  # Instructions pour Claude Code
├── README.md                  # Ce fichier
└── CONTRIBUTING.md            # Guide de contribution
```

## Comment ça marche

1. **CLAUDE.md** contient les instructions que Claude Code lit au démarrage
2. **skills/** contient les capacités modulaires
3. Quand tu fais une demande, Claude Code consulte les skills pertinents et agit

## Roadmap

### Phase 1 : Skills (actuel)
- [x] Structure de base du projet
- [x] Skill-creator (créer des skills)
- [ ] Premiers skills utiles pour Contexte Collectif

### Phase 2 : Mémoire
- [ ] Système de mémoire simple (CAPTURE / LEARNINGS)
- [ ] Persistance entre sessions

### Phase 3 : TELOS
- [ ] Définition du contexte collectif (mission, valeurs, objectifs)
- [ ] Personnalisation individuelle

### Phase 4 : Intégrations
- [ ] Hooks Claude Code
- [ ] Connexions externes (APIs, outils)

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour le workflow de contribution.

## Ressources Claude Code

Documentation pour bien comprendre les concepts utilisés dans cc-pai :

### Skills
Les skills étendent les capacités de Claude avec des connaissances spécialisées.
- [Claude Code Skills](https://code.claude.com/docs/en/skills) - Documentation officielle
- [Anthropic Skills Repository](https://github.com/anthropics/skills) - Exemples de skills
- [Agent Skills Spec](https://agentskills.io/) - Standard ouvert

### Hooks
Les hooks permettent d'exécuter du code en réponse aux événements de Claude Code.
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide) - Guide de démarrage
- [Hooks Reference](https://docs.claude.com/en/docs/claude-code/hooks) - Référence complète
- [Blog: How to Configure Hooks](https://claude.com/blog/how-to-configure-hooks) - Tutoriel

### Subagents
Les sous-agents permettent de déléguer des tâches à des agents spécialisés.
- [Subagents Documentation](https://code.claude.com/docs/en/sub-agents) - Documentation officielle
- [Awesome Claude Code Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) - Collection de 100+ subagents

### MCP (Model Context Protocol)
Le MCP permet à Claude d'interagir avec des outils et services externes.
- [MCP Documentation](https://modelcontextprotocol.io/) - Documentation officielle
- [MCP Servers](https://github.com/modelcontextprotocol/servers) - Serveurs disponibles

## Ressources Daniel Miessler (PAI)

Articles et vidéos qui ont inspiré ce projet :

- [Building a Personal AI Infrastructure (PAI)](https://danielmiessler.com/blog/personal-ai-infrastructure) - Article principal + vidéo walkthrough 40min (Dec 2025)
- [Personal AI Maturity Model (PAIMM)](https://danielmiessler.com/blog/personal-ai-future-state) - Le modèle de maturité en 9 niveaux
- [Building Your Own AI-powered Life Management System](https://newsletter.danielmiessler.com/p/building-your-own-ai-powered-life-management-system) - Newsletter
- [GitHub PAI](https://github.com/danielmiessler/Personal_AI_Infrastructure) - Le repo officiel

## Crédits

- **Inspiration** : [Daniel Miessler](https://danielmiessler.com/) - Personal AI Infrastructure
- **Base technique** : [Anthropic Skills](https://github.com/anthropics/skills) - Format de skills
- **Développement** : [Contexte Collectif](https://github.com/contexte-collectif)

## Licence

**MIT** - Une licence permissive qui permet :
- Utiliser, copier, modifier le code librement
- Distribuer et même vendre des versions modifiées
- Utiliser dans des projets commerciaux ou privés

Seule obligation : conserver la mention de copyright et de licence.

En gros : faites ce que vous voulez, mais ne nous tenez pas responsables.
