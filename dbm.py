import re

def build_dbm_from_constraints(constraints, clock_map):
    # Le nombre de dimensions de la matrice inclut l'horloge globale x0
    num_clocks = len(clock_map) + 1
    
    dbm = [[9999 for _ in range(num_clocks)] for _ in range(num_clocks)]
    for i in range(num_clocks):
        dbm[i][i] = 0

    # Regex pour capturer un vrai nom de variable (ex: x, y, z, horloge_1)
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
            
        # Format B : Contraintes diagonales avec constante (ex: x-y<=5 ou x-y=5)
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
            
        # Format C : Contraintes diagonales simples (ex: x<=y ou x=y)
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
            
        # Format D : Borne inférieure stricte (ex: x>=2 ou x>2)
        match = re.fullmatch(var + r"(>=|>)(-?\d+)", c_str) # Correction ici
        if match:
            name_i, op, val = match.groups() # Plus de crash !
            i = clock_map[name_i]
            dbm[0][i] = min(dbm[0][i], -int(val))
            continue
            
        # Format E : Borne supérieure stricte ou égalité (ex: x<=5, x<5 ou x=5)
        match = re.fullmatch(var + r"(<=|<|=)(-?\d+)", c_str) # Correction ici
        if match:
            name_i, op, val = match.groups() # Plus de crash !
            i = clock_map[name_i]
            val = int(val)
            if op == "=":
                dbm[i][0] = min(dbm[i][0], val)
                dbm[0][i] = min(dbm[0][i], -val)
            else:
                dbm[i][0] = min(dbm[i][0], val)
            continue

    # Fermeture de Floyd-Warshall
    for k in range(num_clocks):
        for i in range(num_clocks):
            for j in range(num_clocks):
                if dbm[i][k] != 9999 and dbm[k][j] != 9999:
                    if dbm[i][j] > dbm[i][k] + dbm[k][j]:
                        dbm[i][j] = dbm[i][k] + dbm[k][j]

    return dbm
# --- 2. Ton instance de modèle ---
model_instance = {
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

# --- 3. Le script de test et d'extraction mis à jour ---
def test_pipeline(instance):
    clocks = instance['clocks']
    # Mapping dynamique basé sur tes vrais noms : {'x': 1, 'y': 2, 'z': 3}
    clock_map = {name: i + 1 for i, name in enumerate(clocks)}
    
    raw_constraints = []
    
    # Extraction des Invariants
    for loc, data in instance['locations'].items():
        raw_constraints.extend(data.get('invariants', []))
        
    # Extraction des Gardes
    for trans in instance['transitions']:
        raw_constraints.extend(trans.get('guards', []))
        
    # Formatage en chaînes de caractères littérales (avec les vrais noms)
    string_constraints = []
    for c in raw_constraints:
        c_name = c['clock']
        op = c['operator']
        
        if c['type'] == 'clock':
            v_name = c['value']
            # On inverse toujours les > et >= pour correspondre au format var<=var de la regex
            if op == '>=':
                string_constraints.append(f"{v_name}<={c_name}")
            elif op == '>':
                string_constraints.append(f"{v_name}<{c_name}")
            else:
                string_constraints.append(f"{c_name}{op}{v_name}")
        else:
            string_constraints.append(f"{c_name}{op}{c['value']}")
            
    print("--- 1. Liste des contraintes extraites ---")
    for s in string_constraints:
        print(s)  # Tu verras ici "y<=x" au lieu de "x2<=x1"
        
    # Génération de la DBM
    dbm = build_dbm_from_constraints(string_constraints, clock_map)
    
    print("\n--- 2. Matrice DBM Résultante ---")
    header = ["x0"] + clocks
    print(f"{'':>5} | " + " | ".join([f"{h:>4}" for h in header]))
    print("-" * 35)
    
    # Label de l'horloge 0
    labels = ["x0"] + clocks
    for i, row in enumerate(dbm):
        row_label = labels[i]
        formatted_row = [f"{'INF':>4}" if val == 9999 else f"{val:>4}" for val in row]
        print(f"{row_label:>5} | " + " | ".join(formatted_row))

if __name__ == "__main__":
    test_pipeline(model_instance)