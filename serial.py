import re
import json

def build_dbm_from_constraints(constraints, clock_map):
    num_clocks = len(clock_map) + 1
    dbm = [[9999 for _ in range(num_clocks)] for _ in range(num_clocks)]
    for i in range(num_clocks):
        dbm[i][i] = 0

    var = r"([a-zA-Z_]\w*)"

    for constraint in constraints:
        c_str = constraint.replace(" ", "")
        
        # Format A : Inégalités encadrées (ex: -5<=x<=10)
        match = re.fullmatch(r"(-?\d+)(<=|<)" + var + r"(<=|<)(-?\d+)", c_str)
        if match:
            c1, op1, name, op2, c2 = match.groups()
            i = clock_map[name]
            dbm[0][i] = min(dbm[0][i], -int(c1))
            dbm[i][0] = min(dbm[i][0], int(c2))
            continue
            
        # Format B : Contraintes diagonales avec constante (ex: x-y<=5)
        match = re.fullmatch(var + r"-" + var + r"(<=|<|=)(-?\d+)", c_str)
        if match:
            name_i, name_j, op, val = match.groups()
            i, j = clock_map[name_i], clock_map[name_j]
            val = int(val)
            if op == "=":
                dbm[i][j] = min(dbm[i][j], val)
                dbm[j][i] = min(dbm[j][i], -val)
            else:
                dbm[i][j] = min(dbm[i][j], val)
            continue
            
        # Format C : Contraintes diagonales simples (ex: x<=y)
        match = re.fullmatch(var + r"(<=|<|=)" + var, c_str)
        if match:
            name_i, op, name_j = match.groups()
            i, j = clock_map[name_i], clock_map[name_j]
            if op == "=":
                dbm[i][j] = min(dbm[i][j], 0)
                dbm[j][i] = min(dbm[j][i], 0)
            else:
                dbm[i][j] = min(dbm[i][j], 0)
            continue
            
        # Format D : Borne inférieure (ex: x>=2)
        match = re.fullmatch(var + r"(>=|>)(-?\d+)", c_str)
        if match:
            name_i, op, val = match.groups()
            i = clock_map[name_i]
            dbm[0][i] = min(dbm[0][i], -int(val))
            continue
            
        # Format E : Borne supérieure (ex: x<=5)
        match = re.fullmatch(var + r"(<=|<|=)(-?\d+)", c_str)
        if match:
            name_i, op, val = match.groups()
            i = clock_map[name_i]
            val = int(val)
            if op == "=":
                dbm[i][0] = min(dbm[i][0], val)
                dbm[0][i] = min(dbm[0][i], -val)
            else:
                dbm[i][0] = min(dbm[i][0], val)
            continue

    # Algorithme de Floyd-Warshall
    for k in range(num_clocks):
        for i in range(num_clocks):
            for j in range(num_clocks):
                if dbm[i][k] != 9999 and dbm[k][j] != 9999:
                    if dbm[i][j] > dbm[i][k] + dbm[k][j]:
                        dbm[i][j] = dbm[i][k] + dbm[k][j]
    return dbm

def parse_to_string_constraints(raw_constraints):
    string_constraints = []
    for c in raw_constraints:
        c_name = c['clock']
        op = c['operator']
        
        if c['type'] == 'clock':
            v_name = c['value']
            if op == '>=':
                string_constraints.append(f"{v_name}<={c_name}")
            elif op == '>':
                string_constraints.append(f"{v_name}<{c_name}")
            else:
                string_constraints.append(f"{c_name}{op}{v_name}")
        else:
            string_constraints.append(f"{c_name}{op}{c['value']}")
    return string_constraints

def generate_and_save_engine_json(instance, output_filepath="model_compiled.json"):
    clocks = instance.get('clocks', [])
    clock_map = {name: i + 1 for i, name in enumerate(clocks)}
    
    output = {
        "actions": instance.get('actions', []),
        "clocks": clocks,
        "locations": list(instance.get('locations', {}).keys()),
        "init": instance.get('init', '')
    }
    
    for loc_id, loc_data in instance.get('locations', {}).items():
        inv_raw = loc_data.get('invariants', [])
        inv_strings = parse_to_string_constraints(inv_raw)
        inv_matrix = build_dbm_from_constraints(inv_strings, clock_map)
        
        for r in range(len(inv_matrix)):
            for c in range(len(inv_matrix[r])):
                if inv_matrix[r][c] == 9999:
                    inv_matrix[r][c] = "inf"
                    
        out_transitions = []
        transitions_layout = []
        
        for t in instance.get('transitions', []):
            if t['source'] == loc_id:
                guard_raw = t.get('guards', [])
                guard_strings = parse_to_string_constraints(guard_raw)
                guard_matrix = build_dbm_from_constraints(guard_strings, clock_map)
                
                for r in range(len(guard_matrix)):
                    for c in range(len(guard_matrix[r])):
                        if guard_matrix[r][c] == 9999:
                            guard_matrix[r][c] = "inf"
                
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
if __name__ == "__main__":
    # Exemple d'utilisation
    instance = {
        'actions': [],
        'clocks': ['x', 'y', 'z'],
        'init': 'l0',
        'locations': {
            'l0': {'invariants': [{'clock': 'x', 'operator': '>=', 'type': 'clock', 'value': 'y'}], 'node_pos': {'x': 362.0, 'y': 218.0}},
            'l1': {'invariants': [], 'node_pos': {'x': 605.0, 'y': 174.0}},
            'l2': {'invariants': [], 'node_pos': {'x': 639.0, 'y': 324.0}},
            'l3': {'invariants': [{'clock': 'y', 'operator': '>=', 'type': 'value', 'value': '3'}], 'node_pos': {'x': 524.0, 'y': 378.0}}
        },
        'transitions': [
            {'guards': [{'clock': 'x', 'operator': '>=', 'type': 'clock', 'value': 'z'}], 'nails': [], 'source': 'l0', 'target': 'l1'},
            {'nails': [], 'source': 'l1', 'target': 'l2'},
            {'nails': [], 'source': 'l2', 'target': 'l3'},
            {'guards': [{'clock': 'x', 'operator': '>=', 'type': 'clock', 'value': 'z'}], 'nails': [], 'source': 'l0', 'target': 'l3'}
        ]
    }
    
    
    generate_and_save_engine_json(instance)