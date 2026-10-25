# SkillForge

Socle commun Django 4.2 pour une plateforme d’apprentissage par compétences.
Les fonctionnalités présentées sur l’accueil sont prévues, pas encore disponibles.
Aucune app métier n’est créée à ce stade.

## Installation locale (PowerShell)

Après avoir cloné le dépôt, depuis sa racine :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Les migrations ci-dessus initialisent uniquement les tables Django standard sur une
nouvelle installation. Ne pas partager l’environnement virtuel ou la base locale.
Ouvrir http://127.0.0.1:8000/. Arrêter le serveur avec Ctrl+C.
Les réglages actuels servent au développement local ; préparer les secrets,
les hôtes autorisés, les fichiers statiques et DEBUG avant toute mise en production.

## Organisation commune

- `config/` : configuration, routes et vue de présentation de l’accueil.
- `templates/base.html` : structure partagée, navigation, CSS et JS globaux.
- `templates/home.html` : présentation de la plateforme.
- `templates/403.html`, `404.html`, `500.html` : erreurs Django standard.
- `static/css/style.css` : palette et composants communs responsive.
- `static/js/main.js` : emplacement des interactions communes, sans dépendance.
- `static/images/` : futures images ; fournir un alt descriptif aux images
  significatives et un alt vide aux images purement décoratives.

Chaque page étend `base.html`, définit `title` et `content`, et contient un seul
h1. Utiliser ensuite h2 et h3 dans l’ordre. Les liens doivent pointer vers des
routes existantes ou des ancres présentes. La navbar reste utilisable sans JS.

## Composants réutilisables

Classes disponibles : `container`, `section`, `section-title`, `btn`,
`btn-primary`, `btn-secondary`, `card`, `badge`, `alert`, `form-group`,
`form-control`, `help-text`, `error-message`, `table-container`, `breadcrumbs`.
Le texte reste foncé sur les fonds beiges pour préserver le contraste.

Exemple d’association accessible pour un futur champ (aucun formulaire métier
n’est implémenté ici) :

```html
<div class="form-group">
  <label for="champ">Libellé du champ</label>
  <input class="form-control" id="champ" name="champ"
         aria-describedby="champ-aide champ-erreur" aria-invalid="true">
  <small id="champ-aide" class="help-text">Instruction utile.</small>
  <p id="champ-erreur" class="error-message">Erreur : indiquez une valeur valide.</p>
</div>
```

Ajouter `aria-invalid` et le message d’erreur seulement en cas d’erreur.
Conserver CSRF dans les futurs formulaires POST. Pour les alertes dynamiques,
choisir `role="status"` pour une information et `role="alert"` pour une erreur
urgente. Toujours écrire le sens du message, sans dépendre uniquement de sa couleur.

Pour les tableaux, prévoir un caption, des th avec scope et un conteneur
`table-container` ; si le tableau déborde, rendre le conteneur accessible au
clavier (`tabindex="0"`, `role="region"` et nom accessible).
Pour un fil d’Ariane, utiliser un nav nommé « Fil d’Ariane », une liste ordonnée
et `aria-current="page"` sur l’élément courant.

## Vérifications manuelles

- Tester à 320 px, 768 px et sur grand écran, ainsi qu’au zoom 200 %.
- Parcourir les liens avec Tab : lien d’évitement visible, focus lisible,
  accès au contenu et activation avec Entrée.
- Vérifier le CTA vers la section fonctionnalités et le retour à l’accueil.
- Lancer Lighthouse Accessibility dans le navigateur ; aucun score n’est
  garanti avant l’audit réel.
- Les pages d’erreur personnalisées sont utilisées par les gestionnaires Django
  avec DEBUG=False ; en mode développement, Django affiche ses pages de diagnostic.
  Une erreur CSRF 403 utilise son gestionnaire distinct.

## Travail en équipe

Le socle est destiné à `main`. Chaque membre créera son module dans sa propre
branche : `accounts`, `learning`, `assessment`, `mentoring` ou `certification`.
Aucun modèle, migration métier, CRUD, authentification personnalisée ou service IA
n’est fourni par ce socle.
