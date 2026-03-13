"""Unit tests for the FlashAlpha client — all API calls are mocked."""

import pytest
import responses

from flashalpha import (
    FlashAlpha,
    AuthenticationError,
    FlashAlphaError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TierRestrictedError,
)

BASE = "https://lab.flashalpha.com"


@pytest.fixture
def fa():
    return FlashAlpha("test-key")


# ── Error handling ──────────────────────────────────────────────────


@responses.activate
def test_401_raises_authentication_error(fa):
    responses.get(f"{BASE}/v1/account", json={"title": "Unauthorized", "status": 401, "detail": "Invalid API key."}, status=401)
    with pytest.raises(AuthenticationError) as exc_info:
        fa.account()
    assert exc_info.value.status_code == 401


@responses.activate
def test_403_raises_tier_restricted_error(fa):
    responses.get(
        f"{BASE}/v1/exposure/summary/SPY",
        json={"status": "ERROR", "error": "tier_restricted", "message": "Requires Growth plan.", "current_plan": "Free", "required_plan": "Growth"},
        status=403,
    )
    with pytest.raises(TierRestrictedError) as exc_info:
        fa.exposure_summary("SPY")
    assert exc_info.value.current_plan == "Free"
    assert exc_info.value.required_plan == "Growth"


@responses.activate
def test_404_raises_not_found_error(fa):
    responses.get(f"{BASE}/stockquote/ZZZZZ", json={"error": "symbol_not_found", "message": "No data for ZZZZZ."}, status=404)
    with pytest.raises(NotFoundError):
        fa.stock_quote("ZZZZZ")


@responses.activate
def test_429_raises_rate_limit_error(fa):
    responses.get(
        f"{BASE}/stockquote/SPY",
        json={"status": "ERROR", "error": "Quota exceeded", "message": "Quota exceeded."},
        status=429,
        headers={"Retry-After": "60"},
    )
    with pytest.raises(RateLimitError) as exc_info:
        fa.stock_quote("SPY")
    assert exc_info.value.retry_after == 60


@responses.activate
def test_500_raises_server_error(fa):
    responses.get(f"{BASE}/health", json={"detail": "Internal server error"}, status=500)
    with pytest.raises(ServerError) as exc_info:
        fa.health()
    assert exc_info.value.status_code == 500


@responses.activate
def test_unknown_error_raises_base(fa):
    responses.get(f"{BASE}/health", json={"detail": "Teapot"}, status=418)
    with pytest.raises(FlashAlphaError) as exc_info:
        fa.health()
    assert exc_info.value.status_code == 418


# ── Market Data ─────────────────────────────────────────────────────


@responses.activate
def test_stock_quote(fa):
    payload = {"ticker": "SPY", "bid": 600.0, "ask": 600.02, "mid": 600.01, "lastPrice": 600.01, "lastUpdate": "2026-03-01T16:00:00Z"}
    responses.get(f"{BASE}/stockquote/SPY", json=payload)
    result = fa.stock_quote("SPY")
    assert result["ticker"] == "SPY"
    assert result["bid"] == 600.0


@responses.activate
def test_option_quote_with_filters(fa):
    payload = {"underlying": "SPY", "type": "C", "expiry": "2026-03-20", "strike": 590.0, "delta": 0.65}
    responses.get(f"{BASE}/optionquote/SPY", json=payload)
    result = fa.option_quote("SPY", expiry="2026-03-20", strike=590, type="C")
    assert result["delta"] == 0.65


@responses.activate
def test_surface(fa):
    responses.get(f"{BASE}/v1/surface/SPY", json={"symbol": "SPY", "data": []})
    result = fa.surface("SPY")
    assert result["symbol"] == "SPY"


@responses.activate
def test_stock_summary(fa):
    responses.get(f"{BASE}/v1/stock/SPY/summary", json={"symbol": "SPY", "market_open": True})
    result = fa.stock_summary("SPY")
    assert result["symbol"] == "SPY"


# ── Historical ──────────────────────────────────────────────────────


@responses.activate
def test_historical_stock_quote(fa):
    payload = {"ticker": "SPY", "date": "2026-03-05", "count": 1, "rows": []}
    responses.get(f"{BASE}/historical/stockquote/SPY", json=payload)
    result = fa.historical_stock_quote("SPY", date="2026-03-05", time="10:30")
    assert result["date"] == "2026-03-05"
    # Verify query params were sent
    assert "date=2026-03-05" in responses.calls[0].request.url
    assert "time=10%3A30" in responses.calls[0].request.url


@responses.activate
def test_historical_option_quote(fa):
    payload = {"ticker": "SPY", "date": "2026-03-05", "count": 1, "rows": []}
    responses.get(f"{BASE}/historical/optionquote/SPY", json=payload)
    result = fa.historical_option_quote("SPY", date="2026-03-05", expiry="2026-03-20", strike=580, type="C")
    assert result["count"] == 1


# ── Exposure Analytics ──────────────────────────────────────────────


@responses.activate
def test_gex(fa):
    payload = {"symbol": "SPY", "net_gex": 2850000000, "gamma_flip": 595.25, "strikes": []}
    responses.get(f"{BASE}/v1/exposure/gex/SPY", json=payload)
    result = fa.gex("SPY")
    assert result["net_gex"] == 2850000000


@responses.activate
def test_gex_with_filters(fa):
    payload = {"symbol": "SPY", "strikes": []}
    responses.get(f"{BASE}/v1/exposure/gex/SPY", json=payload)
    fa.gex("SPY", expiration="2026-03-20", min_oi=100)
    assert "expiration=2026-03-20" in responses.calls[0].request.url
    assert "min_oi=100" in responses.calls[0].request.url


@responses.activate
def test_dex(fa):
    payload = {"symbol": "SPY", "net_dex": -450000000, "strikes": []}
    responses.get(f"{BASE}/v1/exposure/dex/SPY", json=payload)
    result = fa.dex("SPY")
    assert result["net_dex"] == -450000000


@responses.activate
def test_vex(fa):
    payload = {"symbol": "SPY", "net_vex": 1200000000, "strikes": []}
    responses.get(f"{BASE}/v1/exposure/vex/SPY", json=payload)
    result = fa.vex("SPY")
    assert result["net_vex"] == 1200000000


@responses.activate
def test_chex(fa):
    payload = {"symbol": "SPY", "net_chex": 850000000, "strikes": []}
    responses.get(f"{BASE}/v1/exposure/chex/SPY", json=payload)
    result = fa.chex("SPY")
    assert result["net_chex"] == 850000000


@responses.activate
def test_exposure_summary(fa):
    payload = {"symbol": "SPY", "regime": "positive_gamma", "exposures": {}}
    responses.get(f"{BASE}/v1/exposure/summary/SPY", json=payload)
    result = fa.exposure_summary("SPY")
    assert result["regime"] == "positive_gamma"


@responses.activate
def test_exposure_levels(fa):
    payload = {"symbol": "SPY", "levels": {"gamma_flip": 595.25, "call_wall": 600, "put_wall": 590}}
    responses.get(f"{BASE}/v1/exposure/levels/SPY", json=payload)
    result = fa.exposure_levels("SPY")
    assert result["levels"]["call_wall"] == 600


@responses.activate
def test_narrative(fa):
    payload = {"symbol": "SPY", "narrative": {"regime": "Dealers long gamma.", "outlook": "Range-bound."}}
    responses.get(f"{BASE}/v1/exposure/narrative/SPY", json=payload)
    result = fa.narrative("SPY")
    assert "regime" in result["narrative"]


# ── Pricing ─────────────────────────────────────────────────────────


@responses.activate
def test_greeks(fa):
    payload = {"theoretical_price": 12.687, "first_order": {"delta": 0.53, "gamma": 0.013}}
    responses.get(f"{BASE}/v1/pricing/greeks", json=payload)
    result = fa.greeks(spot=580, strike=580, dte=30, sigma=0.18)
    assert result["first_order"]["delta"] == 0.53


@responses.activate
def test_iv(fa):
    payload = {"implied_volatility": 0.18, "implied_volatility_pct": 18.0}
    responses.get(f"{BASE}/v1/pricing/iv", json=payload)
    result = fa.iv(spot=580, strike=580, dte=30, price=12.69)
    assert result["implied_volatility_pct"] == 18.0


@responses.activate
def test_kelly(fa):
    payload = {"sizing": {"kelly_fraction": 0.077, "half_kelly": 0.038}, "recommendation": "Risk 3.8%"}
    responses.get(f"{BASE}/v1/pricing/kelly", json=payload)
    result = fa.kelly(spot=580, strike=580, dte=30, sigma=0.18, premium=12.69, mu=0.12)
    assert result["sizing"]["kelly_fraction"] == 0.077


# ── Volatility ──────────────────────────────────────────────────────


@responses.activate
def test_volatility(fa):
    payload = {"symbol": "TSLA", "atm_iv": 48.5, "realized_vol": {"rv_20d": 45.8}}
    responses.get(f"{BASE}/v1/volatility/TSLA", json=payload)
    result = fa.volatility("TSLA")
    assert result["atm_iv"] == 48.5


# ── Reference Data ──────────────────────────────────────────────────


@responses.activate
def test_tickers(fa):
    payload = {"tickers": ["AAPL", "SPY"], "count": 2}
    responses.get(f"{BASE}/v1/tickers", json=payload)
    result = fa.tickers()
    assert result["count"] == 2


@responses.activate
def test_options(fa):
    payload = {"symbol": "SPY", "expirations": [], "expiration_count": 0}
    responses.get(f"{BASE}/v1/options/SPY", json=payload)
    result = fa.options("SPY")
    assert result["symbol"] == "SPY"


@responses.activate
def test_symbols(fa):
    payload = {"symbols": ["SPY", "QQQ"], "count": 2}
    responses.get(f"{BASE}/v1/symbols", json=payload)
    result = fa.symbols()
    assert result["count"] == 2


# ── Account & System ────────────────────────────────────────────────


@responses.activate
def test_account(fa):
    payload = {"plan": "pro", "daily_limit": "unlimited", "usage_today": 0}
    responses.get(f"{BASE}/v1/account", json=payload)
    result = fa.account()
    assert result["plan"] == "pro"


@responses.activate
def test_health(fa):
    payload = {"status": "Healthy"}
    responses.get(f"{BASE}/health", json=payload)
    result = fa.health()
    assert result["status"] == "Healthy"


# ── Client config ──────────────────────────────────────────────────


def test_api_key_in_header():
    fa = FlashAlpha("my-secret-key")
    assert fa._session.headers["X-Api-Key"] == "my-secret-key"


def test_custom_base_url():
    fa = FlashAlpha("key", base_url="https://custom.api.com/")
    assert fa.base_url == "https://custom.api.com"


def test_custom_timeout():
    fa = FlashAlpha("key", timeout=10)
    assert fa.timeout == 10
