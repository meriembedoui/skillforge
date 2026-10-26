# Rapport de vérification et refonte du socle SkillForge

## Revalidation du 26 octobre 2026

La nouvelle demande reprend le périmètre déjà livré : l’état initial de cette
revalidation était un socle léger, sans app métier ni infrastructure IA/ML,
avec Django 6.1.2 / Python 3.12.14 et huit tests réussis.

Aucune erreur bloquante n’a été trouvée. Deux ajustements de présentation ont
été apportés : le CTA secondaire du hero devient « Commencer » vers l’aperçu,
et le titre isole son contexte d’affichage pour son surlignage décoratif.

**Fichiers créés pendant cette revalidation : aucun.**
Fichiers modifiés :

- `templates/home.html` : libellé et ancre du CTA secondaire du hero.
- `static/css/home.css` : isolation du contexte d’affichage du titre.
- `RAPPORT_SOCLE.md` : résultats de cette revalidation.

Vérifications réexécutées :

- Python 3.12.14 ; Django 6.1.2 ; `pip check` sans problème.
- `manage.py check` : System check identified no issues (0 silenced).
- `manage.py migrate` : No migrations to apply.
- `manage.py test` : 8 tests, OK.
- Navigateur : 1440, 1024, 768 et 390 px, un h1, aucun débordement horizontal.
- Menu : fermeture avec Échap et après sélection d’une ancre, sans erreur console.
- Vraie 404 personnalisée vérifiée sur localhost dans un processus temporaire
  DEBUG=False ; processus arrêté, sans route QA ni changement des settings.
- Aucun dossier métier/IA/ML, aucune dépendance IA/ML et aucune commande Git.

La structure, le design system, les mesures d’accessibilité et la sécurité décrits
ci-dessous sont conservés. Le serveur principal reste accessible sur le port 8000.
Un audit Lighthouse chiffré, un contrôle lecteur d’écran et le zoom 200 % restent
à effectuer ; aucun score d’audit n’est annoncé.

Les sections suivantes documentent la refonte initiale et son inventaire complet.

Travail réalisé uniquement dans `C:\Users\merie\skillforge`, sans commande Git,
sans changement de branche, sans copie de `skillforge_test` et sans module métier.
Le serveur principal reste disponible sur http://127.0.0.1:8000/.

## État initial trouvé

- Python 3.12.14 / Django 6.1.2 dans `.venv-django61` ; ancien `.venv` Python 3.15 / Django 4.2 conservé.
- Configuration locale fonctionnelle, templates globaux et fichiers statiques configurés.
- `check` réussi, migrations standard déjà appliquées, 21 tests initialement réussis.
- Seules les tables standard Django sont présentes dans SQLite (auth, admin, contenttypes, sessions et migrations).
- Présence de core/ai, core/ml, ml et de leurs dépendances, ajoutés à l’étape précédente.
- Documentation orientée vers cette infrastructure, qui ne correspond plus au nouveau périmètre.
- Landing page beige existante, mais sans Inter locale, parcours visuel en six étapes ni aperçu statique demandé.

## Écarts et corrections

Aucune erreur Django bloquante n’était présente dans l’environnement compatible.
Le principal écart concernait le périmètre et les dépendances inutilisées.
L’infrastructure IA/ML, ses tests et le composant ai_status ont été retirés.
Une archive vérifiée a été conservée hors du dépôt, sans secret ni base de données :

`C:\Users\merie\.codex\visualizations\2026\10\25\01a172af-b403-7ea2-9d72-f64cdda5f801\skillforge-infrastructure-ia-ml-archive.zip`

Cette archive contient aussi le rapport de l’étape précédente. Elle ne doit pas être
réintégrée au socle actuel. Les packages IA/ML et leurs dépendances ont également été
retirés du venv compatible. `pip check` ne signale aucun problème. L’ancien venv
n’a pas été supprimé.

Le menu mobile repose maintenant sur le HTML natif `<details>`, utilisable sans JS.
Le JS ajoute la fermeture avec Échap, après sélection d’un lien, au clic extérieur,
et le transfert du focus lors d’un changement de largeur.

## Fichiers créés

| Fichier | Modification / rôle |
|---|---|
| `static/css/home.css` | Composition de la landing page et de ses illustrations CSS. |
| `static/css/responsive.css` | Adaptation de la landing page aux tablettes et mobiles. |
| `static/fonts/InterVariable.woff2` | Police Inter variable servie localement. |
| `static/fonts/OFL.txt` | Licence officielle de la police Inter. |
| `static/images/favicon.svg` | Identité SkillForge dans l’onglet du navigateur. |
| `templates/components/brand.html` | Marque commune, logo vectoriel et nom. |
| `templates/components/footer.html` | Pied de page commun et navigation secondaire. |
| `templates/components/icon.html` | Petites icônes SVG décoratives, sans bibliothèque externe. |
| `templates/components/navbar.html` | Navbar desktop et menu mobile natif. |
| `templates/components/navigation_links.html` | Liens communs réutilisés dans les deux affichages. |

## Fichiers modifiés

| Fichier | Modification / rôle |
|---|---|
| `.env.example` | Retrait des variables IA inutilisées ; exemples sans secret conservés. |
| `.gitignore` | Retrait des anciennes règles ML ; secrets, venv, DB et caches toujours ignorés. |
| `RAPPORT_SOCLE.md` | Rapport actualisé de cette étape. |
| `README.md` | Documentation réécrite autour du socle léger réellement présent. |
| `config/urls.py` | Documentation de routes nettoyée ; seules / et /admin/ sont conservées. |
| `core/tests/test_foundation.py` | Retrait de la référence au composant IA supprimé ; tests génériques conservés. |
| `requirements.txt` | Django 6.1.2 et ses trois dépendances uniquement. |
| `static/css/base.css` | Inter locale, palette, échelle typographique, espacements et tokens. |
| `static/css/components.css` | Boutons, cards, formulaires, navbar, footer, erreurs et composants communs. |
| `static/css/public.css` | Entrée de compatibilité vers home.css et responsive.css. |
| `static/css/style.css` | Entrée de compatibilité vers les CSS communs et publics. |
| `static/js/main.js` | Menu natif : Échap, ancres, clic extérieur et focus lors du redimensionnement. |
| `templates/403.html` | Page d’accès refusé avec l’identité SkillForge. |
| `templates/404.html` | Page introuvable personnalisée et retour à l’accueil. |
| `templates/500.html` | Erreur serveur personnalisée et retour à l’accueil. |
| `templates/base.html` | Métadonnées, police locale, CSS communs, composants navbar/footer, skip link et main. |
| `templates/home.html` | Hero illustré, parcours en six étapes, valeurs, aperçu statique et présentation académique. |
| `templates/layouts/public.html` | Chargement explicite de home.css et responsive.css. |

## Fichiers retirés et archivés

Les suppressions ci-dessous sont justifiées par l’interdiction explicite de
conserver de l’IA/ML dans le nouveau socle ; aucune app métier n’a été supprimée,
car aucune n’existait. Les caches associés sont ignorés et ont été nettoyés.

| Fichier | Modification / rôle |
|---|---|
| `core/ai/__init__.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `core/ai/client.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `core/ai/schemas.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `core/ml/__init__.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `core/ml/predictor.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `core/tests/test_ai.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `core/tests/test_ml.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `ml/README.md` | Retiré du socle conformément au périmètre sans IA/ML. |
| `ml/__init__.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `ml/datasets/.gitkeep` | Retiré du socle conformément au périmètre sans IA/ML. |
| `ml/evaluation/.gitkeep` | Retiré du socle conformément au périmètre sans IA/ML. |
| `ml/models/.gitkeep` | Retiré du socle conformément au périmètre sans IA/ML. |
| `ml/schema.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `ml/training/__init__.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `ml/training/train.py` | Retiré du socle conformément au périmètre sans IA/ML. |
| `templates/components/ai_status.html` | Retiré du socle conformément au périmètre sans IA/ML. |

## Version Django et dépendances

Version finale : **Django 6.1.2 / Python 3.12.14**.
`requirements.txt` contient uniquement :

```text
asgiref==3.13.0
Django==6.1.2
sqlparse==0.6.0
tzdata==2026.5
```

Aucun pandas, scikit-learn, joblib, jsonschema, SDK IA, framework JS ou bibliothèque
CSS n’est requis ou installé dans le venv compatible. La police Inter est un
asset local de 352 240 octets, accompagné de sa licence SIL OFL 1.1.
Source : [projet officiel Inter](https://github.com/rsms/inter).

## Architecture templates et CSS

`base.html` fournit les métadonnées, les assets communs, le skip link, le main,
les messages, la navbar et le footer. Les composants de marque, icônes, liens,
navbar et footer sont indépendants des futurs modules. Messages, breadcrumbs et
pagination restent disponibles.

`layouts/public.html` ajoute les styles de présentation. Les layouts génériques
workspace, learner, mentor et admin sont conservés comme fondations sans route,
modèle, rôle ni logique métier. `/admin/` reste l’admin standard Django.

CSS : base (tokens et typographie), components (éléments partagés), home
(composition publique), responsive (breakpoints publics). Les styles des layouts
génériques restent séparés. style.css et public.css restent des points d’entrée
de compatibilité, sans duplication de leurs anciennes règles.

Le design system contient palette crème/beige, variantes d’état, Inter avec
fallback système, espacements, ombres légères, radius, largeur de conteneur et
transitions. Boutons primary/secondary/ghost/danger avec hover, focus et disabled ;
cards, badges, alerts, champs, tables, progress, empty-state et breadcrumbs.

## Landing page

- Hero : titre et sous-titre demandés, CTA à ancres valides, formes et cartes graphiques.
- Parcours Explorer → Apprendre → Pratiquer → Progresser → Être accompagné → Valider.
- Présentation des six concepts futurs, sans implémentation métier.
- Aperçu statique de progression : valeurs illustratives du brief, explicitement signalées.
- Section académique À propos et invitation finale à explorer la vision du produit.
- Footer discret avec marque, navigation et copyright.

Aucun compte, cours, mentor, quiz, résultat ou certificat n’a été créé.
L’aperçu ne fait aucune requête métier et n’est connecté à aucune donnée.

## Responsive et navigateur

Accueil contrôlé à **1440, 1024, 768 et 390 px** : aucun débordement horizontal,
un seul h1 et composition adaptée. La navbar devient un menu hamburger natif sur
petits écrans ; les deux versions partagent la même source de liens.

Vérifications réussies dans le navigateur :

- menu ouvert au clic et au clavier, refermé avec Entrée et Échap ;
- sélection de Fonctionnalités : menu refermé, ancre atteinte à 32 px du haut ;
- skip link : focus transféré au main ;
- navigation et pied de page présents ; liens internes vérifiés par les tests ;
- console sans erreur ni avertissement important lors du contrôle ;
- vraie 404 personnalisée vérifiée en DEBUG=False sur un serveur localhost temporaire.

Le serveur temporaire de 404 a été arrêté ; aucune route ni configuration QA n’a
été ajoutée au projet. Le navigateur est revenu au serveur normal sur le port 8000.

## Accessibilité

Langue française, structure sémantique, un h1 par page, hiérarchie des titres,
SVG décoratifs cachés des technologies d’assistance, progress nommés, focus visible,
skip link et préférence de réduction des mouvements pris en compte. Les futurs
labels, erreurs, images et tableaux sont documentés dans le README.

Contrastes des principales paires de texte calculés selon la luminance WCAG :

| Texte / fond | Ratio |
|---|---:|
| #1f1f1f / #fff8f1 | 15,66:1 |
| #6b625c / #fff8f1 | 5,66:1 |
| #ffffff / #76523b | 6,91:1 |
| #76523b / #ffeddf | 6,06:1 |
| #4b6042 / #eaf0e5 | 5,93:1 |

Ces contrôles ne remplacent pas un audit complet. Aucun score Lighthouse n’est
annoncé. Un contrôle lecteur d’écran et au zoom 200 % reste recommandé.

## Sécurité et .gitignore

CSRF et authentification Django conservés. Pas de secret API, de clé sensible en
dur, de SQL brut ou de configuration métier ajouté. Langue fr-fr et timezone
Africa/Tunis conservées. Les secrets viennent de l’environnement, avec un secret
local ignoré pour le développement. .env.example ne contient plus de variables IA.

.gitignore conserve .venv/, .venv-django61/, __pycache__/, *.pyc, db.sqlite3, .env,
.development-secret, .vscode/, .idea/ et staticfiles/. Les anciennes exclusions ML
ont été retirées, car ces dossiers n’existent plus. .git n’a pas été touché.

## Résultats finaux

- `python --version` : Python 3.12.14 dans l’environnement compatible.
- `python -m django --version` : 6.1.2.
- `python manage.py check` : **System check identified no issues (0 silenced).**
- `python manage.py migrate` : succès, **No migrations to apply.**
- `python manage.py test` : **8 tests, OK.**
- `python -m pip check` : **No broken requirements found.**
- `python manage.py runserver` : démarré avec rechargement automatique sur 127.0.0.1:8000.

Les 13 tests IA/ML ont été retirés avec les fonctionnalités exclues ; les huit
tests restants couvrent le socle, les layouts, les erreurs, les composants et la
configuration, sans créer de base de test ni données métier.

## Commandes et points restant à traiter

Sur cette machine :

```powershell
.\.venv-django61\Scripts\python.exe manage.py check
.\.venv-django61\Scripts\python.exe manage.py migrate
.\.venv-django61\Scripts\python.exe manage.py test
.\.venv-django61\Scripts\python.exe manage.py runserver
```

Le serveur est déjà lancé ; ne pas démarrer un deuxième processus sur le même port.
Après clonage, suivre le README pour créer un venv avec Python compatible.

Aucun problème bloquant identifié. Restent un audit Lighthouse réel, les contrôles
lecteur d’écran/zoom, puis plus tard l’intégration des modules et la configuration
spécifique au déploiement. Le socle n’est pas présenté comme une application métier
complète ou une configuration de production achevée.

**Aucun dossier accounts, learning, assessment, mentoring, certification, core/ai,
core/ml ou ml n’est présent. Aucune table ni migration métier n’a été créée.
Aucune commande Git n’a été exécutée.**
