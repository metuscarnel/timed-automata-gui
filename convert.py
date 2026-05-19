def convert_to_constraint_string(dbm_matrix):
    constraints = []
    visited_pairs = set()
    for i in range(len(dbm_matrix)):
        for j in range(len(dbm_matrix[i])):
            if (i, j) not in visited_pairs:
                if i == j:
                    visited_pairs.add((i, j))
                    continue
                if dbm_matrix[i][j] == 9999:
                    visited_pairs.add((i, j))
                    continue
                if dbm_matrix[i][j] == 0:
                    if i==0 or j==0:
                        visited_pairs.add((i, j))
                        continue
                    elif dbm_matrix[j][i] == 0:
                        constraints.append(f"x{i} = x{j}")
                        visited_pairs.add((i, j))
                        visited_pairs.add((j, i))
                    else:
                        constraints.append(f"x{i} <= x{j}")
                        visited_pairs.add((i, j))

                else:
                    if i == 0:
                        if dbm_matrix[i][j] == -dbm_matrix[j][i]:
                            constraints.append(f"x{j} = {-dbm_matrix[i][j]}")
                            visited_pairs.add((i, j))
                            visited_pairs.add((j, i))
                        else:
                            if j != 0:
                                if (j, i) not in visited_pairs:
                                    constraints.append(f"{-dbm_matrix[i][j]} <= x{j} <= {dbm_matrix[j][i]}")
                                    visited_pairs.add((i, j))
                                    visited_pairs.add((j, i))
                            else:
                                constraints.append(f"x{j} >= {-dbm_matrix[i][j]}")
                                visited_pairs.add((i, j))
                    elif j == 0:
                        if dbm_matrix[i][j] == -dbm_matrix[j][i]:
                            constraints.append(f"x{i} = {dbm_matrix[i][j]}")
                            visited_pairs.add((i, j))
                            visited_pairs.add((j, i))
                        else:
                            if (j, i) not in visited_pairs:
                                constraints.append(f"{-dbm_matrix[j][i]} <= x{i} <= {dbm_matrix[i][j]}")
                                visited_pairs.add((i, j))
                                visited_pairs.add((j, i))

                            else:
                                constraints.append(f"x{i} <= {dbm_matrix[i][j]}")
                                visited_pairs.add((i, j))

                    else:
                        if dbm_matrix[i][j] == -dbm_matrix[j][i]:
                            constraints.append(f"x{i} - x{j} = {dbm_matrix[i][j]}")
                            visited_pairs.add((i, j))
                            visited_pairs.add((j, i))
                        else:
                            constraints.append(f"x{i} - x{j} <= {dbm_matrix[i][j]}")
                            visited_pairs.add((i, j))
    return constraints

import re

def build_dbm_from_constraints(constraints, num_clocks):
    # 1. Initialisation de la matrice avec 9999 (infini) et 0 sur la diagonale
    dbm = [[9999 for _ in range(num_clocks)] for _ in range(num_clocks)]
    for i in range(num_clocks):
        dbm[i][i] = 0

    # 2. Parsing des contraintes
    for constraint in constraints:
        # Nettoyage des espaces pour faciliter l'analyse par Regex
        c_str = constraint.replace(" ", "")
        
        # Format A : Inégalités encadrées (ex: -5<=x1<=10)
        match = re.fullmatch(r"(-?\d+)(<=|<)x(\d+)(<=|<)(-?\d+)", c_str)
        if match:
            c1 = int(match.group(1))
            i = int(match.group(3))
            c2 = int(match.group(5))
            dbm[0][i] = min(dbm[0][i], -c1)
            dbm[i][0] = min(dbm[i][0], c2)
            continue
            
        # Format B : Contraintes diagonales avec constante (ex: x1-x2<=5 ou x1-x2=5)
        match = re.fullmatch(r"x(\d+)-x(\d+)(<=|<|=)(-?\d+)", c_str)
        if match:
            i = int(match.group(1))
            j = int(match.group(2))
            op = match.group(3)
            val = int(match.group(4))
            if op == "=":
                dbm[i][j] = min(dbm[i][j], val)
                dbm[j][i] = min(dbm[j][i], -val)
            else:
                dbm[i][j] = min(dbm[i][j], val)
            continue
            
        # Format C : Contraintes diagonales simples (ex: x1<=x2 ou x1=x2)
        match = re.fullmatch(r"x(\d+)(<=|<|=)x(\d+)", c_str)
        if match:
            i = int(match.group(1))
            op = match.group(2)
            j = int(match.group(3))
            if op == "=":
                dbm[i][j] = min(dbm[i][j], 0)
                dbm[j][i] = min(dbm[j][i], 0)
            else:
                dbm[i][j] = min(dbm[i][j], 0)
            continue
            
        # Format D : Borne inférieure stricte (ex: x1>=2 ou x1>2)
        match = re.fullmatch(r"x(\d+)(>=|>)((-)?\d+)", c_str)
        if match:
            i = int(match.group(1))
            val = int(match.group(3))
            dbm[0][i] = min(dbm[0][i], -val)
            continue
            
        # Format E : Borne supérieure stricte ou égalité (ex: x1<=5, x1<5 ou x1=5)
        match = re.fullmatch(r"x(\d+)(<=|<|=)((-)?\d+)", c_str)
        if match:
            i = int(match.group(1))
            op = match.group(2)
            val = int(match.group(3))
            if op == "=":
                dbm[i][0] = min(dbm[i][0], val)
                dbm[0][i] = min(dbm[0][i], -val)
            else:
                dbm[i][0] = min(dbm[i][0], val)
            continue

    # 3. Fermeture canonique de Floyd-Warshall (Algorithme en O(V^3))
    # Cela permet de déduire les contraintes implicites entre les horloges
    for k in range(num_clocks):
        for i in range(num_clocks):
            for j in range(num_clocks):
                if dbm[i][k] != 9999 and dbm[k][j] != 9999:
                    if dbm[i][j] > dbm[i][k] + dbm[k][j]:
                        dbm[i][j] = dbm[i][k] + dbm[k][j]

    return dbm