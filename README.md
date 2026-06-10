# FlashAlpha Python SDK

[![PyPI](https://img.shields.io/pypi/v/flashalpha)](https://pypi.org/project/flashalpha/)
[![Python](https://img.shields.io/pypi/pyversions/flashalpha)](https://pypi.org/project/flashalpha/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/FlashAlpha-lab/flashalpha-python/actions/workflows/ci.yml/badge.svg)](https://github.com/FlashAlpha-lab/flashalpha-python/actions/workflows/ci.yml)

Python client for the [FlashAlpha options analytics API](https://flashalpha.com). Access a **live options screener** (filter/rank symbols by gamma exposure, VRP, IV, greeks, harvest scores, and custom formulas), real-time gamma exposure (GEX), delta exposure (DEX), vanna exposure (VEX), charm exposure (CHEX), 0DTE analytics, Black-Scholes greeks, implied volatility, volatility surfaces, dealer positioning, Kelly criterion sizing, and more — all from Python.

> 🔑 **[Get a free API key at flashalpha.com →](https://flashalpha.com)** · 📚 [API documentation](https://flashalpha.com/docs) · 💹 [FlashAlpha options analytics API](https://flashalpha.com)

```bash
pip install flashalpha
```

## Quick Start

```python
from flashalpha import FlashAlpha

fa = FlashAlpha("YOUR_API_KEY")  # Get a free key at flashalpha.com

# Gamma exposure by strike
gex = fa.gex("SPY")
print(f"Net GEX: ${gex['net_gex']:,.0f}")
print(f"Gamma flip: {gex['gamma_flip']}")

for strike in gex["strikes"][:5]:
    print(f"  {strike['strike']}: net ${strike['net_gex']:,.0f}")
```

Get your free API key at [flashalpha.com](https://flashalpha.com) — no credit card required.

## Features

### Live Options Screener

Filter and rank symbols in real time across your universe by gamma exposure,
VRP, implied volatility, greeks, harvest scores, dealer flow risk, and custom
formulas. Data is live from an in-memory store refreshed every 5-10 seconds.

```python
# Harvestable VRP setups with low dealer flow risk
result = fa.screener(
    filters={
        "op": "and",
        "conditions": [
            {"field": "regime", "operator": "eq", "value": "positive_gamma"},
            {"field": "vrp_regime", "operator": "eq", "value": "harvestable"},
            {"field": "dealer_flow_risk", "operator": "lte", "value": 40},
            {"field": "harvest_score", "operator": "gte", "value": 65},
        ],
    },
    sort=[{"field": "harvest_score", "direction": "desc"}],
    select=["symbol", "price", "harvest_score", "dealer_flow_risk"],
)
for row in result["data"]:
    print(f"{row['symbol']}: score={row['harvest_score']} risk={row['dealer_flow_risk']}")

# Custom formula — rank by IV premium over realized vol
result = fa.screener(
    formulas=[{"alias": "iv_premium", "expression": "atm_iv - rv_20d"}],
    sort=[{"formula": "iv_premium", "direction": "desc"}],
    select=["symbol", "atm_iv", "rv_20d", "iv_premium"],
    limit=20,
)
```

Cascading filters on expiries, strikes, and contracts (e.g. `expiries.days_to_expiry`,
`strikes.call_oi`, `contracts.delta`) trim the tree at each level and return only the
matching subtree. See the [Screener spec](https://flashalpha.com/docs/lab-api-screener)
and [cookbook](https://flashalpha.com/docs/lab-api-screener-cookbook) for all fields,
operators, and recipes.

### Options Exposure Analytics

Gamma exposure, delta exposure, vanna exposure, and charm exposure by strike. See where dealers are positioned and how they need to hedge.

```python
gex = fa.gex("SPY")                                        # Gamma exposure
dex = fa.dex("AAPL")                                       # Delta exposure
vex = fa.vex("QQQ")                                        # Vanna exposure
chex = fa.chex("NVDA")                                     # Charm exposure

levels = fa.exposure_levels("SPY")                          # Key levels
print(f"Call wall: {levels['levels']['call_wall']}")
print(f"Put wall: {levels['levels']['put_wall']}")
print(f"Gamma flip: {levels['levels']['gamma_flip']}")

summary = fa.exposure_summary("SPY")                        # Full summary (Growth+)
narrative = fa.narrative("SPY")                              # AI narrative (Growth+)
print(narrative["narrative"]["outlook"])
```

### 0DTE Analytics

Real-time zero-days-to-expiration analysis: gamma regime, expected move, pin risk scoring, dealer hedging estimates, theta decay acceleration, and per-strike breakdown.

```python
dte = fa.zero_dte("SPY")                                    # Growth+
print(f"Pin score: {dte['pin_risk']['pin_score']}/100")
print(f"Expected move: ±{dte['expected_move']['remaining_1sd_pct']:.2f}%")
print(f"Theta/hr: ${dte['decay']['theta_per_hour_remaining']:,.0f}")
print(f"Gamma acceleration: {dte['decay']['gamma_acceleration']}x vs 7DTE")
```

### Black-Scholes Greeks and Implied Volatility

Full BSM greeks — first order (delta, gamma, theta, vega, rho), second order (vanna, charm, vomma), and third order (speed, zomma, color, ultima).

```python
g = fa.greeks(spot=580, strike=580, dte=30, sigma=0.18, type="call")
print(f"Delta: {g['first_order']['delta']}")
print(f"Vanna: {g['second_order']['vanna']}")
print(f"Speed: {g['third_order']['speed']}")

iv = fa.iv(spot=580, strike=580, dte=30, price=12.69)
print(f"IV: {iv['implied_volatility_pct']}%")
```

### Volatility Analytics

Realized vol, IV-RV spreads, skew profiles, term structure, GEX by DTE, theta decay, put/call breakdowns, OI concentration, hedging scenarios, and liquidity analysis.

```python
vol = fa.volatility("TSLA")                                 # Growth+
print(f"ATM IV: {vol['atm_iv']}%")
print(f"RV 20d: {vol['realized_vol']['rv_20d']}%")
print(f"VRP: {vol['iv_rv_spreads']['assessment']}")
print(f"Skew 25d: {vol['skew_profiles'][0]['skew_25d']}")
```

### Advanced Volatility (SVI, Variance Surfaces, Arbitrage Detection)

Raw SVI parameters per expiry, total variance surface grids, butterfly and calendar arbitrage flags, higher-order greeks surfaces (vanna, charm, volga, speed), and variance swap fair values.

```python
adv = fa.adv_volatility("SPY")                              # Alpha+
print(f"SVI params: {adv['svi_parameters'][0]}")
print(f"Arbitrage flags: {len(adv['arbitrage_flags'])}")
print(f"Var swap fair vol: {adv['variance_swap_fair_values'][0]['fair_vol']}%")
```

### Strategy Signals (decision envelope)

Ten decision-support endpoints that score a single trading idea 0-100, classify a regime, and return ranked tradeable structures (legs, credit/debit, breakevens) in one uniform `StrategyDecisionResponse`: flow anomaly, expiry positioning, 0DTE range compression, dealer gamma regime, vol-carry (VRP), yield enhancement (covered call / cash-secured put), surface anomaly, skew, term structure, and tail pricing.

```python
carry = fa.strategy_vol_carry("SPY", target_short_delta=0.20)  # Alpha+
print(carry["decision"], carry["score"], carry["regime"])
for s in carry["best_structures"]:
    print(s["structure"], s["expiry"], s.get("credit"))
```

### Earnings Analytics

Earnings calendar, implied-move decomposition (earnings jump vs baseline diffusion), historical earnings surprises and realized moves, expected IV crush and its historical distribution, earnings VRP richness, dealer positioning into the event, strategy-suitability scores, and a cross-sectional earnings screener.

```python
em = fa.earnings_expected_move("AAPL")                          # Growth+
print(em["earnings_date"], em.get("implied_move_pct"))
events = fa.earnings_screener(sort="vrp_richest", days=14)      # Alpha+
```

### Multi-Leg Structures (pure math)

Deterministic at-expiry P&L diagrams, breakevens, and aggregate Black-Scholes greeks for arbitrary multi-leg option structures — no market-data lookup, you supply the legs.

```python
pnl = fa.structure_pnl(                                         # Basic+
    legs=[
        {"action": "buy",  "type": "call", "strike": 100, "premium": 3.20},
        {"action": "sell", "type": "call", "strike": 110, "premium": 1.10},
    ],
)
print(pnl["max_profit"], pnl["max_loss"], pnl["breakevens"])
```

### Zero-DTE Flow, Dispersion & Macro

Intraday simulation-aware 0DTE flow (snapshot, series, dealer hedge-flow, per-strike heatmap and strike-flow), full-tape Net Dealer Premium, multi-resolution OHLCV+flow bars, implied-vs-realized correlation for dispersion / vol-arb, VIX-state over/under-vixing regime, liquidity scores, skew term structure, spot-vol correlation, expected move, VRP history, and the curated symbol universe.

```python
snap = fa.flow_zero_dte_snapshot("SPY")                         # Growth+
disp = fa.dispersion(index="SPX", symbols=["AAPL", "MSFT", "NVDA"])  # Alpha+
vix = fa.vix_state()                                            # Growth+
```

### Kelly Criterion Position Sizing

Optimal position sizing using numerical integration over the full lognormal distribution — not the simplified gambling formula.

```python
kelly = fa.kelly(                                            # Growth+
    spot=580, strike=580, dte=30,
    sigma=0.18, premium=12.69, mu=0.12,
)
print(kelly["recommendation"])
print(f"Half-Kelly: {kelly['sizing']['half_kelly_pct']}%")
```

### Market Data

```python
quote = fa.stock_quote("AAPL")                              # Live stock quote
opt = fa.option_quote("SPY", expiry="2026-03-21",           # Option quote (Growth+)
                       strike=660, type="C")
summary = fa.stock_summary("SPY")                           # Comprehensive summary
surface = fa.surface("SPY")                                  # Vol surface (public)
```

### Historical Data (ClickHouse)

Minute-by-minute stock and option quotes from ClickHouse — 3.5 billion rows across 141 tickers.

```python
hist = fa.historical_stock_quote("SPY", date="2026-03-05", time="10:30")
hist_opt = fa.historical_option_quote(
    "SPY", date="2026-03-05", expiry="2026-03-20", strike=580, type="C"
)
```

### Reference Data and Account

```python
tickers = fa.tickers()                # All available stock tickers
chain = fa.options("SPY")             # Option chain metadata
symbols = fa.symbols()                # Symbols with live cached data
account = fa.account()                # Plan, usage, quota
health = fa.health()                  # API health check (public)
```

## Error Handling

```python
from flashalpha import (
    FlashAlpha,
    AuthenticationError,
    TierRestrictedError,
    NotFoundError,
    RateLimitError,
)

fa = FlashAlpha("YOUR_API_KEY")

try:
    data = fa.exposure_summary("SPY")
except AuthenticationError:
    print("Invalid API key")
except TierRestrictedError as e:
    print(f"Need {e.required_plan} plan (you have {e.current_plan})")
except NotFoundError:
    print("Symbol not found")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
```

## API Plans

| Plan | Daily Requests | Access |
|------|---------------|--------|
| **Free** | 5 | Stock quotes, GEX/DEX/VEX/CHEX by strike, levels, BSM greeks, IV, historical quotes, tickers, options meta, surface, stock summary |
| **Basic** | 100 | Everything in Free + index symbols (SPX, VIX, RUT, etc.) |
| **Growth** | 2,500 | + Exposure summary, narrative, 0DTE analytics, volatility analytics, option quotes, full-chain GEX, Kelly sizing |
| **Alpha** | Unlimited | + Advanced volatility (SVI, variance surfaces, arbitrage detection, greeks surfaces, variance swap) |

Get your API key at **[flashalpha.com](https://flashalpha.com)**

## All Methods

| Method | Endpoint | Plan |
|--------|----------|------|
| `fa.gex(symbol)` | Gamma exposure by strike | Free+ |
| `fa.dex(symbol)` | Delta exposure by strike | Free+ |
| `fa.vex(symbol)` | Vanna exposure by strike | Free+ |
| `fa.chex(symbol)` | Charm exposure by strike | Free+ |
| `fa.exposure_levels(symbol)` | Key levels (gamma flip, walls, max pain) | Free+ |
| `fa.exposure_summary(symbol)` | Full exposure summary with hedging | Growth+ |
| `fa.narrative(symbol)` | AI narrative analysis | Growth+ |
| `fa.zero_dte(symbol)` | 0DTE analytics (regime, pin risk, decay) | Growth+ |
| `fa.stock_quote(ticker)` | Live stock quote | Free+ |
| `fa.option_quote(ticker)` | Option quotes with greeks | Growth+ |
| `fa.stock_summary(symbol)` | Comprehensive stock summary | Public/Free+ |
| `fa.surface(symbol)` | Volatility surface grid | Public |
| `fa.historical_stock_quote(ticker)` | Historical stock quotes | Free+ |
| `fa.historical_option_quote(ticker)` | Historical option quotes | Free+ |
| `fa.greeks(...)` | BSM greeks (1st, 2nd, 3rd order) | Free+ |
| `fa.iv(...)` | Implied volatility solver | Free+ |
| `fa.kelly(...)` | Kelly criterion sizing | Growth+ |
| `fa.max_pain(symbol)` | Max pain analysis with dealer alignment, pain curve, pin probability | Growth+ |
| `fa.screener(...)` | **Live options screener** — filter/rank by GEX, VRP, IV, greeks, formulas | Growth+ |
| `fa.volatility(symbol)` | Comprehensive volatility analytics | Growth+ |
| `fa.adv_volatility(symbol)` | SVI, variance surface, arb detection | Alpha+ |
| `fa.tickers()` | All available stock tickers | Free+ |
| `fa.options(ticker)` | Option chain metadata | Free+ |
| `fa.symbols()` | Symbols with live data | Free+ |
| `fa.account()` | Account info and quota | Free+ |
| `fa.health()` | Health check | Public |
| `fa.surface_svi(symbol)` | Live SVI surface params per expiry slice | Alpha+ |
| `fa.exposure_sheet(symbol)` | Unified per-strike GEX/DEX/VEX/CHEX/DAG + Line-in-the-Sand + peaks | Growth+ |
| `fa.exposure_term_structure(symbol)` | Exposure aggregated by DTE bucket and expiry | Growth+ |
| `fa.exposure_basket(symbols)` | Weighted cross-symbol exposure aggregate | Growth+ |
| `fa.exposure_oi_diff(symbol)` | Day-over-day open-interest deltas, top-N | Growth+ |
| `fa.liquidity(symbol)` | Per-expiry execution score and bid-ask spreads | Growth+ |
| `fa.skew_term(symbol)` | 25-delta skew and risk-reversal term structure | Growth+ |
| `fa.spot_vol_correlation(symbol)` | Spot-vol correlation (20d/60d) | Growth+ |
| `fa.dispersion(index, symbols, ...)` | Implied-vs-realized correlation / dispersion vol-arb | Alpha+ |
| `fa.expected_move(symbol)` | Straddle-implied expected move per expiry | Basic+ |
| `fa.realized_volatility(symbol)` | Range-based realized vol estimators (10d/20d/30d) | Alpha+ |
| `fa.volatility_forecast(symbol, dist=...)` | Conditional vol forecasts (EWMA / HAR-RV / GARCH) | Alpha+ |
| `fa.vrp_history(symbol)` | Daily VRP time series for charting/backtesting | Alpha+ |
| `fa.vix_state()` | Over/under-vixing regime (VIX vs SPX realized vol) | Growth+ |
| `fa.universe(...)` | Curated tier-1/tier-2 symbol directory | Public |
| `fa.screener_fields()` | List screener-referenceable fields and types | Free+ |
| `fa.flow_dealer_premium(symbol)` | Full-tape Net Dealer Premium roll-up | Alpha+ |
| `fa.flow_stock_bars(symbol, resolution=...)` | Multi-resolution OHLCV+flow bars | Alpha+ |
| `fa.flow_zero_dte_snapshot(symbol)` | Live intraday 0DTE shape + flow direction | Growth+ |
| `fa.flow_zero_dte_series(symbol)` | Intraday 0DTE metric time series | Growth+ |
| `fa.flow_zero_dte_hedge_flow(symbol)` | Dealer hedge-flow time series (0DTE) | Growth+ |
| `fa.flow_zero_dte_heatmap(symbol)` | Per-strike 0DTE intraday heatmap | Alpha+ |
| `fa.flow_zero_dte_strike_flow(symbol)` | Per-strike signed aggressor 0DTE flow | Alpha+ |
| `fa.strategy_flow_anomaly(symbol)` | Strategy signal: directional flow imbalance | Growth+ |
| `fa.strategy_expiry_positioning(symbol)` | Strategy signal: OPEX pin / iron fly | Basic+ |
| `fa.strategy_zero_dte(symbol)` | Strategy signal: same-day 0DTE range compression | Growth+ (+0DTE) |
| `fa.strategy_dealer_regime(symbol)` | Strategy signal: dealer gamma regime | Growth+ |
| `fa.strategy_vol_carry(symbol)` | Strategy signal: VRP carry / short vol | Alpha+ |
| `fa.strategy_yield_enhancement(symbol)` | Strategy signal: covered call / cash-secured put | Growth+ |
| `fa.strategy_surface_anomaly(symbol)` | Strategy signal: rich/cheap wings vs SVI fit | Alpha+ |
| `fa.strategy_skew(symbol)` | Strategy signal: skew richness | Growth+ |
| `fa.strategy_term_structure(symbol)` | Strategy signal: IV term-structure slope | Growth+ |
| `fa.strategy_tail_pricing(symbol)` | Strategy signal: tail (deep-wing) pricing | Growth+ |
| `fa.earnings_calendar(...)` | Upcoming earnings calendar | Growth+ |
| `fa.earnings_expected_move(symbol)` | Earnings implied-move decomposition | Growth+ |
| `fa.earnings_history(symbol)` | Past earnings: surprises, moves, IV crush | Growth+ |
| `fa.earnings_iv_crush(symbol)` | Expected IV crush + historical distribution | Growth+ |
| `fa.earnings_vrp(symbol)` | Earnings VRP richness assessment | Alpha+ |
| `fa.earnings_dealer_positioning(symbol)` | Dealer positioning into the earnings event | Alpha+ |
| `fa.earnings_strategies(symbol)` | Earnings strategy-suitability scores | Alpha+ |
| `fa.earnings_screener(...)` | Cross-sectional earnings screener | Alpha+ |
| `fa.structure_pnl(legs, ...)` | Multi-leg at-expiry P&L, breakevens, max P/L | Basic+ |
| `fa.structure_greeks(legs, spot=...)` | Aggregate multi-leg Black-Scholes greeks | Basic+ |

## Other SDKs

| Language | Package | Repository |
|----------|---------|------------|
| JavaScript | `npm i flashalpha` | [flashalpha-js](https://github.com/FlashAlpha-lab/flashalpha-js) |
| .NET | `dotnet add package FlashAlpha` | [flashalpha-dotnet](https://github.com/FlashAlpha-lab/flashalpha-dotnet) |
| Java | Maven Central | [flashalpha-java](https://github.com/FlashAlpha-lab/flashalpha-java) |
| Go | `go get github.com/FlashAlpha-lab/flashalpha-go` | [flashalpha-go](https://github.com/FlashAlpha-lab/flashalpha-go) |
| MCP | Claude / LLM tool server | [flashalpha-mcp](https://github.com/FlashAlpha-lab/flashalpha-mcp) |

## Links

- [FlashAlpha](https://flashalpha.com) — API keys, docs, pricing
- [API Documentation](https://flashalpha.com/docs)
- [Examples](https://github.com/FlashAlpha-lab/flashalpha-examples) — runnable tutorials
- [GEX Explained](https://github.com/FlashAlpha-lab/gex-explained) — gamma exposure theory and code
- [0DTE Options Analytics](https://github.com/FlashAlpha-lab/0dte-options-analytics) — 0DTE pin risk, expected move, dealer hedging
- [Volatility Surface Python](https://github.com/FlashAlpha-lab/volatility-surface-python) — SVI calibration, variance swap, skew analysis
- [Awesome Options Analytics](https://github.com/FlashAlpha-lab/awesome-options-analytics) — curated resource list

## License

MIT

## What the Alpha tier unlocks

Free and entry tiers cover live exposure analytics. The **Alpha tier ($1,499/mo)**
adds the data you cannot get anywhere else:

- **Aggregate vanna and charm exposure.** FlashAlpha is the only public source for
  these dealer-positioning aggregates.
- **Point-in-time replay since 2018.** Backtest and trade the same code, with no
  look-ahead and no training-serving skew.
- **SVI vol surfaces, VRP analytics, higher-order Greeks**, uncached and unlimited.

Built for quants, prop desks, and vol funds. See the full picture and get a key:
**[flashalpha.com/for-quant-teams](https://flashalpha.com/for-quant-teams?utm_source=github&utm_medium=readme&utm_campaign=repo-flashalpha-python)**
