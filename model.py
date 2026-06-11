from export_engine import generate_and_save_engine_json
from util import dbm_to_string_constraints as convert_dbm_to_constraints
import pprint
import re
import math

class AutomatonModel:
    def __init__(self): 
         self.clear()
         
    def clear(self):
        """Réinitialise complètement le modèle à son état vide (nouveau fichier)."""
        self.data = {
            "omit_ui_data": False,
            "locations": {},
            "init": "",
            "transitions": [],
            "actions": [],
            "clocks": [],
            "variables": {
                "definition": {
                    "define": [],
                    "typedef": {
                        "structure": {},
                        "alias": {}
                    }
                },
                "init_variables": [],
                "update_functions": {},
                "constraints": {}
            }
        }
        self.loc_counter = 0
        self.trans_counter = 0

    def add_location(self, x, y):
        """Crée l'entrée dans le buffer et retourne l'ID"""
        loc_id = f"l{self.loc_counter}"

        if self.loc_counter == 0:
            self.data["init"] = loc_id

        self.loc_counter += 1

        self.data["locations"][loc_id] = {
            "node_pos": {"x": x, "y": y},
            "invariants": [],  # Stocke la liste des conditions d'invariants
        }
        return loc_id

    def add_transition(self, source_id, target_id, nails_pos=None):
        """Ajoute une transition dans le modèle"""
        trans_id = f"t{self.trans_counter}"
        self.trans_counter += 1
        transition = {
            "id": trans_id,
            "source": source_id,
            "target": target_id,
            "nails": nails_pos or [],
        }
        self.data["transitions"].append(transition)
        return trans_id

    def get_transition(self, trans_id):
        for t in self.data["transitions"]:
            if t.get("id") == trans_id:
                return t
        return None

    def change_transition_endpoint(self, trans_id, new_source, new_target):
        """Modifie les points de départ ou d'arrivée d'une transition."""
        t = self.get_transition(trans_id)
        if t:
            t["source"] = new_source
            t["target"] = new_target

    def add_action(self, action_name):
        """Ajoute une action si elle n'existe pas déjà (ignore les doublons)."""
        if action_name and action_name not in self.data["actions"]:
            self.data["actions"].append(action_name)

    def add_clock(self, clock_name):
        """Ajoute une horloge si elle n'existe pas déjà (ignore les doublons)."""
        if clock_name and clock_name not in self.data["clocks"]:
            self.data["clocks"].append(clock_name)

    def update_transition_action(self, trans_id, action_name):
        """Met à jour l'action associée à une transition."""
        t = self.get_transition(trans_id)
        if t:
            t["action"] = action_name if action_name != "Aucune" else ""

    def update_node_position(self, node_id, x, y):
        """Met à jour les coordonnées d'une localité après un déplacement."""
        if node_id in self.data["locations"]:
            self.data["locations"][node_id]["node_pos"] = {"x": x, "y": y}

    def update_nail_position(self, trans_id, nail_index, x, y):
        """Met à jour les coordonnées d'un clou spécifique sur une transition après déplacement."""
        t = self.get_transition(trans_id)
        if t:
            if 0 <= nail_index < len(t["nails"]):
                t["nails"][nail_index] = (x, y)

    def add_node_invariant(
        self, node_id, clock, operator, target_type="value", target_value="0", offset=0
    ):
        """Ajoute une condition d'invariant pour une horloge sur une localité."""
        if node_id in self.data["locations"]:
            if "invariants" not in self.data["locations"][node_id]:
                self.data["locations"][node_id]["invariants"] = []

            invariants = self.data["locations"][node_id]["invariants"]
            new_inv = {
                "clock": clock,
                "operator": operator,
                "type": target_type,
                "value": target_value,
            }
            if target_type == "clock":
                new_inv["offset"] = offset
            invariants.append(new_inv)

    def remove_node_invariant(self, node_id, index):
        """Supprime un invariant spécifique d'une localité via son index."""
        if (
            node_id in self.data["locations"]
            and "invariants" in self.data["locations"][node_id]
        ):
            if 0 <= index < len(self.data["locations"][node_id]["invariants"]):
                self.data["locations"][node_id]["invariants"].pop(index)

    def add_transition_guard(
        self,
        trans_id,
        clock,
        operator,
        target_type="value",
        target_value="0",
        offset=0
    ):
        """Ajoute une condition de garde pour une horloge sur une transition."""
        t = self.get_transition(trans_id)
        if t:
            if "guards" not in t: t["guards"] = []
            new_guard = {
                "clock": clock,
                "operator": operator,
                "type": target_type,
                "value": target_value,
            }
            if target_type == "clock": new_guard["offset"] = offset
            t["guards"].append(new_guard)

    def remove_transition_guard(self, trans_id, index):
        """Supprime une garde spécifique d'une transition via son index."""
        t = self.get_transition(trans_id)
        if t:
            if "guards" in t and 0 <= index < len(t["guards"]):
                t["guards"].pop(index)

    def remove_transition(self, trans_id):
        """Supprime une transition de la liste du modèle."""
        t = self.get_transition(trans_id)
        if t:
            self.data["transitions"].remove(t)

    def set_initial_state(self, loc_id):
        """Définit la localité initiale si elle existe."""
        if loc_id in self.data["locations"]:
            self.data["init"] = loc_id

    def update_variables(self, new_variables_data):
        """Met à jour l'ensemble des données liées aux variables depuis l'éditeur de données."""
        self.data["variables"] = new_variables_data

    def remove_node(self, node_id):
        """Supprime une localité. (Les transitions sont déjà nettoyées par le contrôleur)."""
        if node_id in self.data["locations"]:
            del self.data["locations"][node_id]
        if self.data.get("init") == node_id:
            # Assigner une nouvelle localité initiale par défaut s'il en reste, pour éviter un champ vide
            self.data["init"] = next(iter(self.data["locations"].keys())) if self.data["locations"] else ""

    # generation du json
    def export_to_json(self, filepath):
        """Délègue la compilation DBM au script tiers, puis réordonne le JSON pour mettre 'variables' à la fin."""
        # 1. Sauvegarder le fichier initialement via le script existant
        result = generate_and_save_engine_json(self.data, filepath)
        
        # 2. Post-traitement : Forcer la clé "variables" à être la toute dernière dans le fichier généré
        try:
            import json
            with open(filepath, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                
            if "variables" in saved_data:
                # Retirer et réinsérer la clé la place automatiquement à la fin du dictionnaire (Python 3.7+)
                vars_content = saved_data.pop("variables")
                saved_data["variables"] = vars_content
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    # Réécriture propre du JSON avec variables à la fin
                    json.dump(saved_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[Model] Erreur lors de la réorganisation du JSON : {e}")
            
        return result

    # chargement du json pour reconstruire le dictionnaire "data" du model
    def load_from_json_data(self, json_data):
        """
        Reconstruit le dictionnaire de données interne au format strict du Modèle.
        Élimine toutes les matrices DBM pour ne conserver que les dictionnaires UI.
        """
        # 1. Initialisation de la structure pure attendue par l'UI et le Contrôleur
        self.trans_counter = 0
        
        # Détection d'un fichier externe (sans attributs de position UI)
        meta_keys = {"clocks", "actions", "init", "locations", "transitions", "variables"}
        has_any_pos = False
        for key, value in json_data.items():
            if key not in meta_keys and isinstance(value, dict):
                if "node_pos" in value:
                    has_any_pos = True
                    break
                    
        self.data = {
            "omit_ui_data": not has_any_pos,
            "actions": json_data.get("actions", []),
            "clocks": json_data.get("clocks", []),
            "init": json_data.get("init", ""),
            "locations": {},
            "transitions": [],
            "variables": json_data.get("variables", {
                "definition": {
                    "define": [],
                    "typedef": {
                        "structure": {},
                        "alias": {}
                    }
                },
                "init_variables": [],
                "update_functions": {},
                "constraints": {}
            })
        }
        # Ajout des données 
        # Génération de la map des horloges (indexation décalée de 1 car index 0 = x0)
        clock_map = {name: i + 1 for i, name in enumerate(self.data["clocks"])}

        def parse_to_dict(c_str):
            """Convertit une contrainte texte (DBM) en dictionnaire lisible par l'UI"""
            if isinstance(c_str, dict): return c_str
            clean_str = str(c_str).replace(" ", "")
            match = re.match(r"^([a-zA-Z0-9_]+)(?:-([a-zA-Z0-9_]+))?([<>=!]+)(-?\d+)$", clean_str)
            if match:
                c1, c2, op, val = match.groups()
                if c2 and c2 not in ["x0", "0"]:
                    return {"clock": c1, "operator": op, "type": "clock", "value": c2, "offset": int(val)}
                else:
                    return {"clock": c1, "operator": op, "type": "value", "value": val}
            return {"clock": str(c_str), "operator": "<=", "type": "value", "value": "0"}

        def safe_pos(pos_dict):
            """Extrait et garantit que les coordonnées (x,y) sont de type float, sinon renvoie 0.0"""
            if not isinstance(pos_dict, dict): return {"x": 0.0, "y": 0.0}
            try: x = float(pos_dict.get("x", 0.0))
            except (ValueError, TypeError): x = 0.0
            try: y = float(pos_dict.get("y", 0.0))
            except (ValueError, TypeError): y = 0.0
            return {"x": x, "y": y}

        # 2. Parcours du JSON pour extraire et traduire les données
        for key, value in json_data.items():
            if key not in meta_keys and isinstance(value, dict):
                
                # Traduction immédiate de la matrice d'invariant en dictionnaires UI
                raw_inv = value.get("invariant", [])
                invariants_textuels = [parse_to_dict(c) for c in convert_dbm_to_constraints(raw_inv, clock_map)] if raw_inv else []
                
                # Stockage exclusif des données nettoyées
                self.data["locations"][key] = {
                    "invariants": invariants_textuels,
                    "node_pos": safe_pos(value.get("node_pos")),
                    "name_pos": safe_pos(value.get("name_pos")),
                    "invariant_pos": safe_pos(value.get("invariant_pos"))
                }

                # Traitement des transitions sortantes de cette localité
                transitions_du_noeud = value.get("transitions", [])
                layouts_des_transitions = value.get("transitions_layout", [])

                for idx, t in enumerate(transitions_du_noeud):
                    # Traduction immédiate de la matrice de garde en dictionnaires UI
                    raw_guard = t[1]
                    gardes_textuelles = [parse_to_dict(c) for c in convert_dbm_to_constraints(raw_guard, clock_map)] if raw_guard else []
                    
                    raw_nails = layouts_des_transitions[idx] if idx < len(layouts_des_transitions) else []
                    clean_nails = []
                    if isinstance(raw_nails, list):
                        for n in raw_nails:
                            try:
                                if isinstance(n, dict): # Format Cosmos
                                    clean_nails.append([float(n.get("x", 0.0)), float(n.get("y", 0.0))])
                                elif isinstance(n, (list, tuple)) and len(n) >= 2: # Format liste strict
                                    clean_nails.append([float(n[0]), float(n[1])])
                            except (ValueError, TypeError):
                                pass

                    # Reconstruction de la transition selon la structure exacte du modèle
                    trans_id = f"t{self.trans_counter}"
                    self.trans_counter += 1
                    transition_dict = {
                        "id": trans_id,
                        "guards": gardes_textuelles,
                        "nails": clean_nails,
                        "resets": t[2] if t[2] else [],
                        "source": key,
                        "target": t[3],
                        "action": t[0] if t[0] else ""
                    }

                    self.data["transitions"].append(transition_dict)

        # 3. Synchronisation du compteur de localités du modèle
        self.loc_counter = len(self.data["locations"])
        
        # --- Disposition automatique (Disposition Circulaire) ---
        # Assigne des positions temporaires si le fichier d'origine n'en contient pas
        if self.data.get("omit_ui_data", False):
            loc_keys = list(self.data["locations"].keys())
            num_locs = len(loc_keys)
            if num_locs > 0:
                radius = max(150, num_locs * 50)
                center_x, center_y = 400.0, 300.0
                for i, loc_id in enumerate(loc_keys):
                    angle = 2 * math.pi * i / num_locs
                    self.data["locations"][loc_id]["node_pos"] = {
                        "x": round(center_x + radius * math.cos(angle), 2),
                        "y": round(center_y + radius * math.sin(angle), 2)
                    }
                    
    def add_reset(self, clock, trans_id):
       #ajout d'un reset
        t = self.get_transition(trans_id)
        if t:
            if "resets" not in t: t["resets"] = []
            if clock not in t["resets"]: t["resets"].append(clock)

    def modify_clock(self, old_name, new_name):
        """Modifie le nom d'une horloge partout où elle est utilisée."""
        if old_name not in self.data["clocks"]: return
        if new_name in self.data["clocks"]: return # Eviter d'écraser
        
        idx = self.data["clocks"].index(old_name)
        self.data["clocks"][idx] = new_name
        
        for loc in self.data["locations"].values():
            for inv in loc.get("invariants", []):
                if inv.get("clock") == old_name:
                    inv["clock"] = new_name
                if inv.get("type") == "clock" and inv.get("value") == old_name:
                    inv["value"] = new_name
                    
        for t in self.data["transitions"]:
            for guard in t.get("guards", []):
                if guard.get("clock") == old_name:
                    guard["clock"] = new_name
                if guard.get("type") == "clock" and guard.get("value") == old_name:
                    guard["value"] = new_name
            if "resets" in t:
                t["resets"] = [new_name if r == old_name else r for r in t["resets"]]

    def delete_clock(self, clock_name):
        """Supprime une horloge et toutes les contraintes qui l'utilisent."""
        if clock_name not in self.data["clocks"]: return
        
        self.data["clocks"].remove(clock_name)
        
        for loc in self.data["locations"].values():
            if "invariants" in loc:
                loc["invariants"] = [inv for inv in loc["invariants"] 
                                     if inv.get("clock") != clock_name and not (inv.get("type") == "clock" and inv.get("value") == clock_name)]
        
        for t in self.data["transitions"]:
            if "guards" in t:
                t["guards"] = [guard for guard in t["guards"] 
                               if guard.get("clock") != clock_name and not (guard.get("type") == "clock" and guard.get("value") == clock_name)]
            if "resets" in t and clock_name in t["resets"]:
                t["resets"].remove(clock_name)

    def modify_action(self, old_name, new_name):
        """Modifie le nom d'une action partout où elle est utilisée."""
        if old_name not in self.data["actions"]: return
        if new_name in self.data["actions"]: return
        
        idx = self.data["actions"].index(old_name)
        self.data["actions"][idx] = new_name
        
        for t in self.data["transitions"]:
            if t.get("action") == old_name:
                t["action"] = new_name
                
        vars_data = self.data.get("variables", {})
        if "update_functions" in vars_data and old_name in vars_data["update_functions"]:
            vars_data["update_functions"][new_name] = vars_data["update_functions"].pop(old_name)
        if "constraints" in vars_data and old_name in vars_data["constraints"]:
            vars_data["constraints"][new_name] = vars_data["constraints"].pop(old_name)

    def delete_action(self, action_name):
        """Supprime une action et ses données additionnelles (update-functions et contraintes)."""
        if action_name not in self.data["actions"]: return
        
        self.data["actions"].remove(action_name)
        
        for t in self.data["transitions"]:
            if t.get("action") == action_name:
                t["action"] = ""
                
        vars_data = self.data.get("variables", {})
        if "update_functions" in vars_data and action_name in vars_data["update_functions"]:
            del vars_data["update_functions"][action_name]
        if "constraints" in vars_data and action_name in vars_data["constraints"]:
            del vars_data["constraints"][action_name]
    
    