import re
import json
import os
from collections import Counter
from bs4 import BeautifulSoup

# Парсинг всех данных в общий файл
def parsing_files(filename):

    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    item = {}
    soup = BeautifulSoup(content, 'html.parser')

    item['Тип'] = soup.find('span', string=lambda t: t and "Тип:" in t).text.split(':')[-1].strip()

    title = soup.find('h1', class_='title')
    item['Турнир'] = title.text.replace('Турнир:', '').strip()

    city_and_date = soup.find('p', class_='address-p')
    city_and_time_text = city_and_date.get_text()
    city = city_and_time_text.split('Город:')[1].split('Начало:')[0].strip()
    date = city_and_time_text.split('Начало:')[1].strip()
    item['Город'] = city
    item['Начало'] = date

    tour_count = soup.find('span', class_='count')
    item['Количество туров'] = tour_count.text.replace('Количество туров:', '').strip()

    time_control = soup.find('span', class_='year')
    item['Контроль времени'] = time_control.text.replace('Контроль времени:', '').strip()

    all_spans = soup.find_all('span')

    item['Минимальный рейтинг для участия'] = all_spans[3].text.replace('Минимальный рейтинг для участия:', '').strip()

    item['Ссылка на изображение'] = soup.find('img')['src']

    item['Рейтинг'] = all_spans[4].text.replace('Рейтинг:', '').strip()

    item['Просмотры'] = all_spans[5].text.replace('Просмотры:', '').strip()

    return item

input_folder = 'lab_3/tasks/1'

all_items = []

for filename in os.listdir(input_folder):
    # Полный путь к файлу
    filepath = os.path.join(input_folder, filename)

    # Проверяем, что это файл и имеет расширение .html
    if os.path.isfile(filepath) and filename.endswith('.html'):
        # Обработка файла и добавление результата в общий список
        result = parsing_files(filepath)
        all_items.append(result)

with open('lab_3/results/1/all_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_items, f, ensure_ascii=False, indent=1)

# Сортируем данные по ключу "Город" в алфавитном порядке
sorted_items = sorted(all_items, key=lambda x: x.get('Город', '').lower())

with open('lab_3/results/1/sorted_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_items, f, ensure_ascii=False, indent=1)

# Находим частоту ключа "Город"
cities = [item['Город'] for item in all_items if 'Город' in item]

city_freq = Counter(cities)

with open('lab_3/results/1/cities_freq_data.json', 'w', encoding='utf-8') as f:
    json.dump(city_freq, f, ensure_ascii=False, indent=1)

# Считаем статистику для ключа "Контроль времени"
def remove_letters(text):
    return re.sub(r'[a-zA-Zа-яА-ЯёЁ]', '', text)

for item in all_items:
    if 'Контроль времени' in item:
        item['Контроль времени'] = remove_letters(item['Контроль времени'])

time_control = [int(item['Контроль времени']) for item in all_items if 'Контроль времени' in item]

if time_control:

    min_time = min(time_control)
    max_time = max(time_control)
    avg_time = round(sum(time_control) / len(time_control), 4)

else:

    min_time = max_time = avg_time = None

stat = {
    'Контроль времени': {
        'Минимальное значение': min_time,
        'Максимальное значение': max_time,
        'Среднее значение': avg_time
    }
}

with open('lab_3/results/1/stat_data.json', 'w', encoding='utf-8') as f:
    json.dump(stat, f, ensure_ascii=False, indent=1)