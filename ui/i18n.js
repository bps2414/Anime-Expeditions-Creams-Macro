/**
 * System i18n - Anime Expeditions Creams Macro
 * Gerenciador de internacionalização resiliente, síncrono e hardened para o frontend.
 */

// Dicionário completo de traduções para os idiomas suportados (en, pt-BR)
const TRANSLATIONS = {
  'en': {
    buttons: {
      start: 'Start',
      stop: 'Stop',
      pause: 'Pause',
      resume: 'Resume',
      import: 'Import',
      export: 'Export',
      save: 'Save',
      cancel: 'Cancel',
      reset: 'Reset to Defaults',
      apply: 'Apply',
      popOut: 'Pop Out',
      clear: 'Clear',
      addTask: '+ Add Task',
      skip: 'Skip',
      presets: 'Presets',
      addBlock: '+ Add Block',
      record: 'Record',
      test: 'Test Macro',
      delete: 'Delete',
      edit: 'Edit',
      close: 'Close',
      sendTest: 'Send Test Notification',
      toggleOn: 'Enabled',
      toggleOff: 'Disabled'
    },
    tabs: {
      general: 'General',
      settings: 'Settings',
      dashboard: 'Dashboard',
      task: 'Task Queue',
      creation: 'Macro Manager',
      challenge: 'Challenge',
      hotkeys: 'Hotkeys',
      webhook: 'Discord Webhook',
      debug: 'Debug & Tests',
      prestart: 'Prestart Phase',
      battle: 'Battle Phase'
    },
    header: {
      session: 'Session',
      allTime: 'All Time',
      openSourceSecurity: 'Open-Source Security & False Positives:'
    },
    dashboard: {
      processLog: 'Process Log',
      waitingStart: '> Waiting for macro to start...',
      statusReadout: 'Status Readout',
      action: 'Action',
      currentTask: 'Current Task',
      repeat: 'Repeat',
      map: 'Map',
      lastRun: 'Last Run',
      runsPerHour: 'Runs / Hour',
      timeUntilChallenge: 'Time Until Challenge',
      mode: 'Mode',
      stage: 'Stage',
      difficulty: 'Difficulty',
      playMode: 'Play Mode',
      macro: 'Macro',
      scoreboard: 'Scoreboard',
      wins: 'Wins',
      winRate: 'Win Rate',
      losses: 'Losses',
      totalRuns: 'total runs',
      lifetimeRecord: 'lifetime record',
      controls: 'Controls',
      runHistory: 'Run History',
      noRunsYet: 'No runs yet',
      waitingRoblox: 'Waiting for Roblox',
      launchRoblox: "Launch Roblox, it'll dock in automatically"
    },
    taskQueue: {
      title: 'Task Queue',
      subtitle: 'Order of runs to execute',
      noTasks: 'No tasks in queue. Click "+ Add Task" to get started.',
      taskName: 'Task Name',
      repeatCount: 'Repeat Count',
      selectMap: 'Select Map',
      selectStage: 'Select Stage',
      selectMode: 'Select Mode',
      selectDifficulty: 'Select Difficulty',
      selectMacro: 'Select Macro'
    },
    macroManager: {
      title: 'Macro Manager',
      subtitle: 'Create and edit automated action sequences',
      macroName: 'Macro Name',
      blocks: 'Action Blocks',
      noBlocks: 'No blocks in this phase yet.',
      addAttack: 'Attack',
      addPlacement: 'Place Unit',
      addUpgrade: 'Upgrade Unit',
      addWalkPath: 'Walk Path',
      addWait: 'Wait (ms)',
      addKeypress: 'Keypress',
      addReset: 'Reset Character'
    },
    challenge: {
      title: 'Challenge System',
      subtitle: 'Automatically switch to challenge runs at set intervals',
      enableChallenge: 'Enable Challenge Runs',
      enableChallengeDesc: 'Automatically interrupts current queue to complete challenge stages when active.',
      timerInterval: 'Timer Interval (Minutes)',
      priority: 'Priority Level',
      autoClaim: 'Auto-Claim Challenge Rewards'
    },
    hotkeys: {
      title: 'Hotkeys',
      subtitle: 'Keyboard shortcuts for macro controls',
      startStop: 'Start / Stop Macro',
      pauseResume: 'Pause / Resume Macro',
      compactMode: 'Toggle Compact Strip (F7)'
    },
    webhook: {
      title: 'Discord Webhook',
      subtitle: 'Send real-time updates and screenshots to your Discord channel',
      urlLabel: 'Webhook URL',
      urlPlaceholder: 'https://discord.com/api/webhooks/...',
      enableWebhook: 'Enable Webhook Notifications',
      sendOnWin: 'Send on Victory',
      sendOnLoss: 'Send on Defeat',
      sendOnChallenge: 'Send on Challenge Complete',
      sendOnError: 'Send on Macro Error',
      attachScreenshot: 'Attach Game Screenshot'
    },
    settings: {
      title: 'Settings',
      language: 'Language',
      languageDesc: 'Select application interface language.',
      languageEnglish: 'English',
      languagePortuguese: 'Português do Brasil',
      startMinimized: 'Start Minimized',
      startMinimizedDesc: 'Launch minimized to the taskbar.',
      autoReopen: 'Auto-Reopen Roblox',
      autoReopenDesc: 'If Roblox closes or crashes mid-run, reopen the game automatically.',
      background: 'Background Theme',
      accent: 'Accent Color',
      thresholds: 'Sensitivity Thresholds',
      cutoutMode: 'Game Cutout Mode',
      wgcCapture: 'WGC Capture (Windows Graphics Capture)',
      flickerFree: 'Flicker-Free Window Capture'
    },
    status: {
      running: 'Running',
      stopped: 'Stopped',
      paused: 'Paused',
      idle: 'Idle',
      waiting: 'Waiting for Roblox...'
    },
    notifications: {
      profileSaved: 'Profile saved successfully',
      settingsLoaded: 'Settings loaded',
      languageChanged: 'Language updated to {lang}'
    },
    errors: {
      languageSaveFailed: 'Failed to save language setting',
      startFailed: 'Could not start macro',
      unsupportedLanguage: 'Unsupported language requested',
      persistenceFailed: 'Failed to persist settings'
    },
    messages: {
      translationUnavailable: 'Text unavailable'
    }
  },
  'pt-BR': {
    buttons: {
      start: 'Iniciar',
      stop: 'Parar',
      pause: 'Pausar',
      resume: 'Retomar',
      import: 'Importar',
      export: 'Exportar',
      save: 'Salvar',
      cancel: 'Cancelar',
      reset: 'Redefinir para Padrão',
      apply: 'Aplicar',
      popOut: 'Destacar',
      clear: 'Limpar',
      addTask: '+ Nova Tarefa',
      skip: 'Pular',
      presets: 'Modelos Prontos',
      addBlock: '+ Adicionar Bloco',
      record: 'Gravar',
      test: 'Testar Macro',
      delete: 'Excluir',
      edit: 'Editar',
      close: 'Fechar',
      sendTest: 'Enviar Notificação de Teste',
      toggleOn: 'Ativado',
      toggleOff: 'Desativado'
    },
    tabs: {
      general: 'Geral',
      settings: 'Configurações',
      dashboard: 'Painel',
      task: 'Fila de Tarefas',
      creation: 'Gerenciador de Macros',
      challenge: 'Desafio',
      hotkeys: 'Atalhos',
      webhook: 'Webhook do Discord',
      debug: 'Depuração e Testes',
      prestart: 'Fase Pré-Início',
      battle: 'Fase de Batalha'
    },
    header: {
      session: 'Sessão',
      allTime: 'Total Geral',
      openSourceSecurity: 'Segurança Open-Source e Falsos Positivos:'
    },
    dashboard: {
      processLog: 'Log de Processos',
      waitingStart: '> Aguardando início da macro...',
      statusReadout: 'Leitura de Status',
      action: 'Ação',
      currentTask: 'Tarefa Atual',
      repeat: 'Repetição',
      map: 'Mapa',
      lastRun: 'Última Execução',
      runsPerHour: 'Partidas / Hora',
      timeUntilChallenge: 'Tempo até o Desafio',
      mode: 'Modo',
      stage: 'Fase',
      difficulty: 'Dificuldade',
      playMode: 'Modo de Jogo',
      macro: 'Macro',
      scoreboard: 'Placar',
      wins: 'Vitórias',
      winRate: 'Taxa de Vitória',
      losses: 'Derrotas',
      totalRuns: 'partidas no total',
      lifetimeRecord: 'histórico geral',
      controls: 'Controles',
      runHistory: 'Histórico de Execuções',
      noRunsYet: 'Nenhuma partida ainda',
      waitingRoblox: 'Aguardando o Roblox',
      launchRoblox: 'Abra o Roblox, ele se encaixará automaticamente'
    },
    taskQueue: {
      title: 'Fila de Tarefas',
      subtitle: 'Ordem de execução das partidas',
      noTasks: 'Nenhuma tarefa na fila. Clique em "+ Nova Tarefa" para começar.',
      taskName: 'Nome da Tarefa',
      repeatCount: 'Quantidade de Repetições',
      selectMap: 'Selecionar Mapa',
      selectStage: 'Selecionar Fase',
      selectMode: 'Selecionar Modo',
      selectDifficulty: 'Selecionar Dificuldade',
      selectMacro: 'Selecionar Macro'
    },
    macroManager: {
      title: 'Gerenciador de Macros',
      subtitle: 'Crie e edite sequências de ações automatizadas',
      macroName: 'Nome da Macro',
      blocks: 'Blocos de Ação',
      noBlocks: 'Nenhum bloco nesta fase ainda.',
      addAttack: 'Ataque',
      addPlacement: 'Posicionar Unidade',
      addUpgrade: 'Melhorar Unidade',
      addWalkPath: 'Caminho de Andar',
      addWait: 'Aguardar (ms)',
      addKeypress: 'Pressionar Tecla',
      addReset: 'Resetar Personagem'
    },
    challenge: {
      title: 'Sistema de Desafios',
      subtitle: 'Alterne automaticamente para partidas de desafio em intervalos definidos',
      enableChallenge: 'Ativar Partidas de Desafio',
      enableChallengeDesc: 'Interrompe a fila atual automaticamente para concluir fases de desafio quando ativas.',
      timerInterval: 'Intervalo do Temporizador (Minutos)',
      priority: 'Nível de Prioridade',
      autoClaim: 'Coletar Recompensas do Desafio Automaticamente'
    },
    hotkeys: {
      title: 'Atalhos de Teclado',
      subtitle: 'Atalhos para controlar a macro rapidamente',
      startStop: 'Iniciar / Parar Macro',
      pauseResume: 'Pausar / Retomar Macro',
      compactMode: 'Alternar Barra Compacta (F7)'
    },
    webhook: {
      title: 'Webhook do Discord',
      subtitle: 'Envie atualizações e capturas de tela em tempo real para seu canal do Discord',
      urlLabel: 'URL do Webhook',
      urlPlaceholder: 'https://discord.com/api/webhooks/...',
      enableWebhook: 'Ativar Notificações via Webhook',
      sendOnWin: 'Enviar em caso de Vitória',
      sendOnLoss: 'Enviar em caso de Derrota',
      sendOnChallenge: 'Enviar ao Concluir Desafio',
      sendOnError: 'Enviar em caso de Erro na Macro',
      attachScreenshot: 'Anexar Captura de Tela do Jogo'
    },
    settings: {
      title: 'Configurações',
      language: 'Idioma',
      languageDesc: 'Selecione o idioma da interface da aplicação.',
      languageEnglish: 'English',
      languagePortuguese: 'Português do Brasil',
      startMinimized: 'Iniciar Minimizado',
      startMinimizedDesc: 'Iniciar minimizado na barra de tarefas.',
      autoReopen: 'Reabrir Roblox Automaticamente',
      autoReopenDesc: 'Se o Roblox fechar ou falhar durante a execução, reabre o jogo automaticamente.',
      background: 'Tema de Fundo',
      accent: 'Cor de Destaque',
      thresholds: 'Limiares de Sensibilidade',
      cutoutMode: 'Modo Recorte de Jogo (Cutout)',
      wgcCapture: 'Captura WGC (Windows Graphics Capture)',
      flickerFree: 'Captura de Janela Sem Cintilação'
    },
    status: {
      running: 'Executando',
      stopped: 'Parado',
      paused: 'Pausado',
      idle: 'Inativo',
      waiting: 'Aguardando o Roblox...'
    },
    notifications: {
      profileSaved: 'Perfil salvo com sucesso',
      settingsLoaded: 'Configurações carregadas',
      languageChanged: 'Idioma alterado para {lang}'
    },
    errors: {
      languageSaveFailed: 'Falha ao salvar a configuração de idioma',
      startFailed: 'Não foi possível iniciar a macro',
      unsupportedLanguage: 'Idioma solicitado não suportado',
      persistenceFailed: 'Falha ao salvar as configurações'
    },
    messages: {
      translationUnavailable: 'Texto indisponível'
    }
  }
};

// Idiomas suportados pelo sistema
const SUPPORTED_LANGUAGES = new Set(['en', 'pt-BR']);

// Idioma padrão do sistema
const DEFAULT_LANGUAGE = 'en';

// Atributos permitidos para data-i18n-attr (Allowlist estrita)
const ALLOWED_I18N_ATTRS = new Set(['placeholder', 'title', 'aria-label', 'data-tooltip']);

// Propriedades perigosas a rejeitar no getTranslationValue
const DANGEROUS_KEYS = new Set(['__proto__', 'prototype', 'constructor']);

// Idioma ativo no momento
let currentLanguage = DEFAULT_LANGUAGE;

// Token de controle para evitar condições de corrida em requisições assíncronas de troca de idioma
let requestSequenceToken = 0;

// Flag de inicialização idempotente
let isInitialized = false;

/**
 * Normaliza a string de idioma para um formato suportado ('en' ou 'pt-BR').
 * @param {string} language - Código do idioma a ser normalizado.
 * @returns {string} Código do idioma suportado ou o padrão ('en').
 */
function normalizeLanguage(language) {
  if (!language || typeof language !== 'string') {
    return DEFAULT_LANGUAGE;
  }
  const clean = language.trim();
  if (clean === 'pt' || clean === 'pt-br' || clean === 'pt_BR' || clean.toLowerCase().startsWith('pt')) {
    return 'pt-BR';
  }
  if (clean === 'en' || clean === 'en-US' || clean === 'en_US' || clean.toLowerCase().startsWith('en')) {
    return 'en';
  }
  return SUPPORTED_LANGUAGES.has(clean) ? clean : DEFAULT_LANGUAGE;
}

/**
 * Obtém o valor de tradução no dicionário do idioma especificado.
 * Suporta navegação em propriedades aninhadas ('buttons.start') e chaves diretas.
 * Bloqueia propriedades perigosas como __proto__, prototype, constructor.
 * @param {string} language - Idioma a pesquisar.
 * @param {string} key - Chave da tradução.
 * @returns {string|null} Texto traduzido ou null se não for uma string válida e não-vazia.
 */
function getTranslationValue(language, key) {
  if (!TRANSLATIONS[language] || !key || typeof key !== 'string') return null;
  const dict = TRANSLATIONS[language];

  // Verifica chave exata direta
  if (Object.prototype.hasOwnProperty.call(dict, key)) {
    const val = dict[key];
    return typeof val === 'string' && val.trim().length > 0 ? val : null;
  }

  // Navega em objetos aninhados (ex: dict.buttons.start)
  const parts = key.split('.');
  let current = dict;
  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    if (DANGEROUS_KEYS.has(part)) {
      return null;
    }
    if (!current || typeof current !== 'object' || !Object.prototype.hasOwnProperty.call(current, part)) {
      return null;
    }
    current = current[part];
  }

  return typeof current === 'string' && current.trim().length > 0 ? current : null;
}

/**
 * Verifica se a chave possui tradução cadastrada e válida para o idioma informado.
 * @param {string} language - Código do idioma.
 * @param {string} key - Chave da tradução.
 * @returns {boolean} True se a tradução existir e for válida.
 */
function hasTranslation(language, key) {
  const norm = normalizeLanguage(language);
  return getTranslationValue(norm, key) !== null;
}

/**
 * Retorna o texto traduzido para a chave informada no idioma atual.
 * Trata fallbacks para idioma padrão e fallbackText customizado.
 * NUNCA retorna a chave crua.
 * @param {string} key - Chave da tradução.
 * @param {string} [fallbackText=''] - Texto alternativo se a tradução não existir.
 * @returns {string} Texto traduzido final.
 */
function t(key, fallbackText = '') {
  let translated = getTranslationValue(currentLanguage, key);

  if (translated !== null) {
    return translated;
  }

  // Fallback 1: Se a chave não existir no idioma atual, tenta o idioma padrão ('en')
  if (currentLanguage !== DEFAULT_LANGUAGE) {
    translated = getTranslationValue(DEFAULT_LANGUAGE, key);
    if (translated !== null) {
      return translated;
    }
  }

  // Fallback 2: Se houver fallbackText fornecido e válido, utiliza-o
  if (fallbackText && typeof fallbackText === 'string' && fallbackText.trim() !== '') {
    return fallbackText;
  }

  // Fallback 3: Mensagem genérica legível (NUNCA a chave crua)
  return currentLanguage === 'pt-BR' ? 'Texto indisponível' : 'Text unavailable';
}

/**
 * Substitui marcadores {name} em um texto pelas variáveis fornecidas no objeto.
 * Preserva 0 e false. Trata null/undefined sem converter em texto visível.
 * @param {string} text - Texto contendo marcadores.
 * @param {Object} [variables={}] - Objeto de pares chave/valor para substituição.
 * @returns {string} Texto interpolado.
 */
function interpolate(text, variables = {}) {
  if (typeof text !== 'string') return '';
  if (!variables || typeof variables !== 'object') return text;

  return text.replace(/\{(\w+)\}/g, (match, paramName) => {
    if (Object.prototype.hasOwnProperty.call(variables, paramName)) {
      const val = variables[paramName];
      if (val !== undefined && val !== null) {
        return String(val);
      }
      return '';
    }
    return '';
  });
}

/**
 * Traduz a chave informada e aplica a interpolação de variáveis.
 * @param {string} key - Chave da tradução.
 * @param {string} [fallbackText=''] - Texto alternativo.
 * @param {Object} [variables={}] - Variáveis para interpolação.
 * @returns {string} Texto final formatado.
 */
function translate(key, fallbackText = '', variables = {}) {
  const text = t(key, fallbackText);
  return interpolate(text, variables);
}

/**
 * Atualiza o seletor de idioma na interface (#languageSelect) para o valor atual.
 */
function updateLanguageSelector() {
  if (typeof document === 'undefined') return;
  const select = document.getElementById('languageSelect');
  if (select) {
    select.value = currentLanguage;
  }
}

/**
 * Aplica as traduções a todos os elementos HTML com o atributo [data-i18n].
 * Preserva fallbacks originais do HTML em atributos data-i18n-original.
 * @param {string} [language=currentLanguage] - Idioma a ser aplicado.
 */
function applyTranslations(language = currentLanguage) {
  if (typeof document === 'undefined') return;
  currentLanguage = normalizeLanguage(language);
  if (document.documentElement) {
    document.documentElement.lang = currentLanguage;
  }

  const elements = document.querySelectorAll('[data-i18n]');
  elements.forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (!key) return;

    const attrTarget = el.getAttribute('data-i18n-attr');

    if (attrTarget) {
      const attrs = attrTarget.split(',').map((a) => a.trim());
      attrs.forEach((attr) => {
        // Allowlist estrita de atributos permitidos
        if (!ALLOWED_I18N_ATTRS.has(attr)) {
          console.warn(`[i18n] Rejected unallowed attribute translation target: "${attr}"`);
          return;
        }
        const origKey = `data-i18n-original-${attr}`;
        if (!el.hasAttribute(origKey)) {
          el.setAttribute(origKey, el.getAttribute(attr) || '');
        }
        const origVal = el.getAttribute(origKey);
        const translatedVal = t(key, origVal);
        el.setAttribute(attr, translatedVal);
      });
    } else {
      // Para nós de texto: salva o texto original UMA ÚNICA VEZ
      if (!el.hasAttribute('data-i18n-original')) {
        el.setAttribute('data-i18n-original', el.textContent.trim());
      }
      const origText = el.getAttribute('data-i18n-original');
      el.textContent = t(key, origText);
    }
  });

  updateLanguageSelector();
}

/**
 * Carrega de forma assíncrona o idioma salvo via API do pywebview.
 */
async function loadSavedLanguage() {
  try {
    if (typeof window !== 'undefined' && window.pywebview && window.pywebview.api && typeof window.pywebview.api.get_language === 'function') {
      const savedLang = await window.pywebview.api.get_language();
      if (savedLang) {
        applyTranslations(savedLang);
      }
    }
  } catch (err) {
    console.error('[i18n] Error loading saved language:', err);
    applyTranslations(DEFAULT_LANGUAGE);
  }
}

/**
 * Manipula a alteração de idioma no elemento select e persiste a escolha no backend.
 * Previne condições de corrida com token de sequência.
 * @param {Event} event - Evento de alteração do select.
 */
async function handleLanguageChange(event) {
  const selectedLang = event && event.target ? event.target.value : (document.getElementById('languageSelect')?.value || currentLanguage);
  
  const currentToken = ++requestSequenceToken;
  const previousLang = currentLanguage;

  applyTranslations(selectedLang);

  try {
    if (typeof window !== 'undefined' && window.pywebview && window.pywebview.api && typeof window.pywebview.api.set_language === 'function') {
      const res = await window.pywebview.api.set_language(currentLanguage);
      if (currentToken !== requestSequenceToken) {
        // Requisição obsoleta devido a nova troca rápida de idioma
        return;
      }
      if (!res || res.success === false) {
        throw new Error((res && res.error) || 'Backend rejected language save');
      }
    }
  } catch (err) {
    if (currentToken !== requestSequenceToken) return;
    console.error('[i18n] Error persisting language setting:', err);
    // Reverte a seleção do seletor e a interface para o último estado válido salvo
    applyTranslations(previousLang);
    if (typeof window !== 'undefined' && window.addLog) {
      window.addLog(t('errors.languageSaveFailed', 'Failed to save language setting'), 'error');
    }
  }
}

/**
 * Inicialização idempotente do módulo i18n.
 */
function init() {
  if (isInitialized) return;
  isInitialized = true;

  applyTranslations();
  loadSavedLanguage();

  if (typeof document !== 'undefined') {
    const select = document.getElementById('languageSelect');
    if (select && typeof select.addEventListener === 'function') {
      if (typeof select.removeEventListener === 'function') {
        select.removeEventListener('change', handleLanguageChange);
      }
      select.addEventListener('change', handleLanguageChange);
    }
  }
}

// Exportação global da API I18n
if (typeof window !== 'undefined') {
  window.I18n = {
    t,
    translate,
    interpolate,
    applyTranslations,
    getCurrentLanguage: () => currentLanguage,
    isSupportedLanguage: (lang) => SUPPORTED_LANGUAGES.has(lang),
    loadSavedLanguage,
    handleLanguageChange,
    init,
    TRANSLATIONS
  };
}
