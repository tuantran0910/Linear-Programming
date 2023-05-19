from Class import *
import numpy as np

def simplex_danzig(c, A, b):
    m, n = A.shape
    tableau = np.zeros((m+1, n+1))
    tableau[:-1, :-1] = A
    tableau[:-1, -1] = b
    tableau[-1, :-1] = -c
    
    pivot_col = np.argmin(tableau[-1, :-1])
    iteration = 0
    
    while np.any(tableau[-1, :-1] < 0):
        iteration += 1
        print(f"Iteration {iteration}:")
        
        ratios = np.divide(tableau[:-1, -1], tableau[:-1, pivot_col], out=np.full(m, np.inf), where=tableau[:-1, pivot_col] > 0)
        pivot_row = np.argmin(ratios)
        
        pivot = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot
        
        print(f"Entering Variable (Pivot Column): x{pivot_col+1}")
        print(f"Leaving Variable (Pivot Row): x{pivot_row+1}")
        
        for i in range(m+1):
            if i != pivot_row:
                factor = tableau[i, pivot_col]
                tableau[i, :] -= factor * tableau[pivot_row, :]
        
        pivot_col = np.argmin(tableau[-1, :-1])
        
        print("Tableau:")
        print(tableau)
        print()
    
    objective_value = -tableau[-1, -1]
    optimal_solution = tableau[:-1, -1]
    
    return objective_value, optimal_solution

if __name__ == "__main__":
    test = Linear_Programming_Preprocessing(
        "data/dau_vao.txt",
        "data/ham_muc_tieu.txt",
        "data/rang_buoc.txt",
        "data/dieu_kien_bien.txt",
    )
    test.preprocessing()
    c = test.coef_objective_function()
    A = test.coef_constraints()[0]
    b = test.coef_constraints()[1]

    objective_value, optimal_solution = simplex_danzig(c, A, b)

    print("Optimal Objective Value:", objective_value)
    print("Optimal Solution:", optimal_solution)
    # print(test.coef_objective_function())
    # print(test.coef_constraints()[0])
    # print(test.coef_constraints()[1])