import re
import json

def parse_to_string_constraints(raw_constraints):
    """
    Transforme les dictionnaires du modèle en chaînes normalisées 'xi-xj<=c'.
    Gère strictement et explicitement les opérateurs '<=', '>=' et '=='.
    """
    string_constraints = []
    for c in raw_constraints:
        c_name = c['clock']
        op = c['operator']
        
        if c['type'] == 'clock':
            v_name = c['value']
            val_const = int(c.get('offset', 0))
            
            if op == '>=':
                string_constraints.append(f"{v_name}-{c_name}<={-val_const}")
            elif op == '<=':
                string_constraints.append(f"{c_name}-{v_name}<={val_const}")
            elif op == '==':
                string_constraints.append(f"{c_name}-{v_name}<={val_const}")
                string_constraints.append(f"{v_name}-{c_name}<={-val_const}")
            else:
                raise ValueError(f"Erreur fatale : Opérateur '{op}' non reconnu pour une comparaison d'horloges.")
                
        else: # type == 'value'
            val_const = int(c['value'])
            
            if op == '>=':
                string_constraints.append(f"x0-{c_name}<={-val_const}")
            elif op == '<=':
                string_constraints.append(f"{c_name}-x0<={val_const}")
            elif op == '==':
                string_constraints.append(f"{c_name}-x0<={val_const}")
                string_constraints.append(f"x0-{c_name}<={-val_const}")
            else:
                raise ValueError(f"Erreur fatale : Opérateur '{op}' non reconnu pour une comparaison de constante.")
                
    return string_constraints


def build_dbm_from_constraints(constraints, clock_map):
    """
    Convertit les chaînes normalisées en matrice DBM brute (sans fermeture canonique).
    """
    num_clocks = len(clock_map) + 1
    # Initialisation avec 9999 (représentant l'infini)
    dbm = [[9999 for _ in range(num_clocks)] for _ in range(num_clocks)]
    
    # La diagonale d'une DBM vaut toujours 0 (xi - xi <= 0)
    for i in range(num_clocks):
        dbm[i][i] = 0

    # L'horloge globale x0 est fixée à l'index 0
    full_clock_map = {'x0': 0}
    full_clock_map.update(clock_map)

    # Regex pour capturer le format standardisé garanti par le parser
    var = r"([a-zA-Z_]\w*)"
    regex = var + r"-" + var + r"<=(-?\d+)"

    for constraint in constraints:
        c_str = constraint.replace(" ", "")
        match = re.fullmatch(regex, c_str)
        if match:
            name_i, name_j, val = match.groups()
            i = full_clock_map[name_i]
            j = full_clock_map[name_j]
            
            # On garde la contrainte la plus stricte s'il y a des doublons
            dbm[i][j] = min(dbm[i][j], int(val))
                        
    return dbm
def generate_and_save_engine_json(instance, output_filepath="model_compiled.json"):
    """
    Parcourt le modèle entier, génère toutes les DBM, affiche les contraintes et sauvegarde le JSON.
    """
    print("\n--- DÉBUT DE LA COMPILATION DES CONTRAINTES ---")
    
    clocks = instance.get('clocks', [])
    clock_map = {name: i + 1 for i, name in enumerate(clocks)}
    
    # Structuration stricte des variables selon le format attendu
    variables_raw = instance.get('variables', {})
    def_raw = variables_raw.get('definition', {})
    typedef_raw = def_raw.get('typedef', {})
    
    structured_variables = {
        "definition": {
            "define": def_raw.get("define", []),
            "typedef": {
                "structure": typedef_raw.get("structure", {}),
                "alias": typedef_raw.get("alias", {})
            }
        },
        "init_variables": variables_raw.get("init_variables", []),
        "update_functions": variables_raw.get("update_functions", {}),
        "constraints": variables_raw.get("constraints", {})
    }

    output = {
        "actions": instance.get('actions', []),
        "clocks": clocks,
        "locations": list(instance.get('locations', {}).keys()),
        "init": instance.get('init', ''),
        "variables": structured_variables
    }
    
    for loc_id, loc_data in instance.get('locations', {}).items():
        # --- Invariants ---
        inv_raw = loc_data.get('invariants', [])
        inv_strings = parse_to_string_constraints(inv_raw)
        
        # Affichage Console
        if inv_strings:
            print(f"📍 [Localité {loc_id}] Invariants normalisés : {inv_strings}")
            
        inv_matrix = build_dbm_from_constraints(inv_strings, clock_map)
        
        for r in range(len(inv_matrix)):
            for c in range(len(inv_matrix[r])):
                if inv_matrix[r][c] == 9999:
                    inv_matrix[r][c] = "infty"
                    
        # --- Gardes des transitions ---
        out_transitions = []
        transitions_layout = []
        
        for t in instance.get('transitions', []):
            if t['source'] == loc_id:
                guard_raw = t.get('guards', [])
                guard_strings = parse_to_string_constraints(guard_raw)
                
                # Affichage Console
                if guard_strings:
                    print(f"   ↳[Transition {loc_id} -> {t['target']}] Gardes normalisées : {guard_strings}")
                    
                guard_matrix = build_dbm_from_constraints(guard_strings, clock_map)
                
                for r in range(len(guard_matrix)):
                    for c in range(len(guard_matrix[r])):
                        if guard_matrix[r][c] == 9999:
                            guard_matrix[r][c] = "infty"
                
                action = t.get('action', "")
                resets = t.get('resets', [])
                target = t['target']
                
                out_transitions.append([action, guard_matrix, resets, target])
                transitions_layout.append(t.get('nails', []))
        
        output[loc_id] = {
            "node_pos": loc_data.get("node_pos", {"x": 0, "y": 0}),
            "name_pos": loc_data.get("name_pos", {"x": 0, "y": 0}),
            "invariant": inv_matrix,
            "invariant_pos": loc_data.get("invariant_pos", {"x": 0, "y": 0}),
            "transitions": out_transitions,
            "transitions_layout": transitions_layout
        }
        
    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
        return output
