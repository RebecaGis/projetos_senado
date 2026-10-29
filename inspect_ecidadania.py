import os
from bs4 import BeautifulSoup

html_path = 'ecidadania.html'
if not os.path.exists(html_path):
    html_path = r'C:\Users\96062875\.gemini\antigravity\ecidadania.html'

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("=== Page Title ===")
print(soup.title.text.strip() if soup.title else 'None')

print("\n=== All links containing 'visualizacaomateria' or 'pesquisamateria' ===")
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'visualizacaomateria' in href or 'pesquisamateria' in href:
        print(f"HREF: {href} | TEXT: {a.get_text(' ', strip=True)}")

print("\n=== Looking for themes / form filters ===")
for select in soup.find_all('select'):
    print("SELECT:", select.get('name'), select.get('id'))
    for opt in select.find_all('option'):
        print(f"  [{opt.get('value')}] {opt.text.strip()}")

print("\n=== Main content text sample ===")
main = soup.find('div', id='content') or soup.find('main') or soup.body
if main:
    print(main.get_text('\n', strip=True)[:1500])
