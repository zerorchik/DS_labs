import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math as mt
import warnings
# Вимкнути DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

#-------------------- ЕТАП І ЛІНІЙНИЙ АНАЛІЗ ------------------------------

# Розділення вхідного масиву на кластери за жанрами
def split_anime_by_genre(dataframe, unique_genres):
    genre_clusters = {genre: dataframe[dataframe['genre'].str.contains(genre, na=False, case=False)] for genre in unique_genres if not pd.isna(genre)}
    return genre_clusters

# Графік розділеного масиву на кластери за жанрами
def plot_average_profit(genre_clusters, profit, num_highest=3, num_lowest=3):
    average_profits = {genre: data[profit].mean() for genre, data in genre_clusters.items()}

    genres = list(average_profits.keys())
    profits = list(average_profits.values())

    # Знайти найбільші і найменші значення
    max_profits_indices = np.argsort(profits)[-num_highest:]
    min_profits_indices = np.argsort(profits)[:num_lowest]

    # Створити список кольорів для підписів осі x
    label_colors = ['green' if i in max_profits_indices else 'red' if i in min_profits_indices else 'black' for i in range(len(profits))]

    # Створити список кольорів для стовпчиків
    bar_colors = [
        'skyblue' if i not in max_profits_indices and i not in min_profits_indices else 'green' if i in max_profits_indices else 'red'
        for i in range(len(profits))]

    # Вивести стовпчасту діаграму зі спеціальними кольорами
    plt.bar(genres, profits, color=bar_colors)
    plt.xlabel('Genre')

    # Встановити колір підписів на осі x
    for tick_label, color in zip(plt.gca().get_xticklabels(), label_colors):
        plt.setp(tick_label, color=color)

    plt.xticks(rotation=45, ha='right')
    plt.ylabel(f'Average {profit}')
    plt.title(f'Average {profit} by Genre')
    plt.show()

# Результати показників ефективності
def profit_results(df, unique_genres, profit):
    print(f'\nПоказник ефективності - {profit.capitalize()}')
    print(df[profit])
    print(type(float(df[profit][0])))
    # Графік загального представлення
    plt.title(profit.capitalize())
    df[profit].plot()
    plt.show()
    # Графік представлення за жанрами
    genre_clusters = split_anime_by_genre(df, list(unique_genres))
    plot_average_profit(genre_clusters, profit, num_highest=5, num_lowest=5)

    return genre_clusters

# 1. Парсинг файлу  -----------------------------

# Вхідні дані

df = pd.read_csv('anime.csv')
print('\nВхідні дані')
print(df)
df.to_excel('anime.xlsx', index=False)

# 2. Попередній аналіз даних  -----------------------------

# Очистка рядків із значеннями NaN у стовпці 'rating'
df = df.dropna(subset=['rating']).reset_index(drop=True)
# Очистка рядків із значеннями NaN у стовпці 'members'
df = df.dropna(subset=['members']).reset_index(drop=True)

# Представлені жанри

# Розділення рядків, що містять кілька жанрів
genres_series = df['genre'].str.split(',').explode()
# Вилучення унікальних значень жанрів з виправленням пробілів
unique_genres = genres_series.str.strip().unique()
# Виведення масиву унікальних значень жанрів
print('\nЖанри')
print(unique_genres)
print(len(unique_genres))

# 4. Лінійний аналіз даних  -----------------------------

# Рейтинг
profit = 'rating'
# Виведення результатів
genre_clusters_rating = profit_results(df, unique_genres, profit)

# Фан база
profit = 'members'
# Виведення результатів
genre_clusters_members = profit_results(df, unique_genres, profit)

# Об'єднаний показник ефективності
profit = 'combined score'
# Маштабування значень фан бази від 0 до 10
min_members = df['members'].min()
max_members = df['members'].max()
df['scaled_members'] = ((df['members'] - min_members) / (max_members - min_members)) * 10
print(f'\nМаштабований показний ефективності - Members [0, 10]')
print(df['scaled_members'])
print(type(float(df['scaled_members'][0])))
# Додавання стовпця зі змішаним показником
df[profit] = (df['rating'] + df['scaled_members']) / 2
# Виведення результатів
genre_clusters_combined = profit_results(df, unique_genres, profit)

#-------------------- ЕТАП ІІ СТАТИСТИЧНИЙ АНАЛІЗ --------------------------

# Функція МНК згладжування для визначення лінії тренду
def mnk(df):
    iter = len(df)
    df_1 = np.zeros((iter, 1))
    df_2 = np.ones((iter, 5))
    for i in range(iter):
        df_1[i, 0] = df[i]
        # df_1[i, 0] = df.iloc[i]
        df_2[i, 1] = float(i)
        df_2[i, 2] = float(i * i)
        df_2[i, 3] = float(i * i * i)
        df_2[i, 4] = float(i * i * i * i)
    df_2T = df_2.T
    df_2_df_2T = df_2T.dot(df_2)
    df_2_df_2TI = np.linalg.inv(df_2_df_2T)
    df_2_df_2TI_df_2T = df_2_df_2TI.dot(df_2T)
    C = df_2_df_2TI_df_2T.dot(df_1)
    df_rez = df_2.dot(C)

    return df_rez

def mnk_dict(genre_clusters, profit):
    data = {genre: data[profit].mean() for genre, data in genre_clusters.items()}

    # Створюємо датафрейм
    df = pd.DataFrame(list(data.items()), columns=['Genre', 'AverageProfit'])

    # Визначаємо МНК
    X = np.arange(len(df))
    y = df['AverageProfit'].values
    coefficients = np.polyfit(X, y, deg=1)
    trend_line = np.polyval(coefficients, X)

    # Отримуємо масив значень AverageRating у форматі trend_line
    df_2 = np.interp(np.arange(len(trend_line)), np.arange(len(df)), df['AverageProfit'])

    return df_2, trend_line

# Розрахунок статистичних характеристик вибірки
def stat_characteristics(df, text):
    # Статистичні характеристики вибірки з урахуванням тренду
    df_zglad = mnk_stat_characteristics(df)
    iter = len(df_zglad)
    df_1 = np.zeros((iter))
    for i in range(iter):
        df_1[i] = df[i] - df_zglad[i, 0]
    mat_spod = np.median(df_1)
    duspers = np.var(df_1)
    ser_kvad_vid = mt.sqrt(duspers)
    print('\n-----------------------------------------------------')
    print(text)
    print('-----------------------------------------------------')
    print('Матиматичне сподівання =', mat_spod)
    print('Дисперсія =', duspers)
    print('Середнє квадратичне відхилення =', ser_kvad_vid)
    # Графік МНК вибірки
    plt.title(text)
    plt.hist(df, bins=30, range=(df.min(), df.max()), facecolor="blue", alpha=0.5)
    plt.show()

    return

# МНК згладжуваннядля визначення статистичних характеристик
def mnk_stat_characteristics(df):
    iter = len(df)
    df_1 = np.zeros((iter, 1))
    df_2 = np.ones((iter, 4))
    # Формування структури вхідних матриць МНК
    for i in range(iter):
        # Формування матриці вхідних даних
        df_1[i, 0] = float(df[i])
        df_2[i, 1] = float(i)
        df_2[i, 2] = float(i * i)
        df_2[i, 3] = float(i * i * i)
    df_2T = df_2.T
    df_2_df_2T = df_2T.dot(df_2)
    df_2_df_2TI = np.linalg.inv(df_2_df_2T)
    df_2_df_2TI_df_2T = df_2_df_2TI.dot(df_2T)
    C = df_2_df_2TI_df_2T.dot(df_1)
    df_rez = df_2.dot(C)

    return df_rez

# Графік МНК для розділеного масиву на кластери за жанрами
def plot_mnk_by_genre(mnk_genre_zglad, genre_clusters, profit, num_highest=3, num_lowest=3):
    average_profits = {genre: data[profit].mean() for genre, data in genre_clusters.items()}

    genres = list(average_profits.keys())
    profits = list(average_profits.values())

    # Знайти найбільші і найменші значення
    max_profits_indices = np.argsort(profits)[-num_highest:]
    min_profits_indices = np.argsort(profits)[:num_lowest]

    # Створити список кольорів для підписів осі x
    label_colors = ['green' if i in max_profits_indices else 'red' if i in min_profits_indices else 'black' for i in range(len(profits))]

    # Створити список кольорів для стовпчиків
    bar_colors = [
        'skyblue' if i not in max_profits_indices and i not in min_profits_indices else 'green' if i in max_profits_indices else 'red'
        for i in range(len(profits))]

    # Вивести стовпчасту діаграму зі спеціальними кольорами
    plt.bar(genres, profits, color=bar_colors)
    plt.plot(genres, mnk_genre_zglad)
    plt.plot(genres, mnk_genre_zglad)
    plt.xlabel('Genre')

    # Встановити колір підписів на осі x
    for tick_label, color in zip(plt.gca().get_xticklabels(), label_colors):
        plt.setp(tick_label, color=color)

    plt.xticks(rotation=45, ha='right')
    plt.ylabel(f'Average {profit}')
    plt.title(f'MNK by Genre - {profit.capitalize()}')
    plt.show()

# Знаходження тренду вибірки за показником ефективності
def mnk_zglad(profit, df, mnk_profit):
    stat_characteristics(df[profit], f'Statistical characteristics - {profit.capitalize()}')
    stat_characteristics(mnk_profit, f'Statistical characteristics MNK - {profit.capitalize()}')
    # Графік
    plt.title(f'MNK - {profit.capitalize()}')
    plt.plot(df[profit])
    plt.plot(mnk_profit)
    plt.show()

def mnk_zglad_dict(genre_clusters, profit):
    df_2, mnk_genre_zglad = mnk_dict(genre_clusters, profit)
    # Графік
    stat_characteristics(df_2, f'Statistical characteristics by Genre - {profit.capitalize()}')
    stat_characteristics(mnk_genre_zglad, f'Statistical characteristics MNK by Genre - {profit.capitalize()}')
    plot_mnk_by_genre(mnk_genre_zglad, genre_clusters, profit, num_highest=5, num_lowest=5)

# Результати МНК згладжування
def mnk_results(profit, df):
    # Графік загального представлення
    mnk_profit = mnk(df[profit])
    mnk_zglad(profit, df, mnk_profit)
    # Графік представлення за жанрами
    genre_clusters = split_anime_by_genre(df, list(unique_genres))
    mnk_zglad_dict(genre_clusters, profit)

# 5. Статистичний аналіз даних  -----------------------------

# МНК оцінка

# Рейтинг
profit = 'rating'
mnk_results(profit, df)

# Фан база
profit = 'members'
mnk_results(profit, df)

# Об'єднаний показник ефективності
profit = 'combined score'
mnk_results(profit, df)