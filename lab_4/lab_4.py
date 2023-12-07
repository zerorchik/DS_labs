import speech_recognition as sr

# Створення екземпляру класу Recognizer
recognizer = sr.Recognizer()

# Запис голосового повідомлення
def capture_voice_input():
    with sr.Microphone() as source:
        print('Говоріть...')
        audio = recognizer.listen(source)
    return audio

# Перетворення голосового повідомлення на текст
def convert_voice_to_text(audio):
    try:
        text = recognizer.recognize_google(audio, language='uk-UA')
        print('\n')
        print('-' * 50)
        print('|\tYou: ' + text)
        print('-' * 50)
    except sr.UnknownValueError:
        text = ''
        print('Anime Helper: Вибачте, я Вас не розумію.')
    except sr.RequestError as e:
        text = ''
        print('Anime Helper: Error; {0}'.format(e))
    return text

# Заданий перелік слів
hello_words = ['привіт', 'вітаю', 'добрий день', 'доброго дня', 'доброго ранку', 'добрий ранок', 'добрий вечір', 'доброго вечора', 'підкажи', 'підкажіть']
dub_words = ['дубляж', 'озвучка', 'дубляжем', 'озвучкою']
seasons_words = ['довге', 'сезонів']
new_words = ['нове', 'новинки', 'свіже', 'свіжі', 'цього року']
genre_words = ['жанру', 'жанрі', 'жанр']
bye_words = ['до побачення', 'бувай', 'дякую', 'на все добре']


# Обробка голосових команд
def process_voice_command(text):
    # Якщо 'вітаю'
    if any(word in text.lower() for word in hello_words):
        print('Anime Helper: Привіт! Чим я можу допомогти?')
    # Якщо 'дубляж'
    elif any(word in text.lower() for word in dub_words):
        print('Anime Helper: Якщо Ви шукаєте аніме з дубляжем, ось деякі мої рекомендації')
        print('')
        print('АНІМЕ З ДУБЛЯЖЕМ:')
        print('')
        with open('anime_parsing.txt', 'r', encoding='utf-8') as file:
            # Розділяємо текст на абзаци за двома новими рядками
            paragraphs = file.read().split('\n\n')
            for paragraph in paragraphs:
                if 'DUB' in paragraph or 'D+' in paragraph:
                    print(paragraph)
                    # Додаємо розділювач для читабельності
                    print('-' * 50)
    # Якщо 'довге'
    elif any(word in text.lower() for word in seasons_words):
        print('Anime Helper: Якщо Ви хочете подивитись аніме, що має декілька сезонів, ось приклад аніме, що може Вам сподобатись')
        print('')
        print('АНІМЕ НА ДЕКІЛЬКА СЕЗОНІВ:')
        print('')
        with open('anime_parsing.txt', 'r', encoding='utf-8') as file:
            # Розділяємо текст на абзаци за двома новими рядками
            paragraphs = file.read().split('\n\n')
            for paragraph in paragraphs:
                if 'сезон' in paragraph:
                    print(paragraph)
                    # Додаємо розділювач для читабельності
                    print('-' * 50)
    # Якщо 'новинка'
    elif any(word in text.lower() for word in new_words):
        print('Anime Helper: Якщо Ви хочете подивитись аніме-новинки, ось деякі популярні')
        print('')
        print('АНІМЕ 2023 РОКУ:')
        print('')
        with open('anime_parsing.txt', 'r', encoding='utf-8') as file:
            # Розділяємо текст на абзаци за двома новими рядками
            paragraphs = file.read().split('\n\n')
            for paragraph in paragraphs:
                if '2023' in paragraph:
                    print(paragraph)
                    # Додаємо розділювач для читабельності
                    print('-' * 50)
    # Якщо 'жанр'
    elif any(word in text.lower() for word in genre_words):
        # Розділяємо живу мову на слова
        words = text.split()
        # Визначаємо жанр
        for i, word in enumerate(words):
            if any(word in word.lower() for word in genre_words):
                if i < len(words) - 1:
                    genre_value = words[i + 1].lower()
        print('Anime Helper: Якщо Ви хочете подивитись аніме в жанрі', genre_value, ', ось деякі рекомендації')
        print('')
        print('АНІМЕ В ЖАНРІ', genre_value.upper(), ':')
        print('')
        with open('anime_parsing.txt', 'r', encoding='utf-8') as file:
            # Розділяємо текст на абзаци за двома новими рядками
            paragraphs = file.read().split('\n\n')
            for paragraph in paragraphs:
                if genre_value in paragraph.lower():
                    print(paragraph)
                    # Додаємо розділювач для читабельності
                    print('-' * 50)
    # Якщо 'бувай'
    elif any(word in text.lower() for word in bye_words):
        print('Anime Helper: До побачення! Гарного дня!')
        return True
    else:
        print('Anime Helper: Мені потрібно більше подробиць, щоб дати якісну пораду з вибору аніме. Опиши будь ласка детальніше, що ти шукаєш?')
    return False

# Головні виклики
def main():
    end_program = False
    while not end_program:
        audio = capture_voice_input()
        text = convert_voice_to_text(audio)
        end_program = process_voice_command(text)

if __name__ == '__main__':
    main()