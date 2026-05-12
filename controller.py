import pprint

class MainController:
    def __init__(self, model):
        self.model = model
        self.view = None

    def set_view(self, view):
        self.view = view

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

    def handle_add_action(self):
        print("[Controller] Bouton Action cliqué : Ouverture de la popup.")
        if self.view:
            self.view.show_action_dialog()

    def handle_add_clock(self):
        print("[Controller] Bouton Horloge cliqué : Ouverture de la popup.")
        if self.view:
            self.view.show_clock_dialog()

    def submit_action(self, action_name):
        print(f"[Controller] Réception de l'action : {action_name}")
        self.model.add_action(action_name)

    def submit_clock(self, clock_name):
        print(f"[Controller] Réception de l'horloge : {clock_name}")
        self.model.add_clock(clock_name)

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