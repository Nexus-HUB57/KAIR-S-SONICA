from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from kairos_core.config import Settings

CanonicalMediaKind = Literal["image", "video", "audio", "multimedia"]
ReviewDecision = Literal["READY_FOR_APPROVAL", "REJECTED"]
FindingSeverity = Literal["INFO", "WARNING", "BLOCKER"]
RepairStatus = Literal["APPLIED", "REQUIRES_HUMAN", "NOT_APPLIED"]

CANONICAL_ARTIST_ID = "kairos.khairus_the_dragon"
CANONICAL_VOICE_REFERENCE = "assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3"
CANONICAL_PHYSICAL_PROFILE = "ktd-physical-spec-v1"
CANONICAL_TATTOO_MAP = "dragon-diamond-v1"
CANONICAL_IDENTITY_PROFILE = "ktd-visual-canon-v1"


class AutoReviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    media_kind: CanonicalMediaKind = "multimedia"
    payload: dict[str, Any] = Field(default_factory=dict, max_length=128)
    auto_repair: bool = True


class AutoReviewFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str = Field(min_length=1, max_length=80)
    area: Literal["identity", "image", "video", "audio", "music", "governance"]
    severity: FindingSeverity
    message: str = Field(min_length=1, max_length=500)
    remediation: str = Field(min_length=1, max_length=500)
    automatic: bool = False
    status: Literal["PASS", "FLAGGED", "BLOCKED"]


class AutoReviewRepair(BaseModel):
    model_config = ConfigDict(extra="forbid")

    repair_id: str = Field(min_length=1, max_length=80)
    priority: Literal["P0", "P1", "P2"]
    area: Literal["identity", "image", "video", "audio", "music", "governance"]
    action: str = Field(min_length=1, max_length=500)
    status: RepairStatus
    automatic: bool
    requires_human_approval: bool


class AutoReviewResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    audit_id: str = Field(min_length=1, max_length=80)
    created_at: datetime
    media_kind: CanonicalMediaKind
    decision: ReviewDecision
    hard_gate_passed: bool
    identity_lock: dict[str, Any]
    findings: list[AutoReviewFinding] = Field(default_factory=list, max_length=64)
    roadmap: list[AutoReviewRepair] = Field(default_factory=list, max_length=64)
    normalized_payload: dict[str, Any] = Field(default_factory=dict, max_length=128)
    repairs_applied: list[str] = Field(default_factory=list, max_length=32)
    final_approval_required: bool = True
    auto_publish: bool = False


class AutoReviewEngine:
    """Gate determinístico anterior à produção de áudio, vídeo e imagem.

    O motor rejeita falhas de identidade e de política audiovisual, aplica apenas
    normalizações técnicas explicitamente seguras e devolve um roadmap legível.
    Ele não gera mídia, não escreve sobre assets existentes e não publica nada.
    """

    _forbidden_video_patterns = (
        r"\bstill\b",
        r"\bstatic\s+(?:image|photo|frame)\b",
        r"\bslideshow\b",
        r"\bken\s*burns\b",
        r"\bpan\s*/?\s*zoom\b",
        r"\bphoto\s+animation\b",
        r"\bimage\s+overlay\b",
        r"\boverlay\s+(?:image|photo)\b",
        r"\bimagem\s+(?:estática|sobreposta)\b",
        r"\bfoto\s+animada\b",
        r"\bken\s*burns\b",
    )

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def review(
        self,
        media_kind: CanonicalMediaKind,
        payload: dict[str, Any],
        *,
        auto_repair: bool = True,
        persist: bool = True,
    ) -> AutoReviewResult:
        normalized = dict(payload)
        findings: list[AutoReviewFinding] = []
        roadmap: list[AutoReviewRepair] = []
        repairs_applied: list[str] = []

        self._check_artist_identity(normalized, findings, roadmap, repairs_applied, auto_repair)
        if media_kind in {"image", "video", "multimedia"}:
            self._check_visual_identity(normalized, findings, roadmap, repairs_applied, auto_repair)
        if media_kind in {"audio", "multimedia"}:
            self._check_audio_identity(normalized, findings, roadmap, repairs_applied, auto_repair)
        if media_kind in {"video", "multimedia"}:
            self._check_video_policy(normalized, findings, roadmap, repairs_applied, auto_repair)
        self._check_governance(normalized, findings, roadmap)

        blockers = [finding for finding in findings if finding.severity == "BLOCKER"]
        decision: ReviewDecision = "REJECTED" if blockers else "READY_FOR_APPROVAL"
        result = AutoReviewResult(
            audit_id=f"audit-{uuid4().hex}",
            created_at=datetime.now(timezone.utc),
            media_kind=media_kind,
            decision=decision,
            hard_gate_passed=not blockers,
            identity_lock={
                "artist_id": CANONICAL_ARTIST_ID,
                "physical_profile": CANONICAL_PHYSICAL_PROFILE,
                "tattoo_map": CANONICAL_TATTOO_MAP,
                "voice_reference": CANONICAL_VOICE_REFERENCE,
                "immutable": True,
            },
            findings=findings,
            roadmap=roadmap,
            normalized_payload=normalized,
            repairs_applied=repairs_applied,
        )
        if persist:
            self._persist(result)
        return result

    @staticmethod
    def _check_artist_identity(
        payload: dict[str, Any],
        findings: list[AutoReviewFinding],
        roadmap: list[AutoReviewRepair],
        repairs_applied: list[str],
        auto_repair: bool,
    ) -> None:
        artist_id = payload.get("artist_id")
        if artist_id is None:
            if auto_repair:
                payload["artist_id"] = CANONICAL_ARTIST_ID
                repairs_applied.append("identity-lock-artist-id")
                repair_status: RepairStatus = "APPLIED"
                finding_status: Literal["PASS", "FLAGGED", "BLOCKED"] = "PASS"
                finding_severity: FindingSeverity = "INFO"
                finding_message = "artist_id ausente; o pedido foi normalizado para Kháirus."
            else:
                repair_status = "REQUIRES_HUMAN"
                finding_status = "FLAGGED"
                finding_severity = "WARNING"
                finding_message = "artist_id ausente; a auditoria não alterou o pedido."
            roadmap.append(
                AutoReviewRepair(
                    repair_id="identity-lock-artist-id",
                    priority="P0",
                    area="identity",
                    action="Fixar artist_id no identificador canônico de Kháirus.",
                    status=repair_status,
                    automatic=auto_repair,
                    requires_human_approval=not auto_repair,
                )
            )
            findings.append(
                AutoReviewFinding(
                    code="ID-LOCK-01",
                    area="identity",
                    severity=finding_severity,
                    message=finding_message,
                    remediation="Manter kairos.khairus_the_dragon em toda tarefa do projeto.",
                    automatic=auto_repair,
                    status=finding_status,
                )
            )
        elif artist_id != CANONICAL_ARTIST_ID:
            findings.append(
                AutoReviewFinding(
                    code="ID-LOCK-02",
                    area="identity",
                    severity="BLOCKER",
                    message="O pedido aponta para um artista diferente do cânone de Kháirus.",
                    remediation="Corrigir artist_id ou abrir um projeto separado; não alterar silenciosamente a identidade.",
                    automatic=False,
                    status="BLOCKED",
                )
            )
            roadmap.append(
                AutoReviewRepair(
                    repair_id="identity-artist-mismatch",
                    priority="P0",
                    area="identity",
                    action="Revisar manualmente o artista-alvo antes de qualquer produção.",
                    status="REQUIRES_HUMAN",
                    automatic=False,
                    requires_human_approval=True,
                )
            )

    @staticmethod
    def _check_visual_identity(
        payload: dict[str, Any],
        findings: list[AutoReviewFinding],
        roadmap: list[AutoReviewRepair],
        repairs_applied: list[str],
        auto_repair: bool,
    ) -> None:
        for field, expected, repair_id, label in (
            (
                "physical_profile",
                CANONICAL_PHYSICAL_PROFILE,
                "identity-physical-profile",
                "perfil físico",
            ),
            ("tattoo_map", CANONICAL_TATTOO_MAP, "identity-tattoo-map", "mapa de tatuagens"),
            (
                "identity_profile",
                CANONICAL_IDENTITY_PROFILE,
                "identity-visual-profile",
                "perfil visual",
            ),
        ):
            value = payload.get(field)
            if value is None:
                if auto_repair:
                    payload[field] = expected
                    repairs_applied.append(repair_id)
                    repair_status: RepairStatus = "APPLIED"
                else:
                    repair_status = "REQUIRES_HUMAN"
                roadmap.append(
                    AutoReviewRepair(
                        repair_id=repair_id,
                        priority="P0",
                        area="identity",
                        action=f"Fixar {label} no valor canônico {expected}.",
                        status=repair_status,
                        automatic=auto_repair,
                        requires_human_approval=not auto_repair,
                    )
                )
                if not auto_repair:
                    findings.append(
                        AutoReviewFinding(
                            code=f"ID-{field.upper()}-02",
                            area="identity",
                            severity="WARNING",
                            message=f"{label.capitalize()} ausente; a auditoria não alterou o pedido.",
                            remediation=f"Usar {expected} antes de produzir.",
                            automatic=False,
                            status="FLAGGED",
                        )
                    )
                continue
            if value != expected:
                findings.append(
                    AutoReviewFinding(
                        code=f"ID-{field.upper()}-01",
                        area="identity",
                        severity="BLOCKER",
                        message=f"{label.capitalize()} divergente do cânone imutável de Kháirus.",
                        remediation=f"Usar {expected}; nenhuma alteração de identidade pode ser feita sem autorização artística prévia.",
                        automatic=False,
                        status="BLOCKED",
                    )
                )
                roadmap.append(
                    AutoReviewRepair(
                        repair_id=f"identity-mismatch-{field}",
                        priority="P0",
                        area="identity",
                        action=f"Substituir ou revisar {field} com aprovação humana de KTD.",
                        status="REQUIRES_HUMAN",
                        automatic=False,
                        requires_human_approval=True,
                    )
                )

        if (
            payload.get("identity_modification_requested") is True
            or payload.get("modify_identity") is True
        ):
            findings.append(
                AutoReviewFinding(
                    code="IMG-IMMUTABLE-01",
                    area="image",
                    severity="BLOCKER",
                    message="O pedido solicita modificação da identidade física ou das tatuagens.",
                    remediation="Retirar a modificação ou anexar autorização artística explícita e reabrir o preflight.",
                    automatic=False,
                    status="BLOCKED",
                )
            )
            roadmap.append(
                AutoReviewRepair(
                    repair_id="identity-modification-approval",
                    priority="P0",
                    area="image",
                    action="Obter autorização prévia de KTD; o motor não edita a identidade automaticamente.",
                    status="REQUIRES_HUMAN",
                    automatic=False,
                    requires_human_approval=True,
                )
            )

        if auto_repair:
            payload["identity_lock"] = "immutable"
            payload["tattoo_continuity"] = "exact-canonical-map"

    def _check_audio_identity(
        self,
        payload: dict[str, Any],
        findings: list[AutoReviewFinding],
        roadmap: list[AutoReviewRepair],
        repairs_applied: list[str],
        auto_repair: bool,
    ) -> None:
        voice_reference = payload.get("voice_reference")
        if voice_reference is None:
            if auto_repair:
                payload["voice_reference"] = CANONICAL_VOICE_REFERENCE
                payload["voice_lock"] = "immutable-canonical-reference"
                repairs_applied.append("audio-lock-reference")
                repair_status: RepairStatus = "APPLIED"
            else:
                repair_status = "REQUIRES_HUMAN"
            roadmap.append(
                AutoReviewRepair(
                    repair_id="audio-lock-reference",
                    priority="P0",
                    area="audio",
                    action="Fixar a referência vocal oficial de KTD nos metadados do pedido.",
                    status=repair_status,
                    automatic=auto_repair,
                    requires_human_approval=not auto_repair,
                )
            )
            if not auto_repair:
                findings.append(
                    AutoReviewFinding(
                        code="AUD-VOICE-03",
                        area="audio",
                        severity="WARNING",
                        message="Referência vocal ausente; a auditoria não alterou o pedido.",
                        remediation=f"Usar somente {CANONICAL_VOICE_REFERENCE}.",
                        automatic=False,
                        status="FLAGGED",
                    )
                )
        elif voice_reference != CANONICAL_VOICE_REFERENCE:
            findings.append(
                AutoReviewFinding(
                    code="AUD-VOICE-01",
                    area="audio",
                    severity="BLOCKER",
                    message="A referência vocal indicada não é a âncora oficial de Kháirus.",
                    remediation=f"Usar somente {CANONICAL_VOICE_REFERENCE}; não substituir voz, timbre, sotaque ou identidade sem autorização.",
                    automatic=False,
                    status="BLOCKED",
                )
            )
            roadmap.append(
                AutoReviewRepair(
                    repair_id="audio-voice-reference-mismatch",
                    priority="P0",
                    area="audio",
                    action="Revisar a referência vocal e submeter novamente ao gate humano.",
                    status="REQUIRES_HUMAN",
                    automatic=False,
                    requires_human_approval=True,
                )
            )
        else:
            payload["voice_lock"] = "immutable-canonical-reference"

        if payload.get("voice_identity_override") is True or payload.get("voice_clone") is True:
            findings.append(
                AutoReviewFinding(
                    code="AUD-VOICE-02",
                    area="audio",
                    severity="BLOCKER",
                    message="O pedido tenta substituir ou clonar a identidade vocal protegida.",
                    remediation="Remover o override/clonagem e usar a referência oficial com gravação autorizada.",
                    automatic=False,
                    status="BLOCKED",
                )
            )
            roadmap.append(
                AutoReviewRepair(
                    repair_id="audio-voice-override",
                    priority="P0",
                    area="audio",
                    action="Desativar override ou clonagem vocal; somente KTD aprova a tomada final.",
                    status="REQUIRES_HUMAN",
                    automatic=False,
                    requires_human_approval=True,
                )
            )

        if auto_repair:
            payload.setdefault("vocal_profile", "medium-low-front-clear-controlled-aggression")
            payload.setdefault("performance_profile", "syncopated-double-time-half-time")

    def _check_video_policy(
        self,
        payload: dict[str, Any],
        findings: list[AutoReviewFinding],
        roadmap: list[AutoReviewRepair],
        repairs_applied: list[str],
        auto_repair: bool,
    ) -> None:
        prompt = str(payload.get("prompt") or "")
        lowered = prompt.lower()
        # A própria política exige que o brief declare "no stills", "no overlay", etc.
        # Essas negações não são pedidos proibidos e devem ser removidas antes do scan.
        negated_policy = re.compile(
            r"\b(?:no|without|never|sem|nunca)\s+"
            r"(?:(?:[a-zà-ÿ0-9/-]+|,)\s+){0,2}"
            r"(?:stills?|static\s+images?|slideshow|"
            r"photo\s+animation|image\s+overlay|overlay\s+(?:image|photo)|"
            r"imagem(?:\s+estática|\s+sobreposta)?|foto\s+animada|"
            r"ken\s*burns?(?:\s+pan\s*/?\s*zoom)?|pan\s*/?\s*zoom)\b",
            re.IGNORECASE,
        )
        scan_text = negated_policy.sub(" ", lowered)
        forbidden = [
            pattern for pattern in self._forbidden_video_patterns if re.search(pattern, scan_text)
        ]
        if (
            forbidden
            or payload.get("static_image_only") is True
            or payload.get("image_overlay") is True
        ):
            findings.append(
                AutoReviewFinding(
                    code="VID-POLICY-01",
                    area="video",
                    severity="BLOCKER",
                    message="O pedido contém still, imagem estática, sobreposição ou movimento de câmera sem performance real.",
                    remediation="Reescrever como vídeo live-action contínuo com ação física, câmera motivada e cenário temporal.",
                    automatic=False,
                    status="BLOCKED",
                )
            )
            roadmap.append(
                AutoReviewRepair(
                    repair_id="video-live-action-rewrite",
                    priority="P0",
                    area="video",
                    action="Reescrever o brief audiovisual e reabrir a auditoria; não converter foto em vídeo por pan/zoom.",
                    status="REQUIRES_HUMAN",
                    automatic=False,
                    requires_human_approval=True,
                )
            )
        if not re.search(
            r"live[- ]action|movimento físico|physical action|continuous camera|câmera contínua",
            lowered,
        ):
            constraint = " Live-action contínuo, ação física observável de KTD, câmera contínua motivada, cenário reagindo no tempo, sem still, sem imagem sobreposta e sem pan/zoom sobre foto."
            if auto_repair:
                payload["prompt"] = f"{prompt.strip()}{constraint}".strip()
                repairs_applied.append("video-live-action-constraint")
                repair_status: RepairStatus = "APPLIED"
            else:
                repair_status = "REQUIRES_HUMAN"
                findings.append(
                    AutoReviewFinding(
                        code="VID-POLICY-02",
                        area="video",
                        severity="WARNING",
                        message="O brief não declara movimento live-action suficiente; a auditoria não o alterou.",
                        remediation="Adicionar ação física, câmera contínua motivada e reação temporal do cenário.",
                        automatic=False,
                        status="FLAGGED",
                    )
                )
            roadmap.append(
                AutoReviewRepair(
                    repair_id="video-live-action-constraint",
                    priority="P1",
                    area="video",
                    action="Adicionar restrição automática de live-action, ação física e continuidade temporal ao brief.",
                    status=repair_status,
                    automatic=auto_repair,
                    requires_human_approval=not auto_repair,
                )
            )
        if auto_repair:
            payload["video_policy"] = "live-action-only-no-static-no-overlay"
            payload.setdefault("fps", 24)
            payload.setdefault("aspect_ratio", "9:16")
            payload.setdefault("continuous_motion_required", True)
            payload.setdefault("frame_review_required", True)

    @staticmethod
    def _check_governance(
        payload: dict[str, Any],
        findings: list[AutoReviewFinding],
        roadmap: list[AutoReviewRepair],
    ) -> None:
        if payload.get("source_manifest") is None:
            roadmap.append(
                AutoReviewRepair(
                    repair_id="governance-source-manifest",
                    priority="P1",
                    area="governance",
                    action="Registrar origem, licença, consentimento, versão e hash antes da aprovação final.",
                    status="REQUIRES_HUMAN",
                    automatic=False,
                    requires_human_approval=True,
                )
            )
            findings.append(
                AutoReviewFinding(
                    code="GOV-MANIFEST-01",
                    area="governance",
                    severity="WARNING",
                    message="A solicitação ainda não possui manifesto de origem completo.",
                    remediation="Completar proveniência, licença, consentimento, versão e hash antes de publicar.",
                    automatic=False,
                    status="FLAGGED",
                )
            )
        roadmap.append(
            AutoReviewRepair(
                repair_id="governance-human-approval",
                priority="P0",
                area="governance",
                action="Submeter a versão exata à aprovação humana de KTD antes de qualquer publicação.",
                status="REQUIRES_HUMAN",
                automatic=False,
                requires_human_approval=True,
            )
        )

    def _persist(self, result: AutoReviewResult) -> None:
        try:
            root = self.settings.studio_master_preflight_dir.expanduser()
            root.mkdir(parents=True, exist_ok=True)
            target = root / f"{result.audit_id}.json"
            partial = target.with_suffix(".json.part")
            partial.write_text(
                json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            partial.replace(target)
        except OSError:
            # Auditoria HTTP continua disponível mesmo quando o diretório não pode ser escrito.
            return
