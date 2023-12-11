import random
import pandas as pd

# Параметр кількості абітурієнтів
kilkist_abiturientiv = 1500

# Функція для перевірки унікальності ПІБ
def is_unique_name(pib, dataset):
    for abiturient in dataset:
        if pib == abiturient[0]:
            return False

    return True

# Функція для генерації ПІБ
def generate_name():
    first_names = ['Павло', 'Оксана', 'Дмитро', 'Ольга', 'Михайло', 'Анастасія', 'Ірина',
                   'Оксана', 'Наталія', 'Марія', 'Анна', 'Катерина', 'Вікторія', 'Олена',
                   'Тетяна', 'Людмила', 'Ярослава', 'Іванна', 'Ганна', 'Лідія', 'Ніна',
                   'Софія', 'Ірина', 'Ольга', 'Марта', 'Юлія', 'Іван', 'Олександр',
                   'Михайло', 'Андрій', 'Володимир', 'Віктор', 'Сергій', 'Петро',
                   'Дмитро', 'Олег', 'Максим', 'Роман', 'Ярослав', 'Ігор', 'Богдан',
                   'Тарас', 'Артем', 'Ілля', 'Олексій', 'Анатолій']
    last_names = ['Дмитришенко', 'Загвойко', 'Неборачко', 'Товтиш', 'Ковтун', 'Алібіба',
                  'Іваниш', 'Оксаниш', 'Наталіїш', 'Маріїш', 'Анниш', 'Катериниш',
                  'Вікторіїш', 'Олениш', 'Тетяниш', 'Людмилиш', 'Ярославиш', 'Іванниш',
                  'Ганниш', 'Лідіїш', 'Ніниш', 'Софіїш', 'Іриниш', 'Дмитришенко',
                  'Неборачко', 'Ковтун', 'Іваниш', 'Олександріш', 'Михайлиш', 'Андріїш',
                  'Володимириш', 'Вікторіш', 'Сергіїш', 'Петріш', 'Дмитріш', 'Олегіш',
                  'Максиміш', 'Романіш', 'Ярославіш', 'Ігоріш', 'Богданіш', 'Тарасіш',
                  'Артеміш', 'Ілляш', 'Олексіїш', 'Анатоліїш']

    return random.choice(first_names) + ' ' + random.choice(last_names)

# Функція для генерації датасетів
def generate_dataset(file_name):
    # Генерація датасету з 1500 абітурієнтів
    dataset = []
    for _ in range(kilkist_abiturientiv):
        pib = generate_name()
        while not is_unique_name(pib, dataset):
            pib = generate_name()
        pilga = random.choice([True, False])
        matematyka = random.randint(100, 200)
        angl_mova = random.randint(100, 200)
        ukr_mova = random.randint(100, 200)
        rating = 0.4 * matematyka + 0.3 * angl_mova + 0.3 * ukr_mova
        decision = 'незараховано'
        dataset.append([pib, pilga, matematyka, angl_mova, ukr_mova, rating, decision])

    # Створення DataFrame з датасету
    columns = ['ПІБ', 'Пільги', 'Бал з математики', 'Бал з англійської', 'Бал з української', 'Рейтинг', 'Рішення']
    df = pd.DataFrame(dataset, columns=columns)

    # Сортування за рейтингом у порядку спадання
    df.sort_values(by='Рейтинг', ascending=False, inplace=True)

    # Визначення кількість абітурієнтів з пільгами, які можуть бути зараховані
    kilkist_pilgovukiv = (df['Пільги'] == True).count()
    if kilkist_pilgovukiv > 35: kilkist_pilgovukiv = 35
    # Визначення загальної кількость абітурієнтів, які можуть бути зараховані
    if kilkist_abiturientiv >= 350:
        kilkist_zagalna = 350 - kilkist_pilgovukiv
    else:
        kilkist_zagalna = kilkist_abiturientiv - kilkist_pilgovukiv

    # Відберемо до 35 пільговиків
    pilgovyky_list = df[(df['Пільги'] == True) &
                        (df['Бал з математики'] >= 120) &
                        (df['Бал з англійської'] >= 120) &
                        (df['Бал з української'] >= 120) &
                        (df['Рейтинг'] >= 144)].head(kilkist_pilgovukiv)
    # Відберемо з загального списку тих, хто може бути зарахований як безпільговик
    general_list = df[(df['Бал з математики'] >= 140) &
                      (df['Рейтинг'] >= 160)]
    # Виключимо абітурієнтів, які вже пройшли по пільгах
    general_list = general_list[~general_list['ПІБ'].isin(pilgovyky_list['ПІБ'])]
    # Відберемо решту з загального списку, щоб у сумі було до 350 вступивших
    general_list = general_list.head(kilkist_zagalna)

    # Об'єднання двох списків
    combined_list = pd.concat([general_list, pilgovyky_list])

    # Зміна рішення для всіх абітурієнтів з комбінованого списку
    combined_list['Рішення'] = 'зараховано'

    # Створення фінального датасету з мітками
    # Виключимо абітурієнтів, які вже пройшли
    ne_proysli = df[~df['ПІБ'].isin(combined_list['ПІБ'])]
    total_list = pd.concat([combined_list, ne_proysli])
    # Видалення останнього стовпця
    df_without_last_column = total_list.iloc[:, :-1]

    # Збереження набору даних
    df_without_last_column.to_csv('dataset/{0}_dataset.csv'.format(file_name), index=False)
    df_without_last_column.to_excel('dataset/{0}_dataset.xlsx'.format(file_name), index=False, engine='openpyxl')

    # Вибір останнього стовпця
    last_column = total_list.iloc[:, -1]

    # Збереження міток
    last_column.to_csv('dataset/{0}_mark.csv'.format(file_name), index=False)
    last_column.to_excel('dataset/{0}_mark.xlsx'.format(file_name), index=False, engine='openpyxl')

    return

# Функція об'єднання датасетів у тренувальний
def concat_train_dataset():
    # Зчитування датасету
    df_1 = pd.read_csv('dataset/1_dataset.csv', header=None)
    df_2 = pd.read_csv('dataset/2_dataset.csv', header=None, skiprows=1)
    df_3 = pd.read_csv('dataset/3_dataset.csv', header=None, skiprows=1)

    # Об'єднання даних без повторення заголовків
    df_combined = pd.concat([df_1, df_2, df_3], ignore_index=True)
    # Збереження об'єднаного результату в новому CSV-файлі
    df_combined.to_csv('dataset/train_dataset.csv', index=False, header=None)
    df_combined.to_excel('dataset/train_dataset.xlsx', index=False, header=None)

    # Зчитування міток
    mark_1 = pd.read_csv('dataset/1_mark.csv', header=None)
    mark_2 = pd.read_csv('dataset/2_mark.csv', header=None, skiprows=1)
    mark_3 = pd.read_csv('dataset/3_mark.csv', header=None, skiprows=1)

    # Об'єднання міток без повторення заголовків
    mark_combined = pd.concat([mark_1, mark_2, mark_3], ignore_index=True)
    # Збереження об'єднаного результату в новому CSV-файлі
    mark_combined.to_csv('dataset/train_mark.csv', index=False, header=None)
    mark_combined.to_excel('dataset/train_mark.xlsx', index=False, header=None)

    return

# Головні виклики
descriptions = ['згенерувати тренувальний датасет', 'згенерувати тестовий датасет']

# Вибір режиму роботи програми
print('Оберіть режим роботи програми:')
for i in range(len(descriptions)):
    print(i + 1, '-', descriptions[i])
data_mode = int(input('mode:'))
# Якщо джерело даних існує
if data_mode in range(1, len(descriptions) + 1):

    # Тренувальний датасет
    if (data_mode == 1):
        for i in range(1, 4):
            generate_dataset(i)
        concat_train_dataset()

    # Тестовий датасет
    if (data_mode == 2):
        generate_dataset('test')