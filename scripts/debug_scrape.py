import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://www.bclivesurgery.com.br/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

items = []
# tentar achar blocos que tenham imagens e nomes
for img in soup.find_all('img'):
    src = img.get('src')
    alt = img.get('alt', '')
    parent = img.find_parent('div')
    
    # Tentativa de capturar texto próximo
    if parent and parent.parent:
        text = parent.parent.get_text(strip=True, separator=' | ')
        items.append({"src": src, "alt": alt, "text": text[:100]})

with open('debug_scrape.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

print("Saved debug_scrape.json")
