# e-Cidadania · Letramento Político

Aplicação web de educação cidadã para consultar e acompanhar proposições e consultas públicas do Senado Federal.

## Funcionalidades

- Consulta de proposições, filtros por temas e apresentação de votos populares.
- Conteúdo educativo sobre o processo legislativo e siglas.
- Favoritos e histórico de interação armazenados no navegador.
- Interface responsiva, temas claro e escuro e manifesto para instalação.
- Rotina Python para coletar e atualizar a base local do e-Cidadania.

O projeto é independente. A participação oficial nas consultas ocorre no portal do Senado; a simulação de voto da interface não substitui o voto oficial.

## Executar localmente

Requer Python 3. Execute na pasta do repositório:

```bash
git clone https://github.com/RebecaGis/projetos_senado.git
cd projetos_senado
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# Linux ou macOS
source .venv/bin/activate
```

Instale a dependência usada pelo coletor e inicie o servidor:

```bash
python -m pip install beautifulsoup4
python server.py
```

Abra http://localhost:8080. Para acesso pelo celular, use o endereço de rede exibido no terminal e mantenha ambos na mesma rede. Esse servidor é destinado ao desenvolvimento local.

## Dados e atualização

`proposicoes.json` é uma base versionada. Em hospedagem estática, os dados correspondem ao arquivo publicado; não se deve presumir consulta em tempo real ao Senado.

Para atualizar a cópia local:

```bash
python update_ecidadania.py
```

O comando acessa o e-Cidadania e pode sobrescrever `proposicoes.json`. Confira os resultados e as mudanças do portal antes de publicar. No servidor Python local, a aplicação também possui um endpoint de atualização; em hospedagem estática, esse backend Python não é executado.

Fontes utilizadas pelo coletor:

- [Consultas públicas do Senado](https://www12.senado.leg.br/ecidadania/principalmateria)
- [Pesquisa de matérias](https://www12.senado.leg.br/ecidadania/pesquisamateria)

## Estrutura

| Caminho | Finalidade |
| --- | --- |
| `index.html`, `styles.css`, `app.js` | Interface e lógica do aplicativo |
| `manifest.json` | Manifesto da aplicação web |
| `proposicoes.json` | Base de consultas publicada |
| `server.py` | Servidor local com endpoints de dados e atualização |
| `update_ecidadania.py` | Coletor e processamento dos dados |
| `package.json` | Comando de geração das cópias estáticas |
| `dist/`, `docs/` | Cópias estáticas existentes |
| `netlify.toml`, `_headers`, `_redirects` | Configuração da hospedagem |
| `.github/workflows/` | Automação de publicação no GitHub Pages |

## Desenvolvimento e publicação

O comando `npm run build`, com Node.js e npm disponíveis, gera cópias estáticas em `dist/` e `docs/`. Ele não inicia o servidor Python.

Este README documenta a configuração existente. Alterações de código, dados, caminhos de publicação, domínio ou automações devem ser verificadas separadamente antes de qualquer deploy. Arquivos de distribuição existentes foram preservados.

## Limites

Mudanças na estrutura do portal do Senado podem exigir manutenção do coletor. Resumos e classificações são recursos de apoio; consulte os textos e registros oficiais para confirmar o conteúdo de cada proposição.
