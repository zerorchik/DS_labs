import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

'''Блок отримання вибірки'''

# Функція сортування даних
def sort(df):
    df_sorted = df.sort_values(by='date', ascending=True)
    # Скидаємо індекси та змінюємо їх на нові
    df_sorted = df_sorted.reset_index(drop=True)
    return df_sorted

# Функція парсингу реальних даних
def file_parsing (url, file, column):
    df = pd.read_excel(file)
    # Сортування
    df_sorted = sort(df)
    print('-----------------------------------------------------')
    print('Вибрірка -', column)
    print('-----------------------------------------------------')
    for name, values in df_sorted[[column]].items():
        print(values)
    df_1 = np.zeros((len(values)))
    for i in range(len(values)):
        df_1[i] = values[i]
    print('Джерело даних: ', url)
    return df_1

'''Блок лінії тренду'''

# Функція МНК згладжування для визначення лінії тренду
def mnk (df, mode):
    iter = len(df)
    var = np.zeros((iter, 1))
    val = np.ones((iter, 3))
    for i in range(iter):  # Формування структури вхідних матриць МНК
        var[i, 0] = float(df[i])  # Формування матриці вхідних даних
        val[i, 1] = float(i)
        val[i, 2] = float(i * i)
    valT = val.T
    valT_T = valT.dot(val)
    valT_TI = np.linalg.inv(valT_T)
    valT_TI_valT = valT_TI.dot(valT)
    C = valT_TI_valT.dot(var)
    df_reg = val.dot(C)
    if mode is True:
        print('-----------------------------------------------------')
        print('Регресійна модель')
        print('-----------------------------------------------------')
        print('y(t) = ', C[0, 0], ' + ', C[1, 0], ' * t', ' + ', C[2, 0], ' * t^2')
    return df_reg, C

'''Блок визначення характеристик'''

# Для вибірки
def stat_characteristics_in(df):
    # Статистичні характеристики вибірки з урахуванням тренду
    df_zglad, coef = mnk(df, False)
    iter = len(df)
    df_1 = np.zeros((iter))
    for i in range(iter):
        df_1[i] = df[i] - df_zglad[i, 0]
    mat_spod = np.mean(df_1)
    duspers = np.var(df_1)
    ser_kvad_vid = np.sqrt(duspers)
    print('-----------------------------------------------------')
    print('Статистичні характеристики вибірки')
    print('-----------------------------------------------------')
    print('Кількість елементів вибірки =', iter)
    print('Матиматичне сподівання =', mat_spod)
    print('Дисперсія =', duspers)
    print('Середнє квадратичне відхилення =', ser_kvad_vid)
    return mat_spod, ser_kvad_vid

# Для моделі
def stat_characteristics_out (df):
    # Статистичні характеристики вибірки з урахуванням тренду
    df_zglad, coef = mnk(df, False)
    iter = len(df_zglad)
    df_1 = np.zeros((iter))
    for i in range(iter):
        df_1[i] = df[i] - df_zglad[i, 0]
    mat_spod = np.mean(df_1)
    duspers = np.var(df_1)
    ser_kvad_vid = np.sqrt(duspers)
    # Глобальне лінійне відхилення оцінки - динамічна похибка моделі
    delta = 0
    for i in range(iter):
        delta = delta + abs(df[i] - df_zglad[i, 0])
    delta_average = delta / (iter + 1)
    print('-----------------------------------------------------')
    print('Статистичні характеристики моделі')
    print('-----------------------------------------------------')
    print('Кількість елементів вибірки =', iter)
    print('Матиматичне сподівання =', mat_spod)
    print('Дисперсія =', duspers)
    print('Середнє квадратичне відхилення =', ser_kvad_vid)
    print('Динамічна похибка моделі =', delta_average)

'''Блок моделі'''

def model(a, b, c, mode):
    # Генерування часової послідовності (змінної x)
    x = np.linspace(0, 21, 21)  # Від 0 до 21 з 21 рівномірно розподіленим значенням
    # Розрахунок значень моделі
    y = a + b*x + c*x*x
    plot(y, x, 'Синтезована за лінійним трендом модель', names[mode-1], names[mode-1], '(і+1)-е вересня 2023', 'Штуки')
    return y

# Функція додавання нормального шуму
def norm_shum (model, n, m, skv):
    shum = np.random.normal(m, skv, n)
    df_shum = np.zeros((n))
    for i in range(n):
        df_shum[i] = model[i] + shum[i]
    return df_shum

'''Блок оцінювання якості моделі'''

# Функція для обчислення коефіцієнта детермінації R^2
def r2_score(actual, predicted):
    # Обчислення середнього значення реальних даних
    mean_actual = np.mean(actual)
    # Сума квадратів відхилень реальних даних від їх середнього
    sst = np.sum((actual - mean_actual) ** 2)
    # Сума квадратів помилок (відхилень) моделі
    ssr = np.sum((actual - predicted) ** 2)
    # Обчислення коефіцієнта детермінації R^2
    r2 = 1 - (ssr / sst)
    print('-----------------------------------------------------')
    print('Якість моделі')
    print('-----------------------------------------------------')
    print('Кількість елементів вибірки =', len(predicted))
    print('Коефіцієнт детермінації (ймовірність апроксимації) =', r2)
    return r2

'''Допоміжний блок'''

# Функція для виведення графіку
def plot(df, df_1, title, label, label_1, xlabel, ylabel):
    plt.figure(figsize=(8, 6))
    if label != label_1:
        plt.plot(df_1, label=label_1)
    plt.plot(df, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.title(title)
    plt.show()

'''Основний блок'''

# URL веб-сторінки, з якої отримано реальні дані
url = "https://www.minusrus.com/"

columns = ['personnel', 'armed_vehicles', 'tanks', 'artilleries', 'aircrafts', 'helicopters', 'ships']
names = ['Особовий склад', 'Бойові броньовані машини', 'Танки', 'Артилерія', 'Літаки', 'Гелікоптери', 'Кораблі']
vtratu = ['дохлої', 'знищених броньованих машин', 'знищених танків', 'знищеної артилерії', 'збитих літаків', 'збитих гелікоптерів', 'потоплених кораблів']

# Вибір режиму зчитування даних
print('Оберіть джерело вхідних даних та подальші дії:')
for i in range(len(names)):
    print(i + 1, '-', names[i])
data_mode = int(input('mode:'))
# Якщо джерело даних існує
if data_mode in range(1, len(names) + 1):
    # Зчитування та сортування вибірки
    df_real_sorted = file_parsing(url, 'rosnia.xlsx', columns[data_mode - 1])
    # Визначення тренду
    df_zglad, coef = mnk(df_real_sorted, True)
    plot(df_zglad, df_real_sorted, 'Кількість ' + str(vtratu[data_mode - 1]) + ' росні станом на вересень 2023', 'Лінія тренду', names[data_mode - 1], '(і+1)-е вересня 2023', 'Штуки')
    # Визначення характеристик вибірки
    ser, skv = stat_characteristics_in(df_real_sorted)
    # Синтезація моделі
    model = model(coef[0, 0], coef[1, 0], coef[2, 0], data_mode)
    # Додавання стохастичного шуму
    model_shum = norm_shum(model, len(model), ser, skv)
    plot(model_shum, model_shum, 'Модель + нормальний шум', names[data_mode - 1], names[data_mode - 1], '(і+1)-е вересня 2023', 'Штуки')
    # Визначення характеристик моделі
    stat_characteristics_out(model_shum)
    # Оцінювання якості моделі
    r2_score(df_real_sorted, model_shum)
    plot(model_shum, df_real_sorted, 'Відповідність моделі реальним даним', 'Модель', names[data_mode-1], '(і+1)-е вересня 2023', 'Штуки')