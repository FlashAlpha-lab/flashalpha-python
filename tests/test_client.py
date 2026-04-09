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


@responses.activate
def test_zero_dte(fa):
    payload = {"symbol": "SPY", "regime": {"label": "positive_gamma"}, "pin_risk": {"pin_score": 82}, "decay": {"gamma_acceleration": 2.4}}
    responses.get(f"{BASE}/v1/exposure/zero-dte/SPY", json=payload)
    result = fa.zero_dte("SPY")
    assert result["pin_risk"]["pin_score"] == 82


@responses.activate
def test_zero_dte_with_strike_range(fa):
    payload = {"symbol": "SPY", "strikes": []}
    responses.get(f"{BASE}/v1/exposure/zero-dte/SPY", json=payload)
    fa.zero_dte("SPY", strike_range=0.05)
    assert "strike_range=0.05" in responses.calls[0].request.url


@responses.activate
def test_exposure_history(fa):
    payload = {"symbol": "SPY", "days": 7, "count": 5, "snapshots": []}
    responses.get(f"{BASE}/v1/exposure/history/SPY", json=payload)
    result = fa.exposure_history("SPY", days=7)
    assert result["days"] == 7


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


@responses.activate
def test_adv_volatility(fa):
    payload = {"symbol": "SPY", "svi_parameters": [{"expiry": "2026-04-04", "a": 0.0045}], "arbitrage_flags": []}
    responses.get(f"{BASE}/v1/adv_volatility/SPY", json=payload)
    result = fa.adv_volatility("SPY")
    assert result["svi_parameters"][0]["a"] == 0.0045


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


# ── Max Pain ────────────────────────────────────────────────────────


@responses.activate
def test_max_pain(fa):
    payload = {"symbol": "SPY", "max_pain_strike": 545, "pin_probability": 68}
    responses.get(f"{BASE}/v1/maxpain/SPY", json=payload)
    result = fa.max_pain("SPY")
    assert result["max_pain_strike"] == 545
    assert result["pin_probability"] == 68


@responses.activate
def test_max_pain_calls_correct_path(fa):
    responses.get(f"{BASE}/v1/maxpain/AAPL", json={})
    fa.max_pain("AAPL")
    assert "/v1/maxpain/AAPL" in responses.calls[0].request.url


@responses.activate
def test_max_pain_with_expiration(fa):
    responses.get(f"{BASE}/v1/maxpain/SPY", json={})
    fa.max_pain("SPY", expiration="2026-04-17")
    assert "expiration=2026-04-17" in responses.calls[0].request.url


@responses.activate
def test_max_pain_without_expiration(fa):
    responses.get(f"{BASE}/v1/maxpain/SPY", json={"max_pain_by_expiration": [{"expiration": "2026-04-17"}]})
    result = fa.max_pain("SPY")
    assert "max_pain_by_expiration" in result


@responses.activate
def test_max_pain_full_response(fa):
    payload = {
        "symbol": "SPY",
        "underlying_price": 548.32,
        "max_pain_strike": 545,
        "distance": {"absolute": 3.32, "percent": 0.61, "direction": "above"},
        "signal": "neutral",
        "put_call_oi_ratio": 1.284,
        "pain_curve": [{"strike": 545, "total_pain": 3700000}],
        "oi_by_strike": [{"strike": 545, "call_oi": 35000, "put_oi": 42000}],
        "dealer_alignment": {"alignment": "converging", "gamma_flip": 546},
        "regime": "positive_gamma",
        "expected_move": {"max_pain_within_expected_range": True},
        "pin_probability": 68,
    }
    responses.get(f"{BASE}/v1/maxpain/SPY", json=payload)
    result = fa.max_pain("SPY")
    assert result["distance"]["direction"] == "above"
    assert result["dealer_alignment"]["alignment"] == "converging"
    assert result["signal"] == "neutral"
    assert result["regime"] == "positive_gamma"


@responses.activate
def test_max_pain_403_tier_restricted(fa):
    responses.get(
        f"{BASE}/v1/maxpain/SPY",
        json={"status": "ERROR", "error": "tier_restricted", "message": "Requires Growth plan.", "current_plan": "Free", "required_plan": "Growth"},
        status=403,
    )
    with pytest.raises(TierRestrictedError) as exc:
        fa.max_pain("SPY")
    assert exc.value.current_plan == "Free"


# ── Screener ───────────────────────────────────────────────────────

import json as _json


def _screener_body(call):
    return _json.loads(call.request.body)


@responses.activate
def test_screener_empty(fa):
    payload = {
        "meta": {"total_count": 10, "returned_count": 10, "tier": "growth"},
        "data": [{"symbol": "SPY", "price": 656.01}],
    }
    responses.post(f"{BASE}/v1/screener", json=payload)
    result = fa.screener()
    assert result["meta"]["tier"] == "growth"
    assert result["data"][0]["symbol"] == "SPY"
    # Empty body
    assert _screener_body(responses.calls[0]) == {}


@responses.activate
def test_screener_sends_post_with_json_content_type(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(limit=5)
    req = responses.calls[0].request
    assert req.method == "POST"
    assert req.url == f"{BASE}/v1/screener"
    assert req.headers.get("Content-Type") == "application/json"
    assert req.headers.get("X-Api-Key") == "test-key"


@responses.activate
def test_screener_leaf_filter(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(filters={"field": "regime", "operator": "eq", "value": "positive_gamma"})
    body = _screener_body(responses.calls[0])
    assert body["filters"]["field"] == "regime"
    assert body["filters"]["operator"] == "eq"
    assert body["filters"]["value"] == "positive_gamma"


@responses.activate
def test_screener_and_group(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(
        filters={
            "op": "and",
            "conditions": [
                {"field": "regime", "operator": "eq", "value": "positive_gamma"},
                {"field": "harvest_score", "operator": "gte", "value": 65},
            ],
        },
        sort=[{"field": "harvest_score", "direction": "desc"}],
        select=["symbol", "price", "harvest_score"],
        limit=20,
    )
    body = _screener_body(responses.calls[0])
    assert body["filters"]["op"] == "and"
    assert len(body["filters"]["conditions"]) == 2
    assert body["limit"] == 20
    assert body["select"] == ["symbol", "price", "harvest_score"]
    assert body["sort"] == [{"field": "harvest_score", "direction": "desc"}]


@responses.activate
def test_screener_or_group(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(
        filters={
            "op": "or",
            "conditions": [
                {"field": "vrp_regime", "operator": "eq", "value": "toxic_short_vol"},
                {"field": "vrp_regime", "operator": "eq", "value": "event_only"},
            ],
        },
    )
    body = _screener_body(responses.calls[0])
    assert body["filters"]["op"] == "or"


@responses.activate
def test_screener_nested_and_inside_or(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(
        filters={
            "op": "or",
            "conditions": [
                {
                    "op": "and",
                    "conditions": [
                        {"field": "regime", "operator": "eq", "value": "positive_gamma"},
                        {"field": "harvest_score", "operator": "gte", "value": 70},
                    ],
                },
                {
                    "op": "and",
                    "conditions": [
                        {"field": "regime", "operator": "eq", "value": "negative_gamma"},
                        {"field": "atm_iv", "operator": "gte", "value": 50},
                    ],
                },
            ],
        },
    )
    body = _screener_body(responses.calls[0])
    assert body["filters"]["op"] == "or"
    assert body["filters"]["conditions"][0]["op"] == "and"
    assert body["filters"]["conditions"][1]["op"] == "and"


@responses.activate
def test_screener_between_operator(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(filters={"field": "atm_iv", "operator": "between", "value": [15, 25]})
    body = _screener_body(responses.calls[0])
    assert body["filters"]["operator"] == "between"
    assert body["filters"]["value"] == [15, 25]


@responses.activate
def test_screener_in_operator(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(filters={"field": "term_state", "operator": "in", "value": ["contango", "mixed"]})
    body = _screener_body(responses.calls[0])
    assert body["filters"]["operator"] == "in"
    assert body["filters"]["value"] == ["contango", "mixed"]


@responses.activate
def test_screener_null_operators(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(filters={"field": "vrp_regime", "operator": "is_not_null"})
    body = _screener_body(responses.calls[0])
    assert body["filters"]["operator"] == "is_not_null"
    assert "value" not in body["filters"]


@responses.activate
def test_screener_cascading_filters(fa):
    """Cascading filters on expiries/strikes/contracts levels."""
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(
        filters={
            "op": "and",
            "conditions": [
                {"field": "regime", "operator": "eq", "value": "positive_gamma"},
                {"field": "expiries.days_to_expiry", "operator": "lte", "value": 14},
                {"field": "strikes.call_oi", "operator": "gte", "value": 2000},
                {"field": "contracts.type", "operator": "eq", "value": "C"},
                {"field": "contracts.delta", "operator": "gte", "value": 0.3},
            ],
        },
        select=["*"],
    )
    body = _screener_body(responses.calls[0])
    fields = [c["field"] for c in body["filters"]["conditions"]]
    assert "expiries.days_to_expiry" in fields
    assert "strikes.call_oi" in fields
    assert "contracts.type" in fields
    assert "contracts.delta" in fields
    assert body["select"] == ["*"]


@responses.activate
def test_screener_with_formulas(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(
        formulas=[{"alias": "vrp_ratio", "expression": "atm_iv / rv_20d"}],
        filters={"formula": "vrp_ratio", "operator": "gte", "value": 1.2},
        sort=[{"formula": "vrp_ratio", "direction": "desc"}],
    )
    body = _screener_body(responses.calls[0])
    assert body["formulas"][0]["alias"] == "vrp_ratio"
    assert body["formulas"][0]["expression"] == "atm_iv / rv_20d"
    assert body["filters"]["formula"] == "vrp_ratio"
    assert body["sort"][0]["formula"] == "vrp_ratio"


@responses.activate
def test_screener_inline_formula(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(
        filters={"formula": "atm_iv - rv_20d", "operator": "gt", "value": 6},
    )
    body = _screener_body(responses.calls[0])
    assert body["filters"]["formula"] == "atm_iv - rv_20d"


@responses.activate
def test_screener_multi_sort(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(
        sort=[
            {"field": "dealer_flow_risk", "direction": "asc"},
            {"field": "harvest_score", "direction": "desc"},
        ],
        select=["symbol", "dealer_flow_risk", "harvest_score"],
    )
    body = _screener_body(responses.calls[0])
    assert len(body["sort"]) == 2
    assert body["sort"][0]["direction"] == "asc"
    assert body["sort"][1]["direction"] == "desc"


@responses.activate
def test_screener_pagination(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(limit=10, offset=10)
    body = _screener_body(responses.calls[0])
    assert body["limit"] == 10
    assert body["offset"] == 10


@responses.activate
def test_screener_negative_number(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(filters={"field": "net_gex", "operator": "lt", "value": -500000})
    body = _screener_body(responses.calls[0])
    assert body["filters"]["value"] == -500000


@responses.activate
def test_screener_select_star(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(select=["*"])
    body = _screener_body(responses.calls[0])
    assert body["select"] == ["*"]


@responses.activate
def test_screener_select_star_with_formula(fa):
    responses.post(f"{BASE}/v1/screener", json={"meta": {}, "data": []})
    fa.screener(
        formulas=[{"alias": "ratio", "expression": "call_wall / (put_wall + 30)"}],
        select=["*", "ratio"],
    )
    body = _screener_body(responses.calls[0])
    assert body["select"] == ["*", "ratio"]


@responses.activate
def test_screener_returns_response_structure(fa):
    payload = {
        "meta": {
            "total_count": 7,
            "returned_count": 7,
            "universe_size": 250,
            "offset": 0,
            "limit": 50,
            "tier": "alpha",
            "as_of": "2026-04-05T10:30:00Z",
        },
        "data": [
            {"symbol": "SPY", "price": 656.01, "regime": "positive_gamma", "atm_iv": 20.7}
        ],
    }
    responses.post(f"{BASE}/v1/screener", json=payload)
    result = fa.screener()
    assert result["meta"]["tier"] == "alpha"
    assert result["meta"]["universe_size"] == 250
    assert result["data"][0]["price"] == 656.01


@responses.activate
def test_screener_tier_restricted_alpha_field(fa):
    err_body = {
        "status": "ERROR",
        "error": "validation_error",
        "message": "Field 'harvest_score' requires the Alpha plan or higher.",
    }
    responses.post(f"{BASE}/v1/screener", json=err_body, status=400)
    with pytest.raises(FlashAlphaError) as exc:
        fa.screener(filters={"field": "harvest_score", "operator": "gte", "value": 65})
    assert exc.value.status_code == 400
    assert "Alpha" in str(exc.value)


@responses.activate
def test_screener_formula_error(fa):
    err_body = {
        "status": "ERROR",
        "error": "formula_error",
        "message": "Unexpected token '+' at position 5",
    }
    responses.post(f"{BASE}/v1/screener", json=err_body, status=400)
    with pytest.raises(FlashAlphaError):
        fa.screener(formulas=[{"alias": "bad", "expression": "+ atm_iv"}])


@responses.activate
def test_screener_tier_restricted_403(fa):
    err_body = {
        "status": "ERROR",
        "error": "tier_restricted",
        "message": "Screener requires Growth plan or higher.",
        "current_plan": "Free",
        "required_plan": "Growth",
    }
    responses.post(f"{BASE}/v1/screener", json=err_body, status=403)
    with pytest.raises(TierRestrictedError) as exc:
        fa.screener()
    assert exc.value.current_plan == "Free"
    assert exc.value.required_plan == "Growth"


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
