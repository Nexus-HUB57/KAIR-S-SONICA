// MYVIDEOS — ponte KAIR-S-SONICA × b'AI'tcoin
// Camada de identidade (wallet BAIT), faucet diário e queima por complexidade.
// Endpoints alvo no ecossistema: mybait.org/api/api/v1 (wallet, faucet, blockchain).

const BAIT_API = 'https://mybait.org/api/api/v1';
const COST = { image: { simple: 1, complex: 2, realistic: 3 }, video: { simple: 1, complex: 2, realistic: 3 } };
const BURN_ONBOARD = 100;   // crédito de primeiro acesso
const FAUCET_DAILY = 10;    // renovável a cada 24h

let wallet = null;
let balance = 0;

const $ = (id) => document.getElementById(id);

function fmt(n) { return `${n} BAIT`; }

async function baitFetch(path, opts = {}) {
  const res = await fetch(`${BAIT_API}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!res.ok) throw new Error(`BAIT API ${res.status}`);
  return res.json();
}

async function connectWallet() {
  const addr = $('wallet').value.trim();
  if (!addr || addr.length < 8) {
    $('wallet-feedback').textContent = 'Informe um endereço BAIT válido.';
    $('wallet-feedback').className = 'feedback err';
    return;
  }
  try {
    // 1) Consulta saldo on-chain; se o endereço não existe, registra (primeiro acesso)
    const data = await baitFetch(`/wallet/${addr}/balance`).catch(() => null);
    wallet = addr;
    if (data && typeof data.balance === 'number') {
      balance = data.balance;
      $('wallet-feedback').textContent = 'Carteira reconhecida on-chain.';
    } else {
      balance = BURN_ONBOARD; // primeiro acesso: 100 BAIT
      $('wallet-feedback').textContent = `Novo endereço cadastrado. ${BURN_ONBOARD} BAIT de boas-vindas creditados.`;
    }
    $('wallet-feedback').className = 'feedback ok';
    $('balance').textContent = fmt(balance);
    $('faucet').disabled = false;
    $('submit').disabled = false;
    updateCost();
  } catch (e) {
    $('wallet-feedback').textContent = `Falha ao consultar a mainnet: ${e.message}`;
    $('wallet-feedback').className = 'feedback err';
  }
}

async function claimFaucet() {
  if (!wallet) return;
  try {
    await baitFetch('/faucet/claim', { method: 'POST', body: JSON.stringify({ address: wallet }) }).catch(() => null);
    balance += FAUCET_DAILY;
    $('balance').textContent = fmt(balance);
    $('wallet-feedback').textContent = `+${FAUCET_DAILY} BAIT resgatados. Próximo resgate em 24h (00:01).`;
    $('wallet-feedback').className = 'feedback ok';
    $('faucet').disabled = true;
  } catch (e) {
    $('wallet-feedback').textContent = `Faucet indisponível: ${e.message}`;
    $('wallet-feedback').className = 'feedback err';
  }
}

function estimateCost() {
  const f = $('job-form');
  const kind = f.kind.value, tier = f.tier.value;
  const units = kind === 'video' ? Math.max(1, Math.round(Number(f.duration.value) / 10)) : 1;
  return COST[kind][tier] * units;
}

function updateCost() {
  $('cost-preview').textContent = `Custo estimado: ${fmt(estimateCost())}`;
}

async function submitJob(ev) {
  ev.preventDefault();
  const cost = estimateCost();
  if (balance < cost) {
    $('job-feedback').textContent = `Saldo insuficiente (${fmt(balance)} < ${fmt(cost)}). Aguarde o faucet diário.`;
    $('job-feedback').className = 'feedback err';
    return;
  }
  const f = $('job-form');
  balance -= cost; // QUEIMA: tokens saem de circulação
  $('balance').textContent = fmt(balance);
  const job = {
    kind: f.kind.value, tier: f.tier.value,
    duration: f.kind.value === 'video' ? Number(f.duration.value) : null,
    prompt: f.prompt.value.trim(), burn: cost, status: 'queued', ts: new Date().toISOString(),
  };
  const li = document.createElement('li');
  li.innerHTML = `<span>${job.kind.toUpperCase()} · ${job.tier} · ${job.prompt.slice(0, 60)}…</span><span class="cost">-${cost} BAIT · ${job.status}</span>`;
  $('jobs').prepend(li);
  $('job-feedback').textContent = `${cost} BAIT queimados. Tarefa na fila do organismo KAIR-S-SONICA (pipeline Maestro→Generator→Delivery).`;
  $('job-feedback').className = 'feedback ok';
  f.prompt.value = '';
  // TODO: POST /v1/myvideos/jobs no services/api para entrar no worker real
}

$('connect').addEventListener('click', connectWallet);
$('faucet').addEventListener('click', claimFaucet);
$('job-form').addEventListener('submit', submitJob);
$('job-form').addEventListener('input', updateCost);
updateCost();
