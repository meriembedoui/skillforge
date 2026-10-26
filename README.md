# SkillForge

Socle commun d’une plateforme web d’apprentissage par compétences. Le projet
présente la vision SkillForge et fournit une base Django, des layouts et des
composants réutilisables pour le travail de l’équipe.

**Les modules métier ne sont pas encore intégrés.** La landing page est une
présentation. Son aperçu de progression est une maquette statique, identifiée
comme telle : aucune donnée utilisateur, aucun cours ou résultat n’est créé.
Aucune infrastructure IA/ML n’est incluse dans ce socle.

## Prérequis

- Python 3.12 à 3.14 pour Django **6.1.2**.
- SQLite, fourni avec Python ; aucune base externe nécessaire en local.
- Aucun outil Node, framework frontend ou service externe nécessaire.

Sur la machine actuelle, utiliser **`.venv-django61`** (Python 3.12.14). L’ancien
`.venv` sous Python 3.15 / Django 4.2 a été conservé ; il ne correspond pas au
socle actuel. Ne pas confondre les deux environnements.

## Installation après clonage

Depuis la racine du projet, avec un Python compatible installé :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\Activate.ps1
python --version
python -m django --version
python manage.py check
python manage.py migrate
python manage.py test
python manage.py runserver
```

Si l’activation PowerShell est indisponible, utiliser directement
`.\.venv\Scripts\python.exe` à la place de `python`, sans modifier les stratégies
de sécurité du système.

Sur cette machine, l’environnement est déjà prêt :

```powershell
.\.venv-django61\Scripts\python.exe manage.py runserver
```

Ouvrir http://127.0.0.1:8000/. Arrêter avec Ctrl+C.
`migrate` ne concerne pour l’instant que admin, auth, contenttypes et sessions.
Les quatre packages de requirements sont Django et ses dépendances figées.

## Architecture actuelle

```text
config/
  settings.py, urls.py, views.py, environment.py
core/
  templatetags/skillforge_ui.py       helper de pagination
  tests/test_foundation.py           tests du socle
templates/
  base.html                         structure globale
  home.html                         présentation EdTech
  403.html, 404.html, 500.html        erreurs personnalisées
  components/
    brand.html, icon.html
    navbar.html, navigation_links.html, footer.html
    messages.html, breadcrumbs.html, pagination.html
  layouts/
    public.html                     présentation publique
    workspace.html                  structure générique d’un espace
    learner.html, mentor.html, admin.html
static/
  css/
    base.css                        tokens, police et typographie
    components.css                  composants communs, navbar et footer
    home.css                        composition de la landing page
    responsive.css                  responsive de la landing page
    workspace.css, learner.css, mentor.css, admin.css
    public.css, style.css            entrées de compatibilité
  js/main.js                        interactions du menu mobile
  fonts/InterVariable.woff2, OFL.txt
  images/favicon.svg
```

Les layouts d’espace sont de simples fondations, sans pages, permissions ou
modèles métier. `layouts/admin.html` ne remplace pas `/admin/`, qui reste
l’administration standard Django. Les vues futures devront contrôler leurs accès.

## Templates et design system

Les pages publiques étendent `layouts/public.html` et définissent title et content.
`base.html` fournit métadonnées, police, CSS communs, navigation, messages, skip link,
main et footer. Blocs disponibles : title, extra_css, extra_js, body_class,
navigation, main_class et content.

Les layouts génériques d’espace fournissent page_heading (h1), workspace_label,
workspace_navigation et workspace_content. Ils n’exigent aucune app métier.
Conserver un seul h1 par page, puis organiser les sections avec h2 et h3.

Palette : crème #fff8f1, beige #cbac91, pêche #ffeddf, brun #76523b, surfaces blanches.
Les variables de `base.css` couvrent couleurs, police, espacements, radius, ombres,
largeur et transitions. Les alias `--color-*` conservent la compatibilité des
layouts existants. Les composants incluent :

- container, section, page-header, card, badge, alert et empty-state ;
- btn / button avec btn-primary, btn-secondary, btn-ghost et btn-danger ;
- form-group, form-control, help-text et error-message ;
- table-wrapper, progress, breadcrumb et pagination.

Les variantes success, warning, danger et info gardent un sens textuel explicite.
Ne pas charger style.css ou public.css en plus des CSS déjà chargés par les layouts.
Les helpers de pagination conservent les filtres et leurs valeurs multiples.
Les données de breadcrumbs doivent contenir des URL construites côté serveur.

## Accessibilité et interface

Le menu mobile utilise un `<details>` natif : il fonctionne aussi sans JavaScript.
Le JS ajoute Échap, fermeture après navigation/clic extérieur et gestion du focus
lors d’un changement de taille. Le menu desktop et le menu mobile partagent un
seul composant de liens ; un seul est visible à la fois.

Focus visible, skip link, langue française, hiérarchie des titres, zones sémantiques
et prefers-reduced-motion sont prévus. Chaque futur champ doit avoir un label
visible et des aides/erreurs associées par aria-describedby. Ajouter aria-invalid
seulement en cas d’erreur. Conserver csrf_token pour les formulaires POST.

Donner un alt utile aux futures images significatives, un alt vide aux décoratives.
Les SVG décoratifs actuels sont cachés des technologies d’assistance. Les tableaux
ont un caption et des th avec scope ; rendre le conteneur défilable au clavier si
nécessaire. Chaque progress natif doit avoir un nom et une valeur textuelle.

Inter est servie localement, avec fallback système et font-display: swap.
Source : [projet officiel Inter](https://github.com/rsms/inter), sous licence
SIL Open Font License 1.1 incluse dans `static/fonts/OFL.txt`. Aucun CDN requis.

## Configuration et sécurité

Langue `fr-fr`, timezone `Africa/Tunis`, configurable par TIME_ZONE. Les secrets
viennent de l’environnement. `.env.example` donne les noms et des exemples vides ;
**.env n’est pas chargé automatiquement**. Exporter les valeurs dans le shell ou
utiliser le gestionnaire de secrets du futur déploiement.

Sans DJANGO_SECRET_KEY en développement, une clé aléatoire persistante est créée
localement dans `.development-secret`. Ce fichier, les .env, environnements,
SQLite et caches Python sont ignorés. Ne jamais les partager.

DEBUG=False exige DJANGO_SECRET_KEY et des DJANGO_ALLOWED_HOSTS explicites. Cookies
sécurisés et redirection HTTPS sont alors activés. Le déploiement devra encore
préparer TLS, serveur WSGI/ASGI, fichiers statiques, sauvegardes et journalisation.
Le serveur runserver sert au développement. CSRF et l’authentification standard
Django restent actifs ; aucun système d’authentification personnalisé n’est ajouté.

Les pages d’erreur personnalisées sont utilisées avec DEBUG=False. En DEBUG=True,
la vraie 404 de développement affiche le diagnostic Django. Aucune route de QA
n’est incluse. La page d’erreur CSRF utilise son gestionnaire Django distinct.

## Vérifier le socle

```powershell
.\.venv-django61\Scripts\python.exe manage.py check
.\.venv-django61\Scripts\python.exe manage.py migrate
.\.venv-django61\Scripts\python.exe manage.py test
```

Après clonage, adapter le chemin du venv local. Contrôler aussi la landing page à
1440, 1024, 768 et 390 px, le zoom 200 %, les ancres, Tab, Entrée, Échap et le pied
de page. Un audit Lighthouse réel reste nécessaire avant d’annoncer un score.

Les modules accounts, learning, assessment, mentoring et certification seront
ajoutés ensuite par leurs responsables, sur leurs branches respectives. Ils ne
sont pas présents dans cette version. Les opérations Git restent manuelles.
