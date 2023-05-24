import numpy as np
# Hàm Dantzig (Simplex)
def dantzig_method(c, A, b, variables, objective_sign):
    m, n = len(b), len(c)
    
    # Khoi tao bang Simplex
    tableau = np.array([[0] * (n + 1) for _ in range(m + 1)], dtype = float)
    
    # Tu vung dau tien
    tableau[0][1:] = c
    for i in range(1, m + 1):
        tableau[i][0] = b[i - 1]
        for j in range(1, n + 1):
            tableau[i][j] = -A[i - 1][j - 1]
    
    # Bien co so va khong co so ban dau
    basis = ["w{}".format(i + 1) for i in range(m)]
    non_basis = variables.copy()
    
    while True:
        # Tim kiem bien vao
        negative_non_basis = [[variables[i - 1], i] for i in range(1, n + 1) if tableau[0, i] < 0]
        if len(negative_non_basis) == 0:
            break
        col_idx = sorted(negative_non_basis, key = lambda j: j[0])[0][1]
        var_in = non_basis[col_idx - 1]
        # Check dieu kien dung
        if all(x >= 0 for x in tableau[:, col_idx]):
            break
        
        # Tim kiem bien ra
        row_idx = -1
        min_ratio = float('inf')
        for i in range(1, m + 1):
            if tableau[i, col_idx] >= 0:
                continue
            else:
                ratio = tableau[i, 0] / -tableau[i, col_idx]
                if ratio < min_ratio:
                    row_idx = i
                    min_ratio = ratio

        # Check vo nghiem
        if row_idx == -1:
            raise Exception("Bài toán vô nghiệm.")
        var_out = basis[row_idx - 1]
        
        # Cập nhật bảng Simplex
        pivot = tableau[row_idx, col_idx]
        add_right = np.zeros(m + 1)
        
        # Xoay o cac hang khong chua bien ra
        for i in range(m + 1):
            if i != row_idx:
                ratio = tableau[i, col_idx] / pivot
                add_right[i] = ratio
                for j in range(n + 1):
                    tableau[i, j] -= ratio * tableau[row_idx, j]
        
        # Xoay o hang chua bien ra         
        add_right[row_idx] = -1 / -pivot
        for j in range(0, n + 1):
            tableau[row_idx][j] /= -pivot
        
        # Cap nhat tableau
        tableau = np.delete(tableau, col_idx, axis = 1)
        tableau = np.hstack((tableau, add_right.reshape(len(add_right), -1)))
        non_basis.remove(var_in)
        non_basis.append(var_out)
        basis[row_idx - 1] = var_in
        
    # Find optimal value and optimal variables
    opt_value = tableau[0, 0]
    if objective_sign == "max":
        opt_value *= -1
    
    variables_appeard_final_non_basics = []
    for i in range(n + 1):
        if i == 0:
            continue
        if tableau[0, i] != 0:
            variables_appeard_final_non_basics.append((i, non_basis[i - 1]))
    
    result_tableau = tableau
    result_tableau[:, [variable_appeard_final_non_basics[0] for variable_appeard_final_non_basics in variables_appeard_final_non_basics]] = 0
    
    final_solution = dict()        
    if len(variables_appeard_final_non_basics) == len(variables):
        for variable in variables_appeard_final_non_basics:
            if variable[0] in variables:
                final_solution[variable[0]] = 0
        for i in range(1, m + 1):
            if basis[i - 1] in variables:
                final_solution[basis[i - 1]] = result_tableau[i, 0]
    else:
        for variable in variables_appeard_final_non_basics:
            if variable[1] in variables:
                final_solution[variable[1]] = 0
        for i in range(1, m + 1):
            if basis[i - 1] in variables:
                for l in range(n + 1):
                    if l == 0:
                        final_solution[basis[i - 1]] = str(result_tableau[i, l])
                    else:
                        if result_tableau[i, l] != 0:
                            final_solution[basis[i - 1]] += " {}{}".format(result_tableau[i, l], non_basis[l - 1])
    opt_solution = final_solution
    return opt_value, opt_solution

# Hàm Bland (Simplex)
def bland_method(c, A, b, variables, objective_sign):
    m, n = len(b), len(c)
    
    # Khoi tao bang Simplex
    tableau = np.array([[0] * (n + 1) for _ in range(m + 1)], dtype = float)
    
    # Tu vung dau tien
    tableau[0][1:] = c
    for i in range(1, m + 1):
        tableau[i][0] = b[i - 1]
        for j in range(1, n + 1):
            tableau[i][j] = -A[i - 1][j - 1]
    
    # Bien co so va khong co so ban dau
    basis = ["w{}".format(i + 1) for i in range(m)]
    non_basis = variables.copy()
    
    while True:
        # Tim kiem bien vao
        print(tableau)
        negative_non_basis = [[variables[i - 1], i] for i in range(1, n + 1) if tableau[0, i] < 0]
        # Check dieu kien dung
        if len(negative_non_basis) == 0:
            break
        col_idx = sorted(negative_non_basis, key = lambda j: j[0])[0][1]
        var_in = non_basis[col_idx - 1]
        # if all(x >= 0 for x in tableau[:, col_idx]):
        #     break
        
        # Tim kiem bien ra
        row_idx = -1
        min_ratio = float('inf')
        for i in range(1, m + 1):
            if tableau[i, col_idx] >= 0:
                continue
            else:
                ratio = tableau[i, 0] / -tableau[i, col_idx]
                if ratio < min_ratio:
                    row_idx = i
                    min_ratio = ratio

        # Check vo nghiem
        if row_idx == -1:
            raise Exception("Bài toán vô nghiệm.")
        var_out = basis[row_idx - 1]
        # Cập nhật bảng Simplex
        pivot = tableau[row_idx, col_idx]
        add_right = np.zeros(m + 1)
        
        # Xoay o cac hang khong chua bien ra
        for i in range(m + 1):
            if i != row_idx:
                ratio = tableau[i, col_idx] / pivot
                add_right[i] = ratio
                for j in range(n + 1):
                    tableau[i, j] -= ratio * tableau[row_idx, j]
        
        # Xoay o hang chua bien ra         
        add_right[row_idx] = -1 / -pivot
        for j in range(0, n + 1):
            tableau[row_idx][j] /= -pivot
        
        # Cap nhat tableau
        tableau = np.delete(tableau, col_idx, axis = 1)
        tableau = np.hstack((tableau, add_right.reshape(len(add_right), -1)))
        non_basis.remove(var_in)
        non_basis.append(var_out)
        basis[row_idx - 1] = var_in
        
    # Find optimal value and optimal variables
    opt_value = tableau[0, 0]
    if objective_sign == "max":
        opt_value *= -1
    
    variables_appeard_final_non_basics = []
    for i in range(n + 1):
        if i == 0:
            continue
        if tableau[0, i] != 0:
            variables_appeard_final_non_basics.append((i, non_basis[i - 1]))
    
    result_tableau = tableau
    result_tableau[:, [variable_appeard_final_non_basics[0] for variable_appeard_final_non_basics in variables_appeard_final_non_basics]] = 0

    final_solution = dict()        
    if len(variables_appeard_final_non_basics) == len(variables):
        for variable in variables_appeard_final_non_basics:
            if variable[1] in variables:
                final_solution[variable[1]] = 0
        for i in range(1, m + 1):
            if basis[i - 1] in variables:
                final_solution[basis[i - 1]] = result_tableau[i, 0]
    else:
        for variable in variables_appeard_final_non_basics:
            if variable[1] in variables:
                final_solution[variable[1]] = 0
        for i in range(1, m + 1):
            if basis[i - 1] in variables:
                for l in range(n + 1):
                    if l == 0:
                        final_solution[basis[i - 1]] = str(result_tableau[i, l])
                    else:
                        if result_tableau[i, l] != 0:
                            final_solution[basis[i - 1]] += " {}{}".format(result_tableau[i, l], non_basis[l - 1])
    opt_solution = final_solution
    return opt_value, opt_solution

