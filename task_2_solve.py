import re
import json
import os
from collections import Counter
from bs4 import BeautifulSoup

input_folder = 'lab_3/tasks/2'

def get_li_value(li_tags, li_type):
        for li in li_tags:
            if li.get('type') == li_type:
                return li.get_text().strip()
        return None

# Парсинг всех данных в общий файл
def parsing_files(filename):
    
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    pads = soup.find_all('div', class_='product-item')

    for pad in pads:

        item = {}

        item['id'] = pad.find('a', class_='add-to-favorite')['data-id']

        links = pad.find_all('a')
        item['link'] = links[1]['href'] if len(links) > 1 else None

        img_tag = pad.find('img')
        item['img'] = img_tag['src'] if img_tag else None

        title = pad.find('span')
        item['title'] = (re.sub(r'\\', '',
                        title.get_text()
                        .strip() if title else None))

        price = pad.find('price')
        item['price'] = (price.get_text()
                        .replace('₽', '')
                        .replace(' ', '')
                        .strip() 
                        if price 
                        else None)

        bonus = pad.find('strong')
        item['bonus'] = (bonus.get_text()
                        .replace('+ начислим', '')
                        .replace('бонусов', '')
                        .strip()
                        if bonus 
                        else None)

        ul = pad.find('ul')
        if ul:

            li_tags = ul.find_all('li')

            item['processor'] = (get_li_value(li_tags, 'processor')
                                    .strip()
                                    if get_li_value(li_tags, 'processor') else None)

            item['ram'] = (get_li_value(li_tags, 'ram')
                                    .replace('GB', '')
                                    .strip()
                                    if get_li_value(li_tags, 'ram') else None)

            item['sim'] = (get_li_value(li_tags, 'sim')
                                    .replace('SIM', '')
                                    .strip()
                                    if get_li_value(li_tags, 'sim') else None)
            
            item['resolution'] = (get_li_value(li_tags, 'resolution')
                                    .strip()
                                    if get_li_value(li_tags, 'resolution') else None)
            
            item['camera'] = (get_li_value(li_tags, 'camera')
                                    .replace('MP', '')
                                    .strip()
                                    if get_li_value(li_tags, 'camera') else None)
            

            item['matrix'] = (get_li_value(li_tags, 'matrix')
                            .strip()
                            if get_li_value(li_tags, 'matrix') else None)

            item['battery'] = (get_li_value(li_tags, 'acc')
                                    .replace('мА * ч', '')
                                    .strip()
                                    if get_li_value(li_tags, 'acc') else None)
            
            return item
    
all_items = []

for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)
    if os.path.isfile(filepath) and filename.endswith('.html'):
        result = parsing_files(filepath)
        all_items.append(result)

with open('lab_3/results/2/all_data.json', 'w', encoding='utf-8') as outfile:
    json.dump(all_items, outfile, ensure_ascii=False, indent=1)

# Сортируем данные по ключу "title" в алфавитном порядке
sorted_items = sorted(all_items, key=lambda x: x.get('title', '').lower())

with open('lab_3/results/2/sorted_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_items, f, ensure_ascii=False, indent=1)

# Считаем статистику для ключа "ram"
ram = [int(item['ram']) for item in all_items if 'ram' in item and item['ram'] is not None]

if ram:

    min_ram = min(ram)
    max_ram = max(ram)
    avg_ram = round(sum(ram) / len(ram), 4)

else:

    min_ram = max_ram = avg_ram = None

stat = {
    'ram': {
        'Минимальное значение': min_ram,
        'Максимальное значение': max_ram,
        'Среднее значение': avg_ram
    }
}

with open('lab_3/results/2/stat_data.json', 'w', encoding='utf-8') as f:
    json.dump(stat, f, ensure_ascii=False, indent=1)

# Находим частоту ключа "matrix"
matrix = [item['matrix'] for item in all_items if 'matrix' in item]

matrix_freq = Counter(matrix)

with open('lab_3/results/2/matrix_freq_data.json', 'w', encoding='utf-8') as f:
    json.dump(matrix_freq, f, ensure_ascii=False, indent=1)