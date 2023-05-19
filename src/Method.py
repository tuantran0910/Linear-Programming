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

# Hàm Bland
def bland_method(c, A, b):
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

    # Vòng lặp Bland
    while True:
        # Tìm cột vào
        col_idx = next((j for j in range(n) if tableau[-1][j] < 0), None)

        # Kiểm tra điều kiện dừng
        if col_idx is None:
            break

        # Tìm hàng ra
        ratios = []
        for i in range(m):
            if tableau[i][col_idx] > 0:
                ratio = tableau[i][-1] / tableau[i][col_idx]
                ratios.append((i, ratio))

        # Kiểm tra vô nghiệm
        if not ratios:
            raise Exception("Bài toán vô nghiệm.")

        # Tìm hàng ra theo quy tắc Bland
        row_idx, min_ratio = min(ratios, key=lambda x: x[1])

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

