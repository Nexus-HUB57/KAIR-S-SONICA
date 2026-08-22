from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any, Iterable

_TOKEN_RE = re.compile(r"[\wÀ-ÿ]{3,}", re.UNICODE)


@dataclass(frozen=True, slots=True)
class CommentClassification:
    category: str
    priority: str
    requires_escalation: bool
    reasons: tuple[str, ...]
    normalized_text: str


@dataclass(frozen=True, slots=True)
class NextAction:
    action: str
    rationale: str
    confidence: float


def normalize_text(text: str) -> str:
    return " ".join(text.strip().lower().split())


def content_fingerprint(*parts: str) -> str:
    normalized = "\n".join(normalize_text(part) for part in parts)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def classify_comment(text: str) -> CommentClassification:
    normalized = normalize_text(text)
    tokens = set(_TOKEN_RE.findall(normalized))
    reasons: list[str] = []
    if not normalized:
        return CommentClassification("empty", "low", False, ("Comentário vazio.",), normalized)
    pii_markers = {"cpf", "telefone", "phone", "email", "cartão", "credit", "number"}
    crisis_markers = {"suicide", "suicídio", "selfharm", "autoagressão", "matar", "kill"}
    hate_markers = {"racista", "racismo", "hate", "slur", "ameaça", "threat"}
    spam_markers = {"dm", "whatsapp", "telegram", "crypto", "giveaway", "promoção", "promo"}
    if tokens & pii_markers:
        reasons.append("Possível dado pessoal ou solicitação de contato privado.")
        return CommentClassification("privacy", "critical", True, tuple(reasons), normalized)
    if tokens & crisis_markers:
        reasons.append("Possível crise ou autoagressão; não usar como conteúdo promocional.")
        return CommentClassification("crisis", "critical", True, tuple(reasons), normalized)
    if tokens & hate_markers:
        reasons.append("Possível discurso de ódio, ameaça ou assédio.")
        return CommentClassification("safety", "critical", True, tuple(reasons), normalized)
    if tokens & spam_markers or normalized.count("http") >= 2:
        reasons.append("Padrão compatível com spam ou solicitação de contato externo.")
        return CommentClassification("spam", "medium", False, tuple(reasons), normalized)
    if "?" in normalized or any(token in tokens for token in {"como", "when", "where", "what", "porquê", "porque"}):
        return CommentClassification("question", "high", False, ("Pergunta legítima pode receber resposta contextual.",), normalized)
    if any(token in tokens for token in {"love", "fire", "inspiring", "inspirador", "brabo", "amazing", "forte"}):
        return CommentClassification("positive", "medium", False, ("Reação positiva relacionada ao conteúdo.",), normalized)
    return CommentClassification("general", "low", False, ("Sem sinal suficiente para automação prioritária.",), normalized)


def rank_comments(classifications: Iterable[CommentClassification]) -> list[CommentClassification]:
    weights = {"critical": 100, "high": 60, "medium": 30, "low": 10}
    return sorted(classifications, key=lambda item: weights.get(item.priority, 0), reverse=True)


def choose_next_action(
    *,
    published: bool,
    qualified_comments: int,
    blocked_actions: int,
    recent_failure_rate: float,
    has_unanswered_question: bool,
) -> NextAction:
    if blocked_actions > 0 or recent_failure_rate >= 0.25:
        return NextAction("pause_and_review", "Há bloqueios ou falhas recentes demais para ampliar a automação.", 0.96)
    if has_unanswered_question:
        return NextAction("reply_question", "Existe pergunta qualificada sem resposta e baixo risco aparente.", 0.87)
    if published and qualified_comments >= 3:
        return NextAction("publish_follow_up", "A conversa qualificada sustenta um follow-up contextual, sem repetir o asset.", 0.76)
    return NextAction("collect_more_signal", "Ainda não há evidência suficiente para ampliar a campanha.", 0.72)


def summarize_signals(metrics: dict[str, Any]) -> dict[str, Any]:
    """Extrai sinais comparáveis sem inventar métricas ausentes."""
    numeric = {
        key: value
        for key, value in metrics.items()
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    }
    return {
        "observed_numeric_metrics": numeric,
        "missing_metrics": [key for key in ("reach", "views", "watch_time", "shares", "comments") if key not in metrics],
    }
