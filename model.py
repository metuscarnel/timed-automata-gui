class AutomatonModel:
    def __init__(self):
        self.data = {"locations": {}, "init": "", "transitions": []}
        self.loc_counter = 0

    def add_location(self, x, y):
        """Crée l'entrée dans le buffer et retourne l'ID"""
        loc_id = f"l{self.loc_counter}"
        
        if self.loc_counter == 0:
            self.data["init"] = loc_id
            
        self.loc_counter += 1
            
        self.data["locations"][loc_id] = {
            "node_pos": {"x": x, "y": y},
            "invariant": [] # On garde ça simple pour ce test
        }
        return loc_id

    def add_transition(self, source_id, target_id):
        """Ajoute une transition dans le modèle"""
        transition = {
            "source": source_id,
            "target": target_id
        }
        self.data["transitions"].append(transition)