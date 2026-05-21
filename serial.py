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
    
    output = {
        "actions": instance.get('actions', []),
        "clocks": clocks,
        "locations": list(instance.get('locations', {}).keys()),
        "init": instance.get('init', '')
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
                    print(f"   ↳ 🔀 [Transition {loc_id} -> {t['target']}] Gardes normalisées : {guard_strings}")
                    
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
        
    print("--- FIN DE L'EXTRACTION ---")
    print(f"✅ Compilation terminée avec succès ! Sauvegardé dans : {output_filepath}\n")
    return output

# --- Bloc de test ---
if __name__ == "__main__":
    model_instance = {
        'actions': [],
        'clocks': ['x', 'y', 'z'],
        'init': 'l0',
        'locations': {
            'l0': {'invariants': [{'clock': 'x', 'operator': '>=', 'type': 'clock', 'value': 'y', 'offset': 2}], 'node_pos': {'x': 362.0, 'y': 218.0}},
            'l1': {'invariants': [], 'node_pos': {'x': 605.0, 'y': 174.0}},
            'l2': {'invariants': [], 'node_pos': {'x': 639.0, 'y': 324.0}},
            'l3': {'invariants': [{'clock': 'y', 'operator': '==', 'type': 'value', 'value': '3'}], 'node_pos': {'x': 524.0, 'y': 378.0}}
        },
        'transitions': [
            {'guards': [{'clock': 'x', 'operator': '<=', 'type': 'clock', 'value': 'z'}], 'nails': [], 'source': 'l0', 'target': 'l1'},
            {'nails': [], 'source': 'l1', 'target': 'l2'},
            {'nails': [], 'source': 'l2', 'target': 'l3'},
            {'guards': [{'clock': 'x', 'operator': '>=', 'type': 'clock', 'value': 'z'}], 'nails': [], 'source': 'l0', 'target': 'l3'}
        ]
    }

    generate_and_save_engine_json(model_instance, "model_compiled.json")