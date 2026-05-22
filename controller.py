import pprint
import json
from PySide6.QtWidgets import QFileDialog, QMessageBox

class MainController:
    def __init__(self, model):
        self.model = model
        self.view = None
        self.editing_constraint_index = None # Stocke l'index de la contrainte en cours de modification

    def set_view(self, view):
        self.view = view
        # Connexion dynamique aux signaux de suppression de la scène graphique
        if hasattr(self.view, "canvas"):
            self.view.canvas.node_delete_requested.connect(self.handle_delete_node)
            self.view.canvas.transition_delete_requested.connect(self.handle_delete_transition)

    def handle_add_location(self, checked=False):
        print(f"[Controller] Bouton Localité cliqué (Actif: {checked})")
        if self.view:
            if checked:
                self.view.canvas.set_creation_mode("location")
            else:
                self.view.canvas.set_creation_mode(None)

    def handle_canvas_click(self, x, y):
        """Gère le clic sur le canvas selon le mode de création actif."""
        if self.view and self.view.canvas.creation_mode == "location":
            # 1. Enregistrer dans le Buffer/Model (génère un ID genre "L1")
            loc_id = self.model.add_location(x, y)
            is_initial = (self.model.data.get("init") == loc_id)
            print(f"[Controller] Création de la localité {loc_id} en ({x}, {y})")
            # 2. Ordonner à la Vue de dessiner la localité
            self.view.canvas.draw_node(loc_id, x, y, is_initial)

    def handle_transition_created(self, source_id, target_id, nails_pos):
        """Gère la création effective d'une transition après validation par la Vue."""
        self.model.add_transition(source_id, target_id, nails_pos)
        self.view.canvas.draw_transition(source_id, target_id, nails_pos)
        print(f"[Controller] Transition créée de {source_id} à {target_id} avec {len(nails_pos)} clous")

    def handle_add_transition(self, checked=False):
        print(f"[Controller] Bouton Transition cliqué (Actif: {checked})")
        if self.view:
            if checked:
                self.view.canvas.set_creation_mode("transition")
            else:
                self.view.canvas.set_creation_mode(None)

    def submit_action(self, action_name):
        print(f"[Controller] Réception de l'action : {action_name}")
        self.model.add_action(action_name)
        # --- NOUVEAU : Rafraîchir la vue ---
        if self.view:
            self.view.update_actions_display(self.model.data["actions"])

    def submit_clock(self, clock_name):
        print(f"[Controller] Réception de l'horloge : {clock_name}")
        self.model.add_clock(clock_name)
        # --- NOUVEAU : Rafraîchir la vue ---
        if self.view:
            self.view.update_clocks_display(self.model.data["clocks"])

    # --- NOUVELLES MÉTHODES POUR LE MENU ---

    def handle_new_file(self):
        print("[Controller] Fichier -> Nouveau : Réinitialisation du Buffer.")
        # Plus tard : vider le self.model.data et effacer la scène graphique

    def trigger_open_dialog(self):
        print("[Controller] Fichier -> Ouvrir : Ouverture de la boîte de dialogue.")
        if self.view:
            filepath, _ = QFileDialog.getOpenFileName(
                self.view,
                "Ouvrir un automate",
                "",
                "Fichiers JSON (*.json)"
            )
            if filepath:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        loaded_data = json.load(f)
                    
                    # Reconstruction du modèle interne
                    self.model.load_from_json_data(loaded_data)
                    print(f"-> Automate chargé avec succès depuis : {filepath}")
                    
                    # Rafraîchir la vue
                    self.view.refresh_graph_display()
                except Exception as e:
                    QMessageBox.critical(
                        self.view,
                        "Erreur de chargement",
                        f"Impossible de lire le fichier JSON.\nErreur : {str(e)}"
                    )

    def trigger_save_dialog(self):
        print("[Controller] Fichier -> Sauvegarder : Ouverture de la boîte de dialogue.")
        if self.view:
            filepath, _ = QFileDialog.getSaveFileName(
                self.view,
                "Enregistrer l'automate",
                "",
                "Fichiers JSON (*.json)"
            )
            if filepath:
                # Sécurité : Forcer l'extension si elle n'est pas saisie par l'utilisateur
                if not filepath.endswith(".json"):
                    filepath += ".json"
                
                self.model.export_to_json(filepath)
                print(f"-> Automate sauvegardé avec succès dans : {filepath}")

    def debug_print_model_instance(self):
        """Affiche les attributs de l'instance du modèle (loc_counter, data, etc.)"""
        print("\n--- Attributs de l'instance 'model' ---")
        pprint.pprint(self.model.__dict__)
        print("---------------------------------------")

    # --- GESTION DE LA SÉLECTION ET DES PROPRIÉTÉS ---

    def handle_selection_cleared(self):
        if self.view and hasattr(self.view, 'properties_dock'):
            self.view.properties_dock.hide()

    def handle_node_selected(self, node_id):
        print(f"[Controller] Nœud sélectionné : {node_id}")
        # Réinitialiser le mode d'édition si on change de sélection
        self.editing_constraint_index = None
        if self.view and hasattr(self.view, 'properties_dock') and hasattr(self.view.properties_dock, 'btn_add_constraint'):
            self.view.properties_dock.btn_add_constraint.setText("Ajouter")
            
        if self.view and hasattr(self.view, 'properties_dock'):
            node_data = self.model.data["locations"].get(node_id, {})
            available_clocks = self.model.data.get("clocks", [])
            self.view.properties_dock.show_node_props(node_id, node_data, available_clocks)

    def handle_transition_selected(self, source_id, target_id):
        print(f"[Controller] Transition sélectionnée : {source_id} -> {target_id}")
        # Réinitialiser le mode d'édition si on change de sélection
        self.editing_constraint_index = None
        if self.view and hasattr(self.view, 'properties_dock') and hasattr(self.view.properties_dock, 'btn_add_constraint'):
            self.view.properties_dock.btn_add_constraint.setText("Ajouter")
            
        if self.view and hasattr(self.view, 'properties_dock'):
            # Trouver les données de la transition
            trans_data = next((t for t in self.model.data["transitions"] 
                               if t["source"] == source_id and t["target"] == target_id), {})
            available_actions = self.model.data.get("actions", [])
            available_clocks = self.model.data.get("clocks", [])
            self.view.properties_dock.show_transition_props(source_id, target_id, trans_data, available_actions, available_clocks)

    def update_transition_action(self, source_id, target_id, new_action):
        print(f"[Controller] Action {new_action} assignée à la transition {source_id}->{target_id}")
        self.model.update_transition_action(source_id, target_id, new_action)

    def update_node_position(self, node_id, x, y):
        print(f"[Controller] Localité {node_id} déplacée en ({x}, {y})")
        self.model.update_node_position(node_id, x, y)

    def update_nail_position(self, source_id, target_id, nail_index, x, y):
        print(f"[Controller] Clou n°{nail_index} de {source_id}->{target_id} déplacé en ({x}, {y})")
        self.model.update_nail_position(source_id, target_id, nail_index, x, y)

    def add_node_invariant(self, node_id, clock, operator, target_type, target_value, offset=0):
        print(f"[Controller] Ajout de l'invariant {clock} {operator} {target_value} ({target_type}, offset={offset}) à {node_id}")
        
        # Si on est en mode édition, on supprime l'ancienne contrainte d'abord
        if self.editing_constraint_index is not None:
            self.model.remove_node_invariant(node_id, self.editing_constraint_index)
            self.editing_constraint_index = None
            if hasattr(self.view.properties_dock, 'btn_add_constraint'):
                self.view.properties_dock.btn_add_constraint.setText("Ajouter")
                
        self.model.add_node_invariant(node_id, clock, operator, target_type, target_value, offset)
        # Rafraîchir la vue en simulant une nouvelle sélection
        self.handle_node_selected(node_id)

    def remove_node_invariant(self, node_id, index):
        print(f"[Controller] Suppression de l'invariant index {index} pour {node_id}")
        self.model.remove_node_invariant(node_id, index)
        # Rafraîchir la vue en simulant une nouvelle sélection
        self.handle_node_selected(node_id)

    def add_transition_guard(self, source_id, target_id, clock, operator, target_type, target_value, offset=0):
        print(f"[Controller] Ajout de la garde {clock} {operator} {target_value} ({target_type}, offset={offset}) à la transition {source_id}->{target_id}")
        
        # Si on est en mode édition, on supprime l'ancienne contrainte d'abord
        if self.editing_constraint_index is not None:
            self.model.remove_transition_guard(source_id, target_id, self.editing_constraint_index)
            self.editing_constraint_index = None
            if hasattr(self.view.properties_dock, 'btn_add_constraint'):
                self.view.properties_dock.btn_add_constraint.setText("Ajouter")
                
        self.model.add_transition_guard(source_id, target_id, clock, operator, target_type, target_value, offset)
        # Rafraîchir la vue en simulant une nouvelle sélection de la flèche
        self.handle_transition_selected(source_id, target_id)

    def remove_transition_guard(self, source_id, target_id, index):
        print(f"[Controller] Suppression de la garde index {index} pour la transition {source_id}->{target_id}")
        self.model.remove_transition_guard(source_id, target_id, index)
        # Rafraîchir la vue en simulant une nouvelle sélection
        self.handle_transition_selected(source_id, target_id)
        
    def handle_constraint_double_click(self, item):
        """Gère le double-clic sur une contrainte dans le Dock pour la réinjecter et l'éditer."""
        if not self.view or not hasattr(self.view, 'properties_dock'):
            return
            
        dock = self.view.properties_dock
        idx = dock.list_constraints.currentRow()
        if idx < 0:
            return
            
        constraint_data = None
        
        # 1. Trouver les données (Localité ou Transition)
        if hasattr(dock, 'current_node_id') and dock.current_node_id:
            node_data = self.model.data["locations"].get(dock.current_node_id, {})
            invariants = node_data.get("invariants", [])
            if idx < len(invariants):
                constraint_data = invariants[idx]
                
        elif hasattr(dock, 'current_source_id') and getattr(dock, 'current_source_id', None):
            src, tgt = dock.current_source_id, dock.current_target_id
            trans_data = next((t for t in self.model.data["transitions"] if t["source"] == src and t["target"] == tgt), {})
            guards = trans_data.get("guards", [])
            if idx < len(guards):
                constraint_data = guards[idx]
                
        if not constraint_data:
            return
            
        # 2. Réinjecter les valeurs dans les widgets
        dock.combo_clock1.setCurrentText(constraint_data["clock"])
        dock.combo_operator.setCurrentText(constraint_data["operator"])
        
        # Gestion robuste selon le type de line_value (QLineEdit ou QSpinBox)
        is_spinbox = hasattr(dock.line_value, 'setValue')
        
        if constraint_data["type"] == "value":
            dock.combo_clock2.setCurrentIndex(0) # Index 0 => "---"
            dock.line_value.setValue(int(constraint_data["value"])) if is_spinbox else dock.line_value.setText(str(constraint_data["value"]))
        elif constraint_data["type"] == "clock":
            dock.combo_clock2.setCurrentText(constraint_data["value"])
            dock.line_value.setValue(int(constraint_data.get("offset", 0))) if is_spinbox else dock.line_value.setText(str(constraint_data.get("offset", 0)))
                
        # 3. Mettre à jour l'état du contrôleur et l'UI
        self.editing_constraint_index = idx
        if hasattr(dock, 'btn_add_constraint'):
            dock.btn_add_constraint.setText("Modifier")

    def handle_delete_transition(self, source_id, target_id):
        print(f"[Controller] Demande de suppression de la transition {source_id}->{target_id}")
        self.model.remove_transition(source_id, target_id)
        if self.view:
            self.view.canvas.remove_transition_visual(source_id, target_id)
            self.handle_selection_cleared()

    def handle_delete_node(self, node_id):
        print(f"[Controller] Demande de suppression de la localité {node_id} (Cascade activée)")
        # 1. Identifier et supprimer en cascade les transitions liées
        transitions_to_delete = [
            (t["source"], t["target"]) for t in self.model.data["transitions"]
            if t["source"] == node_id or t["target"] == node_id
        ]
        for src, tgt in transitions_to_delete:
            self.handle_delete_transition(src, tgt)

        # 2. Supprimer le nœud lui-même
        self.model.remove_node(node_id)
        if self.view:
            self.view.canvas.remove_node_visual(node_id)
            self.handle_selection_cleared()
    def handle_edit_inv(self,node_id):
        print(f"[Controller] demande de modification d'un invariant de {node_id}")
        