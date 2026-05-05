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

from typing import List, Literal, Optional, TypedDict


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
    #   - ``"neutral"``: spot within ~1% of flip and net_gex straddles zero
    #   - ``"undetermined"``: insufficient options data to compute a flip
    # Confirmed live values across Py/JS/.NET/Go/Java integration tests.
    # Don't conflate with ``maxpain.signal`` (a separate
    # bullish/bearish/neutral classifier on a different endpoint).
    regime: Literal["positive_gamma", "negative_gamma", "neutral", "undetermined"]
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
    # ``"neutral"`` (when net_gex straddles zero).
    regime: Optional[str]
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

    # ``"positive_gamma"`` | ``"negative_gamma"`` | ``"neutral"`` |
    # ``"undetermined"`` — same classifier as exposure_summary.
    gamma: Optional[str]
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
