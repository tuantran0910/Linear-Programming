from Class import *
import numpy as np
import Method as mt

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
    variables = test.get_variables()
    sign = test.get_objective_function_sign()
    
    opt_value, opt_solution = mt.dantzig_method(c, A, b, variables, sign)
    print(opt_value)
    print(opt_solution)

    # for id in c:
    #     if id < 0:
    #         DieuKienVoSoNghiem = False
    # if DieuKienVoSoNghiem:
    #     print("Bài toán vô số nghiệm")
    # else:
    #     opt_value, opt_solution = mt.bland_method(c, A, b)
    #     # In kết quả
    #     print("Kết quả:")
    #     print("z =", opt_value)
    #     for i, x in enumerate(opt_solution):
    #         print(f"x{i+1} =", x)
    # print(test.coef_objective_function())
    # print(test.coef_constraints()[0])
    # print(test.coef_constraints()[1])