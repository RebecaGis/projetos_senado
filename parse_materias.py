import json
import re
from bs4 import BeautifulSoup

with open(r'C:\Users\96062875\.gemini\antigravity\scratch\letramento_politico\pesquisamateria.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

items = soup.find_all('div', class_='resumo-materia')
print(f"Total items found: {len(items)}")

propositions = []

THEME_KEYWORDS = {
    'Segurança e Justiça': [
        'penal', 'crime', 'armas', 'atirador', 'cacs', 'anistia', 'polícia', 'preso', 'segurança',
        'código penal', 'penas', 'tráfico', 'violência', 'condenados', 'forças armadas', 'militares'
    ],
    'Economia e Finanças': [
        'imposto', 'irpf', 'tribut', 'crédito', 'banco', 'financeir', 'orçamento', 'isenção',
        'taxa', 'renda', 'loterias', 'apostas', 'quota fixa', 'privatiz', 'moeda'
    ],
    'Saúde e Bioética': [
        'vacina', 'saúde', 'sus', 'médic', 'hospital', 'doença', 'remédio', 'medicamento',
        'aborto', 'canabidiol', 'droga', 'terapia', 'psicol'
    ],
    'Direitos Humanos e Cidadania': [
        'anistia', 'manifestações', 'igualdade', 'mulher', 'idoso', 'criança', 'deficiência',
        'indígena', 'racismo', 'liberdade', 'religi', 'cidadania', 'eleição', 'voto'
    ],
    'Trabalho e Previdência': [
        'trabalho', 'trabalhador', 'clt', 'emprego', 'salário', 'aposentadoria', 'previdência',
        'profissão', 'jornada', 'sindicato', 'feriado'
    ],
    'Educação e Cultura': [
        'escola', 'ensino', 'educação', 'estudante', 'professor', 'universidade', 'cultura',
        'livro', 'patrimônio', 'esporte'
    ],
    'Tecnologia e Comunicação': [
        'internet', 'inteligência artificial', 'dados', 'algoritmo', 'apostas', 'digital',
        'redes sociais', 'fake news', 'notícias falsas', 'telecomunica'
    ],
    'Meio Ambiente e Agro': [
        'meio ambiente', 'clima', 'desmatamento', 'agro', 'floresta', 'água', 'animais',
        'caça', 'fauna', 'carbono', 'sustentabilidade'
    ]
}

def detect_theme(sigla, ementa):
    text = (sigla + " " + ementa).lower()
    scores = {}
    for theme, kws in THEME_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in text)
        if score > 0:
            scores[theme] = score
    if scores:
        return max(scores, key=scores.get)
    return 'Geral e Cidadania'

for it in items:
    header = it.find('header')
    sigla = header.get_text(' ', strip=True) if header else ''
    
    link = header.find('a')['href'] if header and header.find('a') else ''
    materia_id = ''
    if 'id=' in link:
        materia_id = link.split('id=')[-1].split('&')[0]
        
    section = it.find('section')
    ementa = section.get_text(' ', strip=True) if section else ''
    
    votos_sim = 0
    votos_nao = 0
    pct_sim = 50.0
    
    fig = it.find('figure', class_='grafico-consulta-publica')
    if fig:
        spans = fig.find('header').find_all('span') if fig.find('header') else []
        if len(spans) >= 2:
            try:
                votos_sim = int(spans[0].text.replace('.', '').strip())
                votos_nao = int(spans[1].text.replace('.', '').strip())
            except Exception:
                pass
        bar = fig.find('section')
        if bar and bar.find('div'):
            style = bar.find('div').get('style', '')
            m = re.search(r'width:\s*([\d\.]+)%', style)
            if m:
                pct_sim = float(m.group(1))
    
    theme = detect_theme(sigla, ementa)
    
    propositions.append({
        'id': materia_id,
        'sigla': sigla,
        'ementa': ementa,
        'votos_sim': votos_sim,
        'votos_nao': votos_nao,
        'total_votos': votos_sim + votos_nao,
        'pct_sim': round(pct_sim, 1),
        'pct_nao': round(100.0 - pct_sim, 1),
        'tema': theme,
        'url': f"https://www12.senado.leg.br/ecidadania/visualizacaomateria?id={materia_id}" if materia_id else "https://www12.senado.leg.br/ecidadania/principalmateria"
    })

print(f"Parsed {len(propositions)} propositions successfully.")
# Count by theme
by_theme = {}
for p in propositions:
    by_theme[p['tema']] = by_theme.get(p['tema'], 0) + 1

print("\nDistribution by Theme:")
for t, c in sorted(by_theme.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c} consultas")

with open(r'C:\Users\96062875\.gemini\antigravity\scratch\letramento_politico\proposicoes.json', 'w', encoding='utf-8') as out:
    json.dump(propositions, out, ensure_ascii=False, indent=2)

print("Saved to proposicoes.json!")
