import json
import re

TIPO_SIGNIFICADOS = {
    'PL': ('Projeto de Lei Ordinária', 'Proposta de nova lei ou alteração de lei existente. Exige aprovação por maioria simples no Congresso.'),
    'PEC': ('Proposta de Emenda à Constituição', 'Muda a Carta Magna do país. É a proposição mais rigorosa: precisa de 3/5 dos votos em dois turnos na Câmara e no Senado.'),
    'MPV': ('Medida Provisória', 'Ato do Presidente da República com força de lei imediata por relevância e urgência. Deve ser votada pelo Congresso em até 120 dias ou perde a validade.'),
    'PLP': ('Projeto de Lei Complementar', 'Regulamenta temas específicos exigidos pela Constituição (ex: tributos, finanças públicas). Exige maioria absoluta (mais da metade do total de membros).'),
    'PDL': ('Projeto de Decreto Legislativo', 'Regula matérias de competência exclusiva do Congresso, como tratados internacionais ou atos do Poder Executivo.'),
    'PDS': ('Projeto de Decreto Legislativo do Senado', 'Norma interna de competência do Senado Federal.'),
    'PLS': ('Projeto de Lei do Senado', 'Nomenclatura anterior usada para Projetos de Lei iniciados por Senadores.'),
    'PLC': ('Projeto de Lei da Câmara', 'Projeto de lei originado na Câmara dos Deputados em análise pelos senadores.'),
    'SUG': ('Sugestão Legislativa', 'Ideia nascida da própria população (pelo e-Cidadania). Se conseguir 20 mil apoios, vira SUG e é debatida pelos Senadores na Comissão de Direitos Humanos e Legislação Participativa (CDH).')
}

with open(r'C:\Users\96062875\.gemini\antigravity\scratch\letramento_politico\proposicoes.json', 'r', encoding='utf-8') as f:
    proposicoes = json.load(f)

for p in proposicoes:
    sigla = p['sigla'].strip()
    match = re.match(r'^([A-Z]+)', sigla)
    tipo_prefix = match.group(1) if match else 'PL'
    
    nome_tipo, explicacao_tipo = TIPO_SIGNIFICADOS.get(tipo_prefix, ('Proposição Legislativa', 'Iniciativa que tramita no Congresso Nacional.'))
    p['tipo_sigla'] = tipo_prefix
    p['tipo_nome'] = nome_tipo
    p['tipo_explicacao'] = explicacao_tipo
    
    # Gerar letramento simples
    ementa = p['ementa']
    tema = p['tema']
    
    # Gerar resumo em linguagem acessível
    resumo_facil = ementa
    if "Altera o Código Penal" in ementa:
        resumo_facil = "Propõe modificações diretas nas punições e regras criminais do país."
    elif "Concede anistia" in ementa:
        resumo_facil = "Propõe perdoar judicialmente acusações ou condenações penais ligadas aos eventos citados."
    elif "isenção do Imposto" in ementa:
        resumo_facil = "Propõe dispensar o pagamento de imposto de renda para categorias ou atividades específicas."
    elif "Proíbe a exploração" in ementa or "apostas" in ementa.lower():
        resumo_facil = "Prevê restrições ou proibição legal sobre empresas de apostas esportivas e jogos de azar online no Brasil."
    elif "Estatuto" in ementa:
        resumo_facil = "Cria um conjunto unificado de regras, direitos e deveres para a categoria mencionada."
    elif "instituir o Imposto sobre Grandes Fortunas" in ementa:
        resumo_facil = "Cria uma taxação específica sobre patrimônios de valor muito elevado, conforme previsto na Constituição de 1988."
    elif "jornada de trabalho" in ementa.lower():
        resumo_facil = "Mexe nas regras e limites de horas trabalhadas na semana e folgas da CLT/Constituição."
    
    p['resumo_facil'] = resumo_facil

with open(r'C:\Users\96062875\.gemini\antigravity\scratch\letramento_politico\proposicoes.json', 'w', encoding='utf-8') as f:
    json.dump(proposicoes, f, ensure_ascii=False, indent=2)

print(f"Enriched {len(proposicoes)} items!")
