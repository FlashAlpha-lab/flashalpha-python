# Changelog

## Unreleased

### Added
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
