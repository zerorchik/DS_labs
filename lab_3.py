import pandas as pd
import numpy as np

def file_parsing (data_name, df):
    for name, values in df[[data_name]].items():
        values
    n_df = int(len(values))
    df_real = np.zeros((n_df))
    for i in range(n_df):
        df_real[i] = values[i].replace(',', '.')
    return df_real, n_df

def matrix_generation (file_name):
    df = pd.read_excel(file_name)
    print(df)
    line_df = int(df.shape[0])
    column_df = int(df.shape[1])
    line_column_matrix = np.zeros(((line_df), (column_df - 2)))
    title_df = df.columns
    for i in range(1, (column_df - 1), 1):
        column_matrix, n_df = file_parsing(title_df[i], df)
        for j in range(len(column_matrix)):
            line_column_matrix[j, (i - 1)] = column_matrix[j]
    return line_column_matrix, title_df, n_df

def matrix_adapter (line_column_matrix, line):
    column_sample_matrix = np.shape(line_column_matrix)
    line_matrix = np.zeros((column_sample_matrix[1]))
    for j in range(column_sample_matrix[1]):
        line_matrix[j] = line_column_matrix[line, j]
    return line_matrix

def multicriteria_optimization(file_name, vag_koefs):
    # Вхідні дані
    line_column_matrix, title_df, n_df = matrix_generation(file_name)
    column_matrix = np.shape(line_column_matrix)

    # Зчитування критеріїв
    criteria_list = [matrix_adapter(line_column_matrix, i) for i in range(n_df)]

    # Нормалізація вагових коефіцієнтів
    normalization_koef = sum(vag_koefs)
    normalized_vag_koefs = np.array(vag_koefs) / normalization_koef
    print('\nНормалізовані вагові коефіцієнти')
    print(normalized_vag_koefs)

    # Нормалізація критеріїв
    sum_criteria = np.zeros(n_df)
    normalized_criteria = np.zeros((n_df, column_matrix[1]))
    integr_score = np.zeros((column_matrix[1]))
    for j in range(n_df):
        for i in range(column_matrix[1]):
            sum_criteria[j] += (1 / criteria_list[j][i]) if (j == 2 or j == 5 or (j >= 6 and j <= 9)) else \
            criteria_list[j][i]
    for i in range(column_matrix[1]):
        for j in range(n_df):
            normalized_criteria[j, i] = (1 / criteria_list[j][i]) / sum_criteria[j] if (j == 2 or j == 5 or (6 <= j <= 9)) else \
            criteria_list[j][i] / sum_criteria[j]

        # Розрахунок інтегральної оцінки
        integr_score[i] = np.sum(vag_koefs * (1 - normalized_criteria[:, i]) ** (-1))
    print('\nНормалізовані критерії')
    print(normalized_criteria)

    # Генерація оптимального рішення
    min_integr_score_index = np.argmin(integr_score)
    optimal_vehicle = title_df[min_integr_score_index + 1]
    print('\nІнтегрована оцінка:')
    print(integr_score)
    print('\nОптимальний позашляховик:', optimal_vehicle)
    return

# Головні виклики
file_name = 'outlander.xlsx'

vag_koefs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# vag_koefs = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
multicriteria_optimization(file_name, vag_koefs)