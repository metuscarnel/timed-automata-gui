# 🏗️ Documentation d'Architecture

**Guide technique pour développeurs et contributeurs**

---

## Table des Matières

1. [Vision Générale](#vision-générale)
2. [Pattern MVC](#pattern-mvc)
3. [Module : Model](#module--model)
4. [Module : View](#module--view)
5. [Module : Controller](#module--controller)
6. [Sérialisation & DBM](#sérialisation--dbm)
7. [Flux de Données Détaillés](#flux-de-données-détaillés)
8. [Optimisations & Performances](#optimisations--performances)
9. [Points d'Extension](#points-dextension)

---

## Vision Générale

### Objectif
Fournir une interface graphique **découpée** pour éditer des automates temporisés, avec séparation stricte entre :
- **Données** (Model)
- **Affichage** (View)
- **Logique métier** (Controller)

### Principes
1. **Unicité du Model** : source unique de vérité
2. **Passivité de la View** : uniquement affichage
3. **Statelessness du Controller** : arbitrage sans état interne
4. **Signaux/Slots** : communication asynchrone et faiblement couplée

---

## Pattern MVC

### Diagramme Complet

```
┌─────────────────────────────────────────────────────┐
│                    main.py                          │
│         (Entry Point + Qt Initialization)           │
└─────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐      ┌─────────┐    ┌──────────┐
   │  Model  │      │  View   │    │Controller│
   │ (Data)  │      │  (UI)   │    │ (Logic)  │
   └─────────┘      └─────────┘    └──────────┘
        │                │              │
   ┌─────────────────────┼──────────────┴────────┐
   │      Signaux Qt (Communication)              │
   │                                              │
   └──────────────────────────────────────────────┘
```

### Responsabilités

#### Model (Données)
```python
class AutomatonModel:
    # ✅ Responsabilités
    - Stocker l'état interne (locations, transitions, etc.)
    - Implémenter la logique métier (CRUD)
    - Valider les données
    - Aucune dépendance vers Qt ou la View
    
    # ❌ Pas responsable de
    - Afficher les données
    - Gérer les événements utilisateur
    - Communiquer directement avec la View
```

**Caractéristiques** :
- 🧠 **Intelligente** : logique métier complexe
- 📦 **Autonome** : peut être testée sans Qt
- 🔄 **Réactive** : émet des signaux à chaque changement

#### View (Présentation)
```python
class MainWindow(QMainWindow), AutomataView(QGraphicsView):
    # ✅ Responsabilités
    - Afficher les données du Model
    - Capturer les événements utilisateur
    - Émettre des signaux vers le Controller
    
    # ❌ Pas responsable de
    - Décider si une action est valide
    - Modifier les données directement
    - Implémenter la logique métier
```

**Caractéristiques** :
- 👁️ **Passive** : réactive, ne décide pas
- 📡 **Sensorielle** : captures clics/drags
- 🖼️ **Graphique** : utilise Qt et OpenGL

#### Controller (Orchestration)
```python
class MainController:
    # ✅ Responsabilités
    - Écouter les signaux de la View
    - Appeler les méthodes du Model
    - Ordonner à la View de se mettre à jour
    - Orchestrer les opérations multi-étapes
    
    # ❌ Pas responsable de
    - Stocker de l'état
    - Calculer la logique complexe
    - Afficher directement
```

**Caractéristiques** :
- 🎛️ **Arbitre** : décide quoi faire
- 📋 **Routeur** : dirige les messages
- 🧵 **Orchestrateur** : coordonne les étapes

---

## Module : Model

### Structure Interne

```python
class AutomatonModel:
    def __init__(self):
        self.data = {
            "locations": {},      # {loc_id: {"node_pos": {x, y}, "invariants": [...]}}
            "transitions": [],    # [{source, target, action, guards, resets, nails}]
            "clocks": [],         # ["x", "y", "z"]
            "actions": [],        # ["a", "b"]
            "init": None          # "l0" (état initial)
        }
        self.loc_counter = 0      # Pour générer l0, l1, l2...
        self.transition_counter = 0
```

### Opérations CRUD

#### Localités
```python
# CREATE
loc_id = model.add_location(x, y)
# → génère "l0", "l1", ...
# → retourne l'ID

# READ
locations = model.data["locations"]

# UPDATE
model.update_node_position(loc_id, new_x, new_y)

# DELETE
model.remove_location(loc_id)
# → supprime aussi les transitions connectées
```

#### Transitions
```python
# CREATE
model.add_transition(source_id, target_id, nails_positions)

# READ
transitions = [t for t in model.data["transitions"] 
               if t["source"] == "l0"]

# UPDATE
model.update_transition(source, target, **updates)

# DELETE
model.remove_transition(source, target)
```

#### Horloges & Actions
```python
# Horloges
model.add_clock("x")
model.add_clock("y")
clocks = model.data["clocks"]  # ["x", "y"]

# Actions
model.add_action("send")
model.add_action("recv")
actions = model.data["actions"]  # ["send", "recv"]

# Anti-doublons (silencieusement ignoriés si existent)
model.add_clock("x")  # Pas ajouté à nouveau
```

#### Contraintes
```python
# Invariants sur localités
model.add_node_invariant("l0", clock="x", operator="<=", value="5")

# Gardes sur transitions
model.add_transition_guard("l0", "l1", clock="x", operator=">", value="3")

# Resets
model.add_transition_reset("l0", "l1", "x")
model.add_transition_reset("l0", "l1", "y")
```

### Validation Interne

```python
def validate():
    # ✅ Vérifications
    - Chaque loc_id en transition existe
    - État initial existe
    - Horloges déclarées avant usage
    - Pas de transitions en doublon
    - Pas d'actions/horloges dupliquées
```

---

## Module : View

### Hiérarchie des Widgets

```
MainWindow (QMainWindow)
├── Canvas (AutomataView, QGraphicsView)
│   ├── QGraphicsScene
│   │   ├── NodeItem (QGraphicsEllipseItem) × N
│   │   │   ├── QGraphicsTextItem (label "l0")
│   │   │   ├── QGraphicsEllipseItem (bordure interne si init)
│   │   │   └── ItemIsMovable + ItemSendsGeometryChanges
│   │   ├── TransitionItem (QGraphicsPathItem) × M
│   │   │   ├── Flèche (QGraphicsPolygonItem)
│   │   │   └── NailItem (QGraphicsRectItem)
│   │   └── NailItem (QGraphicsRectItem) × K
│   └── mousePressEvent, mouseMoveEvent, wheelEvent...
├── Toolbar (QToolBar)
│   ├── Action "Localité"
│   ├── Action "Transition"
│   └── ActionGroup (mutually exclusive)
├── PropertiesDock (QDockWidget)
│   ├── Inspector (sélection)
│   ├── Invariants Editor
│   ├── Guards Editor
│   └── Resets Checkboxes
├── Popups (QDialog)
│   ├── DeclarationDialog (horloges/actions)
│   └── DataEditorDialog (texte long)
└── MenuBar (QMenuBar)
    ├── Fichier
    │   ├── Nouveau
    │   ├── Ouvrir
    │   ├── Sauvegarder
    │   └── Mode Débogage
    └── Édition
        └── ...
```

### Événements & Signaux

#### Canvas Signals
```python
# Définis dans AutomataView
canvas_clicked = Signal(float, float)           # Utilisateur clique vide
node_selected = Signal(str)                     # Un nœud est cliqué
transition_selected = Signal(str, str)          # Une transition est cliquée
selection_cleared = Signal()                    # Clic sur vide
node_moved = Signal(str, float, float)          # Nœud déplacé
nail_moved = Signal(float, float)               # Clou déplacé
transition_created = Signal(str, str, list)     # Transition créée (source, target, nails)
node_delete_requested = Signal(str)             # Clic droit + Delete
transition_delete_requested = Signal(str, str)  # Clic droit + Delete
```

#### MainWindow Signals
```python
# Connexions établies par le Controller
# (Pas de signaux définis, utilise directement les slots)
```

### Thème Visual

```css
/* Global Stylesheet (main.py) */
- Fond : #FAFAFA (blanc cassé)
- Texte : #2C2C2C (noir léger)
- Police : IBM Plex Mono
- Bordures : #E5E5E5 (gris clair)

/* Éléments Spécifiques */
- NodeItem : cercle noir 40px
- TransitionItem : flèche noire, 2px thickness
- NailItem : carrés gris 6×6px (invisible normalement)
- Sélection : surbrillance bleu/rose
```

---

## Module : Controller

### Rôle Fondamental

```python
class MainController:
    """
    Arbitre entre Model et View.
    - Ne stocke AUCUN état (sauf self.model et self.view)
    - Uniquement des slots qui réagissent aux signaux
    - Appelle Model pour CRUD, View pour affichage
    """
```

### Slots Principaux

#### Localités
```python
@Slot(bool)
def handle_add_location(self, checked):
    # Active/désactive le mode création localité
    if checked:
        self.view.canvas.set_creation_mode("location")
    else:
        self.view.canvas.set_creation_mode(None)

@Slot(float, float)
def handle_canvas_click(self, x, y):
    # Utilisateur clique sur le canvas
    if self.view.canvas.creation_mode == "location":
        loc_id = self.model.add_location(x, y)
        is_initial = (self.model.data.get("init") == loc_id)
        self.view.canvas.draw_node(loc_id, x, y, is_initial)
        self.view.update_locations_list(...)
```

#### Transitions
```python
@Slot(bool)
def handle_add_transition(self, checked):
    # Active/désactive le mode création transition
    if checked:
        self.view.canvas.set_creation_mode("transition")

@Slot(str, str, list)
def handle_transition_created(self, source_id, target_id, nails_pos):
    # Transition créée graphiquement par l'utilisateur
    self.model.add_transition(source_id, target_id, nails_pos)
    self.view.canvas.draw_transition(source_id, target_id, nails_pos)
```

#### Sélection & Edition
```python
@Slot(str)
def handle_node_selected(self, loc_id):
    # Utilisateur a cliqué sur un nœud
    # Affiche ses invariants dans le dock
    self.view.properties_dock.show()
    self.view.properties_dock.display_node_properties(self.model, loc_id)

@Slot(str, str)
def handle_transition_selected(self, source, target):
    # Utilisateur a cliqué sur une flèche
    # Affiche ses gardes/resets dans le dock
    self.view.properties_dock.show()
    self.view.properties_dock.display_transition_properties(self.model, source, target)
```

#### Suppression
```python
@Slot(str)
def handle_delete_node(self, loc_id):
    # Supprimer une localité
    self.model.remove_location(loc_id)
    self.view.canvas.remove_node_graphics(loc_id)
    # Supprimer aussi les transitions connectées
    self.view.canvas.remove_transitions_for_node(loc_id)

@Slot(str, str)
def handle_delete_transition(self, source, target):
    self.model.remove_transition(source, target)
    self.view.canvas.remove_transition_graphics(source, target)
```

#### Déplacement
```python
@Slot(str, float, float)
def update_node_position(self, loc_id, x, y):
    self.model.update_node_position(loc_id, x, y)
    # Les transitions connectées se mettent à jour automatiquement via itemChange()
```

---

## Sérialisation & DBM

### Format JSON Interne

```json
{
  "locations": {
    "l0": {
      "node_pos": {"x": 100, "y": 50},
      "invariants": [
        {
          "clock": "x",
          "operator": "<=",
          "type": "value",
          "value": "5"
        }
      ]
    }
  },
  "transitions": [
    {
      "source": "l0",
      "target": "l1",
      "action": "send",
      "guards": [
        {
          "clock": "x",
          "operator": ">",
          "type": "value",
          "value": "0"
        }
      ],
      "resets": ["x"],
      "nails": [{"x": 150, "y": 75}]
    }
  ],
  "clocks": ["x", "y"],
  "actions": ["send", "recv"],
  "init": "l0"
}
```

### Processus d'Export

```
Utilisateur → Fichier → JSON stocké
     │
     ↓
View.trigger_save_dialog()
     │
     ↓
Controller.handle_save()
     │
     ↓
Model.export_to_json(filepath)
     │
     ├─ Valider toutes les données
     ├─ Compiler contraintes → DBM (optional)
     └─ Écrire JSON

Résultat : fichier .json portable
```

### Processus d'Import

```
Fichier JSON → Utilisateur → Application en mémoire
     │
     ↓
View.trigger_open_dialog()
     │
     ↓
Controller.handle_open()
     │
     ↓
Model.load_from_json(filepath)
     │
     ├─ Lire JSON
     ├─ Valider structure
     ├─ Décompiler DBM → contraintes (optional)
     └─ Recréer state interne

Résultat : Model.data rempli, View affichée
```

### DBM (Difference Bound Matrix)

#### Concept
Une DBM représente un ensemble de contraintes temporelles sous forme matricielle :

```
Texte lisible :  x <= 5 AND x >= 0 AND y - x <= 10
                          ↓
DBM (stocké compact) :
  [
    [0, -5],  # x <= 5
    [-0, 0],  # x >= 0
    [10, ∞]   # y - x <= 10
  ]
```

#### Bénéfices
- 📦 Compact (matrice vs. ensemble de contraintes)
- ⚡ Opérations rapides (addition matricielle parallélisable)
- 🔬 Compatible UPPAAL, TiNA

#### Implémentation
- **Stockage** : Python list of lists
- **Compilation** : `serial.compile_constraints_to_dbm()`
- **Décompilation** : `model.extract_constraints_from_dbm()`

---

## Flux de Données Détaillés

### Scénario 1 : Créer une Localité

```
1. Utilisateur clique sur bouton "Localité" dans toolbar
   └─ View.handle_add_location(checked=True)
   └─ Signal: action_group.triggered(action)

2. Controller écoute ce signal
   └─ Controller.handle_add_location(checked=True)
   └─ Canvas.set_creation_mode("location")

3. Utilisateur clique sur le canvas
   └─ Canvas.mousePressEvent(event)
   └─ Extrait coordonnées (x, y)
   └─ Signal: canvas_clicked(x, y)

4. Controller écoute canvas_clicked
   └─ Controller.handle_canvas_click(x, y)
   └─ Vérifie mode: creation_mode == "location" ✓
   └─ Appelle: Model.add_location(x, y)

5. Model traite la création
   └─ Génère ID: "l0" (ou "l1", "l2"...)
   └─ Sauvegarde: data["locations"]["l0"] = {...}
   └─ Crée entry invariants: data["locations"]["l0"]["invariants"] = []
   └─ Si premier: data["init"] = "l0"
   └─ Retourne "l0"

6. Controller ordonne affichage
   └─ View.canvas.draw_node("l0", x, y, is_initial=True)

7. View crée la représentation graphique
   └─ Crée NodeItem(...)
   └─ Ajoute à QGraphicsScene
   └─ Si is_initial: ajoute cercle imbriqué
   └─ Rendu Qt → écran ✓

8. Feedback utilisateur
   └─ Cercle apparaît à (x, y)
   └─ Label "l0" au centre
   └─ Double bordure indique état initial
```

**Garanties** :
- ✅ Model toujours à jour
- ✅ View reflète Model
- ✅ Chaque opération tracée en logs

### Scénario 2 : Éditer un Invariant

```
1. Utilisateur clique sur une localité "l0"
   └─ Canvas.mousePressEvent()
   └─ Détecte NodeItem cliqué
   └─ Signal: node_selected("l0")

2. Controller écoute
   └─ Controller.handle_node_selected("l0")
   └─ Ouvre Properties Dock
   └─ Affiche invariants actuels de l0

3. Utilisateur ajoute un invariant via UI
   └─ Saisit: horloge="x", operator="<=", value="5"
   └─ Clic "Ajouter"
   └─ Signal: add_invariant("l0", "x", "<=", "5")

4. Controller reçoit le signal
   └─ Appelle: Model.add_node_invariant("l0", "x", "<=", "5")

5. Model valide & sauvegarde
   └─ Valide: horloge "x" déclarée ✓
   └─ Ajoute: data["locations"]["l0"]["invariants"].append({...})
   └─ Émet signal interne (pour UI)

6. View se met à jour
   └─ PropertiesDock liste le nouvel invariant
   └─ Canvas peut afficher texte "x <= 5" sous le nœud

7. Utilisateur sauvegarde (Cmd+S)
   └─ Nouvel invariant persisté dans JSON
```

---

## Optimisations & Performances

### Rendering

**Problème** : Redessiner tous les éléments à chaque frame est lent

**Solution** : Qt Graphics View Framework
```python
# QGraphicsScene gère l'affichage efficacement
- Dirty region updates (redraws only changed areas)
- Automatic culling (items outside viewport not rendered)
- Hardware acceleration via OpenGL (optional)
```

### Transitions Dynamiques

**Problème** : Quand un nœud bouge, ses transitions doivent se recalculer

**Solution** : ItemSendsGeometryChanges
```python
# NodeItem signale chaque changement
class NodeItem(QGraphicsEllipseItem):
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # Recalcule les transitions connectées
            for trans in self.connected_transitions:
                trans.update_position()
        return value
```

### Anti-Doublons

**Problème** : Horloges/actions dupliquées → bugs

**Solution** : Filtrage au Model
```python
def add_clock(self, clock_name):
    if clock_name not in self.data["clocks"]:
        self.data["clocks"].append(clock_name)
    # Sinon : ignoré silencieusement
```

### Sérialisation JSON Canonicalisée

**Problème** : Différents formats JSON → merge conflicts en git

**Solution** : JSON.dumps(..., sort_keys=True)
```python
# Garantit ordre prévisible
{
  "actions": ["a", "b"],  # ← Alphabétique
  "clocks": ["x", "y"],
  "init": "l0",
  "locations": {...},     # ← Alphabétique
  "transitions": [...]
}
```

---

## Points d'Extension

### Pour Ajouter une Fonctionnalité

#### Exemple : Importer depuis UPPAAL

```python
# 1. Ajouter méthode au Model
class AutomatonModel:
    def import_from_uppaal(self, filepath):
        # Convertir format UPPAAL → self.data
        pass

# 2. Connecter au Controller
class MainController:
    def handle_import_uppaal(self):
        filepath = QFileDialog.getOpenFileName(...)[0]
        self.model.import_from_uppaal(filepath)
        self.view.canvas.refresh()

# 3. Ajouter entrée menu View
class MainWindow:
    def _setup_menubar(self):
        # ...
        import_action = menu_fichier.addAction("Importer depuis UPPAAL")
        import_action.triggered.connect(self.controller.handle_import_uppaal)
```

#### Exemple : Exporter vers Graphviz

```python
# 1. Nouvelle classe View pour visualisation
class GraphvizViewer(QMainWindow):
    def __init__(self, model):
        self.model = model
        # Générer DOT, lancer graphviz...

# 2. Controller lance la viewer
def handle_export_graphviz(self):
    viewer = GraphvizViewer(self.model)
    viewer.show()

# 3. Menu View/Menus
```

#### Exemple : Ajouter Validations

```python
# 1. Au Model
class AutomatonModel:
    def validate_deadlock_free(self):
        # Vérifier qu'aucun état n'est "bloqué"
        pass

# 2. Au Controller
def handle_validate(self):
    result = self.model.validate_deadlock_free()
    if result:
        QMessageBox.information(self.view, "✓ OK", "Automate valide")
    else:
        QMessageBox.warning(self.view, "✗ Erreur", result.error_msg)
```

---

## Conventions de Code

### Nommage

```python
# Méthodes View
on_*         # Slots Qt: on_button_clicked(self)
*_changed    # Signal handlers: clocks_changed
show_*       # Affichage: show_properties()
update_*     # Mise à jour: update_canvas()

# Méthodes Controller
handle_*     # Réacteurs signaux: handle_canvas_click()
trigger_*    # Dialogues: trigger_save_dialog()

# Méthodes Model
add_*        # CRUD Create: add_location()
remove_*     # CRUD Delete: remove_transition()
update_*     # CRUD Update: update_node_position()
get_*        # CRUD Read: get_invariants()

# Variables
loc_id       # String: "l0"
x, y         # Coordinates: float
nails        # List of nails: [(x1, y1), ...]
trans        # Transition dict: {source, target, ...}
raw_dbm      # Données brutes: matrices
*_textuels   # Représentation lisible: invariants_textuels
```

### Commentaires

```python
# Bon
def add_location(self, x, y):
    """Ajouter une nouvelle localité.
    
    Args:
        x (float): Coordonnée horizontale
        y (float): Coordonnée verticale
        
    Returns:
        str: ID de la localité créée (ex: 'l0')
    """

# Mauvais
def add_location(self, x, y):
    # ajouter location
    pass
```

### Type Hints

```python
# Recommandé pour les interfaces publiques
def add_node_invariant(
    self,
    loc_id: str,
    clock: str,
    operator: str,  # "<" | "<=" | ">" | ">=" | "==" | "!="
    value: str      # Nombre comme string
) -> None:
    """Ajouter un invariant."""
    pass
```

---

## Ressources

- **Qt Docs** : https://doc.qt.io/qt-6/
- **PySide6** : https://doc.qt.io/qtforpython/
- **DBM Papers** : Bengtsson & Yi, "Timed Automata" (survey)
- **UPPAAL** : http://www.uppaal.org (référence format)

---

*Document généré pour le projet COSMO - CILS 2025*
