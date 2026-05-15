"""Integration tests — hit the live FlashAlpha API.

Run with: pytest -m integration
Requires FLASHALPHA_API_KEY env var.
"""

import os
from typing import get_args

import pytest

from flashalpha import (
    AdvVolArbitrageFlag,
    AdvVolForwardPrice,
    AdvVolGreekSurface,
    AdvVolGreeksSurfaces,
    AdvVolSviParam,
    AdvVolTotalVarianceSurface,
    AdvVolVarianceSwap,
    AdvVolatilityResponse,
    ChexResponse,
    ChexStrikeRow,
    DexResponse,
    DexStrikeRow,
    ExposureLevelsResponse,
    FlashAlpha,
    GexResponse,
    GexStrikeRow,
    NarrativeData,
    NarrativeOiChange,
    NarrativeResponse,
    NotFoundError,
    OptionQuoteResponse,
    PricingAdditional,
    PricingFirstOrder,
    PricingGreeksResponse,
    PricingInputs,
    PricingSecondOrder,
    PricingThirdOrder,
    StockQuoteResponse,
    StockSummaryExposure,
    StockSummaryFearAndGreed,
    StockSummaryHedgingEstimate,
    StockSummaryHedgingMove,
    StockSummaryInterpretation,
    StockSummaryMacro,
    StockSummaryMacroIndex,
    StockSummaryOptionsFlow,
    StockSummaryPrice,
    StockSummaryResponse,
    StockSummarySkew25d,
    StockSummaryVixFutures,
    StockSummaryVixTermLevels,
    StockSummaryVixTermStructure,
    StockSummaryVolatility,
    StockSummaryZeroDte,
    SurfaceResponse,
    TierRestrictedError,
    VexResponse,
    VexStrikeRow,
    VolatilityGexByDte,
    VolatilityHedgingScenario,
    VolatilityIvDispersion,
    VolatilityIvRvSpreads,
    VolatilityLiquidity,
    VolatilityOiConcentration,
    VolatilityPcByExpiry,
    VolatilityPcByMoneyness,
    VolatilityPutCallProfile,
    VolatilityRealizedVol,
    VolatilityResponse,
    VolatilitySkewProfile,
    VolatilityTermStructure,
    VolatilityThetaByDte,
)

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
    """Every field declared in ExposureSummaryResponse must be referenced."""
    result = fa.exposure_summary("SPY")
    # ── top-level scalars ──
    assert result["symbol"] == "SPY"
    assert "underlying_price" in result and isinstance(result["underlying_price"], (int, float))
    assert isinstance(result["as_of"], str) and result["as_of"]
    assert isinstance(result["gamma_flip"], (int, float))
    assert result["regime"] in ("positive_gamma", "negative_gamma", "unknown")
    # ── exposures block (4 fields) ──
    e = result["exposures"]
    for k in ("net_gex", "net_dex", "net_vex", "net_chex"):
        assert isinstance(e[k], (int, float)), f"exposures.{k}"
    # ── interpretation block (3 fields) ──
    interp = result["interpretation"]
    for k in ("gamma", "vanna", "charm"):
        assert isinstance(interp[k], str) and interp[k], f"interpretation.{k}"
    # ── hedging_estimate (every leaf field on both sides) ──
    h = result["hedging_estimate"]
    up, down = h["spot_up_1pct"], h["spot_down_1pct"]
    for side in (up, down):
        # Both summary + zero-dte return lowercase.
        assert side["direction"] in ("buy", "sell")
        assert isinstance(side["dealer_shares_to_trade"], (int, float))
        assert isinstance(side["notional_usd"], (int, float))
        assert side["notional_usd"] != 0
    assert up["dealer_shares_to_trade"] == -down["dealer_shares_to_trade"]
    # ── zero_dte block (3 fields) ──
    z = result["zero_dte"]
    assert isinstance(z, dict)
    assert "net_gex" in z and (z["net_gex"] is None or isinstance(z["net_gex"], (int, float)))
    assert "pct_of_total_gex" in z and (
        z["pct_of_total_gex"] is None or isinstance(z["pct_of_total_gex"], (int, float))
    )
    assert "expiration" in z and (z["expiration"] is None or isinstance(z["expiration"], str))


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


def test_zero_dte_new_fields(fa):
    """Validate the full zero-DTE response shape including the v0.3.4 fields:
    distance-to-flip in dollars/sigmas, sub-score breakdown for pin_score,
    fine-grained hedging buckets (10bp/25bp/50bp/100bp + convexity_at_spot),
    flow concentration (atm/top-3 + net_call_minus_put_volume), wall-strength
    and level-cluster scores, the new liquidity and metadata sections, and
    per-strike greeks/quotes/spreads.

    Uses SPX which has daily 0DTE — falls back gracefully on weekends/holidays.
    """
    result = fa.zero_dte("SPX")
    assert result["symbol"] == "SPX"

    if result.get("no_zero_dte"):
        # Weekend / holiday — response is just a stub, nothing else to verify
        assert "next_zero_dte_expiry" in result
        return

    # ── top-level ──────────────────────────────────────────────────────
    for k in ("underlying_price", "expiration", "as_of", "market_open",
              "time_to_close_hours", "time_to_close_pct"):
        assert k in result, f"top-level {k} missing"

    # ── regime ─────────────────────────────────────────────────────────
    regime = result["regime"]
    for k in ("label", "description", "gamma_flip", "spot_vs_flip", "spot_to_flip_pct",
              "distance_to_flip_dollars", "distance_to_flip_sigmas"):
        assert k in regime, f"regime.{k} missing"

    # ── exposures ──────────────────────────────────────────────────────
    exposures = result["exposures"]
    for k in ("net_gex", "net_dex", "net_vex", "net_chex",
              "pct_of_total_gex", "total_chain_net_gex"):
        assert k in exposures, f"exposures.{k} missing"

    # ── expected_move ──────────────────────────────────────────────────
    em = result["expected_move"]
    for k in ("implied_1sd_dollars", "implied_1sd_pct", "remaining_1sd_dollars",
              "remaining_1sd_pct", "upper_bound", "lower_bound",
              "straddle_price", "atm_iv"):
        assert k in em, f"expected_move.{k} missing"

    # ── pin_risk ───────────────────────────────────────────────────────
    pr = result["pin_risk"]
    for k in ("magnet_strike", "magnet_gex", "distance_to_magnet_pct",
              "pin_score", "components", "max_pain",
              "oi_concentration_top3_pct", "description"):
        assert k in pr, f"pin_risk.{k} missing"
    components = pr["components"]
    for k in ("oi_score", "proximity_score", "time_score", "gamma_score"):
        assert k in components, f"pin_risk.components.{k} missing"

    # ── hedging — fine-grained buckets + convexity ─────────────────────
    hedging = result["hedging"]
    for bucket in ("spot_up_10bp", "spot_down_10bp",
                   "spot_up_25bp", "spot_down_25bp",
                   "spot_up_half_pct", "spot_down_half_pct",
                   "spot_up_1pct", "spot_down_1pct"):
        assert bucket in hedging, f"hedging.{bucket} missing"
        b = hedging[bucket]
        for k in ("dealer_shares_to_trade", "direction", "notional_usd"):
            assert k in b, f"hedging.{bucket}.{k} missing"
    assert "convexity_at_spot" in hedging

    # ── decay ──────────────────────────────────────────────────────────
    decay = result["decay"]
    for k in ("net_theta_dollars", "theta_per_hour_remaining", "charm_regime",
              "charm_description", "gamma_acceleration", "description"):
        assert k in decay, f"decay.{k} missing"

    # ── vol_context ────────────────────────────────────────────────────
    vc = result["vol_context"]
    for k in ("zero_dte_atm_iv", "seven_dte_atm_iv", "iv_ratio_0dte_7dte",
              "vix", "vanna_exposure", "vanna_interpretation", "description"):
        assert k in vc, f"vol_context.{k} missing"

    # ── flow ───────────────────────────────────────────────────────────
    flow = result["flow"]
    for k in ("total_volume", "call_volume", "put_volume",
              "net_call_minus_put_volume",
              "total_oi", "call_oi", "put_oi",
              "pc_ratio_volume", "pc_ratio_oi", "volume_to_oi_ratio",
              "atm_volume_share_pct", "top3_strike_volume_pct"):
        assert k in flow, f"flow.{k} missing"

    # ── levels ─────────────────────────────────────────────────────────
    levels = result["levels"]
    for k in ("call_wall", "call_wall_gex", "call_wall_strength",
              "distance_to_call_wall_pct",
              "put_wall", "put_wall_gex", "put_wall_strength",
              "distance_to_put_wall_pct",
              "distance_to_magnet_dollars",
              "highest_oi_strike", "highest_oi_total",
              "max_positive_gamma", "max_negative_gamma",
              "level_cluster_score"):
        assert k in levels, f"levels.{k} missing"

    # ── liquidity (new section) ────────────────────────────────────────
    liquidity = result["liquidity"]
    for k in ("atm_spread_pct", "weighted_spread_pct", "execution_score"):
        assert k in liquidity, f"liquidity.{k} missing"

    # ── metadata (new section) ─────────────────────────────────────────
    metadata = result["metadata"]
    for k in ("snapshot_age_seconds", "chain_contract_count",
              "data_quality_score", "greek_smoothness_score"):
        assert k in metadata, f"metadata.{k} missing"

    # ── per-strike entries ─────────────────────────────────────────────
    strikes = result["strikes"]
    assert isinstance(strikes, list)
    if strikes:
        s = strikes[0]
        for k in ("strike", "distance_from_spot_pct",
                  "call_symbol", "put_symbol",
                  "call_gex", "put_gex", "net_gex",
                  "call_dex", "put_dex", "net_dex",
                  "net_vex", "net_chex",
                  "call_oi", "put_oi", "call_volume", "put_volume",
                  "gex_share_pct", "oi_share_pct", "volume_share_pct",
                  "call_iv", "put_iv",
                  "call_delta", "put_delta",
                  "call_gamma", "put_gamma",
                  "call_theta", "put_theta",
                  "call_mid", "put_mid",
                  "call_spread_pct", "put_spread_pct"):
            assert k in s, f"strikes[0].{k} missing"


def test_zero_dte_typed_response(fa):
    """Comprehensive end-to-end test of the typed ``ZeroDteResponse``.

    Mirrors ``test_zero_dte_new_fields`` field-for-field, but reads via the
    typed paths (``r["regime"]["distance_to_flip_dollars"]`` is fine because
    ``ZeroDteResponse`` is a ``TypedDict`` — at runtime it's identical to
    ``dict``). The point is to lock in that every documented field name
    in the Python type definitions matches what the API actually ships.
    """
    from flashalpha.types import ZeroDteResponse

    r: ZeroDteResponse = fa.zero_dte("SPX")
    assert r["symbol"] == "SPX"

    if r.get("no_zero_dte"):
        assert "next_zero_dte_expiry" in r
        return

    # Top-level
    assert isinstance(r["underlying_price"], (int, float))
    assert "expiration" in r
    assert isinstance(r["as_of"], str)
    assert isinstance(r["market_open"], bool)
    assert "time_to_close_hours" in r
    assert "time_to_close_pct" in r

    # regime
    regime = r["regime"]
    for k in ("label", "description", "gamma_flip", "spot_vs_flip", "spot_to_flip_pct",
              "distance_to_flip_dollars", "distance_to_flip_sigmas"):
        assert k in regime, f"regime.{k} missing in typed access"

    # exposures
    exposures = r["exposures"]
    for k in ("net_gex", "net_dex", "net_vex", "net_chex",
              "pct_of_total_gex", "total_chain_net_gex"):
        assert k in exposures, f"exposures.{k} missing in typed access"

    # expected_move
    em = r["expected_move"]
    for k in ("implied_1sd_dollars", "implied_1sd_pct",
              "remaining_1sd_dollars", "remaining_1sd_pct",
              "upper_bound", "lower_bound",
              "straddle_price", "atm_iv"):
        assert k in em, f"expected_move.{k} missing in typed access"

    # pin_risk
    pr = r["pin_risk"]
    for k in ("magnet_strike", "magnet_gex", "distance_to_magnet_pct",
              "pin_score", "components", "max_pain",
              "oi_concentration_top3_pct", "description"):
        assert k in pr, f"pin_risk.{k} missing in typed access"
    for k in ("oi_score", "proximity_score", "time_score", "gamma_score"):
        assert k in pr["components"], f"pin_risk.components.{k} missing"

    # hedging
    hedging = r["hedging"]
    for bucket in ("spot_up_10bp", "spot_down_10bp",
                   "spot_up_25bp", "spot_down_25bp",
                   "spot_up_half_pct", "spot_down_half_pct",
                   "spot_up_1pct", "spot_down_1pct"):
        assert bucket in hedging, f"hedging.{bucket} missing in typed access"
        for k in ("dealer_shares_to_trade", "direction", "notional_usd"):
            assert k in hedging[bucket], f"hedging.{bucket}.{k} missing"
    assert "convexity_at_spot" in hedging

    # decay
    for k in ("net_theta_dollars", "theta_per_hour_remaining", "charm_regime",
              "charm_description", "gamma_acceleration", "description"):
        assert k in r["decay"], f"decay.{k} missing in typed access"

    # vol_context
    for k in ("zero_dte_atm_iv", "seven_dte_atm_iv", "iv_ratio_0dte_7dte",
              "vix", "vanna_exposure", "vanna_interpretation", "description"):
        assert k in r["vol_context"], f"vol_context.{k} missing in typed access"

    # flow
    for k in ("total_volume", "call_volume", "put_volume",
              "net_call_minus_put_volume",
              "total_oi", "call_oi", "put_oi",
              "pc_ratio_volume", "pc_ratio_oi", "volume_to_oi_ratio",
              "atm_volume_share_pct", "top3_strike_volume_pct"):
        assert k in r["flow"], f"flow.{k} missing in typed access"

    # levels
    for k in ("call_wall", "call_wall_gex", "call_wall_strength",
              "distance_to_call_wall_pct",
              "put_wall", "put_wall_gex", "put_wall_strength",
              "distance_to_put_wall_pct",
              "distance_to_magnet_dollars",
              "highest_oi_strike", "highest_oi_total",
              "max_positive_gamma", "max_negative_gamma",
              "level_cluster_score"):
        assert k in r["levels"], f"levels.{k} missing in typed access"

    # liquidity
    for k in ("atm_spread_pct", "weighted_spread_pct", "execution_score"):
        assert k in r["liquidity"], f"liquidity.{k} missing in typed access"

    # metadata
    for k in ("snapshot_age_seconds", "chain_contract_count",
              "data_quality_score", "greek_smoothness_score"):
        assert k in r["metadata"], f"metadata.{k} missing in typed access"

    # strikes[0] — every per-strike field
    strikes = r["strikes"]
    assert isinstance(strikes, list)
    if strikes:
        s = strikes[0]
        for k in ("strike", "distance_from_spot_pct",
                  "call_symbol", "put_symbol",
                  "call_gex", "put_gex", "net_gex",
                  "call_dex", "put_dex", "net_dex",
                  "net_vex", "net_chex",
                  "call_oi", "put_oi", "call_volume", "put_volume",
                  "gex_share_pct", "oi_share_pct", "volume_share_pct",
                  "call_iv", "put_iv",
                  "call_delta", "put_delta",
                  "call_gamma", "put_gamma",
                  "call_theta", "put_theta",
                  "call_mid", "put_mid",
                  "call_spread_pct", "put_spread_pct"):
            assert k in s, f"strikes[0].{k} missing in typed access"


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


# ── Max Pain ─────────────────────────────────────────────────────────


def test_max_pain(fa):
    result = fa.max_pain("SPY")
    assert "max_pain_strike" in result
    assert "pain_curve" in result
    assert "dealer_alignment" in result
    assert "pin_probability" in result
    assert isinstance(result["pain_curve"], list)


def test_max_pain_response_fields(fa):
    result = fa.max_pain("SPY")
    assert "distance" in result
    assert result["distance"]["direction"] in ("above", "below", "at")
    assert result["signal"] in ("bullish", "bearish", "neutral")
    assert result["regime"] in ("positive_gamma", "negative_gamma")


def test_max_pain_with_expiration(fa):
    # Get first available expiration
    opts = fa.options("SPY")
    if opts.get("expirations") and len(opts["expirations"]) > 0:
        exp = opts["expirations"][0]["expiration"]
        result = fa.max_pain("SPY", expiration=exp)
        assert result["expiration"] == exp
        assert "max_pain_strike" in result


def test_max_pain_oi_by_strike(fa):
    result = fa.max_pain("SPY")
    if result.get("oi_by_strike"):
        row = result["oi_by_strike"][0]
        assert "strike" in row
        assert "call_oi" in row
        assert "put_oi" in row


def test_max_pain_multi_expiry_calendar(fa):
    """Without expiration filter, max_pain_by_expiration should be populated."""
    result = fa.max_pain("SPY")
    if result.get("max_pain_by_expiration"):
        entry = result["max_pain_by_expiration"][0]
        assert "expiration" in entry
        assert "max_pain_strike" in entry
        assert "dte" in entry


def test_max_pain_every_field_declared_in_poco_must_be_referenced(fa):
    """Every leaf field declared in MaxPainResponse must be referenced.

    100% field-coverage discipline (mirrors VRP / ExposureSummary contract).
    Customer traps explicitly checked: signal/regime literal sets,
    distance.direction casing, oi_by_strike row shape, dealer_alignment
    structure, expected_move structure.
    """
    r = fa.max_pain("SPY")

    # ── top-level scalars ──
    assert r["symbol"] == "SPY"
    assert isinstance(r["underlying_price"], (int, float)) and r["underlying_price"] > 0
    assert isinstance(r["as_of"], str) and r["as_of"]
    assert isinstance(r["max_pain_strike"], (int, float))
    assert r["signal"] in ("bullish", "bearish", "neutral")
    assert isinstance(r["expiration"], str) and r["expiration"]
    assert isinstance(r["put_call_oi_ratio"], (int, float))
    assert r["regime"] in ("positive_gamma", "negative_gamma", "unknown")
    assert isinstance(r["pin_probability"], int) and 0 <= r["pin_probability"] <= 100

    # ── distance{absolute, percent, direction} ──
    dist = r["distance"]
    assert isinstance(dist["absolute"], (int, float))
    assert isinstance(dist["percent"], (int, float))
    assert dist["direction"] in ("above", "below", "at")

    # ── pain_curve[]{strike, call_pain, put_pain, total_pain} ──
    pc = r["pain_curve"]
    assert isinstance(pc, list) and len(pc) > 0
    row = pc[0]
    assert isinstance(row["strike"], (int, float))
    assert isinstance(row["call_pain"], (int, float))
    assert isinstance(row["put_pain"], (int, float))
    assert isinstance(row["total_pain"], (int, float))

    # ── oi_by_strike[]{strike, call_oi, put_oi, total_oi, call_volume, put_volume} ──
    oi = r["oi_by_strike"]
    assert isinstance(oi, list) and len(oi) > 0
    oirow = oi[0]
    assert isinstance(oirow["strike"], (int, float))
    assert isinstance(oirow["call_oi"], int)
    assert isinstance(oirow["put_oi"], int)
    assert isinstance(oirow["total_oi"], int)
    assert isinstance(oirow["call_volume"], int)
    assert isinstance(oirow["put_volume"], int)

    # ── max_pain_by_expiration[]{expiration, max_pain_strike, dte, total_oi} ──
    # Populated when no expiration filter is applied (this call uses none).
    mpe = r["max_pain_by_expiration"]
    assert isinstance(mpe, list) and len(mpe) > 0
    mrow = mpe[0]
    assert isinstance(mrow["expiration"], str) and mrow["expiration"]
    assert isinstance(mrow["max_pain_strike"], (int, float))
    assert isinstance(mrow["dte"], int)
    assert isinstance(mrow["total_oi"], int)

    # ── dealer_alignment{alignment, description, gamma_flip, call_wall, put_wall} ──
    da = r["dealer_alignment"]
    assert da["alignment"] in ("converging", "moderate", "diverging", "unknown")
    assert isinstance(da["description"], str) and da["description"]
    assert isinstance(da["gamma_flip"], (int, float))
    assert isinstance(da["call_wall"], (int, float))
    assert isinstance(da["put_wall"], (int, float))

    # ── expected_move{straddle_price, atm_iv, max_pain_within_expected_range} ──
    em = r["expected_move"]
    assert isinstance(em["straddle_price"], (int, float))
    assert isinstance(em["atm_iv"], (int, float))
    assert isinstance(em["max_pain_within_expected_range"], bool)


# ── Screener ────────────────────────────────────────────────────────


def test_screener_empty(fa):
    """Empty request returns default universe for the account's tier."""
    result = fa.screener()
    assert "meta" in result
    assert "data" in result
    assert result["meta"]["tier"] in ("growth", "alpha")
    assert isinstance(result["data"], list)


def test_screener_simple_filter(fa):
    """Leaf filter on a universally-available field."""
    result = fa.screener(
        filters={"field": "regime", "operator": "in", "value": ["positive_gamma", "negative_gamma"]},
        select=["symbol", "price", "regime"],
        limit=5,
    )
    assert "data" in result
    for row in result["data"]:
        assert row["regime"] in ("positive_gamma", "negative_gamma")


def test_screener_and_group(fa):
    result = fa.screener(
        filters={
            "op": "and",
            "conditions": [
                {"field": "atm_iv", "operator": "gte", "value": 0},
                {"field": "atm_iv", "operator": "lte", "value": 500},
            ],
        },
        sort=[{"field": "atm_iv", "direction": "desc"}],
        select=["symbol", "atm_iv"],
        limit=5,
    )
    assert result["meta"]["returned_count"] <= 5
    # Sorted descending
    ivs = [row["atm_iv"] for row in result["data"] if row.get("atm_iv") is not None]
    if len(ivs) >= 2:
        assert ivs == sorted(ivs, reverse=True)


def test_screener_between_operator(fa):
    result = fa.screener(
        filters={"field": "atm_iv", "operator": "between", "value": [0, 500]},
        limit=3,
    )
    assert "data" in result


def test_screener_select_star(fa):
    result = fa.screener(select=["*"], limit=1)
    if result["data"]:
        row = result["data"][0]
        assert "symbol" in row
        # select=["*"] returns the full flat object
        assert "price" in row


def test_screener_limit_respected(fa):
    result = fa.screener(limit=3)
    assert result["meta"]["returned_count"] <= 3
    assert len(result["data"]) <= 3


def test_screener_meta_fields_present(fa):
    result = fa.screener()
    meta = result["meta"]
    assert "total_count" in meta
    assert "returned_count" in meta
    assert "universe_size" in meta
    assert "tier" in meta
    assert "as_of" in meta


def test_screener_invalid_field_raises(fa):
    """Unknown field should trigger a validation error."""
    with pytest.raises(Exception):
        fa.screener(filters={"field": "not_a_real_field_xyz", "operator": "eq", "value": 1})


# ── Customer regression tests ───────────────────────────────────────
#
# Each test replays one of the bugs an Alpha user hit during integration
# and asserts the SDK's public surface now behaves correctly. Written
# against fa.vrp() / fa.stock_summary() / fa.screener() — the methods
# the customer's daemon actually calls.


# Issue #5 — SDK was missing vrp(). Customer had to build a REST
# fallback. The method is now on the client.

def test_vrp_method_exists_on_client(fa):
    """fa.vrp() is a callable method on the SDK client."""
    assert hasattr(fa, "vrp") and callable(fa.vrp)


def test_vrp_returns_full_payload(fa):
    """fa.vrp(symbol) returns the full VRP payload — every documented
    field is readable via its documented access path and has a sane type.
    This is the positive mirror of the customer's 'silent null' bug.
    """
    r = fa.vrp("SPY")

    # Top-level scalars
    assert r["symbol"] == "SPY"
    assert isinstance(r["underlying_price"], (int, float)) and r["underlying_price"] > 0
    assert isinstance(r["as_of"], str) and len(r["as_of"]) > 0
    assert isinstance(r["market_open"], bool)
    assert isinstance(r["net_harvest_score"], (int, float))
    assert isinstance(r["dealer_flow_risk"], (int, float))

    # response["vrp"] — core metrics
    core = r["vrp"]
    for key in ("atm_iv", "rv_5d", "rv_10d", "rv_20d", "rv_30d",
                "vrp_5d", "vrp_10d", "vrp_20d", "vrp_30d",
                "z_score", "percentile", "history_days"):
        assert key in core, f"vrp.{key} missing"
    assert isinstance(core["z_score"], (int, float))
    assert isinstance(core["percentile"], int) and 0 <= core["percentile"] <= 100

    # response["directional"] — skew metrics
    d = r["directional"]
    for key in ("put_wing_iv_25d", "call_wing_iv_25d",
                "downside_rv_20d", "upside_rv_20d",
                "downside_vrp", "upside_vrp"):
        assert key in d, f"directional.{key} missing"

    # response["regime"] — regime snapshot
    reg = r["regime"]
    assert reg["gamma"] in ("positive_gamma", "negative_gamma", "neutral")
    assert "net_gex" in reg and isinstance(reg["net_gex"], (int, float))
    assert "vrp_regime" in reg

    # response["term_vrp"] — list of term-structure points
    assert isinstance(r["term_vrp"], list)
    if r["term_vrp"]:
        pt = r["term_vrp"][0]
        for key in ("dte", "iv", "rv", "vrp"):
            assert key in pt, f"term_vrp[0].{key} missing"

    # response["gex_conditioned"] — harvest scoring
    if r.get("gex_conditioned") is not None:
        gc = r["gex_conditioned"]
        assert "harvest_score" in gc
        assert "regime" in gc
        assert "interpretation" in gc
        assert isinstance(gc["harvest_score"], (int, float))

    # response["strategy_scores"] — 0-100 scores per strategy
    if r.get("strategy_scores") is not None:
        ss = r["strategy_scores"]
        for key in ("short_put_spread", "short_strangle",
                    "iron_condor", "calendar_spread"):
            if ss.get(key) is not None:
                assert 0 <= ss[key] <= 100, f"{key}={ss[key]} out of range"

    # response["macro"] — optional macro context
    if r.get("macro") is not None:
        assert "vix" in r["macro"]


def test_vrp_every_field_declared_in_poco_must_be_referenced(fa):
    """Every leaf field declared in VrpResponse must be referenced.

    100% field-coverage discipline (mirrors the ExposureSummary contract).
    Live-specific:
        - macro.fed_funds is present (live-only field).
        - macro.hy_spread may currently be null (data-pipeline gap).
    """
    r = fa.vrp("SPY")

    # ── top-level scalars ──
    assert r["symbol"] == "SPY"
    assert isinstance(r["underlying_price"], (int, float)) and r["underlying_price"] > 0
    assert isinstance(r["as_of"], str) and r["as_of"]
    assert isinstance(r["market_open"], bool)
    assert isinstance(r["variance_risk_premium"], (int, float))
    assert isinstance(r["convexity_premium"], (int, float))
    assert isinstance(r["fair_vol"], (int, float))
    assert isinstance(r["dealer_flow_risk"], (int, float))
    assert isinstance(r["net_harvest_score"], (int, float))
    assert isinstance(r["warnings"], list)
    # Customer traps: these MUST NOT be top-level
    assert "z_score" not in r
    assert "percentile" not in r
    assert "atm_iv" not in r
    assert "net_gex" not in r
    assert "put_vrp" not in r and "call_vrp" not in r
    assert "harvest_score" not in r  # under gex_conditioned

    # ── vrp.* core block ──
    core = r["vrp"]
    for k in ("atm_iv", "rv_5d", "rv_10d", "rv_20d", "rv_30d",
              "vrp_5d", "vrp_10d", "vrp_20d", "vrp_30d"):
        assert isinstance(core[k], (int, float)), f"vrp.{k}"
    assert isinstance(core["z_score"], (int, float))
    assert isinstance(core["percentile"], int) and 0 <= core["percentile"] <= 100
    assert isinstance(core["history_days"], int)

    # ── directional ──
    d = r["directional"]
    for k in ("put_wing_iv_25d", "call_wing_iv_25d",
              "downside_rv_20d", "upside_rv_20d",
              "downside_vrp", "upside_vrp"):
        assert isinstance(d[k], (int, float)), f"directional.{k}"

    # ── term_vrp[] ──
    term = r["term_vrp"]
    assert isinstance(term, list) and len(term) > 0
    first = term[0]
    assert isinstance(first["dte"], int)
    for k in ("iv", "rv", "vrp"):
        assert isinstance(first[k], (int, float)), f"term_vrp[0].{k}"

    # ── gex_conditioned ──
    gex_c = r["gex_conditioned"]
    assert isinstance(gex_c["regime"], str)
    assert isinstance(gex_c["harvest_score"], (int, float))
    assert isinstance(gex_c["interpretation"], str)

    # ── vanna_conditioned ──
    vanna_c = r["vanna_conditioned"]
    assert isinstance(vanna_c["outlook"], str)
    assert isinstance(vanna_c["interpretation"], str)

    # ── regime (net_gex lives HERE) ──
    reg = r["regime"]
    assert isinstance(reg["gamma"], str)
    assert isinstance(reg["vrp_regime"], str)
    assert isinstance(reg["net_gex"], (int, float))
    assert isinstance(reg["gamma_flip"], (int, float))

    # ── strategy_scores ──
    ss = r["strategy_scores"]
    for k in ("short_put_spread", "short_strangle", "iron_condor", "calendar_spread"):
        assert isinstance(ss[k], int) and 0 <= ss[k] <= 100, f"strategy_scores.{k}"

    # ── macro (live-specific includes fed_funds) ──
    m = r["macro"]
    for k in ("vix", "vix_3m", "vix_term_slope", "dgs10"):
        assert isinstance(m[k], (int, float)), f"macro.{k}"
    # hy_spread present but may be null on live currently
    assert "hy_spread" in m and (m["hy_spread"] is None or isinstance(m["hy_spread"], (int, float)))
    # fed_funds is the live-only macro field
    assert "fed_funds" in m and isinstance(m["fed_funds"], (int, float))


# Issue #1 — Nested response structures. Customer accessed
# response["z_score"] directly and got None. The field lives at
# response["vrp"]["z_score"]. Tests assert the documented nesting.

def test_vrp_core_metrics_are_nested_under_vrp(fa):
    """z_score, percentile, atm_iv, rv_20d live under response['vrp']."""
    r = fa.vrp("SPY")
    assert "z_score" not in r, "z_score must NOT be top-level (customer trap)"
    assert "percentile" not in r
    assert "atm_iv" not in r
    core = r["vrp"]
    for key in ("z_score", "percentile", "atm_iv", "rv_20d", "vrp_20d"):
        assert key in core, f"vrp.{key} missing"


def test_vrp_harvest_score_is_under_gex_conditioned(fa):
    """harvest_score lives under response['gex_conditioned']."""
    r = fa.vrp("SPY")
    assert "harvest_score" not in r, "harvest_score must NOT be top-level"
    if r.get("gex_conditioned") is not None:
        assert "harvest_score" in r["gex_conditioned"]
        assert "regime" in r["gex_conditioned"]


def test_vrp_net_gex_is_under_regime(fa):
    """On the vrp payload, net_gex and gamma_flip live under 'regime'."""
    r = fa.vrp("SPY")
    assert "net_gex" not in r, "net_gex must NOT be top-level on vrp"
    assert "gamma_flip" not in r
    assert "net_gex" in r["regime"]
    assert "gamma" in r["regime"]


def test_vrp_composite_scores_are_top_level(fa):
    """net_harvest_score and dealer_flow_risk ARE top-level (exception)."""
    r = fa.vrp("SPY")
    assert "net_harvest_score" in r
    assert "dealer_flow_risk" in r


def test_exposure_summary_net_gex_is_under_exposures(fa):
    """On exposure_summary, net_gex lives under response['exposures'].
    Validates the full nested read, not just key presence.
    """
    r = fa.exposure_summary("SPY")
    assert r["symbol"] == "SPY"
    assert "net_gex" not in r, "net_gex must NOT be top-level (customer trap)"

    exp = r["exposures"]
    assert "net_gex" in exp and isinstance(exp["net_gex"], (int, float))
    # Other exposures on the summary are readable too:
    for key in ("net_dex", "net_vex", "net_chex"):
        if key in exp:
            assert isinstance(exp[key], (int, float)), f"exposures.{key} not numeric"

    # regime is top-level and readable
    assert "regime" in r
    assert r["regime"] in ("positive_gamma", "negative_gamma", "neutral")


# Issue #2 — Field naming. Customer used put_vrp / call_vrp based on
# conventions from other APIs. The canonical names are downside_vrp /
# upside_vrp.

def test_vrp_directional_uses_downside_upside_names(fa):
    """directional block uses downside_vrp/upside_vrp, not put_vrp/call_vrp."""
    d = fa.vrp("SPY")["directional"]
    assert "downside_vrp" in d
    assert "upside_vrp" in d
    assert "put_wing_iv_25d" in d
    assert "call_wing_iv_25d" in d
    # Silent-null traps — must NOT exist:
    assert "put_vrp" not in d
    assert "call_vrp" not in d


# Issue #3 — URL pattern mix. Customer guessed /v1/summary/{sym} and
# got a silent 404. The SDK methods route to the canonical paths.

def test_stock_summary_method_routes_correctly(fa):
    """fa.stock_summary() returns data (SDK uses /v1/stock/{sym}/summary)
    and the core fields the customer's daemon enriches signals with.
    """
    r = fa.stock_summary("SPY")
    assert r["symbol"] == "SPY"
    assert "price" in r
    # Customer enriches signals with this payload; validate it's non-empty
    assert isinstance(r, dict) and len(r) > 3


def test_stock_quote_method_routes_correctly(fa):
    """fa.stock_quote() uses bare /stockquote/{t} — no /v1/ prefix."""
    r = fa.stock_quote("SPY")
    assert r["ticker"] == "SPY"


def test_all_exposure_methods_route_correctly(fa):
    """Every exposure method on the SDK returns data for SPY."""
    for method in (fa.gex, fa.dex, fa.vex, fa.chex,
                   fa.exposure_summary, fa.exposure_levels):
        assert method("SPY")["symbol"] == "SPY"


def test_vrp_method_routes_correctly(fa):
    """fa.vrp() uses /v1/vrp/{sym} — has /v1/ prefix."""
    r = fa.vrp("SPY")
    assert r["symbol"] == "SPY"


# Issue #4 — Screener URL. SDK's fa.screener() POSTs to /v1/screener
# (canonical since v0.3.1). Test hits the live API and validates the
# full response envelope + row fields.

def test_screener_returns_valid_envelope(fa):
    """fa.screener() returns a response with meta + data against live API."""
    r = fa.screener(limit=5)
    assert "meta" in r and "data" in r
    meta = r["meta"]
    for key in ("total_count", "returned_count", "universe_size", "tier", "as_of"):
        assert key in meta, f"meta.{key} missing"
    assert meta["returned_count"] <= 5
    assert meta["tier"] in ("growth", "alpha")


def test_screener_full_row_is_readable(fa):
    """select=['*'] returns flat rows with the documented key fields."""
    r = fa.screener(select=["*"], limit=1)
    if not r["data"]:
        pytest.skip("no rows returned for universe")
    row = r["data"][0]
    for key in ("symbol", "price", "regime"):
        assert key in row, f"row missing {key}"


# ── Field-walk coverage tests for the rc.4 POCOs ────────────────────
#
# These tests use the TypedDict ``__annotations__`` introspection to walk
# every field declared on a response model and assert the live response
# carries it. The point is to fail loudly the moment server adds (or
# the SDK declares) a field the other side doesn't actually populate —
# without us having to hand-curate per-field assertions for every nested
# block.

# TypedDicts whose nested ``__annotations__`` we want to recurse into.
# Every other annotation type (str, int, float, bool, List[...], unions,
# Literal, Optional[primitive]) is treated as a leaf.
_WALKABLE_TYPED_DICTS = {
    StockSummaryPrice,
    StockSummarySkew25d,
    StockSummaryVolatility,
    StockSummaryOptionsFlow,
    StockSummaryInterpretation,
    StockSummaryHedgingMove,
    StockSummaryHedgingEstimate,
    StockSummaryZeroDte,
    StockSummaryExposure,
    StockSummaryMacroIndex,
    StockSummaryVixTermLevels,
    StockSummaryVixTermStructure,
    StockSummaryVixFutures,
    StockSummaryFearAndGreed,
    StockSummaryMacro,
    NarrativeData,
    NarrativeOiChange,
    PricingInputs,
    PricingFirstOrder,
    PricingSecondOrder,
    PricingThirdOrder,
    PricingAdditional,
    # ── rc.9 nested TypedDicts (Volatility / AdvVolatility) ──
    VolatilityRealizedVol,
    VolatilityIvRvSpreads,
    VolatilityTermStructure,
    VolatilityIvDispersion,
    VolatilityPutCallProfile,
    VolatilityPcByMoneyness,
    VolatilityOiConcentration,
    VolatilityLiquidity,
    AdvVolTotalVarianceSurface,
    AdvVolGreeksSurfaces,
    AdvVolGreekSurface,
}


def _is_walkable_typeddict(ann) -> bool:
    """True if ``ann`` resolves to one of our nested TypedDicts to recurse into."""
    # Strip Optional[X] / Union[X, None] / List[X] envelopes — we only
    # recurse on the *direct* TypedDict annotations (block fields), not on
    # list-of-TypedDict (those are validated elementwise by the caller).
    return ann in _WALKABLE_TYPED_DICTS


def _assert_all_keys_populated(prefix: str, td_class, value: dict) -> None:
    """Walk every key declared on ``td_class.__annotations__`` against ``value``.

    For each declared field:
      * The key must be present in the response dict (the contract guarantee).
      * The value must not be ``None`` *unless* the field is annotated
        ``Optional[...]`` — the API legitimately returns ``null`` for those
        (e.g. ``narrative.data.net_gex_prior`` when there is no prior
        session). Required (non-Optional) fields must still be populated.
      * If the annotation is a nested TypedDict in ``_WALKABLE_TYPED_DICTS``,
        recurse into it.

    Lists, primitives, Literals and ``Optional[...]`` envelopes are treated
    as leaves — caller is responsible for any per-element shape checks
    they care about (e.g. validating ``narrative.data.top_oi_changes[0]``).
    """
    annotations = getattr(td_class, "__annotations__", {})
    assert annotations, f"{prefix}: TypedDict {td_class.__name__} has no __annotations__"
    for key, ann in annotations.items():
        assert key in value, f"{prefix}.{key} missing from response"
        v = value[key]
        # ``Optional[X]`` == ``Union[X, None]`` — null is contractually valid
        # for those fields, so only require non-None on required fields.
        optional = type(None) in get_args(ann)
        if not optional:
            assert v is not None, f"{prefix}.{key} is None"
        if v is not None and _is_walkable_typeddict(ann):
            assert isinstance(v, dict), f"{prefix}.{key} expected dict, got {type(v).__name__}"
            _assert_all_keys_populated(f"{prefix}.{key}", ann, v)


def test_stock_summary_every_field_declared_in_typeddict(fa):
    """Every key declared on ``StockSummaryResponse`` (and walkable nested
    TypedDicts) must be present and non-None on a SPY response.

    The ``exposure`` block is ``Optional`` per the type declaration — only
    walk into it if the server actually returned it for SPY (it always
    does in practice for SPY, but be defensive against off-hours / illiquid
    snapshots).
    """
    result = fa.stock_summary("SPY")

    annotations = StockSummaryResponse.__annotations__
    for key, ann in annotations.items():
        assert key in result, f"stock_summary.{key} missing from response"

    # Top-level scalars (must be non-None on SPY).
    assert result["symbol"] == "SPY"
    assert isinstance(result["as_of"], str) and result["as_of"]
    assert result["market_open"] is not None

    # Walk every nested block.
    _assert_all_keys_populated("price", StockSummaryPrice, result["price"])
    _assert_all_keys_populated("volatility", StockSummaryVolatility, result["volatility"])
    _assert_all_keys_populated("options_flow", StockSummaryOptionsFlow, result["options_flow"])
    _assert_all_keys_populated("macro", StockSummaryMacro, result["macro"])

    # ``exposure`` is Optional — walk only if present (always present for SPY).
    if result.get("exposure") is not None:
        _assert_all_keys_populated("exposure", StockSummaryExposure, result["exposure"])


def test_narrative_every_field_declared_in_typeddict(fa):
    """Every key declared on ``NarrativeResponse``, the ``narrative`` block,
    and ``narrative.data`` must be present on a SPY response.

    The narrative endpoint requires Growth+; if the live key isn't tier-eligible
    skip rather than fail.
    """
    try:
        result = fa.narrative("SPY")
    except Exception as exc:  # noqa: BLE001 — tier check needs broad catch
        if "tier_restricted" in str(exc).lower() or "403" in str(exc):
            pytest.skip(f"narrative requires Growth+: {exc}")
        raise

    # Top-level fields on NarrativeResponse.
    for key in NarrativeResponse.__annotations__:
        assert key in result, f"narrative.{key} missing from response"
    assert result["symbol"] == "SPY"
    assert isinstance(result["as_of"], str) and result["as_of"]
    assert result["underlying_price"] is not None

    # narrative.{regime, gex_change, key_levels, flow, vanna, charm, zero_dte, outlook, data}
    # — every prose string is editorially safe on SPY, so all should be non-empty strings.
    narrative = result["narrative"]
    assert isinstance(narrative, dict)
    from flashalpha import Narrative  # local import to avoid widening module-level imports
    for key, _ann in Narrative.__annotations__.items():
        assert key in narrative, f"narrative.narrative.{key} missing"
        assert narrative[key] is not None, f"narrative.narrative.{key} is None"

    # Prose strings should be non-empty.
    for key in ("regime", "gex_change", "key_levels", "flow", "vanna", "charm", "zero_dte", "outlook"):
        assert isinstance(narrative[key], str) and narrative[key], f"narrative.{key} empty"

    # narrative.data — full numeric block.
    data = narrative["data"]
    _assert_all_keys_populated("narrative.data", NarrativeData, data)

    # top_oi_changes is List[NarrativeOiChange]. If non-empty, validate one element shape.
    top = data["top_oi_changes"]
    assert isinstance(top, list)
    if top:
        _assert_all_keys_populated("narrative.data.top_oi_changes[0]", NarrativeOiChange, top[0])


def test_exposure_levels_every_field_declared_in_typeddict(fa):
    """Every key declared on ``ExposureLevelsResponse`` and ``ExposureLevels``
    must be present on a SPY response.

    Specifically asserts ``zero_dte_magnet`` is in ``result["levels"]`` and
    non-None on SPY (which always has a same-day expiry intraday) — this
    assertion was missing from the existing ``test_exposure_levels``.
    """
    result = fa.exposure_levels("SPY")

    for key in ExposureLevelsResponse.__annotations__:
        assert key in result, f"exposure_levels.{key} missing from response"

    assert result["symbol"] == "SPY"
    assert isinstance(result["as_of"], str) and result["as_of"]
    assert result["underlying_price"] is not None

    levels = result["levels"]
    from flashalpha import ExposureLevels  # local import; widens nothing important
    for key in ExposureLevels.__annotations__:
        assert key in levels, f"exposure_levels.levels.{key} missing"

    # SPY always trades a same-day expiry during RTH, so zero_dte_magnet
    # MUST be populated. This is the assertion the existing field-coverage
    # check was missing in both repos.
    assert levels["zero_dte_magnet"] is not None, "levels.zero_dte_magnet is None on SPY"
    assert isinstance(levels["zero_dte_magnet"], (int, float))


def test_pricing_greeks_every_field_declared_in_typeddict(fa):
    """Every key declared on ``PricingGreeksResponse`` (and the nested
    ``inputs``, ``first_order``, ``second_order``, ``third_order``,
    ``additional`` blocks) must be present and non-None.

    The one exception: ``additional["lambda"]`` is None when
    ``theoretical_price`` is <= 0, because lambda = delta * spot / price
    blows up. The chosen inputs (spot=580, strike=580, dte=30, sigma=0.18,
    type=call) yield a strictly positive theoretical price, so lambda
    should be non-None — but we still guard the assertion.
    """
    result = fa.greeks(spot=580, strike=580, dte=30, sigma=0.18, type="call")

    for key in PricingGreeksResponse.__annotations__:
        assert key in result, f"pricing.greeks.{key} missing from response"

    assert result["theoretical_price"] is not None
    assert isinstance(result["theoretical_price"], (int, float))

    _assert_all_keys_populated("pricing.greeks.inputs", PricingInputs, result["inputs"])
    _assert_all_keys_populated("pricing.greeks.first_order", PricingFirstOrder, result["first_order"])
    _assert_all_keys_populated("pricing.greeks.second_order", PricingSecondOrder, result["second_order"])
    _assert_all_keys_populated("pricing.greeks.third_order", PricingThirdOrder, result["third_order"])

    # ``additional`` carries ``lambda`` (Python keyword — read via dict access)
    # and ``veta``. lambda is None iff theoretical_price <= 0.
    additional = result["additional"]
    assert "lambda" in additional, "pricing.greeks.additional.lambda missing"
    assert "veta" in additional, "pricing.greeks.additional.veta missing"
    assert additional["veta"] is not None
    if result["theoretical_price"] > 0:
        assert additional["lambda"] is not None, "additional.lambda is None despite price > 0"
    # else: lambda may legitimately be None — don't assert.


# ── Field-walk coverage tests for the rc.9 POCOs ────────────────────
#
# Same discipline as the rc.4 / rc.7 helpers above: walk every field
# declared on each rc.9 response TypedDict and assert the live response
# carries it. Recurse into nested TypedDicts that the response actually
# nests (registered in _WALKABLE_TYPED_DICTS above). Lists of TypedDicts
# are validated elementwise on the first row when non-empty.


def test_volatility_every_field_declared_in_typeddict(fa):
    """Every key declared on ``VolatilityResponse`` (and the walkable nested
    blocks ``realized_vol``, ``iv_rv_spreads``, ``term_structure``,
    ``iv_dispersion``, ``put_call_profile``, ``oi_concentration``,
    ``liquidity``) must be present and non-None on a SPY snapshot.

    Volatility is Growth+; skip on tier_restricted rather than fail.
    List-of-TypedDict blocks (``skew_profiles``, ``gex_by_dte``,
    ``theta_by_dte``, ``hedging_scenarios``) are validated elementwise on
    the first row when non-empty.
    """
    try:
        result = fa.volatility("SPY")
    except TierRestrictedError as exc:
        pytest.skip(f"volatility requires Growth+: {exc}")

    # Top-level fields on VolatilityResponse must all be present.
    for key in VolatilityResponse.__annotations__:
        assert key in result, f"volatility.{key} missing from response"

    assert result["symbol"] == "SPY"
    assert isinstance(result["as_of"], str) and result["as_of"]
    assert result["underlying_price"] is not None
    assert result["market_open"] is not None
    assert isinstance(result["atm_iv"], (int, float))

    # Walk every nested block.
    _assert_all_keys_populated("realized_vol", VolatilityRealizedVol, result["realized_vol"])
    _assert_all_keys_populated("iv_rv_spreads", VolatilityIvRvSpreads, result["iv_rv_spreads"])
    _assert_all_keys_populated("term_structure", VolatilityTermStructure, result["term_structure"])
    _assert_all_keys_populated("iv_dispersion", VolatilityIvDispersion, result["iv_dispersion"])
    _assert_all_keys_populated("put_call_profile", VolatilityPutCallProfile, result["put_call_profile"])
    _assert_all_keys_populated("oi_concentration", VolatilityOiConcentration, result["oi_concentration"])
    _assert_all_keys_populated("liquidity", VolatilityLiquidity, result["liquidity"])

    # List-of-TypedDict blocks: validate first row when non-empty.
    skew = result["skew_profiles"]
    assert isinstance(skew, list)
    if skew:
        _assert_all_keys_populated("skew_profiles[0]", VolatilitySkewProfile, skew[0])

    gex_by_dte = result["gex_by_dte"]
    assert isinstance(gex_by_dte, list)
    if gex_by_dte:
        _assert_all_keys_populated("gex_by_dte[0]", VolatilityGexByDte, gex_by_dte[0])

    theta_by_dte = result["theta_by_dte"]
    assert isinstance(theta_by_dte, list)
    if theta_by_dte:
        _assert_all_keys_populated("theta_by_dte[0]", VolatilityThetaByDte, theta_by_dte[0])

    hedging = result["hedging_scenarios"]
    assert isinstance(hedging, list)
    if hedging:
        _assert_all_keys_populated("hedging_scenarios[0]", VolatilityHedgingScenario, hedging[0])

    # put_call_profile.by_expiry is List[VolatilityPcByExpiry].
    pc_by_expiry = result["put_call_profile"]["by_expiry"]
    assert isinstance(pc_by_expiry, list)
    if pc_by_expiry:
        _assert_all_keys_populated(
            "put_call_profile.by_expiry[0]", VolatilityPcByExpiry, pc_by_expiry[0]
        )


def test_adv_volatility_every_field_declared_in_typeddict(fa):
    """Every key declared on ``AdvVolatilityResponse`` (and walkable nested
    surfaces) must be present on a SPY snapshot.

    Alpha+ only — ``pytest.skip`` on ``TierRestrictedError``.
    """
    try:
        result = fa.adv_volatility("SPY")
    except TierRestrictedError as exc:
        pytest.skip(f"adv_volatility requires Alpha+: {exc}")

    for key in AdvVolatilityResponse.__annotations__:
        assert key in result, f"adv_volatility.{key} missing from response"

    assert result["symbol"] == "SPY"
    assert isinstance(result["as_of"], str) and result["as_of"]

    # Walk the two nested object blocks.
    _assert_all_keys_populated(
        "total_variance_surface", AdvVolTotalVarianceSurface, result["total_variance_surface"]
    )
    _assert_all_keys_populated(
        "greeks_surfaces", AdvVolGreeksSurfaces, result["greeks_surfaces"]
    )

    # List-of-TypedDict blocks: validate first row when non-empty.
    svi = result["svi_parameters"]
    assert isinstance(svi, list)
    if svi:
        _assert_all_keys_populated("svi_parameters[0]", AdvVolSviParam, svi[0])

    fwds = result["forward_prices"]
    assert isinstance(fwds, list)
    if fwds:
        _assert_all_keys_populated("forward_prices[0]", AdvVolForwardPrice, fwds[0])

    # arbitrage_flags is often empty (clean surface) — only walk if populated.
    arb = result["arbitrage_flags"]
    assert isinstance(arb, list)
    if arb:
        _assert_all_keys_populated("arbitrage_flags[0]", AdvVolArbitrageFlag, arb[0])

    var_swaps = result["variance_swap_fair_values"]
    assert isinstance(var_swaps, list)
    if var_swaps:
        _assert_all_keys_populated("variance_swap_fair_values[0]", AdvVolVarianceSwap, var_swaps[0])


def test_surface_every_field_declared_in_typeddict(fa):
    """Every key declared on ``SurfaceResponse`` must be present on a SPY
    snapshot. Surface is public — no tier gating to handle.
    """
    result = fa.surface("SPY")

    for key in SurfaceResponse.__annotations__:
        assert key in result, f"surface.{key} missing from response"

    assert result["symbol"] == "SPY"
    assert isinstance(result["as_of"], str) and result["as_of"]
    assert result["spot"] is not None
    assert isinstance(result["grid_size"], int) and result["grid_size"] > 0
    assert isinstance(result["tenors"], list) and len(result["tenors"]) > 0
    assert isinstance(result["moneyness"], list) and len(result["moneyness"]) > 0
    assert isinstance(result["iv"], list) and len(result["iv"]) > 0
    assert isinstance(result["iv"][0], list) and len(result["iv"][0]) > 0
    assert isinstance(result["slices_used"], int)


def test_gex_every_field_declared_in_typeddict(fa):
    """Every key declared on ``GexResponse`` (and ``GexStrikeRow`` per row)
    must be present on a SPY response.
    """
    result = fa.gex("SPY")

    for key in GexResponse.__annotations__:
        assert key in result, f"gex.{key} missing from response"

    assert result["symbol"] == "SPY"
    assert isinstance(result["as_of"], str) and result["as_of"]
    assert result["underlying_price"] is not None
    strikes = result["strikes"]
    assert isinstance(strikes, list) and len(strikes) > 0
    # Walk the first row — every declared field on GexStrikeRow must exist.
    row = strikes[0]
    for key in GexStrikeRow.__annotations__:
        assert key in row, f"gex.strikes[0].{key} missing"


def test_dex_every_field_declared_in_typeddict(fa):
    """Every key declared on ``DexResponse`` must be present on SPY."""
    result = fa.dex("SPY")
    for key in DexResponse.__annotations__:
        assert key in result, f"dex.{key} missing from response"
    assert result["symbol"] == "SPY"
    strikes = result["strikes"]
    assert isinstance(strikes, list) and len(strikes) > 0
    for key in DexStrikeRow.__annotations__:
        assert key in strikes[0], f"dex.strikes[0].{key} missing"


def test_vex_every_field_declared_in_typeddict(fa):
    """Every key declared on ``VexResponse`` must be present on SPY."""
    result = fa.vex("SPY")
    for key in VexResponse.__annotations__:
        assert key in result, f"vex.{key} missing from response"
    assert result["symbol"] == "SPY"
    strikes = result["strikes"]
    assert isinstance(strikes, list) and len(strikes) > 0
    for key in VexStrikeRow.__annotations__:
        assert key in strikes[0], f"vex.strikes[0].{key} missing"


def test_chex_every_field_declared_in_typeddict(fa):
    """Every key declared on ``ChexResponse`` must be present on SPY."""
    result = fa.chex("SPY")
    for key in ChexResponse.__annotations__:
        assert key in result, f"chex.{key} missing from response"
    assert result["symbol"] == "SPY"
    strikes = result["strikes"]
    assert isinstance(strikes, list) and len(strikes) > 0
    for key in ChexStrikeRow.__annotations__:
        assert key in strikes[0], f"chex.strikes[0].{key} missing"


def test_option_quote_every_field_declared_in_typeddict(fa):
    """Every key declared on ``OptionQuoteResponse`` must be present.

    Uses the unfiltered chain (one call) — the list contains only
    contracts that actually have a quote, and the per-element shape is
    identical to the single-contract response. We then validate the
    **ATM** element (strike nearest spot): far-OTM listings legitimately
    omit greeks, so ATM is the strictest reliably-populated contract.
    Growth+; skip on ``TierRestrictedError``.
    """
    try:
        sq = fa.stock_quote("SPY")
        spot = sq.get("mid") or sq.get("lastPrice")
        chain = fa.option_quote("SPY")
    except TierRestrictedError as exc:
        pytest.skip(f"option_quote requires Growth+: {exc}")

    assert isinstance(chain, list) and chain, "option_quote returned no contracts"
    quoted = [c for c in chain if isinstance(c, dict) and c.get("strike") is not None]
    assert quoted, "option_quote returned no contracts with a strike"
    result = (
        min(quoted, key=lambda c: abs(c["strike"] - spot)) if spot else quoted[0]
    )

    # ``underlying`` is modelled for forward-compat but the /optionquote
    # endpoint does not emit it (verified live on both the list and
    # single-contract shapes) — it is a genuinely optional leaf, so don't
    # require its presence. Every other declared field must be present.
    for key in OptionQuoteResponse.__annotations__:
        if key == "underlying":
            continue
        assert key in result, f"option_quote.{key} missing from response"


def test_stock_quote_every_field_declared_in_typeddict(fa):
    """Every key declared on ``StockQuoteResponse`` must be present on SPY."""
    result = fa.stock_quote("SPY")

    for key in StockQuoteResponse.__annotations__:
        assert key in result, f"stock_quote.{key} missing from response"

    assert result["ticker"] == "SPY"
    assert isinstance(result["bid"], (int, float))
    assert isinstance(result["ask"], (int, float))
    assert isinstance(result["mid"], (int, float))
    # Camel-cased on the wire, preserved verbatim on the typed dict.
    assert "lastPrice" in result
    assert "lastUpdate" in result


# ── Flow (live, simulation-aware) — Alpha+ ──────────────────────────
#
# These hit the real /v1/flow/* surface and assert every field declared
# in the canonical contract is present on the live response (and on the
# nested array-element shapes when the arrays are non-empty). The test
# key is Alpha+; if a future key is not, the tier-gate skip keeps the
# suite green rather than red.

FLOW_SYMBOL = "SPY"


def _require(obj, fields, where):
    """Assert every name in ``fields`` is a key of ``obj``."""
    assert isinstance(obj, dict), f"{where}: expected object, got {type(obj)}"
    missing = [f for f in fields if f not in obj]
    assert not missing, f"{where}: missing fields {missing}"


def _flow(call):
    """Invoke a flow call, skipping if the key lacks the Alpha tier."""
    try:
        return call()
    except TierRestrictedError as exc:
        pytest.skip(f"flow requires Alpha plan: {exc}")


def test_flow_levels(fa):
    r = _flow(lambda: fa.flow_levels(FLOW_SYMBOL))
    _require(r, ["symbol", "as_of", "underlying_price", "expiry",
                "live_gamma_flip", "live_call_wall", "live_put_wall",
                "live_max_pain"], "flow/levels")
    assert r["symbol"] == FLOW_SYMBOL


def test_flow_pin_risk(fa):
    r = _flow(lambda: fa.flow_pin_risk(FLOW_SYMBOL))
    _require(r, ["symbol", "as_of", "underlying_price", "expiry",
                "live_pin_risk", "magnet_strike", "distance_to_magnet_pct",
                "time_to_close_hours", "breakdown"], "flow/pin-risk")
    _require(r["breakdown"], ["oi_score", "proximity_score", "time_score",
                              "gamma_score"], "flow/pin-risk.breakdown")


def test_flow_summary(fa):
    r = _flow(lambda: fa.flow_summary(FLOW_SYMBOL))
    _require(r, ["symbol", "as_of", "underlying_price", "expiry",
                "flow_direction", "intraday_oi_delta", "contracts_with_flow",
                "contracts_total", "live_gex", "flow_gex_pct_shift"],
             "flow/summary")


def test_flow_oi(fa):
    r = _flow(lambda: fa.flow_oi(FLOW_SYMBOL))
    _require(r, ["symbol", "as_of", "expiry", "official_oi", "simulated_oi",
                "intraday_oi_delta", "oi_delta_confidence", "effective_oi",
                "contracts_total", "contracts_with_flow"], "flow/oi")


def test_flow_gex(fa):
    r = _flow(lambda: fa.flow_gex(FLOW_SYMBOL))
    _require(r, ["symbol", "as_of", "underlying_price", "expiry",
                "live_net_gex", "live_net_gex_label", "live_gamma_flip",
                "strikes"], "flow/gex")
    assert isinstance(r["strikes"], list) and r["strikes"]
    _require(r["strikes"][0], ["strike", "call_gex", "put_gex", "net_gex",
                               "call_oi", "put_oi", "call_volume",
                               "put_volume"], "flow/gex.strikes[0]")


def test_flow_dex(fa):
    r = _flow(lambda: fa.flow_dex(FLOW_SYMBOL))
    _require(r, ["symbol", "as_of", "underlying_price", "expiry",
                "live_net_dex", "strikes"], "flow/dex")
    assert isinstance(r["strikes"], list) and r["strikes"]
    _require(r["strikes"][0], ["strike", "call_dex", "put_dex", "net_dex"],
             "flow/dex.strikes[0]")


def test_flow_dealer_risk(fa):
    r = _flow(lambda: fa.flow_dealer_risk(FLOW_SYMBOL))
    _require(r, ["symbol", "as_of", "underlying_price", "expiry",
                "settled_net_gex", "live_net_gex", "flow_gex_adjustment",
                "flow_gex_pct_shift", "settled_net_dex", "live_net_dex",
                "flow_dex_adjustment", "flow_dex_pct_shift",
                "total_abs_delta_contracts", "contracts_with_flow",
                "flow_direction", "description"], "flow/dealer-risk")


def test_flow_live(fa):
    r = _flow(lambda: fa.flow_live(FLOW_SYMBOL))
    _require(r, ["symbol", "as_of", "underlying_price", "expiry",
                "contracts", "contracts_with_flow", "official_oi",
                "simulated_oi", "intraday_oi_delta", "oi_delta_confidence",
                "effective_oi", "live_gex", "live_gex_delta",
                "live_gamma_flip", "live_call_wall", "live_put_wall",
                "live_max_pain", "live_pin_risk",
                "flow_adjusted_dealer_risk"], "flow/live")
    _require(r["flow_adjusted_dealer_risk"],
             ["settled_net_gex", "live_net_gex", "flow_gex_adjustment",
              "flow_gex_pct_shift", "settled_net_dex", "live_net_dex",
              "flow_dex_adjustment", "flow_dex_pct_shift",
              "total_abs_delta_contracts", "flow_direction", "description"],
             "flow/live.flow_adjusted_dealer_risk")


def test_flow_option_recent(fa):
    r = _flow(lambda: fa.flow_option_recent(FLOW_SYMBOL, limit=5))
    _require(r, ["symbol", "count", "totalAvailable", "trades"],
             "flow/options/recent")
    assert isinstance(r["trades"], list)
    if r["trades"]:
        _require(r["trades"][0], ["ts", "instrumentId", "expiry", "strike",
                                  "right", "price", "size", "side",
                                  "isBlock", "bid", "ask"],
                 "flow/options/recent.trades[0]")


def test_flow_option_summary(fa):
    r = _flow(lambda: fa.flow_option_summary(FLOW_SYMBOL))
    _require(r, ["symbol", "contractsWithTrades", "totalTrades",
                "buyVolume", "sellVolume", "midVolume", "netVolume",
                "biggestSingleTrade"], "flow/options/summary")


def test_flow_option_blocks(fa):
    r = _flow(lambda: fa.flow_option_blocks(FLOW_SYMBOL, min_size=50))
    _require(r, ["symbol", "minSize", "count", "blocks"],
             "flow/options/blocks")
    if r["blocks"]:
        _require(r["blocks"][0], ["ts", "expiry", "strike", "right",
                                  "price", "size", "side"],
                 "flow/options/blocks.blocks[0]")


def test_flow_option_history(fa):
    r = _flow(lambda: fa.flow_option_history(FLOW_SYMBOL, minutes=30))
    _require(r, ["symbol", "minutes", "count", "buckets"],
             "flow/options/history")
    if r["buckets"]:
        _require(r["buckets"][0], ["ts", "buyVolume", "sellVolume",
                                   "midVolume", "netVolume", "tradeCount",
                                   "biggestTrade", "vwap", "high", "low"],
                 "flow/options/history.buckets[0]")


def test_flow_option_cumulative(fa):
    r = _flow(lambda: fa.flow_option_cumulative(FLOW_SYMBOL, minutes=60))
    _require(r, ["symbol", "minutes", "count", "points"],
             "flow/options/cumulative")
    if r["points"]:
        _require(r["points"][0], ["ts", "netVolume", "cumulative", "vwap",
                                  "tradeCount"],
                 "flow/options/cumulative.points[0]")


def test_flow_stock_recent(fa):
    r = _flow(lambda: fa.flow_stock_recent(FLOW_SYMBOL, limit=5))
    _require(r, ["symbol", "count", "totalAvailable", "trades"],
             "flow/stocks/recent")
    if r["trades"]:
        _require(r["trades"][0], ["ts", "price", "size", "side", "isBlock",
                                  "bid", "ask"],
                 "flow/stocks/recent.trades[0]")


def test_flow_stock_summary(fa):
    r = _flow(lambda: fa.flow_stock_summary(FLOW_SYMBOL))
    _require(r, ["symbol", "totalTrades", "buyVolume", "sellVolume",
                "midVolume", "netVolume", "biggestSingleTrade"],
             "flow/stocks/summary")


def test_flow_stock_blocks(fa):
    r = _flow(lambda: fa.flow_stock_blocks(FLOW_SYMBOL, min_size=1000))
    _require(r, ["symbol", "minSize", "count", "blocks"],
             "flow/stocks/blocks")
    if r["blocks"]:
        _require(r["blocks"][0], ["ts", "price", "size", "side", "bid",
                                  "ask"], "flow/stocks/blocks.blocks[0]")


def test_flow_stock_history(fa):
    r = _flow(lambda: fa.flow_stock_history(FLOW_SYMBOL, minutes=30))
    _require(r, ["symbol", "minutes", "count", "buckets"],
             "flow/stocks/history")
    if r["buckets"]:
        _require(r["buckets"][0], ["ts", "buyVolume", "sellVolume",
                                   "midVolume", "netVolume", "tradeCount",
                                   "biggestTrade", "vwap", "open", "close",
                                   "high", "low"],
                 "flow/stocks/history.buckets[0]")


def test_flow_stock_cumulative(fa):
    r = _flow(lambda: fa.flow_stock_cumulative(FLOW_SYMBOL, minutes=60))
    _require(r, ["symbol", "minutes", "count", "points"],
             "flow/stocks/cumulative")
    if r["points"]:
        _require(r["points"][0], ["ts", "netVolume", "cumulative", "vwap",
                                  "tradeCount"],
                 "flow/stocks/cumulative.points[0]")


def test_flow_options_leaderboard(fa):
    r = _flow(lambda: fa.flow_options_leaderboard(n=3))
    _require(r, ["generatedUtc", "n", "windowMinutes", "buyers", "sellers"],
             "flow/options/leaderboard")
    for row in (r["buyers"] + r["sellers"]):
        _require(row, ["symbol", "netVolume", "netNotional", "buyVolume",
                       "sellVolume", "avgPremium", "tradeCount",
                       "lastTradeUtc"], "flow/options/leaderboard.row")
        break


def test_flow_options_outliers(fa):
    r = _flow(lambda: fa.flow_options_outliers(limit=3))
    _require(r, ["generatedUtc", "windowMinutes", "tracked", "qualified",
                "limit", "outliers"], "flow/options/outliers")
    if r["outliers"]:
        _require(r["outliers"][0], ["symbol", "tradeCount", "buyVolume",
                                    "sellVolume", "midVolume", "netVolume",
                                    "imbalancePct", "skew", "notional",
                                    "netNotional", "biggestTrade",
                                    "biggestTradeUtc", "biggestAgeSec",
                                    "lastVwap", "lastTradeUtc",
                                    "lastTradeAgeSec"],
                 "flow/options/outliers.outliers[0]")


def test_flow_stocks_leaderboard(fa):
    r = _flow(lambda: fa.flow_stocks_leaderboard(n=3))
    _require(r, ["generatedUtc", "n", "windowMinutes", "buyers", "sellers"],
             "flow/stocks/leaderboard")
    for row in (r["buyers"] + r["sellers"]):
        _require(row, ["symbol", "netVolume", "netNotional", "buyVolume",
                       "sellVolume", "vwap", "tradeCount", "lastTradeUtc"],
                 "flow/stocks/leaderboard.row")
        break


def test_flow_stocks_outliers(fa):
    r = _flow(lambda: fa.flow_stocks_outliers(limit=3))
    _require(r, ["generatedUtc", "windowMinutes", "tracked", "qualified",
                "limit", "outliers"], "flow/stocks/outliers")
    if r["outliers"]:
        _require(r["outliers"][0], ["symbol", "tradeCount", "buyVolume",
                                    "sellVolume", "midVolume", "netVolume",
                                    "imbalancePct", "skew", "notional",
                                    "netNotional", "biggestTrade",
                                    "biggestTradeUtc", "biggestAgeSec",
                                    "lastVwap", "lastTradeUtc",
                                    "lastTradeAgeSec"],
                 "flow/stocks/outliers.outliers[0]")
