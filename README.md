# 🏛️ e-Cidadania: Letramento Político Mobile

<!-- project-badges:start -->
![Interface: HTML · CSS · JavaScript](https://img.shields.io/static/v1?label=Interface&message=HTML%20%C2%B7%20CSS%20%C2%B7%20JavaScript&color=E34F26&style=flat)
![Coleta: Python](https://img.shields.io/static/v1?label=Coleta&message=Python&color=3776AB&style=flat)
[![Autoria: Rebeca Diniz Moura](https://img.shields.io/static/v1?label=Autoria&message=Rebeca%20Diniz%20Moura&color=8b5cf6&style=flat)](https://github.com/RebecaGis)
<!-- project-badges:end -->

Aplicativo móvel desenvolvido para facilitar o **letramento político** da população brasileira através da leitura, compreensão e acompanhamento das consultas públicas em tramitação no Senado Federal pelo portal **e-Cidadania** ([https://www12.senado.leg.br/ecidadania/principalmateria](https://www12.senado.leg.br/ecidadania/principalmateria)).

---

## 📱 Recursos Principais do Aplicativo

1. **Leitura Automatizada do e-Cidadania:**
   - Extrai em tempo real as consultas públicas e proposições do portal do Senado Federal (`principalmateria` e `pesquisamateria`).
   - Coleta votos computados de **SIM** e **NÃO**, percentuais, número da matéria e link oficial com autenticação `gov.br`.

2. **Organização por Temas:**
   - 🛡️ **Segurança e Justiça** (Código Penal, anistias, armas, penas)
   - 💼 **Economia e Finanças** (tributação, IRPF, apostas esportivas, grandes fortunas)
   - 🏥 **Saúde e Bioética** (SUS, vacinas, medicamentos)
   - 👷 **Trabalho e Previdência** (jornada de trabalho, CLT, direitos trabalhistas)
   - 🎓 **Educação e Cultura** (escolas, universidades, esportes)
   - 🌿 **Meio Ambiente e Agro** (clima, sustentabilidade, agronegócio)
   - 🤝 **Direitos Humanos e Sociedade** (cidadania, minorias, garantias fundamentais)
   - 💻 **Tecnologia e Informação** (dados, inteligência artificial, redes sociais)
   - 🌐 **Geral e Cidadania**

3. **Central de Letramento Político (Educação Cidadã):**
   - **"Em Miúdos":** Tradução das ementas jurídicas complexas para linguagem simples e direta.
   - **Glossário Interativo das Siglas:** O que significa **PL**, **PEC**, **MPV**, **PLP**, **SUG**, **PDL** e qual a exigência de quórum de cada uma.
   - **Infográfico "Como nasce uma Lei":** Do protocolo inicial, passando pelo voto popular do e-Cidadania, comissões temáticas, plenário da Câmara e Senado, até a sanção ou veto presidencial.
   - **O Poder do e-Cidadania:** Explicação de como o relatório das votações online é formalmente anexado ao processo do senador relator.

4. **Termômetro Popular & Simulador de Voto:**
   - Barras visuais coloridas com o placar de aprovação popular nacional em tempo real.
   - Simulador para o usuário registrar como votaria (Sim ou Não) e comparar seu posicionamento com o resto do país.
   - Armazenamento local seguro (`localStorage`) de matérias favoritadas e histórico cidadão.

5. **Design Mobile-First Nativo:**
   - Moldura de smartphone interativa para desktop (com notch, barra de status dinâmica e botão para tela cheia).
   - Barra de navegação inferior com 4 abas táteis: *Consultas*, *Temas*, *Letramento* e *Meu Voto*.
   - Modo Noturno (Dark Mode) e Modo Claro.
   - Compartilhamento mastigado em 1 clique para WhatsApp.
   - Suporte a PWA (Progressive Web App): pode ser instalado diretamente na tela inicial do celular.

---

## 🚀 Como Executar

### 1. Iniciar o Servidor Local
No terminal, entre na pasta do projeto e execute:

```powershell
cd projetos_senado
python server.py
```

O terminal exibirá os endereços de acesso:
- **No Computador:** `http://localhost:8080`
- **No Celular (mesma rede Wi-Fi):** `http://IP_DO_SEU_PC:8080`

### 2. Abrir no Celular
1. Conecte o celular na mesma rede Wi-Fi do computador.
2. Abra o navegador do celular (Chrome, Safari, etc.) e digite o endereço exibido (ex: `http://192.168.1.15:8080`).
3. Toque no menu do navegador e selecione **"Adicionar à Tela Inicial"** ou **"Instalar Aplicativo"** para usar como um app nativo sem barras de navegador!

---

## 🔄 Como Atualizar os Dados do Senado

Para raspar dados frescos do Senado a qualquer momento:

### Pelo próprio aplicativo:
Clique no botão de atualizar (🔄) no topo do aplicativo. O app acionará o endpoint `/api/atualizar`.

### Pela linha de comando:
```powershell
python update_ecidadania.py
```
Isso fará o download da página oficial do Senado, processará as matérias e atualizará o arquivo `proposicoes.json`.

---

## 📂 Estrutura dos Arquivos

```
letramento_politico/
├── index.html            # Estrutura HTML5 móvel, abas e modais
├── styles.css            # Design System responsivo, variáveis de tema e mockup
├── app.js                # Lógica do app, filtros, simulação e armazenamento
├── update_ecidadania.py  # Extrator/scraper das consultas do Senado Federal
├── server.py             # Servidor HTTP local com suporte a API e acesso via Wi-Fi
├── proposicoes.json      # Base de dados local com 100 consultas catalogadas
└── manifest.json         # Manifesto PWA para instalação no celular
```
