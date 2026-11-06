# Changelog

## 1.4.0 - 2026-11-06

### Added
- **sell-window** (`fa.sell_window(symbol)`) for `GET /v1/strategies/sell-window/{symbol}`: should you sell options today? `sell`, `skip` or `unavailable` for four listed expiries on SPY, QQQ and IWM, with the trades to place on a sell (strikes, quotes, exit rule). More than 5 million backtests led to this endpoint. Live answers need Basic or higher through November 2026, and Growth or higher from December 1, 2026. Backtesting any past session needs Alpha or higher.
- **`SellWindowResponse`** with typed windows, candidates and legs. It has its own shape, not the strategy decision envelope.
- `docs/sell-window.md`, a full reference with the backtest, FAQ and links.

## 1.3.0 - 2026-08-25

### Added
- **`data_as_of` response envelope.** Every successful response now carries
  `data_as_of`, reporting when each upstream feed last delivered to the node that
  answered: equity and index spot, their option chains, futures and futures options,
  the classified trade tape, settled open interest, and the macro series, each
  reported separately because they arrive over different pipes and fail
  independently. `endpoint_version` identifies the deployment that produced the
  response.
- **`DataAsOf`** exported as a `TypedDict` and added to every `*Response` type, so
  the envelope has editor completion and type checking rather than being an untyped
  passthrough. Responses are dicts at runtime, so this is additive: existing code is
  unaffected.

### Notes
- Read each feed against its own cadence rather than against `as_of`. Settled open
  interest dated to the previous session's close is correct, since it is published
  once per session; an options feed an hour behind during the regular session is not.
- A `null` means that node has not seen that feed, not that it is broken.
- The field evidences that a feed delivered recently. It does not assert that every
  contract in a chain is equally current.


## 1.1.0 - 2026-06-08

### Added
- **Strategy Signals** — 10 decision-support endpoints returning a uniform
  `StrategyDecisionResponse` envelope (score, decision band, regime, ranked
  tradeable structures, metrics, risk flags): `strategy_flow_anomaly`,
  `strategy_expiry_positioning`, `strategy_zero_dte`, `strategy_dealer_regime`,
  `strategy_vol_carry`, `strategy_yield_enhancement`, `strategy_surface_anomaly`,
  `strategy_skew`, `strategy_term_structure`, `strategy_tail_pricing`.
- **Earnings Analytics** — `earnings_calendar`, `earnings_expected_move`,
  `earnings_history`, `earnings_iv_crush`, `earnings_vrp`,
  `earnings_dealer_positioning`, `earnings_strategies`, `earnings_screener`
  (event-implied move decomposition, IV crush distribution, earnings VRP
  richness, dealer positioning into the event, suitability scores).
- **Structures** (pure-math, POST) — `structure_pnl` (at-expiry P&L curve,
  breakevens, max profit/loss) and `structure_greeks` (aggregate Black-Scholes
  greeks across multi-leg positions, per-leg expiry + IV).
- **Zero-DTE Flow** — intraday, simulation-aware: `flow_zero_dte_snapshot`,
  `flow_zero_dte_series`, `flow_zero_dte_hedge_flow`, `flow_zero_dte_heatmap`,
  `flow_zero_dte_strike_flow`, plus `flow_dealer_premium` (full-tape Net Dealer
  Premium) and `flow_stock_bars` (multi-resolution OHLCV+flow bars).
- **Exposure (additional)** — `exposure_sheet` (unified per-strike
  GEX/DEX/VEX/CHEX/DAG + Line-in-the-Sand + gamma peaks + OPEX flags),
  `exposure_term_structure`, `exposure_basket` (weighted cross-symbol aggregate),
  `exposure_oi_diff` (day-over-day OI deltas).
- **Volatility / vol-arb** — `surface_svi` (live SVI params per slice),
  `liquidity`, `skew_term`, `spot_vol_correlation`, `dispersion`
  (implied-vs-realized correlation / dispersion trading), `expected_move`,
  `vrp_history`.
- **Macro / reference** — `vix_state` (over/under-vixing regime),
  `universe` (curated tier-1/tier-2 directory), `screener_fields`.
- Response `TypedDict`s for every new endpoint family, all exported from the
  package root (`StrategyDecisionResponse`, the `Earnings*`, `Structure*`,
  `FlowZeroDte*`, `ExposureSheet*`/`ExposureBasket*`/`ExposureOiDiff*`,
  `SurfaceSviResponse`, `DispersionResponse`, `VixStateResponse`,
  `UniverseResponse`, `ExpectedMoveResponse`, `VrpHistoryResponse`, etc.).

### Changed
- `zero_dte(symbol, ...)` gained an optional `expiry="YYYY-MM-DD"` param to
  target a specific same-day-style expiry (1DTE / 2DTE / any expiry).
- `vrp(symbol, ...)` gained an optional `date="YYYY-MM-DD"` param to return the
  persisted VRP snapshot for that date instead of the live dashboard.

## 1.0.1 - 2026-05-21

### Added
- `flow_signals(symbol, ...)` and `flow_signals_summary(symbol, ...)` —
  scored, classified unusual-flow feed for one underlying. Each notable
  print is coalesced into a signal (block/sweep, NBBO aggressor,
  opening/closing bias, intent), scored 0-100 with a transparent
  component breakdown, and enriched with chain context (greeks,
  IV-vs-ATM, moneyness, estimated delta-notional). Summary endpoint
  rolls up net bullish/bearish and opening/closing premium plus the top
  10 signals. New `TypedDict` types: `FlowSignal`, `FlowSignalsResponse`,
  `FlowSignalsSummaryResponse`, `FlowSignalsChain`,
  `FlowSignalScoreBreakdown`, `FlowSignalEnrichment`. Requires Alpha.
- Live integration tests for both signals endpoints.

## 1.0.0 - 2026-05-15

### Added
- **Live Flow API tier** — typed models + client methods + LLM-discoverable docs
  for all 22 `/v1/flow/*` endpoints (analytics: levels, pin-risk, summary, oi,
  gex, dex, dealer-risk, live; raw flow: option/stock recent, summary, blocks,
  history, cumulative, leaderboards, outliers). Flow gex/dex reuse the existing
  `GexStrikeRow`/`DexStrikeRow` types.
- Per-endpoint live integration tests for every Flow endpoint.

### Changed / Breaking
- `SurfaceResponse.slices_used` is now `int` (a slice count), was `List[str]` —
  corrected to match the API.
- Removed `exposure_history()` — the `/v1/exposure/history` endpoint does not exist.

### Added (prior 0.4.0-rc cycle)
- `docs/api.md` — full endpoint reference, URL-prefix table, response schemas, and sample JSON for every endpoint
- 17 integration regression tests (`tests/test_integration.py`) guarding against response-shape and URL-pattern regressions reported by Alpha users:
  - Nested VRP response (`vrp.z_score`, `gex_conditioned.harvest_score`, `regime.net_gex`, `directional.*`)
  - `exposure_summary` nesting (`exposures.net_gex`)
  - VRP directional field names (`downside_vrp`/`upside_vrp`, not `put_vrp`/`call_vrp`)
  - URL-prefix mix — `/stockquote`, `/optionquote`, `/historical/*` without `/v1/`; everything else with
  - `/v1/stock/{sym}/summary` canonical vs `/v1/summary/{sym}` 404
  - Canonical `POST /v1/screener` + `/v1/screener/live` deprecation
  - `/v1/vrp/{sym}` REST endpoint (until `vrp()` method ships)

## 0.3.2 (2026-04-07)

### Added
- `max_pain()` — max pain analysis with dealer alignment overlay, pain curve, OI breakdown, expected move context, pin probability, and multi-expiry calendar (Growth+)

## 0.3.1 (2026-04-02)

### Changed
- Screener endpoint renamed: `/v1/screener/live` → `/v1/screener` (canonical). The SDK's `screener()` method now POSTs to `/v1/screener`.

## 0.3.0 (2026-03-30)

### Added
- `screener()` — live options screener. Filter/rank symbols by gamma exposure, VRP, volatility, greeks, harvest scores, and custom formulas. Growth: 10-symbol universe, up to 10 rows. Alpha: ~250 symbols, up to 50 rows, formulas, and harvest/dealer-flow-risk scores.
- Recursive filter trees (leaf + `and`/`or` groups), cascading filters via `expiries.*` / `strikes.*` / `contracts.*` prefixes, multi-sort, pagination, inline and named formulas, `select=["*"]` for the full flat object.
- Unit + integration test coverage for screener filter tree, operators, formulas, and tier gating.

## 0.2.0 (2026-03-26)

### Added
- `zero_dte()` — real-time 0DTE analytics (regime, pin risk, expected move, hedging, decay)
- `exposure_history()` — daily exposure snapshots for trend analysis
- `adv_volatility()` — advanced volatility analytics (SVI parameters, variance surface, arbitrage detection, greeks surfaces, variance swap pricing)
- Comprehensive method reference table in README
- SEO-optimized keywords in PyPI metadata

### Changed
- Updated API plans table to reflect current tiers (Free/Basic/Growth/Alpha)
- Improved README structure and documentation

## 0.1.0 (2026-03-13)

### Added
- Initial release
- Core client with all FlashAlpha API endpoints
- Exposure analytics: `gex()`, `dex()`, `vex()`, `chex()`, `exposure_levels()`, `exposure_summary()`, `narrative()`
- Market data: `stock_quote()`, `option_quote()`, `stock_summary()`, `surface()`
- Historical data: `historical_stock_quote()`, `historical_option_quote()`
- Pricing: `greeks()`, `iv()`, `kelly()`
- Volatility: `volatility()`
- Reference: `tickers()`, `options()`, `symbols()`, `account()`, `health()`
- Error handling: `AuthenticationError`, `TierRestrictedError`, `NotFoundError`, `RateLimitError`, `ServerError`
- 36 unit tests, 23 integration tests
