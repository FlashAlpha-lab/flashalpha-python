"""FlashAlpha API client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

import requests

from .exceptions import (
    AuthenticationError,
    FlashAlphaError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TierRestrictedError,
)

if TYPE_CHECKING:
    from .types import (
        AccountResponse,
        AdvVolatilityResponse,
        ChexResponse,
        DexResponse,
        DispersionResponse,
        EarningsCalendarResponse,
        EarningsDealerPositioningResponse,
        EarningsExpectedMoveResponse,
        EarningsHistoryResponse,
        EarningsIvCrushResponse,
        EarningsScreenerResponse,
        EarningsStrategiesResponse,
        EarningsVrpResponse,
        ExpectedMoveResponse,
        ExposureBasketResponse,
        ExposureLevelsResponse,
        ExposureOiDiffResponse,
        ExposureSheetResponse,
        ExposureSummaryResponse,
        ExposureTermStructureResponse,
        FlowDealerPremiumResponse,
        FlowDealerRiskResponse,
        FlowDexResponse,
        FlowGexResponse,
        FlowLevelsResponse,
        FlowLiveResponse,
        FlowOiResponse,
        FlowOptionBlocksResponse,
        FlowOptionCumulativeResponse,
        FlowOptionHistoryResponse,
        FlowOptionLeaderboardResponse,
        FlowOptionOutliersResponse,
        FlowOptionRecentResponse,
        FlowOptionSummaryResponse,
        FlowPinRiskResponse,
        FlowSignalsResponse,
        FlowSignalsSummaryResponse,
        FlowStockBlocksResponse,
        FlowStockCumulativeResponse,
        FlowStockHistoryResponse,
        FlowStockLeaderboardResponse,
        FlowStockBarsResponse,
        FlowStockOutliersResponse,
        FlowStockRecentResponse,
        FlowStockSummaryResponse,
        FlowSummaryResponse,
        FlowZeroDteHedgeFlowResponse,
        FlowZeroDteHeatmapResponse,
        FlowZeroDteSeriesResponse,
        FlowZeroDteSnapshotResponse,
        FlowZeroDteStrikeFlowResponse,
        GexResponse,
        HealthResponse,
        LiquidityResponse,
        MaxPainResponse,
        NarrativeResponse,
        OptionQuoteResponse,
        OptionsMetaResponse,
        PricingGreeksResponse,
        PricingIvResponse,
        PricingKellyResponse,
        RealizedVolatilityResponse,
        ScreenerFieldsResponse,
        ScreenerResponse,
        SkewTermResponse,
        SpotVolCorrelationResponse,
        StockQuoteResponse,
        StockSummaryResponse,
        StrategyDecisionResponse,
        StructureGreeksResponse,
        StructurePnlResponse,
        SurfaceResponse,
        SurfaceSviResponse,
        SymbolsResponse,
        TickersResponse,
        UniverseResponse,
        VexResponse,
        VixStateResponse,
        VolatilityForecastResponse,
        VolatilityResponse,
        VrpHistoryResponse,
        VrpResponse,
        ZeroDteResponse,
    )

BASE_URL = "https://lab.flashalpha.com"


def _seg(s: str) -> str:
    """URL-escape a single path segment (e.g. a ticker) — escapes / ? % etc."""
    return quote(s, safe="")


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

    def _post(self, path: str, json_body: dict[str, Any] | None = None) -> dict:
        url = f"{self.base_url}{path}"
        resp = self._session.post(url, json=json_body, timeout=self.timeout)
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

    def stock_quote(self, ticker: str) -> StockQuoteResponse:
        """Live stock quote (bid/ask/mid/last)."""
        return self._get(f"/stockquote/{_seg(ticker)}")

    def option_quote(
        self,
        ticker: str,
        *,
        expiry: str | None = None,
        strike: float | None = None,
        type: str | None = None,
    ) -> OptionQuoteResponse | list[OptionQuoteResponse]:
        """Option quotes with greeks. Requires Growth+.

        Returns a single ``OptionQuoteResponse`` when the request fully
        specifies one contract (all of ``expiry``, ``strike``, ``type``);
        otherwise returns a list of ``OptionQuoteResponse``.
        """
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        if strike is not None:
            params["strike"] = strike
        if type:
            params["type"] = type
        return self._get(f"/optionquote/{_seg(ticker)}", params or None)

    def surface(self, symbol: str) -> SurfaceResponse:
        """Volatility surface grid (public, no auth required)."""
        return self._get(f"/v1/surface/{_seg(symbol)}")

    def surface_svi(self, symbol: str) -> SurfaceSviResponse:
        """Live SVI-fitted vol surface — calibrated (a, b, rho, m, sigma) per
        expiry slice with ATM total variance and ATM IV. Requires Alpha+."""
        return self._get(f"/v1/surface/svi/{_seg(symbol)}")

    def stock_summary(self, symbol: str) -> StockSummaryResponse:
        """Comprehensive stock summary (price, vol, exposure, macro)."""
        return self._get(f"/v1/stock/{_seg(symbol)}/summary")

    # ── Historical ──────────────────────────────────────────────────

    def historical_stock_quote(self, ticker: str, *, date: str, time: str | None = None) -> dict:
        """Historical stock quotes (minute-by-minute from ClickHouse)."""
        params: dict[str, Any] = {"date": date}
        if time:
            params["time"] = time
        return self._get(f"/historical/stockquote/{_seg(ticker)}", params)

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
        return self._get(f"/historical/optionquote/{_seg(ticker)}", params)

    # ── Exposure Analytics ──────────────────────────────────────────

    def gex(self, symbol: str, *, expiration: str | None = None, min_oi: int | None = None) -> GexResponse:
        """Gamma exposure by strike."""
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        if min_oi is not None:
            params["min_oi"] = min_oi
        return self._get(f"/v1/exposure/gex/{_seg(symbol)}", params or None)

    def dex(self, symbol: str, *, expiration: str | None = None) -> DexResponse:
        """Delta exposure by strike."""
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        return self._get(f"/v1/exposure/dex/{_seg(symbol)}", params or None)

    def vex(self, symbol: str, *, expiration: str | None = None) -> VexResponse:
        """Vanna exposure by strike."""
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        return self._get(f"/v1/exposure/vex/{_seg(symbol)}", params or None)

    def chex(self, symbol: str, *, expiration: str | None = None) -> ChexResponse:
        """Charm exposure by strike."""
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        return self._get(f"/v1/exposure/chex/{_seg(symbol)}", params or None)

    def exposure_summary(self, symbol: str) -> ExposureSummaryResponse:
        """Full exposure summary (GEX/DEX/VEX/CHEX + hedging). Requires Growth+."""
        return self._get(f"/v1/exposure/summary/{_seg(symbol)}")

    def exposure_levels(self, symbol: str) -> ExposureLevelsResponse:
        """Key support/resistance levels from options exposure."""
        return self._get(f"/v1/exposure/levels/{_seg(symbol)}")

    def narrative(self, symbol: str) -> NarrativeResponse:
        """Verbal narrative analysis of exposure. Requires Growth+."""
        return self._get(f"/v1/exposure/narrative/{_seg(symbol)}")

    def zero_dte(
        self,
        symbol: str,
        *,
        strike_range: float | None = None,
        expiry: str | None = None,
    ) -> ZeroDteResponse:
        """Real-time 0DTE analytics: regime, expected move, pin risk, hedging, decay. Requires Growth+.

        Returns a ``ZeroDteResponse`` (a ``TypedDict`` — runtime-equivalent to
        ``dict``). Existing ``result["field"]`` access continues to work; new
        callers get autocomplete and type-checking on the documented fields.

        ``expiry`` (``"YYYY-MM-DD"``) targets a specific same-day-style expiry
        (1DTE / 2DTE / any expiry) via the same 0DTE selector; omit for today's
        same-day expiry. ``strike_range`` (0.001–0.10) bounds the per-strike
        array only — aggregates always use the full chain.
        """
        params: dict[str, Any] = {}
        if strike_range is not None:
            params["strike_range"] = strike_range
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/exposure/zero-dte/{_seg(symbol)}", params or None)

    def exposure_sheet(
        self, symbol: str, *, expiration: str | None = None, min_oi: int | None = None
    ) -> ExposureSheetResponse:
        """Unified per-strike GEX/DEX/VEX/CHEX/DAG rowset + chain totals,
        Line-in-the-Sand strike, gamma peaks, and OPEX flags. Requires Growth+."""
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        if min_oi is not None:
            params["min_oi"] = min_oi
        return self._get(f"/v1/exposure/sheet/{_seg(symbol)}", params or None)

    def exposure_term_structure(self, symbol: str) -> ExposureTermStructureResponse:
        """Per-greek exposure aggregated by DTE bucket and rolled up per expiry.
        Requires Growth+."""
        return self._get(f"/v1/exposure/term-structure/{_seg(symbol)}")

    def exposure_basket(
        self, symbols: str | list[str], *, weights: str | list[float] | None = None
    ) -> ExposureBasketResponse:
        """Weighted cross-symbol aggregate of GEX/DEX/VEX/CHEX over up to 50
        symbols. Pass ``symbols`` as a comma string or list; equal-weighted when
        ``weights`` is omitted. Requires Growth+."""
        if isinstance(symbols, (list, tuple)):
            symbols = ",".join(str(s) for s in symbols)
        params: dict[str, Any] = {"symbols": symbols}
        if weights is not None:
            if isinstance(weights, (list, tuple)):
                weights = ",".join(str(w) for w in weights)
            params["weights"] = weights
        return self._get("/v1/exposure/basket", params)

    def exposure_oi_diff(self, symbol: str, *, top_n: int | None = None) -> ExposureOiDiffResponse:
        """Day-over-day open-interest deltas — per-contract changes, top-N by
        absolute magnitude, and call/put aggregate totals. Requires Growth+."""
        params: dict[str, Any] = {}
        if top_n is not None:
            params["topN"] = top_n
        return self._get(f"/v1/exposure/oi-diff/{_seg(symbol)}", params or None)

    # ── Volatility / Liquidity (additional) ─────────────────────────

    def liquidity(self, symbol: str) -> LiquidityResponse:
        """Per-expiry execution score, ATM/OI-weighted spreads, ATM OI depth,
        and chain-level liquidity roll-up. Requires Growth+."""
        return self._get(f"/v1/liquidity/{_seg(symbol)}")

    def skew_term(self, symbol: str) -> SkewTermResponse:
        """Per-expiry 25-delta skew and risk-reversal term structure. Requires Growth+."""
        return self._get(f"/v1/volatility/skew-term/{_seg(symbol)}")

    def spot_vol_correlation(self, symbol: str) -> SpotVolCorrelationResponse:
        """Daily Pearson correlation between spot returns and ATM-IV changes over
        20d/60d windows. Requires Growth+."""
        return self._get(f"/v1/volatility/spot-vol-correlation/{_seg(symbol)}")

    def dispersion(
        self,
        *,
        index: str,
        symbols: str | list[str],
        weights: str | list[float] | None = None,
        horizon_days: int | None = None,
    ) -> DispersionResponse:
        """Implied-vs-realized correlation between an ``index`` and a basket of
        ``symbols`` (dispersion / vol-arb). Returns the correlation premium and
        per-constituent contribution to basket vol. Requires Alpha+."""
        if isinstance(symbols, (list, tuple)):
            symbols = ",".join(str(s) for s in symbols)
        params: dict[str, Any] = {"index": index, "symbols": symbols}
        if weights is not None:
            if isinstance(weights, (list, tuple)):
                weights = ",".join(str(w) for w in weights)
            params["weights"] = weights
        if horizon_days is not None:
            params["horizon_days"] = horizon_days
        return self._get("/v1/dispersion", params)

    # ── Macro / Universe ────────────────────────────────────────────

    def vix_state(self) -> VixStateResponse:
        """Over/under-vixing regime label — spot VIX vs. SPX 20-day realized vol.
        Requires Growth+."""
        return self._get("/v1/macro/vix-state")

    def universe(self, *, sort: str | None = None, limit: int | None = None) -> UniverseResponse:
        """Curated tier-1 / tier-2 symbol directory (the pre-warmed screener
        universe). Public — no auth required."""
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort
        if limit is not None:
            params["limit"] = limit
        return self._get("/v1/universe", params or None)

    # ── Flow (live, simulation-aware) — requires the Alpha plan ──────
    #
    # Analytics endpoints (snake_case wire shape) fold today's intraday
    # trade tape into the settled book. All accept an optional
    # ``expiry="YYYY-MM-DD"`` to slice to a single expiration cycle.

    def flow_levels(self, symbol: str, *, expiry: str | None = None) -> FlowLevelsResponse:
        """Live gamma flip / call & put walls / max pain. Requires Alpha."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/levels/{_seg(symbol)}", params or None)

    def flow_pin_risk(self, symbol: str, *, expiry: str | None = None) -> FlowPinRiskResponse:
        """0DTE pin-risk score + component breakdown. Requires Alpha."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/pin-risk/{_seg(symbol)}", params or None)

    def flow_summary(self, symbol: str, *, expiry: str | None = None) -> FlowSummaryResponse:
        """At-a-glance flow direction + headline GEX shift. Requires Alpha."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/summary/{_seg(symbol)}", params or None)

    def flow_oi(self, symbol: str, *, expiry: str | None = None) -> FlowOiResponse:
        """Open-interest simulator state (official vs intraday). Requires Alpha."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/oi/{_seg(symbol)}", params or None)

    def flow_gex(self, symbol: str, *, expiry: str | None = None) -> FlowGexResponse:
        """Live (flow-adjusted) GEX + per-strike profile. Requires Alpha."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/gex/{_seg(symbol)}", params or None)

    def flow_dex(self, symbol: str, *, expiry: str | None = None) -> FlowDexResponse:
        """Live (flow-adjusted) DEX + per-strike profile. Requires Alpha."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/dex/{_seg(symbol)}", params or None)

    def flow_dealer_risk(self, symbol: str, *, expiry: str | None = None) -> FlowDealerRiskResponse:
        """Settled-vs-live dealer GEX/DEX + flow adjustment. Requires Alpha."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/dealer-risk/{_seg(symbol)}", params or None)

    def flow_live(self, symbol: str, *, expiry: str | None = None) -> FlowLiveResponse:
        """Everything-at-once live flow bundle (convenience). Requires Alpha."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/live/{_seg(symbol)}", params or None)

    # Raw flow data (camelCase wire shape) — proxied trade tape.

    def flow_option_recent(
        self, symbol: str, *, limit: int | None = None, expiry: str | None = None
    ) -> FlowOptionRecentResponse:
        """Recent option trades, newest-first (``limit`` 1–500). Requires Alpha."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/options/{_seg(symbol)}/recent", params or None)

    def flow_option_summary(
        self, symbol: str, *, expiry: str | None = None
    ) -> FlowOptionSummaryResponse:
        """Per-underlying option-flow aggregates. Requires Alpha."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/options/{_seg(symbol)}/summary", params or None)

    def flow_option_blocks(
        self, symbol: str, *, min_size: int | None = None, expiry: str | None = None
    ) -> FlowOptionBlocksResponse:
        """Large option prints (``size >= min_size``). Requires Alpha."""
        params: dict[str, Any] = {}
        if min_size is not None:
            params["minSize"] = min_size
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/options/{_seg(symbol)}/blocks", params or None)

    def flow_option_history(
        self, symbol: str, *, minutes: int | None = None, expiry: str | None = None
    ) -> FlowOptionHistoryResponse:
        """Per-minute option-flow buckets (``minutes`` 1–10080). Requires Alpha."""
        params: dict[str, Any] = {}
        if minutes is not None:
            params["minutes"] = minutes
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/options/{_seg(symbol)}/history", params or None)

    def flow_option_cumulative(
        self, symbol: str, *, minutes: int | None = None, expiry: str | None = None
    ) -> FlowOptionCumulativeResponse:
        """Cumulative option net-flow series. Requires Alpha."""
        params: dict[str, Any] = {}
        if minutes is not None:
            params["minutes"] = minutes
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/options/{_seg(symbol)}/cumulative", params or None)

    def flow_stock_recent(
        self, symbol: str, *, limit: int | None = None
    ) -> FlowStockRecentResponse:
        """Recent stock trades, newest-first (``limit`` 1–500). Requires Alpha."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        return self._get(f"/v1/flow/stocks/{_seg(symbol)}/recent", params or None)

    def flow_stock_summary(self, symbol: str) -> FlowStockSummaryResponse:
        """Per-symbol stock-flow aggregates. Requires Alpha."""
        return self._get(f"/v1/flow/stocks/{_seg(symbol)}/summary")

    def flow_stock_blocks(
        self, symbol: str, *, min_size: int | None = None
    ) -> FlowStockBlocksResponse:
        """Large stock prints (``size >= min_size``). Requires Alpha."""
        params: dict[str, Any] = {}
        if min_size is not None:
            params["minSize"] = min_size
        return self._get(f"/v1/flow/stocks/{_seg(symbol)}/blocks", params or None)

    def flow_stock_history(
        self, symbol: str, *, minutes: int | None = None
    ) -> FlowStockHistoryResponse:
        """Per-minute stock-flow buckets w/ OHLC (``minutes`` 1–10080). Requires Alpha."""
        params: dict[str, Any] = {}
        if minutes is not None:
            params["minutes"] = minutes
        return self._get(f"/v1/flow/stocks/{_seg(symbol)}/history", params or None)

    def flow_stock_cumulative(
        self, symbol: str, *, minutes: int | None = None
    ) -> FlowStockCumulativeResponse:
        """Cumulative stock net-flow series. Requires Alpha."""
        params: dict[str, Any] = {}
        if minutes is not None:
            params["minutes"] = minutes
        return self._get(f"/v1/flow/stocks/{_seg(symbol)}/cumulative", params or None)

    def flow_stock_bars(
        self, symbol: str, *, resolution: str, minutes: int | None = None
    ) -> FlowStockBarsResponse:
        """Multi-resolution OHLCV+flow bars from the live trade tape, oldest-first.
        ``resolution`` (required) ∈ {1s,1m,5m,15m,30m,1h,4h}. Requires Alpha+."""
        params: dict[str, Any] = {"resolution": resolution}
        if minutes is not None:
            params["minutes"] = minutes
        return self._get(f"/v1/flow/stocks/{_seg(symbol)}/bars", params)

    def flow_options_leaderboard(
        self, *, n: int | None = None, window_minutes: int | None = None
    ) -> FlowOptionLeaderboardResponse:
        """Cross-symbol option-flow leaderboard (top ``n`` by net $). Requires Alpha."""
        params: dict[str, Any] = {}
        if n is not None:
            params["n"] = n
        if window_minutes is not None:
            params["windowMinutes"] = window_minutes
        return self._get("/v1/flow/options/leaderboard", params or None)

    def flow_options_outliers(
        self,
        *,
        limit: int | None = None,
        min_trades: int | None = None,
        window_minutes: int | None = None,
    ) -> FlowOptionOutliersResponse:
        """Cross-symbol option-flow outliers (imbalance-ranked). Requires Alpha."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if min_trades is not None:
            params["minTrades"] = min_trades
        if window_minutes is not None:
            params["windowMinutes"] = window_minutes
        return self._get("/v1/flow/options/outliers", params or None)

    def flow_stocks_leaderboard(
        self, *, n: int | None = None, window_minutes: int | None = None
    ) -> FlowStockLeaderboardResponse:
        """Cross-symbol stock-flow leaderboard (top ``n`` by net $). Requires Alpha."""
        params: dict[str, Any] = {}
        if n is not None:
            params["n"] = n
        if window_minutes is not None:
            params["windowMinutes"] = window_minutes
        return self._get("/v1/flow/stocks/leaderboard", params or None)

    def flow_stocks_outliers(
        self,
        *,
        limit: int | None = None,
        min_trades: int | None = None,
        window_minutes: int | None = None,
    ) -> FlowStockOutliersResponse:
        """Cross-symbol stock-flow outliers (imbalance-ranked). Requires Alpha."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if min_trades is not None:
            params["minTrades"] = min_trades
        if window_minutes is not None:
            params["windowMinutes"] = window_minutes
        return self._get("/v1/flow/stocks/outliers", params or None)

    # Flow signals (unusual-flow feed, Alpha+).

    def flow_signals(
        self,
        symbol: str,
        *,
        min_score: int | None = None,
        intent: str | None = None,
        structure: str | None = None,
        window_minutes: int | None = None,
        limit: int | None = None,
        expiry: str | None = None,
    ) -> FlowSignalsResponse:
        """Scored unusual-flow feed for one underlying. Requires Alpha.

        Each notable print is coalesced into a signal, classified
        (block/sweep, NBBO aggressor, opening/closing bias, intent), and
        scored 0–100 with a transparent component breakdown. Ranked by
        score, highest first.

        ``min_score`` drops signals below the threshold; ``intent``
        filters to ``"bullish"``/``"bearish"``/``"neutral"``;
        ``structure`` filters to ``"block"``/``"sweep"``;
        ``window_minutes`` sets the look-back (1–10080, default 240);
        ``limit`` caps the response (1–500, default 50); ``expiry``
        filters to a single ``YYYY-MM-DD`` cycle.
        """
        params: dict[str, Any] = {}
        if min_score is not None:
            params["minScore"] = min_score
        if intent:
            params["intent"] = intent
        if structure:
            params["structure"] = structure
        if window_minutes is not None:
            params["windowMinutes"] = window_minutes
        if limit is not None:
            params["limit"] = limit
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/signals/{_seg(symbol)}", params or None)

    def flow_signals_summary(
        self,
        symbol: str,
        *,
        window_minutes: int | None = None,
        expiry: str | None = None,
    ) -> FlowSignalsSummaryResponse:
        """Net bullish/bearish + opening/closing premium roll-up plus
        the top 10 signals. Cheap "smart-money tilt" read. Requires Alpha.
        """
        params: dict[str, Any] = {}
        if window_minutes is not None:
            params["windowMinutes"] = window_minutes
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/signals/{_seg(symbol)}/summary", params or None)

    def flow_dealer_premium(
        self,
        symbol: str,
        *,
        window_minutes: int | None = None,
        expiry: str | None = None,
    ) -> FlowDealerPremiumResponse:
        """Full-tape Net Dealer Premium roll-up over a window (VWAP-weighted per
        minute bucket). Requires Alpha+."""
        params: dict[str, Any] = {}
        if window_minutes is not None:
            params["windowMinutes"] = window_minutes
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/flow/options/{_seg(symbol)}/dealer-premium", params or None)

    # ── Zero-DTE Flow (intraday, simulation-aware) ──────────────────

    def flow_zero_dte_snapshot(self, symbol: str) -> FlowZeroDteSnapshotResponse:
        """Live 0DTE shape (same as ``zero_dte`` plus a ``flow_direction`` block)
        computed on effective intraday OI. Requires Growth+."""
        return self._get(f"/v1/flow/zero-dte/snapshot/{_seg(symbol)}")

    def flow_zero_dte_series(
        self, symbol: str, *, bar: str | None = None, minutes: int | None = None
    ) -> FlowZeroDteSeriesResponse:
        """Intraday time series of today's 0DTE headline metrics + cumulative
        dealer hedge-flow. ``bar`` ∈ {30s,1m,5m,15m}. Requires Growth+."""
        params: dict[str, Any] = {}
        if bar:
            params["bar"] = bar
        if minutes is not None:
            params["minutes"] = minutes
        return self._get(f"/v1/flow/zero-dte/series/{_seg(symbol)}", params or None)

    def flow_zero_dte_hedge_flow(
        self,
        symbol: str,
        *,
        side: str | None = None,
        bar: str | None = None,
        minutes: int | None = None,
    ) -> FlowZeroDteHedgeFlowResponse:
        """Estimated dealer hedge-flow time series for today's 0DTE chain.
        ``side`` ∈ {all,calls,puts}; ``bar`` ∈ {30s,1m,5m,15m}. Requires Growth+."""
        params: dict[str, Any] = {}
        if side:
            params["side"] = side
        if bar:
            params["bar"] = bar
        if minutes is not None:
            params["minutes"] = minutes
        return self._get(f"/v1/flow/zero-dte/hedge-flow/{_seg(symbol)}", params or None)

    def flow_zero_dte_heatmap(
        self,
        symbol: str,
        *,
        metric: str | None = None,
        mode: str | None = None,
        bar: str | None = None,
        minutes: int | None = None,
    ) -> FlowZeroDteHeatmapResponse:
        """Per-strike intraday 0DTE heatmap. ``metric`` ∈
        {gex,dex,vex,chex,oi,signed_flow}; ``mode`` ∈ {raw,delta};
        ``bar`` only ``1m``. Requires Alpha+."""
        params: dict[str, Any] = {}
        if metric:
            params["metric"] = metric
        if mode:
            params["mode"] = mode
        if bar:
            params["bar"] = bar
        if minutes is not None:
            params["minutes"] = minutes
        return self._get(f"/v1/flow/zero-dte/heatmap/{_seg(symbol)}", params or None)

    def flow_zero_dte_strike_flow(
        self, symbol: str, *, bar: str | None = None, minutes: int | None = None
    ) -> FlowZeroDteStrikeFlowResponse:
        """Per-strike signed aggressor flow over today's 0DTE session (signed
        delta-$, gamma-$, contract count per bar). ``bar`` only ``1m``. Requires Alpha+."""
        params: dict[str, Any] = {}
        if bar:
            params["bar"] = bar
        if minutes is not None:
            params["minutes"] = minutes
        return self._get(f"/v1/flow/zero-dte/strike-flow/{_seg(symbol)}", params or None)

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
    ) -> PricingGreeksResponse:
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
    ) -> PricingIvResponse:
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
    ) -> PricingKellyResponse:
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

    def volatility(self, symbol: str) -> VolatilityResponse:
        """Comprehensive volatility analysis. Requires Growth+."""
        return self._get(f"/v1/volatility/{_seg(symbol)}")

    def adv_volatility(self, symbol: str) -> AdvVolatilityResponse:
        """Advanced volatility analytics: SVI parameters, variance surface, arbitrage detection, greeks surfaces, variance swap. Requires Alpha+."""
        return self._get(f"/v1/adv_volatility/{_seg(symbol)}")

    def expected_move(self, symbol: str, *, expiry: str | None = None) -> ExpectedMoveResponse:
        """Straddle-implied expected move per expiry (from ATM IV). Pass
        ``expiry`` to restrict to a single cycle. Requires Basic+."""
        params: dict[str, Any] = {}
        if expiry:
            params["expiry"] = expiry
        return self._get(f"/v1/expected-move/{_seg(symbol)}", params or None)

    def realized_volatility(self, symbol: str) -> RealizedVolatilityResponse:
        """Range-based realized (historical) vol estimators (close-to-close,
        Parkinson, Garman-Klass, Rogers-Satchell, Yang-Zhang) over 10/20/30-day
        windows. Requires Alpha+."""
        return self._get(f"/v1/volatility/realized/{_seg(symbol)}")

    def volatility_forecast(
        self, symbol: str, *, dist: str | None = None
    ) -> VolatilityForecastResponse:
        """Conditional vol forecasts (EWMA λ=0.94, HAR-RV, GARCH(1,1) MLE). Pass
        ``dist`` (``student_t`` default, or ``gaussian``) to set the GARCH error
        distribution. Requires Alpha+."""
        params: dict[str, Any] = {}
        if dist:
            params["dist"] = dist
        return self._get(f"/v1/volatility/forecast/{_seg(symbol)}", params or None)

    # ── Reference Data ──────────────────────────────────────────────

    def tickers(self) -> TickersResponse:
        """All available stock tickers."""
        return self._get("/v1/tickers")

    def options(self, ticker: str) -> OptionsMetaResponse:
        """Option chain metadata (expirations + strikes)."""
        return self._get(f"/v1/options/{_seg(ticker)}")

    def symbols(self) -> SymbolsResponse:
        """Currently queried symbols with live data."""
        return self._get("/v1/symbols")

    # ── VRP (Variance Risk Premium) ─────────────────────────────────

    def vrp(self, symbol: str, *, date: str | None = None) -> VrpResponse:
        """Variance risk premium analytics — the implied-vs-realized vol
        spread, conditioned on dealer gamma and vanna regime, with
        strategy scores for harvesting.

        Returns a nested payload. Key access paths:

        - ``response["symbol"]``, ``response["underlying_price"]`` — top-level
        - ``response["vrp"]["z_score"]``, ``["percentile"]``,
          ``["atm_iv"]``, ``["rv_20d"]``, ``["vrp_20d"]`` — core VRP metrics
        - ``response["directional"]["downside_vrp"]``,
          ``["upside_vrp"]`` — directional skew (NOT ``put_vrp``/``call_vrp``)
        - ``response["gex_conditioned"]["harvest_score"]``,
          ``["regime"]`` — gamma-regime conditioning
        - ``response["regime"]["net_gex"]``, ``["gamma"]``,
          ``["vrp_regime"]`` — regime snapshot
        - ``response["strategy_scores"]`` — short_put_spread, short_strangle,
          iron_condor, calendar_spread (0–100)
        - ``response["net_harvest_score"]``,
          ``response["dealer_flow_risk"]`` — top-level composite scores

        Pass ``date="YYYY-MM-DD"`` to return the persisted VRP snapshot for that
        date instead of the live dashboard (``404`` if no snapshot exists).

        Requires Alpha+.
        """
        params = {"date": date} if date else None
        return self._get(f"/v1/vrp/{_seg(symbol)}", params)

    def vrp_history(self, symbol: str, *, days: int | None = None) -> VrpHistoryResponse:
        """Daily VRP time series for charting/backtesting (days 1-365,
        default 30). Requires Alpha+."""
        params: dict[str, Any] = {}
        if days is not None:
            params["days"] = days
        return self._get(f"/v1/vrp/{_seg(symbol)}/history", params or None)

    # ── Max Pain ────────────────────────────────────────────────────

    def max_pain(self, symbol: str, *, expiration: str | None = None) -> MaxPainResponse:
        """Max pain analysis with dealer alignment overlay, pain curve, OI
        breakdown, expected move context, pin probability, and multi-expiry
        calendar. Requires Growth+.

        Parameters
        ----------
        symbol : str
            Underlying symbol.
        expiration : str, optional
            Filter to single expiry (YYYY-MM-DD). Omit for full-chain analysis.
        """
        params: dict[str, Any] = {}
        if expiration:
            params["expiration"] = expiration
        return self._get(f"/v1/maxpain/{_seg(symbol)}", params or None)

    # ── Screener ────────────────────────────────────────────────────

    def screener(
        self,
        *,
        filters: dict[str, Any] | None = None,
        sort: list[dict[str, Any]] | None = None,
        select: list[str] | None = None,
        formulas: list[dict[str, str]] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ScreenerResponse:
        """Live options screener — filter/rank symbols by gamma exposure, VRP,
        volatility, greeks, and more.

        Powered by an in-memory store updated every 5-10s from live market data.
        Growth: 10-symbol universe, up to 10 rows. Alpha: ~250 symbols, up to 50
        rows, formulas, and harvest/dealer-flow-risk scores.

        Parameters
        ----------
        filters : dict, optional
            Recursive filter tree. Leaf: {"field": "atm_iv", "operator": "gte",
            "value": 20}. Group: {"op": "and", "conditions": [...]}. Supports
            dotted prefixes `expiries.X`, `strikes.X`, `contracts.X` for
            cascading filters.
        sort : list of dict, optional
            Sort specs (primary first), e.g.
            [{"field": "harvest_score", "direction": "desc"}].
            Also accepts {"formula": "alias_name", ...}.
        select : list of str, optional
            Field names to return, or ["*"] for the full flat object.
        formulas : list of dict, optional
            Computed fields (Alpha only), e.g.
            [{"alias": "vrp_ratio", "expression": "atm_iv / rv_20d"}].
        limit : int, optional
            Row cap. 1-10 on Growth, 1-50 on Alpha. Default 50.
        offset : int, optional
            Pagination offset (Alpha only).

        Returns
        -------
        dict
            {"meta": {"total_count": ..., "tier": ..., ...},
             "data": [{"symbol": ..., ...}, ...]}

        Examples
        --------
        Harvestable VRP screen:

        >>> fa.screener(
        ...     filters={
        ...         "op": "and",
        ...         "conditions": [
        ...             {"field": "regime", "operator": "eq", "value": "positive_gamma"},
        ...             {"field": "vrp_regime", "operator": "eq", "value": "harvestable"},
        ...             {"field": "harvest_score", "operator": "gte", "value": 65},
        ...         ],
        ...     },
        ...     sort=[{"field": "harvest_score", "direction": "desc"}],
        ...     select=["symbol", "price", "harvest_score", "dealer_flow_risk"],
        ... )
        """
        body: dict[str, Any] = {}
        if filters is not None:
            body["filters"] = filters
        if sort is not None:
            body["sort"] = sort
        if select is not None:
            body["select"] = select
        if formulas is not None:
            body["formulas"] = formulas
        if limit is not None:
            body["limit"] = limit
        if offset is not None:
            body["offset"] = offset
        return self._post("/v1/screener", body)

    def screener_fields(self) -> ScreenerFieldsResponse:
        """List every screener-referenceable field with its value type.
        Requires an API key (any tier)."""
        return self._get("/v1/screener/fields")

    # ── Strategy Signals (uniform decision envelope) ────────────────

    def _strategy(self, kind: str, symbol: str, **params: Any) -> StrategyDecisionResponse:
        """Shared dispatcher for /v1/strategies/{kind}/{symbol}. Drops None params."""
        query = {k: v for k, v in params.items() if v is not None}
        return self._get(f"/v1/strategies/{kind}/{_seg(symbol)}", query or None)

    def strategy_flow_anomaly(self, symbol: str, *, expiry: str | None = None) -> StrategyDecisionResponse:
        """Scores directional options-flow imbalance (call vs put). Requires Growth+."""
        return self._strategy("flow-anomaly", symbol, expiry=expiry)

    def strategy_expiry_positioning(
        self,
        symbol: str,
        *,
        expiry: str | None = None,
        min_open_interest: int | None = None,
        wing_width: float | None = None,
    ) -> StrategyDecisionResponse:
        """Scores OPEX pin risk for a single expiry, proposes an iron fly. Requires Basic+."""
        return self._strategy(
            "expiry-positioning",
            symbol,
            expiry=expiry,
            minOpenInterest=min_open_interest,
            wingWidth=wing_width,
        )

    def strategy_zero_dte(
        self,
        symbol: str,
        *,
        expiry: str | None = None,
        min_open_interest: int | None = None,
        wing_width: float | None = None,
    ) -> StrategyDecisionResponse:
        """Same-day 0DTE range-compression read + iron fly. Requires Growth+ and 0DTE access."""
        return self._strategy(
            "zero-dte",
            symbol,
            expiry=expiry,
            minOpenInterest=min_open_interest,
            wingWidth=wing_width,
        )

    def strategy_dealer_regime(self, symbol: str, *, expiry: str | None = None) -> StrategyDecisionResponse:
        """Scores the dealer gamma regime (compression vs acceleration). Requires Growth+."""
        return self._strategy("dealer-regime", symbol, expiry=expiry)

    def strategy_vol_carry(
        self,
        symbol: str,
        *,
        expiry: str | None = None,
        min_open_interest: int | None = None,
        target_short_delta: float | None = None,
        max_width: float | None = None,
        min_credit: float | None = None,
    ) -> StrategyDecisionResponse:
        """Volatility risk-premium carry score + short-vol structures. Requires Alpha+."""
        return self._strategy(
            "vol-carry",
            symbol,
            expiry=expiry,
            minOpenInterest=min_open_interest,
            targetShortDelta=target_short_delta,
            maxWidth=max_width,
            minCredit=min_credit,
        )

    def strategy_yield_enhancement(
        self,
        symbol: str,
        *,
        expiry: str | None = None,
        target_delta: float | None = None,
        min_open_interest: int | None = None,
        structure: str | None = None,
        exclude_earnings_before_expiry: bool | None = None,
    ) -> StrategyDecisionResponse:
        """Income overlay (covered call / cash-secured put) selection. Requires Growth+."""
        return self._strategy(
            "yield-enhancement",
            symbol,
            expiry=expiry,
            targetDelta=target_delta,
            minOpenInterest=min_open_interest,
            structure=structure,
            excludeEarningsBeforeExpiry=exclude_earnings_before_expiry,
        )

    def strategy_surface_anomaly(self, symbol: str, *, expiry: str | None = None) -> StrategyDecisionResponse:
        """Scores rich/cheap wings vs the calibrated SVI fit. Requires Alpha+."""
        return self._strategy("surface-anomaly", symbol, expiry=expiry)

    def strategy_skew(self, symbol: str, *, expiry: str | None = None) -> StrategyDecisionResponse:
        """Scores skew richness and proposes the matching trade. Requires Growth+."""
        return self._strategy("skew", symbol, expiry=expiry)

    def strategy_term_structure(self, symbol: str) -> StrategyDecisionResponse:
        """Scores IV term-structure slope (contango/backwardation). Requires Growth+."""
        return self._strategy("term-structure", symbol)

    def strategy_tail_pricing(self, symbol: str, *, expiry: str | None = None) -> StrategyDecisionResponse:
        """Scores tail (deep-wing) pricing richness. Requires Growth+."""
        return self._strategy("tail-pricing", symbol, expiry=expiry)

    # ── Earnings Analytics ──────────────────────────────────────────

    def earnings_calendar(
        self,
        *,
        days: int | None = None,
        symbols: str | list[str] | None = None,
        importance: int | None = None,
    ) -> EarningsCalendarResponse:
        """Upcoming earnings calendar over a forward window. Requires Growth+."""
        params: dict[str, Any] = {}
        if days is not None:
            params["days"] = days
        if symbols is not None:
            if isinstance(symbols, (list, tuple)):
                symbols = ",".join(str(s) for s in symbols)
            params["symbols"] = symbols
        if importance is not None:
            params["importance"] = importance
        return self._get("/v1/earnings/calendar", params or None)

    def earnings_expected_move(self, symbol: str) -> EarningsExpectedMoveResponse:
        """Earnings-implied move decomposition (jump vs diffusion) for the next
        event. Requires Growth+."""
        return self._get(f"/v1/earnings/expected-move/{_seg(symbol)}")

    def earnings_history(self, symbol: str, *, limit: int | None = None) -> EarningsHistoryResponse:
        """Past earnings events with EPS/revenue surprises, implied-vs-actual
        moves, and realized IV crush. Requires Growth+."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        return self._get(f"/v1/earnings/history/{_seg(symbol)}", params or None)

    def earnings_iv_crush(self, symbol: str) -> EarningsIvCrushResponse:
        """Expected IV crush for the next event + the historical crush
        distribution. Requires Growth+."""
        return self._get(f"/v1/earnings/iv-crush/{_seg(symbol)}")

    def earnings_vrp(self, symbol: str) -> EarningsVrpResponse:
        """Earnings VRP — event-implied move vs realized actual-move history with
        a richness assessment. Requires Alpha+."""
        return self._get(f"/v1/earnings/vrp/{_seg(symbol)}")

    def earnings_dealer_positioning(self, symbol: str) -> EarningsDealerPositioningResponse:
        """Dealer exposure scoped to the earnings event (walls, GEX buckets, charm
        acceleration, top strikes). Requires Alpha+."""
        return self._get(f"/v1/earnings/dealer-positioning/{_seg(symbol)}")

    def earnings_strategies(self, symbol: str) -> EarningsStrategiesResponse:
        """Strategy-suitability scores for the upcoming earnings event. Requires Alpha+."""
        return self._get(f"/v1/earnings/strategies/{_seg(symbol)}")

    def earnings_screener(
        self,
        *,
        sort: str | None = None,
        limit: int | None = None,
        days: int | None = None,
        min_importance: int | None = None,
    ) -> EarningsScreenerResponse:
        """Cross-sectional screener over upcoming earnings (VRP richness, cheapest
        move, highest crush, importance). Requires Alpha+."""
        params: dict[str, Any] = {}
        if sort:
            params["sort"] = sort
        if limit is not None:
            params["limit"] = limit
        if days is not None:
            params["days"] = days
        if min_importance is not None:
            params["min_importance"] = min_importance
        return self._get("/v1/earnings/screener", params or None)

    # ── Structures (pure-math, POST) ────────────────────────────────

    def structure_pnl(
        self,
        legs: list[dict[str, Any]],
        *,
        min_underlying: float | None = None,
        max_underlying: float | None = None,
        points: int | None = None,
    ) -> StructurePnlResponse:
        """At-expiry P&L curve, breakevens, and max profit/loss for a multi-leg
        structure. Each leg: action, type, strike, premium, quantity. Requires Basic+."""
        body: dict[str, Any] = {"legs": legs}
        if min_underlying is not None:
            body["minUnderlying"] = min_underlying
        if max_underlying is not None:
            body["maxUnderlying"] = max_underlying
        if points is not None:
            body["points"] = points
        return self._post("/v1/structures/pnl", body)

    def structure_greeks(
        self,
        legs: list[dict[str, Any]],
        *,
        spot: float,
        today: str | None = None,
        rate: float | None = None,
        dividend_yield: float | None = None,
    ) -> StructureGreeksResponse:
        """Aggregate Black-Scholes greeks across a multi-leg position. Each leg
        carries its own expiry + impliedVol (calendars/diagonals aggregate
        correctly). Requires Basic+."""
        body: dict[str, Any] = {"legs": legs, "spot": spot}
        if today:
            body["today"] = today
        if rate is not None:
            body["rate"] = rate
        if dividend_yield is not None:
            body["dividendYield"] = dividend_yield
        return self._post("/v1/structures/greeks", body)

    # ── Account & System ────────────────────────────────────────────

    def account(self) -> AccountResponse:
        """Account info and quota."""
        return self._get("/v1/account")

    def health(self) -> HealthResponse:
        """Health check (public, no auth required)."""
        return self._get("/health")
