import pprint

class MainController:
    def __init__(self, model):
        self.model = model
        self.view = None

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

    def handle_open_file(self):
        print("[Controller] Fichier -> Ouvrir : Ouverture de la boîte de dialogue.")
        # Plus tard : QFileDialog, lire le JSON, remplir le modèle, dessiner la scène

    def handle_save_file(self):
        print("[Controller] Fichier -> Sauvegarder : Écriture du Buffer sur disque.")
        # C'EST ICI LA CLÉ DE NOTRE ARCHITECTURE
        # On demandera au modèle d'écrire self.model.data dans un fichier .json
        print(f"-> Données prêtes à être écrites : {self.model.data}")

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
        if self.view and hasattr(self.view, 'properties_dock'):
            node_data = self.model.data["locations"].get(node_id, {})
            available_clocks = self.model.data.get("clocks", [])
            self.view.properties_dock.show_node_props(node_id, node_data, available_clocks)

    def handle_transition_selected(self, source_id, target_id):
        print(f"[Controller] Transition sélectionnée : {source_id} -> {target_id}")
        if self.view and hasattr(self.view, 'properties_dock'):
            # Trouver les données de la transition
            trans_data = next((t for t in self.model.data["transitions"] 
                               if t["source"] == source_id and t["target"] == target_id), {})
            available_actions = self.model.data.get("actions", [])
            self.view.properties_dock.show_transition_props(source_id, target_id, trans_data, available_actions)

    def update_transition_action(self, source_id, target_id, new_action):
        print(f"[Controller] Action {new_action} assignée à la transition {source_id}->{target_id}")
        self.model.update_transition_action(source_id, target_id, new_action)

    def update_node_position(self, node_id, x, y):
        print(f"[Controller] Localité {node_id} déplacée en ({x}, {y})")
        self.model.update_node_position(node_id, x, y)

    def update_nail_position(self, source_id, target_id, nail_index, x, y):
        print(f"[Controller] Clou n°{nail_index} de {source_id}->{target_id} déplacé en ({x}, {y})")
        self.model.update_nail_position(source_id, target_id, nail_index, x, y)

    def add_node_invariant(self, node_id, clock, operator, value):
        print(f"[Controller] Ajout de l'invariant {clock} {operator} {value} à {node_id}")
        self.model.add_node_invariant(node_id, clock, operator, value)
        # Rafraîchir la vue en simulant une nouvelle sélection
        self.handle_node_selected(node_id)

    def remove_node_invariant(self, node_id, index):
        print(f"[Controller] Suppression de l'invariant index {index} pour {node_id}")
        self.model.remove_node_invariant(node_id, index)
        # Rafraîchir la vue en simulant une nouvelle sélection
        self.handle_node_selected(node_id)

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