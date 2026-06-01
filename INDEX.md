# 📚 Index de Documentation

Bienvenue ! Ce projet contient une **documentation complète et organisée**. Utilisez ce guide pour trouver exactement ce dont vous avez besoin.

---

## 🎯 Choisissez Votre Chemin

### 👶 Je suis impatient, je veux juste créer un automate (5 min)
→ **[GETTING_STARTED.md](GETTING_STARTED.md)**
- Installation ultra-rapide
- Tutoriel pas-à-pas
- Premier automate en 3 minutes

---

### 📖 Je veux connaître toutes les fonctionnalités (30 min)
→ **[README.md](README.md)**
- Vue d'ensemble complète
- Manuel d'utilisation détaillé
- Raccourcis clavier
- Troubleshooting courant

---

### 🔧 Je veux contribuer au code / comprendre l'architecture (1-2h)
→ **[ARCHITECTURE.md](ARCHITECTURE.md)**
- Pattern MVC expliqué en détail
- Structure module par module
- Flux de données complets
- Points d'extension pour nouvelles fonctionnalités

---

### ✅ Je veux voir ce qui a été implémenté (15 min)
→ **[FEATURES_TRACKING.md](FEATURES_TRACKING.md)** (généré automatiquement)
- Liste de toutes les fonctionnalités
- État de chaque feature
- Composants impliqués
- Dates de livraison

---

## 📋 Références Rapides

### Installation
```bash
cd interface
python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python main.py
```

### Raccourcis Clavier Essentiels
| Touche | Action |
|---|---|
| **Cmd+D** (macOS) / **Ctrl+D** (Windows) | Débogage |
| **Échap** | Quitter le mode |
| **Delete** | Supprimer l'élément sélectionné |

### Fichiers Principaux
| Fichier | Rôle | Lire si... |
|---|---|---|
| `main.py` | Point d'entrée | Vous voulez comprendre l'initialisation |
| `model.py` | Données & logique | Vous modifiez la structure de l'automate |
| `controller.py` | Orchestration | Vous ajoutez une nouvelle fonctionnalité |
| `View/window.py` | Interface principale | Vous modifiez le menu/toolbar |
| `View/canvas.py` | Zone de dessin | Vous modifiez le rendu graphique |
| `View/items.py` | Éléments graphiques | Vous changez l'apparence des nœuds/transitions |

---

## 🚨 Ça Coince ? 

### Problème : L'application ne démarre pas
```bash
pip install PySide6
# ou
pip install -r requirements.txt
```

### Problème : Aucune réaction au clic
1. Vérifiez que le mode est **activé** (bouton surligné)
2. Essayez **Échap** puis réactivez le mode

### Problème : Pas d'aide trouvée
- Consultez **[README.md → Débogage](README.md#débogage--troubleshooting)**
- Activez le mode débogage : `Cmd+D` / `Ctrl+D`
- Vérifiez les logs console : `[Controller]`, `[Model]`, etc.

---

## 📊 Structure Documentation

```
📘 Documentation/
├── 📖 README.md                  ← START HERE (complet, 30 min)
├── 🚀 GETTING_STARTED.md         ← Pour les impatients (5 min)
├── 🏗️ ARCHITECTURE.md            ← Pour développeurs (1-2h)
├── ✅ FEATURES_TRACKING.md       ← État des features
└── 📚 INDEX.md                   ← Ce fichier
```

---

## 🎓 Parcours d'Apprentissage Recommandé

### Utilisateur Final
1. **5 min** : [GETTING_STARTED.md](GETTING_STARTED.md)
2. **15 min** : [README.md → Manuel d'Utilisation](README.md#manuel-dutilisation)
3. **Au besoin** : [README.md → Troubleshooting](README.md#débogage--troubleshooting)

### Développeur Python
1. **5 min** : [GETTING_STARTED.md](GETTING_STARTED.md) pour tester
2. **30 min** : [README.md → Architecture](README.md#documentation-technique)
3. **1h** : [ARCHITECTURE.md](ARCHITECTURE.md) pour comprendre le code
4. **En continu** : Lire le code source (bien commenté)

### Contributeur
1. Suivre parcours développeur
2. Consulter [ARCHITECTURE.md → Points d'Extension](ARCHITECTURE.md#points-dextension)
3. Lire [FEATURES_TRACKING.md](FEATURES_TRACKING.md) pour voir les gaps
4. Créer des issues/PRs

---

## 💬 Questions Fréquentes

**Q: Par où je commence ?**
A: Allez voir [GETTING_STARTED.md](GETTING_STARTED.md) (5 min)

**Q: Comment je crée un automate ?**
A: [README.md → Manuel d'Utilisation](README.md#manuel-dutilisation)

**Q: Comment j'ajoute une nouvelle fonctionnalité ?**
A: [ARCHITECTURE.md → Points d'Extension](ARCHITECTURE.md#points-dextension)

**Q: Qu'est-ce qu'une DBM ?**
A: [README.md → Contraintes Temporelles](README.md#contraintes-temporelles-dbm) ou [ARCHITECTURE.md → Sérialisation & DBM](ARCHITECTURE.md#sérialisation--dbm)

**Q: Ça ne marche pas...**
A: [README.md → Troubleshooting](README.md#problèmes-courants)

---

## 🔗 Ressources Externes

### Automates Temporisés
- **Papier fondateur** : Alur & Dill, 1994
- **Survey** : Bengtsson & Yi, "Timed Automata"

### Outils Complémentaires
- **UPPAAL** : Vérification d'automates (http://www.uppaal.org)
- **TiNA** : Analyse réseau de Petri (http://www.laas.fr/tina)

### Qt & PySide6
- **Qt Docs** : https://doc.qt.io/qt-6/
- **PySide6** : https://doc.qt.io/qtforpython/

---

## 📝 Informations Projet

- **Nom** : Interface de Dessin d'Automates Temporisés
- **Projet** : COSMO - CILS 2025
- **Langage** : Python 3.10+
- **Framework** : PySide6 (Qt pour Python)
- **Format** : JSON + DBM

---

## 🎉 Prêt à démarrer ?

**→ Allez à [GETTING_STARTED.md](GETTING_STARTED.md)**

Bon travail ! 🚀
