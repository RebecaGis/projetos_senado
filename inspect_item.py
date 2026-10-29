from bs4 import BeautifulSoup

with open(r'C:\Users\96062875\.gemini\antigravity\scratch\letramento_politico\pesquisamateria.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find first 3 items linking to visualizacaomateria
items = []
for a in soup.find_all('a', href=lambda h: h and 'visualizacaomateria' in h):
    parent = a.find_parent('li') or a.find_parent('div', class_=lambda c: c and any(x in str(c) for x in ['item', 'linha', 'materia', 'proposicao']))
    if parent and parent not in items:
        items.append(parent)

print(f"Found {len(items)} parent elements")
for idx, it in enumerate(items[:3]):
    print(f"\n--- Item {idx+1} (Tag: {it.name}, Class: {it.get('class')}) ---")
    print(it.prettify()[:1000])
