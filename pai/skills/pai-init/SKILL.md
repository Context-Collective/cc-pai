---
name: pai-init
description: |
  Initializes or updates a Personal AI Infrastructure (PAI).
  USE WHEN user says: initialise ma PAI, configure ma PAI, pai init,
  setup my PAI, or wants to configure their personal context.
---

# PAI Initialization

## Workflow

### Step 1: Check existing configuration

Check if `pai/context/ME.md` exists:
- **Exists** → Offer to update existing configuration
- **Does not exist** → Start full onboarding

### Step 2: Gather information (conversational)

Ask these questions one by one, adapting to user responses:

1. **Qui es-tu ?**
   - Ton rôle professionnel
   - Ton domaine d'expertise
   - Tes compétences clés

2. **Quels sont tes objectifs actuels ?**
   - Ce que tu cherches à accomplir
   - Court terme vs long terme

3. **Sur quels projets tu travailles ?**
   - Liste des projets actifs
   - Priorités

4. **Comment tu aimes travailler ?**
   - Tes préférences
   - Tes outils favoris
   - Ton style de travail

5. **Tes conventions ?**
   - Style de code préféré
   - Langue de travail
   - Formats préférés

### Step 3: Generate files

Based on responses, generate:

**pai/context/ME.md**
```markdown
# Mon Contexte Personnel

## Qui je suis
[Compiled from responses]

## Mes objectifs actuels
[Compiled from responses]

## Mes projets en cours
[Compiled from responses]

## Comment je travaille
[Compiled from responses]

## Mes conventions
[Compiled from responses]
```

**pai/state/CURRENT.md**
```markdown
# État Actuel

## Focus actuel
[Based on current priorities]

## Tâches en cours
- [ ] [First tasks based on objectives]

## Contexte de travail
[Initial context]

## Blocages / Questions
[None initially]
```

### Step 4: Confirm and explain

After generating files:
1. Show summary of what was created
2. Explain how Claude will use this context
3. Suggest next steps (create skills, start working)

## Guidelines

- Be conversational, not robotic
- Adapt questions based on previous answers
- Don't ask all questions at once - one topic at a time
- Provide examples when user seems unsure
- Keep files concise - this is a starting point, not a complete biography
