class AutomatonModel:
    def __init__(self):
        self.data = {
            "locations": {}, 
            "init": "", 
            "transitions": [],
            "actions": [],
            "clocks": []
        }
        self.loc_counter = 0

    def add_location(self, x, y):
        """Crée l'entrée dans le buffer et retourne l'ID"""
        loc_id = f"l{self.loc_counter}"
        
        if self.loc_counter == 0:
            self.data["init"] = loc_id
            
        self.loc_counter += 1
            
        self.data["locations"][loc_id] = {
            "node_pos": {"x": x, "y": y},
            "invariants": [] # Stocke la liste des conditions d'invariants
        }
        return loc_id

    def add_transition(self, source_id, target_id, nails_pos=None):
        """Ajoute une transition dans le modèle"""
        transition = {
            "source": source_id,
            "target": target_id,
            "nails": nails_pos or []
        }
        self.data["transitions"].append(transition)

    def add_action(self, action_name):
        """Ajoute une action si elle n'existe pas déjà (ignore les doublons)."""
        if action_name and action_name not in self.data["actions"]:
            self.data["actions"].append(action_name)

    def add_clock(self, clock_name):
        """Ajoute une horloge si elle n'existe pas déjà (ignore les doublons)."""
        if clock_name and clock_name not in self.data["clocks"]:
            self.data["clocks"].append(clock_name)

    def update_transition_action(self, source_id, target_id, action_name):
        """Met à jour l'action associée à une transition."""
        for t in self.data["transitions"]:
            if t["source"] == source_id and t["target"] == target_id:
                t["action"] = action_name if action_name != "Aucune" else ""
                break

    def update_node_position(self, node_id, x, y):
        """Met à jour les coordonnées d'une localité après un déplacement."""
        if node_id in self.data["locations"]:
            self.data["locations"][node_id]["node_pos"] = {"x": x, "y": y}

    def update_nail_position(self, source_id, target_id, nail_index, x, y):
        """Met à jour les coordonnées d'un clou spécifique sur une transition après déplacement."""
        for t in self.data["transitions"]:
            if t["source"] == source_id and t["target"] == target_id:
                if 0 <= nail_index < len(t["nails"]):
                    t["nails"][nail_index] = (x, y)
                break

    def add_node_invariant(self, node_id, clock, operator, value):
        """Ajoute ou met à jour une condition d'invariant pour une horloge sur une localité."""
        if node_id in self.data["locations"]:
            if "invariants" not in self.data["locations"][node_id]:
                self.data["locations"][node_id]["invariants"] = []
            
            # Vérifie si un invariant existe déjà pour cette horloge et le met à jour
            for inv in self.data["locations"][node_id]["invariants"]:
                if inv["clock"] == clock:
                    inv["operator"] = operator
                    inv["value"] = value
                    return
                    
            self.data["locations"][node_id]["invariants"].append({
                "clock": clock, "operator": operator, "value": value
            })

    def remove_node_invariant(self, node_id, index):
        """Supprime un invariant spécifique d'une localité via son index."""
        if node_id in self.data["locations"] and "invariants" in self.data["locations"][node_id]:
            if 0 <= index < len(self.data["locations"][node_id]["invariants"]):
                self.data["locations"][node_id]["invariants"].pop(index)

    def remove_transition(self, source_id, target_id):
        """Supprime une transition de la liste du modèle."""
        self.data["transitions"] = [
            t for t in self.data["transitions"] 
            if not (t["source"] == source_id and t["target"] == target_id)
        ]

    def remove_node(self, node_id):
        """Supprime une localité. (Les transitions sont déjà nettoyées par le contrôleur)."""
        if node_id in self.data["locations"]:
            del self.data["locations"][node_id]
        if self.data.get("init") == node_id:
            self.data["init"] = ""