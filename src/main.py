from Class import *
import numpy as np
import pandas as pd
import Method as mt
import streamlit as st

if __name__ == "__main__":
    st.title("Chương trình giải bài toán Quy hoạch tuyến tính")
    student = pd.DataFrame({"Họ và Tên": ["Trần Ngọc Tuấn", "Mai Chiến Vĩ Thiên"], "MSSV": ["21280058", "21280049"], "Lớp": ["21KDL1", "21KDL1"]})
    student.index = [1, 2]
    st.table(student)
    soBien = st.text_input('Mời bạn nhập số biến:')
    soRangBuoc = st.text_input('Mời bạn nhập số ràng buộc:')
    file = open('data/dau_vao.txt', 'w')
    file.write(soBien+'\n')
    file.write(soRangBuoc)
    file.close()

    st.markdown("<u>Cách nhập hàm mục tiêu:</u>", unsafe_allow_html = True)
    st.caption("$min / max$ $z = c^Tx$", unsafe_allow_html = True)
    st.caption("- Nhập **'min'** hoặc **'max'** cho hàm mục tiêu trước.")
    st.caption("- Nhập hệ số đi kèm với biến xuất hiện trong hàm mục tiêu ( với hệ số dương ta chỉ cần nhập **số**, còn hệ số âm ta nhập thêm dấu **-**).", unsafe_allow_html=True)
    st.caption("Ví dụ: Nếu muốn nhập hàm mục tiêu là min 2x1 + 3x2 - 6x3 ta nhập như sau: min 2x1 3x2 -6x3.")
    hamMucTieu = st.text_input('Mời bạn nhập hàm mục tiêu: ')
    file = open('data/ham_muc_tieu.txt', 'w')
    file.write(hamMucTieu)
    file.close()

    st.markdown("<u>Cách nhập ràng buộc:</u>", unsafe_allow_html = True)
    st.caption("$a_i x \leq b_i, i \epsilon M_1$", unsafe_allow_html = True)
    st.caption("$a_i x \geq b_i, i \epsilon M_2$", unsafe_allow_html = True)
    st.caption("$a_i x = b_i, i \epsilon M_3$", unsafe_allow_html = True)
    st.caption("- Nhập hệ số đi kèm với biến xuất hiện trong hàm mục tiêu ( với hệ số dương ta chỉ cần nhập **số**, còn hệ số âm ta nhập thêm dấu **-**).")
    st.caption("- Nhập các phần tử cách nhau một khoảng trắng rồi nhập dấu của ràng buộc.")
    st.caption("- Mỗi ràng buộc nhập trên một dòng.")
    st.caption("Ví dụ cần nhập ràng buộc là 2x1 + 3x2 - 6x3 <= 9 ta nhập như sau: 2x1 3x2 -6x3 <= 9.")
    txt = st.text_area('Mời nhập các ràng buộc:')
    file = open('data/rang_buoc.txt', 'w')
    file.write(txt)
    file.close()

    st.markdown("<u>Cách nhập ràng buộc về dấu: </u>", unsafe_allow_html = True)
    st.caption("$x_j \geq 0, j \epsilon M_1$", unsafe_allow_html = True)
    st.caption("$x_j \leq 0, j \epsilon M_2$", unsafe_allow_html = True)
    st.caption("$x_j$ tự do, $j \epsilon M_3$", unsafe_allow_html = True)
    st.caption("- Nhập điều kiện của từng biến trên từng dòng")
    st.caption("- Nếu biến đó tự do thì không cần nhập điều kiện biến")
    st.caption("Ví dụ cần nhập điều kiện biến là x1 >= 0 ta nhập như sau: x1 >= 0")
    txt1 = st.text_area('Mời nhập các điều kiện biến:')
    file = open('data/dieu_kien_bien.txt', 'w')
    file.write(txt1)
    file.close()

    st.write("Click vào nút dưới đây để thực hiện giải bài toán:")
    if st.button('Solve'):
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
        
        if min(b) < 0:
            opt_value, opt_solution = mt.two_phase_method(c, A, b, variables, sign)
        elif min(b) == 0:
            opt_value, opt_solution = mt.bland_method(c, A, b, variables, sign)
        else:
            opt_value, opt_solution = mt.dantzig_method(c, A, b, variables, sign)
        
        gia_tri_toi_uu = "Giá trị tối ưu là: " + str(opt_value)
        st.write(gia_tri_toi_uu)
        st.write("Nghiệm tối ưu:")
        for key,value in opt_solution.items():
            nghiem = '- ' + key + ': ' + str(value)
            st.caption(nghiem)
    else:
        st.write('Bài toán chưa được giải')
    