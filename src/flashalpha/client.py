"""FlashAlpha API client."""

from __future__ import annotations

from typing import Any

import requests

from .exceptions import (
    AuthenticationError,
    FlashAlphaError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TierRestrictedError,
)

BASE_URL = "https://lab.flashalpha.com"


class FlashAlpha:
    """Thin wrapper around the FlashAlpha REST API.

    Parameters
    ----------
    api_key : str
        Your FlashAlpha API key from https://flashalpha.com
    base_url : str, optional
        Override the API base URL (for testing).
    timeout : float, optional
        Request timeout in seconds. Default 30.
    """

    def __init__(self, api_key: str, *, base_url: str = BASE_URL, timeout: float = 30):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers["X-Api-Key"] = api_key

    # ── internal ────────────────────────────────────────────────────

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict:
        url = f"{self.base_url}{path}"
        resp = self._session.get(url, params=params, timeout=self.timeout)
        return self._handle(resp)

    def _handle(self, resp: requests.Response) -> dict:
        if resp.status_code == 200:
            return resp.json()

        try:
            body = resp.json()
        except ValueError:
            body = {"detail": resp.text}

        msg = body.get("message") or body.get("detail") or resp.text

        if resp.status_code == 401:
            raise AuthenticationError(msg, status_code=401, response=body)
        if resp.status_code == 403:
            raise TierRestrictedError(
                msg,
                status_code=403,
                response=body,
                current_plan=body.get("current_plan"),
                required_plan=body.get("required_plan"),
            )
        if resp.status_code == 404:
            raise NotFoundError(msg, status_code=404, response=body)
        if resp.status_code == 429:
            raise RateLimitError(
                msg,
                status_code=429,
                response=body,
                retry_after=int(resp.headers.get("Retry-After", 0)) or None,
            )
        if resp.status_code >= 500:
            raise ServerError(msg, status_code=resp.status_code, response=body)

        raise FlashAlphaError(msg, status_code=resp.status_code, response=body)

    # ── Market Data ─────────────────────────────────────────────────

    def stock_quote(self, ticker: str) -> dict:
        """Live stock quote (bid/ask/mid/last)."""
        return self._get(f"/stockquote/{ticker}")

    def option_quote(
        self,
        ticker: str,
        *,
        expiry: str | None = None,
        strike: float | None = None,
        type: str | None = None,
    ) -> dict | list:
        """Option quotes with greeks. Requires Growth+."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        if strike is not None:
            params["strike"] = strike
        if type:
            params["type"] = type
        return self._get(f"/optionquote/{ticker}", params or None)

    def surface(self, symbol: str) -> dict:
        """Volatility surface grid (public, no auth required)."""
        return self._get(f"/v1/surface/{symbol}")

    def stock_summary(self, symbol: str) -> dict:
        """Comprehensive stock summary (price, vol, exposure, macro)."""
        return self._get(f"/v1/stock/{symbol}/summary")

    # ── Historical ──────────────────────────────────────────────────

    def historical_stock_quote(self, ticker: str, *, date: str, time: str | None = None) -> dict:
        """Historical stock quotes (minute-by-minute from ClickHouse)."""
        params: dict[str, Any] = {"date": date}
        if time:
            params["time"] = time
        return self._get(f"/historical/stockquote/{ticker}", params)

    def historical_option_quote(
        self,
        ticker: str,
        *,
        date: str,
        time: str | None = None,
        expiry: str | None = None,
        strike: float | None = None,
        type: str | None = None,
    ) -> dict:
        """Historical option quotes (minute-by-minute from ClickHouse)."""
        params: dict[str, Any] = {"date": date}
        if time:
            params["time"] = time
        if expiry:
            params["expiry"] = expiry
        if strike is not None:
            params["strike"] = strike
        if type:
            params["type"] = type
        return self._get(f"/historical/optionquote/{ticker}", params)

    # ── Exposure Analytics ──────────────────────────────────────────

    def gex(self, symbol: str, *, expiration: str | None = None, min_oi: int | None = None) -> dict:
        """Gamma exposure by strike."""
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        if min_oi is not None:
            params["min_oi"] = min_oi
        return self._get(f"/v1/exposure/gex/{symbol}", params or None)

    def dex(self, symbol: str, *, expiration: str | None = None) -> dict:
        """Delta exposure by strike."""
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        return self._get(f"/v1/exposure/dex/{symbol}", params or None)

    def vex(self, symbol: str, *, expiration: str | None = None) -> dict:
        """Vanna exposure by strike."""
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        return self._get(f"/v1/exposure/vex/{symbol}", params or None)

    def chex(self, symbol: str, *, expiration: str | None = None) -> dict:
        """Charm exposure by strike."""
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        return self._get(f"/v1/exposure/chex/{symbol}", params or None)

    def exposure_summary(self, symbol: str) -> dict:
        """Full exposure summary (GEX/DEX/VEX/CHEX + hedging). Requires Growth+."""
        return self._get(f"/v1/exposure/summary/{symbol}")

    def exposure_levels(self, symbol: str) -> dict:
        """Key support/resistance levels from options exposure."""
        return self._get(f"/v1/exposure/levels/{symbol}")

    def narrative(self, symbol: str) -> dict:
        """Verbal narrative analysis of exposure. Requires Growth+."""
        return self._get(f"/v1/exposure/narrative/{symbol}")

    # ── Pricing & Sizing ────────────────────────────────────────────

    def greeks(
        self,
        *,
        spot: float,
        strike: float,
        dte: float,
        sigma: float,
        type: str = "call",
        r: float | None = None,
        q: float | None = None,
    ) -> dict:
        """Full BSM greeks (first, second, third order)."""
        params: dict[str, Any] = {"spot": spot, "strike": strike, "dte": dte, "sigma": sigma, "type": type}
        if r is not None:
            params["r"] = r
        if q is not None:
            params["q"] = q
        return self._get("/v1/pricing/greeks", params)

    def iv(
        self,
        *,
        spot: float,
        strike: float,
        dte: float,
        price: float,
        type: str = "call",
        r: float | None = None,
        q: float | None = None,
    ) -> dict:
        """Implied volatility from market price."""
        params: dict[str, Any] = {"spot": spot, "strike": strike, "dte": dte, "price": price, "type": type}
        if r is not None:
            params["r"] = r
        if q is not None:
            params["q"] = q
        return self._get("/v1/pricing/iv", params)

    def kelly(
        self,
        *,
        spot: float,
        strike: float,
        dte: float,
        sigma: float,
        premium: float,
        mu: float,
        type: str = "call",
        r: float | None = None,
        q: float | None = None,
    ) -> dict:
        """Kelly criterion optimal position sizing. Requires Growth+."""
        params: dict[str, Any] = {
            "spot": spot,
            "strike": strike,
            "dte": dte,
            "sigma": sigma,
            "premium": premium,
            "mu": mu,
            "type": type,
        }
        if r is not None:
            params["r"] = r
        if q is not None:
            params["q"] = q
        return self._get("/v1/pricing/kelly", params)

    # ── Volatility Analytics ────────────────────────────────────────

    def volatility(self, symbol: str) -> dict:
        """Comprehensive volatility analysis. Requires Growth+."""
        return self._get(f"/v1/volatility/{symbol}")

    # ── Reference Data ──────────────────────────────────────────────

    def tickers(self) -> dict:
        """All available stock tickers."""
        return self._get("/v1/tickers")

    def options(self, ticker: str) -> dict:
        """Option chain metadata (expirations + strikes)."""
        return self._get(f"/v1/options/{ticker}")

    def symbols(self) -> dict:
        """Currently queried symbols with live data."""
        return self._get("/v1/symbols")

    # ── Account & System ────────────────────────────────────────────

    def account(self) -> dict:
        """Account info and quota."""
        return self._get("/v1/account")

    def health(self) -> dict:
        """Health check (public, no auth required)."""
        return self._get("/health")
