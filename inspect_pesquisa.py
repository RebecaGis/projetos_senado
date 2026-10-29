from bs4 import BeautifulSoup

with open(r'C:\Users\96062875\.gemini\antigravity\scratch\letramento_politico\pesquisamateria.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("=== SELECTS ===")
for s in soup.find_all('select'):
    print("Select:", s.get('name'), s.get('id'))
    opts = s.find_all('option')
    print(f"Total options: {len(opts)}")
    for opt in opts[:15]:
        print(f"  val: '{opt.get('value')}' label: '{opt.text.strip()}'")

print("\n=== CARDS / ITEMS ===")
materias = []
for item in soup.find_all('div', class_='card'):
    materias.append(item.get_text(' ', strip=True)[:150])
print(f"Total cards: {len(materias)}")
for m in materias[:5]:
    print(" -", m)

print("\n=== All links with visualizacaomateria ===")
seen = set()
for a in soup.find_all('a', href=True):
    if 'visualizacaomateria' in a['href'] and a['href'] not in seen:
        seen.add(a['href'])
        print(a['href'], "->", a.get_text(' ', strip=True)[:80])
