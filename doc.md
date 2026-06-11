# Documentation Architecturale

L'application repose sur le patron de conception **MVC (Modèle-Vue-Contrôleur)** implémenté avec **PySide6**. 
* **Règle d'or** : Le Modèle ignore l'existence de la Vue. La Vue émet des signaux sans modifier les données. Le Contrôleur écoute la Vue, met à jour le Modèle, puis demande à la Vue de se rafraîchir.

---

## Les Fichiers et Classes Clés

### 1. Point d'entrée (`main.py`)
* Instancie le trio MVC (`AutomatonModel`, `MainController`, `MainWindow`).
* Définit la feuille de style globale (CSS/QSS) de l'application.

### 2. Le Modèle (`model.py`)
* **Classe `AutomatonModel`** : Le cerveau des données. 
* Possède l'attribut `self.data`, un dictionnaire géant qui représente l'état exact de l'automate (localités, transitions, horloges, actions, variables).
* Contient uniquement des méthodes **CRUD** (Create, Read, Update, Delete) pour manipuler les données.
* Gère la lecture (`load_from_json_data`) et l'écriture (`export_to_json`) des fichiers de sauvegarde.

### 3. Le Contrôleur (`controller.py`)
* **Classe `MainController`** : Le chef d'orchestre.
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
Le projet traduit les contraintes lisibles par l'humain en matrices mathématiques (DBM) pour le JSON de manière bi-directionnelle.
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