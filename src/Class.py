import numpy as np
import re

class Linear_Programming_Preprocessing:
    def __init__(self, input_file_path, obj_func_file_path, cons_file_path, var_cond_file_path):
        self.input_file_path = input_file_path
        self.obj_func_file_path = obj_func_file_path
        self.cons_file_path = cons_file_path
        self.var_cond_file_path = var_cond_file_path
        self.num_variables = 0
        self.num_constraints = 0
        self.objective_sign = None
        self.coef_obj = []
        self.left_cons = None
        self.right_cons = None
        self.variables = []

    def __get_num_variables_cond(self, file_path):
        with open(file_path, "r") as f:
            num_variables_cond = len(f.readlines())
            f.close()
        return num_variables_cond

    def get_num_variables_constraints(self, file_path):
        with open(file_path, "r") as f:
            num_variables = int(f.readline())
            num_constraints = int(f.readline())
            f.close()
        return num_variables, num_constraints

    def __get_existing_variables(self, components):
        variables = []
        for component in components:
            variables.append(
                re.split(">=|<=| ", component)[0][-(len(str(self.num_variables)) + 1) :]
            )
        return variables

    def __get_missing_variables_index(self, existing_variables):
        missing_variables = set()
        for i in range(self.num_variables):
            if "x{}".format(i + 1) not in existing_variables:
                missing_variables.add(i)
        return list(missing_variables)

    def objective_function(self):
        with open(self.obj_func_file_path, "r") as f:
            objective_string = f.read()
            object_components = objective_string.split()
            self.objective_sign = object_components[0]
            object_components.remove(self.objective_sign)

            exist_variables = self.__get_existing_variables(object_components)
            missing_variables_index = self.__get_missing_variables_index(exist_variables)
            # Extract coef
            for component in object_components:
                coef_string = component.split("x")[0]
                if len(coef_string) == 0:
                    coef = int(coef_string.replace("", "1"))
                elif len(coef_string) == 1:
                    coef = int(coef_string.replace("-", "-1"))
                else:
                    coef = int(coef_string)
                self.coef_obj.append(coef)

            if len(missing_variables_index) > 0:
                for i in missing_variables_index:
                    self.coef_obj.insert(i, 0)

            self.coef_obj = np.asarray(self.coef_obj)
            if self.objective_sign == "max":
                self.coef_obj = -1 * self.coef_obj
            f.close()

    def constraints(self):
        with open(self.cons_file_path, "r") as f:
            constraint_string = f.readlines()
            self.left_cons = np.zeros((self.num_constraints, self.num_variables), dtype=int)
            self.right_cons = np.zeros((self.num_constraints, 1))
            constraints_components = [i.split() for i in constraint_string]
            for i in range(self.num_constraints):
                component_string = constraints_components[i]
                sign = component_string[-2]        
                self.right_cons[i] = int(component_string[-1])
                row_left_cons = []
                for component in component_string[:-2]:
                    coef_string = component.split("x")[0]
                    if len(coef_string) == 0:
                        coef = int(coef_string.replace("", "1"))
                    elif len(coef_string) == 1:
                        coef = int(coef_string.replace("-", "-1"))
                    else:
                        coef = int(coef_string)
                    row_left_cons.append(coef)
                
                exist_variables = self.__get_existing_variables(component_string[:-2])
                missing_variables_index = self.__get_missing_variables_index(exist_variables)
                if len(missing_variables_index) > 0:
                    for j in missing_variables_index:
                        row_left_cons.insert(j, 0)
                self.left_cons[i] = row_left_cons
                if sign == ">=":
                    self.left_cons[i] = -1 * self.left_cons[i]
                    self.right_cons[i] = -1 * self.right_cons[i]
                elif sign == "=":
                    self.left_cons = np.vstack((self.left_cons, -1 * self.left_cons[i]))
                    self.right_cons = np.vstack((self.right_cons, [-int(component_string[-1])]))
                    self.num_constraints += 1
            # self.right_cons = np.asarray(self.right_cons)
            f.close()

    def preprocessing(self):
        self.num_variables, self.num_constraints = self.get_num_variables_constraints(self.input_file_path)
        self.objective_function()
        self.constraints()
        variables = ["x{}".format(i + 1) for i in range(self.num_variables)]
        num_variables_cond = self.__get_num_variables_cond(self.var_cond_file_path)
        with open(self.var_cond_file_path, "r") as f:
            var_cond_components = f.readlines()
            f.close()    
        
        for i in range(len(var_cond_components)):
            components = var_cond_components[i].split()
            if components[0][0] == "-":
                if components[-2] == ">=":
                    components[0] = components[0].replace("-", "")
                    components[-2] = "<="
                elif components[-2] == "<=":
                    components[0] = components[0].replace("-", "")
                    components[-2] = ">="
                var_cond_components[i] = " ".join(components)
        
        if num_variables_cond < self.num_variables:
            existing_variables = self.__get_existing_variables(var_cond_components)
            missing_variables_index = self.__get_missing_variables_index(existing_variables)
            add_left_cons = np.zeros((self.num_constraints, len(missing_variables_index)), dtype = int)
            add_variables = []
            for i in range(len(missing_variables_index)):
                add_variables.append("x{}-".format(missing_variables_index[i] + 1))
                variables[missing_variables_index[i]] = "x{}+".format(missing_variables_index[i] + 1)
            for i in range(self.num_constraints):
                row_component_left_cons = self.left_cons[i]
                add_left_cons[i] = row_component_left_cons[missing_variables_index] * -1
            self.left_cons = np.hstack((self.left_cons, add_left_cons))
            self.coef_obj = np.hstack((self.coef_obj, self.coef_obj[missing_variables_index] * -1))
            self.num_variables = len(self.coef_obj)
            self.variables = variables + add_variables
        elif num_variables_cond == self.num_variables:
            self.variables = variables
         
        ltq_var_conds_index = []
        for idx in range(len(var_cond_components)):
            var_cond_component = var_cond_components[idx]
            var_cond_sign = var_cond_component.split()[-2]
            if var_cond_sign == "<=":
                ltq_var_conds_index.append(idx)
                
        if len(ltq_var_conds_index) > 0:
            for i in range(len(ltq_var_conds_index)):
                self.variables[ltq_var_conds_index[i]] += "*"
            self.coef_obj[ltq_var_conds_index] *= -1
            for i in range(self.num_constraints):
                self.left_cons[i][ltq_var_conds_index] *= -1
        
    def coef_objective_function(self):
        return self.coef_obj
    
    def coef_constraints(self):
        return self.left_cons, self.right_cons
    
    def get_variables(self):
        return self.variables
    
    def get_objective_function_sign(self):
        return self.objective_sign