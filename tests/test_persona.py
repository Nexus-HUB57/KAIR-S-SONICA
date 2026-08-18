import json
from pathlib import Path

from kairos_core.persona import DEFAULT_PERSONA

ROOT = Path(__file__).resolve().parents[1]


def test_default_persona_has_stable_identity_and_guardrails() -> None:
    assert DEFAULT_PERSONA.id == "kairos.aai_apo"
    assert DEFAULT_PERSONA.version == "2.0.0"
    assert "Maestro Layer" in DEFAULT_PERSONA.roles
    assert any("proprietário" in rule for rule in DEFAULT_PERSONA.guardrails)
    assert "Você é Káiros" in DEFAULT_PERSONA.system_prompt


def test_persona_serialization_is_json_compatible() -> None:
    payload = DEFAULT_PERSONA.to_dict()
    encoded = json.dumps(payload, ensure_ascii=False)
    assert "kairos.aai_apo" in encoded
    assert isinstance(payload["roles"], list)
    assert isinstance(payload["guardrails"], list)


def test_persona_context_is_delimited() -> None:
    prompt = DEFAULT_PERSONA.prompt_with_context("Gerar um Boom Bap a 92 BPM")
    assert "CONTEXTO DESTA EXECUÇÃO" in prompt
    assert prompt.endswith("Gerar um Boom Bap a 92 BPM")


def test_versioned_manifest_matches_runtime_identity() -> None:
    manifest = json.loads((ROOT / "personas/kairos/manifest.json").read_text(encoding="utf-8"))
    assert manifest["id"] == DEFAULT_PERSONA.id
    assert manifest["version"] == DEFAULT_PERSONA.version
    assert manifest["runtime"]["python_module"] == "kairos_core.persona.DEFAULT_PERSONA"
