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

    clothings = BeautifulSoup(content, 'xml')
    parsed_data = []

    for item in clothings.find_all('clothing'):

            clothings_data = {

                    'id': item.find('id').get_text()
                    .strip()
                    if item.find('id')
                    else None,
                    
                    'name': item.find('name').get_text()
                    .strip()
                    if item.find('name')
                    else None,

                    'category': item.find('category').get_text()
                    .strip()
                    if item.find('category')
                    else None,

                    'size': item.find('size').get_text()
                    .strip()
                    if item.find('size')
                    else None,
                    
                    'color': item.find('color').get_text()
                    .strip()
                    if item.find('color')
                    else None,

                    'material': item.find('material').get_text()
                    .strip()
                    if item.find('material')
                    else None,

                    'price': item.find('price').get_text()
                    .replace('billion years', '')
                    .strip()
                    if item.find('price')
                    else None,

                    'rating': item.find('rating').get_text()
                    .replace('million km', '')
                    .strip()
                    if item.find('rating')
                    else None,

                    'exclusive': item.find('exclusive').get_text()
                    .strip()
                    if item.find('exclusive')
                    else 'no',

                    'reviews': item.find('reviews').get_text()
                    .strip()
                    if item.find('reviews')
                    else None,

                    'sporty': item.find('sporty').get_text()
                    .strip()
                    if item.find('sporty')
                    else 'no',

                    'new': item.find('new').get_text()
                    .strip()
                    if item.find('new')
                    else '-'
        }
            parsed_data.append(clothings_data)

    return parsed_data

all_data = []  
    
input_folder = 'lab_3/tasks/4'

for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)
    if os.path.isfile(filepath) and filename.endswith('.xml'):
        result = parsing_files(filepath)
        all_data.extend(result)

with open('lab_3/results/4/all_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=1)

# Сортируем данные по ключу "name" в алфавитном порядке
sorted_data = sorted(all_data, key=lambda x: x.get('name', '').lower())

with open('lab_3/results/4/sorted_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=1)

# Считаем статистику для ключа "price"
price = [float(clothings_data['price']) for clothings_data in all_data if 'price' in clothings_data and clothings_data['price'] is not None]

if price:

    min_price = min(price)
    max_price = max(price)
    avg_price = round(sum(price) / len(price), 4)

else:

    min_price = max_price = avg_price = None

stat = {
    'price': {
        'Минимальное значение': min_price,
        'Максимальное значение': max_price,
        'Среднее значение': avg_price
    }
}

with open('lab_3/results/4/stat_data.json', 'w', encoding='utf-8') as f:
    json.dump(stat, f, ensure_ascii=False, indent=1)

# Находим частоту ключа "size"
size = [clothings_data['size'] for clothings_data in all_data if 'size' in clothings_data]

size_freq = Counter(size)

with open('lab_3/results/4/size_freq_data.json', 'w', encoding='utf-8') as f:
    json.dump(size_freq, f, ensure_ascii=False, indent=1)