#!/usr/bin/env python3
"""
Scraper e extrator de dados do e-Cidadania do Senado Federal
Lê https://www12.senado.leg.br/ecidadania/principalmateria e /pesquisamateria
e gera o arquivo proposicoes.json com classificação temática e letramento político.
"""

import sys
import os
import json
import re
import urllib.request
from bs4 import BeautifulSoup

URL_PRINCIPAL = "https://www12.senado.leg.br/ecidadania/principalmateria"
URL_PESQUISA = "https://www12.senado.leg.br/ecidadania/pesquisamateria"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "proposicoes.json")

THEME_KEYWORDS = {
    'Segurança e Justiça': [
        'penal', 'crime', 'armas', 'atirador', 'cacs', 'anistia', 'polícia', 'preso', 'segurança',
        'código penal', 'penas', 'tráfico', 'violência', 'condenados', 'forças armadas', 'militares',
        'porte de arma', 'homicídio', 'prisão', 'judiciário'
    ],
    'Economia e Finanças': [
        'imposto', 'irpf', 'tribut', 'crédito', 'banco', 'financeir', 'orçamento', 'isenção',
        'taxa', 'renda', 'loterias', 'apostas', 'quota fixa', 'privatiz', 'moeda', 'grandes fortunas',
        'tarifas', 'fiscal', 'dívida'
    ],
    'Saúde e Bioética': [
        'vacina', 'saúde', 'sus', 'médic', 'hospital', 'doença', 'remédio', 'medicamento',
        'aborto', 'canabidiol', 'droga', 'terapia', 'psicol', 'enferm', 'farmacêut'
    ],
    'Direitos Humanos e Sociedade': [
        'anistia', 'manifestações', 'igualdade', 'mulher', 'idoso', 'criança', 'deficiência',
        'indígena', 'racismo', 'liberdade', 'religi', 'cidadania', 'eleição', 'voto', 'diversidade',
        'discriminação', 'direitos fundamentais'
    ],
    'Trabalho e Previdência': [
        'trabalho', 'trabalhador', 'clt', 'emprego', 'salário', 'aposentadoria', 'previdência',
        'profissão', 'jornada', 'sindicato', 'feriado', 'inss', 'benefício'
    ],
    'Educação e Cultura': [
        'escola', 'ensino', 'educação', 'estudante', 'professor', 'universidade', 'cultura',
        'livro', 'patrimônio', 'esporte', 'pesquisa científica', 'bolsa'
    ],
    'Tecnologia e Informação': [
        'internet', 'inteligência artificial', 'dados', 'algoritmo', 'apostas', 'digital',
        'redes sociais', 'fake news', 'notícias falsas', 'telecomunica', 'privacidade'
    ],
    'Meio Ambiente e Agro': [
        'meio ambiente', 'clima', 'desmatamento', 'agro', 'floresta', 'água', 'animais',
        'caça', 'fauna', 'carbono', 'sustentabilidade', 'indústria química', 'agropecuária'
    ]
}

TIPO_SIGNIFICADOS = {
    'PL': ('Projeto de Lei Ordinária', 'Proposta de nova lei ou alteração de lei existente. Exige aprovação por maioria simples no Congresso.'),
    'PEC': ('Proposta de Emenda à Constituição', 'Muda a Carta Magna do país. É a proposição mais rigorosa: precisa de 3/5 dos votos em dois turnos na Câmara e no Senado.'),
    'MPV': ('Medida Provisória', 'Ato do Presidente da República com força de lei imediata por relevância e urgência. Deve ser votada pelo Congresso em até 120 dias.'),
    'PLP': ('Projeto de Lei Complementar', 'Regulamenta temas específicos exigidos pela Constituição (ex: tributos). Exige maioria absoluta de votos.'),
    'PDL': ('Projeto de Decreto Legislativo', 'Regula matérias de competência exclusiva do Congresso, como tratados internacionais ou atos do Poder Executivo.'),
    'PDS': ('Projeto de Decreto Legislativo do Senado', 'Norma interna de competência exclusiva do Senado Federal.'),
    'PLS': ('Projeto de Lei do Senado', 'Nomenclatura anterior usada para Projetos de Lei iniciados por Senadores.'),
    'PLC': ('Projeto de Lei da Câmara', 'Projeto de lei originado na Câmara dos Deputados em análise pelos senadores.'),
    'SUG': ('Sugestão Legislativa', 'Ideia nascida da própria população no e-Cidadania que atingiu 20 mil apoios e agora é debatida pelos Senadores na Comissão de Direitos Humanos.')
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

def fetch_html(url, fallback_filename=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[Aviso] Falha ao baixar {url} online ({e}).")
        if fallback_filename:
            path = os.path.join(BASE_DIR, fallback_filename)
            if os.path.exists(path):
                print(f"[Info] Carregando arquivo local de fallback: {path}")
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        return None

def parse_ecidadania():
    print(f"Lendo e-Cidadania...")
    html = fetch_html(URL_PESQUISA, fallback_filename="pesquisamateria.html")
    if not html:
        print("Erro: não foi possível obter os dados da página.")
        return []

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='resumo-materia')
    print(f"Encontradas {len(items)} proposições no e-Cidadania.")

    propositions = []

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
        
        # Tipo e letramento
        match = re.match(r'^([A-Z]+)', sigla.strip())
        tipo_prefix = match.group(1) if match else 'PL'
        nome_tipo, explicacao_tipo = TIPO_SIGNIFICADOS.get(tipo_prefix, ('Proposição Legislativa', 'Iniciativa que tramita no Congresso Nacional.'))

        # Resumo simples (linguagem cidadã)
        resumo_facil = ementa
        if "Altera o Código Penal" in ementa:
            resumo_facil = "Propõe modificações diretas nas punições, penas e condutas tipificadas como crime no Código Penal brasileiro."
        elif "Concede anistia" in ementa:
            resumo_facil = "Propõe perdoar judicialmente acusações ou condenações penais ligadas aos eventos ocorridos em Brasília em 08/01/2023."
        elif "isenção do Imposto" in ementa or "IRPF" in ementa:
            resumo_facil = "Propõe dispensar o pagamento de imposto de renda da pessoa física para a categoria ou faixa descrita no texto."
        elif "Proíbe a exploração" in ementa or "apostas" in ementa.lower():
            resumo_facil = "Cria regras de restrição ou proibição total para sites de apostas online (bets), caça-níqueis digitais e sua publicidade."
        elif "Estatuto" in ementa:
            resumo_facil = "Cria um marco legal unificado estabelecendo direitos, deveres, permissões e restrições para o grupo citado."
        elif "instituir o Imposto sobre Grandes Fortunas" in ementa:
            resumo_facil = "Regulamenta o imposto constitucional sobre patrimônios milionários/bilionários para reforçar a arrecadação pública."
        elif "jornada de trabalho" in ementa.lower():
            resumo_facil = "Altera as opções ou limites de horas de trabalho e escalas na semana previstas na Constituição e na CLT."
        elif "vacinação" in ementa.lower():
            resumo_facil = "Trata de regras sanitárias, penalidades e políticas públicas sobre imunização e campanhas de vacinação."
        
        total = votos_sim + votos_nao
        pct_sim_calc = round((votos_sim / total * 100) if total > 0 else pct_sim, 1)
        pct_nao_calc = round(100.0 - pct_sim_calc, 1)

        propositions.append({
            'id': materia_id,
            'sigla': sigla,
            'tipo_sigla': tipo_prefix,
            'tipo_nome': nome_tipo,
            'tipo_explicacao': explicacao_tipo,
            'ementa': ementa,
            'resumo_facil': resumo_facil,
            'tema': theme,
            'votos_sim': votos_sim,
            'votos_nao': votos_nao,
            'total_votos': total,
            'pct_sim': pct_sim_calc,
            'pct_nao': pct_nao_calc,
            'url': f"https://www12.senado.leg.br/ecidadania/visualizacaomateria?id={materia_id}" if materia_id else URL_PRINCIPAL
        })

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(propositions, f, ensure_ascii=False, indent=2)

    print(f"Sucesso! {len(propositions)} consultas salvas em {OUTPUT_FILE}")
    return propositions

if __name__ == '__main__':
    parse_ecidadania()
