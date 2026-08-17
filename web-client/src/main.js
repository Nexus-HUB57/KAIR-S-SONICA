import './styles.css';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
const WS_BASE = API_BASE.replace(/^http/, 'ws');
const app = document.querySelector('#app');
const monitoredTasks = new Map();

app.innerHTML = `
  <section class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">AGENTE KÁIROS · CENTRAL MULTIMÍDIA</p>
        <h1>KAIR-S-SONICA</h1>
        <p class="lede">Crie um artefato de áudio e acompanhe cada tarefa em tempo real, sem perder o pulso do pipeline.</p>
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
    </div>

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
    const links = [
      snapshot.artifact_url ? `<a href="${API_BASE}${escapeHtml(snapshot.artifact_url)}" target="_blank" rel="noreferrer">áudio</a>` : '',
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
