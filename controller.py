import pprint
import json
from PySide6.QtWidgets import QFileDialog, QMessageBox

class MainController:
    def __init__(self, model):
        self.model = model
        self.view = None
        self.editing_constraint_index = None # Stocke l'index de la contrainte en cours de modification
        self.current_filepath = None

    def set_view(self, view):
        self.view = view
        # Connexion dynamique aux signaux de suppression de la scène graphique
        if hasattr(self.view, "canvas"):
            self.view.canvas.node_delete_requested.connect(self.handle_delete_node)
            self.view.canvas.transition_delete_requested.connect(self.handle_delete_transition)

    def handle_add_location(self, checked=False):
        print(f"Bouton Localité cliqué (Actif: {checked})")
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
            print(f"Création de la localité {loc_id} en ({x}, {y})")
            # 2. Ordonner à la Vue de dessiner la localité
            self.view.canvas.draw_node(loc_id, x, y, is_initial)
            # 3. Mettre à jour la liste des états initiaux dans la barre d'outils
            self.view.update_locations_list(list(self.model.data["locations"].keys()), self.model.data.get("init"))

    def handle_transition_created(self, source_id, target_id, nails_pos):
        """Gère la création effective d'une transition après validation par la Vue."""
        trans_id = self.model.add_transition(source_id, target_id, nails_pos)
        self.view.canvas.draw_transition(trans_id, source_id, target_id, nails_pos)
        print(f"Transition créée de {source_id} à {target_id} avec {len(nails_pos)} clous (ID: {trans_id})")

    def handle_add_transition(self, checked=False):
        print(f"Bouton Transition cliqué (Actif: {checked})")
        if self.view:
            if checked:
                self.view.canvas.set_creation_mode("transition")
            else:
                self.view.canvas.set_creation_mode(None)

    def submit_action(self, action_name):
        print(f"Réception de l'action : {action_name}")
        self.model.add_action(action_name)
        # --- NOUVEAU : Rafraîchir la vue ---
        if self.view:
            self.view.update_actions_display(self.model.data["actions"])

    def submit_clock(self, clock_name):
        print(f"Réception de l'horloge : {clock_name}")
        self.model.add_clock(clock_name)
        # --- NOUVEAU : Rafraîchir la vue ---
        if self.view:
            self.view.update_clocks_display(self.model.data["clocks"])

    def handle_initial_state_changed(self, new_init_state):
        """Gère le changement d'état initial depuis la barre d'outils."""
        if new_init_state:
            print(f"Changement de l'état initial vers : {new_init_state}")
            self.model.set_initial_state(new_init_state)
            if self.view:
                self.view.refresh_graph_display() # Rafraîchit pour appliquer la double bordure au bon endroit

    def update_variables_data(self, variables_data):
        print("Mise à jour des variables de données depuis l'éditeur.")
        self.model.update_variables(variables_data)

    # --- NOUVELLES MÉTHODES POUR LE MENU ---

    def handle_new_file(self):
        print("Réinitialisation de buffer : Nouveau modèle vide créé.")
        self.model.clear()
        self.current_filepath = None
        if self.view:
            self.view.refresh_graph_display()
            self.view.update_window_title(self.current_filepath)

    def trigger_open_dialog(self):
        print("Ouverture de la boîte de dialogue.")
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
                    self.current_filepath = filepath
                    self.view.update_window_title(self.current_filepath)
                except Exception as e:
                    QMessageBox.critical(
                        self.view,
                        "Erreur de chargement",
                        f"Impossible de lire le fichier JSON.\nErreur : {str(e)}"
                    )

    def trigger_save_dialog(self):
        print("Fichier -> Sauvegarder : Ouverture de la boîte de dialogue.")
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
                self.current_filepath = filepath
                self.view.update_window_title(self.current_filepath)

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
        print(f"Nœud sélectionné : {node_id}")
        # Réinitialiser le mode d'édition si on change de sélection
        self.editing_constraint_index = None
        if self.view and hasattr(self.view, 'properties_dock') and hasattr(self.view.properties_dock, 'btn_add_inv'):
            self.view.properties_dock.btn_add_inv.setText("+")
            
        if self.view and hasattr(self.view, 'properties_dock'):
            node_data = self.model.data["locations"].get(node_id, {})
            available_clocks = self.model.data.get("clocks", [])
            self.view.properties_dock.show_node_props(node_id, node_data, available_clocks)

    def handle_transition_selected(self, trans_id):
        print(f"Transition sélectionnée : {trans_id}")
        # Réinitialiser le mode d'édition si on change de sélection
        self.editing_constraint_index = None
        if self.view and hasattr(self.view, 'properties_dock') and hasattr(self.view.properties_dock, 'btn_add_guard'):
            self.view.properties_dock.btn_add_guard.setText("+")
            
        if self.view and hasattr(self.view, 'properties_dock'):
            # Trouver les données de la transition
            trans_data = self.model.get_transition(trans_id)
            if not trans_data: return
            source_id = trans_data["source"]
            target_id = trans_data["target"]
            available_actions = self.model.data.get("actions", [])
            available_clocks = self.model.data.get("clocks", [])
            available_locations = list(self.model.data["locations"].keys())
            
            # (Étape 1 & 3) Mise à jour dynamique des cases à cocher pour les resets
            self.view.properties_dock.update_resets_list(available_clocks)
            
            # 3. Étape 3 : Récupération des resets et remplissage des cases
            active_resets = trans_data.get('resets', [])
            for cb in self.view.properties_dock.checkboxes_resets:
                # Désactivation temporaire du signal pour ne pas déclencher la sauvegarde
                cb.blockSignals(True)
                if cb.text() in active_resets:
                    cb.setChecked(True)
                else:
                    cb.setChecked(False)
                cb.blockSignals(False)
                
                # Connexion à l'étape 2 pour que le modèle soit mis à jour instantanément au clic
                cb.stateChanged.connect(lambda state, tid=trans_id: self.update_transition_resets(tid))
                
            self.view.properties_dock.show_transition_props(trans_id, source_id, target_id, trans_data, available_actions, available_clocks, available_locations)

    # 2. Étape 2 : Méthode appelée lors de la validation/sauvegarde de la transition (ou instantanément)
    def update_transition_resets(self, trans_id):
        # Initialisation de la liste vide
        selected_resets = []
        
        if self.view and hasattr(self.view, 'properties_dock'):
            # Parcours de la liste des cases
            for cb in self.view.properties_dock.checkboxes_resets:
                # Si la case est cochée, on récupère son texte
                if cb.isChecked():
                    selected_resets.append(cb.text())
                    
        t = self.model.get_transition(trans_id)
        if t:
            t["resets"] = selected_resets

    def update_transition_action(self, trans_id, new_action):
        print(f"Action {new_action} assignée à la transition {trans_id}")
        self.model.update_transition_action(trans_id, new_action)

    def update_node_position(self, node_id, x, y):
        print(f"Localité {node_id} déplacée en ({x}, {y})")
        self.model.update_node_position(node_id, x, y)

    def update_nail_position(self, trans_id, nail_index, x, y):
        print(f"Clou n°{nail_index} de {trans_id} déplacé en ({x}, {y})")
        self.model.update_nail_position(trans_id, nail_index, x, y)

    @staticmethod
    def is_constraint_equivalent(new_c, existing_c):
        """Vérifie si deux contraintes sont mathématiquement ou logiquement équivalentes."""
        # Récupération sécurisée des valeurs
        c1, op1, t1, v1 = new_c.get('clock'), new_c.get('operator'), new_c.get('type'), new_c.get('value')
        off1 = int(new_c.get('offset', 0))
        
        c2, op2, t2, v2 = existing_c.get('clock'), existing_c.get('operator'), existing_c.get('type'), existing_c.get('value')
        off2 = int(existing_c.get('offset', 0))

        # 1. Comparaison stricte
        if c1 == c2 and op1 == op2 and t1 == t2 and v1 == v2 and off1 == off2:
            return True

        # 2. Comparaison logique avec inversion pour les horloges
        if t1 == 'clock' and t2 == 'clock':
            if c1 == v2 and v1 == c2:
                op_inverse = {'<=': '>=', '>=': '<=', '==': '=='}
                if op_inverse.get(op1) == op2:
                    if off1 == -off2:
                        return True
                        
        return False

    def add_node_invariant(self, node_id, clock, operator, target_type, target_value, offset=0):
        print(f"Ajout de l'invariant {clock} {operator} {target_value} ({target_type}, offset={offset}) à {node_id}")
        
        # --- Validation anti-doublon logique ---
        new_c = {'clock': clock, 'operator': operator, 'type': target_type, 'value': target_value, 'offset': offset}
        node_data = self.model.data["locations"].get(node_id, {})
        existing_invariants = node_data.get("invariants", [])
        
        for i, existing_c in enumerate(existing_invariants):
            if self.editing_constraint_index == i:
                continue # On ignore la comparaison avec la contrainte en cours d'édition
            if self.is_constraint_equivalent(new_c, existing_c):
                print("⚠️ La contrainte existe déjà ou est mathématiquement équivalente. Ajout ignoré.")
                return # On bloque l'ajout
        # ----------------------------------------

        # Si on est en mode édition, on supprime l'ancienne contrainte d'abord
        if self.editing_constraint_index is not None:
            self.model.remove_node_invariant(node_id, self.editing_constraint_index)
            self.editing_constraint_index = None
            if hasattr(self.view.properties_dock, 'btn_add_inv'):
                self.view.properties_dock.btn_add_inv.setText("+")
                
        self.model.add_node_invariant(node_id, clock, operator, target_type, target_value, offset)
        # Rafraîchir la vue en simulant une nouvelle sélection
        self.handle_node_selected(node_id)

    def remove_node_invariant(self, node_id, index):
        print(f"Suppression de l'invariant index {index} pour {node_id}")
        self.model.remove_node_invariant(node_id, index)
        # Rafraîchir la vue en simulant une nouvelle sélection
        self.handle_node_selected(node_id)

    def add_transition_guard(self, trans_id, clock, operator, target_type, target_value, offset=0):
        print(f"Ajout de la garde {clock} {operator} {target_value} ({target_type}, offset={offset}) à la transition {trans_id}")
        
        # --- Validation anti-doublon logique ---
        new_c = {'clock': clock, 'operator': operator, 'type': target_type, 'value': target_value, 'offset': offset}
        trans_data = self.model.get_transition(trans_id) or {}
        existing_guards = trans_data.get("guards", [])
        
        for i, existing_c in enumerate(existing_guards):
            if self.editing_constraint_index == i:
                continue # On ignore la comparaison avec la garde en cours d'édition
            if self.is_constraint_equivalent(new_c, existing_c):
                print("⚠️ La garde existe déjà ou est mathématiquement équivalente. Ajout ignoré.")
                return # On bloque l'ajout
        # ----------------------------------------

        # Si on est en mode édition, on supprime l'ancienne contrainte d'abord
        if self.editing_constraint_index is not None:
            self.model.remove_transition_guard(trans_id, self.editing_constraint_index)
            self.editing_constraint_index = None
            if hasattr(self.view.properties_dock, 'btn_add_guard'):
                self.view.properties_dock.btn_add_guard.setText("+")
                
        self.model.add_transition_guard(trans_id, clock, operator, target_type, target_value, offset)
        # Rafraîchir la vue en simulant une nouvelle sélection de la flèche
        self.handle_transition_selected(trans_id)

    def remove_transition_guard(self, trans_id, index):
        print(f"[Controller] Suppression de la garde index {index} pour la transition {trans_id}")
        self.model.remove_transition_guard(trans_id, index)
        # Rafraîchir la vue en simulant une nouvelle sélection
        self.handle_transition_selected(trans_id)
        
    def handle_constraint_double_click(self, item):
        """Gère le double-clic sur une contrainte dans le Dock pour la réinjecter et l'éditer."""
        if not self.view or not hasattr(self.view, 'properties_dock'):
            return
            
        dock = self.view.properties_dock
        is_node = dock.stacked_widget.currentWidget() == dock.node_panel
        is_trans = dock.stacked_widget.currentWidget() == dock.trans_panel
        
        constraint_data = None
        idx = -1
        
        # 1. Trouver les données (Localité ou Transition)
        if is_node:
            idx = dock.inv_list_widget.currentRow()
            if idx >= 0:
                node_data = self.model.data["locations"].get(dock.node_id_field.text(), {})
                invariants = node_data.get("invariants", [])
                if idx < len(invariants):
                    constraint_data = invariants[idx]
        elif is_trans:
            idx = dock.guard_list_widget.currentRow()
            if idx >= 0:
                trans_id = dock.current_trans_id
                trans_data = self.model.get_transition(trans_id) or {}
                guards = trans_data.get("guards", [])
                if idx < len(guards):
                    constraint_data = guards[idx]
                
        if not constraint_data:
            return
            
        # 2. Réinjecter les valeurs dans les widgets
        if is_node:
            dock.node_inv_clock.setCurrentText(constraint_data["clock"])
            dock.node_inv_op.setCurrentText(constraint_data["operator"])
            if constraint_data["type"] == "value":
                dock.node_inv_clock_target.setCurrentIndex(0)
                dock.node_inv_value.setText(str(constraint_data["value"]))
            else:
                dock.node_inv_clock_target.setCurrentText(constraint_data["value"])
                dock.node_inv_value.setText(str(constraint_data.get("offset", 0)))
        elif is_trans:
            dock.trans_guard_clock.setCurrentText(constraint_data["clock"])
            dock.trans_guard_op.setCurrentText(constraint_data["operator"])
            if constraint_data["type"] == "value":
                dock.trans_guard_clock_target.setCurrentIndex(0)
                dock.trans_guard_value.setText(str(constraint_data["value"]))
            else:
                dock.trans_guard_clock_target.setCurrentText(constraint_data["value"])
                dock.trans_guard_value.setText(str(constraint_data.get("offset", 0)))
                
        # 3. Mettre à jour l'état du contrôleur et l'UI
        self.editing_constraint_index = idx
        if is_node and hasattr(dock, 'btn_add_inv'):
            dock.btn_add_inv.setText("Modif")
        elif is_trans and hasattr(dock, 'btn_add_guard'):
            dock.btn_add_guard.setText("Modif")

    def handle_delete_transition(self, trans_id):
        print(f"Demande de suppression de la transition {trans_id}")
        self.model.remove_transition(trans_id)
        if self.view:
            self.view.canvas.remove_transition_visual(trans_id)
            self.handle_selection_cleared()

    def handle_delete_node(self, node_id):
        print(f"Demande de suppression de la localité {node_id} (Cascade activée)")
        # 1. Identifier et supprimer en cascade les transitions liées
        transitions_to_delete = [
            t["id"] for t in self.model.data["transitions"]
            if t["source"] == node_id or t["target"] == node_id
        ]
        for tid in transitions_to_delete:
            self.handle_delete_transition(tid)

        # 2. Supprimer le nœud lui-même
        self.model.remove_node(node_id)
        if self.view:
            self.view.canvas.remove_node_visual(node_id)
            self.handle_selection_cleared()

    def change_transition_endpoint(self, trans_id, new_source, new_target):
        print(f"Modification de la transition {trans_id} vers {new_source}->{new_target}")
        
        # 1. Update Model
        self.model.change_transition_endpoint(trans_id, new_source, new_target)

        # 2. Update View (Canvas)
        if self.view:
            self.view.canvas.change_transition_endpoints_visual(trans_id, new_source, new_target)
            self.handle_transition_selected(trans_id)

    def handle_edit_inv(self,node_id):
        print(f"demande de modification d'un invariant de {node_id}")
    
    def get_available_clocks(self):
        """Retourne la liste des horloges disponibles dans le modèle."""
        return self.model.data.get("clocks", [])

    def handle_modify_clock(self, old_name, new_name):
        print(f"Modification horloge : {old_name} -> {new_name}")
        self.model.modify_clock(old_name, new_name)
        if self.view:
            self.view.update_clocks_display(self.model.data["clocks"])
            self._refresh_properties_dock()

    def handle_delete_clock(self, clock_name):
        print(f"Suppression horloge : {clock_name}")
        self.model.delete_clock(clock_name)
        if self.view:
            self.view.update_clocks_display(self.model.data["clocks"])
            self._refresh_properties_dock()

    def handle_modify_action(self, old_name, new_name):
        print(f"Modification action : {old_name} -> {new_name}")
        self.model.modify_action(old_name, new_name)
        if self.view:
            self.view.update_actions_display(self.model.data["actions"])
            self._refresh_properties_dock()

    def handle_delete_action(self, action_name):
        print(f"Suppression action : {action_name}")
        self.model.delete_action(action_name)
        if self.view:
            self.view.update_actions_display(self.model.data["actions"])
            self._refresh_properties_dock()

    def _refresh_properties_dock(self):
        """Recharge les propriétés affichées dans le Dock si celui-ci est visible"""
        if self.view and hasattr(self.view, 'properties_dock') and self.view.properties_dock.isVisible():
            selected_items = self.view.canvas.scene.selectedItems()
            if not selected_items: 
                return
            item = selected_items[0]
            
            if hasattr(item, 'source') and hasattr(item, 'target'): # TransitionItem
                self.handle_transition_selected(item.id)
            elif hasattr(item, 'transition'):
                self.handle_transition_selected(item.transition.id)
            elif hasattr(item, 'id'): # NodeItem
                self.handle_node_selected(item.id)
