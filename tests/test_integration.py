"""Integration tests — hit the live FlashAlpha API.

Run with: pytest -m integration
Requires FLASHALPHA_API_KEY env var.
"""

import os

import pytest

from flashalpha import FlashAlpha, NotFoundError

API_KEY = os.environ.get("FLASHALPHA_API_KEY", "")

pytestmark = pytest.mark.integration


@pytest.fixture
def fa():
    if not API_KEY:
        pytest.skip("FLASHALPHA_API_KEY not set")
    return FlashAlpha(API_KEY)


# ── Health (public) ─────────────────────────────────────────────────


def test_health(fa):
    result = fa.health()
    assert "status" in result


# ── Account ─────────────────────────────────────────────────────────


def test_account(fa):
    result = fa.account()
    assert "plan" in result
    assert "user_id" in result


# ── Market Data ─────────────────────────────────────────────────────


def test_stock_quote(fa):
    result = fa.stock_quote("SPY")
    assert result["ticker"] == "SPY"
    assert isinstance(result["bid"], (int, float))
    assert isinstance(result["ask"], (int, float))
    assert result["ask"] >= result["bid"]


def test_stock_quote_not_found(fa):
    with pytest.raises(NotFoundError):
        fa.stock_quote("ZZZZZZZZZ")


def test_stock_summary(fa):
    result = fa.stock_summary("SPY")
    assert result["symbol"] == "SPY"
    assert "price" in result


def test_surface(fa):
    result = fa.surface("SPY")
    assert result is not None


# ── Exposure Analytics ──────────────────────────────────────────────


def test_gex(fa):
    result = fa.gex("SPY")
    assert result["symbol"] == "SPY"
    assert "net_gex" in result
    assert "gamma_flip" in result
    assert isinstance(result["strikes"], list)
    assert len(result["strikes"]) > 0

    strike = result["strikes"][0]
    assert "strike" in strike
    assert "call_gex" in strike
    assert "put_gex" in strike
    assert "net_gex" in strike


def test_dex(fa):
    result = fa.dex("SPY")
    assert result["symbol"] == "SPY"
    assert "net_dex" in result
    assert isinstance(result["strikes"], list)


def test_vex(fa):
    result = fa.vex("SPY")
    assert result["symbol"] == "SPY"
    assert "net_vex" in result


def test_chex(fa):
    result = fa.chex("SPY")
    assert result["symbol"] == "SPY"
    assert "net_chex" in result


def test_exposure_levels(fa):
    result = fa.exposure_levels("SPY")
    assert result["symbol"] == "SPY"
    levels = result["levels"]
    assert "gamma_flip" in levels
    assert "call_wall" in levels
    assert "put_wall" in levels


def test_exposure_summary(fa):
    result = fa.exposure_summary("SPY")
    assert result["symbol"] == "SPY"
    assert "exposures" in result
    assert "regime" in result


def test_narrative(fa):
    result = fa.narrative("SPY")
    assert result["symbol"] == "SPY"
    assert "narrative" in result
    assert "regime" in result["narrative"]


def test_zero_dte(fa):
    result = fa.zero_dte("SPY")
    assert result["symbol"] == "SPY"
    # May have no 0DTE expiry today — either way, response is valid
    if not result.get("no_zero_dte"):
        assert "regime" in result
        assert "pin_risk" in result
        assert "decay" in result


# ── Pricing ─────────────────────────────────────────────────────────


def test_greeks(fa):
    result = fa.greeks(spot=580, strike=580, dte=30, sigma=0.18, type="call")
    assert "theoretical_price" in result
    assert result["theoretical_price"] > 0
    assert "first_order" in result
    fo = result["first_order"]
    assert 0 < fo["delta"] < 1
    assert fo["gamma"] > 0
    assert fo["theta"] < 0
    assert fo["vega"] > 0
    assert "second_order" in result
    assert "third_order" in result


def test_greeks_put(fa):
    result = fa.greeks(spot=580, strike=580, dte=30, sigma=0.18, type="put")
    assert -1 < result["first_order"]["delta"] < 0


def test_iv(fa):
    result = fa.iv(spot=580, strike=580, dte=30, price=12.69, type="call")
    assert "implied_volatility" in result
    assert 0.10 < result["implied_volatility"] < 0.50
    assert "implied_volatility_pct" in result


def test_kelly(fa):
    result = fa.kelly(spot=580, strike=580, dte=30, sigma=0.18, premium=12.69, mu=0.12, type="call")
    assert "sizing" in result
    assert "analysis" in result
    assert "recommendation" in result
    assert result["sizing"]["kelly_fraction"] >= 0


# ── Volatility ──────────────────────────────────────────────────────


def test_volatility(fa):
    result = fa.volatility("SPY")
    assert result["symbol"] == "SPY"
    assert "atm_iv" in result
    assert "realized_vol" in result
    assert "iv_rv_spreads" in result


def test_adv_volatility(fa):
    # Alpha+ only — may get 403 on lower plans
    from flashalpha import TierRestrictedError
    try:
        result = fa.adv_volatility("SPY")
        assert result["symbol"] == "SPY"
        assert "svi_parameters" in result
        assert "total_variance_surface" in result
        assert "arbitrage_flags" in result
    except TierRestrictedError:
        pytest.skip("adv_volatility requires Alpha+ plan")


# ── Reference Data ──────────────────────────────────────────────────


def test_tickers(fa):
    result = fa.tickers()
    assert "tickers" in result
    assert isinstance(result["tickers"], list)
    assert len(result["tickers"]) > 0
    assert "SPY" in result["tickers"] or "AAPL" in result["tickers"]


def test_options(fa):
    result = fa.options("SPY")
    assert result["symbol"] == "SPY"
    assert "expirations" in result
    assert len(result["expirations"]) > 0


def test_symbols(fa):
    result = fa.symbols()
    assert "symbols" in result
    assert isinstance(result["symbols"], list)
