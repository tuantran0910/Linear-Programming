import numpy as np
# Hàm Danzig (Simplex)
def danzig_method(c, A, b):
    m, n = len(b), len(c)

    # Khởi tạo bảng Simplex
    tableau = [[0] * (n + m + 1) for _ in range(m + 1)]
    for i in range(m):
        tableau[i][:n] = A[i]
        tableau[i][n + i] = 1
        tableau[i][-1] = b[i]
    tableau[-1][:n] = c

    # Tìm cột cơ sở khởi đầu
    basis = list(range(n, n + m))

    # Vòng lặp Simplex
    while True:
        # Tìm cột vào
        col_idx = min(range(n), key=lambda j: tableau[-1][j])

        # Kiểm tra điều kiện dừng
        if tableau[-1][col_idx] >= 0:
            break

        # Tìm hàng ra
        row_idx = -1
        min_ratio = float('inf')
        for i in range(m):
            if tableau[i][col_idx] > 0:
                ratio = tableau[i][-1] / tableau[i][col_idx]
                if ratio < min_ratio:
                    row_idx = i
                    min_ratio = ratio

        # Kiểm tra vô nghiệm
        if row_idx == -1:
            raise Exception("Bài toán vô nghiệm.")

        # Cập nhật bảng Simplex
        pivot = tableau[row_idx][col_idx]
        for i in range(m + 1):
            tableau[i][col_idx] /= pivot
        for i in range(m + 1):
            if i != row_idx:
                ratio = tableau[i][col_idx]
                for j in range(n + m + 1):
                    tableau[i][j] -= ratio * tableau[row_idx][j]

        # Cập nhật cột cơ sở
        basis[row_idx] = col_idx

    # Tính giá trị tối ưu và giá trị biến
    opt_value = -tableau[-1][-1]
    opt_solution = [0] * n
    for i, j in enumerate(basis):
        if j < n:
            opt_solution[j] = tableau[i][-1]

    return opt_value, opt_solution

# Hàm Bland (Simplex)
def bland_method(c, A, b, variables, objective_sign):
    m, n = len(b), len(c)

    # Khởi tạo bảng Simplex
    tableau = np.array([[0] * (n + 1) for _ in range(m + 1)], dtype = float)
    
    # Tu vung dau tien
    tableau[0][1:] = c
    for i in range(1, m + 1):
        tableau[i][0] = b[i - 1]
        for j in range(1, n + 1):
            tableau[i][j] = -A[i - 1][j - 1]
    basis = ["w{}".format(i + 1) for i in range(m)]
    non_basis = variables.copy()
    
    print(tableau)
    while True:
        # Find in-column
        negative_basis = [[variables[i - 1], i] for i in range(1, n + 1) if tableau[0][i] < 0]
        if len(negative_basis) == 0:
            break
        col_idx = sorted(negative_basis, key = lambda j: j[0])[0][1]
        var_in = non_basis[col_idx - 1]
        
        # Check halt condition
        if all(x >= 0 for x in tableau[:, col_idx]):
            break
        
        # Find out-column
        row_idx = -1
        min_ratio = float('inf')
        for i in range(1, m + 1):
            if tableau[i][col_idx] >= 0:
                continue
            else:
                ratio = tableau[i][0] / -tableau[i][col_idx]
                if ratio < min_ratio:
                    row_idx = i
                    min_ratio = ratio

        # Check non-root (vo nghiem)
        if row_idx == -1:
            raise Exception("Bài toán vô nghiệm.")
        var_out = basis[row_idx - 1]
        
        # Cập nhật bảng Simplex
        pivot = tableau[row_idx][col_idx]
        add_right = np.zeros(m + 1)
        for i in range(m + 1):
            if i != row_idx:
                ratio = tableau[i][col_idx] / pivot
                add_right[i] = ratio
                for j in range(n + 1):
                    tableau[i][j] -= ratio * tableau[row_idx][j]
            else:
                # tableau[row_idx][col_idx] = coef
                add_right[i] = -1 / -pivot
                for j in range(0, n + 1):
                    tableau[row_idx][j] /= -pivot
        tableau = np.delete(tableau, col_idx, axis = 1)
        tableau = np.hstack((tableau, add_right.reshape(len(add_right), -1)))
        non_basis.remove(var_in)
        non_basis.append(var_out)
        basis[row_idx - 1] = var_in
        print(tableau)
        
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

