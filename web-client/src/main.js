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
    if (!response.ok) { videoFeedback.textContent = 'Falha ao enfileirar vídeo.'; status.innerHTML = `<pre>${escapeHtml(JSON.stringify(result, null, 2))}</pre>`; return; }
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
  const track = { id: crypto.randomUUID(), name: name || `Take ${studio.tracks.length + 1}`, blob, buffer, url: URL.createObjectURL(blob), volume: 0.85, pan: 0, mute: false, solo: false };
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
clearStudio.addEventListener('click', () => { stopStudioPlayback(); studio.tracks.forEach((track) => URL.revokeObjectURL(track.url)); studio.tracks = []; studio.activeTrackId = null; renderStudioTracks(); studioTime.textContent = '00:00.000'; studioFeedback.textContent = 'Sessão limpa localmente.'; setStudioHealth('pronto'); });

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
  if (!response.ok) { feedback.textContent = 'Falha ao iniciar tarefa.'; status.innerHTML = `<pre>${escapeHtml(JSON.stringify(result, null, 2))}</pre>`; return; }
  feedback.textContent = `Tarefa ${result.task_id} criada. Monitorando em tempo real.`;
  await watchTask(result.task_id);
});
