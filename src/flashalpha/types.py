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
# Direction casing: /v1/exposure/summary/ and /v1/exposure/zero-dte/ both
# return lowercase "buy" / "sell". Docs and typed models use that casing
# consistently.


class ExposureSummaryExposures(TypedDict, total=False):
    # Field-level Optional matches C#/Go/Java (defensive — API may return null
    # under unobserved edge conditions even when the parent block is present).
    net_gex: Optional[float]
    net_dex: Optional[float]
    net_vex: Optional[float]
    net_chex: Optional[float]


class ExposureSummaryInterpretation(TypedDict, total=False):
    gamma: Optional[str]
    vanna: Optional[str]
    charm: Optional[str]


class ExposureSummaryHedgingMove(TypedDict, total=False):
    dealer_shares_to_trade: Optional[float]
    direction: Optional[Literal["buy", "sell"]]
    notional_usd: Optional[float]


class ExposureSummaryHedgingEstimate(TypedDict, total=False):
    spot_up_1pct: ExposureSummaryHedgingMove
    spot_down_1pct: ExposureSummaryHedgingMove


class ExposureSummaryZeroDte(TypedDict, total=False):
    net_gex: Optional[float]
    pct_of_total_gex: Optional[float]
    expiration: Optional[str]


class ExposureSummaryResponse(TypedDict, total=False):
    symbol: str
    underlying_price: Optional[float]
    as_of: str
    gamma_flip: Optional[float]
    # Confirmed live values in tests across Py/JS/.NET/Go/Java:
    #   positive_gamma | negative_gamma | neutral
    # Documented fourth value: undetermined (when there's no usable options
    # data). `neutral` appears in edge cases where net_gex straddles zero.
    # Don't conflate with ``maxpain.signal`` (also bullish/bearish/neutral but
    # a separate field).
    regime: Literal["positive_gamma", "negative_gamma", "neutral", "undetermined"]
    exposures: ExposureSummaryExposures
    interpretation: ExposureSummaryInterpretation
    hedging_estimate: ExposureSummaryHedgingEstimate
    zero_dte: ExposureSummaryZeroDte
