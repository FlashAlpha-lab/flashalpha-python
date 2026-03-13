# FlashAlpha Python SDK

[![PyPI](https://img.shields.io/pypi/v/flashalpha)](https://pypi.org/project/flashalpha/)
[![Python](https://img.shields.io/pypi/pyversions/flashalpha)](https://pypi.org/project/flashalpha/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Real-time options exposure analytics for Python.** Gamma exposure (GEX), delta (DEX), vanna (VEX), charm (CHEX), key levels, Black-Scholes greeks, implied volatility, Kelly sizing, and more — from the [FlashAlpha API](https://flashalpha.com).

```bash
pip install flashalpha
```

## Quick Start

```python
from flashalpha import FlashAlpha

fa = FlashAlpha("YOUR_API_KEY")

# Get gamma exposure for SPY
gex = fa.gex("SPY")
print(f"Net GEX: ${gex['net_gex']:,.0f}")
print(f"Gamma flip: {gex['gamma_flip']}")

for strike in gex["strikes"][:5]:
    print(f"  {strike['strike']}: net ${strike['net_gex']:,.0f}")
```

## What You Can Do

### Exposure Analytics — see where dealers are positioned

```python
# Gamma exposure by strike
gex = fa.gex("SPY")
gex = fa.gex("TSLA", expiration="2026-03-21", min_oi=100)

# Delta, vanna, charm exposure
dex = fa.dex("AAPL")
vex = fa.vex("QQQ")
chex = fa.chex("NVDA")

# Key levels (gamma flip, walls, max pain)
levels = fa.exposure_levels("SPY")
print(f"Call wall: {levels['levels']['call_wall']}")
print(f"Put wall: {levels['levels']['put_wall']}")
print(f"Gamma flip: {levels['levels']['gamma_flip']}")

# Full exposure summary with hedging estimates
summary = fa.exposure_summary("SPY")  # Growth+

# AI narrative analysis
narrative = fa.narrative("SPY")  # Growth+
print(narrative["narrative"]["regime"])
print(narrative["narrative"]["outlook"])
```

### Market Data — live quotes and option chains

```python
# Stock quote
quote = fa.stock_quote("AAPL")
print(f"AAPL: ${quote['mid']}")

# Option quote with greeks
opt = fa.option_quote("SPY", expiry="2026-03-21", strike=660, type="C")  # Growth+
print(f"Delta: {opt['delta']}, IV: {opt['implied_vol']}")

# Comprehensive stock summary (price, vol, exposure, macro)
summary = fa.stock_summary("SPY")

# Vol surface (public — no API key needed)
surface = fa.surface("SPY")
```

### Pricing — Black-Scholes greeks and implied vol

```python
# Full BSM greeks (first, second, third order)
g = fa.greeks(spot=580, strike=580, dte=30, sigma=0.18, type="call")
print(f"Delta: {g['first_order']['delta']}")
print(f"Gamma: {g['first_order']['gamma']}")
print(f"Vanna: {g['second_order']['vanna']}")

# Implied volatility from market price
result = fa.iv(spot=580, strike=580, dte=30, price=12.69)
print(f"IV: {result['implied_volatility_pct']}%")

# Kelly criterion position sizing
kelly = fa.kelly(  # Growth+
    spot=580, strike=580, dte=30,
    sigma=0.18, premium=12.69, mu=0.12,
)
print(kelly["recommendation"])
```

### Volatility Analytics — skew, term structure, realized vol

```python
vol = fa.volatility("TSLA")  # Growth+
print(f"ATM IV: {vol['atm_iv']}%")
print(f"RV 20d: {vol['realized_vol']['rv_20d']}%")
print(f"VRP assessment: {vol['iv_rv_spreads']['assessment']}")
```

### Historical Data — minute-by-minute from ClickHouse

```python
# Historical stock quotes
hist = fa.historical_stock_quote("SPY", date="2026-03-05", time="10:30")

# Historical option quotes
hist_opt = fa.historical_option_quote(
    "SPY", date="2026-03-05", expiry="2026-03-20", strike=580, type="C"
)
```

### Reference & Account

```python
# All available tickers
tickers = fa.tickers()

# Option chain metadata (expirations + strikes)
chain = fa.options("SPY")

# Symbols with live cached data
symbols = fa.symbols()

# Account info and quota
account = fa.account()
print(f"Plan: {account['plan']}, Remaining: {account['remaining']}")
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

## Plans

| Plan | Daily Requests | Highlights |
|------|---------------|------------|
| **Free** | 50 | Stock quotes, GEX/DEX/VEX/CHEX by strike, levels, greeks, IV, tickers |
| **Basic** | 250 | Everything in Free |
| **Growth** | 2,500 | + Option quotes, exposure summary, narrative, volatility, Kelly sizing |
| **Pro** | Unlimited | Full access |

**Get your API key at [flashalpha.com](https://flashalpha.com)**

## Links

- [API Documentation](https://flashalpha.com/docs)
- [Interactive Playground](https://lab.flashalpha.com/swagger)
- [GitHub](https://github.com/FlashAlpha/flashalpha-python)
