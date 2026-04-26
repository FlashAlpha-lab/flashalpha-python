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
