# Interface de Dessin d'Automates Temporisés

Interface graphique développée avec PySide6 pour créer et manipuler des automates temporisés.

## Architecture

```
interface/
├── main.py                 # Point d'entrée
├── View/
│   ├── view.py            # Vue principale (AutomataView + AutomataGraphicsView)
│   └── icons.py           # Définitions des icônes SVG
├── Model/
│   ├── model.py
│   └── template_model.json
└── Controller/
    └── controller.py
```

## Fonctionnalités Implémentées

### 1. **Icônes SVG pour la Toolbar** ✅
- Icône **Localité** (cercle) - Créer des états
- Icône **Transition** (flèche) - Créer des transitions
- Icône **Action** (boîte) - À implémenter
- Icône **Horloge** (clock) - À implémenter
- Fichier dédié: `View/icons.py`

### 2. **Zone de Dessin Interactive** ✅
**Classe**: `AutomataGraphicsView` (dans `View/view.py`)

**Fonctionnalités**:
- Fond sombre (gris foncé)
- Antialiasing activé pour un rendu lisse
- Mode création de localités
- Mode création de transitions (démarré, à completer)

**Localités (Minimaliste)**:
- Cercles bleu clair avec contour noir
- Nom automatique généré (L1, L2, L3, etc.)
- Texte noir centré en Arial 11 Bold
- Déplaçables et sélectionnables
- Supprimables avec la touche Delete
- Logs console détaillés à la création/suppression

**Contrôles clavier**:
- `Échap` - Quitter le mode de création
- `Delete` - Supprimer une localité sélectionnée

### 3. **Signaux et Slots** ✅
**Signaux** (depuis `AutomataGraphicsView`):
- `state_created(QPointF)` - Quand une localité est créée
- `transition_requested()` - Quand une transition est demandée
- `state_deleted(object)` - Quand une localité est supprimée

**Slots** (dans `AutomataView`):
- `on_new_state_clicked()` - Toggle mode création localités
- `on_new_transition_clicked()` - Toggle mode création transitions
- `on_action_clicked()` - Placeholder
- `on_clock_clicked()` - Placeholder
- `on_state_created()` - Log
- `on_transition_requested()` - Log
- `on_state_deleted()` - Log

### 4. **Toolbar avec Boutons Toggles** ✅
- Boutons mutuellement exclusifs
- Changement de curseur (croix lors de la création)
- Icônes + texte visibles

## Prochaines Étapes

### À Court Terme
- [ ] Implémentation des transitions (lignes flèchées entre localités)
- [ ] Sélection et édition des transitions
- [ ] Ajouter des labels aux transitions
- [ ] Actions et Horloges sur les transitions

### À Moyen Terme
- [ ] Persistance (sauvegarde/chargement de fichiers)
- [ ] Validation des automates
- [ ] Affichage d'erreurs

### À Long Terme
- [ ] Refactorisation en modules séparés (Model, View, Controller)
- [ ] Tests unitaires
- [ ] Export (SVG, PDF, etc.)

## Utilisation

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer l'application
python main.py
```

### Actions rapides
1. Cliquer "Nouvelle Localité" (curseur devient une croix)
2. Cliquer dans la zone de dessin pour ajouter un cercle
3. Glisser-déposer pour déplacer
4. Sélectionner + Delete pour supprimer
5. Échap pour quitter le mode création

## Structure du Code (View/view.py)

### AutomataGraphicsView
- Hérite de `QGraphicsView`
- **Propriétés**:
  - `creation_mode` - Mode actuel ("state", "transition", ou None)
  - `state_counter` - Compte les localités créées
- **Méthodes**:
  - `set_creation_mode()` - Active/désactive le mode de création
  - `_create_state()` - Crée une localité (cercle + texte)
  - `mousePressEvent()` - Gère les clics souris
  - `keyPressEvent()` - Gère les touches clavier

### AutomataView
- Hérite de `QMainWindow`
- Crée les menus et toolbar
- Connecte les signaux aux slots
- Affiche les messages et dialogues

## Notes Techniques

- **PySide6**: Framework Qt pour Python
- **QGraphicsView/QGraphicsScene**: Système d'affichage 2D performant
- **Signaux/Slots**: Pattern de communication PySide6
- **SVG**: Format vectoriel pour les icônes (dans `icons.py`)

---

*Dernière mise à jour: 6 mai 2026*

## Changelog

### 6 mai 2026 - Icônes Noires & Stabilité Visuelle (v5)

**Changements visuels**:
- ✅ Icônes SVG passées du blanc au noir
- ✅ Toolbuttons - bordure stable (1px) sans effet de grossissement au focus
- ✅ États hover/pressed/checked cohérents avec bordure stable
- ✅ Outline désactivé pour éviter les artefacts

### 6 mai 2026 - Thème Blanc/Noir Strict (v4)

**Changements visuels**:
- ✅ Stylesheet CSS forcé pour toute l'interface
- ✅ Toolbar, Menu, Boutons - fond blanc, texte noir
- ✅ Cercles - blanc pur avec contour noir
- ✅ États hover/selected - gris clair/foncé
- ✅ Indépendant du thème système (pas de dark/light mode)

### 6 mai 2026 - Thème Clair (v3)

**Changements visuels**:
- ✅ Fond blanc (au lieu de noir)
- ✅ Cercles bleu clair avec contour noir
- ✅ Texte noir (au lieu de blanc)
- ✅ Interface plus épurée et lisible

### 6 mai 2026 - Approche Minimaliste (v2)

**Corrections**:
- ✅ Suppression de la classe `State` personnalisée (problèmes de rendu)
- ✅ Utilisation directe de `QGraphicsEllipseItem` 
- ✅ Création du texte comme enfant du cercle
- ✅ Rendu fonctionnel et stable

**Fonctionnalités**:
- ✅ Création de localités (L1, L2, L3...)
- ✅ Texte centré dans les cercles
- ✅ Déplacement au drag
- ✅ Suppression avec Delete
- ✅ Logs console détaillés

### 6 mai 2026 - Dessin des Localités (v1)

**Améliorations**:
- ✅ Création d'une classe `State` dédiée aux localités
- ✅ Génération automatique des noms (L1, L2, L3, etc.)
- ❌ Approche abandonnée (problèmes de rendu avec paint())
