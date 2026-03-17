from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests

DEFAULT_TIMEOUT = 20
class BillingError(Exception):
    pass


class BillingClient:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.config = self._load_json(self.base_dir / "config.json")
        self.local_config = self._load_json(self.base_dir / "config.local.json", required=False) or {}
        self.api_url = self.config["billing_api_url"].rstrip("/")
        self.skill_id = self.config["skill_id"]
        self.scan_price_usdt = float(self.config.get("scan_price_usdt", 0.1))
        self.api_key = self._resolve_api_key()
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    @staticmethod
    def _load_json(path: Path, required: bool = True) -> Optional[Dict[str, Any]]:
        if not path.exists():
            if required:
                raise BillingError(f"Missing config file: {path}")
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise BillingError(f"Failed to load JSON from {path}: {exc}") from exc

    def _resolve_api_key(self) -> str:
        env_name = self.config.get("api_key_env", "SKILLPAY_API_KEY")
        env_key = os.getenv(env_name, "").strip()
        if env_key:
            return env_key
        local_key = str(self.local_config.get("billing_api_key", "")).strip()
        if local_key:
            return local_key
        raise BillingError(
            f"Missing billing API key. Set env {env_name} or write billing_api_key in config.local.json"
        )

    def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        url = f"{self.api_url}{path}"
        try:
            resp = requests.request(method, url, headers=self.headers, timeout=DEFAULT_TIMEOUT, **kwargs)
        except requests.RequestException as exc:
            raise BillingError(f"Billing request failed: {exc}") from exc
        try:
            data = resp.json()
        except Exception as exc:
            raise BillingError(f"Billing API returned non-JSON response: {resp.text[:300]}") from exc
        if resp.status_code >= 400:
            message = data.get("message") or data.get("error") or f"HTTP {resp.status_code}"
            raise BillingError(f"Billing API error: {message}")
        return data

    def check_balance(self, user_id: str) -> float:
        data = self._request(
            "GET",
            "/api/v1/billing/balance",
            params={"user_id": user_id},
        )
        return float(data["balance"])

    def charge_user(self, user_id: str) -> Dict[str, Any]:
        data = self._request(
            "POST",
            "/api/v1/billing/charge",
            json={
                "user_id": user_id,
                "skill_id": self.skill_id,
                "amount": self.scan_price_usdt,
            },
        )
        success = bool(data.get("success"))
        payment_url = data.get("payment_url")
        if not success and not payment_url:
            try:
                payment_url = self.get_payment_link(user_id, self.scan_price_usdt)
            except Exception:
                payment_url = None
        result = {
            "ok": success,
            "balance": float(data.get("balance", 0.0)),
            "payment_url": payment_url,
            "raw": data,
        }
        return result

    def get_payment_link(self, user_id: str, amount: float) -> str:
        data = self._request(
            "POST",
            "/api/v1/billing/payment-link",
            json={"user_id": user_id, "amount": amount},
        )
        return str(data["payment_url"])
