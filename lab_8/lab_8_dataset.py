import pandas as pd
import numpy as np


# Підготовка вхідних даних
def parse_input_data(file_path):
    d_sample_data = pd.read_excel(file_path, parse_dates=['birth_date'])
    print('\nРеальні дані про позичальників')
    print(d_sample_data)
    Title_d_sample_data = d_sample_data.columns

    return d_sample_data, Title_d_sample_data

def analyze_data_structure(data):
    print('\nНазви стовпців DataFrame')
    print(data.columns)
    print('\nТипи даних стовпців DataFrame')
    print(data.dtypes)
    print('\nПропущені значення стовпців (суми)')
    print(data.isnull().sum())

def parse_data_description(file_path):
    d_data_description = pd.read_excel(file_path)
    print('\nСтруктура скорингової карти індикаторів')
    print(d_data_description)

    return d_data_description

# Первинне формування скорингової таблиці
def create_scoring_table(data_description, segment_data_description):
    d_segment_data_description_client_bank = segment_data_description[
        (segment_data_description.Place_of_definition == 'Вказує позичальник') |
        (segment_data_description.Place_of_definition == 'параметри, повязані з виданим продуктом')]
    n_client_bank = d_segment_data_description_client_bank['Place_of_definition'].size
    d_segment_data_description_client_bank.index = range(0, len(d_segment_data_description_client_bank))
    print('\nПервинне формування скорингової карти')
    print(d_segment_data_description_client_bank)

    return d_segment_data_description_client_bank

def check_column_overlap(data, segment_data_description):
    n_columns = segment_data_description['Field_in_data'].size
    j = 0
    Columns_Flag_True = np.zeros((n_columns))

    for i in range(0, n_columns):
        a = segment_data_description['Field_in_data'][i]
        if set([a]).issubset(data.columns):
            j = j + 1
            Columns_Flag_True[j] = i

    return Columns_Flag_True

def create_matched_data_frame(segment_data_description, column_indices):
    d_segment_data_description_client_bank_True = segment_data_description.iloc[column_indices]
    d_segment_data_description_client_bank_True.index = range(0, len(d_segment_data_description_client_bank_True))
    print('\nDataFrame співпадінь')
    print(d_segment_data_description_client_bank_True)

    return d_segment_data_description_client_bank_True

def clean_data(data, matched_data_frame):
    b = matched_data_frame['Field_in_data']
    d_segment_sample_data_client_bank = data[b]
    print('\nПропуски даних сегменту DataFrame')
    print(d_segment_sample_data_client_bank.isnull().sum())

    return d_segment_sample_data_client_bank

# Формування DataFrame даних з урахуванням відсутніх індикаторів скорингової таблиці
def drop_columns_with_nulls(data, columns_to_drop):
    d_segment_sample_cleaning = data.drop(columns=columns_to_drop)
    d_segment_sample_cleaning.index = range(0, len(d_segment_sample_cleaning))
    d_segment_sample_cleaning.to_excel('dataset/d_segment_sample_cleaning.xlsx')
    print('\nКонтроль наявності пропусків даних після очищення на індикаторах')
    print(d_segment_sample_cleaning.isnull().sum())
    print('\nDataFrame вхідних даних - скорингова карта')
    print(d_segment_sample_cleaning)
    print('\nDataFrame індикатори скорингу')
    print(data)

    return d_segment_sample_cleaning

# Головні виклики
if __name__ == '__main__':
    # Підготовка вхідних даних
    data, title_data = parse_input_data('dataset/sample_data.xlsx')
    analyze_data_structure(data)
    data_description = parse_data_description('dataset/data_description.xlsx')

    # Первинне формування скорингової таблиці
    segment_data_description_client_bank = create_scoring_table(data_description, data_description)
    column_indices = check_column_overlap(data, segment_data_description_client_bank)
    matched_data_frame = create_matched_data_frame(segment_data_description_client_bank, column_indices)
    data_cleaned = clean_data(data, matched_data_frame)

    # Формування DataFrame даних з урахуванням відсутніх індикаторів скорингової таблиці
    columns_to_drop = ['fact_addr_start_date', 'position_id', 'employment_date', 'has_prior_employment',
                       'prior_employment_start_date', 'prior_employment_end_date', 'income_frequency_other']
    data_final = drop_columns_with_nulls(data_cleaned, columns_to_drop)