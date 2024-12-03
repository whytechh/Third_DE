import json
import re
import requests
from bs4 import BeautifulSoup

response = requests.get('https://urban3p.ru/objects?page=3')

if response.status_code == 200:
    print("Success!")
else:
    print(f"Failed to retrieve data: {response.status_code}")