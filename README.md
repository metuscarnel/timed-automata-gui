# 📘 Interface de Dessin d'Automates Temporisés
# Interface de Conception d'Automates Temporisés

**Outil complet pour créer, éditer et manipuler des automates temporisés (Timed Automata)** avec support avancé des horloges, invariants, gardes et actions.
## 1. Présentation de l'outil

![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)
![PySide6](https://img.shields.io/badge/PySide6-Latest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
Cet outil offre une interface graphique pour créer, éditer, analyser et exporter des automates temporisés étendus par des données (modèle COSMO). Il s'adresse principalement aux acteurs de la recherche et de l'ingénierie travaillant sur la modélisation et la vérification de systèmes temps-réel.

---
**Fonctionnalités principales :**
* Édition graphique intuitive de localités et de transitions.
* Déclaration et gestion des horloges, actions et variables globales.
* Édition avancée des contraintes (invariants, gardes) et des réinitialisations (resets).
* Import et export au format JSON avec compilation DBM intégrée.

## 📑 Table des Matières
## 2. Installation

1. [Vue d'Ensemble](#vue-densemble)
2. [Fonctionnalités](#fonctionnalités)
3. [Démarrage Rapide](#démarrage-rapide)
4. [Manuel d'Utilisation](#manuel-dutilisation)
5. [Documentation Technique](#documentation-technique)
6. [Raccourcis & Références](#raccourcis--références)
7. [Débogage & Troubleshooting](#débogage--troubleshooting)
**Prérequis :**
* Python 3.10 ou supérieur
* Environnement macOS, Linux ou Windows

---
**Procédure :**
1. Ouvrez un terminal dans le répertoire `interface`.
2. Créez un environnement virtuel : `python3 -m venv venv`
3. Activez l'environnement :
   * macOS / Linux : `source venv/bin/activate`
   * Windows : `venv\Scripts\activate`
4. Installez les dépendances : `pip install -r requirements.txt`

## Vue d'Ensemble
## 3. Prise en main rapide

Cet outil offre une interface graphique intuitive et moderne pour concevoir des automates temporisés, un modèle formel utilisé en vérification de systèmes temps-réel, planification d'ordonnancement et synthèse de contrôleurs.
Pour lancer l'application : `python main.py`

### Cas d'Usage
- **Modélisation** de systèmes temps-réel
- **Vérification** de propriétés 
- **Prototypage** rapide d'automates complexes
- **Éducation** en informatique théorique
**Créer un premier automate :**
1. Cliquez sur l'outil **Nouvelle Localité** dans la barre d'outils et cliquez sur la zone de dessin pour créer deux états.
2. Cliquez sur l'outil **Nouvelle Transition**, puis reliez le premier état (source) au second (cible).
3. Cliquez sur **Fichier → Sauvegarder** pour exporter votre modèle au format JSON.

---
## 4. Description de l'interface

## ✨ Fonctionnalités

### 🎨 Édition Graphique Interactive
| Fonctionnalité | Description |
| Élément | Description |
|---|---|
| **Création de localités** | Clic sur le canvas → génère automatiquement `l0`, `l1`, `l2`, etc. |
| **Création de transitions** | Cliquer source → cliquer cible = transition avec flèche courbe |
| **État initial marqué** | Visualisation par double bordure (cercle imbriqué) |
| **Déplacement fluide** | Drag-and-drop des nœuds avec recalcul géométrique temps-réel |
| **Points de pliage (Nails)** | Contrôle fin des trajectoires de transitions via points intermédiaires |
| **Suppression intelligente** | Supprimer un nœud → supprime aussi ses transitions connectées |
| **Menu contextuel** | Clic droit pour actions rapides (suppression, etc.) |
| **Barre de menus** | Accès aux actions globales (Nouveau, Ouvrir, Sauvegarder, Quitter) et à l'Aide. |
| **Barre d'outils** | Sélection des outils de dessin (Localités, Transitions), choix de l'état initial, et gestion des listes globales (Horloges, Actions, Data). |
| **Zone de dessin** | Espace de travail interactif pour modéliser visuellement le graphe de l'automate. |
| **Panneau latéral** | S'affiche automatiquement lors de la sélection d'un élément pour en éditer les propriétés (Invariants, Gardes, Resets). |

### ⏱️ Gestion Temporelle Avancée
| Fonctionnalité | Description |
|---|---|
| **Horloges globales** | Déclaration centralisée des horloge (ex: `x`, `y`, `z`) |
| **Invariants sur localités** | Contraintes temporelles (ex: `x <= 5`, `y >= 0`) |
| **Gardes sur transitions** | Conditions avant franchissement (ex: `x > 3 AND y < 10`) |
| **Resets d'horloges** | Réinitialisation lors du franchissement |
| **Actions/Événements** | Étiquettes de transitions pour synchronisation |
## 5. Fonctionnalités détaillées

### 💾 Persistance & Formats
| Fonctionnalité | Description |
|---|---|
| **Export JSON** | Sauvegarder automates avec compilation DBM |
| **Import JSON** | Charger et reconvertir automatiquement DBM → texte lisible |
| **Validation interne** | Vérifications cohérence données avant/après I/O |
| **Format portable** | JSON standard (git-friendly, interopérable) |
* **Manipulation graphique** : Les états peuvent être déplacés librement à la souris. Les transitions disposent de points de pliage modifiables pour ajuster la trajectoire. Supprimer une localité supprime automatiquement les transitions associées.
* **Édition des contraintes** : La sélection d'une localité permet de lui ajouter des invariants temporels. La sélection d'une transition permet de définir ses gardes, ses actions associées et ses remises à zéro d'horloge.
* **Gestion des variables étendues** : Le bouton **Data** de la barre d'outils ouvre un éditeur complet pour définir des types (structures, alias), initialiser des variables et déclarer des fonctions de mise à jour spécifiques.
* **Mode Débogage** : Le raccourci `Ctrl+D` (ou `Cmd+D` sur macOS) affiche l'état interne complet du modèle dans la console du terminal à des fins de vérification.

### 🔧 Outils Développeur
| Fonctionnalité | Description |
|---|---|
| **Débogage visuel** | `Cmd+D` → affiche l'état complet du modèle en console |
| **Traces détaillées** | Logs de toutes opérations MVC pour audit |
| **Thème unifié** | Flat design minimaliste (blanc/noir, cohérent) |
## 6. Formats de données

---
L'outil utilise un format JSON standardisé pour assurer la persistance et l'interopérabilité des modèles. 
Lors de la sauvegarde, les contraintes textuelles lisibles saisies dans l'interface sont automatiquement compilées sous forme de matrices DBM (Difference Bound Matrix), adaptées aux moteurs d'analyse formelle. Le chargement effectue l'opération inverse pour restituer un affichage textuel des contraintes.

## 🚀 Démarrage Rapide
## 7. Résolution des problèmes

### Prérequis
- Python 3.10+
- pip ou conda
- macOS, Linux ou Windows
| Problème | Solution |
|---|---|
| **L'application ne démarre pas** | Vérifiez que vous utilisez une version de Python supportée et que le module `PySide6` est bien installé via `requirements.txt`. |
| **Impossible de dessiner** | Assurez-vous d'avoir cliqué sur l'outil approprié (Localité ou Transition) dans la barre d'outils, son bouton doit apparaître surligné. Utilisez Échap pour quitter le mode. |
| **Erreur de chargement JSON** | Vérifiez que le fichier a bien été généré par l'outil ou qu'il respecte strictement la syntaxe attendue. |

### Installation
## 8. Glossaire

```bash
# 1. Aller au répertoire du projet
cd interface

# 2. Créer un environnement virtuel
python3 -m venv venv

# 3. Activer l'environnement
# Sur macOS/Linux:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# 4. Installer les dépendances
pip install -r requirements.txt
```

### Lancer l'Application

```bash
python main.py
```

**Résultat** : Une fenêtre graphique s'ouvre avec une zone blanche vide (canvas).

---

## 📖 Manuel d'Utilisation

### Tutoriel Pas-à-Pas : Créer un Automate Simple

#### Étape 1 : Créer la Première Localité
1. **Mode** : Cliquez sur le bouton **"📍 Localité"** dans la barre d'outils (devient surligné)
2. **Création** : Cliquez sur le canvas → une localité `l0` apparaît (double bordure = initiale)
3. **Position** : Vous pouvez la déplacer avec la souris

#### Étape 2 : Créer une Deuxième Localité
1. Mode localité toujours actif
2. Cliquez ailleurs sur le canvas → `l1` s'ajoute
3. Vous pouvez créer autant de localités que nécessaire

#### Étape 3 : Créer une Transition
1. **Mode** : Cliquez sur **"➔ Transition"** dans la barre d'outils
2. **Source** : Cliquez sur `l0`
3. **Cible** : Cliquez sur `l1` → une flèche apparaît automatiquement
4. Pour **modifier la trajectoire** : Clic-glissez les points de pliage (petits carrés)

#### Étape 4 : Ajouter des Horloges
1. Menu **Fichier** → **Déclarer Horloges**
2. Saisissez un nom (ex: `x`) et appuyez sur Entrée
3. Répétez pour ajouter `y`, `z`, etc.
4. Les horloges apparaissent dans le **panneau latéral (dock droit)**

#### Étape 5 : Ajouter des Invariants à une Localité
1. **Sélectionnez** une localité (clic gauche)
2. **Panneau droit** : Cliquez **"+ Ajouter Invariant"**
3. Choisissez l'horloge (`x`) et l'opérateur (`<=`, `>=`, etc.)
4. Entrez la valeur (ex: `5`)
5. Cliquez **Ajouter** → l'invariant s'affiche dans la liste

#### Étape 6 : Ajouter une Garde à une Transition
1. **Sélectionnez** une transition (clic gauche sur la flèche)
2. **Panneau droit** : Configurez de la même manière que les invariants
3. Les gardes s'affichent en-dessous de la transition

#### Étape 7 : Ajouter un Reset
1. Transition toujours sélectionnée
2. **Panneau droit** : Cochez les horloges à réinitialiser
3. Celles-ci s'afficheront dans une section "Resets" spécifique

#### Étape 8 : Sauvegarder
1. Menu **Fichier** → **Sauvegarder**
2. Choisissez un emplacement et un nom (ex: `mon_automate.json`)
3. L'automate est sauvegardé avec toutes ses données

#### Étape 9 : Charger un Automate
1. Menu **Fichier** → **Ouvrir**
2. Sélectionnez un fichier `.json` créé précédemment
3. L'automate s'affiche complètement reconstitué

### Opérations Courantes

#### Renommer un État Initial
1. Cliquez sur `l0` pour la sélectionner
2. Actuellement : impossible directement (limitation connue)
3. **Workaround** : Supprimez et recréez en premier

#### Modifier l'Ordre des Transitions
1. Clic-glissez les **points de pliage** (carrés gris sur la flèche)
2. La transition se recalcule automatiquement

#### Supprimer une Localité et Ses Transitions
1. Clic droit sur la localité → **Supprimer**
2. Confirmer → la localité **et toutes ses transitions** disparaissent

#### Réinitialiser le Canvas
1. Menu **Fichier** → **Nouveau**
2. Crée un automate vierge prêt à l'emploi

---

## 🏗️ Documentation Technique

### Architecture Générale

#### Pattern MVC (Model-View-Controller)

```
                    ┌──────────────────┐
                    │    main.py       │
                    │  (Point d'entrée)│
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
        ┌────────┐      ┌────────┐      ┌──────────┐
        │ Model  │◄────►│ View   │◄────►│Controller│
        │ (Data) │      │ (UI)   │      │ (Logic)  │
        └────────┘      └────────┘      └──────────┘
            ▲               ▲               ▲
            └───────────────┼───────────────┘
                  (Signaux Qt/Slots)
```

**Principes** :
- **Séparation des responsabilités** : chaque couche a un rôle distinct
- **Découplage** : le Model ne connaît pas la View
- **Réactivité** : signaux Qt assurent la propagation des changements
- **Testabilité** : chaque couche peut être testée indépendamment

#### Structure des Fichiers

```
interface/
├── 📄 main.py
│   └─ Point d'entrée, initialise Qt, stylesheets globaux
│
├── 📄 model.py
│   └─ Modèle de données, logique métier (CRUD)
│
├── 📄 controller.py
│   └─ Orchestration MVC, gestion événements
│
├── 📄 serial.py
│   └─ Sérialisation JSON, compilation DBM
│
├── 📄 convert.py
│   └─ Conversions de contraintes, utilitaires
│
├── 📁 View/
│   ├── __init__.py
│   ├── window.py         ← MainWindow, menus, toolbar, docks
│   ├── canvas.py         ← QGraphicsScene, gestion clics
│   ├── items.py          ← NodeItem, TransitionItem, NailItem
│   ├── properties_dock.py ← Panneau latéral propriétés
│   ├── popups.py         ← Dialogs/popups (horloges, actions)
│   └── data_editor.py    ← Éditeur multi-ligne pour texte long
│
├── 📁 resources/
│   └── icons.py          ← Icônes SVG embedded
│
├── 📝 requirements.txt
├── 📝 README.md          ← Ce fichier
└── 📄 model_template.json ← Template automate vide
```

### Flux de Données : Exemple Concret

**Scénario** : L'utilisateur clique sur le canvas pour créer une localité

```
1. UTILISATEUR CLIQUE
   └─ Souris → Canvas (zones de dessin graphique)

2. VUE (canvas.py) REÇOIT L'ÉVÉNEMENT
   ├─ mousePressEvent() détecte le clic
   ├─ Calcule les coordonnées (x, y)
   └─ Émet signal : 'canvas_clicked(x, y)'

3. CONTRÔLEUR ÉCOUTE LE SIGNAL
   ├─ handle_canvas_click(x, y) s'exécute
   ├─ Vérifie le mode de création (location? transition?)
   └─ Appelle : Model.add_location(x, y)

4. MODÈLE (model.py) TRAITE LA DEMANDE
   ├─ Génère un ID unique : 'l0'
   ├─ Sauvegarde dans self.data["locations"]["l0"]
   ├─ Sauvegarde la position x, y
   ├─ Vérifie si c'est le premier : si oui, data["init"] = 'l0'
   └─ Retourne l'ID au Contrôleur

5. CONTRÔLEUR ORDONNE LA MISE À JOUR DE LA VUE
   ├─ Appelle : View.canvas.draw_node('l0', x, y, is_initial=True)
   └─ Émet signal : 'locations_updated'

6. VUE (canvas.py) DESSINE LE RÉSULTAT
   ├─ Crée un NodeItem (cercle + texte)
   ├─ L'ajoute à la QGraphicsScene
   ├─ Si is_initial=True : ajoute une double bordure
   └─ L'utilisateur voit un cercle sur le canvas ✓
```

**Avantages de ce flux** :
- ✅ Model reste pur (pas de dépendance Qt)
- ✅ View reste passive (uniquement affichage)
- ✅ Chaque changement passe par le Contrôleur (audit trail)

### Modèle de Données

#### Structure `Model.data`

```python
{
    # === LOCALITÉS ===
    "locations": {
        "l0": {
            "node_pos": {"x": 100, "y": 50},           # Position sur canvas
            "invariants": [                             # Contraintes temporelles
                {
                    "clock": "x",
                    "operator": "<=",
                    "type": "value",
                    "value": "5"
                },
                {
                    "clock": "y",
                    "operator": ">=",
                    "type": "value",
                    "value": "0"
                }
            ]
        },
        "l1": {
            "node_pos": {"x": 300, "y": 50},
            "invariants": []
        }
    },

    # === TRANSITIONS ===
    "transitions": [
        {
            "source": "l0",                            # ID source
            "target": "l1",                            # ID cible
            "action": "a",                             # Étiquette (optionnelle)
            "guards": [                                # Conditions de franchissement
                {
                    "clock": "x",
                    "operator": ">",
                    "type": "value",
                    "value": "3"
                }
            ],
            "resets": ["x", "y"],                     # Horloges à réinitialiser
            "nails": [                                # Points de pliage
                {"x": 150, "y": 100},
                {"x": 200, "y": 120}
            ]
        }
    ],

    # === GLOBALES ===
    "clocks": ["x", "y", "z"],                       # Horloges disponibles
    "actions": ["a", "b", "skip"],                   # Actions disponibles
    "init": "l0"                                      # État initial
}
```

#### Traduction Textuelle

Pour l'utilisateur, cela se traduit par :

```
Localité l0 :
  └─ Invariants : x <= 5, y >= 0

Transition l0 → l1 :
  ├─ Action : a
  ├─ Garde : x > 3
  └─ Resets : x, y
```

### Contraintes Temporelles (DBM)

#### Qu'est-ce qu'une Matrice DBM ?

Une **Difference Bound Matrix** est une représentation interne compacte des contraintes sur horloge. Format :

```
Texte lisible :  "x <= 5 AND x >= 0"
                     ↓ (sérialisation)
DBM stocké :     [[0, -5], [∞, 0]]
                     ↓ (désérialisation)
Texte restitué :  "x <= 5 AND x >= 0"
```

#### Bénéfices
- 📦 **Compact** : matrice plutôt que chaînes
- ⚡ **Rapide** : opérations matricielles parallélisables
- 🔬 **Formel** : utilisable par outils de vérification (UPPAAL, TiNA)

#### Comment ça fonctionne dans l'outil

1. **À la saisie** : L'utilisateur rentre `x <= 5` en texte
2. **Au modèle** : Le texte est stocké tel quel (`serial.py`)
3. **À l'export** : Conversion texte → DBM (compression)
4. **À l'import** : Conversion DBM → texte (restitution lisible)

---

## 🛠️ Technologies & Dépendances

| Technologie | Version | Rôle |
|---|---|---|
| **Python** | 3.10+ | Langage principal |
| **PySide6** | Latest | Framework Qt pour GUI |
| **PyYAML** | (optionnel) | Config avancée |
| **JSON** | native | Sérialisation |

### Installation des Dépendances

```bash
# Via requirements.txt
pip install -r requirements.txt

# Ou manuellement
pip install PySide6>=6.0.0
```

---

## ⌨️ Raccourcis & Références

### Raccourcis Clavier

| Raccourci | Plateforme | Action |
|---|---|---|
| **Cmd+D** | macOS | Mode débogage (affiche Model en console) |
| **Ctrl+D** | Windows/Linux | Mode débogage |
| **Échap** | Toutes | Quitter le mode de création (localité/transition) |
| **Delete** | Toutes | Supprimer l'objet sélectionné |
| **Entrée** | Dialogs | Valider une saisie (horloge, action) |
| **Clic droit** | Toutes | Menu contextuel |

### Menu Fichier

| Option | Raccourci | Fonction |
|---|---|---|
| Nouveau | Cmd+N | Créer automate vierge |
| Ouvrir | Cmd+O | Charger depuis JSON |
| Sauvegarder | Cmd+S | Exporter vers JSON |
| Mode Débogage | Cmd+D | Affiche state complet en console |

### Conventions de Nommage

**Localités** :
- Format : `l0`, `l1`, `l2`, ...
- Générées automatiquement, croissantes

**Horloges** :
- Format : caractères alphanumériques (ex: `x`, `y`, `timeout1`)
- Cas-sensitives

**Actions** :
- Format : identifiants simples (ex: `send`, `recv`, `tick`)
- Pas d'espaces

**Opérateurs** :
- `<` : strictement inférieur
- `<=` : inférieur ou égal
- `>` : strictement supérieur
- `>=` : supérieur ou égal
- `==` : égal (en gardes uniquement)
- `!=` : différent (en gardes uniquement)

---

## 🐛 Débogage & Troubleshooting

### Mode Débogage : Afficher l'État Complet

```bash
# Dans l'application :
# Macintosh : Cmd+D
# Windows/Linux : Ctrl+D

# Résultat en console :
--- Attributs de l'instance 'model' ---
{
    'data': {
        'locations': {'l0': {...}, 'l1': {...}},
        'transitions': [...],
        'clocks': [...],
        'actions': [...],
        'init': 'l0'
    },
    'loc_counter': 2,
    'transition_counter': 1
}
---------------------------------------
```

### Problèmes Courants

#### ❌ L'application ne démarre pas
**Symptôme** : `ModuleNotFoundError: No module named 'PySide6'`

```bash
# Solution
pip install PySide6
# Ou
pip install -r requirements.txt
```

#### ❌ Pas de réaction aux clics
**Symptôme** : Cliquer sur le canvas ne crée rien

**Causes possibles** :
1. ✋ Vérifiez que le **mode est activé** (bouton surligné dans la toolbar)
2. 🖱️ Essayez de **quitter le mode** (Échap) puis réactivez

```bash
# Debug : afficher les logs
# Dans le terminal, cherchez :
# [Controller] Bouton Localité cliqué (Actif: True)
```

#### ❌ Fichier JSON invalide à l'import
**Symptôme** : `JSON decode error` ou `Key error`

**Solutions** :
1. Vérifiez que c'est un fichier créé par cet outil
2. Ouvrez-le avec un éditeur texte et cherchez des caractères mal formés
3. Utilisez le template : `model_template.json`

#### ❌ Les transitions ne se dessinent pas
**Symptôme** : Les localités sont présentes mais aucune flèche

**Causes** :
1. Mode transition non activé
2. Clic sur le même nœud deux fois (source = cible)
3. Transition déjà existante entre les deux nœuds

### Logs & Traces

L'application génère des logs détaillés en console :

```
[Controller] Création de la localité l0 en (100, 50)
[Controller] Transition créée de l0 à l1 avec 0 clous
[Model] Invariant ajouté à l0
```

Utilisez ces logs pour **tracer** votre workflow.

### Variables d'Environnement (Avancé)

```bash
# Activer le verbose logging
export DEBUG=1
python main.py

# Afficher les timings de rendu
export PROFILE=1
python main.py
```

---

## 📚 Ressources Supplémentaires

### À Propos des Automates Temporisés
- **UPPAAL** : Outil de vérification (http://www.uppaal.org)
- **TiNA** : Autre outil formel (http://www.laas.fr/tina)
- **Papier fondateur** : Alur & Dill, 1994

### Documentation Technique
- `FEATURES_TRACKING.md` : Suivi détaillé des fonctionnalités implémentées
- Code source : bien commenté, lisez directement

---

## 📝 Notes de Version

**Version 1.0 - Juin 2026**
- ✅ Interface graphique complète
- ✅ Support des automates temporisés
- ✅ Export/Import JSON
- ✅ Panneau de propriétés
- ✅ Thème flat design

---

## 📄 Licence

[À définir selon votre projet]

---

## 👤 Auteurs & Contributions

Développé dans le cadre du projet **COSMO - CILS 2025**.

---

**Questions ?** Consultez la console en mode débogage (`Cmd+D`) ou les fichiers `FEATURES_TRACKING.md`.
* **Automate temporisé** : Automate à états finis enrichi de variables temporelles (horloges) réelles.
* **Localité** : Nœud ou état de l'automate.
* **Transition** : Arc reliant deux localités, conditionnant le changement d'état.
* **Horloge** : Variable globale mesurant le temps écoulé de manière continue.
* **Invariant** : Condition sur une horloge qui doit rester vraie tant que l'automate est dans une localité donnée.
* **Garde** : Condition sur une horloge devant être satisfaite pour qu'une transition puisse être franchie.
* **Reset** : Action remettant la valeur d'une horloge à zéro lors du franchissement d'une transition.
