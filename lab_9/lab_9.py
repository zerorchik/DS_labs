import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from shapely.geometry import Point
from geopy.distance import geodesic
import warnings
# Відключення попередження SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=Warning)

# Завантаження даних
def load_data(filename_universities, filename_states):
    universities = gpd.read_file(filename_universities)
    states = gpd.read_file(filename_states)

    # Переведення до EPSG:4326
    universities = universities.to_crs('EPSG:4326')
    states = states.to_crs('EPSG:4326')

    return universities, states

# Опис даатсету
def describe_enry_data(data, title):
    # Колонки
    print(data.columns)
    # Опис датасету за колонками
    for column in data.columns:
        unique_values = data[column].unique()
        print(f'\nУнікальні значення у стовпці {column}:\n{unique_values}')
    # Графік
    map_plot(data, title)

    return

# Вибір місцезнаходження користувача
def choose_location():
    user_address = input('\nУведіть Вашу адресу:')
    user_latitude, user_longitude = locate_address(user_address)

    return user_latitude, user_longitude

# Визначення координат адреси користувача
def locate_address(address):
    # Створення геолокатора
    geolocator = Nominatim(user_agent="your_app_name")
    # Геолокація за адресою
    location = geolocator.geocode(address)
    print('\nКоординати адреси користувача:')
    print(f'({location.latitude}, {location.longitude})')

    return location.latitude, location.longitude

# Визначення до якого штату належить користувач
def detect_user_state(user_longitude, user_latitude, states):
    user_location = Point(user_longitude, user_latitude)

    user_state = None
    for index, state in states.iterrows():
        if user_location.within(state['geometry']):
            user_state = state['State_Name']
            user_state_code = state['State_Code']
            break
    if user_state:
        print(f'\nВаше місцезнаходження належить штату {user_state} ({user_state_code})')
    else:
        print('\nНе вдалося визначити штат для вашого місцезнаходження')

    return

# Вибір типу навчального закладу
def choose_location_type():
    print('\nУведіть бажаний тип навчального закладу:')
    # Знаходження унікальних значень типів навчальних закладів
    types = universities_usa['NAICS_DESC'].unique()
    for i in range(len(types)):
        print(i + 1, '-', types[i])
    facility_type = int(input('type:'))
    print('\nОбраний тип закладів:')
    print(types[facility_type - 1])

    return types[facility_type - 1]

# Знаходження N найближчих закладів вищої освіти
def find_nearest_locations(data, states, num_locations=5):
    # Створення точки для місцезнаходження користувача
    user_latitude, user_longitude = choose_location()
    user_location = (user_longitude, user_latitude)
    # Визначення до якого штату належить користувач
    detect_user_state(user_longitude, user_latitude, states)

    # Визначення типу навчального закладу
    facility_type = choose_location_type()
    # Вибір закладів обраного типу
    selected_facilities = data[data['NAICS_DESC'] == facility_type]
    # Вивід кількості даних
    print(f'\nКількість навчальних закладів типу {facility_type}:')
    print(len(selected_facilities))

    # Візуалізація графіку
    filter_plot(states, selected_facilities, 'STATE', True, user_location, f'Навчальні заклади типу {facility_type}')

    # Обчислення відстаней до всіх закладів
    selected_facilities['distance'] = selected_facilities['geometry'].apply(
        lambda x: geodesic((x.y, x.x), (Point(user_location).y, Point(user_location).x)).kilometers)
    # selected_facilities['distance'] = selected_facilities['geometry'].distance(Point(user_location))

    print(f'\nВідстані до навчальних закладів типу {facility_type}')
    print(selected_facilities['distance'])

    # Сортування за відстанню та вибір перших num_locations записів
    nearest_locations = selected_facilities.sort_values(by='distance').head(num_locations)
    print(f'\nНайближчі {num_locations} навчальних закладів типу {facility_type}')
    print(nearest_locations)
    print(f'\nНазви найближчих {num_locations} навчальних закладів типу {facility_type}')
    print(nearest_locations['NAME'])

    # Візуалізація графіку
    filter_plot(states, nearest_locations, 'STATE', True, user_location, f'Найближчі до Вас навчальні заклади типу {facility_type}')

    return nearest_locations

# Вхідні графіки
def map_plot(df, title):
    # Відображення структури даних цифрової карти
    print(f'\n{title}')
    print(df.head())
    # Візуалізація вмісту одного прошарку цифрової карти
    fig, ax = plt.subplots(1, 1)
    df.plot(ax=ax)
    plt.title(title)
    plt.show()

    return

# Фільтраційні графіки
def filter_plot(states, df, column, user_detect, user_location, title):
    fig, ax = plt.subplots()
    # Відображення контурів штатів
    states.plot(ax=ax)
    # Відображення точок університетів та коледжів в межах кордону США
    df.plot(ax=ax, column=column, legend=True, markersize=5, cmap='viridis')
    if user_detect:
        # Додавання червоної точки для користувача
        ax.scatter(user_location[0], user_location[1], color='red', label='Ваше місцезнаходження')
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    legend = ax.get_legend()
    plt.show()

    return

if __name__ == '__main__':
    # Завантаження даних
    filename_universities = 'USA/Colleges_and_Universities/CollegesUniversities.shp'
    filename_states = 'USA/States_shapefile.shp'
    universities, states = load_data(filename_universities, filename_states)

    # Візуалізація вхідних даних

    # Навчальні заклади
    describe_enry_data(universities, 'Навчальні заклади США - EPSG:4326')
    # Штати
    describe_enry_data(states, 'США - EPSG:4326')

    # Фільтрація

    # Фільтрація закладів у межах США
    universities_usa = universities[universities['COUNTRY'] == 'USA']
    # Візуалізація результату фільтрації
    map_plot(universities_usa, 'Навчальні заклади в межах США на карті')
    filter_plot(states, universities_usa, 'NAICS_DESC', False, None, 'Навчальні заклади в межах США на карті')

    # Детекція найближчих
    nearest_locations = find_nearest_locations(universities_usa, states, 10)

    # Збереження результатів
    nearest_locations.to_excel('nearest_locations.xlsx', index=False)

    # 121 N LaSalle St, Chicago