from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def request_json(method: str, url: str, token: str, body: bytes | None = None) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=body,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            value = json.loads(response.read().decode("utf-8"))
            return value if isinstance(value, dict) else {"data": value}
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(type(exc).__name__) from exc


def check_instagram() -> None:
    token = os.getenv("KTD_INSTAGRAM_ACCESS_TOKEN", "")
    expected_username = os.getenv("KTD_INSTAGRAM_EXPECTED_USERNAME", "khairusktd_ofc")
    if not token:
        raise RuntimeError("Instagram token ausente")
    params = urllib.parse.urlencode({"fields": "user_id,username,account_type"})
    payload = request_json("GET", f"https://graph.instagram.com/v26.0/me?{params}", token)
    data = payload.get("data", payload)
    record = data[0] if isinstance(data, list) and data else data
    if not isinstance(record, dict):
        raise RuntimeError("resposta Instagram sem conta")
    username = str(record.get("username", ""))
    if username.lower() != expected_username.lower():
        raise RuntimeError("Instagram username não corresponde ao perfil esperado")
    print(f"instagram_token_ok username={username} account_type={record.get('account_type', 'unknown')}")


def check_tiktok() -> None:
    token = os.getenv("KTD_TIKTOK_ACCESS_TOKEN", "")
    if not token:
        raise RuntimeError("TikTok token ausente")
    payload = request_json(
        "POST",
        "https://open.tiktokapis.com/v2/post/publish/creator_info/query/",
        token,
        body=b"{}",
    )
    if "error" in payload and payload.get("error") not in (None, "ok"):
        raise RuntimeError("TikTok creator_info retornou erro")
    print("tiktok_token_ok creator_info_ok=true")


def main() -> int:
    checks = {"instagram": check_instagram, "tiktok": check_tiktok}
    selected = os.getenv("KTD_SOCIAL_HEALTH_PLATFORMS", "instagram,tiktok").split(",")
    failed = False
    for name in selected:
        name = name.strip()
        if not name:
            continue
        try:
            checks[name]()
        except (KeyError, RuntimeError) as exc:
            print(f"{name}_token_check_failed reason={exc}", file=sys.stderr)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
