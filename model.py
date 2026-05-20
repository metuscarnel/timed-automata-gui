from serial import generate_and_save_engine_json
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

    def add_node_invariant(self, node_id, clock, operator, target_type="value", target_value="0", offset=0):
        """Ajoute ou met à jour une condition d'invariant pour une horloge sur une localité."""
        if node_id in self.data["locations"]:
            if "invariants" not in self.data["locations"][node_id]:
                self.data["locations"][node_id]["invariants"] = []
            
            invariants = self.data["locations"][node_id]["invariants"]
            to_remove = []
            updated = False
            
            for i, inv in enumerate(invariants):
                same_target = (inv["clock"] == clock and inv["type"] == target_type)
                if same_target and target_type == "clock" and inv["value"] != target_value:
                    same_target = False
                    
                if same_target:
                    same_operator = (inv["operator"] == operator)
                    same_value = (inv["value"] == target_value)
                    if target_type == "clock" and inv.get("offset", 0) != offset:
                        same_value = False
                        
                    # Remplace si même opérateur, même valeur exacte, ou si on impose une égalité (==)
                    if same_operator or same_value or operator == "==" or inv["operator"] == "==":
                        if not updated:
                            inv["operator"] = operator
                            inv["value"] = target_value
                            if target_type == "clock":
                                inv["offset"] = offset
                            elif "offset" in inv:
                                del inv["offset"]
                            updated = True
                        else:
                            to_remove.append(i)
                            
            for i in reversed(to_remove):
                invariants.pop(i)
                
            if not updated:
                new_inv = {"clock": clock, "operator": operator, "type": target_type, "value": target_value}
                if target_type == "clock":
                    new_inv["offset"] = offset
                invariants.append(new_inv)

    def remove_node_invariant(self, node_id, index):
        """Supprime un invariant spécifique d'une localité via son index."""
        if node_id in self.data["locations"] and "invariants" in self.data["locations"][node_id]:
            if 0 <= index < len(self.data["locations"][node_id]["invariants"]):
                self.data["locations"][node_id]["invariants"].pop(index)

    def add_transition_guard(self, source_id, target_id, clock, operator, target_type="value", target_value="0", offset=0):
        """Ajoute ou met à jour une condition de garde pour une horloge sur une transition."""
        for t in self.data["transitions"]:
            if t["source"] == source_id and t["target"] == target_id:
                if "guards" not in t:
                    t["guards"] = []
                
                guards = t["guards"]
                to_remove = []
                updated = False
                
                for i, guard in enumerate(guards):
                    same_target = (guard["clock"] == clock and guard["type"] == target_type)
                    if same_target and target_type == "clock" and guard["value"] != target_value:
                        same_target = False
                        
                    if same_target:
                        same_operator = (guard["operator"] == operator)
                        same_value = (guard["value"] == target_value)
                        if target_type == "clock" and guard.get("offset", 0) != offset:
                            same_value = False
                            
                        if same_operator or same_value or operator == "==" or guard["operator"] == "==":
                            if not updated:
                                guard["operator"] = operator
                                guard["value"] = target_value
                                if target_type == "clock":
                                    guard["offset"] = offset
                                elif "offset" in guard:
                                    del guard["offset"]
                                updated = True
                            else:
                                to_remove.append(i)
                                
                for i in reversed(to_remove):
                    guards.pop(i)
                    
                if not updated:
                    new_guard = {"clock": clock, "operator": operator, "type": target_type, "value": target_value}
                    if target_type == "clock":
                        new_guard["offset"] = offset
                    guards.append(new_guard)
                break

    def remove_transition_guard(self, source_id, target_id, index):
        """Supprime une garde spécifique d'une transition via son index."""
        for t in self.data["transitions"]:
            if t["source"] == source_id and t["target"] == target_id:
                if "guards" in t and 0 <= index < len(t["guards"]):
                    t["guards"].pop(index)
                break

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
    
    def export_to_json(self, filepath):
        """Délègue la compilation DBM et la sauvegarde au script tiers"""
        return generate_and_save_engine_json(self.data, filepath)