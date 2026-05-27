# Interface de Dessin d'Automates Temporisés

Interface graphique complète pour créer et manipuler des **automates temporisés** (Timed Automata) avec support des horloges, invariants, gardes et actions.

---

## 🎯 Fonctionnalités Principales

### Édition Graphique
- ✅ **Création de localités** (états) avec nommage automatique (l0, l1, l2...)
- ✅ **Création de transitions** avec support des points de pliage (nails) 
- ✅ **État initial** visualisé par une double bordure
- ✅ **Suppression en cascade** (nœud → transitions connectées)
- ✅ **Déplacement fluide** des nœuds et transitions avec recalcul géométrique en temps réel
- ✅ **Menu contextuel** pour suppression avec alertes visuelles

### Gestion Temporelle
- ✅ **Déclaration d'horloges** globales via dialog
- ✅ **Invariants sur localités** (contraintes temporelles de type `x <= 5`, `y >= 0`)
- ✅ **Gardes sur transitions** (conditions avant franchissement)
- ✅ **Resets d'horloges** lors du franchissement
- ✅ **Actions sur transitions** (étiquettes d'événements)

### Persistance & Sérialisation
- ✅ **Export JSON** avec compilation des contraintes en matrices DBM (Difference Bound Matrix)
- ✅ **Import JSON** avec décompilation automatique DBM → dictionnaires textuels
- ✅ **Validation des données** internes

### Outillage Développeur
- ✅ **Mode débogage** (Cmd+D) - affiche l'état complet du modèle en console
- ✅ **Traces console** détaillées des opérations MVC
- ✅ **Thème visuel cohérent** (flat design, minimaliste)

---

## 🏗️ Architecture

### Pattern MVC (Model-View-Controller)

```
┌─────────────────────────────────────────────────────────────┐
│                      main.py (Point d'entrée)               │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
            ┌─────────┐  ┌──────────┐  ┌──────────┐
            │ Model   │  │ View     │  │Controller│
            │ (Data)  │  │ (UI)     │  │ (Logic)  │
            └─────────┘  └──────────┘  └──────────┘
                ▲             ▲             ▲
                └─────────────┼─────────────┘
                     (Signaux/Slots)
```

### Structure du Projet

```
interface/
├── main.py                      # Point d'entrée (initialise MVC)
├── model.py                     # Modèle (données + logique métier)
├── controller.py                # Contrôleur (signaux/slots)
├── serial.py                    # Sérialisation (DBM ↔ JSON)
├── convert.py                   # Conversion de contraintes
│
├── View/
│   ├── __init__.py
│   ├── window.py                # MainWindow (menus, toolbar, docks)
│   ├── canvas.py                # Canvas graphique (QGraphicsScene)
│   ├── items.py                 # Nœuds, transitions, clous
│   ├── properties_dock.py        # Panneau latéral (propriétés)
│   ├── popups.py                # Dialogs (actions, horloges)
│
├── resources/
│   └── icons.py                 # Icônes SVG (embedded)
│
├── model_template.json          # Template vide
└── README.md                    # Ce fichier
```

---

## 🛠️ Technologies

| Technologie | Rôle |
|---|---|
| **Python 3.10+** | Langage principal |
| **PySide6** | Framework Qt pour l'interface graphique |
| **JSON** | Format de stockage/sérialisation |
| **DBM (Difference Bound Matrix)** | Représentation interne des contraintes temporelles |
| **SVG** | Format des icônes vectorielles |

---

## � Flux de Données MVC

### 1️⃣ **Model** (`model.py`)
Responsable du **state interne** et de la **logique métier** :
- Stockage hiérarchisé : localités, transitions, horloges, actions, invariants, gardes
- Opérations CRUD : `add_location()`, `add_transition()`, `add_node_invariant()`, etc.
- Compilation/décompilation DBM pour sérialisation JSON
- **Pas de dépendance** vers la Vue ou le Contrôleur

### 2️⃣ **View** (`View/window.py`, `View/canvas.py`, `View/items.py`)
Responsable de l'**interface graphique** :
- **MainWindow** : menus, toolbar, docks
- **Canvas** (QGraphicsScene) : zone de dessin interactive
- **Items** : NodeItem (cercles), TransitionItem (flèches), NailItem (clous)
- Émission de **signaux** pour chaque action utilisateur
- **Pas de logique métier** : envoie les événements au Contrôleur

### 3️⃣ **Controller** (`controller.py`)
**Arbitre** entre Model et View :
- Écoute les signaux de la Vue
- Appelle les méthodes du Modèle
- Demande à la Vue de se mettre à jour
- Gère l'ordre des opérations

### 🔄 Exemple : Création d'une Localité
```
Utilisateur clique → Canvas.mousePressEvent()
    ↓
Canvas envoie signal 'canvas_clicked(x, y)'
    ↓
Controller.handle_canvas_click(x, y)
    ↓
Model.add_location(x, y) → retourne 'l0'
    ↓
Controller.canvas.draw_node('l0', x, y, is_initial=True)
    ↓
Canvas dessine un NodeItem visuel
```

---

## 🔧 Méthode de Développement

### Pattern Signaux/Slots (Publish-Subscribe)
- **Découplage** : Model ≠ View
- **Réactivité** : Changements propagés via signaux Qt
- **Testabilité** : Chaque couche peut être testée indépendamment

### Conventions de Code
- **Préfixes des méthodes** :
  - `add_*` : ajoute une entité
  - `remove_*` : supprime une entité
  - `update_*` : modifie une entité
  - `handle_*` (Controller) : réacteur aux signaux
  - `on_*` (View) : slots Qt

- **Nommage des variables** :
  - `loc_id` : identifiant de localité (ex: 'l0')
  - `trans` : transition
  - `raw_*` : données brutes (matrices DBM)
  - `*_textuels` : représentation lisible

### Gestion des Contraintes Temporelles (DBM)

**Format interne** : Matrice DBM (Difference Bound Matrix)
```json
{
  "locations": {
    "l0": {
      "invariants": [
        {"clock": "x", "operator": "<=", "type": "value", "value": "5"},
        {"clock": "y", "operator": ">=", "type": "value", "value": "0"}
      ]
    }
  }
}
```

**Sérialisation** (`serial.py`) :
- Contraintes textuelles → Matrices DBM (canonicalization)
- Stockage compact en JSON

**Désérialisation** (`model.py.extract_constraints_from_dbm()`) :
- Matrices DBM → Contraintes textuelles 
- Restauration intelligible de l'UI

---

## 🚀 Installation & Utilisation

### Prérequis
- Python 3.10 ou supérieur
- pip ou conda

### Installation

```bash
# Cloner le projet
cd interface

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer l'Application

```bash
python main.py
```

---

## ⌨️ Raccourcis Clavier

| Raccourci | Action |
|---|---|
| **Cmd+D** / **Ctrl+D** | Mode débogage (affiche le Model en console) |
| **Échap** | Quitter le mode de création (localité/transition) |
| **Delete** | Supprimer une localité sélectionnée |
| **Clic droit** | Menu contextuel (suppression) |
| **Entrée** (dialogs) | Valider une saisie (action/horloge) |

---

## 📁 Fichiers Clés

| Fichier | Responsabilité |
|---|---|
| `main.py` | Point d'entrée, initialisation MVC, stylesheet global |
| `model.py` | Modèle de données, logique métier |
| `controller.py` | Orchestration MVC, gestion des événements |
| `serial.py` | Sérialisation JSON + compilation DBM |
| `View/window.py` | MainWindow, menus, toolbar, docks |
| `View/canvas.py` | QGraphicsScene, gestion des clics |
| `View/items.py` | NodeItem, TransitionItem, NailItem (rendu) |
| `View/properties_dock.py` | Panneau latéral (invariants, gardes, resets) |
| `resources/icons.py` | Icônes SVG (embedded) |

---

## 📊 État Interne du Modèle

Structure `Model.data` :
```python
{
    "locations": {
        "l0": {
            "node_pos": {"x": 100, "y": 50},
            "invariants": [...]  # Contraintes temporelles
        },
        "l1": {...}
    },
    "transitions": [
        {
            "source": "l0",
            "target": "l1",
            "action": "a",  # Étiquette (optionnelle)
            "guards": [...],  # Conditions avant franchissement
            "resets": ["x"],  # Horloges à réinitialiser
            "nails": [(x1, y1), (x2, y2)]  # Points de pliage
        }
    ],
    "clocks": ["x", "y"],  # Horloges globales
    "actions": ["a", "b"],  # Actions globales
    "init": "l0"  # État initial
}
```

---

## 🐛 Débogage

### Afficher l'État Complet
```python
# Dans l'application : Cmd+D (macOS) ou Ctrl+D (Windows/Linux)
# Affiche la structure complète du Model dans la console
```

### Traces Console
- Le Contrôleur enregistre chaque opération :
  - `[Controller] Création de la localité l0...`
  - `[Controller] Transition créée de l0 à l1...`
  - `[Model] Invariant ajouté...`

---

## 📝 Notes Techniques

- **QGraphicsView/QGraphicsScene** : Système 2D performant pour les automates complexes
- **ItemSendsGeometryChanges** : Mise à jour en temps réel des transitions lors du déplacement
- **SVG dans PySide6** : Icônes vectorielles scalables sans fichier externe
- **JSON canonicalisé** : Format portable et versionnable (git-friendly)

---

*Dernière mise à jour: 27 mai 2026*
