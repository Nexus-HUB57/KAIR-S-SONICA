import './styles.css';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
const app = document.querySelector('#app');

app.innerHTML = `
  <section class="shell">
    <header>
      <p class="eyebrow">AGENTE KÁIROS · CENTRAL MULTIMÍDIA</p>
      <h1>KAIR-S-SONICA</h1>
      <p class="lede">Planeje, gere e acompanhe um artefato de áudio por meio do pipeline modular.</p>
    </header>
    <form id="generate-form" class="card">
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
    </form>
    <section id="status" class="card status" aria-live="polite"><p>Aguardando uma solicitação.</p></section>
  </section>`;

const status = document.querySelector('#status');
const form = document.querySelector('#generate-form');

function show(snapshot) {
  const progress = snapshot.progress || {};
  status.innerHTML = `<p class="eyebrow">${snapshot.status}</p><h2>${progress.step || 'queued'} · ${progress.percent || 0}%</h2><p>${progress.message || ''}</p>${snapshot.artifact_url ? `<audio controls src="${API_BASE}${snapshot.artifact_url}"></audio><a class="download" href="${API_BASE}${snapshot.artifact_url}" download>Baixar artefato</a>` : ''}${snapshot.error ? `<pre>${snapshot.error}</pre>` : ''}`;
}

async function poll(taskId) {
  for (;;) {
    const response = await fetch(`${API_BASE}/v1/tasks/${taskId}`);
    const snapshot = await response.json();
    show(snapshot);
    if (['SUCCEEDED', 'FAILED'].includes(snapshot.status)) return;
    await new Promise((resolve) => setTimeout(resolve, 400));
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  data.bpm = Number(data.bpm);
  data.duration_seconds = Number(data.duration_seconds);
  data.swing = Number(data.swing);
  if (!data.lyrics) data.lyrics = null;
  status.innerHTML = '<p>Enviando ao gateway...</p>';
  const response = await fetch(`${API_BASE}/v1/generate`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
  const result = await response.json();
  if (!response.ok) { status.innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`; return; }
  await poll(result.task_id);
});
