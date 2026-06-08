# Interface de Conception d'Automates Temporisés



**Outil graphique complet pour modéliser, éditer et exporter des automates temporisés étendus par des données.**

Cet outil s'adresse principalement à la modélisation pour la vérification formelle.

## Table des Matières

- Fonctionnalités
- Démarrage Rapide
- Manuel d'Utilisation
- Architecture et Formats
- Raccourcis Clavier
- Dépannage

## Fonctionnalités

### Édition Graphique Interactive
- **Modélisation visuelle** : Création de localités et de transitions par pointer-cliquer.
- **Trajectoires personnalisées** : Contrôle fin des flèches via des points de pliage (nails).


### Gestion Temporelle & Contraintes
- **Horloges globales** : Déclaration centralisée des variables temporelles via la barre d'outils.
- **Invariants** : Ajout de contraintes de séjour sur les localités (ex: `x <= 5`).
- **Gardes & Actions** : Définition de conditions de franchissement et d'événements de synchronisation sur les transitions.
- **Resets** : Remise à zéro sélective des horloges lors des franchissements.

### Persistance & Interopérabilité
- **Import / Export JSON** : Format standardisé pour assurer la portabilité et la comptabilité avec d'autres outils comme UPPAL.

- **Éditeur de données étendues** : Interface dédiée ("Data") pour définir des structures, alias, variables initiales et fonctions de mise à jour.

## Démarrage Rapide

### Prérequis
- Python 3.10 ou supérieur
- Linux

### Installation

1. **Cloner ou télécharger le dépôt** et se placer dans le répertoire `interface` :
   ```bash
   cd interface
   ```
2. **Créer un environnement virtuel** :
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```
3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

### Lancer l'Application

```bash
python main.py
```
L'interface graphique s'ouvrira, vous présentant une zone de travail vierge prête à l'emploi.

## 📖 Manuel d'Utilisation

### Créer votre premier automate
1. **Ajouter un état** : Cliquez le petit cercle sur la barre d'outils **"Nouvelle Localité"** puis cliquez sur le canvas. Le premier état créé est automatiquement défini comme état initial (double bordure).
2. **Ajouter une transition** : Cliquez sur **"➔ Nouvelle Transition"**, puis reliez un état source à un état cible.
3. **Définir des horloges** : Utilisez l'icône 🕒 dans la barre d'outils pour ajouter de nouvelles horloges (ex: `x`, `y`).
4. **Éditer les contraintes** : Sélectionnez une localité ou une transition avec le clic  droit. Le **panneau de droite** s'ouvre pour vous permettre d'ajouter des invariants, des gardes, ou des actions.
5. **Sauvegarder** : Allez dans **Fichier > Sauvegarder** ou faite " Ctrl + S" pour sauvegarder modèle sous JSON.

*💡 Astuce : Vous pouvez annuler l'outil en cours d'utilisation en appuyant sur la touche `Échap`.*

## Architecture et Formats

Le projet respecte scrupuleusement le patron de conception **MVC (Model-View-Controller)**, garantissant un code découplé et maintenable :
- **Model** (`model.py`) : Gère les données de l'automate indépendamment de l'interface (CRUD).
- **View** (`View/`) : Composants PySide6 gérant exclusivement l'affichage et les interactions utilisateur.
- **Controller** (`controller.py`) : Orchestre les événements entre la vue et le modèle de manière stricte.

### Format de Données (JSON & DBM)
Les modèles sont exportés en JSON. Les contraintes saisies humainement (ex: `x <= 5`) sont compilées en matrices **DBM** (`serial.py`) pour une compatibilité directe avec les outils de vérification formelle. À l'ouverture d'un fichier, l'opération inverse est effectuée pour restaurer l'affichage textuel dans l'interface de manière transparente.

## Raccourcis Clavier

| Raccourci | Action |
|---|---|
| `Cmd+N` / `Ctrl+N` | Créer un nouvel automate vierge |
| `Cmd+O` / `Ctrl+O` | Ouvrir un fichier JSON existant |
| `Cmd+S` / `Ctrl+S` | Sauvegarder l'automate courant |
| `Cmd+D` / `Ctrl+D` | Afficher l'état interne du modèle dans la console (Mode Débogage) |
| `Échap` | Annuler le mode de création en cours ou l'action en cours |
| `Clic Droit` | Menu contextuel sur les labels ou forcer la sélection d'un élément graphique |

## Dépannage

| Problème | Solution |
|---|---|
| **L'application ne démarre pas** | Vérifiez que le module `PySide6` est bien installé (`pip install -r requirements.txt`) et que votre version de Python est ≥ 3.10. |
| **Impossible d'ajouter un nœud/flèche** | Vérifiez que l'outil correspondant est bien en surbrillance dans la barre d'outils en haut de la fenêtre. |
| **Erreur lors du chargement JSON** | Assurez-vous que le fichier a été généré par cet outil. Les matrices DBM mal formées ou les fichiers altérés manuellement peuvent bloquer l'importation. |

---
