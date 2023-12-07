import re
import pandas as pd

data = """24.09.2023
Танки — 4662 (+7)
ББМ — 8914 (+2)
Гармати — 6233 (+23)
РСЗВ — 789
Засоби ППО — 531 (+1)
Літаки — 315
Гелікоптери — 316
БПЛА — 4888 (+21)
Крилаті ракети — 1518
Кораблі (катери) — 20
Підводні човни — 1
Автомобілі та автоцистерни — 8734 (+18)
Спеціальна техніка — 914 (+2)
Особовий склад — близько 275850 осіб (+390)"""

# Розділити рядок на рядки
lines = data.split('\n')

# Ініціалізувати порожній масив для збереження чисел
numbers = []
# Створюємо словник для збереження результатів
result_list = {'date': [], 'personnel': [], 'armed_vehicles': [], 'tanks': [], 'artilleries': [], 'aircrafts': [], 'helicopters': [], 'ships': []}

# Обробити перший рядок окремо
first_line = lines[0]
# Розділити рядок на числа та додати їх до масиву
numbers.extend(map(str, first_line.split()))

# Перебирати решту рядків, починаючи з другого
for line in lines[1:]:
    # Видаляти числа в дужках з рядка та залишати лише числа поза дужками
    stripped_line = re.sub(r'\(\+\d+\)', '', line)
    # Вилучити всі символи, окрім цифр та крапок
    cleaned_line = re.sub(r'[^\d.]', ' ', stripped_line)
    # Розділити рядок на числа та додати їх до масиву
    numbers.extend(map(int, cleaned_line.split()))

# Додати числа до списку згідно з вказаним порядком
result_list['date'].append(numbers[0])
result_list['personnel'].append(numbers[14])
result_list['armed_vehicles'].append(numbers[2])
result_list['tanks'].append(numbers[1])
result_list['artilleries'].append(numbers[3])
result_list['aircrafts'].append(numbers[6])
result_list['helicopters'].append(numbers[7])
result_list['ships'].append(numbers[10])

# Перетворюємо словник в DataFrame
new_df = pd.DataFrame(result_list)

# Вивести результат
print(new_df)

# Читаємо існуючу таблицю з файлу, якщо вона існує
try:
    existing_df = pd.read_excel("rosnia_1.xlsx")
except FileNotFoundError:
    existing_df = None

# Перевіряємо, чи є існуюча таблиця
if existing_df is not None:
    # Дописуємо нові дані до існуючої таблиці
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
else:
    updated_df = new_df

# Зберігаємо оновлену таблицю
updated_df.to_excel("rosnia_1.xlsx", index=False)