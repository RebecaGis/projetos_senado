/**
 * e-Cidadania: Letramento Político Mobile - Lógica do Aplicativo
 */

// Estado global da aplicação
const state = {
  proposicoes: [],
  filtered: [],
  selectedTheme: 'Todos',
  searchQuery: '',
  sortBy: 'mais_votados',
  currentTab: 'tab-consultas',
  darkMode: false,
  fullscreen: false,
  activeMateriaModal: null,
  userVotes: JSON.parse(localStorage.getItem('poli_user_votes') || '{}'),
  savedMaterias: JSON.parse(localStorage.getItem('poli_saved_materias') || '[]')
};

// Elementos do DOM
const DOM = {
  propositionsList: document.getElementById('propositionsList'),
  themeChipsNav: document.getElementById('themeChipsNav'),
  searchInput: document.getElementById('searchInput'),
  clearSearchBtn: document.getElementById('clearSearchBtn'),
  sortSelect: document.getElementById('sortSelect'),
  resultsCount: document.getElementById('resultsCount'),
  emptyState: document.getElementById('emptyState'),
  resetFiltersBtn: document.getElementById('resetFiltersBtn'),
  refreshBtn: document.getElementById('refreshBtn'),
  themeToggleBtn: document.getElementById('themeToggleBtn'),
  themeIcon: document.getElementById('themeIcon'),
  statusTime: document.getElementById('statusTime'),
  toggleFullscreenBtn: document.getElementById('toggleFullscreenBtn'),
  deviceFrame: document.getElementById('deviceFrame'),
  statTotalMaterias: document.getElementById('statTotalMaterias'),
  statTotalVotos: document.getElementById('statTotalVotos'),
  themesGrid: document.getElementById('themesGrid'),
  
  // Modal
  materiaModal: document.getElementById('materiaModal'),
  modalCloseBtn: document.getElementById('modalCloseBtn'),
  modalSigla: document.getElementById('modalSigla'),
  modalTipoTag: document.getElementById('modalTipoTag'),
  modalTemaTag: document.getElementById('modalTemaTag'),
  modalTipoNome: document.getElementById('modalTipoNome'),
  modalResumoFacil: document.getElementById('modalResumoFacil'),
  modalEmenta: document.getElementById('modalEmenta'),
  modalBarSim: document.getElementById('modalBarSim'),
  modalBarNao: document.getElementById('modalBarNao'),
  modalVotosSim: document.getElementById('modalVotosSim'),
  modalPctSim: document.getElementById('modalPctSim'),
  modalVotosNao: document.getElementById('modalVotosNao'),
  modalPctNao: document.getElementById('modalPctNao'),
  modalVoteSimBtn: document.getElementById('modalVoteSimBtn'),
  modalVoteNaoBtn: document.getElementById('modalVoteNaoBtn'),
  userVotedFeedback: document.getElementById('userVotedFeedback'),
  modalOficialBtn: document.getElementById('modalOficialBtn'),
  modalShareBtn: document.getElementById('modalShareBtn'),
  modalSaveBtn: document.getElementById('modalSaveBtn'),
  
  // Perfil
  userTotalSimulated: document.getElementById('userTotalSimulated'),
  userCountSim: document.getElementById('userCountSim'),
  userCountNao: document.getElementById('userCountNao'),
  userCountSaved: document.getElementById('userCountSaved'),
  savedList: document.getElementById('savedList'),
  clearDataBtn: document.getElementById('clearDataBtn'),
  
  toast: document.getElementById('toastNotification')
};

// Ícone SVG de estrela para favoritar
function getStarIcon(isFilled) {
  if (isFilled) {
    return `<svg width="18" height="18" viewBox="0 0 24 24" fill="#D97706" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`;
  }
  return `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`;
}

// Formatação brasileira de números (ex: 725.958)
function formatNumber(num) {
  if (num === undefined || num === null) return '0';
  return num.toLocaleString('pt-BR');
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
  initClock();
  initTheme();
  setupEventListeners();
  loadData();
});

// Relógio da barra de status móvel
function initClock() {
  const updateTime = () => {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    if (DOM.statusTime) DOM.statusTime.textContent = `${hours}:${minutes}`;
  };
  updateTime();
  setInterval(updateTime, 30000);
}

// Tema Claro / Escuro
function initTheme() {
  const savedTheme = localStorage.getItem('poli_theme');
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    state.darkMode = true;
    document.body.classList.add('dark-mode');
    updateThemeIcon();
  } else {
    state.darkMode = false;
    document.body.classList.remove('dark-mode');
    updateThemeIcon();
  }
}

function updateThemeIcon() {
  if (state.darkMode) {
    DOM.themeIcon.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
  } else {
    DOM.themeIcon.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
  }
}

function toggleTheme() {
  state.darkMode = !state.darkMode;
  document.body.classList.toggle('dark-mode', state.darkMode);
  updateThemeIcon();
  localStorage.setItem('poli_theme', state.darkMode ? 'dark' : 'light');
  showToast(state.darkMode ? 'Modo Noturno ativado' : 'Modo Claro ativado');
}

// Carregar dados de proposicoes.json
async function loadData() {
  DOM.resultsCount.textContent = 'Buscando consultas do Senado...';
  try {
    const res = await fetch('proposicoes.json');
    if (!res.ok) throw new Error('Falha ao ler proposicoes.json');
    state.proposicoes = await res.json();
    onDataLoaded();
  } catch (err) {
    console.error('Erro ao carregar dados:', err);
    try {
      const res = await fetch('/api/proposicoes');
      state.proposicoes = await res.json();
      onDataLoaded();
    } catch (err2) {
      DOM.resultsCount.textContent = 'Erro ao carregar dados locais.';
      showToast('Erro ao carregar consultas.');
    }
  }
}

function onDataLoaded() {
  DOM.statTotalMaterias.textContent = state.proposicoes.length;
  
  const totalVotos = state.proposicoes.reduce((acc, curr) => acc + (curr.total_votos || 0), 0);
  DOM.statTotalVotos.textContent = `${(totalVotos / 1000000).toFixed(1)}M+`;

  renderThemeChips();
  renderThemesCatalog();
  applyFiltersAndSort();
  updateUserProfile();
}

// Renderiza carrossel horizontal de temas (sem emojis)
function renderThemeChips() {
  const counts = { 'Todos': state.proposicoes.length };
  state.proposicoes.forEach(p => {
    const t = p.tema || 'Geral e Cidadania';
    counts[t] = (counts[t] || 0) + 1;
  });

  DOM.themeChipsNav.innerHTML = '';
  
  Object.keys(counts).forEach(themeName => {
    const chip = document.createElement('button');
    chip.className = `theme-chip ${state.selectedTheme === themeName ? 'active' : ''}`;
    chip.innerHTML = `
      <span>${themeName}</span>
      <span class="chip-count">${counts[themeName]}</span>
    `;
    chip.addEventListener('click', () => {
      selectTheme(themeName);
    });
    DOM.themeChipsNav.appendChild(chip);
  });
}

function selectTheme(themeName) {
  state.selectedTheme = themeName;
  document.querySelectorAll('.theme-chip').forEach(c => {
    c.classList.toggle('active', c.textContent.includes(themeName));
  });
  applyFiltersAndSort();
}

// Renderiza catálogo na Aba Temas
function renderThemesCatalog() {
  const themesMap = {};
  state.proposicoes.forEach(p => {
    const t = p.tema || 'Geral e Cidadania';
    if (!themesMap[t]) {
      themesMap[t] = { count: 0, votos: 0, topMateria: p.sigla };
    }
    themesMap[t].count++;
    themesMap[t].votos += (p.total_votos || 0);
  });

  DOM.themesGrid.innerHTML = '';
  Object.entries(themesMap).sort((a, b) => b[1].count - a[1].count).forEach(([theme, info]) => {
    const card = document.createElement('div');
    card.className = 'theme-card';
    card.innerHTML = `
      <div class="theme-card-left">
        <div class="theme-icon-box">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
        <div class="theme-card-info">
          <h3>${theme}</h3>
          <span>${info.count} consultas • ${(info.votos / 1000).toFixed(0)}k votos</span>
        </div>
      </div>
      <div class="theme-card-arrow">→</div>
    `;
    card.addEventListener('click', () => {
      switchTab('tab-consultas');
      selectTheme(theme);
    });
    DOM.themesGrid.appendChild(card);
  });
}

// Filtra e ordena proposições
function applyFiltersAndSort() {
  let list = [...state.proposicoes];

  if (state.selectedTheme !== 'Todos') {
    list = list.filter(p => p.tema === state.selectedTheme);
  }

  if (state.searchQuery.trim() !== '') {
    const q = state.searchQuery.toLowerCase().trim();
    list = list.filter(p => 
      p.sigla.toLowerCase().includes(q) ||
      p.ementa.toLowerCase().includes(q) ||
      (p.resumo_facil && p.resumo_facil.toLowerCase().includes(q)) ||
      (p.tipo_nome && p.tipo_nome.toLowerCase().includes(q))
    );
  }

  if (state.sortBy === 'mais_votados') {
    list.sort((a, b) => (b.total_votos || 0) - (a.total_votos || 0));
  } else if (state.sortBy === 'mais_aprovadas') {
    list.sort((a, b) => (b.pct_sim || 0) - (a.pct_sim || 0));
  } else if (state.sortBy === 'mais_rejeitadas') {
    list.sort((a, b) => (b.pct_nao || 0) - (a.pct_nao || 0));
  } else if (state.sortBy === 'recentes') {
    list.sort((a, b) => (b.id || 0) - (a.id || 0));
  }

  state.filtered = list;
  renderPropositionsFeed();
}

// Renderiza feed de cards
function renderPropositionsFeed() {
  DOM.propositionsList.innerHTML = '';
  
  if (state.filtered.length === 0) {
    DOM.emptyState.style.display = 'block';
    DOM.resultsCount.textContent = '0 consultas encontradas';
    return;
  }

  DOM.emptyState.style.display = 'none';
  DOM.resultsCount.textContent = `Exibindo ${state.filtered.length} consultas`;

  state.filtered.slice(0, 40).forEach(p => {
    const card = createMateriaCard(p);
    DOM.propositionsList.appendChild(card);
  });
}

// Criação do elemento DOM de cada Card (sem emojis)
function createMateriaCard(p) {
  const card = document.createElement('article');
  card.className = 'materia-card';
  card.setAttribute('data-id', p.id);

  const isSaved = state.savedMaterias.includes(p.id);
  const userVote = state.userVotes[p.id];
  const siglaPrefix = (p.tipo_sigla || 'PL').toLowerCase();

  card.innerHTML = `
    <div class="card-top">
      <div class="card-badges">
        <span class="tag-tipo ${siglaPrefix}">${p.tipo_sigla || 'PL'}</span>
        <span class="tag-tema">${p.tema}</span>
      </div>
      <button class="btn-fav ${isSaved ? 'active' : ''}" title="${isSaved ? 'Remover dos salvos' : 'Salvar para acompanhar'}" aria-label="Favoritar">
        ${getStarIcon(isSaved)}
      </button>
    </div>

    <h2 class="card-sigla">${p.sigla}</h2>

    <!-- Box de Letramento: Explicação em Linguagem Simples -->
    <div class="letramento-preview">
      <strong>Em Linguagem Simples:</strong>
      ${p.resumo_facil || p.ementa}
    </div>

    <p class="card-ementa" title="${p.ementa}">${p.ementa}</p>

    <!-- Termômetro de Votação Popular Oficial -->
    <div class="card-poll">
      <div class="poll-labels">
        <span class="poll-label sim">SIM: ${p.pct_sim}% (${formatNumber(p.votos_sim)})</span>
        <span class="poll-label nao">NÃO: ${p.pct_nao}% (${formatNumber(p.votos_nao)})</span>
      </div>
      <div class="poll-bar">
        <div class="poll-bar-sim" style="width: ${p.pct_sim}%;"></div>
      </div>
      <div class="poll-footer">
        <span>Total: ${formatNumber(p.total_votos)} votos</span>
        ${userVote ? `<span>Seu voto simulado: <strong>${userVote}</strong></span>` : '<span>Não votado ainda</span>'}
      </div>
    </div>

    <!-- Ações Rápidas -->
    <div class="card-actions">
      <button class="card-btn primary btn-open-modal">
        Entender Proposta
      </button>
      <a href="${p.url}" target="_blank" rel="noopener" class="card-btn">
        Votar no Senado ↗
      </a>
    </div>
  `;

  const favBtn = card.querySelector('.btn-fav');
  favBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleSaveMateria(p.id);
  });

  const openModalBtn = card.querySelector('.btn-open-modal');
  openModalBtn.addEventListener('click', () => {
    openMateriaModal(p);
  });

  return card;
}

// Abrir Modal de Detalhes Aprofundados
function openMateriaModal(p) {
  state.activeMateriaModal = p;

  DOM.modalSigla.textContent = p.sigla;
  DOM.modalTipoTag.textContent = p.tipo_sigla || 'PL';
  DOM.modalTipoTag.className = `modal-tipo-tag ${(p.tipo_sigla || 'pl').toLowerCase()}`;
  DOM.modalTemaTag.textContent = p.tema;
  DOM.modalTipoNome.textContent = p.tipo_nome ? `${p.tipo_nome} • ${p.tipo_explicacao || ''}` : 'Proposição Legislativa';

  DOM.modalResumoFacil.textContent = p.resumo_facil || p.ementa;
  DOM.modalEmenta.textContent = p.ementa;

  DOM.modalBarSim.style.width = `${p.pct_sim}%`;
  DOM.modalBarNao.style.width = `${p.pct_nao}%`;

  DOM.modalVotosSim.textContent = formatNumber(p.votos_sim);
  DOM.modalPctSim.textContent = `${p.pct_sim}% dos votos populares`;

  DOM.modalVotosNao.textContent = formatNumber(p.votos_nao);
  DOM.modalPctNao.textContent = `${p.pct_nao}% dos votos populares`;

  DOM.modalOficialBtn.href = p.url;

  updateModalUserVoteState(p.id);

  const isSaved = state.savedMaterias.includes(p.id);
  DOM.modalSaveBtn.textContent = isSaved ? 'Salva (Remover)' : 'Salvar para Acompanhar';

  DOM.materiaModal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

function updateModalUserVoteState(materiaId) {
  const currentVote = state.userVotes[materiaId];
  DOM.modalVoteSimBtn.classList.toggle('selected', currentVote === 'SIM');
  DOM.modalVoteNaoBtn.classList.toggle('selected', currentVote === 'NÃO');

  if (currentVote) {
    DOM.userVotedFeedback.style.display = 'block';
    DOM.userVotedFeedback.textContent = `Você simulou voto ${currentVote}. Posicionamento registrado no perfil.`;
  } else {
    DOM.userVotedFeedback.style.display = 'none';
  }
}

function closeMateriaModal() {
  DOM.materiaModal.style.display = 'none';
  document.body.style.overflow = 'auto';
  state.activeMateriaModal = null;
}

// Simulação de Voto
function simulateVote(voteType) {
  if (!state.activeMateriaModal) return;
  const p = state.activeMateriaModal;

  state.userVotes[p.id] = voteType;
  localStorage.setItem('poli_user_votes', JSON.stringify(state.userVotes));

  updateModalUserVoteState(p.id);
  updateUserProfile();
  applyFiltersAndSort();
  showToast(`Voto ${voteType} simulado com sucesso.`);
}

// Salvar / Favoritar Matéria
function toggleSaveMateria(materiaId) {
  const idx = state.savedMaterias.indexOf(materiaId);
  if (idx >= 0) {
    state.savedMaterias.splice(idx, 1);
    showToast('Removido das matérias salvas.');
  } else {
    state.savedMaterias.push(materiaId);
    showToast('Salvo no perfil.');
  }

  localStorage.setItem('poli_saved_materias', JSON.stringify(state.savedMaterias));
  
  if (state.activeMateriaModal && state.activeMateriaModal.id === materiaId) {
    const isSaved = state.savedMaterias.includes(materiaId);
    DOM.modalSaveBtn.textContent = isSaved ? 'Salva (Remover)' : 'Salvar para Acompanhar';
  }

  applyFiltersAndSort();
  updateUserProfile();
}

// Compartilhar no WhatsApp (sem emojis)
function shareOnWhatsApp() {
  if (!state.activeMateriaModal) return;
  const p = state.activeMateriaModal;
  const texto = `Consulta Pública no Senado: ${p.sigla} (${p.tema})\n\nEm Linguagem Simples: ${p.resumo_facil || p.ementa}\n\nPlacar no e-Cidadania: ${p.pct_sim}% SIM vs ${p.pct_nao}% NÃO (${formatNumber(p.total_votos)} votos)\n\nParticipe da votação: ${p.url}`;
  const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(texto)}`;
  window.open(url, '_blank');
}

// Navegação de Abas
function switchTab(tabId) {
  state.currentTab = tabId;
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));

  const targetPane = document.getElementById(tabId);
  if (targetPane) targetPane.classList.add('active');

  const activeBtn = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
  if (activeBtn) activeBtn.classList.add('active');

  if (tabId === 'tab-perfil') {
    updateUserProfile();
  }
}

// Atualizar Perfil do Usuário
function updateUserProfile() {
  const voteEntries = Object.entries(state.userVotes);
  const totalVotes = voteEntries.length;
  const simCount = voteEntries.filter(([_, v]) => v === 'SIM').length;
  const naoCount = voteEntries.filter(([_, v]) => v === 'NÃO').length;

  DOM.userTotalSimulated.textContent = totalVotes;
  DOM.userCountSim.textContent = simCount;
  DOM.userCountNao.textContent = naoCount;
  DOM.userCountSaved.textContent = state.savedMaterias.length;

  DOM.savedList.innerHTML = '';
  if (state.savedMaterias.length === 0) {
    DOM.savedList.innerHTML = `
      <div style="text-align: center; padding: 20px; color: var(--text-muted); font-size: 0.85rem;">
        Nenhuma matéria salva ainda. Clique no ícone de estrela de qualquer projeto para acompanhá-lo aqui.
      </div>
    `;
    return;
  }

  state.savedMaterias.forEach(id => {
    const p = state.proposicoes.find(x => x.id === id);
    if (!p) return;
    const item = document.createElement('div');
    item.className = 'theme-card';
    item.innerHTML = `
      <div class="theme-card-left">
        <div class="theme-icon-box">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
        </div>
        <div class="theme-card-info">
          <h3>${p.sigla}</h3>
          <span>${p.tema} • ${p.pct_sim}% SIM vs ${p.pct_nao}% NÃO</span>
        </div>
      </div>
      <button class="text-btn danger btn-remove-saved" data-id="${p.id}">Remover</button>
    `;
    item.querySelector('.btn-remove-saved').addEventListener('click', (e) => {
      e.stopPropagation();
      toggleSaveMateria(p.id);
    });
    item.addEventListener('click', () => {
      openMateriaModal(p);
    });
    DOM.savedList.appendChild(item);
  });
}

// Toast de feedback
let toastTimeout;
function showToast(msg) {
  if (!DOM.toast) return;
  DOM.toast.textContent = msg;
  DOM.toast.classList.add('show');
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    DOM.toast.classList.remove('show');
  }, 2500);
}

// Configuração de Event Listeners
function setupEventListeners() {
  DOM.searchInput.addEventListener('input', (e) => {
    state.searchQuery = e.target.value;
    DOM.clearSearchBtn.style.display = state.searchQuery ? 'block' : 'none';
    applyFiltersAndSort();
  });

  DOM.clearSearchBtn.addEventListener('click', () => {
    DOM.searchInput.value = '';
    state.searchQuery = '';
    DOM.clearSearchBtn.style.display = 'none';
    applyFiltersAndSort();
  });

  DOM.sortSelect.addEventListener('change', (e) => {
    state.sortBy = e.target.value;
    applyFiltersAndSort();
  });

  DOM.resetFiltersBtn.addEventListener('click', () => {
    DOM.searchInput.value = '';
    state.searchQuery = '';
    DOM.clearSearchBtn.style.display = 'none';
    selectTheme('Todos');
  });

  document.querySelectorAll('.bottom-nav .nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.getAttribute('data-tab');
      switchTab(tabId);
    });
  });

  DOM.themeToggleBtn.addEventListener('click', toggleTheme);

  DOM.refreshBtn.addEventListener('click', async () => {
    DOM.refreshBtn.style.transform = 'rotate(360deg)';
    DOM.refreshBtn.style.transition = 'transform 0.5s ease';
    showToast('Sincronizando com o Senado...');
    try {
      const res = await fetch('/api/atualizar');
      if (res.ok) {
        showToast('Consultas atualizadas com sucesso.');
        await loadData();
      } else {
        await loadData();
        showToast('Base recarregada com sucesso.');
      }
    } catch {
      await loadData();
      showToast('Base recarregada.');
    }
    setTimeout(() => {
      DOM.refreshBtn.style.transform = 'none';
    }, 600);
  });

  DOM.toggleFullscreenBtn.addEventListener('click', () => {
    state.fullscreen = !state.fullscreen;
    document.body.classList.toggle('fullscreen-mode', state.fullscreen);
    DOM.toggleFullscreenBtn.textContent = state.fullscreen ? 'Modo Celular' : 'Modo Tela Cheia';
    showToast(state.fullscreen ? 'Exibindo em Tela Cheia' : 'Exibindo em Moldura de Smartphone');
  });

  DOM.modalCloseBtn.addEventListener('click', closeMateriaModal);
  DOM.materiaModal.addEventListener('click', (e) => {
    if (e.target === DOM.materiaModal) closeMateriaModal();
  });

  DOM.modalVoteSimBtn.addEventListener('click', () => simulateVote('SIM'));
  DOM.modalVoteNaoBtn.addEventListener('click', () => simulateVote('NÃO'));
  DOM.modalShareBtn.addEventListener('click', shareOnWhatsApp);
  DOM.modalSaveBtn.addEventListener('click', () => {
    if (state.activeMateriaModal) toggleSaveMateria(state.activeMateriaModal.id);
  });

  DOM.clearDataBtn.addEventListener('click', () => {
    if (confirm('Deseja realmente apagar suas votações simuladas e matérias salvas?')) {
      state.userVotes = {};
      state.savedMaterias = [];
      localStorage.removeItem('poli_user_votes');
      localStorage.removeItem('poli_saved_materias');
      updateUserProfile();
      applyFiltersAndSort();
      showToast('Histórico limpo com sucesso.');
    }
  });
}
