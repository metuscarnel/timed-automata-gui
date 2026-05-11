class MainController:
    def __init__(self, model):
        self.model = model
        self.view = None
        self.source_node_id = None # Mémorise le 1er noeud cliqué pour la Transition

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

    def handle_node_click(self, node_id):
        """Gère le clic sur un noeud existant."""
        if self.view and self.view.canvas.creation_mode == "transition":
            if not self.source_node_id:
                # 1er clic : On enregistre le noeud de départ
                self.source_node_id = node_id
                print(f"[Controller] Transition : Noeud source sélectionné -> {node_id}")
            else:
                # 2ème clic : On a la cible, on crée la transition !
                self.model.add_transition(self.source_node_id, node_id)
                self.view.canvas.draw_transition(self.source_node_id, node_id)
                print(f"[Controller] Transition créée de {self.source_node_id} à {node_id}")
                self.source_node_id = None # Réinitialisation pour en dessiner d'autres

    def handle_add_transition(self, checked=False):
        print(f"[Controller] Bouton Transition cliqué (Actif: {checked})")
        self.source_node_id = None # On annule toute sélection en cours
        if self.view:
            if checked:
                self.view.canvas.set_creation_mode("transition")
            else:
                self.view.canvas.set_creation_mode(None)

    def handle_add_action(self):
        print("[Controller] Bouton Action cliqué : Action à définir.")

    def handle_add_clock(self):
        print("[Controller] Bouton Horloge cliqué : Action à définir.")

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