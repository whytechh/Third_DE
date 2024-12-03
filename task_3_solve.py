import json
import os
from collections import Counter
from bs4 import BeautifulSoup

def safe_float(value):
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

# Парсим всю дату
def parsing_files(filename):
    
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    stars = BeautifulSoup(content, 'xml')
    parsed_data = []

    for star in stars.find_all('star'):

            star_data = {
                    'name': star.find('name').get_text()
                    .strip(),

                    'constellation': star.find('constellation').get_text()
                    .strip()
                    if star.find('constellation')
                    else None,

                    'spectral-class': star.find('spectral-class').get_text()
                    .strip()
                    if star.find('spectral-class')
                    else None,
                    
                    'radius': safe_float(star.find('radius').get_text()
                    .strip())
                    if star.find('radius')
                    else None,

                    'rotation': safe_float(star.find('rotation').get_text()
                    .replace('days', '')
                    .strip())
                    if star.find('rotation')
                    else None,

                    'age': safe_float(star.find('age').get_text()
                    .replace('billion years', '')
                    .strip())
                    if star.find('age')
                    else None,

                    'distance': safe_float(star.find('distance').get_text()
                    .replace('million km', '')
                    .strip())
                    if star.find('distance')
                    else None,

                    'absolute-magnitude': safe_float(star.find('absolute-magnitude').get_text()
                    .replace('million km', '')
                    .strip())
                    if star.find('absolute-magnitude')
                    else None
        }
            parsed_data.append(star_data)

    return parsed_data

all_data = []  
    
input_folder = 'lab_3/tasks/3'

for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)
    if os.path.isfile(filepath) and filename.endswith('.xml'):
        result = parsing_files(filepath)
        all_data.extend(result)

with open('lab_3/results/3/all_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=1)

# Сортируем данные по ключу "constellation" в алфавитном порядке
sorted_data = sorted(all_data, key=lambda x: x.get('constellation', '').lower())

with open('lab_3/results/3/sorted_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=1)

# Считаем статистику для ключа "radius"
radius = [float(star_data['radius']) for star_data in all_data if 'radius' in star_data and star_data['radius'] is not None]

if radius:

    min_radius = min(radius)
    max_radius = max(radius)
    avg_radius = round(sum(radius) / len(radius), 4)

else:

    min_radius = max_radius = avg_radius = None

stat = {
    'radius': {
        'Минимальное значение': min_radius,
        'Максимальное значение': max_radius,
        'Среднее значение': avg_radius
    }
}

with open('lab_3/results/3/stat_data.json', 'w', encoding='utf-8') as f:
    json.dump(stat, f, ensure_ascii=False, indent=1)

# Находим частоту ключа "constellation"
constellation = [star_data['constellation'] for star_data in all_data if 'constellation' in star_data]

constellation_freq = Counter(constellation)

with open('lab_3/results/3/constellation_freq_data.json', 'w', encoding='utf-8') as f:
    json.dump(constellation_freq, f, ensure_ascii=False, indent=1)