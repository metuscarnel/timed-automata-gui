# 🚀 Guide de Démarrage Rapide

**5 minutes pour créer votre premier automate temporisé !**

---

## Installation (2 min)

```bash
# Aller dans le dossier
cd interface

# Créer un environnement Python
python3 -m venv venv

# L'activer
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

---

## Lancer l'outil (30 sec)

```bash
python main.py
```

Une fenêtre graphique s'ouvre avec une zone blanche vide.

---

## Premier Automate (3 min)

### 1️⃣ Créer un État
- Cliquez sur **"📍 Localité"** dans la toolbar (en haut)
- Cliquez n'importe où sur la zone blanche
- ✅ **Résultat** : Un cercle "l0" apparaît

### 2️⃣ Créer un Deuxième État
- Mode localité toujours actif
- Cliquez ailleurs → un cercle "l1" apparaît

### 3️⃣ Créer une Transition
- Cliquez sur **"➔ Transition"** dans la toolbar
- Cliquez sur le cercle "l0"
- Cliquez sur le cercle "l1"
- ✅ **Résultat** : Une flèche apparaît de l0 vers l1

### 4️⃣ Ajouter une Horloge
- Menu **Fichier** → **Déclarer Horloges**
- Tapez `x` et appuyez sur Entrée
- ✅ **Résultat** : Une horloge `x` est créée

### 5️⃣ Ajouter une Garde à la Transition
- Cliquez sur la flèche (elle devient sélectionnée)
- **Panneau droit** : cliquez **"+ Ajouter Garde"**
- Horloge : `x` → Opérateur : `>` → Valeur : `3`
- ✅ **Résultat** : La garde s'affiche sur la flèche

### 6️⃣ Sauvegarder
- Menu **Fichier** → **Sauvegarder**
- Choisissez un nom et un emplacement
- ✅ **Résultat** : Un fichier `.json` est créé

---

## Ce que vous avez créé

```
Automate temporisé :

        x > 3 ; {}
    l0 -------→ l1

Horloge : x
État initial : l0
```

---

## Prochaines Étapes

### Lire la Documentation Complète
- Voir [README.md](README.md) pour tous les détails

### Ajouter des Invariants
1. Cliquez sur un état (ex: l0)
2. Panneau droit → "+ Ajouter Invariant"
3. Horloge : `x` → Opérateur : `<=` → Valeur : `10`

### Ajouter des Resets
1. Sélectionnez une transition
2. Panneau droit → Cochez les horloges à réinitialiser

### Créer un Automate Complexe
- Répétez les étapes pour ajouter plus d'états et de transitions
- Utilisez le panneau droit pour configurer chaque élément

---

## Raccourcis Utiles

| Touche | Action |
|---|---|
| **Cmd+D** (macOS) / **Ctrl+D** (Windows) | Débogage - affiche l'état complet |
| **Échap** | Quitter le mode de création |
| **Delete** | Supprimer l'élément sélectionné |
| **Clic droit** | Menu contextuel |

---

## 🐛 Ça ne marche pas ?

### Aucune réaction au clic
- ✅ Vérifiez que le bouton de mode est **surligné** dans la toolbar
- ✅ Essayez **Échap** puis réactivez le mode

### Les transitions ne s'affichent pas
- ✅ Assurez-vous que le mode transition est **activé**
- ✅ Cliquez sur un état, puis sur un **autre** état (pas le même)

### Erreur "ModuleNotFoundError"
```bash
# Réinstallez les dépendances
pip install -r requirements.txt
```

---

## 📚 Besoin d'aide ?

- **Usage** → Voir [README.md](README.md#manuel-dutilisation)
- **Architecture** → Voir [ARCHITECTURE.md](ARCHITECTURE.md)
- **Débogage** → Voir [README.md](README.md#débogage--troubleshooting)

**Bon divertissement ! 🎉**
