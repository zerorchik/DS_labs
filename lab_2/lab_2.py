import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import warnings
# Вимкнути DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
def stat_characteristics_in(df, mode):
    # Статистичні характеристики вибірки з урахуванням тренду
    df_zglad, coef = mnk(df, False)
    iter = len(df)
    df_1 = np.zeros((iter))
    for i in range(iter):
        df_1[i] = df[i] - df_zglad[i, 0]
    mat_spod = np.mean(df_1)
    duspers = np.var(df_1)
    ser_kvad_vid = np.sqrt(duspers)
    if mode is True:
        print('-----------------------------------------------------')
        print('Статистичні характеристики вибірки')
        print('-----------------------------------------------------')
        print('Кількість елементів вибірки =', iter)
        print('Матиматичне сподівання =', mat_spod)
        print('Дисперсія =', duspers)
        print('Середнє квадратичне відхилення =', ser_kvad_vid)
    return mat_spod, ser_kvad_vid

# Для моделі
def stat_characteristics_out (df, text):
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
    print('Статистичні характеристики', text)
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
    # plot(y, x, 'Синтезована за лінійним трендом модель', names[mode-1], names[mode-1], '(і+1)-е вересня 2023', 'Штуки')
    return y

# Функція додавання нормального шуму
def norm_shum(model, n, m, skv):
    # генерація випадкового шумуза нормальним законом
    shum = np.random.normal(m, skv, n)
    df_shum = np.zeros(n)
    for i in range(n):
        df_shum[i] = model[i] + shum[i]
    return df_shum

'''Блок аномалій'''

# Функція додавання аномалій
def av(model, num_anomalies, anomaly_mean, anomaly_std):
    # Генерація випадкових аномалій за нормальним законом
    av = np.random.normal(anomaly_mean, anomaly_std, num_anomalies)
    model_av = np.zeros(num_anomalies)
    for i in range(num_anomalies):
        model_av[i] = model[i] + av[i]
    return model_av

# Функція виявлення та усунення аномалій за алгоритмом medium
def av_medium(df, window_size, threshold):
    n = len(df)
    # Створимо копію вибірки для очищення
    df_cleaned = np.copy(df)
    for i in range(n):
        if i >= window_size:
            # Отримаємо поточне ковзне вікно
            window = df[i - window_size:i]
            # Обчислимо медіану ковзного вікна
            median = np.median(window)
            # Якщо різниця поточного значення та медіани перевищує поріг, вважаємо це аномалією
            if abs(df[i] - median) > threshold:
                # Замінюємо аномальне значення на медіану
                df_cleaned[i] = median
    return df_cleaned

# Функція виявлення найпідходящих коефіцієнтів для очищення методом МНК
def mnk_av(df):
    iter = len(df)
    df_1 = np.zeros((iter, 1))
    df_2 = np.ones((iter, 3))
    # Формування структури вхідних матриць МНК
    for i in range(iter):
        # Формування матриці вхідних даних
        df_1[i, 0] = float(df[i])
        df_2[i, 1] = float(i)
        df_2[i, 2] = float(i * i)
    df_2T = df_2.T
    df_2df_2T = df_2T.dot(df_2)
    df_2df_2TI = np.linalg.inv(df_2df_2T)
    df_2df_2TIdf_2T = df_2df_2TI.dot(df_2T)
    C = df_2df_2TIdf_2T.dot(df_1)
    return C[1, 0]

# Функція виявлення та усунення аномалій за алгоритмом МНК
def av_mnk(df, window_size, threshold):
    iter = len(df)
    j_wind = int(iter - window_size + 1)
    df_wind = np.zeros(window_size)
    # Розраховуємо коефіцієнти МНК та тренд для еталонного вікна
    speed_standart = mnk_av(df)
    df_zglad, coef = mnk(df, False)
    speed_standart_1 = abs(speed_standart * np.sqrt(iter))
    # Ковзне вікно та обробка даних
    for j in range(j_wind):
        for i in range(window_size):
            l = j + i
            df_wind[i] = df[l]
        # Виявлення аномалій
        duspers = np.var(df_wind)
        skv = np.sqrt(duspers)
        speed_1 = abs(threshold * speed_standart * np.sqrt(window_size) * skv)
        # Усунення аномалій
        if speed_1 > speed_standart_1:
            df[l] = df_zglad[l, 0]
    return df

# Функція виявлення та усунення аномалій за алгоритмом sliding window
def av_sliding_wind(df, window_size):
    iter = len(df)
    j_wind = int(np.ceil(iter - window_size) + 1)
    df_wind = np.zeros(window_size)
    midi = np.zeros(iter)
    # Ковзне вікно та обробка даних
    for j in range(j_wind):
        for i in range(window_size):
            l = (j + i)
            df_wind[i] = df[l]
        # Обчислимо медіану кожного ковзного вікна
        midi[l] = np.median(df_wind)
    # Запишемо медіану назад в df_midi
    df_midi = np.zeros(iter)
    for j in range(iter):
        df_midi[j] = midi[j]
    for j in range(window_size):
        df_midi[j] = df[j]
    return df_midi

'''Блок оптимізації параметрів усунення аномалій'''

# Функція для оптимізації параметрів window_size та threshold
def optimize(data0, data, min_window_size, max_window_size, min_threshold, max_threshold, mode):
    best_window_size = None
    best_threshold = None
    best_mae = float('inf')
    best_r2 = -float('inf')
    for window_size in range(min_window_size, max_window_size + 1):
        for threshold in np.linspace(min_threshold, max_threshold, num=100):
            if mode == 1:
                cleaned_data = av_medium(data, window_size, threshold)
            if mode == 2:
                cleaned_data = av_mnk(data, window_size, threshold)
            else:
                cleaned_data = av_sliding_wind(data, window_size)
            mae, r2 = mae_r2_score(data0, cleaned_data)
            if (mae + (1 - r2)) < (best_mae + (1 - best_r2)):
                best_window_size = window_size
                best_threshold = threshold
                best_mae = mae
                best_r2 = r2
    return best_window_size, best_threshold, best_mae, best_r2

'''Блок фільтрації'''

# Функція алгоритму -а-b фільтру
def a_b_filter(df):
    iter = len(df)
    df_1 = np.zeros((iter, 1))
    df_filtred = np.zeros((iter, 1))
    t = 1
    for i in range(iter):
        df_1[i, 0] = float(df[i])
    # Початкові дані для запуску фільтра
    df_speed_retro = (df_1[1, 0] - df_1[0, 0]) / t
    df_extra = df_1[0, 0] + df_speed_retro
    alfa = 2 * (2 * 1 - 1) / (1 * (1 + 1))
    beta = (6 / 1) * (1 + 1)
    df_filtred[0, 0] = df_1[0, 0] + alfa * (df_1[0, 0])
    # Рекурентний прохід по вимірам
    for i in range(1, iter):
        df_filtred[i, 0] = df_extra + alfa * (df_1[i, 0] - df_extra)
        df_speed = df_speed_retro + (beta / t) * (df_1[i, 0] - df_extra)
        df_speed_retro = df_speed
        df_extra = df_filtred[i, 0] + df_speed_retro
        alfa = (2 * (2 * i - 1)) / (i * (i + 1))
        beta = 6 / (i * (i + 1))
    return df_filtred

'''Блок оцінювання якості моделі'''

# Функція для обчислення коефіцієнта детермінації R^2
def mae_r2_score(actual, predicted):
    # Розрахунок MAE
    mae = np.mean(np.abs(actual - predicted))
    # Розрахунок R^2
    mean_actual = np.mean(actual)
    sst = np.sum((actual - mean_actual) ** 2)
    ssr = np.sum((actual - predicted) ** 2)
    r2 = 1 - (ssr / sst)
    return mae, r2

'''Допоміжний блок'''

# Функція для виведення часу, витраченого на очищення аномалій
def print_time(start_time):
    # Фіксуємо час, на очищення від аномалій
    total_time = (time.time() - start_time)
    print('Час виконання операцій =', total_time, 'с')

# Функція для виведення якості очищення даних від аномалій
def quality_av_detection(df_cleaned, specified_text, specified_text_1, alg, start_time, av_mode, threshold, window_size, mae, r2, df_zglad, names, data_mode, df_real_sorted, text_1, text_2, mode):
    stat_characteristics_out(df_cleaned, str(specified_text_1) + '\nочищеної від аномалій ' + str(text_2) + ' за алгоритмом ' + str(alg))
    print('-----------------------------------------------------')
    print('Якість', text_1)
    print('-----------------------------------------------------')
    if mode is False:
        print_time(start_time)
        if av_mode != 3:
            print('Поріг =', threshold)
        print('Розмір вікна =', window_size)
    print('Середньо-абсолютна помилка =', mae)
    print('Коефіцієнт детермінації =', r2)
    if mode is False:
        plot(df_zglad, df_cleaned, str(specified_text) + ' очищена від аномалій ' + str(text_2) + ' за алгоритмом ' + str(alg), 'Лінія тренду', names[data_mode - 1], '(і+1)-е вересня 2023', 'Штуки')
        plot(df_real_sorted, df_cleaned, 'Порівняння вхідних даних з очищеними від аномалій ' + str(text_2) + ' за алгоритмом ' + str(alg), 'Вхідні дані', 'Алгоритм ' + str(alg), '(і+1)-е вересня 2023', 'Штуки')
    else:
        plot(df_zglad, df_cleaned, str(specified_text) + ' після фільтрації', 'Лінія тренду', names[data_mode - 1], '(і+1)-е вересня 2023', 'Штуки')
        plot(df_real_sorted, df_cleaned, 'Порівняння вхідних даних з результатами фільтрації', 'Вхідні дані', 'Фільтрація', '(і+1)-е вересня 2023', 'Штуки')

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

# Вибір режиму отримання даних
print('Оберіть режим отримання вхідних даних:')
print('1 - Модель')
print('2 - Реальні дані')
data_var = int(input('mode:'))
# Якщо режим існує
if data_var in range(1, 3):
    # Вибір джерела вхідних даних
    print('Оберіть джерело вхідних даних:')
    for i in range(len(names)):
        print(i + 1, '-', names[i])
    data_mode = int(input('mode:'))
    # Якщо джерело даних існує
    if data_mode in range(1, len(names) + 1):
        # Зчитування та сортування вибірки
        df_real_sorted = file_parsing(url, '../lab_1/rosnia.xlsx', columns[data_mode - 1])
        # Визначення тренду та коефіцієнтів регресії
        df_zglad, coef = mnk(df_real_sorted, False)
        # Визначення характеристик вибірки
        ser, skv = stat_characteristics_in(df_real_sorted, True)
        # Якщо модель
        if (data_var == 1):
            specified_text = 'Модель'
            specified_text_1 = 'моделі'
            # Синтезація моделі
            df = model(coef[0, 0], coef[1, 0], coef[2, 0], data_mode)
            # Стохастичний шум
            df_real_sorted = norm_shum(df, len(df), ser, skv)
            # Характеристики
            stat_characteristics_out(df_real_sorted, 'моделі + шум')
            ser, skv = stat_characteristics_in(df_real_sorted, False)
            plot(df_zglad, df_real_sorted, 'Модель + нормальний шум', 'Лінія тренду', names[data_mode - 1], '(і+1)-е вересня 2023', 'Штуки')
            # Аномальні відхилення
            df_av = av(df_real_sorted, len(df_real_sorted), ser, skv)
            # Характеристики
            stat_characteristics_out(df_av, 'моделі + шум + аномалії')
            plot(df_zglad, df_av, 'Модель + нормальний шум + аномалії', 'Лінія тренду', names[data_mode - 1], '(і+1)-е вересня 2023', 'Штуки')
        # Якщо реальні дані
        else:
            specified_text = 'Вибірка'
            specified_text_1 = 'вибірки'
            plot(df_zglad, df_real_sorted, 'Кількість ' + str(vtratu[data_mode - 1]) + ' росні станом на вересень 2023', 'Лінія тренду', names[data_mode - 1], '(і+1)-е вересня 2023', 'Штуки')
            # Аномальні відхилення
            df_av = av(df_real_sorted, len(df_real_sorted), ser, skv)
            # Характеристики
            stat_characteristics_out(df_av, 'вибірки + аномалії')
            plot(df_zglad, df_av, 'Вибірка + аномалії', 'Лінія тренду', names[data_mode - 1], '(і+1)-е вересня 2023', 'Штуки')
        # Вибір алгоритму детекції та усунення аномалій
        print('-----------------------------------------------------')
        print('Оберіть алгоритм виявлення та усунення аномалій:')
        print('1 - Метод medium')
        print('2 - Метод MNK')
        print('3 - Метод sliding window')
        av_mode = int(input('mode:'))
        # Якщо алгоритм існує
        if av_mode in range(1, 4):
            min_window_size = int(len(df_av) / 6)
            max_window_size = int(len(df_av) / 2)
            # Алгоритм медіан
            if av_mode == 1:
                alg = 'medium'
                # Використання характеристик даних
                window_size = int(len(df_real_sorted) / 4)
                threshold = skv * 2
                # Фіксуємо час початку обчислень
                start_time = time.time()
                df_cleaned = av_medium(df_av, window_size, threshold)
                mae, r2 = mae_r2_score(df_real_sorted, df_cleaned)
                quality_av_detection(df_cleaned, specified_text, specified_text_1, alg, start_time, av_mode, threshold, window_size, mae, r2, df_zglad, names, data_mode, df_real_sorted, 'моделі', '', False)
                # Оптимізація
                min_threshold = skv
                max_threshold = skv * 3
                # Фіксуємо час початку обчислень
                start_time = time.time()
                window_size, threshold, mae, r2 = optimize(df_real_sorted, df_av, min_window_size, max_window_size, min_threshold, max_threshold, av_mode)
                df_cleaned = av_medium(df_av, window_size, threshold)
                quality_av_detection(df_cleaned, specified_text, specified_text_1, alg, start_time, av_mode, threshold, window_size, mae, r2, df_zglad, names, data_mode, df_real_sorted, 'оптимізації', 'та оптимізована', False)
            # Алгоритм MNK
            elif av_mode == 2:
                alg = 'MNK'
                # Використання характеристик даних
                window_size = int(len(df_real_sorted) / 4)
                threshold = skv * 50
                # Фіксуємо час початку обчислень
                start_time = time.time()
                df_cleaned = av_mnk(df_av, window_size, threshold)
                mae, r2 = mae_r2_score(df_real_sorted, df_cleaned)
                quality_av_detection(df_cleaned, specified_text, specified_text_1, alg, start_time, av_mode, threshold, window_size, mae, r2, df_zglad, names, data_mode, df_real_sorted, 'моделі', '', False)
                # Оптимізація
                min_threshold = skv * 30
                max_threshold = skv * 70
                # Фіксуємо час початку обчислень
                start_time = time.time()
                window_size, threshold, mae, r2 = optimize(df_real_sorted, df_av, min_window_size, max_window_size, min_threshold, max_threshold, av_mode)
                df_cleaned = av_mnk(df_av, window_size, threshold)
                quality_av_detection(df_cleaned, specified_text, specified_text_1, alg, start_time, av_mode, threshold, window_size, mae, r2, df_zglad, names, data_mode, df_real_sorted, 'оптимізації', 'та оптимізована', False)
            # Алгоритм ковзаючого вікна
            else:
                alg = 'sliding_wind'
                # Використання характеристик даних
                window_size = int(len(df_real_sorted) / 5)
                # Фіксуємо час початку обчислень
                start_time = time.time()
                df_cleaned = av_sliding_wind(df_av, window_size)
                mae, r2 = mae_r2_score(df_real_sorted, df_cleaned)
                threshold = 0
                quality_av_detection(df_cleaned, specified_text, specified_text_1, alg, start_time, av_mode, threshold, window_size, mae, r2, df_zglad, names, data_mode, df_real_sorted, 'моделі', '', False)
                # Оптимізація
                min_threshold = 0
                max_threshold = 0
                # Фіксуємо час початку обчислень
                start_time = time.time()
                window_size, threshold, mae, r2 = optimize(df_real_sorted, df_av, min_window_size, max_window_size, min_threshold, max_threshold, av_mode)
                df_cleaned = av_sliding_wind(df_av, window_size)
                quality_av_detection(df_cleaned, specified_text, specified_text_1, alg, start_time, av_mode, threshold, window_size, mae, r2, df_zglad, names, data_mode, df_real_sorted, 'оптимізації', 'та оптимізована', False)
            # Фільтрація
            df_filtred = a_b_filter(df_cleaned)
            mae, r2 = mae_r2_score(df_real_sorted, df_filtred)
            quality_av_detection(df_filtred, specified_text, specified_text_1, alg, 0, av_mode, 0, 0, mae, r2, df_zglad, names, data_mode, df_real_sorted, 'фільтрації', '', True)