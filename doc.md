# Documentation Technique & Architecture Détaillée

L'outil est développé en **Python** et utilise le framework **PySide6** (Qt) pour l'interface graphique.

Il repose sur une séparation stricte des responsabilités grâce au pattern de conception **MVC (Modèle-Vue-Contrôleur)**.

---

## 1. Architecture Logicielle (MVC)

L'architecture est découpée en trois couches distinctes.

### 1.1. Le Modèle (`model.py`)
Le **Modèle** (`AutomatonModel`) est le cœur de l'application. Il est totalement agnostique de l'interface graphique (il n'importe aucun module PySide6).
*   **État Interne (`self.data`)** : Il stocke l'intégralité des données de l'automate (localités, transitions, variables C/C++, horloges, actions, état initial) sous forme d'un dictionnaire Python standard.
*   **Logique Métier (CRUD)** : Il expose des méthodes pour Créer, Lire, Mettre à jour et Supprimer des éléments (ex: `add_location`, `add_transition_guard`, `delete_action`).
*   **Intégrité** : Il est garant de la cohérence des données (ex: supprimer une horloge la retire de toutes les contraintes existantes).
*   **Persistance** : Il gère le chargement et l'exportation au format JSON, en déléguant la conversion mathématique au moteur DBM.

### 1.2. La Vue (`View/`)
La **Vue** gère exclusivement l'affichage et l'interaction avec l'utilisateur. Elle ne modifie **jamais** le modèle directement.
*   **Composants Indépendants** : L'interface est découpée en plusieurs fichiers selon les éléments graphiques (Fenêtre principale, Canvas de dessin, Popups, Éditeur de données).
*   **Signaux (Signals)** : La Vue communique avec le monde extérieur (le Contrôleur) en émettant des événements via le mécanisme de signaux de Qt (ex: `canvas_clicked`, `node_selected`).

### 1.3. Le Contrôleur (`controller.py`)
Le **Contrôleur** (`MainController`) est le chef d'orchestre. Il fait le pont entre la Vue et le Modèle.
*   **Abonnement aux Signaux** : Au démarrage, il connecte les signaux émis par la Vue à ses propres méthodes (les *slots*).
*   **Orchestration** : Lorsqu'un événement survient (ex: l'utilisateur valide l'ajout d'une garde), le contrôleur reçoit l'information, appelle la méthode appropriée du Modèle pour sauvegarder la donnée, puis donne l'ordre à la Vue de se rafraîchir pour afficher le changement.

---

## 2. Structure du Projet

```text
timed-automata-gui/
├── main.py                # Point d'entrée, initialisation MVC, style CSS/QSS global
├── model.py               # Le Modèle (AutomatonModel)
├── controller.py          # Le Contrôleur (MainController) 
├── doc.md                 # Cette documentation
├── README.md              # Manuel d'utilisation
│
├── View/                  # La Couche Visuelle (Vue)
│   ├── __init__.py
│   ├── window.py          # Fenêtre principale (MainWindow), barre d'outils, menus
│   ├── canvas.py          # Espace de dessin interactif (AutomataView / QGraphicsView)
│   ├── items.py           # Objets graphiques natifs (NodeItem, TransitionItem, NailItem) 
│   ├── properties_dock.py # Panneau latéral dynamique (Invariants, Gardes, Actions)
│   ├── data_editor.py     # Fenêtre d'édition avancée (Variables C/C++, #define, structs)
│   └── popups.py          # Fenêtres contextuelles rapides
│
├── utils/                 # Sous-outils transverses
    ├── __init__.py
    └── dbm_engine.py      # Couche de traduction bidirectionnelle (Dictionnaires UI <-> Matrices DBM) 
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

---

## Flux de Données Typique (Exemple : Ajouter un Nœud)
Pour bien comprendre la maintenance, voici le cheminement d'une action de l'utilisateur à l'interface :

1. **Vue** : L'utilisateur clique sur le `canvas`. `AutomataView` émet le signal `canvas_clicked(x, y)`.
2. **Contrôleur** : `MainController.handle_canvas_click` reçoit le signal.
3. **Modèle** : Le contrôleur appelle `model.add_location(x, y)` qui crée l'ID et stocke la donnée dans `self.data`.
4. **Mise à jour Vue** : Le contrôleur appelle `view.canvas.draw_node(...)` pour faire apparaître le cercle à l'écran.