import pandas as pd
import numpy as np

# Парсінг файлу вхідних даних
d_sample_data = pd.read_excel('sample_data.xlsx', parse_dates=['birth_date'])
print('\nСтруктура скорингової карти індикаторів')
print(d_sample_data)
Title_d_sample_data = d_sample_data.columns

# Аналіз структури вхідних даних
print('\nНазви стовпців DataFrame')
print(Title_d_sample_data)
print('\nТипи даних стовпців DataFrame')
print(d_sample_data.dtypes)
print('\nПропущені значення стовпців (суми)')
print(d_sample_data.isnull().sum())

# Парсинг файлу пояснень параметрів
d_data_description = pd.read_excel('data_description.xlsx')
print('\nСтруктура скорингової карти індикаторів')
print(d_data_description)

# Сегментація ознак клієнта та кредиту
d_segment_data_description_client_bank = d_data_description[(d_data_description.Place_of_definition == 'Вказує позичальник')
                                                            | (d_data_description.Place_of_definition == 'параметри, повязані з виданим продуктом')]
n_client_bank = d_segment_data_description_client_bank['Place_of_definition'].size
d_segment_data_description_client_bank.index = range(0, len(d_segment_data_description_client_bank))
print('\nПервинне формування скорингової карти')
print(d_segment_data_description_client_bank)

# Перевірка наявності індексів клієнта та кредиту з d_data_description в даних d_sample_data
b = d_segment_data_description_client_bank['Field_in_data']

# Кількість співпадінь
n_columns = d_segment_data_description_client_bank['Field_in_data'].size
j = 0
for i in range(0, n_columns):
    a = d_segment_data_description_client_bank['Field_in_data'][i]
    if set([a]).issubset(d_sample_data.columns):
        j = j + 1
print(' j = ', j)

# Індекси співпадінь
Columns_Flag_True = np.zeros((j))
j = 0
for i in range(0, n_columns):
    a = d_segment_data_description_client_bank['Field_in_data'][i]
    if set([a]).issubset(d_sample_data.columns):
        Flag = 'Flag_True'
        Columns_Flag_True[j] = i
        j = j + 1
    else:
        Flag = 'Flag_False'
print('Індекси співпадінь', Columns_Flag_True)

# Формування DataFrame даних з урахуванням відсутніх індикаторів скорингової таблиці
d_segment_data_description_client_bank_True = d_segment_data_description_client_bank.iloc[Columns_Flag_True]
d_segment_data_description_client_bank_True.index = range(0, len(d_segment_data_description_client_bank_True))
print('\nDataFrame співпадінь')
print( d_segment_data_description_client_bank_True)

# Формування сегменту вхідних даних за рейтингом кліент + банк
b = d_segment_data_description_client_bank_True['Field_in_data']
d_segment_sample_data_client_bank = d_sample_data[b]
print('\nПропуски даних сегменту DataFrame')
print(d_segment_sample_data_client_bank.isnull().sum())

# Очищення індикаторів скорингової таблиці
d_segment_data_description_cleaning = d_segment_data_description_client_bank_True.loc[
      (d_segment_data_description_client_bank_True['Field_in_data'] != 'fact_addr_start_date')]
d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
      (d_segment_data_description_cleaning['Field_in_data'] != 'position_id')]
d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
      (d_segment_data_description_cleaning['Field_in_data'] != 'employment_date')]
d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
      (d_segment_data_description_cleaning['Field_in_data'] != 'has_prior_employment')]
d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
      (d_segment_data_description_cleaning['Field_in_data'] != 'prior_employment_start_date')]
d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
      (d_segment_data_description_cleaning['Field_in_data'] != 'prior_employment_end_date')]
d_segment_data_description_cleaning = d_segment_data_description_cleaning.loc[
      (d_segment_data_description_cleaning['Field_in_data'] != 'income_frequency_other')]
d_segment_data_description_cleaning.index = range(0, len(d_segment_data_description_cleaning))
d_segment_data_description_cleaning.to_excel('d_segment_data_description_cleaning.xlsx')

# Очищення вхідних даних
d_segment_sample_cleaning = d_segment_sample_data_client_bank.drop(columns=['fact_addr_start_date', 'position_id', 'employment_date',
                                                                            'has_prior_employment', 'prior_employment_start_date',
                                                                            'prior_employment_end_date','income_frequency_other'])
d_segment_sample_cleaning.index = range(0, len(d_segment_sample_cleaning))
d_segment_sample_cleaning.to_excel('d_segment_sample_cleaning.xlsx')
print('\nКонтроль наявності пропусків даних після очищення на індикаторах')
print(d_segment_sample_cleaning.isnull().sum())
print('\nDataFrame вхідних даних - скорингова карта')
print(d_segment_sample_cleaning)
print('\nDataFrame індикатори скорингу')
print(d_segment_data_description_cleaning)