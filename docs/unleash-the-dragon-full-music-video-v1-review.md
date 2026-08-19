# UNLEASH THE DRAGON — clipe completo v1 — relatório de revisão técnica

## Identificação

| Campo | Valor |
| --- | --- |
| Arquivo | `assets/video/promos/unleash-the-dragon-full-music-video-v1.mp4` |
| Renderizador | `scripts/render_ktd_unleash_the_dragon_full.py` |
| Roteiro | `docs/unleash-the-dragon-full-music-video-script.md` |
| Áudio muxado | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav` |
| Data de render | 2026-08-19 |
| Status | Candidato a avaliação editorial humana |

## Especificação técnica verificada

O render foi validado com `ffprobe` e atende ao padrão do cânone fixado em `docs/ktd-asset-catalog.md`: resolução **720x1280** (9:16 vertical), **24 fps**, vídeo **H.264** (CRF 18, yuv420p, faststart), áudio **AAC 192 kbps**, duração exata de **150,000 s** — idêntica à duração do WAV oficial de trabalho — e tamanho de aproximadamente 67 MB. Não há texto, logo ou gráficos sobrepostos em nenhum plano; o encerramento usa o movimento `pull_out_fade` do microfone solitário com queda controlada para preto, conforme o bloco F2 do roteiro.

## Conformidade com o cânone

| Regra do cânone | Resultado |
| --- | --- |
| Push-in predominante com planos estáveis e fluidos | 16 planos, todos com movimento procedural contínuo; push-in aplicado em A1, A3, B1, C1 e F1 |
| Hard cuts em múltiplos do beat (0,588 s a 102 BPM) | Fins de plano alinhados à grade de barras de 4 batidas (~2,353 s) |
| Sujeito/objeto-símbolo no terço vertical central | Verificado na folha de contato; interface do TikTok não obstrui o eixo central |
| Chiaroscuro com pretos densos; paleta exclusiva | Carvão, bronze, vermelho queimado e âmbar em todos os planos; zero azul elétrico, néon frio, chuva ou água |
| Identidade KTD | Heterocromia (âmbar/azul-claro), cabeça raspada, barba longa, sete garras no peito e Dragão Diamante presentes nas keyframes |
| Não repetição | Manifesto SHA-256 consultado no render (`--forbidden-manifest`); nenhum hash GOLDEN_SCARS presente; nenhuma imagem de SIX NAMES reutilizada |

## Sequência dos planos

| Tempo | Cena | Movimento |
| --- | --- | --- |
| 0,00–9,41 s | Camarote: KTD amarrando o tênis, espelho de luzes com sete garras a giz | push_in |
| 9,41–18,82 s | Bastidor: mão tatuada na parede com pôsteres antigos | tracking_right |
| 18,82–28,24 s | Porta de acesso ao palco entreaberta com luz quente | push_in |
| 28,24–37,65 s | Mão apertando palheta sobre o violão, amplificador ao fundo | cut_push |
| 37,65–47,06 s | Tênis atravessando cabos e pedal no chão do palco | tilt_up |
| 47,06–56,47 s | Mão no microfone vintage | push_in |
| 56,47–65,88 s | KTD de costas sob spotlight, Dragão Diamante nas costas | push_in |
| 65,88–75,29 s | Close do rosto heterocromático sob luz âmbar | pull_out |
| 75,29–84,71 s | Performance do hook com luzes em leque | tracking_right |
| 84,71–94,12 s | Ajuste dos amplificadores valvulados | tracking_left |
| 94,12–103,53 s | Perfil de KTD na borda do palco, silhuetas ao fundo | push_in |
| 103,53–112,94 s | Luzes de palco com mural de dragão, ponte contemplativa | pull_out_fade |
| 112,94–122,35 s | KTD sentado na borda do palco, cabeça baixa | push_in |
| 122,35–131,76 s | Multidão em silhueta com mãos no alto | tracking_right |
| 131,76–141,18 s | Performance máxima de braços abertos na luz principal | push_in |
| 141,18–150,00 s | Microfone solitário iluminado, queda para preto | cut_push + fade |

## Materiais de apoio

Doze keyframes exclusivas foram geradas para este clipe em `assets/video/references/lyrics/` (padrão `song1-fullmv-scene-*`), todas em 1440x2560 e registradas no inventário por SHA-256. Os planos de transição (porta, tênis/cabos, microfone, luzes) reutilizam as keyframes validadas do teaser v1 sem repetição de frame idêntico, pois cada plano aplica recorte e movimento independentes.

## Critérios editoriais pendentes

Conforme o manifesto de criação, o clipe permanece **candidato**: a aprovação editorial humana deve confirmar a retenção dos primeiros dois segundos, a leitura correta do arco narrativo (bastidor → travessia → palco → recompensa) e a sensação de energia crescente antes de qualquer uso promocional. A prova de arranjo vocal muxada (`proof-v1`) não constitui gravação vocal oficial definitiva.
