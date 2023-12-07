import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# Відповіді HTTP-сервера:

# 200: запит виконано успішно.
# 400: запит не сформовано належним чином.
# 401: несанкціонований запит, клієнт повинен надіслати дані автентифікації.
# 404: вказаний у запиті ресурс не знайдено.
# 500: внутрішня помилка сервера HTTP.
# 501: запит не реалізований сервером HTTP.
# 502: служба не доступна.

# URL веб-сторінки, яку будемо парсити
url = "https://www.minusrus.com/"

# Очищення значень
def clean_number(raw_number):
    cleaned_number = ''.join(filter(lambda char: char.isdigit(), raw_number))
    return int(cleaned_number)

def parsing_site (url):
    # Відправляємо GET-запит на веб-сторінку
    response = requests.get(url)
    # Створюємо словник для збереження результатів
    result_list = {'date': [], 'personnel': [], 'armed_vehicles': [], 'tanks': [], 'artilleries': [], 'aircrafts': [], 'helicopters': [], 'ships': []}
    print('-------------------------------------')
    print('Статус код: ' + str(response.status_code))
    print('-------------------------------------')
    print('HTML сторінка:\n\n' + response.text)
    # Перевіряємо, чи успішно отримали сторінку
    if response.status_code == 200:
        soup = bs(response.text, "html.parser")
        dates = soup.find_all('span', class_="date__label")
        personnel = soup.find_all('span', class_="card__amount-total")[0]
        armed_vehicles = soup.find_all('span', class_="card__amount-total")[1]
        tanks = soup.find_all('span', class_="card__amount-total")[2]
        artilleries = soup.find_all('span', class_="card__amount-total")[3]
        aircrafts = soup.find_all('span', class_="card__amount-total")[4]
        helicopters = soup.find_all('span', class_="card__amount-total")[5]
        ships = soup.find_all('span', class_="card__amount-total")[6]
        # Вносимо дані в список
        for date in dates:
            result_list['date'].append(date.text)
        for person in personnel:
            result_list['personnel'].append(clean_number(person.text))
        for a_v in armed_vehicles:
            result_list['armed_vehicles'].append(int(a_v.text))
        for tank in tanks:
            result_list['tanks'].append(int(tank.text))
        for artillery in artilleries:
            result_list['artilleries'].append(int(artillery.text))
        for aircraft in aircrafts:
            result_list['aircrafts'].append(int(aircraft.text))
        for helicopter in helicopters:
            result_list['helicopters'].append(int(helicopter.text))
        for ship in ships:
            result_list['ships'].append(int(ship.text))
    # Виводимо результати парсингу
    print('-------------------------------------')
    print('Результат париснгу:')
    print('-------------------------------------')
    print(result_list['date'])
    print(result_list['personnel'])
    print(result_list['armed_vehicles'])
    print(result_list['tanks'])
    print(result_list['artilleries'])
    print(result_list['aircrafts'])
    print(result_list['helicopters'])
    print(result_list['ships'])
    return result_list

# Читаємо існуючу таблицю з файлу, якщо вона існує
try:
    existing_df = pd.read_excel("rosnia_new.xlsx")
except FileNotFoundError:
    existing_df = None

# Перетворюємо результати парсингу в DataFrame
new_df = pd.DataFrame(data=parsing_site(url))

# Перевіряємо, чи є існуюча таблиця
if existing_df is not None:
    # Дописуємо нові дані до існуючої таблиці
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
else:
    updated_df = new_df

# Зберігаємо оновлену таблицю
updated_df.to_excel("rosnia_new.xlsx", index=False)