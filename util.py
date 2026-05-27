def dbm_to_string_constraints(dbm, clock_map):
    """
    Parcourt une DBM et reconstruit la liste de dictionnaires au format de création UI.
    Exemple de sortie : [{'clock': 'x', 'operator': '<=', 'type': 'clock', 'value': 'y', 'offset': 2}]
    Fusionne automatiquement les paires en un opérateur '=='.
    """
    # 1. Inverser la map pour retrouver les noms (ex: {1: 'x', 2: 'y'})
    inverse_clock_map = {0: 'x0'}
    for name, idx in clock_map.items():
        inverse_clock_map[idx] = name

    raw_constraints = []
    num_clocks = len(dbm)
    processed_pairs = set()

    for i in range(num_clocks):
        for j in range(num_clocks):
            # On ignore la diagonale
            if i == j: 
                continue
            # On ignore les paires déjà traitées pour les égalités
            if (i, j) in processed_pairs: 
                continue

            val_ij = dbm[i][j]
            # Gestion des formats d'infini
            if val_ij in ["inf", "infty", 9999]:
                continue
            
            val_ij = int(val_ij)
            
            # 2. Détection d'une Égalité (==)
            val_ji = dbm[j][i]
            is_equality = False
            if val_ji not in ["inf", "infty", 9999]:
                val_ji = int(val_ji)
                if val_ij == -val_ji:
                    is_equality = True
                    processed_pairs.add((j, i))

            # 3. Récupération des noms d'horloges
            c_i = inverse_clock_map[i]
            c_j = inverse_clock_map[j]

            # Cas A : Comparaison avec une constante (x0 - c_j <= V => c_j >= -V)
            if i == 0:
                op = '==' if is_equality else '>='
                raw_constraints.append({
                    'clock': c_j,
                    'operator': op,
                    'type': 'value',
                    'value': str(-val_ij)
                })
            
            # Cas B : Comparaison avec une constante (c_i - x0 <= V => c_i <= V)
            elif j == 0:
                op = '==' if is_equality else '<='
                raw_constraints.append({
                    'clock': c_i,
                    'operator': op,
                    'type': 'value',
                    'value': str(val_ij)
                })

            # Cas C : Comparaison entre deux horloges (c_i - c_j <= V => c_i <= c_j + V)
            else:
                op = '==' if is_equality else '<='
                raw_constraints.append({
                    'clock': c_i,
                    'operator': op,
                    'type': 'clock',
                    'value': c_j,
                    'offset': val_ij  # C'est l'offset exact sans le signe '-' de l'équation
                })
                
    return raw_constraints
if __name__ == "__main__":
    # 1. Tes données (telles que lues dans le JSON)
    clocks = ["x", "y", "z", "t"]
    clock_map = {name: i + 1 for i, name in enumerate(clocks)}

# Exemple d'une DBM 5x5 brute (0 pour x0, 1 pour x, 2 pour y, 3 pour z, 4 pour t)
# J'ai mis "inf" partout, sauf quelques contraintes pour tester.
    dbm_json = [
    [0,      "inf", -3,    "inf", "inf"], # Ligne x0 : x0 - y <= -3 (donc y >= 3)
    [5,      0,     "inf", "inf", "inf"], # Ligne x  : x - x0 <= 5  (donc x <= 5)
    ["inf",  2,     0,     "inf", "inf"], # Ligne y  : y - x <= 2
    ["inf",  "inf", "inf", 0,     "inf"], # Ligne z  : Aucune contrainte
    ["inf",  "inf", "inf", "inf", 0    ]  # Ligne t  : Aucune contrainte
    ]

# 2. Appel de la fonction
    resultat_strings = dbm_to_string_constraints(dbm_json, clock_map)

# 3. Résultat
    print(resultat_strings)