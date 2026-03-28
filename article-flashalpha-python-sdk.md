# FlashAlpha Python SDK: Open-Source Tools for Options Analytics

FlashAlpha provides a REST API for real-time options exposure analytics — gamma exposure (GEX), delta exposure (DEX), vanna exposure (VEX), charm exposure (CHEX), Black-Scholes greeks, implied volatility, 0DTE analytics, volatility surfaces, and dealer positioning data.

To make the API accessible to Python developers, we've published an open-source SDK and a collection of educational repositories on GitHub. This article covers what's available, how to use it, and what each repo is for.

---

## The SDK: `pip install flashalpha`

The Python SDK is a thin wrapper around the FlashAlpha REST API. It handles authentication, error handling, and returns typed Python dicts instead of raw JSON.

**Install:**

```bash
pip install flashalpha
```

**Quick start:**

```python
from flashalpha import FlashAlpha

fa = FlashAlpha("YOUR_API_KEY")

# Gamma exposure by strike
gex = fa.gex("SPY")
print(f"Net GEX: ${gex['net_gex']:,.0f}")
print(f"Gamma flip: {gex['gamma_flip']}")
```

**PyPI:** [pypi.org/project/flashalpha](https://pypi.org/project/flashalpha/)
**Source:** [github.com/FlashAlpha-lab/flashalpha-python](https://github.com/FlashAlpha-lab/flashalpha-python)

### What's Covered

The SDK wraps every live endpoint in the FlashAlpha API:

| Category | Methods | Plan |
|----------|---------|------|
| **Exposure analytics** | `gex()`, `dex()`, `vex()`, `chex()`, `exposure_levels()`, `exposure_summary()`, `narrative()` | Free+ / Growth+ |
| **0DTE analytics** | `zero_dte()` | Growth+ |
| **Market data** | `stock_quote()`, `option_quote()`, `stock_summary()`, `surface()` | Free+ / Growth+ |
| **Historical data** | `historical_stock_quote()`, `historical_option_quote()` | Free+ |
| **Pricing** | `greeks()`, `iv()`, `kelly()` | Free+ / Growth+ |
| **Volatility** | `volatility()`, `adv_volatility()` | Growth+ / Alpha+ |
| **Reference** | `tickers()`, `options()`, `symbols()`, `account()`, `health()` | Free+ |

### Error Handling

The SDK raises specific exceptions for each error type:

```python
from flashalpha import (
    FlashAlpha,
    AuthenticationError,    # 401 — invalid API key
    TierRestrictedError,    # 403 — endpoint requires higher plan
    NotFoundError,          # 404 — symbol not found
    RateLimitError,         # 429 — daily quota exceeded
)

try:
    data = fa.exposure_summary("SPY")
except TierRestrictedError as e:
    print(f"Need {e.required_plan} plan (you have {e.current_plan})")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
```

---

## Gamma Exposure Explained

**Repo:** [github.com/FlashAlpha-lab/gex-explained](https://github.com/FlashAlpha-lab/gex-explained)

This repo explains what gamma exposure is, how to calculate it from raw options data, and how to use it for trading. It includes both theory (markdown articles) and runnable Python code.

### Theory

- **What is gamma exposure** — the formula, the intuition, why it matters for price action
- **Dealer hedging mechanics** — how market makers hedge, why positive gamma dampens moves and negative gamma amplifies them
- **GEX regimes** — what happens above vs below the gamma flip level

### Code Examples

| File | What it does |
|------|-------------|
| `compute_gex.py` | Calculates GEX from a raw options chain — the full formula from scratch |
| `gamma_exposure_by_strike.py` | Pulls GEX by strike from the API and displays a per-strike breakdown |
| `gamma_flip_level_tracker.py` | Tracks gamma flip, call wall, put wall, max pain, and 0DTE magnet |
| `call_wall_put_wall_finder.py` | Scans multiple symbols (SPY, QQQ, AAPL, TSLA, NVDA) for support/resistance levels |
| `dealer_hedging_flow_analysis.py` | Shows estimated dealer hedging flows at +/-1% spot moves |
| `gex_trading_spy_tsla_qqq.py` | Full GEX analysis across SPY, TSLA, QQQ — regime, levels, narrative |
| `exposure_narrative_analysis.py` | AI-generated exposure narrative — regime, flow, vanna, charm, outlook |
| `delta_vanna_charm_exposure.py` | DEX, VEX, CHEX analysis — second-order exposure beyond gamma |

### Example: Key Levels

```python
from flashalpha import FlashAlpha

fa = FlashAlpha("YOUR_API_KEY")

levels = fa.exposure_levels("SPY")
lvl = levels["levels"]
print(f"Gamma flip: {lvl['gamma_flip']}")
print(f"Call wall:  {lvl['call_wall']}  (resistance)")
print(f"Put wall:   {lvl['put_wall']}   (support)")
print(f"Max pain:   {lvl['max_pain']}")
```

**Further reading:** [GEX Trading Guide — How to Read and Trade Gamma Exposure](https://flashalpha.com/articles/gex-trading-guide-gamma-exposure-api-spy-tsla)

---

## 0DTE Options Analytics

**Repo:** [github.com/FlashAlpha-lab/0dte-options-analytics](https://github.com/FlashAlpha-lab/0dte-options-analytics)

Zero-days-to-expiration (0DTE) options now account for over 40% of SPX options volume on some days. This repo provides Python examples for analyzing 0DTE dynamics in real time: pin risk, expected move, gamma regime, dealer hedging, and theta decay.

### Why 0DTE Matters

0DTE options behave differently from longer-dated contracts:

- **Gamma is 2-10x higher** than equivalent 7DTE options — small spot moves create large hedging flows
- **Theta accelerates exponentially** — a $5 option at 9:30 AM can be worth $0.10 by 3:30 PM
- **Pin risk is real** — high OI concentration at round strikes creates "magnetic" price action
- **Expected move shrinks in real time** — remaining 1SD at 3:00 PM is much smaller than at open

### Code Examples

| File | What it does |
|------|-------------|
| `0dte_pin_risk_analysis.py` | Pin score (0-100), magnet strike, OI concentration, max pain |
| `0dte_expected_move_calculator.py` | Full-day and remaining 1SD, straddle price, upper/lower bounds |
| `0dte_gamma_regime_tracker.py` | Positive vs negative gamma, gamma flip, % of total GEX from 0DTE |
| `0dte_dealer_hedging_flows.py` | Dealer hedging at +/-0.5% and +/-1% moves (shares, notional, direction) |
| `0dte_theta_decay_monitor.py` | Net theta, theta per hour remaining, charm regime, gamma acceleration |
| `0dte_spy_intraday_playbook.py` | Complete intraday report combining all sections |
| `0dte_trading_strategies.py` | 5 strategies: pin play, gamma scalp, vol crush, momentum fade, straddle |
| `0dte_vol_context_analysis.py` | 0DTE vs 7DTE IV ratio, VIX, vanna exposure, vol regime |

### Example: Pin Risk

```python
from flashalpha import FlashAlpha

fa = FlashAlpha("YOUR_API_KEY")

dte = fa.zero_dte("SPY")
pin = dte["pin_risk"]
print(f"Pin score:     {pin['pin_score']}/100")
print(f"Magnet strike: {pin['magnet_strike']}")
print(f"Distance:      {pin['distance_to_magnet_pct']:.2f}%")
print(f"Max pain:      {pin['max_pain']}")
print(f"Top 3 OI:      {pin['oi_concentration_top3_pct']:.1f}%")
```

A pin score above 70 with spot within 0.15% of the magnet strike suggests a high probability of pinning near that strike into close.

### Example: Expected Move (Time-Adjusted)

```python
em = dte["expected_move"]
print(f"Full-day 1SD:      +/-${em['implied_1sd_dollars']:.2f}")
print(f"Remaining 1SD:     +/-${em['remaining_1sd_dollars']:.2f}")
print(f"Range:             ${em['lower_bound']:.2f} - ${em['upper_bound']:.2f}")
print(f"ATM straddle:      ${em['straddle_price']:.2f}")
```

The remaining expected move shrinks as the day progresses. At 3:00 PM, it's roughly 27% of the full-day move. This is how 0DTE straddle sellers profit — they sell the full implied move and collect as theta decays it.

**Further reading:**
- [0DTE SPY: The Complete Intraday Playbook](https://flashalpha.com/articles/0dte-spy-complete-intraday-playbook-same-day-options)
- [0DTE Gamma Exposure and Pin Risk](https://flashalpha.com/articles/0dte-gamma-exposure-pin-risk-intraday-options-analytics)
- [Guide to 0DTE Trading Strategies](https://flashalpha.com/articles/guide-to-0dte-trading-strategies-real-time-data)

---

## Volatility Surface Analysis

**Repo:** [github.com/FlashAlpha-lab/volatility-surface-python](https://github.com/FlashAlpha-lab/volatility-surface-python)

This repo covers implied volatility surface construction, SVI calibration, variance swap pricing, arbitrage detection, and volatility analytics. It targets the Alpha tier of the API, which provides raw SVI parameters, total variance grids, and higher-order greeks surfaces.

### What's an Implied Volatility Surface?

An implied volatility surface maps IV across two dimensions: strike (or moneyness) and expiration. It reveals the market's view of risk across different outcomes and time horizons. Key features:

- **Skew** — puts trade at higher IV than calls (crash protection premium)
- **Term structure** — near-term vs long-term IV (contango = calm, backwardation = fear)
- **Smile** — deep OTM options on both sides trade at higher IV than ATM

### SVI Parameterization

The API fits Gatheral's SVI (Stochastic Volatility Inspired) model to each expiry slice:

```
w(k) = a + b(rho(k - m) + sqrt((k - m)^2 + sigma^2))
```

Where `k` is log-moneyness, and `a`, `b`, `rho`, `m`, `sigma` are the five SVI parameters. This gives a smooth, arbitrage-constrained representation of the smile.

### Code Examples

| File | What it does |
|------|-------------|
| `implied_volatility_surface.py` | Total variance surface grid — moneyness x expiry |
| `svi_calibration_example.py` | Raw SVI parameters per expiry with analytical smile reconstruction |
| `variance_swap_pricing.py` | Fair variance, fair vol, convexity adjustment per expiry |
| `volatility_skew_analysis.py` | 10-delta/25-delta put/call skew, risk reversal, smile ratio |
| `realized_vs_implied_volatility.py` | RV across 5 windows, VRP, and strategy guidance |
| `volatility_term_structure.py` | Contango/backwardation shape, near/far slope |
| `arbitrage_detection_butterfly_calendar.py` | Butterfly and calendar arbitrage violations |
| `greeks_surface_vanna_charm.py` | Vanna, charm, volga, speed surfaces across strikes and expiries |
| `iv_rank_scanner.py` | Multi-symbol IV rank scanner |
| `vol_risk_premium_analysis.py` | Deep-dive VRP analysis with trade signals |
| `forward_implied_volatility.py` | Implied forward prices and cost-of-carry basis |

### Example: SVI Parameters

```python
from flashalpha import FlashAlpha

fa = FlashAlpha("YOUR_API_KEY")

adv = fa.adv_volatility("SPY")
for s in adv["svi_parameters"]:
    print(f"{s['expiry']} ({s['days_to_expiry']}d)")
    print(f"  a={s['a']:.6f}  b={s['b']:.6f}  rho={s['rho']:.4f}")
    print(f"  m={s['m']:.6f}  sigma={s['sigma']:.6f}")
    print(f"  ATM IV: {s['atm_iv']:.2f}%  Forward: {s['forward']:.2f}")
```

### Example: Realized vs Implied Volatility

```python
vol = fa.volatility("TSLA")
print(f"ATM IV:     {vol['atm_iv']:.1f}%")
print(f"RV 20d:     {vol['realized_vol']['rv_20d']:.1f}%")
print(f"VRP:        {vol['iv_rv_spreads']['vrp_20d']:.1f}%")
print(f"Assessment: {vol['iv_rv_spreads']['assessment']}")
```

When IV is significantly above realized vol (positive VRP), options are "expensive" — favoring premium sellers. When VRP is negative, options are cheap relative to actual moves.

**Further reading:**
- [Advanced Volatility API: SVI, Variance Surface, Arbitrage Detection](https://flashalpha.com/articles/advanced-volatility-api-svi-variance-surface-arbitrage-detection)
- [Realized vs Implied Volatility Risk Premium](https://flashalpha.com/articles/realized-vs-implied-volatility-risk-premium)
- [Volatility Term Structure: Contango, Backwardation, and Events](https://flashalpha.com/articles/volatility-term-structure-contango-backwardation-events)

---

## More Examples

**Repo:** [github.com/FlashAlpha-lab/flashalpha-examples](https://github.com/FlashAlpha-lab/flashalpha-examples)

Runnable Python examples covering the full API:

| Example | What it shows |
|---------|-------------|
| `01_quick_start.py` | First API call — GEX for SPY in 3 lines |
| `02_gex_dashboard.py` | GEX dashboard with levels and regime |
| `03_iv_rank_scanner.py` | IV rank scanner across multiple symbols |
| `04_vol_surface_3d.py` | 3D volatility surface visualization |
| `05_dealer_positioning.py` | Dealer positioning analysis with hedging estimates |
| `06_kelly_sizing.py` | Kelly criterion position sizing for options |
| `07_zero_dte_analytics.py` | 0DTE intraday analysis |
| `08_advanced_volatility.py` | SVI parameters, variance surface, arbitrage detection |
| `09_volatility_analysis.py` | Comprehensive volatility analysis |

---

## API Plans

| Plan | Daily Requests | Access |
|------|---------------|--------|
| **Free** | 10 | Stock quotes, GEX/DEX/VEX/CHEX by strike, levels, BSM greeks, IV, historical quotes, vol surface, stock summary |
| **Basic** | 250 | Everything in Free + index symbols (SPX, VIX, RUT) |
| **Growth** | 2,500 | + Exposure summary, narrative, 0DTE analytics, volatility analytics, option quotes, full-chain GEX, Kelly sizing |
| **Alpha** | Unlimited | + Advanced volatility (SVI parameters, variance surfaces, arbitrage detection, greeks surfaces, variance swap pricing) |

Get your free API key at [flashalpha.com](https://flashalpha.com).

---

## Test Coverage

Every repo includes comprehensive unit tests (mocked, no API key needed) and integration tests (live API). Total across all repos:

| Repo | Unit tests | Integration tests |
|------|-----------|------------------|
| flashalpha-python | 36 | 23 |
| 0dte-options-analytics | 27 | 15 |
| gex-explained | 44 | 18 |
| volatility-surface-python | 20 | 15 |
| **Total** | **127** | **71** |

---

## Links

- [FlashAlpha](https://flashalpha.com) — API keys, docs, pricing
- [API Documentation](https://flashalpha.com/docs)
- [Python SDK (PyPI)](https://pypi.org/project/flashalpha/)
- [GitHub Organization](https://github.com/FlashAlpha-lab)

### All Repositories

| Repo | Description |
|------|-------------|
| [flashalpha-python](https://github.com/FlashAlpha-lab/flashalpha-python) | Python SDK — `pip install flashalpha` |
| [gex-explained](https://github.com/FlashAlpha-lab/gex-explained) | Gamma exposure theory, math, and Python code |
| [0dte-options-analytics](https://github.com/FlashAlpha-lab/0dte-options-analytics) | 0DTE pin risk, expected move, dealer hedging, theta decay |
| [volatility-surface-python](https://github.com/FlashAlpha-lab/volatility-surface-python) | SVI calibration, variance swap, skew, term structure |
| [flashalpha-examples](https://github.com/FlashAlpha-lab/flashalpha-examples) | Runnable examples and tutorials |
| [awesome-options-analytics](https://github.com/FlashAlpha-lab/awesome-options-analytics) | Curated list of options analytics resources |

### Articles

- [GEX Trading Guide — How to Read and Trade Gamma Exposure](https://flashalpha.com/articles/gex-trading-guide-gamma-exposure-api-spy-tsla)
- [0DTE SPY: The Complete Intraday Playbook](https://flashalpha.com/articles/0dte-spy-complete-intraday-playbook-same-day-options)
- [0DTE Gamma Exposure and Pin Risk](https://flashalpha.com/articles/0dte-gamma-exposure-pin-risk-intraday-options-analytics)
- [Guide to 0DTE Trading Strategies](https://flashalpha.com/articles/guide-to-0dte-trading-strategies-real-time-data)
- [Advanced Volatility API: SVI, Variance Surface, Arbitrage Detection](https://flashalpha.com/articles/advanced-volatility-api-svi-variance-surface-arbitrage-detection)
- [Realized vs Implied Volatility Risk Premium](https://flashalpha.com/articles/realized-vs-implied-volatility-risk-premium)
- [Volatility Term Structure: Contango, Backwardation, and Events](https://flashalpha.com/articles/volatility-term-structure-contango-backwardation-events)
