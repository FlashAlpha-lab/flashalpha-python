"""Typed response models for FlashAlpha SDK.

These are ``TypedDict`` aliases — at runtime each is a plain ``dict``. Existing
code that does ``result["field"]`` keeps working unchanged. Static type
checkers (mypy/pyright) and IDEs see the field shape and provide autocomplete.

Currently typed:
    - ``ZeroDteResponse`` (full payload of GET /v1/exposure/zero-dte/{symbol})

All numeric fields are typed ``Optional[float]``/``Optional[int]`` because
the API returns ``null`` for any value it can't compute (insufficient data,
market closed, etc.). Treat the typed shape as a *hint*, not a guarantee —
unknown fields added by the API in future revisions will still pass through.
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict


class ZeroDteRegime(TypedDict, total=False):
    label: str
    description: str
    gamma_flip: Optional[float]
    spot_vs_flip: Literal["above", "below"]
    spot_to_flip_pct: Optional[float]
    distance_to_flip_dollars: Optional[float]
    distance_to_flip_sigmas: Optional[float]


class ZeroDteExposures(TypedDict, total=False):
    net_gex: float
    net_dex: float
    net_vex: float
    net_chex: float
    pct_of_total_gex: Optional[float]
    total_chain_net_gex: float


class ZeroDteExpectedMove(TypedDict, total=False):
    implied_1sd_dollars: Optional[float]
    implied_1sd_pct: Optional[float]
    remaining_1sd_dollars: Optional[float]
    remaining_1sd_pct: Optional[float]
    upper_bound: Optional[float]
    lower_bound: Optional[float]
    straddle_price: Optional[float]
    atm_iv: Optional[float]


class ZeroDtePinComponents(TypedDict, total=False):
    oi_score: int
    proximity_score: int
    time_score: int
    gamma_score: int


class ZeroDtePinRisk(TypedDict, total=False):
    magnet_strike: Optional[float]
    magnet_gex: Optional[float]
    distance_to_magnet_pct: Optional[float]
    pin_score: int
    components: ZeroDtePinComponents
    max_pain: Optional[float]
    oi_concentration_top3_pct: Optional[float]
    description: str


class ZeroDteHedgingBucket(TypedDict, total=False):
    dealer_shares_to_trade: float
    direction: Literal["buy", "sell"]
    notional_usd: float


class ZeroDteHedging(TypedDict, total=False):
    spot_up_10bp: ZeroDteHedgingBucket
    spot_down_10bp: ZeroDteHedgingBucket
    spot_up_25bp: ZeroDteHedgingBucket
    spot_down_25bp: ZeroDteHedgingBucket
    spot_up_half_pct: ZeroDteHedgingBucket
    spot_down_half_pct: ZeroDteHedgingBucket
    spot_up_1pct: ZeroDteHedgingBucket
    spot_down_1pct: ZeroDteHedgingBucket
    convexity_at_spot: Optional[float]


class ZeroDteDecay(TypedDict, total=False):
    net_theta_dollars: Optional[float]
    theta_per_hour_remaining: Optional[float]
    charm_regime: str
    charm_description: str
    gamma_acceleration: Optional[float]
    description: str


class ZeroDteVolContext(TypedDict, total=False):
    zero_dte_atm_iv: Optional[float]
    seven_dte_atm_iv: Optional[float]
    iv_ratio_0dte_7dte: Optional[float]
    vix: Optional[float]
    vanna_exposure: Optional[float]
    vanna_interpretation: str
    description: str


class ZeroDteFlow(TypedDict, total=False):
    total_volume: int
    call_volume: int
    put_volume: int
    net_call_minus_put_volume: int
    total_oi: int
    call_oi: int
    put_oi: int
    pc_ratio_volume: Optional[float]
    pc_ratio_oi: Optional[float]
    volume_to_oi_ratio: Optional[float]
    atm_volume_share_pct: Optional[float]
    top3_strike_volume_pct: Optional[float]


class ZeroDteLevels(TypedDict, total=False):
    call_wall: Optional[float]
    call_wall_gex: Optional[float]
    call_wall_strength: Optional[float]
    distance_to_call_wall_pct: Optional[float]
    put_wall: Optional[float]
    put_wall_gex: Optional[float]
    put_wall_strength: Optional[float]
    distance_to_put_wall_pct: Optional[float]
    distance_to_magnet_dollars: Optional[float]
    highest_oi_strike: Optional[float]
    highest_oi_total: Optional[int]
    max_positive_gamma: Optional[float]
    max_negative_gamma: Optional[float]
    level_cluster_score: Optional[int]


class ZeroDteLiquidity(TypedDict, total=False):
    atm_spread_pct: Optional[float]
    weighted_spread_pct: Optional[float]
    execution_score: Optional[int]


class ZeroDteMetadata(TypedDict, total=False):
    snapshot_age_seconds: Optional[float]
    chain_contract_count: int
    data_quality_score: Optional[int]
    greek_smoothness_score: Optional[int]


class ZeroDteStrike(TypedDict, total=False):
    strike: float
    distance_from_spot_pct: float
    call_symbol: str
    put_symbol: str
    call_gex: Optional[float]
    put_gex: Optional[float]
    net_gex: Optional[float]
    call_dex: Optional[float]
    put_dex: Optional[float]
    net_dex: Optional[float]
    net_vex: Optional[float]
    net_chex: Optional[float]
    call_oi: Optional[int]
    put_oi: Optional[int]
    call_volume: Optional[int]
    put_volume: Optional[int]
    gex_share_pct: Optional[float]
    oi_share_pct: Optional[float]
    volume_share_pct: Optional[float]
    call_iv: Optional[float]
    put_iv: Optional[float]
    call_delta: Optional[float]
    put_delta: Optional[float]
    call_gamma: Optional[float]
    put_gamma: Optional[float]
    call_theta: Optional[float]
    put_theta: Optional[float]
    call_mid: Optional[float]
    put_mid: Optional[float]
    call_spread_pct: Optional[float]
    put_spread_pct: Optional[float]


class ZeroDteResponse(TypedDict, total=False):
    """Full response for GET /v1/exposure/zero-dte/{symbol}.

    On weekends/holidays or symbols without 0DTE today, ``no_zero_dte`` is
    ``True`` and most fields are absent — only ``symbol``, ``as_of``,
    ``message``, and ``next_zero_dte_expiry`` are populated.
    """

    symbol: str
    underlying_price: float
    expiration: Optional[str]
    as_of: str
    market_open: bool
    time_to_close_hours: Optional[float]
    time_to_close_pct: Optional[float]
    regime: ZeroDteRegime
    exposures: ZeroDteExposures
    expected_move: ZeroDteExpectedMove
    pin_risk: ZeroDtePinRisk
    hedging: ZeroDteHedging
    decay: ZeroDteDecay
    vol_context: ZeroDteVolContext
    flow: ZeroDteFlow
    levels: ZeroDteLevels
    liquidity: ZeroDteLiquidity
    metadata: ZeroDteMetadata
    strikes: List[ZeroDteStrike]
    # Optional — only present near close (<5 min) when greeks may be unstable.
    warnings: List[str]
    # ── No-0DTE fallback ─────────────────────────────────────────────
    no_zero_dte: bool
    message: str
    next_zero_dte_expiry: Optional[str]


# ─── ExposureSummary ─────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/exposure/summary/{symbol}``.
#
# This is the single most-called endpoint in the FlashAlpha SDK family:
# one round-trip returns net dealer Greeks (gamma/delta/vanna/charm), the
# gamma-flip strike, the dealer hedging-flow estimate at ±1% spot moves,
# verbal regime narratives, and a 0DTE attribution. The shape is identical
# on the live API and on /v1/exposure/summary/{symbol}?at=... (historical).
#
# Direction casing: /v1/exposure/summary/ and /v1/exposure/zero-dte/ both
# return lowercase "buy" / "sell". The published API doc shows uppercase
# on summary, but the actual response is lowercase — these typed models
# reflect the live response, not the doc.


class ExposureSummaryExposures(TypedDict, total=False):
    """Net dealer Greek totals across the entire option chain.

    Each value is computed as ``Σ greek × OI × multiplier × spot_factor``
    over every contract in the chain. Sign convention: positive means
    dealers are net long that Greek, negative means net short.

    Field-level ``Optional`` matches C#/Go/Java (defensive — the API may
    return ``null`` under unobserved edge conditions even when the parent
    block is present, e.g. very thin chains where one Greek can't be
    aggregated cleanly).
    """

    # Net gamma exposure in dollars per 1% spot move. Positive (dealers
    # long gamma) → moves dampened, mean-reversion likely. Negative (short
    # gamma) → moves amplified, trend-following likely.
    net_gex: Optional[float]
    # Net delta exposure in dollars. Sign is the direction of the dealer
    # hedge book against options inventory. Negative ≈ dealers net-short
    # the underlying as a delta hedge against long-call inventory.
    net_dex: Optional[float]
    # Net vanna exposure in dollars per 1-vol-point. Positive = dealers
    # benefit from vol compression and tend to BUY stock when vol drops
    # (vanna-driven supportive bid); negative is the inverse.
    net_vex: Optional[float]
    # Net charm exposure in dollars per day. Captures the time-decay drift
    # in dealer delta. Positive = dealers must BUY into close to stay
    # neutral (supportive); negative = SELL into close (pressure).
    net_chex: Optional[float]


class ExposureSummaryInterpretation(TypedDict, total=False):
    """Plain-English narrative for each Greek regime.

    Generated server-side from the numeric exposures and macro context;
    safe to surface verbatim in customer-facing UIs (newsletters, chat
    bots, dashboards). One-sentence summaries — not full analysis.
    """

    # E.g. "Dealers long gamma — moves dampened, mean reversion likely".
    gamma: Optional[str]
    # E.g. "Vol up = dealers buy delta — downside dampened if vol spikes".
    # Conditional on prevailing VIX.
    vanna: Optional[str]
    # E.g. "Time decay pushing dealers to sell — pressure into close".
    charm: Optional[str]


class ExposureSummaryHedgingMove(TypedDict, total=False):
    """One side (up or down) of the dealer-hedging-flow estimate.

    Estimates the order flow dealers would generate to remain delta-neutral
    if spot moved by the indicated amount (typically ±1% on summary). Use
    these as a sizing reference for intraday momentum/mean-reversion
    setups: large positive ``dealer_shares_to_trade`` = lots of forced
    BUYING by dealers if spot rises = self-reinforcing momentum.
    """

    # Estimated shares dealers must trade. Positive = buy, negative = sell.
    # spot_up_1pct and spot_down_1pct are equal in magnitude with opposite
    # signs (linearised from net_dex around current spot).
    dealer_shares_to_trade: Optional[float]
    # Lowercase ``"buy"`` or ``"sell"`` — convenience label matching the
    # sign of ``dealer_shares_to_trade``. (The public API doc shows
    # uppercase ``"BUY"``/``"SELL"`` but the live response is lowercase —
    # confirmed via probe; we model the actual response.)
    direction: Optional[Literal["buy", "sell"]]
    # ``|dealer_shares_to_trade| × current_spot``. Useful for cross-symbol
    # comparison: a 1M-share hedge in SPY ($600 spot) is much larger than
    # a 1M-share hedge in HOOD ($30 spot), and notional captures that.
    notional_usd: Optional[float]


class ExposureSummaryHedgingEstimate(TypedDict, total=False):
    """Estimated dealer hedging flow at +/- 1% spot moves.

    The two sides are symmetric: equal magnitude with opposite signs
    (linearised from ``net_dex``). For a fully nonlinear view at multiple
    move sizes, use the zero-dte endpoint which exposes ±10bp / ±25bp /
    ±50bp / ±1pct buckets plus a convexity-at-spot term.
    """

    # Hedging flow if spot rises 1%.
    spot_up_1pct: ExposureSummaryHedgingMove
    # Hedging flow if spot falls 1%. Equal magnitude to spot_up_1pct,
    # opposite sign.
    spot_down_1pct: ExposureSummaryHedgingMove


class ExposureSummaryZeroDte(TypedDict, total=False):
    """Same-day-expiration contribution to the chain totals.

    0DTE GEX is often the dominant intraday driver — gamma compresses to
    a delta function as expiry approaches, so even a small notional 0DTE
    book can swamp the rest of the chain in dealer-flow terms.
    """

    # Net GEX contribution from same-day-expiration contracts only.
    net_gex: Optional[float]
    # 0DTE share of full-chain GEX as a percentage. >50% means today's
    # expiry drives the dealer book; tradable signal.
    pct_of_total_gex: Optional[float]
    # ISO date of today's 0DTE if one exists (``"yyyy-MM-dd"``). ``None``
    # on days without a same-day expiry (e.g. SPY on Tuesday/Thursday
    # before the daily-expiry rollout in 2022; equity options that don't
    # offer daily expiries).
    expiration: Optional[str]


class ExposureSummaryResponse(TypedDict, total=False):
    """Composite dealer-positioning snapshot from ``GET /v1/exposure/summary/{symbol}``.

    The single most common endpoint for "where are dealers right now?"
    (live API) or "where were dealers at this minute?" (historical API
    via ``?at=...``). One round-trip returns:

        - net Greeks (gamma/delta/vanna/charm) across the entire chain
        - the gamma-flip strike (where net GEX crosses zero)
        - the hedging-flow estimate at ±1% spot moves
        - verbal interpretation of each regime
        - 0DTE attribution to the totals

    For deeper intraday detail (±10bp / ±25bp / ±50bp hedging buckets,
    pin-risk scoring, time-to-close decay) use ``GET /v1/exposure/zero-dte/``.

    Notes
    -----
    - All response fields are nullable at the leaf level — the API may
      omit individual numbers under thin-data conditions.
    - ``regime`` is computed from ``spot vs gamma_flip``; not directly
      from ``net_gex``. They usually agree but not always (e.g. when a
      single deep ITM strike skews ``net_gex`` away from the flip).
    - The historical version of this endpoint (``historical.flashalpha.com``)
      returns the exact same shape, just with a required ``?at=`` query
      parameter and ``as_of`` snapped to the available minute.
    """

    # Underlying symbol echoed from the request path (e.g. ``"SPY"``).
    symbol: str
    # Current spot mid (live) or minute-snapped quote (historical), in
    # dollars. The reference price for all GEX/DEX/VEX/CHEX dollarisation.
    underlying_price: Optional[float]
    # ET wall-clock timestamp this snapshot was computed for. On historical,
    # snapped to the nearest available minute; on live, the most recent
    # quote tick used in the calculation.
    as_of: str
    # Strike where net dealer gamma exposure crosses zero. Spot ABOVE the
    # flip = positive-gamma regime (dealers dampen moves, mean-reversion
    # likely). Spot BELOW = negative-gamma (dealers amplify moves, trend-
    # following likely). One of the two or three numbers most experienced
    # users actually look at on this endpoint.
    gamma_flip: Optional[float]
    # Dealer-positioning regime classification:
    #   - ``"positive_gamma"``: spot above gamma_flip
    #   - ``"negative_gamma"``: spot below gamma_flip
    #   - ``"unknown"``: insufficient options data to compute a flip
    # Confirmed live values across Py/JS/.NET/Go/Java integration tests.
    # Don't conflate with ``maxpain.signal`` (a separate
    # bullish/bearish/neutral classifier on a different endpoint).
    regime: Literal["positive_gamma", "negative_gamma", "unknown"]
    # Net Greek totals across the entire chain. See ``ExposureSummaryExposures``.
    exposures: ExposureSummaryExposures
    # Plain-English narrative for each Greek regime — safe to surface to
    # end users verbatim. See ``ExposureSummaryInterpretation``.
    interpretation: ExposureSummaryInterpretation
    hedging_estimate: ExposureSummaryHedgingEstimate
    zero_dte: ExposureSummaryZeroDte


# ─── VRP (Variance Risk Premium) ─────────────────────────────────────────────
#
# Typed model for ``GET /v1/vrp/{symbol}`` (Alpha+).
#
# This is THE classic nested-trap endpoint in the FlashAlpha API. Every
# customer who has tripped on this response has hit at least one of the
# silent-null patterns these types make impossible at the SDK boundary:
#
#   - ``response["z_score"]``  ✗  (KeyError) — actual: ``response["vrp"]["z_score"]``
#   - ``response["percentile"]`` ✗ — actual: ``response["vrp"]["percentile"]``
#   - ``response["put_vrp"]`` ✗ — actual: ``response["directional"]["downside_vrp"]``
#   - ``response["net_gex"]`` ✗ — actual: ``response["regime"]["net_gex"]``
#
# The canonical FlashAlpha names are nested deliberately so a "vrp"
# response cleanly groups core metrics, directional skew, regime, and
# strategy scores into separate sub-objects, at the cost of one extra
# attribute lookup. Use the typed shape; the docstrings tell you exactly
# where to look.


class VrpCore(TypedDict, total=False):
    """Core VRP metrics block — the heart of the response.

    The variance risk premium is the spread between IMPLIED volatility
    (forward-looking, priced into options) and REALIZED volatility
    (backward-looking, observed from spot returns). Positive VRP = options
    are pricing more vol than the underlying actually moved → premium for
    selling vol. Negative VRP = options too cheap relative to realized →
    premium for buying vol.

    Nested under ``response["vrp"]`` — NOT top-level. ``response["z_score"]``
    is a KeyError; use ``response["vrp"]["z_score"]``.
    """

    # At-the-money implied volatility (annualised, percentage points,
    # e.g. 18.5 = 18.5%). Pulled from the nearest SVI slice.
    atm_iv: Optional[float]
    # Realized volatility ladders — annualised %, computed from spot
    # log-returns over the trailing 5/10/20/30 trading days.
    rv_5d: Optional[float]
    rv_10d: Optional[float]
    rv_20d: Optional[float]
    rv_30d: Optional[float]
    # Variance risk premia at each horizon: ``atm_iv - rv_Nd``. Positive =
    # IV richer than realised (premium for selling vol). Negative = IV
    # cheaper than realised (premium for buying vol).
    vrp_5d: Optional[float]
    vrp_10d: Optional[float]
    vrp_20d: Optional[float]
    vrp_30d: Optional[float]
    # Z-score of the current 20-day VRP vs its trailing ``history_days``-
    # day window. ``+2.0`` means today's VRP is 2 standard deviations
    # richer than recent history → unusually rich, often a fade signal.
    # ``None`` on historical responses with insufficient warm-up
    # (e.g. queries near 2018-04-16, the start of the dataset).
    z_score: Optional[float]
    # Percentile rank (0-100) of the current VRP within the trailing
    # window. ``100`` = highest VRP in living memory; ``0`` = lowest.
    # ``None`` when ``history_days`` is too small to compute a percentile.
    percentile: Optional[int]
    # Number of trading days in the trailing percentile/z-score window.
    # When this is small (< ~30), treat ``z_score`` and ``percentile`` as
    # noise. Live API computes against ~252 days; historical scales with
    # how far past 2018-04-16 the ``at`` timestamp is.
    history_days: Optional[int]


class VrpDirectional(TypedDict, total=False):
    """Directional VRP skew — separates upside-tail vs downside-tail premia.

    Splits the variance risk premium by direction: how much premium are
    options pricing on the DOWNSIDE (puts) vs the UPSIDE (calls). A large
    ``downside_vrp`` with small ``upside_vrp`` is the classic "expensive
    crash insurance" pattern — premium for selling puts in calm tape.

    The canonical field names are ``downside_vrp`` and ``upside_vrp``.
    Customers from other vendors often type ``put_vrp`` / ``call_vrp`` —
    those don't exist on this response. Use the documented names.
    """

    # IV at the 25-delta put wing (bottom-tail crash insurance pricing).
    put_wing_iv_25d: Optional[float]
    # IV at the 25-delta call wing (top-tail upside insurance pricing).
    call_wing_iv_25d: Optional[float]
    # Realized vol of the DOWNSIDE-only return distribution (negative spot
    # returns over trailing 20 days, semi-deviation).
    downside_rv_20d: Optional[float]
    # Realized vol of the UPSIDE-only return distribution.
    upside_rv_20d: Optional[float]
    # ``put_wing_iv_25d - downside_rv_20d``. Positive = downside crash
    # protection priced richer than the actual downside RV — premium for
    # short-put / short-strangle harvest.
    downside_vrp: Optional[float]
    # ``call_wing_iv_25d - upside_rv_20d``. Positive = upside calls priced
    # rich → premium for short-call / covered-call harvest.
    upside_vrp: Optional[float]


class VrpTermItem(TypedDict, total=False):
    """One row of the VRP term structure — an (DTE, IV, RV, VRP) tuple."""

    # Days to expiry for this row (e.g. 7, 14, 30, 60, 90).
    dte: Optional[int]
    # Implied vol at this tenor (annualised %).
    iv: Optional[float]
    # Realized vol over a window matched to the tenor (annualised %).
    rv: Optional[float]
    # Tenor-matched VRP: ``iv - rv`` for this DTE bucket.
    vrp: Optional[float]


class VrpGexConditioned(TypedDict, total=False):
    """VRP harvest score conditioned on the prevailing dealer-gamma regime.

    The same VRP number means very different things depending on whether
    dealers are long or short gamma. Long-gamma + rich VRP = mean-reverting
    tape with rich vol → ideal short-vol harvest. Short-gamma + rich VRP =
    trending tape with rich vol → harvest is dangerous, dealers will
    amplify any directional move that breaks the range.
    """

    # Gamma regime at this snapshot — derived from spot vs gamma-flip on
    # the same chain. ``"positive_gamma"`` | ``"negative_gamma"`` |
    # ``"unknown"`` (when net_gex straddles zero or there's insufficient
    # data to classify).
    regime: Optional[Literal["positive_gamma", "negative_gamma", "unknown"]]
    # 0-100 composite — how favourable the current VRP is to harvest GIVEN
    # the gamma regime. >70 = strong harvest signal; <30 = avoid; in
    # between = mixed.
    harvest_score: Optional[float]
    # Plain-English explanation of the harvest_score. Safe to surface
    # verbatim in customer-facing UIs.
    interpretation: Optional[str]


class VrpVannaConditioned(TypedDict, total=False):
    """VRP outlook conditioned on net dealer vanna exposure.

    Dealer vanna determines how the dealer hedge book responds to a vol
    shock. Positive vanna + spike in VIX = dealers buy stock (supportive);
    negative vanna + VIX spike = dealers sell (cascade risk).
    """

    # Forward-looking outlook label (e.g. ``"vanna_supportive"``,
    # ``"vanna_cascade_risk"``, ``"vanna_neutral"``).
    outlook: Optional[str]
    # Plain-English narrative for the vanna outlook.
    interpretation: Optional[str]


class VrpRegime(TypedDict, total=False):
    """Regime snapshot block — gamma + vrp regime + dealer state.

    The ``net_gex`` field on this object is the canonical place to read
    net dealer GEX from a VRP response. Customers often expect
    ``response["net_gex"]`` (top-level) — that's a KeyError. Use
    ``response["regime"]["net_gex"]``.
    """

    # ``"positive_gamma"`` | ``"negative_gamma"`` | ``"unknown"`` —
    # same classifier as exposure_summary.
    gamma: Optional[Literal["positive_gamma", "negative_gamma", "unknown"]]
    # ``"harvestable"`` | ``"selling_too_cheap"`` | ``"buying_too_cheap"``
    # | ``"neutral"`` etc. — describes the VRP environment in trading
    # vocabulary. ``None`` on historical when there's not enough history
    # to classify.
    vrp_regime: Optional[str]
    # Net dealer gamma exposure in dollars per 1% spot move. Same as
    # exposure_summary.exposures.net_gex (just exposed under a different
    # parent on this endpoint for convenience). NOT top-level.
    net_gex: Optional[float]
    # Strike where net dealer gamma crosses zero. Same as
    # exposure_summary.gamma_flip.
    gamma_flip: Optional[float]


class VrpStrategyScores(TypedDict, total=False):
    """0-100 suitability scores for canonical short-vol strategies.

    Higher = better fit for current market conditions. These are
    heuristic composites of VRP magnitude, directional skew, gamma regime,
    and vanna conditioning. ``None`` for any field on historical responses
    where the underlying inputs (e.g. percentile) are not computable.
    """

    # Short put credit spread — sells downside VRP with capped loss.
    short_put_spread: Optional[int]
    # Short strangle — sells both wings; max profit if spot pins.
    short_strangle: Optional[int]
    # Iron condor — defined-risk version of short strangle.
    iron_condor: Optional[int]
    # Calendar spread — sells front-month vol, buys back-month. Profits
    # from front-month time decay if spot pins. Best when the term
    # structure is steep contango.
    calendar_spread: Optional[int]


class VrpMacro(TypedDict, total=False):
    """Macro-context snapshot used to condition the VRP outlook.

    Note diffs across live vs historical:
        - ``hy_spread``: live = ``None``; historical = float.
        - ``fed_funds``: live = float; historical = field absent.
    """

    # CBOE VIX index level.
    vix: Optional[float]
    # CBOE VIX3M (3-month VIX).
    vix_3m: Optional[float]
    # ``(vix_3m - vix) / vix * 100`` — % steepness of near-term term
    # structure. Positive = contango; negative = backwardation.
    vix_term_slope: Optional[float]
    # 10-year US Treasury yield (%, FRED ``DGS10``).
    dgs10: Optional[float]
    # ICE BofA US High Yield OAS (%, FRED ``BAMLH0A0HYM2``). ``None`` on
    # live currently (data pipeline gap on the live API). Populated on
    # historical responses.
    hy_spread: Optional[float]
    # Federal Funds effective rate (%, FRED ``DFF``). Live-only;
    # historical responses omit this field.
    fed_funds: Optional[float]


class VrpResponse(TypedDict, total=False):
    """Variance Risk Premium dashboard from ``GET /v1/vrp/{symbol}``.

    The single most-misread response shape in the FlashAlpha API. Every
    nested block exists for a reason — core metrics, directional skew,
    gamma conditioning, vanna conditioning, regime snapshot, strategy
    scores, and macro context are deliberately separated so the consumer
    can read just the one they care about.

    Common silent-null traps (now type-checked at the SDK boundary):
        - ``response.z_score``  → use ``response["vrp"]["z_score"]``
        - ``response.percentile`` → use ``response["vrp"]["percentile"]``
        - ``response.atm_iv``   → use ``response["vrp"]["atm_iv"]``
        - ``response.rv_20d``   → use ``response["vrp"]["rv_20d"]``
        - ``response.vrp_20d``  → use ``response["vrp"]["vrp_20d"]``
        - ``response.put_vrp``  → use ``response["directional"]["downside_vrp"]``
        - ``response.call_vrp`` → use ``response["directional"]["upside_vrp"]``
        - ``response.net_gex``  → use ``response["regime"]["net_gex"]``
        - ``response.harvest_score`` (top-level scalar) → use
          ``response["gex_conditioned"]["harvest_score"]``;
          ``response["net_harvest_score"]`` is a SEPARATE composite.

    Empty list / null caveats:
        - ``warnings``: present on every response. Empty list when nothing
          worth flagging; populated with strings like
          ``"insufficient_history_for_zscore"`` on historical responses
          that hit data-warmup limits.
        - ``strategy_scores`` and ``net_harvest_score``: ``None`` on
          historical when the inputs (notably ``percentile``) are not
          computable for that ``at`` timestamp.

    Returns 403 ``tier_restricted`` for anything below Alpha plan on both
    live and historical; the endpoint requires Alpha+.
    """

    # Echoed from the request path.
    symbol: str
    # Spot mid at ``as_of`` (live = current; historical = minute-snapped).
    underlying_price: Optional[float]
    # ET wall-clock timestamp of this snapshot.
    as_of: str
    # ``True`` if NYSE was open at ``as_of``. False overnight, weekends,
    # and on holidays.
    market_open: Optional[bool]
    # Core VRP metrics block. See ``VrpCore``.
    vrp: VrpCore
    # Top-level convenience: ``vrp_20d`` / 100, expressed as a decimal
    # for variance-swap-style calculations. (Same number as
    # ``vrp.vrp_20d / 100``.)
    variance_risk_premium: Optional[float]
    # Convexity premium = ``fair_vol - atm_iv``. Captures the curvature
    # premium between the IV smile and the variance-swap fair vol.
    convexity_premium: Optional[float]
    # Variance-swap fair vol — the breakeven implied vol for a synthetic
    # variance swap on this name (annualised %).
    fair_vol: Optional[float]
    # Directional VRP skew (downside vs upside). See ``VrpDirectional``.
    directional: VrpDirectional
    # Term structure — VRP at multiple DTE buckets. List of
    # ``VrpTermItem``. Empty when surface fitting fails.
    term_vrp: List[VrpTermItem]
    # GEX-conditioned harvest score. See ``VrpGexConditioned``.
    gex_conditioned: VrpGexConditioned
    # Vanna-conditioned outlook. See ``VrpVannaConditioned``.
    vanna_conditioned: VrpVannaConditioned
    # Regime snapshot — gamma + vrp regime + dealer state. See
    # ``VrpRegime``. ``net_gex`` lives HERE, not at the top level.
    regime: VrpRegime
    # 0-100 strategy suitability scores. See ``VrpStrategyScores``.
    # ``None`` on historical when warmup is too short.
    strategy_scores: Optional[VrpStrategyScores]
    # 0-100 composite — overall harvest signal across all four strategy
    # scores plus the gamma/vanna conditioning. Use this as the single
    # number you'd put on a dashboard. ``None`` on historical when
    # warmup is too short.
    net_harvest_score: Optional[int]
    # 0-100 — risk that dealer hedging flow disrupts a short-vol harvest
    # (e.g. negative gamma cascade, vanna-driven sell into vol spike).
    # Use as a ``careful``-flag alongside ``net_harvest_score``.
    dealer_flow_risk: Optional[int]
    # Server-side warnings about data quality / regime instability.
    # Examples: ``"insufficient_history_for_zscore"``,
    # ``"thin_chain_open_interest"``. Always present (possibly empty list).
    warnings: List[str]
    # Macro context. See ``VrpMacro``.
    macro: VrpMacro


# ─── MaxPain ─────────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/maxpain/{symbol}`` (Basic+).
#
# Max pain is the strike where total option-holder intrinsic value across all
# OI in the chain is minimized — equivalently, the strike at which dealers
# (the counterparty) lose the least to expiring contracts. The endpoint also
# overlays GEX-based dealer alignment, a multi-expiry calendar (full chain
# only), and a 0-100 pin probability score.


class MaxPainDistance(TypedDict, total=False):
    """Distance from spot to the max-pain strike."""

    # Dollar distance: ``|underlying_price - max_pain_strike|``.
    absolute: Optional[float]
    # Percent of spot: ``absolute / underlying_price * 100``. Use this to
    # compare across symbols of different price levels.
    percent: Optional[float]
    # ``"above"`` (spot > max_pain), ``"below"`` (spot < max_pain), or
    # ``"at"`` (within rounding). The signal field uses this + a 5%
    # threshold to derive the bullish/bearish/neutral classification.
    direction: Optional[Literal["above", "below", "at"]]


class MaxPainCurveRow(TypedDict, total=False):
    """One row of the strike-by-strike pain curve.

    Each row is the dollar pain (intrinsic value × OI × 100 contract
    multiplier) summed across all expirations at that strike. The strike
    where ``total_pain`` is minimized is the max-pain strike.
    """

    strike: Optional[float]
    # Dollar intrinsic value of all calls at this strike summed across the
    # chain (when spot pins here, this is what call holders collectively win
    # vs the dealer side).
    call_pain: Optional[float]
    # Dollar intrinsic value of all puts at this strike. Mirror of
    # ``call_pain`` for the put side.
    put_pain: Optional[float]
    # ``call_pain + put_pain``. The pain curve's minimum identifies max pain.
    total_pain: Optional[float]


class MaxPainOiRow(TypedDict, total=False):
    """One row of the OI-by-strike breakdown.

    Per-strike open interest and volume by side. Lets you see where the
    OI is concentrated independent of the dollar-weighted pain calculation.

    Note: on the Historical API, ``call_volume`` and ``put_volume`` are
    always ``0`` (placeholder fields — the minute table doesn't carry
    intraday volume).
    """

    strike: Optional[float]
    call_oi: Optional[int]
    put_oi: Optional[int]
    total_oi: Optional[int]
    call_volume: Optional[int]
    put_volume: Optional[int]


class MaxPainByExpirationRow(TypedDict, total=False):
    """Per-expiry max-pain breakdown when no ``expiration`` filter is applied.

    Lets you see how max pain shifts across the term structure — useful for
    spotting cases where the front-week max pain differs sharply from the
    LEAP max pain (often a sign of where the dealer flow is most active).

    This list is ``None`` when the request specifies an ``expiration``
    filter — the response is then scoped to that single expiry and the
    multi-expiry view is suppressed.
    """

    # ``"yyyy-MM-dd"`` of this expiry.
    expiration: Optional[str]
    # Max-pain strike for this expiry's option chain alone.
    max_pain_strike: Optional[float]
    # Days to expiry (counting from ``as_of``).
    dte: Optional[int]
    # Sum of OI across all contracts at this expiry.
    total_oi: Optional[int]


class MaxPainDealerAlignment(TypedDict, total=False):
    """GEX-based dealer-alignment overlay on the max-pain view.

    Re-uses the same gamma-exposure inputs as ``/v1/exposure/levels`` and
    ``/v1/exposure/summary``. The headline ``alignment`` label tells you
    whether dealer hedging will REINFORCE the max-pain pin or fight it:

        - ``"converging"``: max pain near gamma flip and between the
          walls — dealer hedging supports the pin (strongest pin setup).
        - ``"moderate"``: max pain between the walls but far from flip.
        - ``"diverging"``: max pain outside the wall range — dealer
          hedging actively pushes spot away from max pain.
        - ``"unknown"``: insufficient data to classify.
    """

    alignment: Optional[Literal["converging", "moderate", "diverging", "unknown"]]
    # Plain-English explanation. Safe to surface verbatim.
    description: Optional[str]
    # Strike where net dealer gamma crosses zero. Same definition as
    # ``exposure_summary.gamma_flip``.
    gamma_flip: Optional[float]
    # Strike with highest absolute call GEX (dealer-side resistance).
    call_wall: Optional[float]
    # Strike with highest absolute put GEX (dealer-side support).
    put_wall: Optional[float]


class MaxPainExpectedMove(TypedDict, total=False):
    """Implied move from the ATM straddle, contextualized vs max pain.

    Tells you whether the max-pain strike is even reachable within the
    options-implied 1σ move. If ``max_pain_within_expected_range`` is
    ``False``, the pin is unlikely to play out by expiry under the current
    IV regime — the magnet exists but spot probably can't get there.
    """

    # ATM straddle mid in dollars. Rough proxy for the 1σ implied move.
    straddle_price: Optional[float]
    # ATM implied volatility (annualised %, e.g. 18.5 = 18.5%).
    atm_iv: Optional[float]
    # ``True`` when ``|spot - max_pain_strike| <= straddle_price``.
    max_pain_within_expected_range: Optional[bool]


class MaxPainResponse(TypedDict, total=False):
    """Max pain dashboard from ``GET /v1/maxpain/{symbol}``.

    Returns the strike where total option-holder pain (intrinsic value × OI)
    is minimized, plus:

        - per-strike pain curve and OI breakdown
        - per-expiry calendar (when no ``expiration`` filter is set)
        - GEX-based dealer alignment overlay (call wall / put wall /
          gamma flip — same numbers as ``/v1/exposure/levels``)
        - expected move from the ATM straddle
        - 0-100 pin probability composite

    The endpoint accepts an optional ``expiration`` query filter
    (``yyyy-MM-dd``). When present, the response is scoped to that single
    expiry and ``max_pain_by_expiration`` is ``None``. When absent, the
    full-chain max pain is returned alongside the multi-expiry calendar.

    Returns 403 ``tier_restricted`` for Free-tier users; requires Basic+.
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    # The headline number. Strike where total chain pain is minimized.
    max_pain_strike: Optional[float]
    # Distance from spot to ``max_pain_strike`` (absolute, percent, direction).
    distance: MaxPainDistance
    # ``"bullish"`` (spot >= 5% below max_pain — pin attracts upside),
    # ``"bearish"`` (>= 5% above), or ``"neutral"`` (within 5%).
    signal: Optional[Literal["bullish", "bearish", "neutral"]]
    # Expiration this view is scoped to. When the request omits the
    # ``expiration`` filter, this field is the front-month expiry the
    # full-chain max pain happened to land on.
    expiration: Optional[str]
    # Total put OI / total call OI across the relevant chain. >1.0 means
    # put-heavy positioning. Often correlates with ``signal == "bullish"``
    # (puts are protection; heavy-put chains often have spot below max pain).
    put_call_oi_ratio: Optional[float]
    # Strike-by-strike pain curve. The minimum is at ``max_pain_strike``.
    pain_curve: List[MaxPainCurveRow]
    # Per-strike OI + volume breakdown. Same strike grid as ``pain_curve``.
    oi_by_strike: List[MaxPainOiRow]
    # Per-expiry calendar. ``None`` when the request specified an expiry.
    max_pain_by_expiration: Optional[List[MaxPainByExpirationRow]]
    # GEX-based dealer alignment overlay. See ``MaxPainDealerAlignment``.
    dealer_alignment: MaxPainDealerAlignment
    # Same gamma classification as on ``exposure_summary``:
    # positive_gamma | negative_gamma | unknown.
    regime: Optional[Literal["positive_gamma", "negative_gamma", "unknown"]]
    # Expected move from the ATM straddle, contextualized vs max pain.
    expected_move: MaxPainExpectedMove
    # 0-100 composite — likelihood of pinning to ``max_pain_strike``.
    # Inputs: OI concentration (30%), magnet proximity (25%), time
    # remaining (25%), gamma magnitude (20%). Most meaningful for near-term
    # expiries — for LEAPs this score will be low regardless of OI shape.
    pin_probability: Optional[int]


# ─── StockSummary ────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/stock/{symbol}/summary``.
#
# This is FlashAlpha's "single best snapshot" endpoint — one round-trip
# returns the price quote, IV/HV/VRP, the 25-delta skew triangle, the IV
# term structure, options flow aggregates, the full dealer-exposure view
# (Greeks, walls, gamma flip, max pain, hedging estimate, 0DTE attribution,
# top strikes), and the macro context (VIX, VVIX, SKEW, MOVE, term
# structure, fear/greed). Use this when you need a one-call dashboard
# rather than orchestrating exposure/zero-dte/vrp/macro separately.
#
# Dual-mode auth:
#   - Authenticated (with API key): live, current-minute snapshot.
#   - Unauthenticated: previous-day cached snapshot (free preview tier).
#
# Hedging-estimate sign convention DIFFERS from /v1/exposure/zero-dte:
#   - On stock_summary, ``hedging_estimate.spot_*_1pct.dealer_shares`` is a
#     MAGNITUDE (always positive). The ``direction`` field
#     (``"buy"``/``"sell"``) carries the sign separately.
#   - On zero-dte, the corresponding ``dealer_shares_to_trade`` is signed
#     (positive = buy, negative = sell) AND a ``direction`` label is also
#     present.
# Don't mix the two when porting code between endpoints.


class StockSummaryPrice(TypedDict, total=False):
    """Quote block — bid/ask/mid/last for the underlying."""

    # National best bid in dollars.
    bid: Optional[float]
    # National best offer in dollars.
    ask: Optional[float]
    # ``(bid + ask) / 2``. The reference price used for all option
    # dollarisation (GEX, hedging estimate, expected move).
    mid: Optional[float]
    # Last printed trade in dollars. May lag ``mid`` outside RTH.
    last: Optional[float]
    # ET wall-clock timestamp of the underlying ``last`` print used in
    # this snapshot.
    last_update: Optional[str]


class StockSummarySkew25d(TypedDict, total=False):
    """25-delta skew snapshot at the front-month expiry.

    A compact "smile" descriptor: IVs at the 25-delta put, the ATM, and
    the 25-delta call, plus two derived measures. Useful for spotting
    whether crash insurance is unusually rich (large positive
    ``skew_25d``) or whether call wings are bid (negative ``skew_25d``,
    common in meme-name squeezes).
    """

    # ``"yyyy-MM-dd"`` of the expiry the skew is measured at.
    expiry: Optional[str]
    # Calendar days from ``as_of`` to ``expiry``.
    days_to_expiry: Optional[int]
    # IV at the 25-delta put (annualised %).
    put_25d_iv: Optional[float]
    # ATM implied volatility at this expiry (annualised %).
    atm_iv: Optional[float]
    # IV at the 25-delta call (annualised %).
    call_25d_iv: Optional[float]
    # ``put_25d_iv - call_25d_iv``. Positive = puts richer than calls
    # (downside-skewed smile, the typical equity-index regime).
    skew_25d: Optional[float]
    # ``(put_25d_iv + call_25d_iv) / (2 * atm_iv)`` — the curvature
    # premium of the wings vs the ATM. ``> 1`` means the wings are
    # richer than the ATM (kurtotic smile).
    smile_ratio: Optional[float]


class StockSummaryIvTermItem(TypedDict, total=False):
    """One row of the IV term structure — (expiry, IV, DTE)."""

    # ``"yyyy-MM-dd"`` of this expiry.
    expiry: Optional[str]
    # ATM IV at this expiry (annualised %).
    iv: Optional[float]
    # Calendar days from ``as_of`` to ``expiry``.
    days_to_expiry: Optional[int]


class StockSummaryVolatility(TypedDict, total=False):
    """Volatility block — ATM IV, HV ladders, VRP, skew, term structure.

    Pulls together what would otherwise be three separate endpoint calls
    (``/v1/iv``, ``/v1/hv``, ``/v1/vrp`` headline) into one block.
    """

    # ATM implied volatility at the front-month expiry (annualised %).
    atm_iv: Optional[float]
    # Realized vol over trailing 20 trading days (annualised %).
    hv_20: Optional[float]
    # Realized vol over trailing 60 trading days (annualised %).
    hv_60: Optional[float]
    # Variance Risk Premium = ``atm_iv - hv_20``. Positive = options are
    # pricing more vol than the underlying realised → premium for selling
    # vol. Negative = options too cheap relative to realised. For the
    # full VRP dashboard (z-score, percentile, directional skew) call
    # ``/v1/vrp/{symbol}`` instead.
    vrp: Optional[float]
    # 25-delta skew snapshot. See ``StockSummarySkew25d``.
    skew_25d: StockSummarySkew25d
    # IV term structure — list of (expiry, IV, DTE) rows ordered by DTE.
    iv_term_structure: List[StockSummaryIvTermItem]


class StockSummaryOptionsFlow(TypedDict, total=False):
    """Aggregated chain flow — total OI, volume, and put/call ratios."""

    # Total call open interest across the chain.
    total_call_oi: Optional[int]
    # Total put open interest across the chain.
    total_put_oi: Optional[int]
    # Total call volume traded so far in the session (live) or for the
    # cached day (unauthenticated).
    total_call_volume: Optional[int]
    # Total put volume traded so far in the session.
    total_put_volume: Optional[int]
    # ``total_put_oi / total_call_oi``. ``> 1`` = put-heavy chain
    # (defensive positioning).
    pc_ratio_oi: Optional[float]
    # ``total_put_volume / total_call_volume``. Intraday flow tilt;
    # noisier than the OI ratio but more responsive.
    pc_ratio_volume: Optional[float]
    # Number of distinct expirations carried in the chain at ``as_of``.
    active_expirations: Optional[int]


class StockSummaryInterpretation(TypedDict, total=False):
    """Plain-English narrative for each Greek regime.

    Generated server-side from the numeric exposures and macro context.
    Safe to surface verbatim in customer-facing UIs.
    """

    # E.g. "Dealers long gamma — moves dampened, mean reversion likely".
    gamma: Optional[str]
    # E.g. "Vol up = dealers buy delta — downside dampened if vol spikes".
    vanna: Optional[str]
    # E.g. "Time decay pushing dealers to sell — pressure into close".
    charm: Optional[str]


class StockSummaryHedgingMove(TypedDict, total=False):
    """One side (up or down) of the dealer-hedging-flow estimate.

    NOTE — sign convention DIFFERS from the zero-dte endpoint:
        - On stock_summary, ``dealer_shares`` is the absolute MAGNITUDE
          (always non-negative). The ``direction`` field carries the sign.
        - On zero-dte, ``dealer_shares_to_trade`` is signed.
    """

    # Estimated dealer shares to trade — MAGNITUDE only. Use ``direction``
    # to determine buy vs sell. (Differs from zero-dte; see the parent
    # class docstring.)
    dealer_shares: Optional[float]
    # ``"buy"`` or ``"sell"`` — carries the sign that ``dealer_shares``
    # omits.
    direction: Optional[Literal["buy", "sell"]]
    # ``dealer_shares × current_spot``. Useful for cross-symbol
    # comparison (a 1M-share hedge in SPY is much larger than in HOOD).
    notional_usd: Optional[float]


class StockSummaryHedgingEstimate(TypedDict, total=False):
    """Estimated dealer hedging flow at +/- 1% spot moves.

    Symmetric: equal magnitudes with opposite directions, linearised from
    ``net_dex``. For finer (±10bp / ±25bp / ±50bp) buckets and a
    convexity-at-spot term, use ``/v1/exposure/zero-dte``.
    """

    # Hedging flow estimate if spot rises 1%.
    spot_up_1pct: StockSummaryHedgingMove
    # Hedging flow estimate if spot falls 1%. Equal magnitude, opposite
    # direction.
    spot_down_1pct: StockSummaryHedgingMove


class StockSummaryZeroDte(TypedDict, total=False):
    """Same-day-expiration contribution to the chain totals.

    0DTE GEX is often the dominant intraday driver — gamma compresses to
    a delta function as expiry approaches.
    """

    # Net GEX contribution from same-day-expiration contracts only.
    # Signed: positive = dealers long 0DTE gamma (dampening),
    # negative = short (amplifying).
    net_gex: Optional[float]
    # 0DTE share of full-chain GEX as a percentage. ``> 50`` = today's
    # expiry drives the dealer book.
    pct_of_total: Optional[float]
    # ISO date of today's 0DTE if one exists (``"yyyy-MM-dd"``). ``None``
    # on names without a same-day expiry.
    expiration: Optional[str]


class StockSummaryTopStrike(TypedDict, total=False):
    """One row of the "top strikes by net GEX" leaderboard.

    A condensed version of the per-strike chain: which 5-10 strikes are
    carrying the most dealer-gamma exposure right now.
    """

    # Strike in dollars.
    strike: Optional[float]
    # Net GEX contribution from this strike (calls minus puts, both
    # sides aggregated). Signed: positive = dealer long gamma at this
    # strike; negative = short.
    net_gex: Optional[float]
    # Call open interest at this strike.
    call_oi: Optional[int]
    # Put open interest at this strike.
    put_oi: Optional[int]
    # ``call_oi + put_oi``.
    total_oi: Optional[int]


class StockSummaryExposure(TypedDict, total=False):
    """Full dealer-exposure block — Greeks, walls, regime, hedging, top strikes.

    Combines the headline numbers from ``/v1/exposure/summary``,
    ``/v1/exposure/levels``, and a condensed top-strikes leaderboard.
    For the canonical full-chain view use the dedicated endpoints.

    This block is ``Optional[StockSummaryExposure]`` on the parent
    response — when the symbol has no usable options data, the entire
    exposure block is ``None`` rather than a dict full of nulls.
    """

    # Net dealer gamma exposure, dollars per 1% spot move. Signed.
    net_gex: Optional[float]
    # Net dealer delta exposure, dollars. Signed.
    net_dex: Optional[float]
    # Net dealer vanna exposure, dollars per 1-vol-point. Signed.
    net_vex: Optional[float]
    # Net dealer charm exposure, dollars per day. Signed.
    net_chex: Optional[float]
    # Strike where net dealer gamma crosses zero. Spot ABOVE = positive-
    # gamma regime (mean-reverting); spot BELOW = negative-gamma
    # (trend-following).
    gamma_flip: Optional[float]
    # Strike with highest absolute call GEX (dealer-side resistance).
    call_wall: Optional[float]
    # Strike with highest absolute put GEX (dealer-side support).
    put_wall: Optional[float]
    # Strike where total option-holder pain (intrinsic × OI) is
    # minimized — pin magnet near expiry.
    max_pain: Optional[float]
    # Strike with the largest total OI (calls + puts) across the chain.
    highest_oi_strike: Optional[float]
    # Dealer-positioning regime classification:
    #   - ``"positive_gamma"``: spot above gamma_flip (mean-reverting)
    #   - ``"negative_gamma"``: spot below gamma_flip (trend-following)
    #   - ``"unknown"``: insufficient options data to compute
    regime: Optional[Literal["positive_gamma", "negative_gamma", "unknown"]]
    # Plain-English narrative for each Greek regime. Safe to surface
    # verbatim. See ``StockSummaryInterpretation``.
    interpretation: StockSummaryInterpretation
    # Estimated dealer hedging flow at ±1% spot moves. NOTE: the
    # ``dealer_shares`` field on this endpoint is MAGNITUDE only — the
    # ``direction`` field carries the sign. See
    # ``StockSummaryHedgingMove``.
    hedging_estimate: StockSummaryHedgingEstimate
    # Same-day-expiration attribution. See ``StockSummaryZeroDte``.
    zero_dte: StockSummaryZeroDte
    # Top strikes leaderboard ordered by ``|net_gex|`` (descending).
    top_strikes: List[StockSummaryTopStrike]
    # OI-weighted average days-to-expiry of the chain. Higher = chain
    # weighted toward longer-dated contracts.
    oi_weighted_dte: Optional[float]


class StockSummaryMacroIndex(TypedDict, total=False):
    """One macro index level (VIX, VVIX, SKEW, SPX, MOVE).

    All three fields can be ``None`` together when the upstream macro
    feed is unavailable — the parent ``StockSummaryMacro`` block
    degrades field-by-field rather than going entirely missing.
    """

    # Current level of the index.
    value: Optional[float]
    # Absolute change vs prior close.
    change: Optional[float]
    # Percent change vs prior close.
    change_pct: Optional[float]


class StockSummaryVixTermLevels(TypedDict, total=False):
    """VIX term-structure levels: 9-day / 30-day / 3-month / 6-month."""

    # CBOE VIX9D (9-day).
    vix9d: Optional[float]
    # CBOE VIX (30-day).
    vix: Optional[float]
    # CBOE VIX3M (3-month).
    vix3m: Optional[float]
    # CBOE VIX6M (6-month).
    vix6m: Optional[float]


class StockSummaryVixTermStructure(TypedDict, total=False):
    """VIX term structure shape — levels, near slope, contango/backwardation."""

    # The four term-structure levels. See ``StockSummaryVixTermLevels``.
    levels: StockSummaryVixTermLevels
    # ``(vix3m - vix) / vix * 100`` — % steepness of the near term.
    # Positive = contango.
    near_slope_pct: Optional[float]
    # Headline classification: ``"contango"`` (vix < vix3m, normal
    # regime) or ``"backwardation"`` (vix > vix3m, stress regime).
    structure: Optional[Literal["contango", "backwardation"]]


class StockSummaryVixFutures(TypedDict, total=False):
    """VIX futures basis — front-month vs spot VIX."""

    # Front-month VIX futures price.
    front_month: Optional[float]
    # Spot VIX index level.
    spot: Optional[float]
    # ``front_month - spot``. Positive = futures above spot
    # (contango); negative = below (backwardation).
    spread: Optional[float]
    # ``spread / spot * 100`` — basis as a percentage of spot.
    basis_pct: Optional[float]
    # Headline classification: ``"contango"`` (futures > spot, normal)
    # or ``"backwardation"`` (futures < spot, stress).
    basis: Optional[Literal["contango", "backwardation"]]


class StockSummaryFearAndGreed(TypedDict, total=False):
    """CNN-style fear-and-greed composite for the broader market."""

    # 0-100 score. ``< 25`` = extreme fear, ``> 75`` = extreme greed.
    score: Optional[int]
    # Plain-English label: ``"extreme_fear"``, ``"fear"``, ``"neutral"``,
    # ``"greed"``, ``"extreme_greed"`` (or similar).
    rating: Optional[str]


class StockSummaryMacro(TypedDict, total=False):
    """Macro context block — VIX, VVIX, SKEW, SPX, MOVE, term structure, F&G.

    Any individual field here can be ``None`` when the upstream macro
    feed is degraded or the timestamp is outside the feed's coverage
    (weekends/holidays for some sub-feeds). The block itself is always
    present on a successful response, even if every member is ``None``.
    """

    # CBOE VIX index. See ``StockSummaryMacroIndex``.
    vix: StockSummaryMacroIndex
    # CBOE VVIX (vol of VIX).
    vvix: StockSummaryMacroIndex
    # CBOE SKEW index.
    skew: StockSummaryMacroIndex
    # S&P 500 cash index.
    spx: StockSummaryMacroIndex
    # ICE BofAML MOVE index (rates vol).
    move: StockSummaryMacroIndex
    # VIX term structure shape. See ``StockSummaryVixTermStructure``.
    vix_term_structure: StockSummaryVixTermStructure
    # VIX futures basis. See ``StockSummaryVixFutures``.
    vix_futures: StockSummaryVixFutures
    # Fear & Greed composite. See ``StockSummaryFearAndGreed``.
    fear_and_greed: StockSummaryFearAndGreed


class StockSummaryResponse(TypedDict, total=False):
    """FlashAlpha's "single best snapshot" from ``GET /v1/stock/{symbol}/summary``.

    One round-trip returns the full picture for a name: price quote,
    full volatility view (ATM IV, HV20, HV60, VRP, 25-delta skew, IV
    term structure), aggregated options flow (OI, volume, put/call
    ratios), the complete dealer exposure (net Greeks, gamma flip,
    walls, max pain, hedging estimate, 0DTE attribution, top strikes by
    GEX), and macro context (VIX, VVIX, SKEW, SPX, MOVE, term
    structure, fear & greed).

    Use this as the default endpoint for "give me everything you have
    on SPY right now" — saves orchestrating /exposure/summary +
    /exposure/levels + /vrp + /skew + /macro into one call.

    Dual-mode authentication
    ------------------------
    - **Authenticated** (with API key): live, current-minute snapshot.
      Pricing reflects the most recent quote tick; all derived numbers
      are computed against that spot.
    - **Unauthenticated**: previous-day cached snapshot, served as a
      free preview tier — the response shape is identical but ``as_of``
      is the prior trading day's close. Useful for demos / docs / LLM
      tool-call examples without burning a key.

    Hedging-estimate sign convention (IMPORTANT)
    --------------------------------------------
    On THIS endpoint, ``exposure.hedging_estimate.spot_*_1pct.dealer_shares``
    is a MAGNITUDE (always non-negative); the ``direction`` field
    (``"buy"``/``"sell"``) carries the sign. This DIFFERS from the
    zero-dte endpoint, where ``dealer_shares_to_trade`` is signed
    (positive = buy, negative = sell). Keep this in mind when porting
    code that consumes both endpoints — a naive copy will double-sign
    or sign-flip the hedging flow.

    Field-level nullability
    -----------------------
    - ``exposure``: ``Optional[StockSummaryExposure]`` — entire block
      is ``None`` on names with no usable options chain.
    - ``macro``: every leaf field can be ``None`` when the upstream
      macro feed is unavailable (the block itself is always present).
    - All numeric leaves throughout are ``Optional`` defensively.
    """

    # Underlying symbol echoed from the request path (e.g. ``"SPY"``).
    symbol: str
    # ET wall-clock timestamp this snapshot was computed for. On the
    # authenticated path this is the most recent quote tick used; on the
    # unauthenticated free preview, it's the prior trading day's close.
    as_of: str
    # ``True`` if NYSE was open at ``as_of``. Always ``False`` on the
    # unauthenticated preview (prior day's close = market closed).
    market_open: Optional[bool]
    # Quote block. See ``StockSummaryPrice``.
    price: StockSummaryPrice
    # Volatility block — ATM IV, HV ladders, VRP, skew, term structure.
    # See ``StockSummaryVolatility``.
    volatility: StockSummaryVolatility
    # Aggregated options flow (OI, volume, put/call ratios). See
    # ``StockSummaryOptionsFlow``.
    options_flow: StockSummaryOptionsFlow
    # Dealer exposure block. ``None`` on names without a usable options
    # chain. See ``StockSummaryExposure``.
    exposure: Optional[StockSummaryExposure]
    # Macro context (VIX, VVIX, SKEW, SPX, MOVE, term structure, F&G).
    # Block always present; individual leaves can be ``None`` when the
    # upstream macro feed is unavailable. See ``StockSummaryMacro``.
    macro: StockSummaryMacro


# ─── ExposureNarrative ───────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/exposure/narrative/{symbol}`` (Growth+).
#
# This is FlashAlpha's "LLM-friendly verbal output" endpoint — the
# response is dominated by plain-English narrative strings designed to be
# surfaced verbatim into customer-facing chat / newsletters / reports.
# Every string under ``narrative.*`` is editorially safe.


class NarrativeOiChange(TypedDict, total=False):
    """One row of the "top OI changes vs prior session" leaderboard.

    Identifies the strikes that experienced the largest open-interest
    deltas, broken out by call/put — useful for spotting where new
    positioning was put on (or rolled out of) overnight.
    """

    # Strike in dollars.
    strike: Optional[float]
    # ``"call"`` or ``"put"``.
    type: Optional[Literal["call", "put"]]
    # Change in OI vs prior session. Signed: positive = position added,
    # negative = position closed.
    oi_change: Optional[int]
    # Volume traded at this strike for the relevant side. Useful for
    # disambiguating a large oi_change driven by genuine flow vs a
    # corporate-action OI roll.
    volume: Optional[int]


class NarrativeData(TypedDict, total=False):
    """Numeric data block backing the narrative strings.

    The narrative endpoint deliberately exposes the underlying numbers
    too — so a coding agent can both surface the prose verbatim AND
    cross-check / re-derive it against the raw values.
    """

    # Net dealer gamma exposure at ``as_of``, dollars per 1% spot move.
    net_gex: Optional[float]
    # Net dealer GEX at the prior session's close — anchor for the
    # ``net_gex_change_pct`` rate-of-change framing in the narrative.
    net_gex_prior: Optional[float]
    # ``(net_gex - net_gex_prior) / |net_gex_prior| * 100``. Used by the
    # ``gex_change`` narrative line.
    net_gex_change_pct: Optional[float]
    # CBOE VIX index level at ``as_of``.
    vix: Optional[float]
    # Strike where net dealer gamma crosses zero.
    gamma_flip: Optional[float]
    # Strike with the highest absolute call GEX (dealer-side resistance).
    call_wall: Optional[float]
    # Strike with the highest absolute put GEX (dealer-side support).
    put_wall: Optional[float]
    # Dealer-positioning regime classification (same enum as
    # ``exposure_summary.regime``).
    regime: Optional[Literal["positive_gamma", "negative_gamma", "unknown"]]
    # 0DTE share of full-chain GEX as a percentage. Backs the
    # ``zero_dte`` narrative line.
    zero_dte_pct: Optional[float]
    # Top OI changes by absolute magnitude — see ``NarrativeOiChange``.
    top_oi_changes: List[NarrativeOiChange]


class Narrative(TypedDict, total=False):
    """Narrative strings + the data block that backs them.

    Every string field in this block is editorially safe to surface
    verbatim in customer-facing UIs (chat, newsletters, dashboards,
    LLM tool-call outputs). They are short, declarative, and avoid
    making explicit trade recommendations.
    """

    # Headline regime sentence. E.g. "Dealers are positioned long gamma
    # — moves dampened, mean reversion likely."
    regime: Optional[str]
    # Day-over-day GEX change framing. E.g. "Net GEX has rolled +28%
    # vs yesterday's close — dealer-stabilising flow has strengthened."
    gex_change: Optional[str]
    # Plain-English description of gamma flip / call wall / put wall.
    key_levels: Optional[str]
    # Aggregated flow narrative (volume, put/call ratios).
    flow: Optional[str]
    # Vanna conditioning — how the dealer book responds to a vol shock.
    vanna: Optional[str]
    # Charm decay narrative — how dealer delta drifts intraday.
    charm: Optional[str]
    # Same-day-expiry attribution narrative.
    zero_dte: Optional[str]
    # Forward-looking outlook synthesis. The single most quoted line in
    # downstream LLM-rendered briefings.
    outlook: Optional[str]
    # Numeric data backing the narrative. See ``NarrativeData``.
    data: NarrativeData


class NarrativeResponse(TypedDict, total=False):
    """FlashAlpha's "LLM-friendly verbal output" endpoint.

    Response from ``GET /v1/exposure/narrative/{symbol}`` (Growth+).
    Returns a block of plain-English narrative strings (regime,
    gex_change, key_levels, flow, vanna, charm, zero_dte, outlook)
    paired with the numeric data block that backs them. Every string
    under ``narrative.*`` is editorially safe to surface verbatim in
    customer-facing UIs / LLM tool-call outputs / automated briefings.

    Tier requirement: Growth+ (returns 403 ``tier_restricted`` below).
    """

    # Underlying symbol echoed from the request path.
    symbol: str
    # Current spot mid (live) or minute-snapped quote (historical).
    underlying_price: Optional[float]
    # ET wall-clock timestamp.
    as_of: str
    # Narrative strings + data block. See ``Narrative``.
    narrative: Narrative


# ─── ExposureLevels ──────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/exposure/levels/{symbol}``.
#
# A pared-down view of the key dealer-flow strikes. Use this when you
# only need the headline levels (gamma flip, max +/- gamma, walls,
# highest OI strike, 0DTE magnet) and don't need the full Greeks or the
# narrative. Cheaper / smaller payload than ``/v1/exposure/summary``.


class ExposureLevels(TypedDict, total=False):
    """The seven canonical dealer-flow levels for a symbol."""

    # Strike where net dealer gamma crosses zero. Spot above = positive-
    # gamma regime; spot below = negative-gamma.
    gamma_flip: Optional[float]
    # Strike carrying the largest positive net GEX (dealers most long
    # gamma here — strongest local mean-reversion magnet).
    max_positive_gamma: Optional[float]
    # Strike carrying the largest negative net GEX (dealers most short
    # gamma here — strongest local trend-amplification point).
    max_negative_gamma: Optional[float]
    # Strike with highest absolute call GEX (dealer-side resistance).
    call_wall: Optional[float]
    # Strike with highest absolute put GEX (dealer-side support).
    put_wall: Optional[float]
    # Strike with the largest total OI (calls + puts).
    highest_oi_strike: Optional[float]
    # Strike on today's 0DTE with the strongest pin magnet (highest
    # |GEX| weighted by OI proximity). ``None`` on names without a
    # same-day expiry today.
    zero_dte_magnet: Optional[float]


class ExposureLevelsResponse(TypedDict, total=False):
    """Dealer-flow levels from ``GET /v1/exposure/levels/{symbol}``.

    Returns just the headline strikes — gamma flip, max ±gamma, call
    wall, put wall, highest OI strike, 0DTE magnet — without the full
    Greek breakdown or narrative. Use this when a UI just needs to draw
    horizontal level lines on a price chart.
    """

    # Underlying symbol echoed from the request path.
    symbol: str
    # Current spot mid (live) or minute-snapped quote (historical).
    underlying_price: Optional[float]
    # ET wall-clock timestamp.
    as_of: str
    # The seven canonical dealer-flow levels. See ``ExposureLevels``.
    levels: ExposureLevels


# ─── PricingGreeks ───────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/pricing/greeks``.
#
# Black-Scholes-Merton option pricing utility — given (spot, strike, dte,
# sigma, type, risk_free_rate, dividend_yield), returns the theoretical
# price plus first/second/third-order Greeks and a couple of additional
# higher-order sensitivities. Useful for SDK consumers who want a
# stateless analytical-pricing endpoint without taking a hard dep on a
# local quant library.
#
# Python keyword conflict: the response carries a ``"lambda"`` key, but
# ``lambda`` is a reserved keyword in Python — we use the alternative
# ``TypedDict("PricingAdditional", {"lambda": ..., "veta": ...})`` form
# so the JSON name is preserved exactly. Read it as
# ``response["additional"]["lambda"]``.


class PricingInputs(TypedDict, total=False):
    """Echo of the request inputs the pricing was computed against."""

    # Underlying spot in dollars.
    spot: Optional[float]
    # Strike in dollars.
    strike: Optional[float]
    # Days to expiry (calendar days).
    dte: Optional[float]
    # Implied volatility (annualised, percentage points — e.g. 18.5
    # means 18.5%).
    sigma: Optional[float]
    # ``"call"`` or ``"put"``.
    type: Optional[Literal["call", "put"]]
    # Continuously-compounded risk-free rate (decimal, e.g. 0.045 for
    # 4.5%).
    risk_free_rate: Optional[float]
    # Continuously-compounded dividend yield (decimal).
    dividend_yield: Optional[float]


class PricingFirstOrder(TypedDict, total=False):
    """First-order Greeks — delta, gamma, theta, vega, rho.

    Note ``gamma`` is technically second-order in spot but lives here
    by long-standing market convention (it's reported alongside delta
    in every BSM dashboard).
    """

    # ``∂Price / ∂Spot``.
    delta: Optional[float]
    # ``∂²Price / ∂Spot²``.
    gamma: Optional[float]
    # ``∂Price / ∂t`` — per calendar day.
    theta: Optional[float]
    # ``∂Price / ∂σ`` — per 1-vol-point change in IV.
    vega: Optional[float]
    # ``∂Price / ∂r`` — per 1bp change in risk-free rate.
    rho: Optional[float]


class PricingSecondOrder(TypedDict, total=False):
    """Second-order Greeks — vanna, charm, vomma, dual_delta."""

    # ``∂²Price / ∂Spot∂σ`` — how delta changes with IV.
    vanna: Optional[float]
    # ``∂²Price / ∂Spot∂t`` — how delta drifts with time.
    charm: Optional[float]
    # ``∂²Price / ∂σ²`` — how vega changes with IV (vol-of-vol).
    vomma: Optional[float]
    # ``∂Price / ∂Strike`` — sensitivity to strike (used in
    # risk-neutral density extraction).
    dual_delta: Optional[float]


class PricingThirdOrder(TypedDict, total=False):
    """Third-order Greeks — speed, zomma, color, ultima."""

    # ``∂³Price / ∂Spot³`` — gamma-of-spot.
    speed: Optional[float]
    # ``∂³Price / ∂Spot²∂σ`` — gamma-of-vol.
    zomma: Optional[float]
    # ``∂³Price / ∂Spot²∂t`` — gamma decay through time.
    color: Optional[float]
    # ``∂³Price / ∂σ³`` — third derivative wrt IV.
    ultima: Optional[float]


# Python keyword conflict: ``lambda`` is reserved, so we declare this
# TypedDict via the functional-form constructor that lets us use string
# keys. Access at runtime as ``response["additional"]["lambda"]``.
PricingAdditional = TypedDict(
    "PricingAdditional",
    {
        # Lambda (Ω, "leverage") — elasticity of option value to spot:
        # ``delta × spot / price``. JSON key is ``"lambda"`` (Python
        # keyword), so this TypedDict uses the functional form to keep
        # the JSON name verbatim.
        "lambda": Optional[float],
        # Veta (DvegaDtime) — ``∂Vega / ∂t``. How vega decays with time.
        "veta": Optional[float],
    },
    total=False,
)


class PricingGreeksResponse(TypedDict, total=False):
    """Black-Scholes-Merton pricing utility from ``GET /v1/pricing/greeks``.

    Stateless analytical pricer — pass (spot, strike, dte, sigma, type,
    risk_free_rate, dividend_yield) as query parameters, receive
    theoretical price + first/second/third-order Greeks + a couple of
    additional higher-order sensitivities (``lambda``, ``veta``).

    Note the JSON ``additional.lambda`` key conflicts with Python's
    ``lambda`` reserved word. The ``PricingAdditional`` TypedDict uses
    the functional constructor form to preserve the JSON name verbatim
    — read it as ``response["additional"]["lambda"]``.
    """

    # Echo of the request inputs.
    inputs: PricingInputs
    # Theoretical option price in dollars.
    theoretical_price: Optional[float]
    # First-order Greeks. See ``PricingFirstOrder``.
    first_order: PricingFirstOrder
    # Second-order Greeks. See ``PricingSecondOrder``.
    second_order: PricingSecondOrder
    # Third-order Greeks. See ``PricingThirdOrder``.
    third_order: PricingThirdOrder
    # Additional higher-order Greeks (``lambda``, ``veta``). See
    # ``PricingAdditional``.
    additional: PricingAdditional


# ─── Volatility ──────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/volatility/{symbol}`` (Growth+).
#
# Single-call vol dashboard. Bundles the realized-vol ladder, ATM IV, the
# IV-RV spread (VRP) at multiple horizons, the per-expiry skew profiles,
# the term-structure slope, IV dispersion across the surface, GEX/theta
# bucketed by DTE, the put/call profile (per-expiry + by-moneyness), OI
# concentration, the multi-move dealer hedging table, and chain liquidity.
#
# Same shape on the live API and on the historical API with ``?at=``.


class VolatilityRealizedVol(TypedDict, total=False):
    """Realized-volatility ladder — annualised %, computed from spot
    log-returns over the trailing 5/10/20/30/60 trading days.

    Use against ``atm_iv`` to read the variance risk premium at multiple
    horizons (see ``iv_rv_spreads``). All fields are ``Optional`` because
    very thin or new-listed symbols may not have enough data to compute the
    longer-window numbers.
    """

    rv_5d: Optional[float]
    rv_10d: Optional[float]
    rv_20d: Optional[float]
    rv_30d: Optional[float]
    rv_60d: Optional[float]


class VolatilityIvRvSpreads(TypedDict, total=False):
    """IV-RV spreads (variance risk premia) at the standard horizons.

    Each ``vrp_Nd`` field is ``atm_iv - rv_Nd``. Positive = options price
    more vol than realised → premium for selling vol. Negative = options
    cheap vs realised → premium for buying vol. ``assessment`` is a
    short categorical label (e.g. ``"rich"``, ``"fair"``, ``"cheap"``)
    summarising the overall posture across horizons.
    """

    vrp_5d: Optional[float]
    vrp_10d: Optional[float]
    vrp_20d: Optional[float]
    vrp_30d: Optional[float]
    # Plain-text classification of the prevailing VRP regime — safe to
    # surface verbatim. Values are not enumerated by the API; treat as a
    # free-form string.
    assessment: Optional[str]


class VolatilitySkewProfile(TypedDict, total=False):
    """One per-expiry row of the skew profile.

    Reports IV at five canonical points across the smile (10-delta put,
    25-delta put, ATM, 25-delta call, 10-delta call) along with two
    derived measures (``skew_25d``, ``smile_ratio``) and the wing-tail
    convexity descriptor.
    """

    # ``"yyyy-MM-dd"`` of the expiry this row was measured at.
    expiry: Optional[str]
    # Calendar days from ``as_of`` to ``expiry``.
    days_to_expiry: Optional[int]
    # IV at the 10-delta put (deep crash-insurance wing, annualised %).
    put_10d_iv: Optional[float]
    # IV at the 25-delta put (annualised %).
    put_25d_iv: Optional[float]
    # ATM IV at this expiry (annualised %).
    atm_iv: Optional[float]
    # IV at the 25-delta call (annualised %).
    call_25d_iv: Optional[float]
    # IV at the 10-delta call (deep upside-tail wing, annualised %).
    call_10d_iv: Optional[float]
    # ``put_25d_iv - call_25d_iv``. Positive = puts richer than calls
    # (downside-skewed smile, the typical equity-index regime).
    skew_25d: Optional[float]
    # ``(put_25d_iv + call_25d_iv) / (2 * atm_iv)`` — wing-vs-ATM
    # curvature premium. ``> 1`` means kurtotic smile.
    smile_ratio: Optional[float]
    # Tail convexity descriptor — captures the additional curvature of
    # the 10-delta wings beyond the 25-delta points.
    tail_convexity: Optional[float]


class VolatilityTermStructure(TypedDict, total=False):
    """IV term structure shape — near-end slope, far-end slope, regime label."""

    # Slope of the near-end of the IV term structure as a percentage
    # (e.g. ``2.5`` = +2.5% steepness from front to mid). Positive =
    # contango on the front; negative = front-month inversion.
    near_slope_pct: Optional[float]
    # Slope of the far-end of the term structure (mid- to long-dated).
    far_slope_pct: Optional[float]
    # Categorical label summarising the overall term-structure shape —
    # values like ``"contango"``, ``"backwardation"``, ``"flat"``, etc.
    # Treat as free-form; not enumerated.
    state: Optional[str]


class VolatilityIvDispersion(TypedDict, total=False):
    """IV dispersion across the surface.

    ``cross_expiry`` measures how much ATM IV varies across expirations;
    ``cross_strike`` measures how much IV varies across moneyness at a
    fixed expiry. Together they summarise how "lumpy" the surface is
    relative to a smooth reference.
    """

    cross_expiry: Optional[float]
    cross_strike: Optional[float]


class VolatilityGexByDte(TypedDict, total=False):
    """One row of the GEX-by-DTE-bucket breakdown.

    Bucketing the chain by days-to-expiry exposes which tenors are
    driving the dealer-gamma book — e.g. 0-7d dominance signals a 0DTE-
    weighted regime, while >90d weight signals leaps-driven positioning.
    """

    # Bucket label (e.g. ``"0-7d"``, ``"8-30d"``, ``"31-90d"``,
    # ``">90d"``). Treat as free-form string; the API may add buckets.
    bucket: Optional[str]
    # Net GEX contribution from this bucket, dollars per 1% spot move.
    net_gex: Optional[float]
    # This bucket's share of total chain GEX as a percentage.
    pct_of_total: Optional[float]
    # Number of distinct contracts contributing to this bucket.
    contract_count: Optional[int]


class VolatilityThetaByDte(TypedDict, total=False):
    """One row of the theta-by-DTE-bucket breakdown."""

    bucket: Optional[str]
    # Net theta contribution from this bucket (dollars/day, signed).
    net_theta: Optional[float]
    contract_count: Optional[int]


class VolatilityPcByExpiry(TypedDict, total=False):
    """One row of the per-expiry put/call OI + volume breakdown."""

    expiry: Optional[str]
    call_oi: Optional[int]
    put_oi: Optional[int]
    # ``put_oi / call_oi``. ``> 1`` = put-heavy at this expiry.
    pc_ratio_oi: Optional[float]
    call_volume: Optional[int]
    put_volume: Optional[int]
    # ``put_volume / call_volume``. Intraday flow tilt; noisier than OI.
    pc_ratio_volume: Optional[float]


class VolatilityPcByMoneyness(TypedDict, total=False):
    """Put/call OI grouped into OTM / ATM / ITM buckets.

    ``otm`` / ``atm`` / ``itm`` here use the canonical FlashAlpha
    moneyness bands (driven by spot, not delta). Useful for spotting
    a name where OI is concentrated in OTM puts (defensive crash
    insurance) vs ITM calls (synthetic stock positioning).
    """

    otm_call_oi: Optional[int]
    atm_call_oi: Optional[int]
    itm_call_oi: Optional[int]
    otm_put_oi: Optional[int]
    atm_put_oi: Optional[int]
    itm_put_oi: Optional[int]


class VolatilityPutCallProfile(TypedDict, total=False):
    """Put/call profile — per-expiry rows + an OTM/ATM/ITM moneyness cube."""

    by_expiry: List[VolatilityPcByExpiry]
    by_moneyness: VolatilityPcByMoneyness


class VolatilityOiConcentration(TypedDict, total=False):
    """OI concentration metrics — top-N strike share + Herfindahl index.

    High concentration (e.g. ``top_3_pct > 50``) signals a chain where
    a small handful of strikes dominate — typical of pinning setups or
    LEAP-heavy positioning. Low concentration = diffuse positioning.
    """

    # Combined OI share of the three highest-OI strikes, as a percentage.
    top_3_pct: Optional[float]
    top_5_pct: Optional[float]
    top_10_pct: Optional[float]
    # Herfindahl-Hirschman index over per-strike OI shares. Range 0-1
    # (often expressed 0-10000 in classical HHI; here normalised 0-1).
    # Higher = more concentrated.
    herfindahl: Optional[float]


class VolatilityHedgingScenario(TypedDict, total=False):
    """One row of the multi-move dealer-hedging-flow table.

    Unlike ``exposure_summary`` (which only exposes ±1%), this endpoint
    returns the hedging flow at multiple ``move_pct`` levels in a single
    list — useful for plotting the full convexity curve.
    """

    # Spot-move percentage this row was computed at (signed; positive =
    # spot up, negative = spot down).
    move_pct: Optional[float]
    # Estimated dealer shares to trade. Sign aligned with ``direction``.
    dealer_shares: Optional[float]
    # ``"buy"`` or ``"sell"`` — convenience label matching the sign of
    # ``dealer_shares``.
    direction: Optional[Literal["buy", "sell"]]
    # ``|dealer_shares| × current_spot``. Cross-symbol comparison.
    notional_usd: Optional[float]


class VolatilityLiquidity(TypedDict, total=False):
    """Chain-liquidity summary — ATM vs wing average spreads + counts."""

    # Average bid-ask spread of ATM contracts as a percentage of mid.
    atm_avg_spread_pct: Optional[float]
    # Average bid-ask spread of wing (deep OTM/ITM) contracts.
    wing_avg_spread_pct: Optional[float]
    # Count of contracts in the ATM band.
    atm_contracts: Optional[int]
    # Count of contracts in the wing band.
    wing_contracts: Optional[int]


class VolatilityResponse(TypedDict, total=False):
    """Comprehensive volatility dashboard from ``GET /v1/volatility/{symbol}``.

    Single-call payload bundling the realized-vol ladder, ATM IV, IV-RV
    spreads at multiple horizons, per-expiry skew profiles, term-structure
    slope, IV dispersion, GEX/theta by DTE bucket, the put/call profile,
    OI concentration, multi-move dealer hedging table, and chain liquidity.

    Same shape on the live API and on the historical API with ``?at=``
    (snapped to the requested minute).

    Tier requirement: Growth+ (returns 403 ``tier_restricted`` below).
    """

    # Underlying symbol echoed from the request path.
    symbol: str
    # Spot mid (live) or minute-snapped quote (historical), in dollars.
    underlying_price: Optional[float]
    # ET wall-clock timestamp this snapshot was computed for.
    as_of: str
    # ``True`` if NYSE was open at ``as_of``.
    market_open: Optional[bool]
    # Realized-volatility ladder. See ``VolatilityRealizedVol``.
    realized_vol: VolatilityRealizedVol
    # Front-month ATM IV (annualised %, e.g. 18.5 = 18.5%).
    atm_iv: Optional[float]
    # IV-RV spreads at multiple horizons + classification. See
    # ``VolatilityIvRvSpreads``.
    iv_rv_spreads: VolatilityIvRvSpreads
    # Per-expiry skew profiles. See ``VolatilitySkewProfile``.
    skew_profiles: List[VolatilitySkewProfile]
    # IV term-structure shape. See ``VolatilityTermStructure``.
    term_structure: VolatilityTermStructure
    # IV dispersion across the surface. See ``VolatilityIvDispersion``.
    iv_dispersion: VolatilityIvDispersion
    # GEX bucketed by DTE. See ``VolatilityGexByDte``.
    gex_by_dte: List[VolatilityGexByDte]
    # Theta bucketed by DTE. See ``VolatilityThetaByDte``.
    theta_by_dte: List[VolatilityThetaByDte]
    # Put/call profile (per-expiry + by-moneyness). See
    # ``VolatilityPutCallProfile``.
    put_call_profile: VolatilityPutCallProfile
    # OI concentration metrics. See ``VolatilityOiConcentration``.
    oi_concentration: VolatilityOiConcentration
    # Multi-move dealer hedging table. See ``VolatilityHedgingScenario``.
    hedging_scenarios: List[VolatilityHedgingScenario]
    # Chain-liquidity summary. See ``VolatilityLiquidity``.
    liquidity: VolatilityLiquidity


# ─── AdvVolatility ───────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/adv_volatility/{symbol}`` (Alpha+).
#
# Quant-level vol surface analytics: SVI parameters per expiry, forward
# prices, the full total-variance surface (moneyness × expiries grid),
# arbitrage flags, variance-swap fair values, and the higher-order Greek
# surfaces (vanna, charm, volga, speed). Same shape on live and historical.


class AdvVolSviParam(TypedDict, total=False):
    """One per-expiry row of fitted SVI (Stochastic Volatility Inspired)
    parameters.

    The SVI parameterisation models total variance as
    ``a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))`` where ``k``
    is log-moneyness. The five free parameters (``a``, ``b``, ``rho``,
    ``m``, ``sigma``) fit each expiry independently. ``atm_total_variance``
    and ``atm_iv`` are derived for convenience.
    """

    expiry: Optional[str]
    days_to_expiry: Optional[int]
    # Forward price used as the SVI reference (i.e. ``log(K/F)`` is the
    # moneyness coordinate on this row's curve).
    forward: Optional[float]
    # Vertical-shift parameter (overall variance level).
    a: Optional[float]
    # Slope parameter (controls the angle of the wings).
    b: Optional[float]
    # Correlation parameter (skew direction; -1..+1).
    rho: Optional[float]
    # Horizontal-shift parameter (moneyness location of the curve's
    # minimum).
    m: Optional[float]
    # ATM curvature parameter (controls smile sharpness).
    sigma: Optional[float]
    # Total variance at ATM (``T × atm_iv²``). Useful for comparing
    # tenors directly.
    atm_total_variance: Optional[float]
    # ATM IV implied by the fit (annualised %).
    atm_iv: Optional[float]


class AdvVolForwardPrice(TypedDict, total=False):
    """One per-expiry row of the forward-price + basis breakdown."""

    expiry: Optional[str]
    days_to_expiry: Optional[int]
    # Forward price for this expiry, in dollars.
    forward: Optional[float]
    # Underlying spot used as the basis reference.
    spot: Optional[float]
    # ``(forward - spot) / spot * 100``. Positive = forward priced above
    # spot (typical contango / cost-of-carry); negative = backwardation
    # (often dividend-rich names approaching ex-dividend).
    basis_pct: Optional[float]


class AdvVolTotalVarianceSurface(TypedDict, total=False):
    """The full total-variance / IV surface as parallel grids.

    ``total_variance`` and ``implied_vol`` are 2D lists indexed
    ``[i][j]`` where ``i`` is the moneyness index and ``j`` is the
    expiry index. Use ``moneyness[i]`` and ``expiries[j]`` /
    ``tenors[j]`` to recover the axes.
    """

    # Log-moneyness grid axis (one entry per row of the surface grids).
    moneyness: List[float]
    # Expiry-date axis (``"yyyy-MM-dd"``, one entry per column).
    expiries: List[str]
    # Calendar-day-to-expiry axis aligned with ``expiries``.
    tenors: List[float]
    # Total variance grid: ``T × σ²`` at each (moneyness, expiry) point.
    total_variance: List[List[float]]
    # Implied vol grid in annualised %.
    implied_vol: List[List[float]]


class AdvVolArbitrageFlag(TypedDict, total=False):
    """One arbitrage-violation flag detected on the fitted surface.

    Detects calendar/butterfly arbitrage in the fitted SVI surface —
    points where total variance is non-monotone in time (calendar
    arb) or where the call price is non-convex in strike (butterfly arb).
    Production traders should treat any non-empty flag list with caution.
    """

    expiry: Optional[str]
    # Arbitrage type — common values include ``"calendar"`` and
    # ``"butterfly"``. Treat as free-form; the API may add types.
    type: Optional[str]
    # Strike or log-moneyness coordinate where the violation was detected.
    strike_or_k: Optional[float]
    # Plain-English description of the violation. Safe to surface
    # verbatim in diagnostic UIs.
    description: Optional[str]


class AdvVolVarianceSwap(TypedDict, total=False):
    """One per-expiry row of variance-swap fair values."""

    expiry: Optional[str]
    days_to_expiry: Optional[int]
    # Fair variance for a synthetic variance swap on this name at this
    # tenor (annualised variance, decimal — e.g. 0.04 = 20% vol²).
    fair_variance: Optional[float]
    # ``sqrt(fair_variance) * 100`` — the variance-swap fair vol
    # expressed as an annualised percentage.
    fair_vol: Optional[float]
    # ATM IV at this expiry, for comparison against ``fair_vol``. The
    # spread ``fair_vol - atm_iv`` is the convexity premium.
    atm_iv: Optional[float]
    # ``fair_vol - atm_iv`` — captures the curvature premium (variance-
    # swap fair vol is always ≥ ATM IV in arbitrage-free markets).
    convexity_adjustment: Optional[float]


class AdvVolGreekSurface(TypedDict, total=False):
    """A single higher-order Greek surface as a parallel grid.

    ``values`` is a 2D list indexed ``[i][j]`` where ``i`` is the strike
    index and ``j`` is the expiry index. Use ``strikes[i]`` and
    ``expiries[j]`` to recover the axes.
    """

    # Strike grid axis (one entry per row).
    strikes: List[float]
    # Expiry-date axis (``"yyyy-MM-dd"``, one per column).
    expiries: List[str]
    # The Greek-value grid.
    values: List[List[float]]


class AdvVolGreeksSurfaces(TypedDict, total=False):
    """The four canonical higher-order Greek surfaces.

    All four use the same axes (strikes × expiries) but different value
    semantics. Vanna and charm are second-order; volga is the second
    derivative wrt vol; speed is the third derivative wrt spot.
    """

    # ``∂²Price / ∂Spot∂σ`` surface — how delta changes with IV.
    vanna: AdvVolGreekSurface
    # ``∂²Price / ∂Spot∂t`` surface — how delta drifts with time.
    charm: AdvVolGreekSurface
    # ``∂²Price / ∂σ²`` surface — how vega changes with IV (vol-of-vol).
    volga: AdvVolGreekSurface
    # ``∂³Price / ∂Spot³`` surface — gamma-of-spot, the cubic spot
    # derivative.
    speed: AdvVolGreekSurface


class AdvVolatilityResponse(TypedDict, total=False):
    """Advanced volatility dashboard from ``GET /v1/adv_volatility/{symbol}``.

    Quant-level surface analytics: per-expiry SVI parameters, forward
    prices, the full total-variance surface (moneyness × expiries grid),
    arbitrage-flag diagnostics, variance-swap fair values, and the four
    higher-order Greek surfaces (vanna, charm, volga, speed).

    Same shape on the live API and on the historical API with ``?at=``.

    Tier requirement: Alpha+ (returns 403 ``tier_restricted`` below).
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    market_open: Optional[bool]
    # Per-expiry fitted SVI parameters. See ``AdvVolSviParam``.
    svi_parameters: List[AdvVolSviParam]
    # Forward prices + basis. See ``AdvVolForwardPrice``.
    forward_prices: List[AdvVolForwardPrice]
    # The full total-variance / IV surface. See
    # ``AdvVolTotalVarianceSurface``.
    total_variance_surface: AdvVolTotalVarianceSurface
    # Arbitrage-violation flags. Empty list = clean surface. See
    # ``AdvVolArbitrageFlag``.
    arbitrage_flags: List[AdvVolArbitrageFlag]
    # Variance-swap fair values. See ``AdvVolVarianceSwap``.
    variance_swap_fair_values: List[AdvVolVarianceSwap]
    # Four higher-order Greek surfaces. See ``AdvVolGreeksSurfaces``.
    greeks_surfaces: AdvVolGreeksSurfaces


# ─── Surface ─────────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/surface/{symbol}`` (public).
#
# Compact rectangular IV grid for plotting / interpolating against. Public
# (no auth required on live; historical requires ``at=`` and an API key).


class SurfaceResponse(TypedDict, total=False):
    """Implied-vol surface grid from ``GET /v1/surface/{symbol}``.

    Returns a rectangular ``tenors × moneyness`` grid of implied vols
    (annualised %) along with the axes and the list of expiry slices
    that fed the fit. Useful for direct plotting or interpolation.

    On the historical API, this endpoint requires ``?at=`` and may raise
    ``InsufficientDataError`` when the chain has too few liquid OTM
    contracts to fill the grid at that minute.
    """

    # Underlying symbol echoed from the request path.
    symbol: str
    # Spot mid at ``as_of``.
    spot: Optional[float]
    # ET wall-clock timestamp.
    as_of: str
    # Grid dimension (the surface is ``grid_size × grid_size``).
    grid_size: Optional[int]
    # Tenor axis in years (one entry per row of ``iv``).
    tenors: List[float]
    # Log-moneyness axis (one entry per column of ``iv``).
    moneyness: List[float]
    # The IV grid, annualised %. Indexed ``iv[i][j]`` with
    # ``i`` = tenor index, ``j`` = moneyness index.
    iv: List[List[float]]
    # Count of expiry slices that contributed to the surface fit.
    slices_used: int


# ─── Exposure (GEX/DEX/VEX/CHEX) ─────────────────────────────────────────────
#
# Typed models for the per-strike exposure endpoints:
#   - ``GET /v1/exposure/gex/{symbol}``
#   - ``GET /v1/exposure/dex/{symbol}``
#   - ``GET /v1/exposure/vex/{symbol}``
#   - ``GET /v1/exposure/chex/{symbol}``
#
# Each one returns a thin response wrapper plus a per-strike row list. The
# row schemas differ per Greek but share the same headline shape (strike +
# call/put/net values). Same wire shape on live + historical.


class GexStrikeRow(TypedDict, total=False):
    """One per-strike row of the GEX breakdown.

    Contains the call/put/net GEX values plus the supporting OI and
    volume context for that strike. ``call_oi_change`` /
    ``put_oi_change`` are the day-over-day OI deltas; on the historical
    API these are always ``None`` (no prior-day OI join yet).
    """

    strike: Optional[float]
    # Call-side GEX contribution at this strike (dollars per 1% spot).
    call_gex: Optional[float]
    # Put-side GEX contribution at this strike.
    put_gex: Optional[float]
    # ``call_gex - put_gex`` (sign convention: positive = dealers long
    # gamma at this strike).
    net_gex: Optional[float]
    call_oi: Optional[int]
    put_oi: Optional[int]
    call_volume: Optional[int]
    put_volume: Optional[int]
    # Day-over-day OI delta for the call side. ``None`` on historical.
    call_oi_change: Optional[int]
    put_oi_change: Optional[int]


class GexResponse(TypedDict, total=False):
    """Per-strike GEX breakdown from ``GET /v1/exposure/gex/{symbol}``.

    Headline numbers (``net_gex``, ``gamma_flip``, ``net_gex_label``)
    plus a per-strike row list. Filterable by ``expiration`` and
    ``min_oi`` query parameters; same shape on live + historical.
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    # Strike where net dealer gamma crosses zero across the chain.
    gamma_flip: Optional[float]
    # Net GEX across the chain (dollars per 1% spot move).
    net_gex: Optional[float]
    # Plain-text categorical label for the GEX regime
    # (e.g. ``"long_gamma"``, ``"short_gamma"``, ``"flat"``).
    net_gex_label: Optional[str]
    # Per-strike rows. See ``GexStrikeRow``.
    strikes: List[GexStrikeRow]


class DexStrikeRow(TypedDict, total=False):
    """One per-strike row of the DEX breakdown."""

    strike: Optional[float]
    # Call-side DEX (dollars).
    call_dex: Optional[float]
    # Put-side DEX (dollars).
    put_dex: Optional[float]
    # ``call_dex + put_dex`` (signed; sign indicates dealer hedge
    # direction at this strike).
    net_dex: Optional[float]


class DexResponse(TypedDict, total=False):
    """Per-strike DEX breakdown from ``GET /v1/exposure/dex/{symbol}``."""

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    # Net DEX across the chain (dollars).
    net_dex: Optional[float]
    strikes: List[DexStrikeRow]


class VexStrikeRow(TypedDict, total=False):
    """One per-strike row of the VEX (vanna exposure) breakdown."""

    strike: Optional[float]
    call_vex: Optional[float]
    put_vex: Optional[float]
    net_vex: Optional[float]


class VexResponse(TypedDict, total=False):
    """Per-strike VEX breakdown from ``GET /v1/exposure/vex/{symbol}``.

    Vanna exposure measures the dealer-book sensitivity to a 1-vol-point
    move in IV. ``vex_interpretation`` is a plain-English narrative line
    summarising the prevailing vanna posture — safe to surface verbatim.
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    # Net VEX across the chain (dollars per 1-vol-point).
    net_vex: Optional[float]
    # Plain-English narrative for the vanna regime. Safe to surface
    # verbatim in customer-facing UIs.
    vex_interpretation: Optional[str]
    strikes: List[VexStrikeRow]


class ChexStrikeRow(TypedDict, total=False):
    """One per-strike row of the CHEX (charm exposure) breakdown."""

    strike: Optional[float]
    call_chex: Optional[float]
    put_chex: Optional[float]
    net_chex: Optional[float]


class ChexResponse(TypedDict, total=False):
    """Per-strike CHEX breakdown from ``GET /v1/exposure/chex/{symbol}``.

    Charm (``∂Delta/∂t``) exposure — captures the time-decay drift in
    the dealer hedge book. ``chex_interpretation`` is a plain-English
    line summarising the prevailing posture (e.g. into-close pressure
    direction); safe to surface verbatim.
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    # Net CHEX across the chain (dollars per day).
    net_chex: Optional[float]
    # Plain-English narrative for the charm regime.
    chex_interpretation: Optional[str]
    strikes: List[ChexStrikeRow]


# ─── OptionQuote / StockQuote (live only) ────────────────────────────────────
#
# Typed models for the live-only market-data endpoints:
#   - ``GET /optionquote/{ticker}`` (Growth+)
#   - ``GET /stockquote/{ticker}`` (Free+)
#
# These do not exist on the historical API in the same form (historical
# uses ``/v1/optionquote`` and ``/v1/stockquote`` with ``?at=``). The wire
# shape carries several camelCase field names — preserved here verbatim so
# the typed dict matches the actual JSON keys (NOT pythonised).


class OptionQuoteResponse(TypedDict, total=False):
    """Single-contract option quote from ``GET /optionquote/{ticker}`` (live).

    Growth+ endpoint. Returns the bid/ask/mid for one option contract
    along with the full first/second-order Greek block, the IV (with
    bid/ask IV bracket), the SVI-vol estimate (gated by tier — see
    ``svi_vol_gated``), and OI / volume.

    Camel-cased keys on the wire — ``bidSize``, ``askSize``,
    ``lastUpdate`` are NOT pythonised. Read them as
    ``response["lastUpdate"]`` etc.
    """

    # ``"call"`` or ``"put"``.
    type: Optional[Literal["call", "put"]]
    # ``"yyyy-MM-dd"`` of the expiry.
    expiry: Optional[str]
    # Strike in dollars.
    strike: Optional[float]
    # National best bid / best offer / mid (dollars).
    bid: Optional[float]
    ask: Optional[float]
    mid: Optional[float]
    # Camel-cased on the wire — preserved verbatim.
    bidSize: Optional[int]
    askSize: Optional[int]
    # ET wall-clock timestamp of the underlying ``last`` print backing
    # this quote. Camel-cased on the wire.
    lastUpdate: Optional[str]
    # Mid-IV (annualised %, e.g. 18.5 = 18.5%).
    implied_vol: Optional[float]
    # IV at the bid and ask (brackets ``implied_vol``).
    iv_bid: Optional[float]
    iv_ask: Optional[float]
    # First-order Greeks.
    delta: Optional[float]
    gamma: Optional[float]
    theta: Optional[float]
    vega: Optional[float]
    rho: Optional[float]
    # Second-order Greeks.
    vanna: Optional[float]
    charm: Optional[float]
    # SVI-fitted vol estimate. ``None`` when ``svi_vol_gated`` is not
    # ``"open"`` (e.g. ``"backtest_mode"`` on historical-replay calls,
    # ``"tier_restricted"`` on lower tiers, ``"unfit"`` when the surface
    # could not be fit at this expiry). Treat the gating string as
    # free-form — values may be added.
    svi_vol: Optional[float]
    # Free-form gating reason for ``svi_vol`` (e.g. ``"open"``,
    # ``"tier_restricted"``, ``"unfit"``, ``"backtest_mode"``).
    svi_vol_gated: Optional[str]
    open_interest: Optional[int]
    volume: Optional[int]
    # Underlying symbol — present on some response variants (e.g. when
    # the request omits one of the strike/expiry/type filters), absent
    # on the strict single-contract response.
    underlying: Optional[str]


class StockQuoteResponse(TypedDict, total=False):
    """Stock quote from ``GET /stockquote/{ticker}`` (live).

    Free+ endpoint. Returns a thin bid/ask/mid + last quote for the
    underlying. Camel-cased keys on the wire — ``lastPrice``,
    ``lastUpdate`` are NOT pythonised.
    """

    ticker: Optional[str]
    bid: Optional[float]
    ask: Optional[float]
    # ``(bid + ask) / 2``.
    mid: Optional[float]
    # Last printed trade in dollars. Camel-cased on the wire.
    lastPrice: Optional[float]
    # ET wall-clock timestamp of the ``lastPrice`` print. Camel-cased.
    lastUpdate: Optional[str]


# ─── Pricing IV ──────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/pricing/iv`` (Free+, live-only).
#
# Inverts the BSM pricer to recover implied volatility from a market price.
# Echoes the requested inputs alongside the solved IV.


class PricingIvInputs(TypedDict, total=False):
    """Inputs echoed from the implied-vol request.

    Useful for downstream callers that need to keep the original request
    parameters paired with the response without reconstructing them.
    """

    spot: Optional[float]
    strike: Optional[float]
    # Days to expiry (calendar days, fractional allowed).
    dte: Optional[float]
    # Market price the IV was solved against.
    price: Optional[float]
    # ``"call"`` or ``"put"``.
    type: Optional[Literal["call", "put"]]
    # Risk-free rate (decimal, e.g. 0.0425 for 4.25%).
    risk_free_rate: Optional[float]
    # Continuous dividend yield (decimal).
    dividend_yield: Optional[float]


class PricingIvResponse(TypedDict, total=False):
    """Implied-volatility response from ``GET /v1/pricing/iv``.

    Returns the IV that recovers the supplied market ``price`` under BSM,
    as a decimal (``implied_volatility``) and as a percentage
    (``implied_volatility_pct``). Free+ on live; not available on historical.
    """

    inputs: PricingIvInputs
    # Solved implied volatility as a decimal (e.g. 0.185 = 18.5%).
    implied_volatility: Optional[float]
    # Same number expressed as a percentage (e.g. 18.5).
    implied_volatility_pct: Optional[float]


# ─── Pricing Kelly ───────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/pricing/kelly`` (Growth+, live-only).
#
# Computes the Kelly-optimal sizing fraction for a single option position
# along with the supporting probability/return analysis. Returns three
# nested blocks (inputs, sizing, analysis) and a free-form recommendation.


class PricingKellyInputs(TypedDict, total=False):
    """Inputs echoed from the Kelly sizing request."""

    spot: Optional[float]
    strike: Optional[float]
    # Days to expiry (calendar days, fractional allowed).
    dte: Optional[float]
    # Volatility used for the BSM pricing (decimal, e.g. 0.18).
    sigma: Optional[float]
    # Premium paid per contract (dollars).
    premium: Optional[float]
    # Drift / expected return assumption used for the probability calc.
    mu: Optional[float]
    type: Optional[Literal["call", "put"]]
    risk_free_rate: Optional[float]
    dividend_yield: Optional[float]


class PricingKellySizing(TypedDict, total=False):
    """Kelly-optimal sizing fractions.

    ``kelly_fraction`` is the canonical Kelly fraction (``edge / variance``)
    expressed as a fraction of bankroll. ``half_kelly`` and ``quarter_kelly``
    are the standard de-risked variants (more popular in practice — full
    Kelly's drawdown profile is rough). The ``_pct`` variants are the same
    numbers in percentage points.
    """

    kelly_fraction: Optional[float]
    half_kelly: Optional[float]
    quarter_kelly: Optional[float]
    kelly_pct: Optional[float]
    half_kelly_pct: Optional[float]


class PricingKellyAnalysis(TypedDict, total=False):
    """Underlying probability / return analysis behind the Kelly sizing.

    All ``probability_*`` fields are decimals in ``[0, 1]``; the ``_pct``
    variants are the same numbers in percentage points.
    """

    # Expected ROI per contract (decimal, e.g. 0.45 = +45%).
    expected_roi: Optional[float]
    expected_roi_pct: Optional[float]
    # Expected dollar payoff per contract under the drift assumption.
    expected_payoff: Optional[float]
    # P(payoff > premium) — probability of finishing in profit.
    probability_of_profit: Optional[float]
    probability_of_profit_pct: Optional[float]
    # P(spot > strike at expiry) for calls, < strike for puts.
    probability_itm: Optional[float]
    probability_itm_pct: Optional[float]
    # Maximum loss per contract (= premium for long options).
    max_loss: Optional[float]
    # Underlying price at which P/L = 0 at expiry.
    breakeven: Optional[float]
    # Expected log-growth rate of the bankroll under the Kelly fraction.
    expected_growth_rate: Optional[float]


class PricingKellyResponse(TypedDict, total=False):
    """Full response from ``GET /v1/pricing/kelly`` (Growth+, live-only).

    Bundles the echoed inputs, the Kelly sizing block, the supporting
    probability/return analysis, and a free-form ``recommendation`` string
    summarising the result for end-user display.
    """

    inputs: PricingKellyInputs
    sizing: PricingKellySizing
    analysis: PricingKellyAnalysis
    # Plain-English summary — safe to surface verbatim.
    recommendation: Optional[str]


# ─── Account / Reference / System ────────────────────────────────────────────
#
# Typed models for the small endpoints that don't fit anywhere else:
#   - ``GET /v1/account``      — quota & plan
#   - ``GET /v1/tickers``      — list of available tickers
#   - ``GET /v1/symbols``      — symbols with live data
#   - ``GET /v1/options/{t}``  — option-chain metadata (expirations + strikes)
#   - ``GET /health``          — health check (public)


class AccountResponse(TypedDict, total=False):
    """Account info & quota from ``GET /v1/account``.

    Returns the caller's plan tier, the day's request quota, how much has
    been consumed, and when the counter resets.

    Note ``daily_limit`` and ``remaining`` are **strings, not ints** —
    they are numeric strings (e.g. ``"1000"``) on bounded plans and the
    literal ``"unlimited"`` on Alpha / Enterprise tiers. Only ``usage_today``
    is a true integer.
    """

    user_id: Optional[str]
    email: Optional[str]
    # Plan tier (e.g. ``"free"``, ``"basic"``, ``"growth"``, ``"alpha"``).
    plan: Optional[str]
    # Numeric string (e.g. ``"1000"``) on bounded plans; literal
    # ``"unlimited"`` on Alpha/Enterprise.
    daily_limit: Optional[str]
    # Requests consumed today (integer).
    usage_today: Optional[int]
    # Numeric string on bounded plans; ``"unlimited"`` on uncapped tiers.
    remaining: Optional[str]
    # ISO timestamp at which ``usage_today`` resets to zero.
    resets_at: Optional[str]


class TickersResponse(TypedDict, total=False):
    """List of available stock tickers from ``GET /v1/tickers``."""

    tickers: List[str]
    count: Optional[int]


class SymbolsResponse(TypedDict, total=False):
    """Currently queried symbols with live data from ``GET /v1/symbols``."""

    symbols: List[str]
    count: Optional[int]
    # Free-form note from the server (e.g. coverage caveats).
    note: Optional[str]
    # ISO timestamp of the last refresh of the symbol list.
    last_updated: Optional[str]


class OptionsMetaExpiration(TypedDict, total=False):
    """One per-expiry row of the option-chain metadata.

    ``strikes`` is the list of available strikes for this expiry.
    """

    # ``"yyyy-MM-dd"`` of the expiry.
    expiration: Optional[str]
    strikes: List[float]


class OptionsMetaResponse(TypedDict, total=False):
    """Option-chain metadata from ``GET /v1/options/{ticker}``.

    Returns the list of expirations and the strikes available at each
    expiry. Use this to discover the chain shape before calling option-quote
    or pricing endpoints.
    """

    symbol: Optional[str]
    expirations: List[OptionsMetaExpiration]
    expiration_count: Optional[int]
    total_contracts: Optional[int]


class HealthResponse(TypedDict, total=False):
    """Public health-check response from ``GET /health``."""

    status: Optional[str]


# ─── Screener ────────────────────────────────────────────────────────────────
#
# Typed model for ``POST /v1/screener``.
#
# Lightweight envelope: a ``meta`` block describing the query bounds and a
# ``data`` list of result rows. Rows are intentionally untyped — ``select``
# and ``formulas`` make the row shape user-controlled, so the canonical type
# is ``List[Dict[str, Any]]``. Read row fields with ordinary dict access;
# the meta block tells you ``returned_count`` / ``total_count`` / ``tier``.


class ScreenerMeta(TypedDict, total=False):
    """Query metadata returned with every screener response.

    Reports the universe size, the total number of matching rows BEFORE
    pagination, and the number returned in the ``data`` list. ``tier`` echoes
    the calling account's tier (drives universe size and row caps).
    """

    # Total matching rows before pagination.
    total_count: Optional[int]
    # Number of rows in the ``data`` list (after limit/offset).
    returned_count: Optional[int]
    # Number of symbols in the calling account's universe.
    universe_size: Optional[int]
    # Pagination offset of this page.
    offset: Optional[int]
    # Effective row cap for this request.
    limit: Optional[int]
    # Tier label (``"growth"`` | ``"alpha"`` etc.).
    tier: Optional[str]
    # ET wall-clock timestamp the result set was computed at.
    as_of: Optional[str]


class ScreenerResponse(TypedDict, total=False):
    """Screener envelope from ``POST /v1/screener``.

    The ``data`` list rows are intentionally typed as ``List[Dict[str, Any]]``
    because the row shape is user-controlled — ``select`` chooses which fields
    are returned and ``formulas`` (Alpha+) adds computed columns. The canonical
    field set is documented separately on the API reference. Read fields with
    ordinary dict access (``row["symbol"]``, ``row["price"]``, ...).
    """

    meta: ScreenerMeta
    # Rows are select-dependent; left untyped. Read with ``row["symbol"]`` etc.
    data: List[Dict[str, Any]]


# ─── Flow (live, simulation-aware) ───────────────────────────────────────────
#
# Typed models for the ``/v1/flow/*`` surface. Two families:
#
#   * **Analytics** (``/v1/flow/{levels,pin-risk,summary,oi,gex,dex,
#     dealer-risk,live}/{symbol}``) — *simulation-aware* exposure analytics
#     that fold the live intraday trade tape into the settled snapshot, so
#     gamma flip / walls / GEX reflect *today's* flow, not yesterday's close.
#     Wire shape is snake_case. Optional ``expiry=YYYY-MM-DD`` slices to one
#     expiration cycle (OPEX- or 0DTE-only views). Requires the Alpha plan.
#
#   * **Raw flow data** (``/v1/flow/options/*``, ``/v1/flow/stocks/*``) — the
#     underlying trade tape: per-trade prints, blocks, per-minute history
#     buckets, cumulative net-flow series, and cross-symbol leaderboards /
#     outliers. These are proxied verbatim from the ingest tier, so the wire
#     keys are **camelCase** (preserved here exactly, NOT pythonised) and
#     timestamps are ISO-8601 UTC strings. Requires the Alpha plan.
#
# Flow ``gex``/``dex`` per-strike rows are the *same* wire shape as the
# settled ``/v1/exposure/gex``/``/dex`` endpoints, so they reuse
# ``GexStrikeRow`` / ``DexStrikeRow`` rather than duplicating the schema.


class FlowLevelsResponse(TypedDict, total=False):
    """Live key levels from ``GET /v1/flow/levels/{symbol}``.

    Gamma flip, call/put walls and max-pain recomputed against the
    *live* (intraday-flow-adjusted) book rather than the settled
    snapshot. Each level is ``None`` when it can't be located (e.g. no
    sign change in net gamma across the chain). Requires the Alpha plan.
    """

    symbol: str
    as_of: str
    underlying_price: Optional[float]
    # Expiration filter echoed back (``YYYY-MM-DD``), or ``None`` when
    # the whole chain was used.
    expiry: Optional[str]
    # Spot where live net dealer gamma crosses zero. ``None`` if no flip.
    live_gamma_flip: Optional[float]
    # Strike of the largest live call-gamma concentration (upside magnet).
    live_call_wall: Optional[float]
    # Strike of the largest live put-gamma concentration (downside magnet).
    live_put_wall: Optional[float]
    # Live max-pain strike (where the most option value expires worthless).
    live_max_pain: Optional[float]


class FlowPinRiskBreakdown(TypedDict, total=False):
    """Component scores (0–100) behind the ``live_pin_risk`` headline."""

    # Open-interest concentration around the magnet strike.
    oi_score: int
    # How close spot is to the magnet strike.
    proximity_score: int
    # Time-to-close weighting (pin pressure rises into the cash close).
    time_score: int
    # Dealer-gamma intensity at the magnet strike.
    gamma_score: int


class FlowPinRiskResponse(TypedDict, total=False):
    """0DTE pin-risk score from ``GET /v1/flow/pin-risk/{symbol}``.

    ``live_pin_risk`` is a 0–100 composite of the four ``breakdown``
    components. ``magnet_strike`` is the strike spot is most likely
    pinned toward into the close. Requires the Alpha plan.
    """

    symbol: str
    as_of: str
    underlying_price: Optional[float]
    expiry: Optional[str]
    # Composite 0–100 pin-risk score (higher = stronger pin pull).
    live_pin_risk: int
    # Strike acting as the pin magnet (``argmax|net gamma|``). ``None``
    # when the chain has no dominant strike.
    magnet_strike: Optional[float]
    # Signed % distance from spot to the magnet strike.
    distance_to_magnet_pct: Optional[float]
    # Hours remaining until the regular-session cash close.
    time_to_close_hours: Optional[float]
    breakdown: FlowPinRiskBreakdown


class FlowSummaryResponse(TypedDict, total=False):
    """At-a-glance flow direction from ``GET /v1/flow/summary/{symbol}``.

    Headline read on whether today's tape has shifted the dealer book.
    Requires the Alpha plan.
    """

    symbol: str
    as_of: str
    underlying_price: Optional[float]
    expiry: Optional[str]
    # Net classified direction of intraday flow
    # (e.g. ``"bullish"``, ``"bearish"``, ``"neutral"``).
    flow_direction: str
    # Net change in simulated open interest since the open (contracts).
    intraday_oi_delta: int
    # Contracts that have printed at least one trade today.
    contracts_with_flow: int
    # Total contracts tracked for the underlying.
    contracts_total: int
    # Live (flow-adjusted) net GEX (dollars per 1% spot move).
    live_gex: Optional[float]
    # % shift in net GEX caused by today's flow vs the settled book.
    # ``None`` when the settled baseline is zero (undefined ratio).
    flow_gex_pct_shift: Optional[float]


class FlowOiResponse(TypedDict, total=False):
    """Open-interest simulator state from ``GET /v1/flow/oi/{symbol}``.

    The settled (official) OI versus the intraday simulated OI built by
    folding today's trade tape onto the open. Requires the Alpha plan.
    Note: this endpoint does **not** return ``underlying_price``.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Timestamp this snapshot was computed for (ISO-8601 UTC).
    as_of: str
    # Expiration filter echoed back (``YYYY-MM-DD``), or ``None``.
    expiry: Optional[str]
    # Official exchange OI from the settled snapshot (sum across chain).
    official_oi: int
    # Intraday simulated OI (official + estimated open/close from tape).
    simulated_oi: int
    # ``simulated_oi - official_oi`` (signed).
    intraday_oi_delta: int
    # Confidence 0–1 in the intraday OI estimate (trade-tape coverage).
    oi_delta_confidence: Optional[float]
    # OI actually used by the live analytics (blended).
    effective_oi: int
    # Total contracts tracked for the underlying.
    contracts_total: int
    # Contracts that have printed at least one trade today.
    contracts_with_flow: int


class FlowGexResponse(TypedDict, total=False):
    """Live per-strike GEX from ``GET /v1/flow/gex/{symbol}``.

    Same per-strike shape as ``GET /v1/exposure/gex`` (reuses
    ``GexStrikeRow``) but computed against the live flow-adjusted book.
    Requires the Alpha plan.
    """

    symbol: str
    as_of: str
    underlying_price: Optional[float]
    expiry: Optional[str]
    # Live net GEX across the chain (dollars per 1% spot move).
    live_net_gex: Optional[float]
    # Categorical regime label (e.g. ``"positive"``, ``"negative"``).
    live_net_gex_label: str
    # Live gamma-flip spot. ``None`` if no sign change.
    live_gamma_flip: Optional[float]
    # Per-strike rows (identical schema to settled GEX). See ``GexStrikeRow``.
    strikes: List[GexStrikeRow]


class FlowDexResponse(TypedDict, total=False):
    """Live per-strike DEX from ``GET /v1/flow/dex/{symbol}``.

    Same per-strike shape as ``GET /v1/exposure/dex`` (reuses
    ``DexStrikeRow``) computed against the live book. Requires Alpha.
    """

    symbol: str
    as_of: str
    underlying_price: Optional[float]
    expiry: Optional[str]
    # Live net DEX across the chain (dollars).
    live_net_dex: Optional[float]
    strikes: List[DexStrikeRow]


class FlowDealerRiskResponse(TypedDict, total=False):
    """Settled-vs-live dealer risk from ``GET /v1/flow/dealer-risk/{symbol}``.

    Side-by-side of the settled snapshot and the live flow-adjusted
    book, with the dollar adjustment and % shift today's tape produced.
    Requires the Alpha plan.
    """

    symbol: str
    as_of: str
    underlying_price: Optional[float]
    expiry: Optional[str]
    # Net GEX from the settled (prior close) snapshot.
    settled_net_gex: Optional[float]
    # Net GEX from the live flow-adjusted book.
    live_net_gex: Optional[float]
    # ``live_net_gex - settled_net_gex`` (dollars).
    flow_gex_adjustment: Optional[float]
    # % GEX shift from flow. ``None`` when settled baseline is zero.
    flow_gex_pct_shift: Optional[float]
    # Net DEX from the settled (prior close) snapshot.
    settled_net_dex: Optional[float]
    # Net DEX from the live flow-adjusted book.
    live_net_dex: Optional[float]
    # ``live_net_dex - settled_net_dex`` (dollars).
    flow_dex_adjustment: Optional[float]
    # % DEX shift from flow. ``None`` when settled baseline is zero.
    flow_dex_pct_shift: Optional[float]
    # Absolute delta-weighted contracts traded today (flow magnitude).
    total_abs_delta_contracts: int
    # Contracts that have printed at least one trade today.
    contracts_with_flow: int
    # Net classified flow direction.
    flow_direction: str
    # Plain-English summary of whether flow has materially moved the
    # dealer book — safe to surface verbatim.
    description: str


class FlowAdjustedDealerRisk(TypedDict, total=False):
    """Nested dealer-risk block inside ``FlowLiveResponse``.

    Identical to ``FlowDealerRiskResponse`` minus ``contracts_with_flow``
    (carried on the parent ``live`` envelope instead).
    """

    # Net GEX from the settled (prior close) snapshot.
    settled_net_gex: Optional[float]
    # Net GEX from the live flow-adjusted book.
    live_net_gex: Optional[float]
    # ``live_net_gex - settled_net_gex`` (dollars).
    flow_gex_adjustment: Optional[float]
    # % GEX shift from flow. ``None`` when settled baseline is zero.
    flow_gex_pct_shift: Optional[float]
    # Net DEX from the settled snapshot.
    settled_net_dex: Optional[float]
    # Net DEX from the live flow-adjusted book.
    live_net_dex: Optional[float]
    # ``live_net_dex - settled_net_dex`` (dollars).
    flow_dex_adjustment: Optional[float]
    # % DEX shift from flow. ``None`` when settled baseline is zero.
    flow_dex_pct_shift: Optional[float]
    # Absolute delta-weighted contracts traded today (flow magnitude).
    total_abs_delta_contracts: int
    # Net classified flow direction.
    flow_direction: str
    # Plain-English summary of the shift — safe to surface verbatim.
    description: str


class FlowLiveResponse(TypedDict, total=False):
    """Everything-at-once bundle from ``GET /v1/flow/live/{symbol}``.

    Convenience aggregate: OI simulator state + live exposure metrics +
    live levels + pin risk + the nested dealer-risk block, in one call.
    Requires the Alpha plan.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Timestamp this snapshot was computed for (ISO-8601 UTC).
    as_of: str
    # Spot mid at ``as_of``.
    underlying_price: Optional[float]
    # Expiration filter echoed back (``YYYY-MM-DD``), or ``None``.
    expiry: Optional[str]
    # Total contracts tracked for the underlying.
    contracts: int
    # Contracts that have printed at least one trade today.
    contracts_with_flow: int
    # Official exchange OI from the settled snapshot.
    official_oi: int
    # Intraday simulated OI (official + estimated open/close from tape).
    simulated_oi: int
    # ``simulated_oi - official_oi`` (signed).
    intraday_oi_delta: int
    # Confidence 0–1 in the intraday OI estimate (trade-tape coverage).
    oi_delta_confidence: Optional[float]
    # OI actually used by the live analytics (blended).
    effective_oi: int
    # Live net GEX (dollars per 1% spot move).
    live_gex: Optional[float]
    # Live net DEX (dollars). (Named ``live_gex_delta`` on the wire.)
    live_gex_delta: Optional[float]
    # Live gamma-flip spot. ``None`` if no sign change.
    live_gamma_flip: Optional[float]
    # Largest live call-gamma concentration strike (upside magnet).
    live_call_wall: Optional[float]
    # Largest live put-gamma concentration strike (downside magnet).
    live_put_wall: Optional[float]
    # Live max-pain strike (most option value expires worthless).
    live_max_pain: Optional[float]
    # Composite 0–100 pin-risk score (higher = stronger pin pull).
    live_pin_risk: int
    # Nested settled-vs-live dealer-risk block. See ``FlowAdjustedDealerRisk``.
    flow_adjusted_dealer_risk: FlowAdjustedDealerRisk


# ── Raw flow data (camelCase wire keys, proxied from the ingest tier) ────────


class FlowOptionTrade(TypedDict, total=False):
    """A single option trade print (``trades[]`` element)."""

    # Trade timestamp (ISO-8601 UTC).
    ts: str
    # OPRA instrument id of the contract.
    instrumentId: int
    # Contract expiration (``YYYY-MM-DD``).
    expiry: str
    # Contract strike price.
    strike: float
    # ``"C"`` (call) or ``"P"`` (put).
    right: str
    # Trade price.
    price: float
    # Trade size in contracts.
    size: int
    # Trade-side classification vs the NBBO at print
    # (e.g. ``"buy"``, ``"sell"``, ``"mid"``).
    side: str
    # True when the print is at/above the block-size threshold.
    isBlock: bool
    # NBBO bid at the moment of the trade.
    bid: float
    # NBBO ask at the moment of the trade.
    ask: float


class FlowOptionRecentResponse(TypedDict, total=False):
    """Recent option trades from ``GET /v1/flow/options/{symbol}/recent``.

    Newest-first trade tape across the whole chain (or one ``expiry``).
    ``count`` is the number returned (capped by ``limit``);
    ``totalAvailable`` is the unclamped total. Requires the Alpha plan.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Expiration filter echoed back when supplied, else absent.
    expiry: Optional[str]
    # Number of trades returned (capped by ``limit``).
    count: int
    # Unclamped total trade count available.
    totalAvailable: int
    # Newest-first list of trade prints.
    trades: List[FlowOptionTrade]


class FlowOptionSummaryResponse(TypedDict, total=False):
    """Per-underlying option-flow aggregates from
    ``GET /v1/flow/options/{symbol}/summary``. Requires the Alpha plan.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Expiration filter echoed back when supplied, else absent.
    expiry: Optional[str]
    # Distinct contracts that printed at least one trade.
    contractsWithTrades: int
    # Total number of trade prints.
    totalTrades: int
    # Buy-classified contract volume.
    buyVolume: int
    # Sell-classified contract volume.
    sellVolume: int
    # Volume classified at the mid (uninformed).
    midVolume: int
    # ``buyVolume - sellVolume``.
    netVolume: int
    # Largest single trade size.
    biggestSingleTrade: int
    # Timestamp of the most recent print; ``None``/absent when no trades.
    lastTradeUtc: Optional[str]


class FlowOptionBlock(TypedDict, total=False):
    """A single large option print (``blocks[]`` element)."""

    # Trade timestamp (ISO-8601 UTC).
    ts: str
    # Contract expiration (``YYYY-MM-DD``).
    expiry: str
    # Contract strike price.
    strike: float
    # ``"C"`` (call) or ``"P"`` (put).
    right: str
    # Trade price.
    price: float
    # Trade size in contracts.
    size: int
    # Trade-side classification (``"buy"``/``"sell"``/``"mid"``).
    side: str


class FlowOptionBlocksResponse(TypedDict, total=False):
    """Large option prints from ``GET /v1/flow/options/{symbol}/blocks``.

    All trades with ``size >= minSize`` newest-first. Requires Alpha.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Expiration filter echoed back when supplied, else absent.
    expiry: Optional[str]
    # Minimum trade size that qualified as a block (echoed back).
    minSize: int
    # Number of blocks returned.
    count: int
    # Newest-first list of large prints.
    blocks: List[FlowOptionBlock]


class FlowOptionHistoryBucket(TypedDict, total=False):
    """One per-minute option-flow bucket (``buckets[]`` element)."""

    # Bucket start (ISO-8601 UTC, minute-aligned).
    ts: str
    # Buy-classified volume in the bucket.
    buyVolume: int
    # Sell-classified volume in the bucket.
    sellVolume: int
    # Mid-classified volume in the bucket.
    midVolume: int
    # ``buyVolume - sellVolume``.
    netVolume: int
    # Number of trades in the bucket.
    tradeCount: int
    # Largest single trade size in the bucket.
    biggestTrade: int
    # Volume-weighted average trade price across the bucket.
    vwap: float
    # Highest trade price in the bucket.
    high: float
    # Lowest trade price in the bucket.
    low: float


class FlowOptionHistoryResponse(TypedDict, total=False):
    """Per-minute option-flow history from
    ``GET /v1/flow/options/{symbol}/history``. Newest-first, capped to
    the ``minutes`` window. Requires the Alpha plan.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Expiration filter echoed back when supplied, else absent.
    expiry: Optional[str]
    # Lookback window in minutes (echoed back).
    minutes: int
    # Number of buckets returned.
    count: int
    # Newest-first list of per-minute aggregates.
    buckets: List[FlowOptionHistoryBucket]


class FlowCumulativePoint(TypedDict, total=False):
    """One point of a cumulative net-flow series (``points[]`` element).

    Shared by the option and stock ``/cumulative`` endpoints.
    """

    # Bucket start (ISO-8601 UTC, minute-aligned).
    ts: str
    # Net volume in this minute bucket.
    netVolume: int
    # Running sum of ``netVolume`` from the start of the window
    # (the "HIRO-style" cumulative line).
    cumulative: int
    # Volume-weighted average price in the bucket.
    vwap: float
    # Number of trades in the bucket.
    tradeCount: int


class FlowOptionCumulativeResponse(TypedDict, total=False):
    """Cumulative option net-flow series from
    ``GET /v1/flow/options/{symbol}/cumulative``. Requires Alpha.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Expiration filter echoed back when supplied, else absent.
    expiry: Optional[str]
    # Lookback window in minutes (echoed back).
    minutes: int
    # Number of points returned.
    count: int
    # Chronological cumulative net-flow series.
    points: List[FlowCumulativePoint]


class FlowStockTrade(TypedDict, total=False):
    """A single stock trade print (``trades[]`` element)."""

    # Trade timestamp (ISO-8601 UTC).
    ts: str
    # Trade price.
    price: float
    # Trade size in shares.
    size: int
    # Trade-side classification (``"buy"``/``"sell"``/``"mid"``).
    side: str
    # True when the print is at/above the block-size threshold.
    isBlock: bool
    # NBBO bid at the moment of the trade.
    bid: float
    # NBBO ask at the moment of the trade.
    ask: float


class FlowStockRecentResponse(TypedDict, total=False):
    """Recent stock trades from ``GET /v1/flow/stocks/{symbol}/recent``.

    Newest-first stock tape. Requires the Alpha plan.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Number of trades returned (capped by ``limit``).
    count: int
    # Unclamped total trade count available.
    totalAvailable: int
    # Newest-first list of trade prints.
    trades: List[FlowStockTrade]


class FlowStockSummaryResponse(TypedDict, total=False):
    """Per-symbol stock-flow aggregates from
    ``GET /v1/flow/stocks/{symbol}/summary``. Requires the Alpha plan.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Total number of trade prints.
    totalTrades: int
    # Buy-classified share volume.
    buyVolume: int
    # Sell-classified share volume.
    sellVolume: int
    # Volume classified at the mid (uninformed).
    midVolume: int
    # ``buyVolume - sellVolume``.
    netVolume: int
    # Largest single trade size.
    biggestSingleTrade: int
    # Timestamp of the most recent print; absent when no trades.
    lastTradeUtc: Optional[str]


class FlowStockBlock(TypedDict, total=False):
    """A single large stock print (``blocks[]`` element)."""

    # Trade timestamp (ISO-8601 UTC).
    ts: str
    # Trade price.
    price: float
    # Trade size in shares.
    size: int
    # Trade-side classification (``"buy"``/``"sell"``/``"mid"``).
    side: str
    # NBBO bid at the moment of the trade.
    bid: float
    # NBBO ask at the moment of the trade.
    ask: float


class FlowStockBlocksResponse(TypedDict, total=False):
    """Large stock prints from ``GET /v1/flow/stocks/{symbol}/blocks``.

    All trades with ``size >= minSize`` newest-first. Requires Alpha.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Minimum trade size that qualified as a block (echoed back).
    minSize: int
    # Number of blocks returned.
    count: int
    # Newest-first list of large prints.
    blocks: List[FlowStockBlock]


class FlowStockHistoryBucket(TypedDict, total=False):
    """One per-minute stock-flow bucket (``buckets[]`` element).

    Like ``FlowOptionHistoryBucket`` but also carries OHLC
    (``open``/``close``/``high``/``low``) of the underlying print price.
    """

    # Bucket start (ISO-8601 UTC, minute-aligned).
    ts: str
    # Buy-classified volume in the bucket.
    buyVolume: int
    # Sell-classified volume in the bucket.
    sellVolume: int
    # Mid-classified volume in the bucket.
    midVolume: int
    # ``buyVolume - sellVolume``.
    netVolume: int
    # Number of trades in the bucket.
    tradeCount: int
    # Largest single trade size in the bucket.
    biggestTrade: int
    # Volume-weighted average trade price across the bucket.
    vwap: float
    # First trade price in the bucket.
    open: float
    # Last trade price in the bucket.
    close: float
    # Highest trade price in the bucket.
    high: float
    # Lowest trade price in the bucket.
    low: float


class FlowStockHistoryResponse(TypedDict, total=False):
    """Per-minute stock-flow history from
    ``GET /v1/flow/stocks/{symbol}/history``. Newest-first, capped to
    the ``minutes`` window. Requires the Alpha plan.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Lookback window in minutes (echoed back).
    minutes: int
    # Number of buckets returned.
    count: int
    # Newest-first list of per-minute aggregates.
    buckets: List[FlowStockHistoryBucket]


class FlowStockCumulativeResponse(TypedDict, total=False):
    """Cumulative stock net-flow series from
    ``GET /v1/flow/stocks/{symbol}/cumulative``. Requires Alpha.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Lookback window in minutes (echoed back).
    minutes: int
    # Number of points returned.
    count: int
    # Chronological cumulative net-flow series.
    points: List[FlowCumulativePoint]


class FlowOptionLeaderRow(TypedDict, total=False):
    """One ranked underlying in the option-flow leaderboard.

    Note: option rows carry ``avgPremium`` (avg option price); the stock
    leaderboard uses ``vwap`` instead.
    """

    # Ranked underlying.
    symbol: str
    # Net contracts (``buyVolume - sellVolume``).
    netVolume: int
    # Net dollar option flow (≈ net contracts × avg premium × 100).
    netNotional: float
    # Buy-classified contract volume.
    buyVolume: int
    # Sell-classified contract volume.
    sellVolume: int
    # Volume-weighted average option premium over the window.
    avgPremium: float
    # Number of trades over the window.
    tradeCount: int
    # Timestamp of the most recent print (ISO-8601 UTC).
    lastTradeUtc: str


class FlowOptionLeaderboardResponse(TypedDict, total=False):
    """Cross-symbol option-flow leaderboard from
    ``GET /v1/flow/options/leaderboard``.

    Top ``n`` net-dollar buyers and sellers over the window. Cached ~30s.
    Requires the Alpha plan.
    """

    # When the snapshot was generated (ISO-8601 UTC).
    generatedUtc: str
    # Number of ranked rows requested per side.
    n: int
    # Aggregation window in minutes.
    windowMinutes: int
    # Top net-dollar buyers.
    buyers: List[FlowOptionLeaderRow]
    # Top net-dollar sellers.
    sellers: List[FlowOptionLeaderRow]


class FlowOutlierRow(TypedDict, total=False):
    """One flagged underlying in an outliers table (option or stock)."""

    # Flagged underlying.
    symbol: str
    # Number of trades over the window.
    tradeCount: int
    # Buy-classified volume.
    buyVolume: int
    # Sell-classified volume.
    sellVolume: int
    # Mid-classified volume.
    midVolume: int
    # ``buyVolume - sellVolume``.
    netVolume: int
    # ``|buy-sell| / (buy+sell)`` × 100: 0 = balanced, 100 = one-sided.
    imbalancePct: float
    # Tiered skew label (``FLAT``/``MILD_BUY``/``BUY``/``STRONG_BUY``/…).
    skew: str
    # Gross traded notional over the window (dollars).
    notional: float
    # Net (signed) traded notional over the window (dollars).
    netNotional: float
    # Largest single trade size.
    biggestTrade: int
    # Timestamp of the biggest print; ``None`` if none in window.
    biggestTradeUtc: Optional[str]
    # Age of the biggest print in seconds; ``-1`` if none.
    biggestAgeSec: int
    # VWAP of the most recent activity.
    lastVwap: float
    # Timestamp of the last print; ``None`` if none.
    lastTradeUtc: Optional[str]
    # Age of the last print in seconds; ``-1`` if none.
    lastTradeAgeSec: int


class FlowOptionOutliersResponse(TypedDict, total=False):
    """Cross-symbol option-flow outliers from
    ``GET /v1/flow/options/outliers``. Cached ~30s. Requires Alpha.
    """

    # When the snapshot was generated (ISO-8601 UTC).
    generatedUtc: str
    # Aggregation window in minutes.
    windowMinutes: int
    # Symbols evaluated.
    tracked: int
    # Symbols that met ``minTrades`` and had non-zero volume.
    qualified: int
    # Max rows requested.
    limit: int
    # Imbalance-ranked flagged underlyings.
    outliers: List[FlowOutlierRow]


class FlowStockLeaderRow(TypedDict, total=False):
    """One ranked symbol in the stock-flow leaderboard.

    Note: stock rows carry ``vwap``; the option leaderboard uses
    ``avgPremium`` instead.
    """

    # Ranked symbol.
    symbol: str
    # Net shares (``buyVolume - sellVolume``).
    netVolume: int
    # Net dollar flow (net shares × VWAP).
    netNotional: float
    # Buy-classified share volume.
    buyVolume: int
    # Sell-classified share volume.
    sellVolume: int
    # Volume-weighted average trade price over the window.
    vwap: float
    # Number of trades over the window.
    tradeCount: int
    # Timestamp of the most recent print (ISO-8601 UTC).
    lastTradeUtc: str


class FlowStockLeaderboardResponse(TypedDict, total=False):
    """Cross-symbol stock-flow leaderboard from
    ``GET /v1/flow/stocks/leaderboard``. Cached ~30s. Requires Alpha.
    """

    # When the snapshot was generated (ISO-8601 UTC).
    generatedUtc: str
    # Number of ranked rows requested per side.
    n: int
    # Aggregation window in minutes.
    windowMinutes: int
    # Top net-dollar buyers.
    buyers: List[FlowStockLeaderRow]
    # Top net-dollar sellers.
    sellers: List[FlowStockLeaderRow]


class FlowStockOutliersResponse(TypedDict, total=False):
    """Cross-symbol stock-flow outliers from
    ``GET /v1/flow/stocks/outliers``. Cached ~30s. Requires Alpha.
    """

    # When the snapshot was generated (ISO-8601 UTC).
    generatedUtc: str
    # Aggregation window in minutes.
    windowMinutes: int
    # Symbols evaluated.
    tracked: int
    # Symbols that met ``minTrades`` and had non-zero volume.
    qualified: int
    # Max rows requested.
    limit: int
    # Imbalance-ranked flagged symbols.
    outliers: List[FlowOutlierRow]


# ── Flow signals (unusual-flow feed, Alpha+) ─────────────────────────
#
# Per-underlying scored/classified unusual-flow signals. Snake_case wire
# shape (analytics family). Both endpoints reuse ``FlowSignal``.


class FlowSignalsChain(TypedDict, total=False):
    """Settled-chain reference levels echoed alongside the signals.

    Computed once per request from the settled snapshot — independent of
    the live flow surface. All fields are ``None`` when the chain
    snapshot is unavailable.
    """

    call_wall: Optional[float]
    put_wall: Optional[float]
    max_pain: Optional[float]
    gamma_flip: Optional[float]


class FlowSignalScoreBreakdown(TypedDict, total=False):
    """Component contributions that sum to the headline ``score``.

    Weights are server-tunable so absolute values may shift, but the
    ordering of components is stable.
    """

    premium: int
    size_vs_oi: int
    aggressor: int
    sweep: int
    opening_bias: int
    tenor: int


class FlowSignalEnrichment(TypedDict, total=False):
    """Chain-derived context attached to a signal.

    All numeric fields are ``None`` and ``moneyness`` is ``"unknown"``
    when the contract isn't in the settled chain snapshot.
    """

    iv: Optional[float]
    delta: Optional[float]
    gamma: Optional[float]
    # IV minus the nearest ATM IV (signed).
    iv_vs_atm: Optional[float]
    # ``"OTM"`` / ``"ATM"`` / ``"ITM"`` / ``"unknown"``.
    moneyness: str
    # Estimated dollar delta-notional of this print.
    estimated_delta_notional: Optional[float]
    # Standalone gamma-$ this print would add if it were opening and
    # fully dealer-absorbed. **Not** applied to the live chain — don't
    # sum it against ``/v1/flow/gex``.
    hypothetical_gex_impact_if_opening: Optional[float]


class FlowSignal(TypedDict, total=False):
    """One scored unusual-flow signal.

    A signal is a coalesced view of one notable (block-sized) print on a
    single contract: classification, scoring, and chain-context
    enrichment. Same shape across ``/v1/flow/signals/{symbol}`` and
    ``/v1/flow/signals/{symbol}/summary``'s ``top_signals``.
    """

    # Trade timestamp (ISO-8601 UTC).
    ts: str
    # Contract expiry (``YYYY-MM-DD``).
    expiry: str
    # Contract strike price.
    strike: float
    # ``"C"`` (call) or ``"P"`` (put).
    right: str
    # Upstream buy/sell/mid aggressor classification (distinct from the
    # NBBO ``aggressor`` label).
    side: str
    # Trade price.
    price: float
    # Trade size in contracts.
    size: int
    # Dollar premium of this print: ``price * size * 100``.
    premium: float
    # Days to expiry at trade time.
    dte: int
    # ``"block"`` (lone block-sized print) or ``"sweep"`` (≥2 same-side
    # prints on one contract within ~500ms).
    structure: str
    # NBBO position at trade: ``"above_ask"`` / ``"at_ask"`` / ``"mid"`` /
    # ``"at_bid"`` / ``"below_bid"``.
    aggressor: str
    # Contract-level OI-simulator inference: ``"opening_bias"`` /
    # ``"closing_bias"`` / ``"unknown"``. Not a per-print label.
    open_close_bias: str
    # Simulator confidence weight for the bias above.
    open_close_confidence: float
    # Signed simulator estimate of contracts opened (+) or closed (−)
    # today on this contract.
    contract_net_oi_delta: int
    # ``"bullish"`` / ``"bearish"`` / ``"neutral"``. Neutral whenever
    # ``open_close_bias == "closing_bias"`` (can't attribute on unwinds)
    # or ``side == "mid"``.
    intent: str
    # 0–100 composite (components sum to this).
    score: int
    # ``"low"`` / ``"medium"`` / ``"high"``.
    conviction: str
    # Subset of ``"sweep"``, ``"block"``, ``"opening"``, ``"closing"``,
    # ``"0dte"``, ``"whale"`` (premium ≥ $1M), ``"golden"`` (top decile
    # in this response set *and* score ≥ 70 absolute).
    tags: List[str]
    score_breakdown: FlowSignalScoreBreakdown
    enrichment: FlowSignalEnrichment


class FlowSignalsResponse(TypedDict, total=False):
    """Scored, classified unusual-flow feed from
    ``GET /v1/flow/signals/{symbol}``.

    Each notable print in the look-back window is coalesced into a
    signal, scored 0–100, and ranked highest score first. Requires the
    Alpha plan.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Timestamp this snapshot was computed for (ISO-8601 UTC).
    as_of: str
    # Look-back window applied (minutes).
    window_minutes: int
    # Expiration filter echoed back, or ``None``.
    expiry: Optional[str]
    # Spot mid at the snapshot time.
    underlying_price: Optional[float]
    # Settled-chain reference levels (computed once per request).
    chain: FlowSignalsChain
    # Number of signals returned (after server-side filtering).
    count: int
    # Signals, highest score first.
    signals: List[FlowSignal]


class FlowSignalsSummaryResponse(TypedDict, total=False):
    """Net-directional roll-up from
    ``GET /v1/flow/signals/{symbol}/summary``.

    Sums classified premium across the window into bullish/bearish and
    opening/closing buckets — a cheap "smart-money tilt" read for one
    underlying. Requires the Alpha plan.
    """

    # Underlying ticker echoed from the request path.
    symbol: str
    # Timestamp this snapshot was computed for (ISO-8601 UTC).
    as_of: str
    # Look-back window applied (minutes).
    window_minutes: int
    # Expiration filter echoed back, or ``None``.
    expiry: Optional[str]
    # Spot mid at the snapshot time.
    underlying_price: Optional[float]
    # Total signal count in the window (full count, not the
    # ``top_signals`` length).
    signal_count: int
    # Sum of signal premium with ``intent == "bullish"``.
    bullish_premium: float
    # Sum of signal premium with ``intent == "bearish"``.
    bearish_premium: float
    # ``bullish_premium - bearish_premium``.
    net_directional_premium: float
    # Sum of signal premium with ``open_close_bias == "opening_bias"``.
    opening_premium: float
    # Sum of signal premium with ``open_close_bias == "closing_bias"``.
    closing_premium: float
    # Highest-scoring signals (≤ 10). Same shape as ``FlowSignal``.
    top_signals: List[FlowSignal]


# ─── Strategy Signals (shared decision envelope) ─────────────────────────────
#
# Typed model for the ten ``GET /v1/strategies/*/{symbol}`` endpoints. Every
# strategy returns the SAME envelope shape — only ``metrics`` and ``regime``
# change between strategies. ``metrics`` is a free-form ``Dict[str, Any]``
# (the keys documented per-endpoint differ; ``underlying_price`` is always
# present), so one ``StrategyDecisionResponse`` covers all ten named methods.


class StrategyLeg(TypedDict, total=False):
    """One leg of a proposed tradeable structure."""

    # ``"buy"`` (alias ``"long"``) or ``"sell"`` (alias ``"short"``).
    action: str
    # ``"call"`` or ``"put"``.
    type: str
    strike: Optional[float]
    # Greek delta of the leg (signed).
    delta: Optional[float]
    # Per-contract premium paid/received.
    premium: Optional[float]
    # Number of contracts.
    quantity: Optional[int]


class StrategyStructure(TypedDict, total=False):
    """One ranked candidate structure from ``best_structures[]``.

    Pure-signal strategies (``skew``, ``term_structure``, ``tail_pricing``)
    always return an empty ``best_structures`` list — they emit a read, not a
    trade.
    """

    # 1-based rank (1 = best).
    rank: Optional[int]
    # Structure name (e.g. ``"short_put_spread"``, ``"iron_fly"``,
    # ``"iron_condor"``, ``"covered_call"``). Free-form.
    structure: Optional[str]
    # ``"yyyy-MM-dd"`` of the structure's target expiry.
    expiry: Optional[str]
    legs: List[StrategyLeg]
    # Net credit collected (``None`` for debit structures).
    credit: Optional[float]
    # Net debit paid (``None`` for credit structures).
    debit: Optional[float]
    # Max profit / loss at expiry (``None`` when unbounded on that side).
    max_profit: Optional[float]
    max_loss: Optional[float]
    # Underlying prices where P&L crosses zero.
    breakevens: List[float]
    # 0-100 edge score for this structure.
    edge_score: Optional[int]
    # 0-1 liquidity score for this structure.
    liquidity_score: Optional[float]


class StrategyRiskFlag(TypedDict, total=False):
    """One risk callout attached to a strategy decision."""

    # ``"low"`` / ``"medium"`` / ``"high"``.
    severity: Optional[str]
    # Machine-readable code (e.g. ``"EARNINGS_BEFORE_EXPIRY"``).
    code: Optional[str]
    # Human-readable message — safe to surface verbatim.
    message: Optional[str]


class StrategyDataQuality(TypedDict, total=False):
    """Input-quality gate. Gate on ``score`` before acting on a decision."""

    # 0-100 input-quality score.
    score: Optional[int]
    # Free-form warning strings (empty when clean).
    warnings: List[str]


class StrategyDecisionResponse(TypedDict, total=False):
    """Uniform decision envelope for every ``GET /v1/strategies/*/{symbol}``.

    Shared across all ten strategy endpoints (flow-anomaly,
    expiry-positioning, zero-dte, dealer-regime, vol-carry,
    yield-enhancement, surface-anomaly, skew, term-structure,
    tail-pricing). Only ``metrics`` and ``regime`` vary between strategies;
    everything else has a fixed shape.

    Strategies can short-circuit with ``decision == "insufficient_data"``
    and a strategy-specific ``regime`` (e.g. ``"symbol_not_covered_historically"``,
    ``"vrp_unavailable"``, ``"no_fitted_surface"``, ``"no_skew_data"``).
    """

    # Which strategy produced this result (e.g. ``"flow_anomaly"``).
    strategy: str
    # Resolved, upper-cased underlying symbol.
    symbol: str
    # ISO-8601 UTC time the decision was built.
    timestamp: str
    # ``"insufficient_data"`` / ``"avoid"`` / ``"neutral"`` / ``"candidate"``.
    decision: str
    # 0-100 strategy score (drives ``decision``).
    score: Optional[int]
    # 0-1 input-quality / sample-size weight.
    confidence: Optional[float]
    # Strategy-specific regime label (vocabulary differs per endpoint).
    regime: Optional[str]
    # Ranked candidate structures (empty for pure-signal strategies).
    best_structures: List[StrategyStructure]
    # Strategy-specific key/value bag. ``underlying_price`` always present.
    metrics: Dict[str, Any]
    # Optional risk callouts (often empty).
    risk_flags: List[StrategyRiskFlag]
    # Human-readable rationale for the decision.
    why: List[str]
    # Conditions under which the read should be discarded.
    avoid_if: List[str]
    # Input-quality gate — check before trading.
    data_quality: StrategyDataQuality


# ─── Earnings ────────────────────────────────────────────────────────────────
#
# Typed models for the eight ``GET /v1/earnings/*`` endpoints. Earnings-event
# analytics derived from the upcoming/historical earnings calendar plus live
# options term structure.


class EarningsCalendarEvent(TypedDict, total=False):
    """One upcoming earnings event row (``events[]`` of the calendar)."""

    symbol: Optional[str]
    company_name: Optional[str]
    # ``"yyyy-MM-dd"``.
    earnings_date: Optional[str]
    # Reporting session: ``"bmo"`` (before open) / ``"amc"`` (after close);
    # may be null/unknown.
    timing: Optional[str]
    # Whether the date is confirmed (vs. estimated) by the provider.
    is_confirmed: Optional[bool]
    fiscal_period: Optional[str]
    fiscal_year: Optional[int]
    # Provider importance rating (higher = more market-moving); nullable.
    importance: Optional[int]
    eps_estimate: Optional[float]
    # Stored earnings-implied move (%), if available; nullable.
    implied_move_pct: Optional[float]
    # Calendar days from today (UTC) to the earnings date.
    days_to_event: Optional[int]


class EarningsCalendarResponse(TypedDict, total=False):
    """Upcoming earnings calendar from ``GET /v1/earnings/calendar`` (Growth+)."""

    events: List[EarningsCalendarEvent]
    count: Optional[int]


class EarningsExpectedMoveBlock(TypedDict, total=False):
    """Earnings-implied move decomposition.

    ``None`` (the whole block) when the pre/post-event expiry IVs cannot be
    resolved from the live term structure.
    """

    # Total expected move (%) implied by the front straddle.
    raw_straddle_pct: Optional[float]
    # Portion (%) attributed to the earnings jump.
    earnings_implied_pct: Optional[float]
    # Portion (%) attributed to ordinary baseline diffusion.
    baseline_drift_pct: Optional[float]
    # ATM IV (%) of the pre-event (front) expiry.
    earnings_iv: Optional[float]
    # ATM IV (%) of the first post-event expiry.
    term_iv_post_event: Optional[float]
    # Term-structure kink (%) across the event.
    term_kink_pct: Optional[float]


class EarningsExpectedMoveResponse(TypedDict, total=False):
    """Live earnings expected-move decomposition from
    ``GET /v1/earnings/expected-move/{symbol}`` (Growth+).
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    earnings_date: Optional[str]
    # Reporting session (``"bmo"`` / ``"amc"``).
    session: Optional[str]
    days_to_event: Optional[int]
    # ``None`` when the decomposition can't be resolved.
    expected_move: Optional[EarningsExpectedMoveBlock]


class EarningsHistoryRow(TypedDict, total=False):
    """One past earnings event (``history[]``)."""

    date: Optional[str]
    fiscal_period: Optional[str]
    fiscal_year: Optional[int]
    eps_estimate: Optional[float]
    eps_actual: Optional[float]
    # EPS surprise vs. estimate (%); positive = beat.
    eps_surprise_pct: Optional[float]
    revenue_actual: Optional[float]
    revenue_surprise_pct: Optional[float]
    # Earnings-implied move (%) priced before the event.
    implied_move_pct: Optional[float]
    # Realized post-earnings move (%); sign indicates direction.
    actual_move_pct: Optional[float]
    # Realized IV crush (%) from pre- to post-event ATM IV.
    iv_crush_pct: Optional[float]
    pre_atm_iv: Optional[float]
    post_atm_iv: Optional[float]


class EarningsHistoryResponse(TypedDict, total=False):
    """Past earnings events from ``GET /v1/earnings/history/{symbol}`` (Growth+).

    Only already-reported events (with an actual EPS result) are returned.
    """

    symbol: str
    count: Optional[int]
    history: List[EarningsHistoryRow]


class EarningsIvCrushCurrent(TypedDict, total=False):
    """Live IV-crush estimate for the next event.

    ``None`` (the whole block) when no upcoming event or the term structure
    can't be resolved.
    """

    # Expected ATM IV drop (%) = ``(pre_iv − post_iv) / pre_iv × 100``.
    expected_crush_pct: Optional[float]
    pre_iv: Optional[float]
    post_iv: Optional[float]


class EarningsIvCrushDistribution(TypedDict, total=False):
    """Historical realized IV-crush distribution (up to last 20 events)."""

    median: Optional[float]
    p25: Optional[float]
    p75: Optional[float]
    # Smallest / largest historical crush (%).
    worst: Optional[float]
    best: Optional[float]
    count: Optional[int]


class EarningsIvCrushResponse(TypedDict, total=False):
    """Expected IV crush + historical distribution from
    ``GET /v1/earnings/iv-crush/{symbol}`` (Growth+).
    """

    symbol: str
    as_of: str
    # Next event date; ``None`` when no upcoming event but history exists.
    earnings_date: Optional[str]
    # ``None`` when no upcoming event / term structure unresolvable.
    current_estimate: Optional[EarningsIvCrushCurrent]
    distribution: EarningsIvCrushDistribution


class EarningsVrpBlock(TypedDict, total=False):
    """Earnings VRP — implied event move vs. realized history of actual moves."""

    # Live earnings-implied move (%); falls back to stored implied move.
    implied_move_pct: Optional[float]
    # Median / mean of historical absolute actual moves (%).
    realized_median: Optional[float]
    realized_mean: Optional[float]
    # ``implied_move / realized_median`` — >1 means options price more.
    premium_ratio: Optional[float]
    # Implied move vs. realized distribution (z); ``None`` when <5 moves.
    z_score: Optional[float]
    # Percentile of implied within historical realized; ``None`` when <5.
    percentile: Optional[int]
    # ``"rich"`` / ``"slightly_rich"`` / ``"fair"`` / ``"slightly_cheap"`` /
    # ``"cheap"`` / ``"insufficient_data"``.
    assessment: Optional[str]
    # ``"downside_overpriced"`` / ``"upside_overpriced"`` or ``None``.
    directional_bias: Optional[str]


class EarningsSurpriseReaction(TypedDict, total=False):
    """Average post-earnings move by EPS-surprise bucket."""

    # Avg actual move (%) following EPS beats (surprise > 1%).
    beat_avg_move_pct: Optional[float]
    # Avg actual move (%) following EPS misses (surprise < −1%).
    miss_avg_move_pct: Optional[float]
    # Avg actual move (%) following in-line results.
    inline_avg_move_pct: Optional[float]


class EarningsVrpResponse(TypedDict, total=False):
    """Earnings volatility-risk-premium from
    ``GET /v1/earnings/vrp/{symbol}`` (Alpha+).
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    earnings_date: Optional[str]
    days_to_event: Optional[int]
    earnings_vrp: EarningsVrpBlock
    surprise_reaction: EarningsSurpriseReaction


class EarningsDealerLevels(TypedDict, total=False):
    """Dealer levels scoped to the event-week expiries."""

    gamma_flip: Optional[float]
    call_wall: Optional[float]
    put_wall: Optional[float]
    highest_oi_strike: Optional[float]


class EarningsDealerGexBucket(TypedDict, total=False):
    """One GEX bucket (``pre_event`` / ``event_week`` / ``post_event``)."""

    bucket: Optional[str]
    net_gex: Optional[float]
    contract_count: Optional[int]


class EarningsDealerTopStrike(TypedDict, total=False):
    """One of the top strikes by absolute net GEX."""

    strike: Optional[float]
    net_gex: Optional[float]
    call_oi: Optional[int]
    put_oi: Optional[int]


class EarningsDealerPositioningResponse(TypedDict, total=False):
    """Dealer exposure scoped to the earnings event from
    ``GET /v1/earnings/dealer-positioning/{symbol}`` (Alpha+).
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    earnings_date: Optional[str]
    # Closest options expiry on or after the earnings date; ``None`` if none.
    event_expiry: Optional[str]
    levels: EarningsDealerLevels
    gex_by_dte_bucket: List[EarningsDealerGexBucket]
    top_strikes: List[EarningsDealerTopStrike]
    # Ratio of event-expiry CHEX to full-chain CHEX; ``None`` when N/A.
    charm_acceleration: Optional[float]
    # ``"positive_gamma"`` / ``"negative_gamma"`` / ``"undetermined"``.
    regime: Optional[str]


class EarningsStrategyScores(TypedDict, total=False):
    """0-100 suitability scores per earnings structure."""

    long_straddle: Optional[int]
    short_strangle: Optional[int]
    iron_condor: Optional[int]
    calendar_spread: Optional[int]
    earnings_diagonal: Optional[int]


class EarningsStrategyContext(TypedDict, total=False):
    """Scoring inputs behind the earnings strategy scores."""

    premium_ratio: Optional[float]
    iv_crush_median: Optional[float]
    # ``"positive_gamma"`` / ``"negative_gamma"`` / ``"undetermined"``.
    regime: Optional[str]
    implied_move_pct: Optional[float]


class EarningsStrategiesResponse(TypedDict, total=False):
    """Earnings strategy-suitability scores from
    ``GET /v1/earnings/strategies/{symbol}`` (Alpha+).
    """

    symbol: str
    as_of: str
    earnings_date: Optional[str]
    scores: EarningsStrategyScores
    context: EarningsStrategyContext


class EarningsScreenerEvent(TypedDict, total=False):
    """One row of the earnings screener (``events[]``)."""

    symbol: Optional[str]
    company_name: Optional[str]
    earnings_date: Optional[str]
    days_to_event: Optional[int]
    timing: Optional[str]
    importance: Optional[int]
    implied_move_pct: Optional[float]
    # VRP premium ratio (implied / realized-median); ``None`` when no history.
    premium_ratio: Optional[float]
    # Median historical IV crush (%); ``None`` when no crush history.
    iv_crush_median: Optional[float]
    # VRP richness classification; ``None`` when no history.
    assessment: Optional[str]


class EarningsScreenerResponse(TypedDict, total=False):
    """Cross-sectional earnings screener from
    ``GET /v1/earnings/screener`` (Alpha+).

    ``count`` is the total matched before ``limit`` (the ``events`` array is
    capped at ``limit``).
    """

    events: List[EarningsScreenerEvent]
    count: Optional[int]


# ─── Structures (pure-math, POST) ────────────────────────────────────────────
#
# Typed models for ``POST /v1/structures/pnl`` and
# ``POST /v1/structures/greeks``. Deterministic functions of the supplied
# legs — no market-data lookup. Request leg dicts use camelCase-free simple
# keys for pnl, plus ``expiry``/``impliedVol`` (camelCase on the wire) for
# greeks.


class StructurePnlLeg(TypedDict, total=False):
    """One leg of a P&L structure request.

    ``action`` accepts ``buy``/``sell`` (aliases ``long``/``short``);
    ``type`` accepts ``call``/``put`` (aliases ``c``/``p``).
    """

    action: str
    type: str
    strike: float
    # Per-contract premium paid/received (``>= 0``).
    premium: float
    # Number of contracts (``> 0``; defaults to 1 server-side).
    quantity: int


class StructurePnlPoint(TypedDict, total=False):
    """One sample of the at-expiry P&L curve."""

    underlying: float
    pnl: float


class StructurePnlResponse(TypedDict, total=False):
    """At-expiry P&L curve from ``POST /v1/structures/pnl`` (Basic+).

    ``max_profit`` / ``max_loss`` are ``None`` on any side that is unbounded.
    """

    # Echoes the request legs verbatim.
    legs: List[StructurePnlLeg]
    pnl_curve: List[StructurePnlPoint]
    # Underlying prices where P&L crosses zero (may be empty).
    breakevens: List[float]
    max_profit: Optional[float]
    max_loss: Optional[float]


class StructureGreeksLeg(TypedDict, total=False):
    """One leg of a Greeks structure request.

    Carries its own ``expiry`` and ``impliedVol`` (camelCase on the wire) so
    calendars and diagonals aggregate correctly.
    """

    action: str
    type: str
    strike: float
    # ``"yyyy-MM-dd"``.
    expiry: str
    # Implied vol as a decimal (e.g. ``0.28``); ``> 0``. CamelCase on wire.
    impliedVol: float
    quantity: int


class StructurePositionGreeks(TypedDict, total=False):
    """Aggregated position Greeks (signed for direction, scaled by quantity)."""

    delta: Optional[float]
    gamma: Optional[float]
    theta: Optional[float]
    vega: Optional[float]
    rho: Optional[float]
    vanna: Optional[float]
    charm: Optional[float]


class StructureGreeksResponse(TypedDict, total=False):
    """Aggregate position Greeks from ``POST /v1/structures/greeks`` (Basic+).

    Top-level keys are snake_case; echoed ``legs`` keep the request's
    camelCase (``impliedVol``).
    """

    spot: Optional[float]
    as_of: str
    # The resolved ``today`` valuation date.
    valuation_date: Optional[str]
    rate: Optional[float]
    dividend_yield: Optional[float]
    legs: List[StructureGreeksLeg]
    position_greeks: StructurePositionGreeks


# ─── Surface SVI ─────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/surface/svi/{symbol}`` (Alpha+). A lightweight
# subset of the advanced-volatility payload — just the per-expiry SVI params.
# Reuses ``AdvVolSviParam`` for the per-slice rows.


class SurfaceSviResponse(TypedDict, total=False):
    """Live SVI-fitted surface from ``GET /v1/surface/svi/{symbol}`` (Alpha+).

    ``svi_parameters`` is ordered by ``days_to_expiry``; each slice gives the
    raw SVI params (``a``, ``b``, ``rho``, ``m``, ``sigma``), the per-expiry
    ``forward``, ``atm_total_variance``, and ``atm_iv`` (%). Reuses
    ``AdvVolSviParam`` for the rows.
    """

    symbol: str
    # Mid of the underlying.
    underlying_price: Optional[float]
    as_of: str
    market_open: Optional[bool]
    svi_parameters: List[AdvVolSviParam]


# ─── Expected Move ───────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/expected-move/{symbol}`` (Basic+). NOTE: the items
# inside ``expected_moves`` use camelCase keys (``daysToExpiry``, ``atmIv``,
# ``expectedMove``, ``expectedMovePct``, ``lowerBound``, ``upperBound``) even
# though the top-level keys are snake_case.


class ExpectedMoveItem(TypedDict, total=False):
    """One per-expiry expected-move row (camelCase keys on the wire)."""

    expiry: Optional[str]
    # Calendar days. CamelCase on wire.
    daysToExpiry: Optional[int]
    # ATM IV as a decimal, or ``None`` when no ATM IV. CamelCase on wire.
    atmIv: Optional[float]
    # 1-σ move in price terms. CamelCase on wire.
    expectedMove: Optional[float]
    # As a percentage of spot. CamelCase on wire.
    expectedMovePct: Optional[float]
    # ``spot − expectedMove`` / ``spot + expectedMove``. CamelCase on wire.
    lowerBound: Optional[float]
    upperBound: Optional[float]


class ExpectedMoveResponse(TypedDict, total=False):
    """Straddle-implied expected move per expiry from
    ``GET /v1/expected-move/{symbol}`` (Basic+).

    Top-level keys are snake_case; ``expected_moves`` items are camelCase.
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    expected_moves: List[ExpectedMoveItem]


# ─── Exposure Sheet ──────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/exposure/sheet/{symbol}`` (Growth+). Unified
# per-strike GEX/DEX/VEX/CHEX/DAG rowset + chain totals, Line-in-the-Sand
# inflection strike, all gamma peaks, and OPEX / triple-witching flags.


class ExposureSheetTotals(TypedDict, total=False):
    """Chain totals across all greeks plus DAG (delta-adjusted gamma)."""

    net_gex: Optional[float]
    net_dex: Optional[float]
    net_vex: Optional[float]
    net_chex: Optional[float]
    # Σ DAG = ``|delta| × gamma × OI × 100 × spot² × 0.01`` (puts sign-flipped).
    net_dag: Optional[float]


class ExposureSheetLis(TypedDict, total=False):
    """Line-in-the-Sand inflection strike (largest ``|d²(net_gex)/dK²|``).

    ``None`` (whole block) when the chain has <3 strikes or every second
    difference is zero. ``magnitude`` is currently always ``1.0`` (reserved).
    """

    strike: Optional[float]
    magnitude: Optional[float]


class ExposureSheetPeak(TypedDict, total=False):
    """One local maximum of ``|net_gex|`` (``strength ≥ 0.1``)."""

    strike: Optional[float]
    net_gex: Optional[float]
    # Fraction of max ``|net_gex|`` in the chain.
    strength: Optional[float]
    # ``"call_wall"`` when ``net_gex ≥ 0``, else ``"put_wall"``.
    side: Optional[str]


class ExposureSheetStrike(TypedDict, total=False):
    """One unified per-strike row joining all greeks + DAG + OI."""

    strike: Optional[float]
    call_gex: Optional[float]
    put_gex: Optional[float]
    net_gex: Optional[float]
    call_dex: Optional[float]
    put_dex: Optional[float]
    net_dex: Optional[float]
    call_vex: Optional[float]
    put_vex: Optional[float]
    net_vex: Optional[float]
    call_chex: Optional[float]
    put_chex: Optional[float]
    net_chex: Optional[float]
    # Per-strike DAG aggregated across calls + puts.
    dag: Optional[float]
    call_oi: Optional[int]
    put_oi: Optional[int]


class ExposureSheetResponse(TypedDict, total=False):
    """Unified exposure sheet from ``GET /v1/exposure/sheet/{symbol}`` (Growth+).

    ``is_opex`` / ``is_triple_witching`` are only meaningful when an
    ``expiration`` filter is supplied.
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    expiration: Optional[str]
    # True when ``expiration`` is the holiday-adjusted monthly OPEX.
    is_opex: Optional[bool]
    # True when ``is_opex`` AND month ∈ {Mar, Jun, Sep, Dec}.
    is_triple_witching: Optional[bool]
    totals: ExposureSheetTotals
    # ``None`` when not computable. See ``ExposureSheetLis``.
    lis: Optional[ExposureSheetLis]
    peaks: List[ExposureSheetPeak]
    strikes: List[ExposureSheetStrike]


# ─── Exposure Term Structure ─────────────────────────────────────────────────
#
# Typed model for ``GET /v1/exposure/term-structure/{symbol}`` (Growth+).
# Per-greek exposure aggregated by DTE bucket and rolled up per expiry.


class ExposureTermDteBucket(TypedDict, total=False):
    """One DTE bucket (``0-7d`` / ``8-30d`` / ``31-60d`` / ``61-180d`` /
    ``180d+``). Buckets with no contracts are omitted.
    """

    bucket: Optional[str]
    # Inclusive ``[lower, upper]`` DTE bounds (final bucket upper = int.Max).
    dte_range: List[int]
    net_gex: Optional[float]
    net_dex: Optional[float]
    net_vex: Optional[float]
    net_chex: Optional[float]
    contract_count: Optional[int]


class ExposureTermExpiry(TypedDict, total=False):
    """One per-expiry rollup row, ordered ascending by expiry."""

    expiration: Optional[str]
    dte: Optional[int]
    is_opex: Optional[bool]
    is_triple_witching: Optional[bool]
    net_gex: Optional[float]
    net_dex: Optional[float]
    net_vex: Optional[float]
    net_chex: Optional[float]
    # This expiry's ``|net_gex|`` as a share of chain ``Σ|net_gex|`` (0-100).
    pct_of_chain_gex: Optional[float]


class ExposureTermStructureResponse(TypedDict, total=False):
    """Exposure term structure from
    ``GET /v1/exposure/term-structure/{symbol}`` (Growth+).
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    by_dte_bucket: List[ExposureTermDteBucket]
    by_expiry: List[ExposureTermExpiry]


# ─── Exposure Basket ─────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/exposure/basket`` (Growth+). Weighted cross-symbol
# aggregate of GEX/DEX/VEX/CHEX across up to 50 user-supplied symbols.


class ExposureBasketAggregate(TypedDict, total=False):
    """``Σ wᵢ × net_{greek}_i`` after weight renormalisation."""

    net_gex: Optional[float]
    net_dex: Optional[float]
    net_vex: Optional[float]
    net_chex: Optional[float]


class ExposureBasketConstituent(TypedDict, total=False):
    """One basket constituent with its renormalised weight + contribution."""

    symbol: Optional[str]
    # Renormalised weight (sums to 1 across the response).
    weight: Optional[float]
    underlying_price: Optional[float]
    net_gex: Optional[float]
    net_dex: Optional[float]
    net_vex: Optional[float]
    net_chex: Optional[float]
    # ``|wᵢ × net_gex_i| / Σ|wⱼ × net_gex_j|`` (0-100, weighted GEX).
    contribution_pct: Optional[float]
    # ``"positive_gamma"`` when ``net_gex ≥ 0``, else ``"negative_gamma"``.
    regime: Optional[str]


class ExposureBasketResponse(TypedDict, total=False):
    """Weighted basket exposure from ``GET /v1/exposure/basket`` (Growth+).

    Symbols with no data are dropped, surviving weights re-normalised, and the
    dropped tickers reported in ``missing_symbols``.
    """

    as_of: str
    # Number of symbols that actually contributed (after drops).
    constituent_count: Optional[int]
    missing_symbols: List[str]
    aggregate: ExposureBasketAggregate
    constituents: List[ExposureBasketConstituent]


# ─── Exposure OI-Diff ────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/exposure/oi-diff/{symbol}`` (Growth+). Day-over-day
# open-interest deltas — fills the ``top_oi_changes`` placeholder on narrative.


class ExposureOiDiffRow(TypedDict, total=False):
    """One per-contract OI delta row (sorted by ``|oi_change|`` descending)."""

    strike: Optional[float]
    # ``"C"`` (call) or ``"P"`` (put).
    type: Optional[str]
    expiry: Optional[str]
    today_oi: Optional[int]
    prior_oi: Optional[int]
    # Signed: today's OI minus prior trading day's OI.
    oi_change: Optional[int]


class ExposureOiDiffResponse(TypedDict, total=False):
    """Day-over-day OI deltas from
    ``GET /v1/exposure/oi-diff/{symbol}`` (Growth+).

    When ``prior_snapshot_available`` is ``False`` the totals are ``0`` and
    ``top_oi_changes`` is empty.
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    prior_snapshot_available: Optional[bool]
    total_call_oi_change: Optional[int]
    total_put_oi_change: Optional[int]
    top_oi_changes: List[ExposureOiDiffRow]


# ─── Liquidity ───────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/liquidity/{symbol}`` (Growth+). Per-expiry
# execution score, spreads, ATM OI depth + chain-level roll-up.


class LiquidityExpiry(TypedDict, total=False):
    """One per-expiry liquidity row."""

    expiration: Optional[str]
    dte: Optional[int]
    # ATM bid-ask spread %; ``None`` when neither side quotes.
    atm_spread_pct: Optional[float]
    # OI-weighted spread %; ``None`` when no contract qualifies.
    weighted_spread_pct: Optional[float]
    # Sum of call+put OI at the strike closest to spot.
    atm_oi: Optional[int]
    # 0-100 composite execution score.
    execution_score: Optional[int]
    # ``"tight"`` (≥75) / ``"normal"`` (≥50) / ``"wide"`` (≥20) /
    # ``"illiquid"`` (<20).
    label: Optional[str]


class LiquidityResponse(TypedDict, total=False):
    """Chain liquidity from ``GET /v1/liquidity/{symbol}`` (Growth+)."""

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    # OI-weighted average of per-expiry ``execution_score`` (0-100).
    chain_execution_score: Optional[int]
    best_expiry: Optional[str]
    worst_expiry: Optional[str]
    # Number of expiries labelled ``illiquid``.
    thin_expiry_count: Optional[int]
    expiries: List[LiquidityExpiry]


# ─── Skew Term ───────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/volatility/skew-term/{symbol}`` (Growth+). Skew
# term structure with vol-desk naming conventions (skew/risk-reversal/butterfly).


class SkewTermExpiry(TypedDict, total=False):
    """One per-expiry skew row with the named conventions."""

    expiry: Optional[str]
    dte: Optional[int]
    atm_iv: Optional[float]
    put_25d_iv: Optional[float]
    call_25d_iv: Optional[float]
    put_10d_iv: Optional[float]
    call_10d_iv: Optional[float]
    # ``put_25d_iv − call_25d_iv``. Positive ⇒ put skew dominant.
    skew_25d: Optional[float]
    # ``call_25d_iv − put_25d_iv`` (= ``−skew_25d``). FX / vol-desk convention.
    risk_reversal_25d: Optional[float]
    # ``(call_25d_iv + put_25d_iv) / 2 − atm_iv``. Wing premium over ATM.
    butterfly_25d: Optional[float]
    # Second difference of the put wing. Positive ⇒ steep tail.
    tail_convexity: Optional[float]


class SkewTermResponse(TypedDict, total=False):
    """Skew term structure from
    ``GET /v1/volatility/skew-term/{symbol}`` (Growth+).
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    expiries: List[SkewTermExpiry]


# ─── Spot-Vol Correlation ────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/volatility/spot-vol-correlation/{symbol}`` (Growth+).


class SpotVolCorrelationResponse(TypedDict, total=False):
    """Spot-vol correlation from
    ``GET /v1/volatility/spot-vol-correlation/{symbol}`` (Growth+).

    Daily Pearson between spot log-returns and first-differences of ATM IV
    over 20-day and 60-day windows. Equity indices typically run strongly
    negative.
    """

    symbol: str
    as_of: str
    # ``None`` when variance is zero or fewer than 20 points exist.
    spot_vol_correlation_20d: Optional[float]
    spot_vol_correlation_60d: Optional[float]
    data_points_20d: Optional[int]
    data_points_60d: Optional[int]
    # Plain-English label keyed off the shorter window. Safe to surface.
    interpretation: Optional[str]


# ─── Realized Volatility ─────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/volatility/realized/{symbol}`` (Alpha+). Range-based
# realized (historical) vol estimators over 10/20/30-day windows.


class RealizedVolatilityEstimator(TypedDict, total=False):
    """One estimator's annualized realized vol (percent) by window length.

    Each field serialises as JSON ``null`` when there are too few observations
    in the window — treat ``None`` as "not computable."
    """

    rv10: Optional[float]
    rv20: Optional[float]
    rv30: Optional[float]


class RealizedVolatilityEstimators(TypedDict, total=False):
    """The five fixed range-based estimators, each keyed by window."""

    close_to_close: RealizedVolatilityEstimator
    parkinson: RealizedVolatilityEstimator
    garman_klass: RealizedVolatilityEstimator
    rogers_satchell: RealizedVolatilityEstimator
    yang_zhang: RealizedVolatilityEstimator


class RealizedVolatilityResponse(TypedDict, total=False):
    """Realized vol estimators from
    ``GET /v1/volatility/realized/{symbol}`` (Alpha+).

    All ``rvN`` values are annualized realized vol expressed in percent.
    """

    symbol: str
    as_of: str
    underlying_price: Optional[float]
    estimators: RealizedVolatilityEstimators


# ─── Volatility Forecast ─────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/volatility/forecast/{symbol}`` (Alpha+). Conditional
# vol forecasts via EWMA (λ=0.94), HAR-RV and GARCH(1,1) MLE.


class VolatilityForecastEwma(TypedDict, total=False):
    """EWMA block. ``lambda`` is the decay factor (0.94)."""

    lambda: float
    vol_annualized: Optional[float]
    next_day_forecast: Optional[float]


class VolatilityForecastHarComponents(TypedDict, total=False):
    """Daily / weekly / monthly HAR-RV component vols (annualized percent)."""

    daily: Optional[float]
    weekly: Optional[float]
    monthly: Optional[float]


class VolatilityForecastHar(TypedDict, total=False):
    """HAR-RV block."""

    vol_annualized: Optional[float]
    components: VolatilityForecastHarComponents
    next_day_forecast: Optional[float]


class VolatilityForecastGarchParams(TypedDict, total=False):
    """Fitted GARCH(1,1) parameters. ``dof`` is present only for ``student_t``."""

    omega: Optional[float]
    alpha: Optional[float]
    beta: Optional[float]
    dof: Optional[float]


class VolatilityForecastGarchPoint(TypedDict, total=False):
    """One GARCH multi-step forecast point (annualized percent)."""

    horizon_days: Optional[int]
    vol_annualized: Optional[float]


class VolatilityForecastGarch(TypedDict, total=False):
    """GARCH(1,1) block.

    ``forecast`` is ``None`` when the fit did not converge; ``params.dof`` is
    only populated for the ``student_t`` distribution.
    """

    model: Optional[str]
    distribution: Optional[str]
    params: VolatilityForecastGarchParams
    persistence: Optional[float]
    # ``None`` when persistence ≥ 1 (long-run vol undefined).
    long_run_vol_annualized: Optional[float]
    half_life_days: Optional[float]
    converged: Optional[bool]
    forecast: Optional[List[VolatilityForecastGarchPoint]]


class VolatilityForecastResponse(TypedDict, total=False):
    """Conditional vol forecasts from
    ``GET /v1/volatility/forecast/{symbol}`` (Alpha+).

    All vols are annualized and expressed in percent.
    """

    symbol: str
    as_of: str
    ewma: VolatilityForecastEwma
    har_rv: VolatilityForecastHar
    garch: VolatilityForecastGarch


# ─── Dispersion ──────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/dispersion`` (Alpha+). Implied vs realized
# correlation between an index and a user-supplied basket of constituents.


class DispersionContributor(TypedDict, total=False):
    """One constituent's contribution to basket vol (sorted descending)."""

    symbol: Optional[str]
    weight: Optional[float]
    # The constituent's ATM IV (decimal).
    iv: Optional[float]
    # ``wᵢ × σᵢ``. ``Σ contribution == implied_vol_basket`` by construction.
    contribution_to_basket_vol: Optional[float]


class DispersionResponse(TypedDict, total=False):
    """Implied-vs-realized correlation from ``GET /v1/dispersion`` (Alpha+).

    Correlation fields serialise as JSON ``null`` (not ``NaN``) when the
    underlying math is undefined — treat ``None`` as "not computable from
    this basket / window."
    """

    as_of: str
    index: Optional[str]
    constituent_count: Optional[int]
    missing_symbols: List[str]
    horizon_days: Optional[int]
    # Demeterfi-Derman-Kani implied correlation; ``None`` for degenerate basket.
    implied_correlation: Optional[float]
    # 1-factor realized correlation over the horizon; ``None`` when N/A.
    realized_correlation: Optional[float]
    # ``implied − realized``. Positive ⇒ market pricing in more correlation.
    correlation_premium: Optional[float]
    # Index ATM IV (decimal).
    implied_vol_index: Optional[float]
    # ``Σ wᵢ σᵢ`` after weight renormalisation.
    implied_vol_basket: Optional[float]
    top_contributors: List[DispersionContributor]


# ─── VIX State ───────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/macro/vix-state`` (Growth+). "overvixing /
# undervixing" regime — VIX vs SPX 20-day realized vol.


class VixStateResponse(TypedDict, total=False):
    """VIX-state regime from ``GET /v1/macro/vix-state`` (Growth+)."""

    as_of: str
    # VIX spot.
    vix: Optional[float]
    # SPX 20-day annualised realized vol (%).
    spx_rv_20d: Optional[float]
    # ``vix − spx_rv_20d`` (vol points).
    spread: Optional[float]
    # ``vix / spx_rv_20d``. ``None`` when ``spx_rv_20d == 0``.
    ratio: Optional[float]
    # ``"overvixing"`` (spread ≥ 5) / ``"undervixing"`` (≤ 0) / ``"neutral"``.
    state: Optional[str]
    # Plain-English label. Safe to surface verbatim.
    interpretation: Optional[str]


# ─── Universe ────────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/universe`` (public). Curated tier-1 / tier-2
# symbol directory the screener loop keeps pre-warmed.


class UniverseSymbol(TypedDict, total=False):
    """One universe symbol with its tier + pre-warm flag."""

    symbol: Optional[str]
    # 1 = high-traffic loop (fast refresh); 2 = remaining curated symbols.
    tier: Optional[int]
    # Currently always ``True`` — the screener loop keeps members populated.
    is_pre_warmed: Optional[bool]


class UniverseResponse(TypedDict, total=False):
    """Curated symbol universe from ``GET /v1/universe`` (public)."""

    as_of: str
    # Total universe size (tier-1 ∪ tier-2, deduplicated).
    count: Optional[int]
    # ``min(count, limit)``.
    returned: Optional[int]
    limit: Optional[int]
    # Echoes the effective sort (unknown values fall back to ``"tier"``).
    sort: Optional[str]
    symbols: List[UniverseSymbol]


# ─── Flow Dealer Premium ─────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/flow/options/{symbol}/dealer-premium`` (Alpha+).
# Full-tape Net Dealer Premium roll-up over a configurable window.


class FlowDealerPremiumResponse(TypedDict, total=False):
    """Net Dealer Premium from
    ``GET /v1/flow/options/{symbol}/dealer-premium`` (Alpha+).
    """

    symbol: str
    as_of: str
    window_minutes: int
    # Expiration filter echoed back, or ``None``.
    expiry: Optional[str]
    # ``Σ (sellVolume × vwap × 100)`` — dealer BUYS when customer hits the bid.
    dealer_buy_premium: Optional[float]
    # ``Σ (buyVolume × vwap × 100)`` — dealer WRITES when customer lifts the ask.
    dealer_write_premium: Optional[float]
    # ``dealer_buy_premium − dealer_write_premium``. Positive ⇒ dealers net long.
    net_dealer_premium: Optional[float]
    # ``dealer_buy_premium + dealer_write_premium`` (excludes mid prints).
    total_premium: Optional[float]
    trade_count: Optional[int]
    bucket_count: Optional[int]


# ─── Zero-DTE Flow ───────────────────────────────────────────────────────────
#
# Typed models for the five ``GET /v1/flow/zero-dte/*`` endpoints. The
# snapshot reuses the full ``ZeroDteResponse`` fields plus a ``flow_direction``
# block; the series/hedge-flow/heatmap/strike-flow endpoints are intraday
# time-series wrappers with empty-``bars`` degraded shapes.


class ZeroDteFlowDirection(TypedDict, total=False):
    """Live flow-adjustment block appended to the 0DTE snapshot."""

    # ``"no_flow"`` / ``"neutral"`` / ``"amplifying"`` / ``"dampening"`` /
    # ``"regime_flip"``.
    label: Optional[str]
    settled_net_gex: Optional[float]
    live_net_gex: Optional[float]
    flow_gex_adjustment: Optional[float]
    # ``None`` when settled GEX is 0.
    flow_gex_pct_shift: Optional[float]
    contracts_with_flow: Optional[int]
    total_abs_delta_contracts: Optional[int]
    description: Optional[str]


class FlowZeroDteSnapshotResponse(TypedDict, total=False):
    """Live 0DTE snapshot from
    ``GET /v1/flow/zero-dte/snapshot/{symbol}`` (Growth+).

    Same shape as ``ZeroDteResponse`` (regime, exposures, expected_move,
    pin_risk, hedging, decay, vol_context, flow, levels, liquidity, strikes)
    PLUS a ``flow_direction`` block. Degraded shapes set ``no_zero_dte`` or
    ``session_closed`` to ``True``.
    """

    symbol: str
    underlying_price: Optional[float]
    as_of: str
    market_open: Optional[bool]
    regime: ZeroDteRegime
    exposures: ZeroDteExposures
    expected_move: ZeroDteExpectedMove
    pin_risk: ZeroDtePinRisk
    hedging: ZeroDteHedging
    decay: ZeroDteDecay
    vol_context: ZeroDteVolContext
    flow: ZeroDteFlow
    levels: ZeroDteLevels
    liquidity: ZeroDteLiquidity
    metadata: ZeroDteMetadata
    strikes: List[ZeroDteStrike]
    # Live flow-adjustment block.
    flow_direction: ZeroDteFlowDirection
    # ── Degraded shapes ──
    no_zero_dte: bool
    session_closed: bool
    last_session: Optional[str]
    next_zero_dte_expiry: Optional[str]
    message: str


class FlowZeroDteSeriesBar(TypedDict, total=False):
    """One downsampled bar of the 0DTE series."""

    # Bar timestamp (UTC, snapped to :00/:30 ET upstream).
    t: str
    spot: Optional[float]
    net_gex: Optional[float]
    net_dex: Optional[float]
    gamma_flip: Optional[float]
    call_wall: Optional[float]
    put_wall: Optional[float]
    magnet: Optional[float]
    pin_score: Optional[int]
    pin_probability_pct: Optional[float]
    regime: Optional[str]
    atm_iv: Optional[float]
    charm_dollars_per_hour: Optional[float]
    # $-units, cumulative since session open.
    hedge_flow_call_cumulative: Optional[float]
    hedge_flow_put_cumulative: Optional[float]
    hedge_flow_cumulative_all: Optional[float]


class FlowZeroDteSeriesResponse(TypedDict, total=False):
    """Intraday 0DTE series from
    ``GET /v1/flow/zero-dte/series/{symbol}`` (Growth+).

    No samples in the window returns ``200`` with an empty ``bars`` array.
    """

    symbol: str
    # Today's 0DTE expiry being sampled.
    expiration: Optional[str]
    as_of: str
    # Echoes the requested bar (``30s`` / ``1m`` / ``5m`` / ``15m``).
    bar_size: Optional[str]
    bars: List[FlowZeroDteSeriesBar]


class FlowZeroDteHedgeFlowBar(TypedDict, total=False):
    """One bar of the 0DTE hedge-flow series."""

    t: str
    # Per-bar signed delta-dollars in this bucket.
    bar: Optional[float]
    # Running sum since session open (for the requested ``side``).
    cumulative: Optional[float]


class FlowZeroDteHedgeFlowResponse(TypedDict, total=False):
    """0DTE dealer hedge-flow from
    ``GET /v1/flow/zero-dte/hedge-flow/{symbol}`` (Growth+).
    """

    symbol: str
    expiration: Optional[str]
    as_of: str
    # Echoes the requested side (``all`` / ``calls`` / ``puts``).
    side: Optional[str]
    bar_size: Optional[str]
    bars: List[FlowZeroDteHedgeFlowBar]


class FlowZeroDteHeatmapBar(TypedDict, total=False):
    """One bar of the 0DTE heatmap; ``values`` is index-aligned to
    ``strikes_grid``.
    """

    t: str
    spot: Optional[float]
    # ``values[i]`` is the metric for ``strikes_grid[i]``.
    values: List[float]


class FlowZeroDteHeatmapResponse(TypedDict, total=False):
    """Per-strike 0DTE heatmap from
    ``GET /v1/flow/zero-dte/heatmap/{symbol}`` (Alpha+).

    No samples returns ``200`` with empty ``strikes_grid`` and ``bars``.
    """

    symbol: str
    underlying_price: Optional[float]
    expiration: Optional[str]
    # Echoes the requested metric (``gex``/``dex``/``vex``/``chex``/``oi``/
    # ``signed_flow``).
    metric: Optional[str]
    # Echoes the requested mode (``raw`` / ``delta``).
    mode: Optional[str]
    bar_size: Optional[str]
    as_of: str
    tier_used: Optional[str]
    strikes_grid: List[float]
    bars: List[FlowZeroDteHeatmapBar]
    # Reserved for sampler-gap intervals; not yet populated.
    gap_intervals: List[Any]


class FlowZeroDteStrikeFlowBar(TypedDict, total=False):
    """One bar of per-strike signed aggressor flow (arrays index-aligned to
    ``strikes_grid``).
    """

    t: str
    spot: Optional[float]
    # Per strike, per-bar increments (not cumulative).
    signed_delta_dollars: List[float]
    signed_gamma_dollars: List[float]
    contracts: List[int]


class FlowZeroDteStrikeFlowResponse(TypedDict, total=False):
    """Per-strike 0DTE signed flow from
    ``GET /v1/flow/zero-dte/strike-flow/{symbol}`` (Alpha+).
    """

    symbol: str
    underlying_price: Optional[float]
    expiration: Optional[str]
    bar_size: Optional[str]
    as_of: str
    tier_used: Optional[str]
    strikes_grid: List[float]
    bars: List[FlowZeroDteStrikeFlowBar]
    gap_intervals: List[Any]


class FlowZeroDteLeaderboardEntry(TypedDict, total=False):
    """One ranked symbol in the cross-symbol 0DTE leaderboard."""

    rank: int
    symbol: str
    # Value of the requested ``metric`` for this symbol.
    value: float


class FlowZeroDteLeaderboardResponse(TypedDict, total=False):
    """Cross-symbol 0DTE leaderboard from
    ``GET /v1/flow/zero-dte/leaderboard`` (Alpha+).

    Ranks the curated universe by the requested ``metric``
    (``heat`` / ``pin_risk`` / ``abs_flow`` / ``charm_intensity``).
    """

    # Echoes the requested metric.
    metric: str
    # Echoes the requested number of entries.
    n: int
    as_of: str
    market_open: bool
    entries: List[FlowZeroDteLeaderboardEntry]


# ─── Flow Stock Bars ─────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/flow/stocks/{symbol}/bars`` (Alpha+).
# Multi-resolution OHLCV+flow bars, oldest-first, camelCase wire keys.


class FlowStockBar(TypedDict, total=False):
    """One OHLCV+flow bar (camelCase wire keys, oldest-first)."""

    # Bar start (UTC).
    ts: str
    # ``True`` once the bar is final; right-edge bar is typically ``False``.
    closed: bool
    open: float
    high: float
    low: float
    close: float
    vwap: float
    buyVolume: int
    sellVolume: int
    midVolume: int
    netVolume: int
    tradeCount: int
    biggestTrade: int


class FlowStockBarsResponse(TypedDict, total=False):
    """Multi-resolution stock bars from
    ``GET /v1/flow/stocks/{symbol}/bars`` (Alpha+).

    Bars are oldest-first (contrast ``/history``, newest-first).
    """

    symbol: str
    # Echo of the requested resolution.
    resolution: str
    minutes: int
    count: int
    # Oldest 1-second bucket in the ring (UTC), or ``None`` when no history.
    dataStartUtc: Optional[str]
    bars: List[FlowStockBar]


# ─── VRP History ─────────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/vrp/{symbol}/history`` (Alpha+). Daily VRP time
# series for charting and backtesting.


class VrpHistoryRow(TypedDict, total=False):
    """One daily VRP snapshot row."""

    # Snapshot date (``"yyyy-MM-dd"``).
    date: Optional[str]
    # Close price.
    spot: Optional[float]
    atm_iv: Optional[float]
    rv_5d: Optional[float]
    rv_10d: Optional[float]
    rv_20d: Optional[float]
    rv_30d: Optional[float]
    # VRP spread (``atm_iv − rv_20d``).
    vrp_20d: Optional[float]
    # ATM straddle price ($).
    straddle: Optional[float]
    # 1-day expected move ($).
    expected_move_1d: Optional[float]


class VrpHistoryResponse(TypedDict, total=False):
    """Daily VRP time series from ``GET /v1/vrp/{symbol}/history`` (Alpha+)."""

    symbol: str
    # Requested lookback.
    days: Optional[int]
    data_points: Optional[int]
    history: List[VrpHistoryRow]


# ─── Screener Fields ─────────────────────────────────────────────────────────
#
# Typed model for ``GET /v1/screener/fields`` (any authenticated tier).


class ScreenerField(TypedDict, total=False):
    """One queryable screener field with its value type."""

    name: Optional[str]
    # Value type used by the filter/sort engine (e.g. ``"number"``,
    # ``"string"``).
    type: Optional[str]


class ScreenerFieldsResponse(TypedDict, total=False):
    """Queryable screener fields from ``GET /v1/screener/fields``.

    Fields are returned sorted by ``name``.
    """

    fields: List[ScreenerField]
    count: Optional[int]
