# MYLINK — mybait.org/mylink

Hub de navegação oficial do ecossistema b'AI'tcoin × KAIR-S-SONICA (referência: link-in-bio nível Dola).

- Estático, zero dependências de build, <12KB, mobile-first, safe-area, toque otimizado
- Seções: Plataforma (MYVIDEOS, Faucet, Explorer, AI Store, B'AI'nkr, SDK) · KTD (Instagram, TikTok, repo) · Status da mainnet (live via /api/api/v1/status)
- Design: dark carvão + âmbar KTD, glassmorphism, micro-interações, compartilhar com 1 toque

## Rotas em producao (mybait.org/mylink)

| Rota | Arquivo | Origem |
|---|---|---|
| `/mylink/` | `index.html` + `styles.css` + `app.js` + `particles.js` | Hub interativo Dola-grade (commit `8567daf`, PR #13) |
| `/mylink/cadastro.html` | `cadastro.html` | Cadastro Oficial de Agente - Protocolo 3 Etapas (preservado byte-a-byte de producao, sha256 `c70a9eca862e48b5c31e74d5086ed16054aa9de02a4b874fb68263a51de0dbb7`) |

O hub e a porta de entrada e aponta para o cadastro no card "Cadastro Oficial de Agente".
Nenhuma linha do fluxo de cadastro foi alterada; a pagina original segue intacta em sua propria rota.
