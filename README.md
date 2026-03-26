# FlashAlpha Python SDK

[![PyPI](https://img.shields.io/pypi/v/flashalpha)](https://pypi.org/project/flashalpha/)
[![Python](https://img.shields.io/pypi/pyversions/flashalpha)](https://pypi.org/project/flashalpha/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/FlashAlpha-lab/flashalpha-python/actions/workflows/ci.yml/badge.svg)](https://github.com/FlashAlpha-lab/flashalpha-python/actions/workflows/ci.yml)

**Python client for the FlashAlpha options analytics API.** Access real-time gamma exposure (GEX), delta exposure (DEX), vanna exposure (VEX), charm exposure (CHEX), 0DTE analytics, Black-Scholes greeks, implied volatility, volatility surfaces, dealer positioning, Kelly criterion sizing, and more — all from Python.

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

Get your free API key at [flashalpha.com](https://flashalpha.com) — 10 requests/day, no credit card.

## Features

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
| **Free** | 10 | Stock quotes, GEX/DEX/VEX/CHEX by strike, levels, BSM greeks, IV, historical quotes, tickers, options meta, surface, stock summary |
| **Basic** | 250 | Everything in Free + index symbols (SPX, VIX, RUT, etc.) |
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
| `fa.exposure_history(symbol)` | Daily exposure snapshots | Growth+ |
| `fa.stock_quote(ticker)` | Live stock quote | Free+ |
| `fa.option_quote(ticker)` | Option quotes with greeks | Growth+ |
| `fa.stock_summary(symbol)` | Comprehensive stock summary | Public/Free+ |
| `fa.surface(symbol)` | Volatility surface grid | Public |
| `fa.historical_stock_quote(ticker)` | Historical stock quotes | Free+ |
| `fa.historical_option_quote(ticker)` | Historical option quotes | Free+ |
| `fa.greeks(...)` | BSM greeks (1st, 2nd, 3rd order) | Free+ |
| `fa.iv(...)` | Implied volatility solver | Free+ |
| `fa.kelly(...)` | Kelly criterion sizing | Growth+ |
| `fa.volatility(symbol)` | Comprehensive volatility analytics | Growth+ |
| `fa.adv_volatility(symbol)` | SVI, variance surface, arb detection | Alpha+ |
| `fa.tickers()` | All available stock tickers | Free+ |
| `fa.options(ticker)` | Option chain metadata | Free+ |
| `fa.symbols()` | Symbols with live data | Free+ |
| `fa.account()` | Account info and quota | Free+ |
| `fa.health()` | Health check | Public |

## Links

- [FlashAlpha](https://flashalpha.com) — API keys, docs, pricing
- [API Documentation](https://flashalpha.com/docs)
- [GEX Explained](https://github.com/FlashAlpha-lab/gex-explained) — gamma exposure theory and code
- [0DTE Options Analytics](https://github.com/FlashAlpha-lab/0dte-options-analytics) — 0DTE pin risk, expected move, dealer hedging
- [Volatility Surface Python](https://github.com/FlashAlpha-lab/volatility-surface-python) — SVI calibration, variance swap, skew analysis
- [Examples](https://github.com/FlashAlpha-lab/flashalpha-examples) — runnable tutorials
- [Awesome Options Analytics](https://github.com/FlashAlpha-lab/awesome-options-analytics) — curated resource list

## License

MIT
