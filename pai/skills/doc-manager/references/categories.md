# Categories de Documentation

Reference des categories utilisees par `doc-manager`.

## Categories principales

### `architecture/`
Documentation stable sur l'architecture du projet.

**Prefixes detectes** :
- PRD, SPEC, MODEL, SCHEMA
- OVERVIEW, ARCHITECTURE, DESIGN
- STRUCTURE, DATA_MODEL

**Exemples** :
- `PRD.md` -> `docs/architecture/prd.md`
- `DATA_MODEL_V2.md` -> `docs/architecture/data-model-v2.md`

### `devbooks/`
Documentation vivante liee au developpement.

**Prefixes detectes** :
- FIX_, BUG_, RESOLUTION_
- INVESTIGATION_, DEBUG_, HOTFIX_
- RAPPORT_, VERIFICATION_

**Exemples** :
- `FIX_BUG_123.md` -> `docs/devbooks/fix-bug-123.md`
- `RAPPORT_ANALYSE_REGRESSION.md` -> `docs/devbooks/rapport-analyse-regression.md`

### `research/`
Analyses et recherches.

**Prefixes detectes** :
- ANALYSE_, ANALYSIS_
- COMPARE_, COMPARATIF_
- VEILLE_, BENCHMARK_
- EVALUATION_, ETUDE_

**Exemples** :
- `ANALYSE_PERF_API.md` -> `docs/research/analyse-perf-api.md`
- `COMPARATIF_LIBS.md` -> `docs/research/comparatif-libs.md`

### `reference/`
Documentation de reference.

**Prefixes detectes** :
- API_, CONFIG_, GUIDE_
- DOC_, REFERENCE_
- SETUP_, INSTALL_

**Exemples** :
- `API_ENDPOINTS.md` -> `docs/reference/api-endpoints.md`
- `GUIDE_INSTALLATION.md` -> `docs/reference/guide-installation.md`

### `data/`
Fichiers de donnees.

**Extensions detectees** :
- `.csv`, `.xlsx`, `.xls`
- `.json` (hors package.json, tsconfig.json, etc.)
- `.geojson`, `.xml`
- `.yaml`, `.yml` (hors config)

**Exemples** :
- `export_2024.csv` -> `data/export-2024.csv`
- `parcelles.geojson` -> `data/parcelles.geojson`

### `archive/`
Fichiers obsoletes ou historiques.

**Prefixes detectes** :
- OLD_, ARCHIVE_, DEPRECATED_
- BACKUP_, CHANGELOG_YYYY

**Detection automatique** :
- Fichiers avec dates dans le nom (`_20240115`, `_2024-01-15`)

**Exemples** :
- `CHANGELOG_2024-11-06.md` -> `_archive/changelog-2024-11-06.md`
- `OLD_CONFIG.md` -> `_archive/old-config.md`

### `ambiguous`
Fichiers non categorisables automatiquement.

**Conditions** :
- Aucun prefixe reconnu
- Confidence < 0.7

**Action requise** : Demander a l'utilisateur de choisir.

## Conventions de nommage

### Transformation automatique

| Original | Resultat |
|----------|----------|
| `MAJUSCULES` | `minuscules` |
| `Underscores_Here` | `underscores-here` |
| `CamelCase` | `camel-case` |
| `Date_20240115` | `date-20240115` |
| `Espaces ici` | `espaces-ici` |
| `Accents_éèà` | `accents-eea` |

### Fichiers ignores

Ces fichiers ne sont jamais deplaces :
- `README.md`, `CLAUDE.md`, `CONTRIBUTING.md`
- `LICENSE.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`
- `.env`, `.env.example`

### Dossiers ignores

Ces dossiers ne sont jamais scannes :
- `node_modules`, `.git`, `dist`, `build`
- `.next`, `__pycache__`, `.vscode`, `.idea`
- `vendor`, `coverage`, `.cache`

## Scores de confiance

| Score | Signification |
|-------|---------------|
| 0.9+ | Prefixe reconnu avec certitude |
| 0.7-0.9 | Prefixe probable |
| < 0.7 | Ambigu, demander confirmation |
