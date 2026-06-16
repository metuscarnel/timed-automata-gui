# Documentation Technique

L'application repose sur le pattern de conception **MVC (Modèle-Vue-Contrôleur)** implémenté en Python.


---

## Structure du Projet

Pour faciliter la navigation dans le code, voici l'arborescence complète du code de l'outil :

```text
timed-automata-gui/
├── main.py                # Point d'entrée de l'application
├── model.py               # Modèle de données (AutomatonModel)
├── controller.py          # Logique métier et orchestration (MainController)
├── doc.md                 # Ce fichier (Documentation technique architecturale)
├── README.md              # Manuel d'utilisation et présentation globale
│
├── View/                  # Interface Graphique (Vue)
│   ├── __init__.py
│   ├── window.py          # Fenêtre principale et menus (MainWindow)
│   ├── canvas.py          # Espace de dessin interactif (AutomataView)
│   ├── items.py           # Éléments graphiques natifs (NodeItem, TransitionItem...)
│   ├── properties_dock.py # Panneau latéral d'édition (Invariants, Gardes, Actions)
│   ├── data_editor.py     # Fenêtre d'édition des variables C/C++ étendues
│   └── popups.py          # Fenêtres contextuelles rapides
│
└── utils/                 # Utilitaires et Moteurs de conversion
    ├── __init__.py
    └── dbm_engine.py      # Conversion mathématique bidirectionnelle (UI <-> DBM)
│
└── resources/             # Ressources statiques de l'application
    ├── images/            # Captures d'écran pour le manuel d'utilisation
    └── icons.py           # Dictionnaire d'icônes
```

---

## Les Fichiers et Classes Clés

### 1. Point d'entrée (`main.py`)
* Instancie le classes maitresses MVC (`AutomatonModel`, `MainController`, `MainWindow`).
* Définit la feuille de style globale (CSS/QSS) de l'application.

### 2. Le Modèle (`model.py`)
* **Classe `AutomatonModel`** :
* Possède l'attribut `self.data`, un dictionnaire qui comprends à une instants les élements de définitions du modèle(localités, transitions, horloges, actions, variables).
* Contient uniquement des méthodes **CRUD** (Create, Read, Update, Delete) pour manipuler les données.
* Gère la lecture (`load_from_json_data`) et l'écriture (`export_to_json`) des fichiers de sauvegarde.

### 3. Le Contrôleur (`controller.py`)
* **Classe `MainController`** : Le contrôleur.
* Intercepte les signaux de l'interface (ex: `handle_canvas_click`, `handle_delete_node`).
* Exécute la logique métier (vérification anti-doublon des contraintes, etc.).
* Met à jour le `model`, puis appelle les méthodes de la `view` pour refléter les changements.

### 4. La Vue (`View/`)
Gère exclusivement l'affichage et l'interaction utilisateur.
* **`window.py` (`MainWindow`)** : La fenêtre principale. Contient la structure (menus, barre d'outils, layout global).
* **`canvas.py` (`AutomataView`)** : L'espace de dessin interactif (`QGraphicsView`). Gère la machine à états de la création visuelle (pose de clous temporel, tracer une ligne, etc.).
* **`items.py` (`NodeItem`, `TransitionItem`, `NailItem`)** : Les éléments graphiques natifs (`QGraphicsItem`). 
    * *Spécificité* : Ils gèrent eux-mêmes leur apparence (cercle, flèche courbée) et intègrent l'algorithme d'esquive des obstacles (`TransitionItem.update_position`).
* **Docks & Popups** (`properties_dock.py`, `data_editor.py`, `popups.py`) : Formulaires d'édition des propriétés (Invariants, Gardes, Variables C/C++).

### 5. Moteur Mathématique / Conversion (`utils/dbm_engine.py`)
Le projet traduit les contraintes sous leurs expressions textuelles en matrices mathématiques (DBM) pour le JSON, et vis-versa.
* **`utils/dbm_engine.py`** : Centralise toute la logique de conversion :
    * Transforme les dictionnaires UI en texte, puis en matrice **DBM** lors de la sauvegarde (`generate_and_save_engine_json`).
    * Fait l'opération inverse (Matrice DBM ➔ format UI) lors de l'ouverture d'un fichier existant (`dbm_to_string_constraints`).
### 6. Resources statiques (`resources`)
Sont présents dans ce dossier :
* `icons.py` ** : contient des svg des icônes utilisées au niveau de la toolbar
* `resources/images` : contient les captures d'écrans utilisées dans la guide d'utilisation
---

## Flux de Données Typique (Exemple : Ajouter un Nœud)
Voici le cheminement d'une action de l'utilisateur à l'interface :

1. **Vue** : L'utilisateur clique sur le `canvas`. `AutomataView` émet le signal `canvas_clicked(x, y)`.
2. **Contrôleur** : `MainController.handle_canvas_click` reçoit le signal.
3. **Modèle** : Le contrôleur appelle `model.add_location(x, y)` qui crée l'ID et stocke la donnée dans `self.data`.
4. **Mise à jour Vue** : Le contrôleur appelle `view.canvas.draw_node(...)` pour faire apparaître le cercle à l'écran.