import './styles.css';

const API_BASE = (import.meta.env.VITE_API_BASE || window.location.origin).replace(/\/$/, '');
const WS_BASE = API_BASE.replace(/^http/, 'ws');
const app = document.querySelector('#app');
const monitoredTasks = new Map();

app.innerHTML = `
  <section class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">AGENTE KÁIROS · CENTRAL MULTIMÍDIA</p>
        <h1>KAIR-S-SONICA</h1>
        <p class="lede">Crie artefatos de áudio e vídeo e acompanhe cada tarefa em tempo real, sem perder o pulso do pipeline.</p>
      </div>
      <div class="hero-orbit" aria-hidden="true"><span></span><span></span><span></span></div>
    </header>

    <section class="card autoreview-card" aria-labelledby="autoreview-title">
      <div class="section-head">
        <div><p class="eyebrow">AUTO-REVIEW / PHD GATE</p><h2 id="autoreview-title">Pré-auditoria antes da produção</h2></div>
        <span id="autoreview-status" class="chip chip-armed">ARMADO</span>
      </div>
      <p class="studio-subtitle">Toda solicitação passa por identidade, voz, música, vídeo, proveniência e continuidade antes de entrar no worker. Falhas críticas bloqueiam; apenas ajustes técnicos seguros podem ser aplicados automaticamente.</p>
      <div class="autoreview-grid">
        <div><span class="autoreview-label">POLÍTICA</span><strong id="autoreview-policy">KTD · identidade imutável</strong></div>
        <div><span class="autoreview-label">ÚLTIMA AUDITORIA</span><strong id="autoreview-audit">Aguardando solicitação</strong></div>
        <div><span class="autoreview-label">REPAROS</span><strong id="autoreview-repairs">Nenhum</strong></div>
      </div>
      <div id="autoreview-output" class="autoreview-output"><span>O resultado do preflight aparecerá aqui antes de qualquer execução.</span></div>
    </section>

    <div class="layout-grid">
      <form id="generate-form" class="card composer-card">
        <div class="section-head">
          <div><p class="eyebrow">COMPOSER</p><h2>Iniciar pipeline</h2></div>
          <span class="chip">CPU / DEMO</span>
        </div>
        <label>Prompt musical<input name="prompt" value="Trap Soul noturno, groove atrás do tempo" required /></label>
        <div class="grid">
          <label>Gênero<input name="genre" value="Trap Soul" /></label>
          <label>BPM<input name="bpm" type="number" min="40" max="240" value="140" /></label>
          <label>Tonalidade<input name="key" value="C#" /></label>
          <label>Escala<select name="scale"><option value="minor">Menor</option><option value="major">Maior</option></select></label>
        </div>
        <label>Letra opcional<textarea name="lyrics" rows="3" placeholder="Escreva uma ideia lírica..."></textarea></label>
        <div class="grid">
          <label>Duração (s)<input name="duration_seconds" type="number" min="1" max="120" value="8" /></label>
          <label>Swing<input name="swing" type="number" min="0.5" max="0.67" step="0.01" value="0.60" /></label>
          <label>Formato<select name="output_format"><option value="wav">WAV</option><option value="mp3">MP3 320 kbps</option></select></label>
        </div>
        <button type="submit">Iniciar pipeline</button>
        <div id="submit-feedback" class="feedback" aria-live="polite"></div>
      </form>

      <section class="card monitor-card" aria-labelledby="monitor-title">
        <div class="section-head">
          <div><p class="eyebrow">LIVE OPS</p><h2 id="monitor-title">Streams em tempo real</h2></div>
          <span id="socket-health" class="health-badge"><i></i> aguardando</span>
        </div>
        <form id="watch-form" class="watch-form">
          <input id="task-ids" placeholder="Cole um ou mais task IDs separados por vírgula" aria-label="IDs de tarefas" />
          <button type="submit" class="button-secondary">Acompanhar</button>
        </form>
        <div id="tasks-grid" class="tasks-grid">
          <div class="empty-state">Nenhuma tarefa acompanhada. Inicie um pipeline ou cole um task ID acima.</div>
        </div>
      </section>

      <form id="video-form" class="card composer-card video-card">
        <div class="section-head">
          <div><p class="eyebrow">VIDEO LAB</p><h2>Produzir vídeo generativo</h2></div>
          <span class="chip">SKYREELS · GPU</span>
        </div>
        <label>Direção audiovisual<textarea name="prompt" rows="3" required>Cinematic live-action editorial rap video, continuous camera movement, rain, water, vapor and practical amber light, no text, no logo, no watermark.</textarea></label>
        <div class="grid">
          <label>Modo<select name="mode"><option value="t2v">Texto → vídeo</option><option value="i2v">Keyframe → vídeo</option><option value="extend">Extensão de vídeo</option><option value="start_end">Frame inicial → frame final</option></select></label>
          <label>Engine<select name="engine"><option value="diffusion_forcing">Diffusion Forcing</option><option value="standard">Standard T2V/I2V</option></select></label>
          <label>Backend<select name="backend"><option value="native">API nativa Diffusers</option><option value="cli">CLI SkyReels</option></select></label>
          <label>Resolução<select name="resolution"><option value="540P">540P</option><option value="720P">720P</option></select></label>
          <label>Frames<input name="num_frames" type="number" min="1" max="1457" placeholder="97 / 121" /></label>
          <label>FPS<input name="fps" type="number" min="1" max="120" value="24" /></label>
          <label>Seed<input name="seed" type="number" min="0" max="4294967294" placeholder="opcional" /></label>
        </div>
        <div class="grid">
          <label>Imagem / keyframe<input name="image_path" placeholder="arquivo em data/uploads" /></label>
          <label>Frame final<input name="end_image_path" placeholder="necessário em start/end" /></label>
          <label>Vídeo prefixo<input name="video_path" placeholder="necessário em extensão" /></label>
          <label>Passos<input name="inference_steps" type="number" min="1" max="200" value="30" /></label>
        </div>
        <p class="form-note">As referências devem estar montadas em <code>data/uploads</code> ou <code>data/output</code>. O checkpoint e a GPU são configurados no worker de produção.</p>
        <button type="submit">Enfileirar vídeo</button>
        <div id="video-feedback" class="feedback" aria-live="polite"></div>
      </form>
    </div>

    <section id="recording-studio" class="card studio-card" aria-labelledby="studio-title">
      <div class="section-head">
        <div><p class="eyebrow">RECORDING / MIXING STUDIO</p><h2 id="studio-title">Estúdio do DJ / Produtor Káiros</h2><p class="studio-subtitle">Capture takes, organize camadas e faça um bounce de referência direto no navegador.</p></div>
        <span id="studio-health" class="health-badge"><i></i> pronto</span>
      </div>
      <div class="studio-toolbar">
        <div class="transport-group" aria-label="Controles de transporte">
          <button id="record-toggle" class="transport-button record-button" type="button"><span class="transport-dot"></span> Gravar</button>
          <button id="play-toggle" class="transport-button" type="button">▶ Reproduzir mix</button>
          <button id="stop-mix" class="transport-button button-secondary" type="button">■ Parar</button>
          <button id="clear-studio" class="transport-button button-secondary" type="button">Limpar sessão</button>
        </div>
        <div class="studio-clock"><span id="studio-time">00:00.000</span><span id="studio-sample-rate">48 kHz · estéreo</span></div>
      </div>
      <div class="studio-main-grid">
        <div class="studio-console">
          <div class="waveform-shell">
            <canvas id="studio-waveform" width="1200" height="180" aria-label="Visualização do nível de áudio"></canvas>
            <div class="waveform-label"><span>INPUT MONITOR</span><span id="studio-input-label">microfone não iniciado</span></div>
          </div>
          <div class="studio-input-row">
            <label>Nome do take<input id="take-name" value="Káiros Take 01" maxlength="80" /></label>
            <label>Entrada<select id="input-device"><option value="default">Microfone padrão do sistema</option></select></label>
            <label>Formato<select id="record-format"><option value="audio/webm;codecs=opus">WebM / Opus</option><option value="audio/webm">WebM</option></select></label>
          </div>
          <div class="studio-actions">
            <label class="upload-button"><input id="take-upload" type="file" accept="audio/*" /> Importar take</label>
            <button id="bounce-mix" type="button">Exportar bounce WAV</button>
            <span id="studio-feedback" class="feedback" aria-live="polite">Nenhum take carregado.</span>
          </div>
          <div class="studio-handoff-panel">
            <div class="tracks-head"><div><p class="eyebrow">EXPLICIT HANDOFF</p><h3>Enviar take ao pipeline Káiros</h3></div><span id="studio-handoff-status" class="chip">local por padrão</span></div>
            <p class="studio-subtitle">O envio é manual, autenticado e separado da gravação. O token não é armazenado pelo navegador.</p>
            <div class="studio-handoff-grid">
              <label>Token do estúdio<input id="studio-upload-token" type="password" autocomplete="off" placeholder="Bearer configurado no backend" /></label>
              <label class="toggle-control"><span>Gerar nova base após análise</span><input id="studio-generate-audio" type="checkbox" /></label>
              <button id="studio-upload-handoff" class="button-secondary" type="button">Enviar take ativo</button>
            </div>
            <div id="studio-handoff-feedback" class="feedback" aria-live="polite">Nenhum take foi enviado ao backend.</div>
          </div>
        </div>
        <aside class="studio-meter-card" aria-label="Medição de áudio">
          <p class="eyebrow">MASTER BUS</p>
          <div class="meter-stack"><span class="meter-scale">0</span><div class="meter-track"><span id="master-meter"></span></div><span class="meter-scale">-24</span><span class="meter-scale">-48</span></div>
          <div class="master-readout"><strong id="master-db">-∞ dB</strong><span>peak hold</span></div>
          <div class="studio-note">O áudio capturado permanece local no navegador até você exportar o bounce. Nenhuma gravação é enviada automaticamente.</div>
        </aside>
      </div>
      <div class="tracks-head"><div><p class="eyebrow">SESSION TRACKS</p><h3>Camadas da sessão</h3></div><span id="track-count" class="chip">0 takes</span></div>
      <div id="studio-tracks" class="studio-tracks"><div class="empty-state">Grave ou importe um take para começar a mixagem.</div></div>
      <div class="island-panel">
        <div class="tracks-head"><div><p class="eyebrow">SKILL CHAIN / ATLAS</p><h3>Ilha de Produção Artística</h3></div><span id="island-status" class="chip">plan-first</span></div>
        <div class="island-grid">
          <label>Instrumento<select id="island-instrument"><option value="lead_vocal">Carregando Atlas…</option></select></label>
          <label>Contexto<select id="island-context"><option value="music">Música</option><option value="vocal">Vocal</option><option value="beat">Beat</option><option value="cinematic">Cinemático</option><option value="orchestra">Orquestra</option></select></label>
          <label>Referência / preset<input id="island-reference" placeholder="opcional: ref-001" maxlength="160" /></label>
          <button id="island-plan" type="button">Gerar cadeia sugerida</button>
        </div>
        <div id="island-chain" class="island-chain"><div class="empty-state">Escolha um instrumento para visualizar a cadeia de processamento.</div></div>
      </div>
      <div class="studio-master-panel">
        <div class="tracks-head"><div><p class="eyebrow">STUDIOMASTER / GROOVE INTELLIGENCE</p><h3>Command deck responsivo</h3></div><span id="studio-master-status" class="chip">offline</span></div>
        <p class="studio-subtitle">Faça a base respirar com o flow: primeiro analise o take, depois aprove o plano e ajuste o pocket ao vivo.</p>
        <div class="studio-master-grid">
          <label>Família de produção<select id="studio-master-style"><option value="boom_bap">Boom bap</option><option value="brazilian_funk_heavy">Funk brasileiro pesado</option><option value="brazilian_funk_swing">Funk brasileiro suingado</option><option value="vocal_focus">Foco vocal</option></select></label>
          <label>Padrão canônico<select id="studio-master-canon"><option value="">Selecionando cânone…</option></select></label>
          <label>BPM<input id="studio-master-bpm" type="number" min="40" max="240" value="140" /></label>
          <label>Swing ratio<input id="studio-master-swing" type="number" min="0.5" max="0.67" step="0.01" value="0.60" /></label>
          <label class="toggle-control"><span>Grid follow</span><input id="studio-master-grid-follow" type="checkbox" checked /></label>
          <button id="studio-master-analyze" type="button">Analisar take ativo</button>
          <button id="studio-master-plan" class="button-secondary" type="button">Gerar plano responsivo</button>
        </div>
        <div class="performance-deck">
          <div><p class="eyebrow">LIVE PERFORMANCE</p><strong id="studio-master-pocket">Pocket aguardando análise</strong><span id="studio-master-flow-note">Nenhum mapa de flow carregado.</span></div>
          <div class="performance-actions"><button id="studio-master-boost" class="performance-button" type="button">Boost punchline</button><button id="studio-master-push" class="performance-button" type="button">Propor ao cânone</button></div>
        </div>
        <div id="studio-master-plan-view" class="studio-master-plan"><div class="empty-state">O plano responsivo aprovado aparecerá aqui. Nenhuma alteração automática será enviada ao worker.</div></div>
        <div class="studio-master-2-panel">
          <div class="tracks-head"><div><p class="eyebrow">STUDIOMASTER 2.0 / CONTROL ROOM</p><h3>Arquitetura, assinatura e lançamento</h3></div><span id="studio-master-2-status" class="chip">aguardando</span></div>
          <p class="studio-subtitle">Transforme a ideia em proposta de arranjo, expressão e distribuição sem ocultar a revisão do operador.</p>
          <div class="studio-master-2-grid">
            <label>Humor do arranjo<select id="studio-arrangement-mood"><option value="energetic">Energético</option><option value="focused">Focado</option><option value="reflective">Reflexivo</option><option value="cinematic">Cinemático</option></select></label>
            <label>Barras<input id="studio-arrangement-bars" type="number" min="4" max="256" value="32" /></label>
            <label>Intensidade Káiros<input id="studio-signature-intensity" type="range" min="0" max="1" step="0.01" value="0.65" /></label>
            <label>Destino do Modo Káiros<select id="studio-signature-target"><option value="audio_input">Áudio importado</option><option value="mix_bus">Mix bus</option><option value="vocal_bus">Vocal bus</option></select></label>
          </div>
          <div class="studio-master-2-actions">
            <button id="studio-arrangement-plan" type="button">Propor arranjo</button>
            <button id="studio-signature-plan" class="button-secondary" type="button">Propor Modo Káiros</button>
            <button id="studio-viral-plan" class="button-secondary" type="button">Planejar clip 15s</button>
          </div>
          <div class="studio-master-2-readouts">
            <article><span class="eyebrow">ANALYTICS</span><strong id="studio-analytics-readout">histórico vazio</strong><p id="studio-analytics-note">Nenhuma produção registrada no caminho configurado.</p></article>
            <article><span class="eyebrow">AUTO-RETRAINING</span><strong id="studio-retraining-readout">desligado</strong><p id="studio-retraining-note">Aguardando manifesto e aprovação.</p></article>
          </div>
          <div id="studio-master-2-output" class="studio-master-plan"><div class="empty-state">As propostas 2.0 aparecerão aqui e nunca publicarão ou treinarão automaticamente.</div></div>
          <div class="real-adapters-panel">
            <div class="tracks-head"><div><p class="eyebrow">REAL ADAPTERS / PREFLIGHT</p><h3>Capacidades licenciadas</h3></div><span id="studio-real-adapters-status" class="chip">carregando</span></div>
            <p class="studio-subtitle">A presença do pacote não habilita execução: cada adapter precisa de gate, allowlist, licença aceita e manifesto de artefato quando aplicável.</p>
            <div class="real-adapters-toolbar"><button id="studio-real-adapters-refresh" class="button-secondary" type="button">Atualizar preflight</button><span id="studio-real-adapters-gate">gate global desligado</span></div>
            <div id="studio-real-adapters-grid" class="real-adapters-grid"><div class="empty-state">Lendo capabilities do gateway…</div></div>
          </div>
          <div class="frontier-panel">
            <div class="tracks-head"><div><p class="eyebrow">FRONTIER / PHD HARNESS</p><h3>Arquitetura audiovisual de última onda</h3></div><span id="frontier-status" class="chip">preflight</span></div>
            <p class="studio-subtitle">Preflight, Handoff e Determinism: WebCodecs, WebGPU, áudio reativo e adapters generativos opcionais com fallback explícito.</p>
            <div class="frontier-grid">
              <label>Perfil<select id="frontier-profile"><option value="audio_reactive_video">Vídeo audio-reactive</option><option value="music_video">Videoclipe</option><option value="live_capture">Performance ao vivo</option><option value="release_preflight">Preflight de lançamento</option></select></label>
              <label>Computação<select id="frontier-compute"><option value="auto">Auto / fallback seguro</option><option value="webgpu">WebGPU</option><option value="cuda">CUDA</option><option value="cpu">CPU determinística</option></select></label>
              <label>Vídeo<select id="frontier-video-backend"><option value="browser_webcodecs">Browser · WebCodecs</option><option value="ltx2_optional">LTX-2 · opcional</option><option value="skyreels_optional">SkyReels · opcional</option></select></label>
              <label>FPS<input id="frontier-fps" type="number" min="1" max="120" value="24" /></label>
              <button id="frontier-plan" type="button">Gerar plano PHD</button>
            </div>
            <div class="frontier-readouts"><span id="frontier-components">Lendo capabilities…</span><span id="frontier-gates">Aprovação humana obrigatória</span></div>
            <div id="frontier-output" class="studio-master-plan"><div class="empty-state">O plano frontier aparecerá aqui como proposta revisável.</div></div>
          </div>
        </div>
      </div>
    </section>

    <section id="status" class="card status" aria-live="polite">
      <p class="eyebrow">LAST EVENT</p><p>Aguardando uma solicitação.</p>
    </section>
  </section>`;

const status = document.querySelector('#status');
const form = document.querySelector('#generate-form');
const watchForm = document.querySelector('#watch-form');
const taskIdsInput = document.querySelector('#task-ids');
const tasksGrid = document.querySelector('#tasks-grid');
const socketHealth = document.querySelector('#socket-health');
const feedback = document.querySelector('#submit-feedback');
const videoForm = document.querySelector('#video-form');
const videoFeedback = document.querySelector('#video-feedback');
const autoReviewStatus = document.querySelector('#autoreview-status');
const autoReviewAudit = document.querySelector('#autoreview-audit');
const autoReviewRepairs = document.querySelector('#autoreview-repairs');
const autoReviewOutput = document.querySelector('#autoreview-output');
const studio = {
  audioContext: null,
  analyser: null,
  inputStream: null,
  recorder: null,
  recordingStartedAt: 0,
  timer: null,
  animationFrame: null,
  playbackSources: [],
  tracks: [],
  activeTrackId: null,
  remoteAsset: null,
};
const studioWaveform = document.querySelector('#studio-waveform');
const studioWaveformContext = studioWaveform.getContext('2d');
const recordToggle = document.querySelector('#record-toggle');
const playToggle = document.querySelector('#play-toggle');
const stopMix = document.querySelector('#stop-mix');
const clearStudio = document.querySelector('#clear-studio');
const takeName = document.querySelector('#take-name');
const takeUpload = document.querySelector('#take-upload');
const bounceMix = document.querySelector('#bounce-mix');
const studioFeedback = document.querySelector('#studio-feedback');
const studioHandoffStatus = document.querySelector('#studio-handoff-status');
const studioUploadToken = document.querySelector('#studio-upload-token');
const studioGenerateAudio = document.querySelector('#studio-generate-audio');
const studioUploadHandoff = document.querySelector('#studio-upload-handoff');
const studioHandoffFeedback = document.querySelector('#studio-handoff-feedback');
const studioHealth = document.querySelector('#studio-health');
const studioTime = document.querySelector('#studio-time');
const studioTracks = document.querySelector('#studio-tracks');
const trackCount = document.querySelector('#track-count');
const masterMeter = document.querySelector('#master-meter');
const masterDb = document.querySelector('#master-db');
const islandInstrument = document.querySelector('#island-instrument');
const islandContext = document.querySelector('#island-context');
const islandReference = document.querySelector('#island-reference');
const islandPlanButton = document.querySelector('#island-plan');
const islandChain = document.querySelector('#island-chain');
const islandStatus = document.querySelector('#island-status');
const studioMaster = {
  canon: [],
  flow: null,
  plan: null,
  socket: null,
  sessionId: `studio-${crypto.randomUUID()}`,
};
const studioMasterStatus = document.querySelector('#studio-master-status');
const studioMasterStyle = document.querySelector('#studio-master-style');
const studioMasterCanon = document.querySelector('#studio-master-canon');
const studioMasterBpm = document.querySelector('#studio-master-bpm');
const studioMasterSwing = document.querySelector('#studio-master-swing');
const studioMasterGridFollow = document.querySelector('#studio-master-grid-follow');
const studioMasterAnalyze = document.querySelector('#studio-master-analyze');
const studioMasterPlanButton = document.querySelector('#studio-master-plan');
const studioMasterBoost = document.querySelector('#studio-master-boost');
const studioMasterPush = document.querySelector('#studio-master-push');
const studioMasterPocket = document.querySelector('#studio-master-pocket');
const studioMasterFlowNote = document.querySelector('#studio-master-flow-note');
const studioMasterPlanView = document.querySelector('#studio-master-plan-view');
const studioMaster2Status = document.querySelector('#studio-master-2-status');
const studioArrangementMood = document.querySelector('#studio-arrangement-mood');
const studioArrangementBars = document.querySelector('#studio-arrangement-bars');
const studioSignatureIntensity = document.querySelector('#studio-signature-intensity');
const studioSignatureTarget = document.querySelector('#studio-signature-target');
const studioArrangementButton = document.querySelector('#studio-arrangement-plan');
const studioSignatureButton = document.querySelector('#studio-signature-plan');
const studioViralButton = document.querySelector('#studio-viral-plan');
const studioAnalyticsReadout = document.querySelector('#studio-analytics-readout');
const studioAnalyticsNote = document.querySelector('#studio-analytics-note');
const studioRetrainingReadout = document.querySelector('#studio-retraining-readout');
const studioRetrainingNote = document.querySelector('#studio-retraining-note');
const studioMaster2Output = document.querySelector('#studio-master-2-output');
const studioRealAdaptersStatus = document.querySelector('#studio-real-adapters-status');
const studioRealAdaptersGate = document.querySelector('#studio-real-adapters-gate');
const studioRealAdaptersRefresh = document.querySelector('#studio-real-adapters-refresh');
const studioRealAdaptersGrid = document.querySelector('#studio-real-adapters-grid');
const frontierStatus = document.querySelector('#frontier-status');
const frontierProfile = document.querySelector('#frontier-profile');
const frontierCompute = document.querySelector('#frontier-compute');
const frontierVideoBackend = document.querySelector('#frontier-video-backend');
const frontierFps = document.querySelector('#frontier-fps');
const frontierPlanButton = document.querySelector('#frontier-plan');
const frontierComponents = document.querySelector('#frontier-components');
const frontierGates = document.querySelector('#frontier-gates');
const frontierOutput = document.querySelector('#frontier-output');

function renderAutoReview(payload) {
  const audit = payload?.detail?.audit || payload?.audit || payload;
  if (!audit || (!audit.preflight_id && !audit.audit_id && !audit.decision)) return;
  const decision = audit.decision || payload.preflight_decision || 'READY_FOR_APPROVAL';
  const findings = audit.findings || [];
  const roadmap = audit.roadmap || [];
  const repairs = audit.repairs_applied || payload.repairs_applied || [];
  autoReviewStatus.textContent = decision === 'REJECTED' ? 'BLOQUEADO' : decision;
  autoReviewStatus.className = `chip ${decision === 'REJECTED' ? 'chip-blocked' : 'chip-ready'}`;
  autoReviewAudit.textContent = audit.audit_id || payload.preflight_id || 'não persistida';
  autoReviewRepairs.textContent = repairs.length ? `${repairs.length} aplicado(s)` : 'Nenhum';
  const findingMarkup = findings.slice(0, 6).map((item) => `<li class="autoreview-${String(item.severity || 'INFO').toLowerCase()}"><strong>${escapeHtml(item.code)}</strong> ${escapeHtml(item.message)}</li>`).join('');
  const roadmapMarkup = roadmap.slice(0, 6).map((item) => `<li><strong>${escapeHtml(item.priority)}</strong> ${escapeHtml(item.action)} <span>${escapeHtml(item.status)}</span></li>`).join('');
  autoReviewOutput.innerHTML = `<div class="autoreview-result-head"><strong>${escapeHtml(decision)}</strong><span>${repairs.length ? `${repairs.length} reparo(s) seguro(s) aplicado(s)` : 'sem reparos automáticos'}</span></div>${findingMarkup ? `<div><span class="autoreview-label">FINDINGS</span><ul>${findingMarkup}</ul></div>` : ''}${roadmapMarkup ? `<div><span class="autoreview-label">ROADMAP</span><ul>${roadmapMarkup}</ul></div>` : ''}`;
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  })[character]);
}

function setHealth(label, active = false) {
  socketHealth.className = `health-badge${active ? ' active' : ''}`;
  socketHealth.innerHTML = `<i></i> ${escapeHtml(label)}`;
}

function renderTasks() {
  if (!monitoredTasks.size) {
    tasksGrid.innerHTML = '<div class="empty-state">Nenhuma tarefa acompanhada. Inicie um pipeline ou cole um task ID acima.</div>';
    return;
  }
  tasksGrid.innerHTML = [...monitoredTasks.values()].map((snapshot) => {
    const progress = snapshot.progress || {};
    const percent = Math.max(0, Math.min(100, Number(progress.percent || 0)));
    const terminal = ['SUCCEEDED', 'FAILED'].includes(snapshot.status);
    const result = snapshot.result || {};
    const isVideo = Boolean(result.video_url);
    const links = [
      snapshot.artifact_url ? `<a href="${API_BASE}${escapeHtml(snapshot.artifact_url)}" target="_blank" rel="noreferrer">${isVideo ? 'vídeo' : 'áudio'}</a>` : '',
      result.transcript_url ? `<a href="${API_BASE}${escapeHtml(result.transcript_url)}" target="_blank" rel="noreferrer">transcrição</a>` : '',
      result.metadata_url ? `<a href="${API_BASE}${escapeHtml(result.metadata_url)}" target="_blank" rel="noreferrer">metadados</a>` : ''
    ].filter(Boolean).join(' · ');
    return `<article class="task-tile ${escapeHtml(snapshot.status.toLowerCase())}">
      <div class="task-topline"><span class="task-status">${escapeHtml(snapshot.status)}</span><button class="icon-button" data-remove-task="${escapeHtml(snapshot.task_id)}" aria-label="Remover tarefa">×</button></div>
      <code>${escapeHtml(snapshot.task_id)}</code>
      <div class="progress-track"><span style="width:${percent}%"></span></div>
      <div class="task-progress"><strong>${percent}%</strong><span>${escapeHtml(progress.step || 'queued')}</span></div>
      <p class="task-message">${escapeHtml(progress.message || snapshot.error || 'Conectando ao stream...')}</p>
      ${links ? `<div class="task-links">${links}</div>` : ''}
      ${terminal ? '<span class="task-terminal">stream encerrado</span>' : '<span class="task-terminal live">stream conectado</span>'}
    </article>`;
  }).join('');
  tasksGrid.querySelectorAll('[data-remove-task]').forEach((button) => {
    button.addEventListener('click', () => {
      const taskId = button.dataset.removeTask;
      const item = monitoredTasks.get(taskId);
      item?.socket?.close();
      monitoredTasks.delete(taskId);
      renderTasks();
    });
  });
}

function updateTask(snapshot) {
  const item = monitoredTasks.get(snapshot.task_id) || {};
  monitoredTasks.set(snapshot.task_id, { ...item, ...snapshot });
  if (snapshot.status === 'RUNNING') setHealth('stream ativo', true);
  if (['SUCCEEDED', 'FAILED'].includes(snapshot.status)) setHealth('evento recebido', true);
  renderTasks();
  status.innerHTML = `<p class="eyebrow">LAST EVENT · ${escapeHtml(snapshot.task_id)}</p><p>${escapeHtml(snapshot.progress?.message || snapshot.status)}</p>`;
}

async function watchTask(taskId) {
  const cleanId = taskId.trim();
  if (!cleanId || monitoredTasks.has(cleanId)) return;
  monitoredTasks.set(cleanId, { task_id: cleanId, status: 'CONNECTING', progress: { step: 'connecting', percent: 0, message: 'Abrindo snapshot e WebSocket...' } });
  renderTasks();
  try {
    const response = await fetch(`${API_BASE}/v1/tasks/${encodeURIComponent(cleanId)}`);
    if (!response.ok) throw new Error('Tarefa não encontrada');
    updateTask(await response.json());
    const socket = new WebSocket(`${WS_BASE}/ws/tasks/${encodeURIComponent(cleanId)}`);
    monitoredTasks.set(cleanId, { ...monitoredTasks.get(cleanId), socket });
    socket.onopen = () => setHealth('streams ativos', true);
    socket.onmessage = (event) => updateTask(JSON.parse(event.data));
    socket.onerror = () => {
      updateTask({ task_id: cleanId, status: 'FAILED', progress: { step: 'websocket_error', percent: 100, message: 'Falha no canal WebSocket' } });
      setHealth('erro de conexão');
    };
    socket.onclose = () => {
      const item = monitoredTasks.get(cleanId);
      if (item && !['SUCCEEDED', 'FAILED'].includes(item.status)) updateTask({ ...item, status: 'DISCONNECTED', progress: { ...(item.progress || {}), message: 'WebSocket desconectado; consulte o snapshot HTTP' } });
    };
  } catch (error) {
    updateTask({ task_id: cleanId, status: 'FAILED', progress: { step: 'lookup_failed', percent: 100, message: error.message } });
  }
}

watchForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  taskIdsInput.value.split(',').forEach(watchTask);
  taskIdsInput.value = '';
});

tasksGrid.addEventListener('click', (event) => {
  if (event.target.matches('[data-remove-task]')) event.preventDefault();
});

const videoMode = videoForm.elements.mode;
const videoEngine = videoForm.elements.engine;
const videoImage = videoForm.elements.image_path;
const videoEndImage = videoForm.elements.end_image_path;
const videoPath = videoForm.elements.video_path;
const videoBackend = videoForm.elements.backend;
const videoChip = videoForm.querySelector('.chip');

function syncVideoMode() {
  const mode = videoMode.value;
  const isI2V = mode === 'i2v' || mode === 'start_end';
  const isStartEnd = mode === 'start_end';
  const isExtend = mode === 'extend';
  videoImage.required = isI2V;
  videoEndImage.required = isStartEnd;
  videoPath.required = isExtend;
  videoImage.disabled = isExtend;
  videoEndImage.disabled = !isStartEnd;
  videoPath.disabled = !isExtend;
  videoEngine.value = isExtend || isStartEnd ? 'diffusion_forcing' : videoEngine.value;
  videoEngine.disabled = isExtend || isStartEnd;
}

videoMode.addEventListener('change', syncVideoMode);
syncVideoMode();

async function loadVideoCapabilities() {
  try {
    const response = await fetch(`${API_BASE}/v1/video/capabilities`);
    if (!response.ok) throw new Error('capabilities unavailable');
    const payload = await response.json();
    const native = payload.backends?.native;
    const nativeOption = videoBackend.querySelector('option[value="native"]');
    if (nativeOption) {
      nativeOption.disabled = !native?.ready;
      nativeOption.textContent = native?.ready ? 'API nativa Diffusers · pronta' : 'API nativa Diffusers · não pronta';
    }
    if (native?.ready) videoBackend.value = 'native';
    else videoBackend.value = 'cli';
    videoChip.textContent = native?.ready ? 'SKYREELS · NATIVE GPU' : 'SKYREELS · CLI GPU';
  } catch {
    videoBackend.value = 'cli';
    videoChip.textContent = 'SKYREELS · GPU';
  }
}

loadVideoCapabilities();

videoForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const raw = Object.fromEntries(new FormData(videoForm));
  const data = { ...raw };
  for (const field of ['num_frames', 'fps', 'seed', 'inference_steps']) {
    if (data[field] === '') delete data[field];
    else if (data[field] !== undefined) data[field] = Number(data[field]);
  }
  for (const field of ['image_path', 'end_image_path', 'video_path']) {
    if (!data[field]) delete data[field];
  }
  videoFeedback.textContent = 'Enviando pedido de vídeo ao worker GPU...';
  try {
    const response = await fetch(`${API_BASE}/v1/video/generate`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
    const result = await response.json();
    renderAutoReview(result);
    if (!response.ok) { videoFeedback.textContent = 'Falha ao enfileirar vídeo: gate PHD bloqueou ou rejeitou o pedido.'; status.innerHTML = `<pre>${escapeHtml(JSON.stringify(result, null, 2))}</pre>`; return; }
    videoFeedback.textContent = `Tarefa ${result.task_id} criada. Monitorando em tempo real.`;
    await watchTask(result.task_id);
  } catch (error) {
    videoFeedback.textContent = `Falha de comunicação: ${error.message}`;
  }
});

function formatStudioTime(seconds) {
  const safeSeconds = Math.max(0, Number(seconds) || 0);
  const minutes = Math.floor(safeSeconds / 60).toString().padStart(2, '0');
  const remainder = (safeSeconds % 60).toFixed(3).padStart(6, '0');
  return `${minutes}:${remainder}`;
}

function setStudioHealth(label, active = false) {
  studioHealth.className = `health-badge${active ? ' active' : ''}`;
  studioHealth.innerHTML = `<i></i> ${escapeHtml(label)}`;
}

function ensureAudioContext() {
  if (!studio.audioContext) {
    studio.audioContext = new AudioContext({ latencyHint: 'interactive', sampleRate: 48000 });
    studio.analyser = studio.audioContext.createAnalyser();
    studio.analyser.fftSize = 2048;
    studio.analyser.smoothingTimeConstant = 0.82;
    studio.analyser.connect(studio.audioContext.destination);
    drawStudioWaveform();
  }
  if (studio.audioContext.state === 'suspended') studio.audioContext.resume();
  return studio.audioContext;
}

function drawStudioWaveform() {
  if (!studio.analyser) return;
  const data = new Uint8Array(studio.analyser.fftSize);
  studio.analyser.getByteTimeDomainData(data);
  const width = studioWaveform.width;
  const height = studioWaveform.height;
  studioWaveformContext.clearRect(0, 0, width, height);
  studioWaveformContext.fillStyle = '#0e1422';
  studioWaveformContext.fillRect(0, 0, width, height);
  studioWaveformContext.strokeStyle = 'rgba(117,213,194,.14)';
  studioWaveformContext.lineWidth = 1;
  for (let line = 1; line < 5; line += 1) {
    const y = (height / 5) * line;
    studioWaveformContext.beginPath();
    studioWaveformContext.moveTo(0, y);
    studioWaveformContext.lineTo(width, y);
    studioWaveformContext.stroke();
  }
  studioWaveformContext.strokeStyle = '#75d5c2';
  studioWaveformContext.lineWidth = 2;
  studioWaveformContext.beginPath();
  data.forEach((value, index) => {
    const x = (index / (data.length - 1)) * width;
    const y = (value / 255) * height;
    if (index === 0) studioWaveformContext.moveTo(x, y);
    else studioWaveformContext.lineTo(x, y);
  });
  studioWaveformContext.stroke();
  const peak = Math.max(...data.map((value) => Math.abs(value - 128))) / 128;
  const db = peak > 0.0001 ? 20 * Math.log10(peak) : -Infinity;
  masterMeter.style.height = `${Math.min(100, Math.max(3, peak * 100))}%`;
  masterDb.textContent = Number.isFinite(db) ? `${db.toFixed(1)} dB` : '-∞ dB';
  studio.animationFrame = requestAnimationFrame(drawStudioWaveform);
}

function stopStudioTimer() {
  if (studio.timer) window.clearInterval(studio.timer);
  studio.timer = null;
}

function updateStudioTimer() {
  if (studio.recordingStartedAt) studioTime.textContent = formatStudioTime((performance.now() - studio.recordingStartedAt) / 1000);
}

async function addStudioTrack(blob, name) {
  const context = ensureAudioContext();
  const buffer = await context.decodeAudioData(await blob.arrayBuffer());
  const track = { id: crypto.randomUUID(), name: name || `Take ${studio.tracks.length + 1}`, filename: blob.name || `${name || `take-${studio.tracks.length + 1}`}.webm`, blob, buffer, url: URL.createObjectURL(blob), volume: 0.85, pan: 0, mute: false, solo: false };
  studio.tracks.push(track);
  studio.activeTrackId = track.id;
  renderStudioTracks();
  studioFeedback.textContent = `${track.name} carregado · ${formatStudioTime(buffer.duration)}`;
  setStudioHealth('sessão armada', true);
}

function renderStudioTracks() {
  trackCount.textContent = `${studio.tracks.length} ${studio.tracks.length === 1 ? 'take' : 'takes'}`;
  if (!studio.tracks.length) {
    studioTracks.innerHTML = '<div class="empty-state">Grave ou importe um take para começar a mixagem.</div>';
    return;
  }
  studioTracks.innerHTML = studio.tracks.map((track, index) => `<article class="studio-track ${track.id === studio.activeTrackId ? 'selected' : ''}">
    <div class="track-index">${String(index + 1).padStart(2, '0')}</div>
    <div class="track-identity"><strong>${escapeHtml(track.name)}</strong><span>${formatStudioTime(track.buffer.duration)} · ${track.buffer.sampleRate / 1000} kHz</span></div>
    <div class="track-wave"><span style="width:${Math.max(12, Math.min(100, track.buffer.duration * 4))}%"></span></div>
    <label class="mini-control">VOL<input data-track-volume="${track.id}" type="range" min="0" max="1" step="0.01" value="${track.volume}" /></label>
    <label class="mini-control">PAN<input data-track-pan="${track.id}" type="range" min="-1" max="1" step="0.01" value="${track.pan}" /></label>
    <button class="track-toggle ${track.mute ? 'active' : ''}" data-track-mute="${track.id}" type="button">M</button>
    <button class="track-toggle ${track.solo ? 'active solo' : ''}" data-track-solo="${track.id}" type="button">S</button>
    <button class="icon-button" data-track-remove="${track.id}" type="button" aria-label="Remover take">×</button>
  </article>`).join('');
  studioTracks.querySelectorAll('[data-track-volume]').forEach((input) => input.addEventListener('input', () => { const track = studio.tracks.find((item) => item.id === input.dataset.trackVolume); if (track) track.volume = Number(input.value); }));
  studioTracks.querySelectorAll('[data-track-pan]').forEach((input) => input.addEventListener('input', () => { const track = studio.tracks.find((item) => item.id === input.dataset.trackPan); if (track) track.pan = Number(input.value); }));
  studioTracks.querySelectorAll('[data-track-mute]').forEach((button) => button.addEventListener('click', () => { const track = studio.tracks.find((item) => item.id === button.dataset.trackMute); if (track) { track.mute = !track.mute; renderStudioTracks(); } }));
  studioTracks.querySelectorAll('[data-track-solo]').forEach((button) => button.addEventListener('click', () => { const track = studio.tracks.find((item) => item.id === button.dataset.trackSolo); if (track) { track.solo = !track.solo; renderStudioTracks(); } }));
  studioTracks.querySelectorAll('[data-track-remove]').forEach((button) => button.addEventListener('click', () => { const indexToRemove = studio.tracks.findIndex((item) => item.id === button.dataset.trackRemove); if (indexToRemove >= 0) { URL.revokeObjectURL(studio.tracks[indexToRemove].url); studio.tracks.splice(indexToRemove, 1); studio.activeTrackId = studio.tracks.at(-1)?.id || null; renderStudioTracks(); } }));
}

async function startStudioRecording() {
  const context = ensureAudioContext();
  if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) throw new Error('Este navegador não oferece captura de áudio compatível.');
  studio.inputStream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, echoCancellation: false, noiseSuppression: false, autoGainControl: false } });
  const source = context.createMediaStreamSource(studio.inputStream);
  source.connect(studio.analyser);
  const format = document.querySelector('#record-format').value;
  const mimeType = MediaRecorder.isTypeSupported(format) ? format : 'audio/webm';
  studio.recorder = new MediaRecorder(studio.inputStream, { mimeType, audioBitsPerSecond: 192000 });
  const chunks = [];
  studio.recorder.ondataavailable = (event) => { if (event.data.size) chunks.push(event.data); };
  studio.recorder.onstop = async () => {
    studio.inputStream?.getTracks().forEach((track) => track.stop());
    studio.inputStream = null;
    const blob = new Blob(chunks, { type: mimeType });
    try { await addStudioTrack(blob, takeName.value.trim() || `Káiros Take ${studio.tracks.length + 1}`); } catch { studioFeedback.textContent = 'Não foi possível decodificar o take gravado.'; setStudioHealth('erro no take'); }
  };
  studio.recordingStartedAt = performance.now();
  studio.recorder.start(100);
  stopStudioTimer();
  studio.timer = window.setInterval(updateStudioTimer, 40);
  recordToggle.classList.add('recording');
  recordToggle.innerHTML = '<span class="transport-dot"></span> Parar gravação';
  studioFeedback.textContent = 'Capturando monitoramento do microfone...';
  studioHealth.innerHTML = '<i></i> gravando';
  studioHealth.className = 'health-badge active recording-health';
}

function stopStudioRecording() {
  if (studio.recorder?.state === 'recording') studio.recorder.stop();
  studio.recordingStartedAt = 0;
  stopStudioTimer();
  recordToggle.classList.remove('recording');
  recordToggle.innerHTML = '<span class="transport-dot"></span> Gravar';
  setStudioHealth('processando take', true);
}

function stopStudioPlayback() {
  studio.playbackSources.forEach((source) => { try { source.stop(); } catch {} });
  studio.playbackSources = [];
  playToggle.textContent = '▶ Reproduzir mix';
  setStudioHealth(studio.tracks.length ? 'sessão armada' : 'pronto', Boolean(studio.tracks.length));
}

function playStudioMix() {
  if (!studio.tracks.length) { studioFeedback.textContent = 'Grave ou importe um take antes de reproduzir.'; return; }
  const context = ensureAudioContext();
  stopStudioPlayback();
  const hasSolo = studio.tracks.some((track) => track.solo);
  studio.tracks.forEach((track) => {
    if (track.mute || (hasSolo && !track.solo)) return;
    const source = context.createBufferSource();
    const gain = context.createGain();
    const panner = context.createStereoPanner ? context.createStereoPanner() : null;
    source.buffer = track.buffer;
    gain.gain.value = track.volume;
    source.connect(gain);
    if (panner) { panner.pan.value = track.pan; gain.connect(panner); panner.connect(studio.analyser); } else gain.connect(studio.analyser);
    source.onended = () => { studio.playbackSources = studio.playbackSources.filter((item) => item !== source); if (!studio.playbackSources.length) stopStudioPlayback(); };
    studio.playbackSources.push(source);
    source.start();
  });
  playToggle.textContent = '❚❚ Mix em reprodução';
  setStudioHealth('mix em reprodução', true);
}

function audioBufferToWav(buffer) {
  const channels = Math.min(2, buffer.numberOfChannels);
  const frameLength = buffer.length;
  const bytes = 44 + frameLength * channels * 2;
  const view = new DataView(new ArrayBuffer(bytes));
  const writeString = (offset, value) => [...value].forEach((character, index) => view.setUint8(offset + index, character.charCodeAt(0)));
  writeString(0, 'RIFF'); view.setUint32(4, bytes - 8, true); writeString(8, 'WAVE'); writeString(12, 'fmt '); view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, channels, true); view.setUint32(24, buffer.sampleRate, true); view.setUint32(28, buffer.sampleRate * channels * 2, true); view.setUint16(32, channels * 2, true); view.setUint16(34, 16, true); writeString(36, 'data'); view.setUint32(40, bytes - 44, true);
  const sources = Array.from({ length: channels }, (_, channel) => buffer.getChannelData(channel));
  let offset = 44;
  for (let frame = 0; frame < frameLength; frame += 1) for (let channel = 0; channel < channels; channel += 1) { const sample = Math.max(-1, Math.min(1, sources[channel][frame])); view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true); offset += 2; }
  return new Blob([view], { type: 'audio/wav' });
}

async function bounceStudioMix() {
  if (!studio.tracks.length) { studioFeedback.textContent = 'Não há takes para exportar.'; return; }
  const sampleRate = studio.audioContext?.sampleRate || 48000;
  const length = Math.max(...studio.tracks.map((track) => track.buffer.length));
  const offline = new OfflineAudioContext(2, length, sampleRate);
  const hasSolo = studio.tracks.some((track) => track.solo);
  studio.tracks.forEach((track) => {
    if (track.mute || (hasSolo && !track.solo)) return;
    const source = offline.createBufferSource(); const gain = offline.createGain(); const panner = offline.createStereoPanner ? offline.createStereoPanner() : null;
    source.buffer = track.buffer; gain.gain.value = track.volume; source.connect(gain);
    if (panner) { panner.pan.value = track.pan; gain.connect(panner); panner.connect(offline.destination); } else gain.connect(offline.destination); source.start();
  });
  const rendered = await offline.startRendering();
  const url = URL.createObjectURL(audioBufferToWav(rendered));
  const anchor = document.createElement('a'); anchor.href = url; anchor.download = `kairos-mix-${new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-')}.wav`; anchor.click(); window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  studioFeedback.textContent = 'Bounce WAV exportado para o seu dispositivo.';
  setStudioHealth('bounce exportado', true);
}

recordToggle.addEventListener('click', () => { if (studio.recorder?.state === 'recording') stopStudioRecording(); else startStudioRecording().catch((error) => { studioFeedback.textContent = error.message; setStudioHealth('microfone bloqueado'); }); });
playToggle.addEventListener('click', playStudioMix);
stopMix.addEventListener('click', stopStudioPlayback);
bounceMix.addEventListener('click', () => bounceStudioMix().catch(() => { studioFeedback.textContent = 'Falha ao renderizar o bounce WAV.'; }));
takeUpload.addEventListener('change', () => { const file = takeUpload.files?.[0]; if (file) addStudioTrack(file, file.name.replace(/\.[^.]+$/, '')).catch(() => { studioFeedback.textContent = 'Não foi possível carregar esse arquivo de áudio.'; }); takeUpload.value = ''; });

async function uploadActiveStudioTake() {
  const track = activeStudioTrack();
  if (!track) { studioHandoffFeedback.textContent = 'Grave ou importe um take antes de enviar.'; return; }
  const token = studioUploadToken.value.trim();
  if (!token) { studioHandoffFeedback.textContent = 'Informe o token Bearer configurado no backend.'; return; }
  studioUploadHandoff.disabled = true;
  studioHandoffStatus.textContent = 'enviando…';
  studioHandoffFeedback.textContent = 'Enviando o take ativo com autenticação…';
  try {
    const extension = track.filename.includes('.') ? '' : (track.blob.type.includes('wav') ? '.wav' : '.webm');
    const uploadFile = new File([track.blob], `${track.filename}${extension}`, { type: track.blob.type || 'application/octet-stream' });
    const formData = new FormData();
    formData.append('file', uploadFile);
    const uploadResponse = await fetch(`${API_BASE}/v1/studio/assets`, { method: 'POST', headers: { Authorization: `Bearer ${token}` }, body: formData });
    const uploadPayload = await uploadResponse.json();
    if (!uploadResponse.ok) throw new Error(uploadPayload.detail || 'Falha ao enviar o take');
    studio.remoteAsset = uploadPayload;
    studioHandoffStatus.textContent = 'asset recebido';
    studioHandoffFeedback.textContent = `${uploadPayload.asset_id} recebido · ${Number(uploadPayload.duration_seconds).toFixed(2)} s. Criando handoff explícito…`;
    const request = {
      prompt: form.elements.prompt?.value?.trim() || 'Analisar take vocal do Kháirus the Dragon',
      route_id: 'studio-recording',
      artist_id: 'kairos.khairus_the_dragon',
      genre: form.elements.genre?.value || 'Trap Soul',
      bpm: Number(form.elements.bpm?.value || 140),
      key: form.elements.key?.value || 'C#',
      scale: form.elements.scale?.value || 'minor',
      lyrics: form.elements.lyrics?.value?.trim() || null,
      duration_seconds: Math.min(120, Math.max(1, Number(track.buffer.duration.toFixed(3)))),
      analyze_audio: true,
      transcribe: false,
      generate_audio: studioGenerateAudio.checked,
      output_format: 'wav',
    };
    const handoffResponse = await fetch(`${API_BASE}/v1/studio/handoff`, { method: 'POST', headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ asset_id: uploadPayload.asset_id, request }) });
    const handoffPayload = await handoffResponse.json();
    if (!handoffResponse.ok) throw new Error(handoffPayload.detail || 'Falha ao criar handoff');
    studioHandoffStatus.textContent = 'handoff criado';
    studioHandoffFeedback.textContent = `Tarefa ${handoffPayload.task_id} criada. Acompanhando no Live Ops.`;
    await watchTask(handoffPayload.task_id);
  } catch (error) {
    studioHandoffStatus.textContent = 'erro';
    studioHandoffFeedback.textContent = error.message;
  } finally {
    studioUploadHandoff.disabled = false;
  }
}

studioUploadHandoff.addEventListener('click', uploadActiveStudioTake);
clearStudio.addEventListener('click', () => { stopStudioPlayback(); studio.tracks.forEach((track) => URL.revokeObjectURL(track.url)); studio.tracks = []; studio.activeTrackId = null; studio.remoteAsset = null; renderStudioTracks(); studioTime.textContent = '00:00.000'; studioFeedback.textContent = 'Sessão limpa localmente.'; studioHandoffStatus.textContent = 'local por padrão'; studioHandoffFeedback.textContent = 'Nenhum take foi enviado ao backend.'; setStudioHealth('pronto'); });

function renderIslandChain(payload) {
  islandStatus.textContent = `${payload.chain.length} etapas`;
  islandChain.innerHTML = `<div class="chain-summary"><span>${escapeHtml(payload.instrument)} · ${escapeHtml(payload.family)}</span><span>${escapeHtml(payload.source)}</span></div>${payload.chain.map((step) => `<article class="chain-step"><span class="chain-order">${String(step.order).padStart(2, '0')}</span><div><strong>${escapeHtml(step.algorithm.replaceAll('_', ' '))}</strong><p>${escapeHtml(step.rationale)}</p></div><code>${escapeHtml(JSON.stringify(step.parameters))}</code></article>`).join('')}<div class="chain-warning">${payload.warnings.map((warning) => `<p>! ${escapeHtml(warning)}</p>`).join('')}</div>`;
}

async function loadIslandInstruments() {
  try {
    const response = await fetch(`${API_BASE}/v1/artistic-island/instruments`);
    if (!response.ok) throw new Error('Atlas indisponível');
    const payload = await response.json();
    islandInstrument.innerHTML = payload.instruments.map((instrument) => `<option value="${escapeHtml(instrument.name)}">${escapeHtml(instrument.name.replaceAll('_', ' '))} · ${escapeHtml(instrument.family)}</option>`).join('');
    islandStatus.textContent = `${payload.instruments.length} perfis`;
  } catch (error) {
    islandStatus.textContent = 'offline';
    islandChain.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}. O endpoint de capabilities precisa estar ativo.</div>`;
  }
}

async function requestIslandPlan() {
  islandPlanButton.disabled = true;
  islandStatus.textContent = 'calculando…';
  try {
    const response = await fetch(`${API_BASE}/v1/artistic-island/mix-plan`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ instrument: islandInstrument.value, context: islandContext.value, reference_id: islandReference.value || null, prompt: 'Plano de mixagem para a sessão Káiros', include_optional: true }) });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || 'Falha ao gerar cadeia');
    renderIslandChain(payload);
  } catch (error) {
    islandStatus.textContent = 'erro';
    islandChain.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  } finally {
    islandPlanButton.disabled = false;
  }
}

islandPlanButton.addEventListener('click', requestIslandPlan);
loadIslandInstruments();

function setStudioMasterStatus(label, active = false) {
  studioMasterStatus.className = `chip${active ? ' live-chip' : ''}`;
  studioMasterStatus.textContent = label;
}

function renderStudioMasterFlow(flow) {
  const swing = Number(flow.swing_ratio || 0.5);
  const swingMs = Number(flow.mean_offset_ms || 0);
  const culture = (flow.culture || []).slice(0, 2).map((item) => `${item.label} ${(Number(item.probability) * 100).toFixed(0)}%`).join(' · ');
  studioMasterPocket.textContent = `${(Number(flow.bpm) || 140).toFixed(1)} BPM · swing ${(swing * 100).toFixed(1)}%`;
  studioMasterFlowNote.textContent = `${flow.onsets?.length || 0} onsets · offset médio ${swingMs.toFixed(1)} ms · ${culture || 'cultura pendente'}`;
  setStudioMasterStatus('flow carregado', true);
}

function renderStudioMasterPlan(plan) {
  studioMaster.plan = plan;
  const timing = plan.timing || {};
  const warnings = (plan.warnings || []).map((warning) => `<p>! ${escapeHtml(warning)}</p>`).join('');
  studioMasterPocket.textContent = `${Number(timing.bpm || 140).toFixed(1)} BPM · ${(Number(timing.swing_ms || 0)).toFixed(1)} ms off-beat`;
  studioMasterFlowNote.textContent = `${escapeHtml(plan.canon?.name || 'cânone próximo')} · ${timing.grid_follow ? 'grid follow ativo' : 'tempo preservado'}`;
  studioMasterPlanView.innerHTML = `<div class="studio-master-plan-summary"><span><strong>${escapeHtml(plan.style)}</strong> · ${escapeHtml(plan.repertoire?.id || 'repertório')}</span><span>${escapeHtml(plan.status)}</span></div><div class="studio-master-plan-grid"><span>Canon<strong>${escapeHtml(plan.canon?.name || '—')}</strong></span><span>Swing<strong>${(Number(timing.swing_ratio || 0.5) * 100).toFixed(1)}%</strong></span><span>Vocal focus<strong>${plan.vocal_focus?.enabled ? 'sidechain ativo' : 'desligado'}</strong></span><span>Handoff<strong>${plan.handoff?.approval_required ? 'aprovação requerida' : 'não aplicável'}</strong></span></div>${warnings ? `<div class="chain-warning">${warnings}</div>` : ''}`;
  setStudioMasterStatus('plano pronto', true);
}

function connectStudioMasterPerformance() {
  if (studioMaster.socket && [WebSocket.OPEN, WebSocket.CONNECTING].includes(studioMaster.socket.readyState)) return;
  studioMaster.socket = new WebSocket(`${WS_BASE}/ws/studio-master/${encodeURIComponent(studioMaster.sessionId)}/performance`);
  studioMaster.socket.onopen = () => setStudioMasterStatus('performance ativa', true);
  studioMaster.socket.onmessage = (event) => {
    const payload = JSON.parse(event.data);
    if (payload.event === 'command_error') {
      setStudioMasterStatus('comando recusado');
      studioFeedback.textContent = payload.error;
      return;
    }
    const state = payload.state || {};
    studioMasterGridFollow.checked = Boolean(state.grid_follow);
    studioMasterBpm.value = Number(state.bpm || 140).toFixed(1);
    studioMasterSwing.value = Number(state.swing_ratio || 0.60).toFixed(2);
    studioMasterPocket.textContent = `${Number(state.bpm || 140).toFixed(1)} BPM · ${(Number(state.swing_ms || 0)).toFixed(1)} ms swing`;
    if (state.status === 'PENDING_APPROVAL') studioFeedback.textContent = 'Proposta criada para revisão; nenhum arquivo foi persistido.';
    if (state.last_action === 'BOOST_PUNCHLINE') studioFeedback.textContent = `Punchline: +${Number(state.punchline_boost_db || 0).toFixed(1)} dB · reverb -${Number(state.reverb_reduction_db || 0).toFixed(1)} dB`;
    setStudioMasterStatus(state.status === 'PENDING_APPROVAL' ? 'aguarda aprovação' : 'performance ativa', true);
  };
  studioMaster.socket.onerror = () => setStudioMasterStatus('WebSocket indisponível');
  studioMaster.socket.onclose = () => { studioMaster.socket = null; setStudioMasterStatus('performance offline'); };
}

function sendStudioMasterCommand(command) {
  connectStudioMasterPerformance();
  if (studioMaster.socket?.readyState !== WebSocket.OPEN) {
    studioFeedback.textContent = 'Conectando o command deck; tente novamente em um instante.';
    return;
  }
  studioMaster.socket.send(JSON.stringify(command));
}

function activeStudioTrack() {
  return studio.tracks.find((track) => track.id === studio.activeTrackId) || studio.tracks[0];
}

async function analyzeStudioMasterTake() {
  const track = activeStudioTrack();
  if (!track) { studioFeedback.textContent = 'Grave ou importe um take antes de analisar o flow.'; return; }
  studioMasterAnalyze.disabled = true;
  setStudioMasterStatus('analisando…');
  try {
    const source = track.buffer.getChannelData(0);
    const stride = Math.max(1, Math.ceil(source.length / 200000));
    const samples = Array.from({ length: Math.ceil(source.length / stride) }, (_, index) => Number(source[index * stride] || 0));
    const response = await fetch(`${API_BASE}/v1/studio-master/groove/analyze`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ samples, sample_rate: Math.ceil(track.buffer.sampleRate / stride), bpm: Number(studioMasterBpm.value || 140), canon_id: studioMasterCanon.value || null }) });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || 'Falha ao analisar take');
    studioMaster.flow = payload;
    renderStudioMasterFlow(payload);
    studioFeedback.textContent = `Flow analisado: ${payload.onsets?.length || 0} onsets · cânone próximo ${payload.canon_match || 'não identificado'}.`;
  } catch (error) {
    setStudioMasterStatus('erro');
    studioFeedback.textContent = error.message;
  } finally {
    studioMasterAnalyze.disabled = false;
  }
}

async function requestStudioMasterPlan() {
  studioMasterPlanButton.disabled = true;
  setStudioMasterStatus('planejando…');
  try {
    const response = await fetch(`${API_BASE}/v1/studio-master/responsive-plan`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ style: studioMasterStyle.value, canon_id: studioMasterCanon.value || null, bpm: Number(studioMasterBpm.value || 140), swing_ratio: Number(studioMasterSwing.value || 0.60), grid_follow: studioMasterGridFollow.checked, flow: studioMaster.flow }) });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || 'Falha ao gerar plano responsivo');
    renderStudioMasterPlan(payload);
    studioFeedback.textContent = 'Plano responsivo pronto para revisão; o pipeline não foi iniciado.';
  } catch (error) {
    setStudioMasterStatus('erro');
    studioMasterPlanView.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  } finally {
    studioMasterPlanButton.disabled = false;
  }
}

async function loadStudioMasterCatalog() {
  try {
    const [canonResponse, repertoireResponse] = await Promise.all([fetch(`${API_BASE}/v1/studio-master/canon`), fetch(`${API_BASE}/v1/studio-master/repertoire`)]);
    if (!canonResponse.ok || !repertoireResponse.ok) throw new Error('StudioMaster indisponível');
    const canonPayload = await canonResponse.json();
    const repertoirePayload = await repertoireResponse.json();
    studioMaster.canon = canonPayload.entries || [];
    studioMasterCanon.innerHTML = `<option value="">Mais próximo por BPM/swing</option>${studioMaster.canon.map((entry) => `<option value="${escapeHtml(entry.id)}">${escapeHtml(entry.name)} · ${escapeHtml(entry.region)}</option>`).join('')}`;
    setStudioMasterStatus(`${studioMaster.canon.length} padrões`, true);
    if (repertoirePayload.profiles?.length) studioMasterFlowNote.textContent = `${repertoirePayload.profiles.length} perfis instrumentais · command deck pronto.`;
    connectStudioMasterPerformance();
  } catch (error) {
    setStudioMasterStatus('offline');
    studioMasterFlowNote.textContent = error.message;
  }
}

function setStudioMaster2Status(label, active = false) {
  studioMaster2Status.className = `chip${active ? ' live-chip' : ''}`;
  studioMaster2Status.textContent = label;
}

function renderStudioMaster2Output(payload, mode) {
  const warnings = (payload.warnings || []).map((warning) => `<p>! ${escapeHtml(warning)}</p>`).join('');
  if (mode === 'arrangement') {
    const sections = (payload.sections || []).map((section) => `<span class="arrangement-pill"><strong>${escapeHtml(section.id)}</strong> ${section.bars} bars · ${(Number(section.energy) * 100).toFixed(0)}%</span>`).join('');
    studioMaster2Output.innerHTML = `<div class="studio-master-plan-summary"><span><strong>${escapeHtml(payload.style)}</strong> · ${escapeHtml(payload.mood)}</span><span>${escapeHtml(payload.status)}</span></div><div class="arrangement-pills">${sections}</div>${warnings ? `<div class="chain-warning">${warnings}</div>` : ''}`;
  } else if (mode === 'signature') {
    const chain = (payload.chain || []).map((step) => `<article class="chain-step"><span class="chain-order">•</span><div><strong>${escapeHtml(step.algorithm)}</strong><p>${escapeHtml(step.rationale)}</p></div><code>${escapeHtml(JSON.stringify(step.parameters))}</code></article>`).join('');
    studioMaster2Output.innerHTML = `<div class="studio-master-plan-summary"><span><strong>Modo Káiros</strong> · ${escapeHtml(payload.target)}</span><span>${escapeHtml(payload.status)}</span></div>${chain}${warnings ? `<div class="chain-warning">${warnings}</div>` : ''}`;
  } else {
    studioMaster2Output.innerHTML = `<div class="studio-master-plan-summary"><span><strong>Clip social</strong> · ${escapeHtml(payload.platform)}</span><span>${escapeHtml(payload.status)}</span></div><div class="studio-master-plan-grid"><span>Canvas<strong>${payload.canvas?.width} × ${payload.canvas?.height}</strong></span><span>Duração<strong>${payload.duration_seconds}s</strong></span><span>Render<strong>${escapeHtml(payload.render?.adapter || 'adapter')}</strong></span><span>Publicação<strong>bloqueada</strong></span></div>${warnings ? `<div class="chain-warning">${warnings}</div>` : ''}`;
  }
  setStudioMaster2Status('proposta pronta', true);
}

async function requestStudioMaster2(path, body, mode) {
  setStudioMaster2Status('calculando…');
  try {
    const response = await fetch(`${API_BASE}${path}`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body) });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || 'Falha ao gerar proposta');
    renderStudioMaster2Output(payload, mode);
    studioFeedback.textContent = 'Proposta 2.0 pronta para revisão; nenhum arquivo, treino ou publicação foi iniciado.';
  } catch (error) {
    setStudioMaster2Status('erro');
    studioMaster2Output.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

function requestArrangementPlan() {
  studioArrangementButton.disabled = true;
  requestStudioMaster2('/v1/studio-master/arrangement', {
    style: studioMasterStyle.value,
    mood: studioArrangementMood.value,
    bpm: Number(studioMasterBpm.value || 140),
    total_bars: Number(studioArrangementBars.value || 32),
    key: form.elements.key?.value || 'C#',
  }, 'arrangement').finally(() => { studioArrangementButton.disabled = false; });
}

function requestSignaturePlan() {
  studioSignatureButton.disabled = true;
  requestStudioMaster2('/v1/studio-master/signature-plan', {
    intensity: Number(studioSignatureIntensity.value),
    vocal_presence: studioMasterStyle.value === 'vocal_focus' ? 0.9 : 0.7,
    low_end_focus: studioMasterStyle.value === 'brazilian_funk_heavy' ? 0.85 : 0.65,
    spatial_depth: 0.35,
    target: studioSignatureTarget.value,
  }, 'signature').finally(() => { studioSignatureButton.disabled = false; });
}

function requestViralClipPlan() {
  studioViralButton.disabled = true;
  requestStudioMaster2('/v1/studio-master/viral-clip-plan', {
    title: 'DJ Káiros | StudioMaster',
    duration_seconds: 15,
    aspect_ratio: '9:16',
    platform: 'generic',
    audio_asset_id: null,
  }, 'viral').finally(() => { studioViralButton.disabled = false; });
}

function renderRealAdapterCapabilities(payload) {
  const adapters = payload.adapters || [];
  studioRealAdaptersGate.textContent = payload.gate_enabled ? 'gate global ativo · allowlist e manifesto ainda obrigatórios' : 'gate global desligado';
  studioRealAdaptersStatus.className = `chip${adapters.some((adapter) => adapter.enabled) ? ' live-chip' : ''}`;
  studioRealAdaptersStatus.textContent = `${adapters.filter((adapter) => adapter.enabled).length}/${adapters.length} prontos`;
  studioRealAdaptersGrid.innerHTML = adapters.map((adapter) => {
    const license = adapter.license || {};
    const state = adapter.operational_status || (adapter.enabled ? 'READY' : 'FALLBACK_ONLY');
    return `<article class="real-adapter-card ${state === 'READY' ? 'ready' : 'fallback'}">
      <div class="real-adapter-topline"><strong>${escapeHtml(adapter.adapter_id)}</strong><span>${escapeHtml(state)}</span></div>
      <p>${escapeHtml(adapter.package)}${adapter.package_version ? ` · v${escapeHtml(adapter.package_version)}` : ''}</p>
      <div class="real-adapter-meta"><span>License: ${escapeHtml(license.code_license || 'pendente')}</span><span>GPU: ${adapter.requires_gpu ? 'sim' : 'não'}</span></div>
      <p class="real-adapter-reason">${escapeHtml(adapter.reason || 'Pronto para preflight.')}</p>
      <code>fallback: ${escapeHtml(adapter.fallback || '—')}</code>
    </article>`;
  }).join('') || '<div class="empty-state">Nenhum adapter no manifesto.</div>';
}

function setFrontierStatus(label, active = false) {
  frontierStatus.className = `chip${active ? ' live-chip' : ''}`;
  frontierStatus.textContent = label;
}

function renderFrontierPlan(plan) {
  const stack = (plan.selected_stack || []).map((item) => `<span class="frontier-stack-pill">${escapeHtml(item)}</span>`).join('');
  const stages = (plan.stages || []).map((stage) => `<article class="chain-step"><span class="chain-order">•</span><div><strong>${escapeHtml(stage.name)}</strong><p>${escapeHtml(stage.owner)} · ${escapeHtml(stage.output)}</p></div><code>${escapeHtml(stage.id)}</code></article>`).join('');
  const warnings = (plan.warnings || []).map((warning) => `<p>! ${escapeHtml(warning)}</p>`).join('');
  frontierOutput.innerHTML = `<div class="studio-master-plan-summary"><span><strong>${escapeHtml(plan.harness)} Harness</strong> · ${escapeHtml(plan.profile)}</span><span>${escapeHtml(plan.status)}</span></div><div class="frontier-stack">${stack}</div>${stages}${warnings ? `<div class="chain-warning">${warnings}</div>` : ''}`;
  setFrontierStatus('plano pronto', true);
}

async function loadFrontierCapabilities() {
  setFrontierStatus('carregando…');
  try {
    const response = await fetch(`${API_BASE}/v1/studio-master/frontier/capabilities`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || 'Frontier indisponível');
    const components = payload.components || [];
    frontierComponents.textContent = `${components.length} componentes · ${components.filter((item) => item.status === 'READY').length} prontos · ${components.filter((item) => item.status === 'OPTIONAL').length} opcionais`;
    frontierGates.textContent = payload.governance?.human_approval_required ? 'Aprovação humana obrigatória · auto-publish bloqueado' : 'Gates não informados';
    setFrontierStatus('capabilities prontas', true);
  } catch (error) {
    setFrontierStatus('offline');
    frontierComponents.textContent = error.message;
  }
}

async function requestFrontierPlan() {
  frontierPlanButton.disabled = true;
  setFrontierStatus('planejando…');
  try {
    const response = await fetch(`${API_BASE}/v1/studio-master/frontier/plan`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ profile: frontierProfile.value, compute: frontierCompute.value, video_backend: frontierVideoBackend.value, fps: Number(frontierFps.value || 24) }) });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || 'Falha ao gerar plano frontier');
    renderFrontierPlan(payload);
    studioFeedback.textContent = 'PHD Harness pronto para revisão; nenhum render ou download foi iniciado.';
  } catch (error) {
    setFrontierStatus('erro');
    frontierOutput.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  } finally {
    frontierPlanButton.disabled = false;
  }
}

async function loadRealAdapterCapabilities() {
  studioRealAdaptersStatus.textContent = 'atualizando…';
  try {
    const response = await fetch(`${API_BASE}/v1/studio-master/real-adapters/capabilities`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || 'capabilities reais indisponíveis');
    renderRealAdapterCapabilities(payload);
  } catch (error) {
    studioRealAdaptersStatus.className = 'chip';
    studioRealAdaptersStatus.textContent = 'offline';
    studioRealAdaptersGate.textContent = error.message;
    studioRealAdaptersGrid.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

async function loadStudioMaster2Status() {
  try {
    const [analyticsResponse, retrainingResponse, adaptersResponse] = await Promise.all([
      fetch(`${API_BASE}/v1/studio-master/analytics`),
      fetch(`${API_BASE}/v1/studio-master/retraining`),
      fetch(`${API_BASE}/v1/studio-master/adapters`),
    ]);
    if (!analyticsResponse.ok || !retrainingResponse.ok || !adaptersResponse.ok) throw new Error('status 2.0 indisponível');
    const analytics = await analyticsResponse.json();
    const retraining = await retrainingResponse.json();
    const adapters = await adaptersResponse.json();
    const mos = analytics.average_mos == null ? 'MOS pendente' : `MOS médio ${Number(analytics.average_mos).toFixed(2)}`;
    studioAnalyticsReadout.textContent = `${analytics.total_productions} produções · ${mos}`;
    studioAnalyticsNote.textContent = Object.entries(analytics.genres || {}).map(([genre, count]) => `${genre}: ${count}`).join(' · ') || 'Sem histórico de produção.';
    studioRetrainingReadout.textContent = retraining.status === 'DISABLED' ? 'desligado' : retraining.status.toLowerCase();
    studioRetrainingNote.textContent = retraining.warnings?.[0] || 'Manifesto não disponível.';
    const available = (adapters.adapters || []).filter((adapter) => adapter.available).length;
    setStudioMaster2Status(`${available}/${(adapters.adapters || []).length} adapters detectados`, true);
  } catch (error) {
    setStudioMaster2Status('status offline');
    studioAnalyticsNote.textContent = error.message;
  }
}

studioMasterAnalyze.addEventListener('click', () => analyzeStudioMasterTake());
studioMasterPlanButton.addEventListener('click', () => requestStudioMasterPlan());
studioMasterGridFollow.addEventListener('change', () => sendStudioMasterCommand({ action: 'SET_GRID_FOLLOW', value: studioMasterGridFollow.checked }));
studioMasterSwing.addEventListener('change', () => sendStudioMasterCommand({ action: 'SET_SWING', value: studioMasterSwing.value }));
studioMasterBpm.addEventListener('change', () => sendStudioMasterCommand({ action: 'SET_BPM', bpm: Number(studioMasterBpm.value) }));
studioMasterBoost.addEventListener('click', () => sendStudioMasterCommand({ action: 'BOOST_PUNCHLINE', value: true }));
studioMasterPush.addEventListener('click', () => sendStudioMasterCommand({ action: 'PUSH_TO_LIBRARY', reference_id: studioMasterCanon.value || null }));
studioArrangementButton.addEventListener('click', requestArrangementPlan);
studioSignatureButton.addEventListener('click', requestSignaturePlan);
studioViralButton.addEventListener('click', requestViralClipPlan);
studioRealAdaptersRefresh.addEventListener('click', loadRealAdapterCapabilities);
frontierPlanButton.addEventListener('click', requestFrontierPlan);
loadStudioMasterCatalog();
loadStudioMaster2Status();
loadRealAdapterCapabilities();
loadFrontierCapabilities();

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  data.bpm = Number(data.bpm);
  data.duration_seconds = Number(data.duration_seconds);
  data.swing = Number(data.swing);
  if (!data.lyrics) data.lyrics = null;
  feedback.textContent = 'Enviando ao gateway...';
  const response = await fetch(`${API_BASE}/v1/generate`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  const result = await response.json();
  renderAutoReview(result);
  if (!response.ok) { feedback.textContent = 'Falha ao iniciar tarefa: gate PHD bloqueou ou rejeitou o pedido.'; status.innerHTML = `<pre>${escapeHtml(JSON.stringify(result, null, 2))}</pre>`; return; }
  feedback.textContent = `Tarefa ${result.task_id} criada. Monitorando em tempo real.`;
  await watchTask(result.task_id);
});
