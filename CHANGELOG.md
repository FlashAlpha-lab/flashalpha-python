# Changelog

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
