import requests
from bs4 import BeautifulSoup
import re
import os

# URL веб-сторінки, яку будемо парсити
url = 'https://anitube.in.ua/anime/'
print('Обрано інформаційне джерело:', url)

def parser_url (url):
    response = requests.get(url)

    # Аналіз структури html документу
    print('Друкувати структуру HTML документу?')
    print('0 - так')
    print('1 - ні')
    data_mode = int(input('mode:'))
    soup = BeautifulSoup(response.text, 'lxml')
    if data_mode == 0:
        print(soup)

    # Вилучення із html документу списку аніме
    quotes = soup.find_all('div', class_='story_c')

    # Запис сирого списку аніме у додоатковий файл для обробки
    with open('anime_parsing_beta.txt', 'w', encoding='utf-8') as file:
        for quote in quotes:
            file.write(quote.text)

    # Запис обробленого списку аніме в файл "anime_parsing.txt"
    with open('anime_parsing.txt', 'w', encoding='utf-8') as file:
        text = text_mining('anime_parsing_beta.txt')
        file.write(text)
        print('\n----------------------------------')
        print('Список аніме:')
        print('----------------------------------')
        print(text)

    # Видалення додаткового файлу для обробки
    if os.path.exists('anime_parsing_beta.txt'):
        os.remove('anime_parsing_beta.txt')

    return

def text_mining(filename):
    # Шаблони для вилучення
    pattern_comments = r'\n*\d+ком\.'
    pattern_anime_year = r'\n\n\n\s*(?=Рік виходу аніме: \d+)'
    pattern_added = r'.*Додана.*\n\n'
    pattern_added_2 = r'.*Додані.*\n\n'
    pattern_added_3 = r'.*Перегляд.*\n\n'
    pattern_rating = r'\n*(.*/10.*)\n\n\n'
    pattern_3_space = r'\n\n\n'
    pattern_5_space = r'\n\n\n\n\n'
    pattern_2_space = r'\n\n'

    # Застосування регулярних виразів для вилучення
    with open(filename, encoding="utf-8") as file:
        text = file.read()
    text = re.sub(pattern_comments, '', text)
    text = re.sub(pattern_anime_year, '\n\n', text)
    text = re.sub(pattern_added, '', text)
    text = re.sub(pattern_added_2, '', text)
    text = re.sub(pattern_added_3, '', text)
    text = re.sub(pattern_rating, r'\n\n\1\n', text)
    text = re.sub(pattern_3_space, '\n\n', text)
    text = re.sub(pattern_5_space, '\n', text)
    text = re.sub(pattern_2_space, '\n', text)
    return text

parser_url(url)