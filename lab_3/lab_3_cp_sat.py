from ortools.sat.python import cp_model

def cp_model_solver():
    # Оптимізаційна математична модель
    model = cp_model.CpModel()
    var_upper_bound = max(24, 8, 16, 12)
    x1 = model.NewIntVar(0, var_upper_bound, 'x1')
    x2 = model.NewIntVar(0, var_upper_bound, 'x2')
    x3 = model.NewIntVar(0, var_upper_bound, 'x3')
    x4 = model.NewIntVar(0, var_upper_bound, 'x4')
    x5 = model.NewIntVar(0, var_upper_bound, 'x5')
    x6 = model.NewIntVar(0, var_upper_bound, 'x6')

    # Обмеження
    model.Add(3*x1 + 4*x2 <= 24)
    model.Add(1*x1 + 2*x2 <= 8)
    model.Add(4*x1 <= 16)
    model.Add(4*x2 <= 12)

    # Цільова функція ефективності
    efficiency_function = - 2*x1 - 2*x2
    model.Minimize(efficiency_function)

    # Вирішувач
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        efficiency_function_opt = solver.ObjectiveValue()
        print('Значення цільової функції в т. оптимуму:', efficiency_function_opt)
        x1_opt = solver.Value(x1)
        x2_opt = solver.Value(x2)
        x3_opt = solver.Value(x3)
        x4_opt = solver.Value(x4)
        x5_opt = solver.Value(x5)
        x6_opt = solver.Value(x6)
        print('x1 =', x1_opt)
        print('x2 =', x2_opt)
        print('x3 =', x3_opt)
        print('x4 =', x4_opt)
        print('x5 =', x5_opt)
        print('x6 =', x6_opt)
    else:
        print('Точки оптимуму не знайдено')

cp_model_solver()