from __future__ import annotations

import re
from dataclasses import dataclass

from kairos_core.social.contracts import ActionType, PolicyDecision, SocialPlatform


@dataclass(frozen=True, slots=True)
class SocialPolicy:
    version: str = "social-policy-v1"
    min_llm_confidence: float = 0.78
    max_posts_per_run: int = 4

    def evaluate(
        self,
        *,
        action_type: ActionType,
        platform: SocialPlatform,
        text: str,
        content_state: str,
        autonomy_mode: str,
        llm_confidence: float = 1.0,
    ) -> PolicyDecision:
        reasons: list[str] = []
        lowered = text.lower()
        sensitive_patterns = (
            r"\b(?:suicide|suicídio|self[- ]?harm|autoagressão|kill yourself|mate-se)\b",
            r"\b(?:doxx|doxxing|telefone|phone number|cpf|credit card|cartão de crédito)\b",
            r"\b(?:hate speech|racial slur|ameaça|threat)\b",
        )
        if any(re.search(pattern, lowered) for pattern in sensitive_patterns):
            return PolicyDecision(
                allowed=False,
                decision="escalate",
                reasons=["Texto contém sinal de crise, dados pessoais, ameaça ou discurso de ódio."],
                policy_version=self.version,
                confidence=1.0,
            )
        if action_type == ActionType.PUBLISH and content_state not in {"approved", "released"}:
            reasons.append("Publicação exige conteúdo aprovado ou released; o agente pode apenas preparar o pacote.")
        if action_type in {ActionType.REPLY_COMMENT, ActionType.HIDE_COMMENT} and autonomy_mode == "simulate":
            reasons.append("Modo simulate não executa ações de comunidade.")
        if llm_confidence < self.min_llm_confidence:
            reasons.append("Confiança do LLM abaixo do limiar de autonomia.")
        if action_type in {ActionType.PUBLISH, ActionType.REPLY_COMMENT, ActionType.HIDE_COMMENT} and autonomy_mode == "collaborative":
            reasons.append("Modo collaborative registra a ação e pode delegar a um peer.")
        if reasons:
            decision = "escalate" if any("crise" in reason or "Confiança" in reason for reason in reasons) else "block"
            return PolicyDecision(
                allowed=False,
                decision=decision,
                reasons=reasons,
                policy_version=self.version,
                confidence=llm_confidence,
            )
        return PolicyDecision(
            allowed=True,
            decision="allow",
            reasons=[f"Ação {action_type.value} em {platform.value} aprovada pela política."],
            policy_version=self.version,
            confidence=llm_confidence,
        )
