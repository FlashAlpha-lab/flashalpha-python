# FlashAlpha API Documentation

Real-time options exposure analytics. Live gamma (GEX), delta (DEX), vanna (VEX), and charm (CHEX) exposure data, key levels, dealer hedging estimates, and verbal narrative analysis — all derived from live options flow.

---

## Playground

Try the API right now — no setup required.

Open the [interactive playground](https://lab.flashalpha.com/swagger) to browse endpoints, send requests, and inspect live responses directly in your browser.

Enter your API key in the **Authorize** button at the top, then expand any endpoint and click **Try it out**.

---

## Quick Start

**1. Get your API key** from [flashalpha.com](https://flashalpha.com)

**2. Make your first call:**

```bash
curl -H "X-Api-Key: YOUR_API_KEY" https://lab.flashalpha.com/v1/exposure/gex/SPY
```

**3. Explore the response** — you'll get gamma exposure by strike with OI, volume, and day-over-day changes.

That's it. Every US equity and ETF symbol is supported. Data is fetched on-demand with a 15-second cache.

---

## Authentication

All endpoints (except `/health`, `/v1/surface`, and unauthenticated `/v1/stock/{symbol}/summary`) require an API key. Pass it in the `X-Api-Key` header:

```bash
curl -H "X-Api-Key: YOUR_API_KEY" https://lab.flashalpha.com/v1/symbols
```

Or as a query parameter:

```
https://lab.flashalpha.com/v1/symbols?apiKey=YOUR_API_KEY
```

---

## Endpoints

### Market Data

- [`GET /stockquote/{ticker}`](#get-stockquoteticker) — Live stock quote `Free+`
- [`GET /optionquote/{ticker}`](#get-optionquoteticker) — Option quotes with greeks `Growth+`
- [`GET /v1/surface/{symbol}`](#get-v1surfacesymbol) — Vol surface grid `Public`
- [`GET /v1/stock/{symbol}/summary`](#get-v1stocksymbolsummary) — Comprehensive stock summary `Public` (cached) / `Free+` (live)

### Exposure Analytics

- [`GET /v1/exposure/gex/{symbol}`](#get-v1exposuregexsymbol) — Gamma exposure by strike `Free+` (single expiry) / `Growth+` (full chain)
- [`GET /v1/exposure/dex/{symbol}`](#get-v1exposuredexsymbol) — Delta exposure by strike `Basic+`
- [`GET /v1/exposure/vex/{symbol}`](#get-v1exposurevexsymbol) — Vanna exposure by strike `Basic+`
- [`GET /v1/exposure/chex/{symbol}`](#get-v1exposurechexsymbol) — Charm exposure by strike `Basic+`
- [`GET /v1/exposure/summary/{symbol}`](#get-v1exposuresummarysymbol) — Full exposure summary `Growth+`
- [`GET /v1/exposure/levels/{symbol}`](#get-v1exposurelevelssymbol) — Key support/resistance levels `Free+`
- [`GET /v1/exposure/narrative/{symbol}`](#get-v1exposurenarrativesymbol) — Verbal narrative analysis `Growth+`
- [`GET /v1/exposure/zero-dte/{symbol}`](#get-v1exposurezero-dtesymbol) — Real-time 0DTE analytics `Growth+`
- [`GET /v1/maxpain/{symbol}`](#get-v1maxpainsymbol) — Max pain analysis with dealer alignment `Basic+`
- [`GET /v1/exposure/history/{symbol}`](#get-v1exposurehistorysymbol) — Daily exposure history `Growth+` *(coming soon)*

### Pricing & Sizing

- [`GET /v1/pricing/greeks`](#get-v1pricinggreeks) — Full BSM greeks (first, second, third order) `Free+`
- [`GET /v1/pricing/iv`](#get-v1pricingiv) — Implied volatility from market price `Free+`
- [`GET /v1/pricing/kelly`](#get-v1pricingkelly) — Kelly criterion sizing for options `Growth+`

### Volatility Analytics

- [`GET /v1/volatility/{symbol}`](#get-v1volatilitysymbol) — Comprehensive volatility analysis `Growth+`
- [`GET /v1/adv_volatility/{symbol}`](#get-v1adv_volatilitysymbol) — Advanced volatility analytics (SVI, variance surface, arb detection, greeks surfaces, var swap) `Alpha+`

### VRP Analytics

- [`GET /v1/vrp/{symbol}`](#get-v1vrpsymbol) — Volatility Risk Premium dashboard (VRP spreads, z-score, percentile, directional VRP, term structure, GEX-conditioned regime, strategy scores, dealer risk, warnings, macro context) `Alpha+`
- [`GET /v1/vrp/{symbol}/history`](#get-v1vrpsymbolhistory) — Daily VRP time series for charting and backtesting `Alpha+`

### Reference Data

- [`GET /v1/tickers`](#get-v1tickers) — All available stock tickers `Free+`
- [`GET /v1/options/{ticker}`](#get-v1optionsticker) — Option chain metadata (expirations + strikes) `Free+`
- [`GET /v1/symbols`](#get-v1symbols) — Currently queried symbols with live data `Free+`

### Account & System

- [`GET /v1/account`](#get-v1account) — Account info and quota `Free+`
- [`GET /health`](#get-health) — Health check `Public`

---

## Rate Limits & Plans

Every authenticated response includes rate limit headers:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Max requests per day (or `unlimited`) |
| `X-RateLimit-Remaining` | Requests remaining today |
| `X-RateLimit-Reset` | Unix timestamp when quota resets |
| `Retry-After` | Seconds to wait (only on 429) |

### Plans

| Plan | Daily Requests | Access |
|------|---------------|--------|
| Free | 5 | Stock quotes, gamma exposure by strike (GEX, levels), BSM greeks, IV solver, tickers, options meta, symbols, surface, stock summary (cached for unauthenticated, live for authenticated) |
| Basic | 100 | Everything in Free + delta/vanna/charm exposure (DEX/VEX/CHEX) + index symbols + max pain analysis |
| Growth | 2,500 | + Exposure summary, narrative, history, 0DTE analytics, volatility analytics, option quotes, full-chain GEX (no expiry filter), Kelly sizing |
| Alpha | Unlimited | + Advanced volatility (SVI, variance surfaces, arbitrage detection, greeks surfaces, var swap), VRP analytics (risk premium, z-score, percentile, directional VRP, term structure, GEX/vanna-conditioned regime, strategy suitability scores, dealer flow risk, macro context), SVI-smoothed IV on option quotes |
| Enterprise | Unlimited | Full access + admin endpoints |

### Index Symbols

Index symbols (SPX, VIX, RUT, DJX, DJI, OEX, XSP, XEO, SPXW, MRUT, MNX, VVIX, RVX, VXST, VXEEM, GVZ, OVX, TYVIX, SRVIX, SKEW, BSZ, BVZ, TNX, TYX, FVX, IRX, MXEA, MXEF) require the **Basic plan or higher** on any endpoint. Free-tier requests for index symbols return `403`.

### 0DTE Access

Requests with `?expiration=` set to today's date (0DTE) require the **Growth plan or higher**. This applies to GEX, DEX, VEX, CHEX, and Levels endpoints. Non-0DTE expiration filters are available on all plans. Users who subscribed before 2026-03-20 are grandfathered and retain 0DTE access on their current plan.

---

## `GET /stockquote/{ticker}`

Returns the current bid, ask, mid, and last price for a symbol.

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `ticker` | path | yes | Stock symbol (e.g. `SPY`, `QQQ`, `AAPL`) |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" https://lab.flashalpha.com/stockquote/SPY
```

### Response `200`

```json
{
  "ticker": "SPY",
  "bid": 597.50,
  "ask": 597.51,
  "mid": 597.505,
  "lastPrice": 597.505,
  "lastUpdate": "2026-02-28T16:30:45Z"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | No quote available for symbol |

---

## `GET /optionquote/{ticker}`

Returns option quotes enriched with BSM greeks, open interest, and volume.

- **No filters** → returns all contracts for the symbol (array)
- **Partial filters** → returns matching subset (array)
- **All three filters** → returns a single contract (object)

**Requires Growth plan or higher.** The `svi_vol` field (SVI-smoothed implied volatility) requires the **Alpha plan or higher** — on lower tiers it returns `null` with `"svi_vol_gated": "requires_alpha_tier"`.

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `ticker` | path | yes | Underlying symbol |
| `expiry` | query | no | Expiration date (`yyyy-MM-dd`) |
| `strike` | query | no | Strike price |
| `type` | query | no | `C` / `Call` or `P` / `Put` |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/optionquote/SPY?expiry=2026-03-20&strike=590&type=C"
```

### Response `200`

```json
{
  "underlying": "SPY",
  "type": "C",
  "expiry": "2026-03-20",
  "strike": 590.0,
  "bid": 15.25,
  "ask": 15.35,
  "mid": 15.30,
  "bidSize": 1200,
  "askSize": 1500,
  "lastUpdate": "2026-02-28T16:30:45Z",
  "implied_vol": 0.1823,
  "delta": 0.6543,
  "gamma": 0.0089,
  "theta": -0.0234,
  "vega": 0.0456,
  "rho": 0.1234,
  "vanna": 0.0078,
  "charm": -0.0045,
  "svi_vol": 0.1820,
  "open_interest": 45000,
  "volume": 3250
}
```

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid expiry format or invalid type |
| `403` | Requires Growth plan or higher |
| `404` | No matching options found |

---

## `GET /v1/surface/{symbol}`

Returns the cached volatility surface grid for a symbol. **Public endpoint — no authentication required.**

The surface is pre-computed from SVI fits and cached in the database. Updated periodically during market hours.

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `symbol` | path | yes | Underlying symbol (e.g. `SPY`) |

### Example

```bash
curl https://lab.flashalpha.com/v1/surface/SPY
```

### Response `200`

Returns the cached JSON response containing the vol surface grid data.

### Errors

| Status | Description |
|--------|-------------|
| `503` | Surface data is still loading — try again shortly |

---

## `GET /v1/stock/{symbol}/summary`

Returns a comprehensive stock summary: price, ATM IV, historical volatility, vol risk premium, 25-delta skew, IV term structure, options flow (OI, volume, put/call ratios), exposure data (GEX/DEX/VEX/CHEX, gamma flip, walls, max pain, hedging estimates, zero-DTE, top strikes, regime), and macro context (VIX, VVIX, SKEW, SPX, MOVE, VIX term structure, VIX futures basis, Fear & Greed index).

**Dual access:**
- **Authenticated** — returns live, real-time data computed on the spot
- **Unauthenticated (no API key)** — returns the previous day's cached snapshot from the database (populated daily at market open)

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `symbol` | path | yes | Underlying symbol (e.g. `SPY`) |

### Example (authenticated — live data)

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/stock/SPY/summary"
```

### Example (unauthenticated — previous day snapshot)

```bash
curl "https://lab.flashalpha.com/v1/stock/SPY/summary"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "as_of": "2026-03-06T14:30:00Z",
  "market_open": true,
  "price": {
    "bid": 580.50,
    "ask": 580.52,
    "mid": 580.51,
    "last": 580.51,
    "last_update": "2026-03-06T14:30:00Z"
  },
  "volatility": {
    "atm_iv": 18.45,
    "hv_20": 15.32,
    "hv_60": 16.78,
    "vrp": 3.13,
    "skew_25d": {
      "expiry": "2026-03-14",
      "days_to_expiry": 8,
      "put_25d_iv": 20.12,
      "atm_iv": 18.45,
      "call_25d_iv": 17.10,
      "skew_25d": 3.02,
      "smile_ratio": 1.177
    },
    "iv_term_structure": [
      { "expiry": "2026-03-14", "iv": 17.8, "days_to_expiry": 8 },
      { "expiry": "2026-03-21", "iv": 18.2, "days_to_expiry": 15 }
    ]
  },
  "options_flow": {
    "total_call_oi": 12500000,
    "total_put_oi": 9800000,
    "total_call_volume": 850000,
    "total_put_volume": 620000,
    "pc_ratio_oi": 0.784,
    "pc_ratio_volume": 0.729,
    "active_expirations": 12
  },
  "exposure": {
    "net_gex": 2850000000,
    "net_dex": -450000000,
    "net_vex": 1200000000,
    "net_chex": 850000000,
    "gamma_flip": 575.25,
    "call_wall": 585.0,
    "put_wall": 570.0,
    "max_pain": 578.0,
    "highest_oi_strike": 580.0,
    "regime": "positive_gamma",
    "interpretation": {
      "gamma": "Dealers long gamma — expect range-bound, mean-reverting price action",
      "vanna": "Positive vanna — benefits from vol compression",
      "charm": "Time decay favors dealers — supports decline into close"
    },
    "hedging_estimate": {
      "spot_down_1pct": { "dealer_shares": 1250000, "direction": "buy", "notional_usd": 725000000 },
      "spot_up_1pct": { "dealer_shares": 1250000, "direction": "sell", "notional_usd": 725000000 }
    },
    "zero_dte": {
      "net_gex": 450000000,
      "pct_of_total": 15.8,
      "expiration": "2026-03-06"
    },
    "top_strikes": [
      { "strike": 580.0, "net_gex": 850000000, "call_oi": 120000, "put_oi": 95000, "total_oi": 215000 },
      { "strike": 575.0, "net_gex": -620000000, "call_oi": 80000, "put_oi": 110000, "total_oi": 190000 }
    ],
    "oi_weighted_dte": 18.5
  },
  "macro": {
    "vix": { "value": 18.5, "change": -0.85, "change_pct": -4.39 },
    "vvix": { "value": 92.3, "change": 1.2, "change_pct": 1.32 },
    "skew": { "value": 138.5, "change": -0.5, "change_pct": -0.36 },
    "spx": { "value": 5820.0, "change": 15.3, "change_pct": 0.26 },
    "move": { "value": 95.2, "change": -2.1, "change_pct": -2.16 },
    "vix_term_structure": {
      "levels": { "vix9d": 16.2, "vix": 18.5, "vix3m": 19.8, "vix6m": 20.5 },
      "near_slope_pct": 14.2,
      "structure": "contango"
    },
    "vix_futures": {
      "front_month": 19.8,
      "spot": 18.5,
      "spread": 1.3,
      "basis_pct": 7.03,
      "basis": "contango"
    },
    "fear_and_greed": { "score": 42, "rating": "Fear" }
  }
}
```

### Response Fields

| Section | Description |
|---------|-------------|
| `price` | Current bid/ask/mid/last from live market data |
| `volatility.atm_iv` | At-the-money implied vol from nearest SVI slice (%) |
| `volatility.hv_20` / `hv_60` | 20-day and 60-day realized (historical) volatility (%) |
| `volatility.vrp` | Vol risk premium = ATM IV − HV20 |
| `volatility.skew_25d` | 25-delta put/call skew from nearest SVI slice (put IV, ATM IV, call IV, skew spread, smile ratio) |
| `volatility.iv_term_structure` | IV at ATM for each active expiration (filtered to 5–200% to exclude bad SVI fits) |
| `options_flow` | Aggregate OI, volume, and put/call ratios across all active expirations |
| `exposure.net_gex/dex/vex/chex` | Net gamma/delta/vanna/charm exposure |
| `exposure.gamma_flip` | Strike where net GEX crosses zero |
| `exposure.call_wall` / `put_wall` | Strikes with highest call/put GEX concentration |
| `exposure.max_pain` | Strike where total option holder loss is maximized |
| `exposure.highest_oi_strike` | Strike with highest total open interest |
| `exposure.regime` | `positive_gamma` or `negative_gamma` based on spot vs gamma flip |
| `exposure.interpretation` | Verbal descriptions of gamma regime, vanna, and charm effects |
| `exposure.hedging_estimate` | Estimated dealer hedging flow (shares + notional) for ±1% spot moves |
| `exposure.zero_dte` | 0DTE contribution to total GEX (net GEX, % of total, expiration date) |
| `exposure.top_strikes` | Top 5 strikes by absolute net GEX with OI breakdown |
| `exposure.oi_weighted_dte` | OI-weighted average days to expiry across all active options |
| `macro.vix/vvix/skew/spx/move` | Index values with daily change and change % |
| `macro.vix_term_structure` | VIX9D, VIX, VIX3M, VIX6M levels with near-term slope and contango/backwardation |
| `macro.vix_futures` | VIX futures basis approximated from VIX3M vs VIX spot (spread, basis %, contango/backwardation) |
| `macro.fear_and_greed` | CNN Fear & Greed Index score (0–100) and rating |

### Errors

| Status | Description |
|--------|-------------|
| `404` | No data for symbol (authenticated) or no cached snapshot (unauthenticated) |

### Notes

- Unauthenticated responses are cached daily at 9:31 AM ET and reflect the previous trading day's data
- Macro fields (`vix`, `vvix`, etc.) may be `null` if the external data source is unavailable
- `exposure` is `null` if no options/greeks data is loaded for the symbol
- HV is computed from Yahoo Finance historical closes using annualized log-return standard deviation (√252)
- `skew_25d` uses SVI-parameterized vol surface; k_25d ≈ ±σ√t × 0.675 (inverse normal of 0.25)
- `vix_futures.basis` is approximated from VIX3M vs VIX spot (not actual futures prices)
- `top_strikes` returns up to 5 strikes sorted by absolute net GEX
- `max_pain` is the strike where total intrinsic value × OI across all options is minimized
- IV term structure filters out slices with IV < 5% or > 200% to exclude bad SVI fits

---

## `GET /v1/exposure/gex/{symbol}`

Returns gamma exposure by strike, including open interest, volume, and day-over-day OI changes.

### Parameters

| Name | In | Required | Default | Description |
|------|----|----------|---------|-------------|
| `symbol` | path | yes | — | Underlying symbol |
| `expiration` | query | no | all | Filter to single expiry (`yyyy-MM-dd`) |
| `min_oi` | query | no | `0` | Minimum open interest threshold |

> **Note:** Full-chain GEX (all expirations) requires the Growth plan. Add `?expiration=yyyy-MM-dd` to filter by a single expiry on lower plans.

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/exposure/gex/SPY?min_oi=100"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 597.505,
  "as_of": "2026-02-28T16:30:45Z",
  "gamma_flip": 595.25,
  "net_gex": 2850000000,
  "net_gex_label": "positive",
  "strikes": [
    {
      "strike": 575.0,
      "call_gex": 12500000,
      "put_gex": 8900000,
      "net_gex": 21400000,
      "call_oi": 15000,
      "put_oi": 12000,
      "call_volume": 250,
      "put_volume": 180,
      "call_oi_change": 500,
      "put_oi_change": -200
    }
  ]
}
```

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid expiration format |
| `403` | Full-chain GEX requires Growth plan |
| `404` | Symbol not found or no data |

---

## `GET /v1/exposure/dex/{symbol}`

Returns delta exposure by strike.

**Requires Basic plan or higher.**

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `symbol` | path | yes | Underlying symbol |
| `expiration` | query | no | Filter to single expiry (`yyyy-MM-dd`) |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/exposure/dex/SPY"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 597.505,
  "as_of": "2026-02-28T16:30:45Z",
  "net_dex": -450000000,
  "strikes": [
    {
      "strike": 575.0,
      "call_dex": 5600000,
      "put_dex": 4200000,
      "net_dex": 9800000
    }
  ]
}
```

---

## `GET /v1/exposure/vex/{symbol}`

Returns vanna exposure by strike. Vanna measures the sensitivity of delta to changes in implied volatility.

**Requires Basic plan or higher.**

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `symbol` | path | yes | Underlying symbol |
| `expiration` | query | no | Filter to single expiry (`yyyy-MM-dd`) |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/exposure/vex/SPY"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 597.505,
  "as_of": "2026-02-28T16:30:45Z",
  "net_vex": 1200000000,
  "vex_interpretation": "Positive vanna — benefits from vol compression",
  "strikes": [
    {
      "strike": 575.0,
      "call_vex": 2300000,
      "put_vex": 1800000,
      "net_vex": 4100000
    }
  ]
}
```

---

## `GET /v1/exposure/chex/{symbol}`

Returns charm exposure by strike. Charm measures the sensitivity of delta to the passage of time.

**Requires Basic plan or higher.**

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `symbol` | path | yes | Underlying symbol |
| `expiration` | query | no | Filter to single expiry (`yyyy-MM-dd`) |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/exposure/chex/SPY"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 597.505,
  "as_of": "2026-02-28T16:30:45Z",
  "net_chex": 850000000,
  "chex_interpretation": "Positive charm — time decay benefits dealers",
  "strikes": [
    {
      "strike": 575.0,
      "call_chex": 950000,
      "put_chex": 620000,
      "net_chex": 1570000
    }
  ]
}
```

---

## `GET /v1/exposure/summary/{symbol}`

Returns a comprehensive exposure summary: net GEX/DEX/VEX/CHEX totals, gamma regime, verbal interpretation, dealer hedging estimates for +/-1% spot moves, and 0DTE contribution.

**Requires Growth plan or higher.**

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `symbol` | path | yes | Underlying symbol |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/exposure/summary/SPY"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 597.505,
  "as_of": "2026-02-28T16:30:45Z",
  "gamma_flip": 595.25,
  "regime": "positive_gamma",
  "exposures": {
    "net_gex": 2850000000,
    "net_dex": -450000000,
    "net_vex": 1200000000,
    "net_chex": 850000000
  },
  "interpretation": {
    "gamma": "Dealers long gamma — expect range-bound, mean-reverting price action",
    "vanna": "Positive vanna — benefits from vol compression",
    "charm": "Time decay favors dealers — supports decline into close"
  },
  "hedging_estimate": {
    "spot_down_1pct": {
      "dealer_shares_to_trade": 4780000,
      "direction": "BUY",
      "notional_usd": 2852000000
    },
    "spot_up_1pct": {
      "dealer_shares_to_trade": -4780000,
      "direction": "SELL",
      "notional_usd": 2852000000
    }
  },
  "zero_dte": {
    "net_gex": 285000000,
    "pct_of_total_gex": 10.0,
    "expiration": "2026-02-28"
  }
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `regime` | `positive_gamma`, `negative_gamma`, or `undetermined` |
| `hedging_estimate` | Estimated dealer hedging flow if spot moves +/-1% |
| `zero_dte` | Same-day expiration contribution to total GEX |

---

## `GET /v1/exposure/levels/{symbol}`

Returns key technical levels derived from options exposure: gamma flip, call/put walls, max gamma strikes, highest OI strike, and 0DTE magnet.

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `symbol` | path | yes | Underlying symbol |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/exposure/levels/SPY"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 597.505,
  "as_of": "2026-02-28T16:30:45Z",
  "levels": {
    "gamma_flip": 595.25,
    "max_positive_gamma": 600.0,
    "max_negative_gamma": 585.0,
    "call_wall": 600.0,
    "put_wall": 595.0,
    "highest_oi_strike": 600.0,
    "zero_dte_magnet": 598.0
  }
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `gamma_flip` | Price where net GEX crosses zero — above = positive gamma, below = negative |
| `call_wall` | Strike with highest call GEX — acts as resistance |
| `put_wall` | Strike with highest put GEX — acts as support |
| `max_positive_gamma` | Strike with highest positive net GEX |
| `max_negative_gamma` | Strike with most negative net GEX |
| `highest_oi_strike` | Strike with highest total open interest |
| `zero_dte_magnet` | 0DTE strike with highest GEX — intraday price magnet |

---

## `GET /v1/exposure/narrative/{symbol}`

Returns a verbal analysis of the current options exposure landscape with day-over-day changes, key levels context, notable OI flow, vanna/charm interpretation, and market outlook. Includes structured data backing each section.

**Requires Growth plan or higher.**

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `symbol` | path | yes | Underlying symbol |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/exposure/narrative/SPY"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 597.505,
  "as_of": "2026-02-28T16:30:45Z",
  "narrative": {
    "regime": "Dealers are long gamma (net GEX +$2.9B) — expect mean-reverting, range-bound price action.",
    "gex_change": "Net GEX increased from +$2.6B to +$2.9B (+11.5%) — gamma cushion strengthening.",
    "key_levels": "Call wall at 600, Put wall at 595, Gamma flip at 595.25.",
    "flow": "Top OI changes: +5,000 call OI at 600 strike, -2,000 put OI at 595 strike.",
    "vanna": "Positive vanna (+$1.2B) with VIX at 18.5 — vol compression supports upside.",
    "charm": "Positive charm (+$850M) — time decay pushing dealers to buy, providing support.",
    "zero_dte": "0DTE accounts for 10% of total GEX — minimal intraday impact.",
    "outlook": "Positive gamma regime with strengthening cushion. Testing 600 call wall.",
    "data": {
      "net_gex": 2850000000,
      "net_gex_prior": 2600000000,
      "net_gex_change_pct": 9.6,
      "vix": 18.5,
      "gamma_flip": 595.25,
      "call_wall": 600.0,
      "put_wall": 595.0,
      "regime": "positive_gamma",
      "zero_dte_pct": 10.0,
      "top_oi_changes": [
        {
          "strike": 600.0,
          "type": "C",
          "oi_change": 5000,
          "volume": 1250
        }
      ]
    }
  }
}
```

### Narrative Sections

| Field | Description |
|-------|-------------|
| `regime` | Current gamma regime and what it implies for price action |
| `gex_change` | How net GEX changed vs. prior day |
| `key_levels` | Call wall, put wall, gamma flip in context of spot |
| `flow` | Largest OI changes — where is new positioning concentrating |
| `vanna` | Vanna exposure interpretation with VIX context |
| `charm` | Charm/time-decay effect on dealer positioning |
| `zero_dte` | Same-day expiration significance |
| `outlook` | Overall synthesis and directional bias |
| `data` | Raw numeric data backing the narrative |

---

## `GET /v1/exposure/zero-dte/{symbol}`

Returns a comprehensive 0DTE (zero days to expiration) analytics view for intraday options trading. Includes gamma regime, expected move, pin risk scoring, dealer hedging estimates at ±0.5%/±1% moves, time decay acceleration, vol context, flow data, and per-strike breakdown.

**Requires Growth plan or higher.**

### Parameters

| Name | In | Required | Default | Description |
|------|----|----------|---------|-------------|
| `symbol` | path | yes | — | Underlying symbol |
| `strike_range` | query | no | `0.03` | Fraction of spot to include in strikes array (0.001–0.10). Aggregates always use full chain. |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/exposure/zero-dte/SPY?strike_range=0.03"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 590.42,
  "expiration": "2026-03-19",
  "as_of": "2026-03-19T14:45:12Z",
  "market_open": true,
  "time_to_close_hours": 1.25,
  "time_to_close_pct": 80.8,
  "regime": {
    "label": "positive_gamma",
    "description": "Dealers long gamma — moves dampened, mean reversion likely",
    "gamma_flip": 588.50,
    "spot_vs_flip": "above",
    "spot_to_flip_pct": 0.33
  },
  "exposures": {
    "net_gex": 1842000000,
    "net_dex": 48200000000,
    "net_vex": -320000000,
    "net_chex": 95000000,
    "pct_of_total_gex": 62.4,
    "total_chain_net_gex": 2952000000
  },
  "expected_move": {
    "implied_1sd_dollars": 2.18,
    "implied_1sd_pct": 0.37,
    "remaining_1sd_dollars": 1.05,
    "remaining_1sd_pct": 0.18,
    "upper_bound": 591.47,
    "lower_bound": 589.37,
    "straddle_price": 1.62,
    "atm_iv": 0.123
  },
  "pin_risk": {
    "magnet_strike": 590,
    "magnet_gex": 580000000,
    "distance_to_magnet_pct": 0.07,
    "pin_score": 82,
    "max_pain": 590,
    "oi_concentration_top3_pct": 41.2,
    "description": "Strong pin at 590. 82/100 pin score with 41% of OI in top 3 strikes."
  },
  "hedging": {
    "spot_up_half_pct": { "dealer_shares_to_trade": -156100, "direction": "sell", "notional_usd": -92158000 },
    "spot_down_half_pct": { "dealer_shares_to_trade": 156100, "direction": "buy", "notional_usd": 92158000 },
    "spot_up_1pct": { "dealer_shares_to_trade": -312200, "direction": "sell", "notional_usd": -184316000 },
    "spot_down_1pct": { "dealer_shares_to_trade": 312200, "direction": "buy", "notional_usd": 184316000 }
  },
  "decay": {
    "net_theta_dollars": -4820000,
    "theta_per_hour_remaining": -3856000,
    "charm_regime": "time_decay_dealers_buy",
    "charm_description": "Time decay pushing dealers to buy — supportive into close",
    "gamma_acceleration": 2.4,
    "description": "0DTE theta bleeding $3,856/hr. Gamma 2.4x higher than equivalent 7DTE."
  },
  "vol_context": {
    "zero_dte_atm_iv": 12.3,
    "seven_dte_atm_iv": 14.8,
    "iv_ratio_0dte_7dte": 0.83,
    "vix": 16.2,
    "vanna_exposure": -320000000,
    "vanna_interpretation": "vol_up_dealers_sell",
    "description": "0DTE IV at 12.3% vs 7DTE at 14.8%. Negative vanna — vol spike triggers dealer selling."
  },
  "flow": {
    "total_volume": 842000,
    "call_volume": 520000,
    "put_volume": 322000,
    "total_oi": 1240000,
    "call_oi": 680000,
    "put_oi": 560000,
    "pc_ratio_volume": 0.619,
    "pc_ratio_oi": 0.824,
    "volume_to_oi_ratio": 0.679
  },
  "levels": {
    "call_wall": 595,
    "call_wall_gex": 420000000,
    "put_wall": 585,
    "put_wall_gex": -380000000,
    "highest_oi_strike": 590,
    "highest_oi_total": 48200,
    "max_positive_gamma": 592,
    "max_negative_gamma": 586
  },
  "strikes": [
    {
      "strike": 590,
      "call_gex": 450000000, "put_gex": -380000000, "net_gex": 70000000,
      "call_dex": 12500000, "put_dex": -15000000, "net_dex": -2500000,
      "call_oi": 25000, "put_oi": 30000,
      "call_volume": 15000, "put_volume": 12000,
      "call_iv": 0.18, "put_iv": 0.19,
      "call_delta": 0.50, "put_delta": -0.50,
      "call_gamma": 0.025, "put_gamma": 0.025,
      "call_theta": -1.0, "put_theta": -1.0
    }
  ]
}
```

### Response Fields

| Section | Description |
|---------|-------------|
| `time_to_close_hours` | Hours until 4:00 PM ET. The single most important 0DTE context variable. |
| `time_to_close_pct` | Percentage of trading day elapsed (0=open, 100=close) |
| `regime` | 0DTE-specific gamma regime (separate from full-chain flip) |
| `exposures.pct_of_total_gex` | 0DTE GEX as % of full-chain GEX. >50% = 0DTE dominates intraday |
| `expected_move.remaining_1sd_*` | Shrinks in real-time as close approaches. At 9:31 AM = full day; at 3:30 PM = 27.7% of full day |
| `expected_move.straddle_price` | ATM 0DTE straddle mid — direct market-implied expected move |
| `pin_risk.pin_score` | 0-100 composite: OI concentration (30%), magnet proximity (25%), time remaining (25%), gamma magnitude (20%) |
| `pin_risk.max_pain` | Strike where total option holder intrinsic value is minimized |
| `hedging.spot_*_half_pct` | Dealer hedging for ±0.5% moves — more relevant for 0DTE than ±1% |
| `decay.theta_per_hour_remaining` | `net_theta_dollars / time_to_close_hours` — accelerates as denominator shrinks |
| `decay.gamma_acceleration` | 0DTE ATM gamma / 7DTE ATM gamma. Typically 2-5x, can hit 10x+ near close |
| `vol_context.iv_ratio_0dte_7dte` | <1.0 = 0DTE is "cheap" vs term structure; >1.0 = event premium |
| `flow.volume_to_oi_ratio` | >1.0 = heavy day-trading (intraday flow exceeds overnight positioning) |

### No 0DTE Expiry

If the symbol has no 0DTE expiry today (e.g. SPY on Tuesday/Thursday):

```json
{
  "symbol": "SPY",
  "underlying_price": 590.42,
  "expiration": null,
  "as_of": "2026-03-17T15:30:00Z",
  "market_open": true,
  "no_zero_dte": true,
  "message": "No 0DTE expiry for SPY today (Tuesday). Next expiry: 2026-03-18.",
  "next_zero_dte_expiry": "2026-03-18"
}
```

### Errors

| Status | Description |
|--------|-------------|
| `403` | Requires Growth plan or higher |
| `404` | Symbol not found or no data |

### Notes

- SPY has 0DTE on Mon/Wed/Fri. SPX (SPXW) has daily 0DTE.
- `theta_per_hour_remaining` is `null` when `time_to_close_hours` is 0 (market closed)
- Near close (<5 minutes), a `warnings` array is included noting potential greek instability
- `strike_range` only filters the `strikes` array — all aggregate calculations use the full 0DTE chain
- All calculations are pure static (no external calls beyond the initial data fetch)

---

## `GET /v1/exposure/history/{symbol}`

Returns daily exposure snapshots for trend analysis. Data is stored end-of-day and returned newest first.

**Requires Growth plan or higher.** *Currently returns `503 coming_soon`.*

### Parameters

| Name | In | Required | Default | Description |
|------|----|----------|---------|-------------|
| `symbol` | path | yes | — | Underlying symbol |
| `days` | query | no | `30` | Days of history (1-365) |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/exposure/history/SPY?days=7"
```

### Response `200` *(when available)*

```json
{
  "symbol": "SPY",
  "days": 7,
  "count": 5,
  "snapshots": [
    {
      "date": "2026-02-28",
      "underlying_price": 597.505,
      "net_gex": 2850000000,
      "net_dex": -450000000,
      "net_vex": 1200000000,
      "net_chex": 850000000,
      "gamma_flip": 595.25,
      "call_wall": 600.0,
      "put_wall": 595.0,
      "regime": "positive_gamma"
    }
  ]
}
```

---

## `GET /v1/maxpain/{symbol}`

Returns max pain analysis for a symbol — the strike where total option holder payout is minimized. Includes pain curve, OI breakdown, dealer alignment overlay (gamma flip, call/put walls), expected move context, pin probability, and multi-expiry calendar.

**Requires Basic plan or higher.**

### Parameters

| Name | In | Required | Default | Description |
|------|----|----------|---------|-------------|
| `symbol` | path | yes | — | Underlying symbol |
| `expiration` | query | no | — | Filter to a single expiry (`yyyy-MM-dd`). Omit for full-chain analysis with multi-expiry breakdown. |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/maxpain/SPY"
```

With expiration filter:

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/maxpain/SPY?expiration=2026-04-17"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 548.32,
  "as_of": "2026-04-09T15:30:00Z",
  "max_pain_strike": 545,
  "distance": {
    "absolute": 3.32,
    "percent": 0.61,
    "direction": "above"
  },
  "signal": "neutral",
  "expiration": "2026-04-17",
  "put_call_oi_ratio": 1.284,
  "pain_curve": [
    { "strike": 540, "call_pain": 0, "put_pain": 18500000, "total_pain": 18500000 },
    { "strike": 545, "call_pain": 2500000, "put_pain": 1200000, "total_pain": 3700000 },
    { "strike": 550, "call_pain": 8400000, "put_pain": 0, "total_pain": 8400000 }
  ],
  "oi_by_strike": [
    { "strike": 540, "call_oi": 12000, "put_oi": 28000, "total_oi": 40000, "call_volume": 3200, "put_volume": 5800 },
    { "strike": 545, "call_oi": 35000, "put_oi": 42000, "total_oi": 77000, "call_volume": 8100, "put_volume": 9400 },
    { "strike": 550, "call_oi": 18000, "put_oi": 8000, "total_oi": 26000, "call_volume": 4500, "put_volume": 2100 }
  ],
  "max_pain_by_expiration": [
    { "expiration": "2026-04-11", "max_pain_strike": 547, "dte": 2, "total_oi": 520000 },
    { "expiration": "2026-04-17", "max_pain_strike": 545, "dte": 8, "total_oi": 1840000 },
    { "expiration": "2026-05-16", "max_pain_strike": 540, "dte": 37, "total_oi": 980000 }
  ],
  "dealer_alignment": {
    "alignment": "converging",
    "description": "Max pain (545) near gamma flip (546) between walls (538–555) — strong converging magnet.",
    "gamma_flip": 546,
    "call_wall": 555,
    "put_wall": 538
  },
  "regime": "positive_gamma",
  "expected_move": {
    "straddle_price": 4.82,
    "atm_iv": 18.4,
    "max_pain_within_expected_range": true
  },
  "pin_probability": 68
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `max_pain_strike` | Strike where total option holder intrinsic value is minimized |
| `distance.absolute` | Dollar distance from spot to max pain |
| `distance.percent` | Percentage distance from spot to max pain |
| `distance.direction` | `above`, `below`, or `at` — spot relative to max pain |
| `signal` | `bullish` (spot >= 5% below max pain), `bearish` (>= 5% above), `neutral` (within 5%) |
| `put_call_oi_ratio` | Total put OI / total call OI. >1.0 = put-heavy chain |
| `pain_curve` | Per-strike breakdown: call pain, put pain, total pain. Minimum `total_pain` matches `max_pain_strike`. |
| `oi_by_strike` | Per-strike OI and volume for calls and puts |
| `max_pain_by_expiration` | Per-expiry max pain with DTE and total OI. Only present when no `?expiration=` filter. |
| `dealer_alignment.alignment` | `converging` (max pain near gamma flip, between walls), `moderate` (between walls, far from flip), `diverging` (outside walls), `unknown` (insufficient data) |
| `dealer_alignment.gamma_flip` | Strike where net GEX crosses zero |
| `dealer_alignment.call_wall` / `put_wall` | Strikes with highest absolute call/put GEX |
| `regime` | `positive_gamma` or `negative_gamma` based on spot vs gamma flip |
| `expected_move.straddle_price` | ATM straddle mid price |
| `expected_move.atm_iv` | ATM implied volatility (percentage, e.g. 18.4 = 18.4%) |
| `expected_move.max_pain_within_expected_range` | Whether max pain is within the straddle-implied expected move |
| `pin_probability` | 0–100 composite score: OI concentration (30%), magnet proximity (25%), time remaining (25%), gamma magnitude (20%) |

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid expiration format (must be `yyyy-MM-dd`) |
| `403` | Requires Basic plan or higher |
| `404` | Symbol not found, no options data, or no data for requested expiration |

### Notes

- Without `?expiration=`, the response uses the full options chain and includes `max_pain_by_expiration` for all available expiries
- With `?expiration=`, the response is scoped to that single expiry and `max_pain_by_expiration` is `null`
- The dealer alignment overlay reuses the same GEX calculations as `/v1/exposure/levels` — call wall, put wall, and gamma flip values should be consistent
- `pin_probability` is most meaningful for near-term expirations; for LEAPs it will be low regardless of OI distribution
- Pain curve values are in **USD notional** (intrinsic value × OI × 100 contract multiplier)

---

## `GET /v1/pricing/greeks`

Compute full Black-Scholes-Merton greeks from provided inputs. Returns theoretical price plus first-order, second-order, and third-order greeks. Pure calculation — no market data required.

**Available on all plans (Free+).**

### Parameters

| Name | In | Required | Default | Description |
|------|----|----------|---------|-------------|
| `spot` | query | yes | — | Underlying spot price |
| `strike` | query | yes | — | Strike price |
| `dte` | query | yes | — | Days to expiration |
| `sigma` | query | yes | — | Implied volatility (annualized, e.g. `0.18` = 18%) |
| `type` | query | no | `call` | `call` or `put` |
| `r` | query | no | `0.045` | Risk-free rate (annualized) |
| `q` | query | no | `0.013` | Dividend yield (annualized) |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/pricing/greeks?spot=580&strike=580&dte=30&sigma=0.18&type=call"
```

### Response `200`

```json
{
  "inputs": {
    "spot": 580,
    "strike": 580,
    "dte": 30,
    "sigma": 0.18,
    "type": "call",
    "risk_free_rate": 0.045,
    "dividend_yield": 0.013
  },
  "theoretical_price": 12.687211,
  "first_order": {
    "delta": 0.53003,
    "gamma": 0.013276,
    "theta": -0.223599,
    "vega": 0.660706,
    "rho": 24.224395
  },
  "second_order": {
    "vanna": -0.055551,
    "charm": 0.00049,
    "vomma": 0.709126,
    "dual_delta": -0.508155
  },
  "third_order": {
    "speed": -0.00005694,
    "zomma": -0.07361041,
    "color": -0.00022304,
    "ultima": -17.241619
  },
  "additional": {
    "lambda": 24.2305,
    "veta": 1.092334
  }
}
```

### Response Fields

| Section | Field | Description |
|---------|-------|-------------|
| `theoretical_price` | — | BSM theoretical option price |
| **First-order** | | |
| `first_order` | `delta` | ∂V/∂S — sensitivity to spot price |
| `first_order` | `gamma` | ∂²V/∂S² — rate of change of delta |
| `first_order` | `theta` | ∂V/∂t — daily time decay (per day) |
| `first_order` | `vega` | ∂V/∂σ — sensitivity to 1% vol change |
| `first_order` | `rho` | ∂V/∂r — sensitivity to interest rate |
| **Second-order** | | |
| `second_order` | `vanna` | ∂²V/∂S∂σ — delta sensitivity to vol |
| `second_order` | `charm` | ∂²V/∂S∂t — delta decay per day |
| `second_order` | `vomma` | ∂²V/∂σ² — vega convexity (volga) |
| `second_order` | `dual_delta` | ∂V/∂K — sensitivity to strike price |
| **Third-order** | | |
| `third_order` | `speed` | ∂³V/∂S³ — gamma sensitivity to spot |
| `third_order` | `zomma` | ∂³V/∂S²∂σ — gamma sensitivity to vol |
| `third_order` | `color` | ∂³V/∂S²∂t — gamma decay per day |
| `third_order` | `ultima` | ∂³V/∂σ³ — vomma sensitivity to vol |
| **Additional** | | |
| `additional` | `lambda` | Delta × S / V — option leverage ratio (null if price ≤ 0) |
| `additional` | `veta` | ∂²V/∂σ∂t — vega decay per day |

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid or missing input parameter |

---

## `GET /v1/pricing/iv`

Compute implied volatility from a market price using Newton-Raphson root finding.

**Available on all plans (Free+).**

### Parameters

| Name | In | Required | Default | Description |
|------|----|----------|---------|-------------|
| `spot` | query | yes | — | Underlying spot price |
| `strike` | query | yes | — | Strike price |
| `dte` | query | yes | — | Days to expiration |
| `price` | query | yes | — | Market option price (mid) |
| `type` | query | no | `call` | `call` or `put` |
| `r` | query | no | `0.045` | Risk-free rate |
| `q` | query | no | `0.013` | Dividend yield |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/pricing/iv?spot=580&strike=580&dte=30&price=12.69&type=call"
```

### Response `200`

```json
{
  "inputs": {
    "spot": 580, "strike": 580, "dte": 30, "price": 12.69,
    "type": "call", "risk_free_rate": 0.045, "dividend_yield": 0.013
  },
  "implied_volatility": 0.180042,
  "implied_volatility_pct": 18.0
}
```

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid or missing input parameter |
| `422` | Could not determine IV (price outside arbitrage-free range) |

---

## `GET /v1/pricing/kelly`

Compute Kelly criterion optimal position sizing for an option trade. Uses numerical integration over the full lognormal distribution of the underlying to maximize expected log-wealth growth — not the simplified gambling formula.

Unlike standard Kelly (designed for fixed-odds bets), this handles the asymmetric, bounded-loss payoff structure of options: max loss is capped at the premium paid, while upside can be unbounded.

**Requires Growth plan or higher.**

### Parameters

| Name | In | Required | Default | Description |
|------|----|----------|---------|-------------|
| `spot` | query | yes | — | Underlying spot price |
| `strike` | query | yes | — | Strike price |
| `dte` | query | yes | — | Days to expiration |
| `sigma` | query | yes | — | Implied volatility (annualized) |
| `premium` | query | yes | — | Option premium paid (per share) |
| `mu` | query | yes | — | Expected annualized return of the underlying (your view, e.g. `0.12` = 12%). Range: -200% to +200%. |
| `type` | query | no | `call` | `call` or `put` |
| `r` | query | no | `0.045` | Risk-free rate |
| `q` | query | no | `0.013` | Dividend yield |

### How `mu` works

The key input is `mu` — your expected annual return for the underlying. This is what gives you an *edge* over the market price (which uses `r`):

- `mu > r` → you're more bullish than the market → calls have positive edge
- `mu < r` → you're more bearish → puts have positive edge
- `mu = r` → no edge → Kelly recommends no position

For example, if SPY is priced with `r = 4.5%` but you expect `mu = 12%` annual return, your calls have an edge and Kelly will tell you how much to bet.

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/pricing/kelly?spot=580&strike=580&dte=30&sigma=0.18&premium=12.69&mu=0.12&type=call"
```

### Response `200`

```json
{
  "inputs": {
    "spot": 580, "strike": 580, "dte": 30, "sigma": 0.18, "premium": 12.69,
    "mu": 0.12, "type": "call", "risk_free_rate": 0.045, "dividend_yield": 0.013
  },
  "sizing": {
    "kelly_fraction": 0.076842,
    "half_kelly": 0.038421,
    "quarter_kelly": 0.01921,
    "kelly_pct": 7.68,
    "half_kelly_pct": 3.84
  },
  "analysis": {
    "expected_roi": 0.160546,
    "expected_roi_pct": 16.05,
    "expected_payoff": 14.7273,
    "probability_of_profit": 0.391739,
    "probability_of_profit_pct": 39.17,
    "probability_itm": 0.557494,
    "probability_itm_pct": 55.75,
    "max_loss": 12.69,
    "breakeven": 592.69,
    "expected_growth_rate": 0.00584368
  },
  "recommendation": "Risk 3.8% of bankroll (half-Kelly). Probability of profit: 39.2%. Expected ROI: 16.1%."
}
```

### Response Fields

| Section | Field | Description |
|---------|-------|-------------|
| **Sizing** | | |
| `sizing` | `kelly_fraction` | Full Kelly — optimal fraction of bankroll to risk (0–1) |
| `sizing` | `half_kelly` | Half Kelly — recommended for practice (less volatile) |
| `sizing` | `quarter_kelly` | Quarter Kelly — very conservative |
| `sizing` | `kelly_pct` / `half_kelly_pct` | Same as above, in percent |
| **Analysis** | | |
| `analysis` | `expected_roi` | Expected return on investment (payoff/premium − 1) |
| `analysis` | `probability_of_profit` | P(option profit at expiry) — real-world measure using `mu` |
| `analysis` | `probability_itm` | P(option in-the-money at expiry) — real-world measure |
| `analysis` | `max_loss` | Maximum loss per share (= premium paid) |
| `analysis` | `breakeven` | Underlying price needed at expiry to break even |
| `analysis` | `expected_growth_rate` | Expected log-growth rate of bankroll at Kelly fraction |
| **Recommendation** | | |
| `recommendation` | — | Human-readable sizing recommendation |

### Negative Expected Value

If the option has negative expected value (your view doesn't justify the premium), Kelly returns zero:

```json
{
  "sizing": { "kelly_fraction": 0, "half_kelly": 0, "quarter_kelly": 0 },
  "recommendation": "Negative expected value — Kelly recommends no position."
}
```

### Errors

| Status | Description |
|--------|-------------|
| `400` | Invalid or missing input parameter (including mu outside ±200%) |
| `403` | Requires Growth plan or higher |

### Notes

- All probabilities use the **real-world measure** (with `mu`), not the risk-neutral measure (with `r`). This is what you actually expect to happen, not what's priced in.
- Kelly fraction is bounded to [0, 1] — it will never recommend shorting or leveraging beyond 100%.
- **Half-Kelly is strongly recommended** in practice — full Kelly is mathematically optimal but very aggressive and assumes perfect parameter estimation.
- The numerical integration uses 2000 steps over ±6σ of the lognormal distribution, giving high accuracy for typical parameters.

---

## `GET /v1/tickers`

Returns all available stock tickers from the Polygon catalog.

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" https://lab.flashalpha.com/v1/tickers
```

### Response `200`

```json
{
  "tickers": ["AAPL", "AMZN", "GOOGL", "META", "MSFT", "QQQ", "SPY", "TSLA"],
  "count": 8
}
```

---

## `GET /v1/options/{ticker}`

Returns option chain metadata for a symbol: all available expirations with their strikes.

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `ticker` | path | yes | Underlying symbol |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" https://lab.flashalpha.com/v1/options/SPY
```

### Response `200`

```json
{
  "symbol": "SPY",
  "expirations": [
    {
      "expiration": "2026-03-07",
      "strikes": [550.0, 555.0, 560.0, 565.0, 570.0, 575.0, 580.0]
    },
    {
      "expiration": "2026-03-14",
      "strikes": [550.0, 555.0, 560.0, 565.0, 570.0]
    }
  ],
  "expiration_count": 2,
  "total_contracts": 12
}
```

### Errors

| Status | Description |
|--------|-------------|
| `404` | No options data for symbol |

---

## `GET /v1/symbols`

Returns the list of symbols that have been queried and have live data cached.

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" https://lab.flashalpha.com/v1/symbols
```

### Response `200`

```json
{
  "symbols": ["SPY", "QQQ"],
  "count": 2,
  "note": "Any US equity or ETF symbol is supported. All data is fetched on-demand with a 15-second cache.",
  "last_updated": "2026-02-28T16:30:45Z"
}
```

---

## `GET /v1/volatility/{symbol}`

Returns comprehensive volatility analysis for any US equity or ETF. Includes realized vol, IV-RV spreads, skew profiles, term structure, GEX by DTE, theta decay, put/call breakdowns, OI concentration, multi-move hedging scenarios, and liquidity analysis.

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" https://lab.flashalpha.com/v1/volatility/TSLA
```

### Response `200`

```json
{
  "symbol": "TSLA",
  "underlying_price": 265.50,
  "as_of": "2026-03-09T15:30:00Z",
  "market_open": true,
  "realized_vol": {
    "rv_5d": 52.31,
    "rv_10d": 48.12,
    "rv_20d": 45.80,
    "rv_30d": 44.20,
    "rv_60d": 42.15
  },
  "atm_iv": 48.50,
  "iv_rv_spreads": {
    "vrp_5d": -3.81,
    "vrp_10d": 0.38,
    "vrp_20d": 2.70,
    "vrp_30d": 4.30,
    "assessment": "moderate_premium"
  },
  "skew_profiles": [
    {
      "expiry": "2026-03-14",
      "days_to_expiry": 5,
      "put_10d_iv": 62.50,
      "put_25d_iv": 54.20,
      "atm_iv": 48.50,
      "call_25d_iv": 45.10,
      "call_10d_iv": 43.80,
      "skew_25d": 9.10,
      "smile_ratio": 1.202,
      "tail_convexity": 2.60
    }
  ],
  "term_structure": {
    "near_slope_pct": 5.20,
    "far_slope_pct": 3.10,
    "state": "contango"
  },
  "iv_dispersion": {
    "cross_expiry": 3.45,
    "cross_strike": 12.80
  },
  "gex_by_dte": [
    { "bucket": "0-7d", "net_gex": 1200000, "pct_of_total": 35.2, "contract_count": 450 },
    { "bucket": "8-30d", "net_gex": 800000, "pct_of_total": 23.5, "contract_count": 1200 },
    { "bucket": "31-60d", "net_gex": 950000, "pct_of_total": 27.9, "contract_count": 800 },
    { "bucket": "60d+", "net_gex": 460000, "pct_of_total": 13.4, "contract_count": 600 }
  ],
  "theta_by_dte": [
    { "bucket": "0-7d", "net_theta": -450000, "contract_count": 450 },
    { "bucket": "8-30d", "net_theta": -320000, "contract_count": 1200 },
    { "bucket": "31-60d", "net_theta": -180000, "contract_count": 800 },
    { "bucket": "60d+", "net_theta": -95000, "contract_count": 600 }
  ],
  "put_call_profile": {
    "by_expiry": [
      {
        "expiry": "2026-03-14",
        "call_oi": 120000,
        "put_oi": 95000,
        "pc_ratio_oi": 0.792,
        "call_volume": 45000,
        "put_volume": 38000,
        "pc_ratio_volume": 0.844
      }
    ],
    "by_moneyness": {
      "otm_call_oi": 85000,
      "atm_call_oi": 25000,
      "itm_call_oi": 10000,
      "otm_put_oi": 60000,
      "atm_put_oi": 20000,
      "itm_put_oi": 15000
    }
  },
  "oi_concentration": {
    "top_3_pct": 18.5,
    "top_5_pct": 28.2,
    "top_10_pct": 45.0,
    "herfindahl": 0.032
  },
  "hedging_scenarios": [
    { "move_pct": -5, "dealer_shares": 850000, "direction": "buy", "notional_usd": 225575000 },
    { "move_pct": -2, "dealer_shares": 340000, "direction": "buy", "notional_usd": 90230000 },
    { "move_pct": -1, "dealer_shares": 170000, "direction": "buy", "notional_usd": 45115000 },
    { "move_pct": 1, "dealer_shares": -170000, "direction": "sell", "notional_usd": 45115000 },
    { "move_pct": 2, "dealer_shares": -340000, "direction": "sell", "notional_usd": 90230000 },
    { "move_pct": 5, "dealer_shares": -850000, "direction": "sell", "notional_usd": 225575000 }
  ],
  "liquidity": {
    "atm_avg_spread_pct": 1.85,
    "wing_avg_spread_pct": 45.20,
    "atm_contracts": 120,
    "wing_contracts": 340
  }
}
```

### Response fields

| Section | Field | Description |
|---------|-------|-------------|
| `realized_vol` | `rv_5d` through `rv_60d` | Annualized realized vol (%) for 5, 10, 20, 30, 60 day windows. Log-returns, sample std dev, ×√252. |
| `atm_iv` | — | At-the-money implied volatility (%) from nearest SVI slice |
| `iv_rv_spreads` | `vrp_Nd` | IV minus RV spread per window. Positive = IV rich. |
| `iv_rv_spreads` | `assessment` | VRP regime: `very_high_premium`, `healthy_premium`, `moderate_premium`, `thin_premium`, `negative_spread`, `danger_zone` |
| `skew_profiles[]` | `put_10d_iv`, `put_25d_iv`, `atm_iv`, `call_25d_iv`, `call_10d_iv` | Full delta-based skew from SVI per expiry |
| `skew_profiles[]` | `skew_25d` | 25-delta risk reversal: put_25d - call_25d |
| `skew_profiles[]` | `smile_ratio` | Put 25d IV / Call 25d IV. >1 = put skew dominant |
| `skew_profiles[]` | `tail_convexity` | Wing curvature: (put10-put25) - (put25-ATM). Positive = steep tail |
| `term_structure` | `near_slope_pct` | (30d IV - 7d IV) / 7d IV × 100 |
| `term_structure` | `far_slope_pct` | (90d IV - 30d IV) / 30d IV × 100 |
| `term_structure` | `state` | `contango`, `backwardation`, `mixed`, or `unknown` |
| `iv_dispersion` | `cross_expiry` | Std dev of ATM IVs across expirations (term structure dispersion) |
| `iv_dispersion` | `cross_strike` | Std dev of IVs across strikes at nearest expiry (smile dispersion) |
| `gex_by_dte[]` | `bucket`, `net_gex`, `pct_of_total`, `contract_count` | GEX bucketed by DTE: 0-7d, 8-30d, 31-60d, 60d+ |
| `theta_by_dte[]` | `bucket`, `net_theta`, `contract_count` | Aggregate theta × OI × 100 per DTE bucket |
| `put_call_profile` | `by_expiry[]` | P/C ratio (OI and volume) per expiration |
| `put_call_profile` | `by_moneyness` | OI breakdown: OTM/ATM/ITM for calls and puts (ATM = within 5% of spot) |
| `oi_concentration` | `top_3_pct`, `top_5_pct`, `top_10_pct` | % of total OI in top N strikes |
| `oi_concentration` | `herfindahl` | Herfindahl index (0-1). Higher = more concentrated |
| `hedging_scenarios[]` | `move_pct`, `dealer_shares`, `direction`, `notional_usd` | Estimated dealer hedging flow for ±1%, ±2%, ±5% moves |
| `liquidity` | `atm_avg_spread_pct` | Average bid-ask spread % for ATM options (within 2% of spot) |
| `liquidity` | `wing_avg_spread_pct` | Average bid-ask spread % for wings (>10% OTM) |

### Notes

1. **Realized vol** uses close-to-close log-returns with sample standard deviation (N-1), annualized by √252. This matches Yahoo Finance, Bloomberg, and QuantLib conventions.
2. **Skew profiles** use delta-to-moneyness approximation: k = ±σ√t × Φ⁻¹(δ). 25-delta uses 0.6745, 10-delta uses 1.2816.
3. **Tail convexity** measures the second difference of the skew. Positive values indicate steep left-wing curvature (crash protection being bid).
4. **GEX by DTE** uses the SpotGamma convention: gamma × OI × 100 × spot² × 0.01. Calls positive, puts negated.
5. **Herfindahl index** ranges from 1/N (perfectly even) to 1.0 (all OI at one strike). Values above 0.10 suggest high concentration.
6. **Hedging scenarios** assume dealers are net short options. Positive GEX + upward move = dealers sell shares (negative delta hedge).

---

## `GET /v1/adv_volatility/{symbol}`

Returns advanced volatility analytics for quantitative analysis: raw SVI parameters per expiry, implied forward prices, total variance surface grid, butterfly and calendar arbitrage detection, second/third-order greeks surfaces (vanna, charm, volga, speed), and variance swap fair values.

**Requires Alpha plan or higher.**

### Parameters

| Name | In | Required | Description |
|------|----|----------|-------------|
| `symbol` | path | yes | Underlying symbol (e.g. `SPY`) |

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" \
  "https://lab.flashalpha.com/v1/adv_volatility/SPY"
```

### Response `200`

```json
{
  "symbol": "SPY",
  "underlying_price": 580.51,
  "as_of": "2026-03-25T15:00:00Z",
  "market_open": true,

  "svi_parameters": [
    {
      "expiry": "2026-04-04",
      "days_to_expiry": 10,
      "forward": 581.25,
      "a": 0.004521,
      "b": 0.031245,
      "rho": -0.182345,
      "m": 0.012345,
      "sigma": 0.098765,
      "atm_total_variance": 0.008912,
      "atm_iv": 17.85
    }
  ],

  "forward_prices": [
    {
      "expiry": "2026-04-04",
      "days_to_expiry": 10,
      "forward": 581.25,
      "spot": 580.51,
      "basis_pct": 0.1275
    }
  ],

  "total_variance_surface": {
    "moneyness": [-0.5, -0.475, "...", 0.475, 0.5],
    "expiries": ["2026-04-04", "2026-04-17"],
    "tenors": [0.027397, 0.063014],
    "total_variance": [[0.0089, 0.0087, "..."], ["..."]],
    "implied_vol": [[18.05, 17.92, "..."], ["..."]]
  },

  "arbitrage_flags": [
    {
      "expiry": "2026-04-04",
      "type": "butterfly",
      "strike_or_k": -0.35,
      "description": "Negative butterfly at k=-0.350: d²w/dk²=-0.0152"
    },
    {
      "expiry": "2026-04-04/2026-04-17",
      "type": "calendar",
      "strike_or_k": 0.2,
      "description": "Calendar arb at k=0.2: w(2026-04-04)=0.0125 > w(2026-04-17)=0.0118"
    }
  ],

  "variance_swap_fair_values": [
    {
      "expiry": "2026-04-04",
      "days_to_expiry": 10,
      "fair_variance": 0.009234,
      "fair_vol": 18.35,
      "atm_iv": 17.85,
      "convexity_adjustment": 0.50
    }
  ],

  "greeks_surfaces": {
    "vanna": {
      "strikes": [555, 560, 565, "...", 600, 605],
      "expiries": ["2026-04-04", "2026-04-17"],
      "values": [[0.00012345, 0.00023456, "..."], ["..."]]
    },
    "charm": { "strikes": ["..."], "expiries": ["..."], "values": [["..."]] },
    "volga": { "strikes": ["..."], "expiries": ["..."], "values": [["..."]] },
    "speed": { "strikes": ["..."], "expiries": ["..."], "values": [["..."]] }
  }
}
```

### Response Fields

| Section | Field | Description |
|---------|-------|-------------|
| **SVI Parameters** | | Raw SVI (Stochastic Volatility Inspired) fit parameters per expiry slice |
| `svi_parameters[]` | `a`, `b`, `rho`, `m`, `sigma` | SVI raw parameterization: w(k) = a + b(ρ(k−m) + √((k−m)² + σ²)) |
| `svi_parameters[]` | `forward` | Implied forward price from put-call parity |
| `svi_parameters[]` | `atm_total_variance` | w(0) — total variance at-the-money |
| `svi_parameters[]` | `atm_iv` | ATM implied vol (%) derived from total variance |
| **Forward Prices** | | Implied forward prices per expiry with cost-of-carry basis |
| `forward_prices[]` | `basis_pct` | (Forward − Spot) / Spot × 100 |
| **Total Variance Surface** | | 2D grid of total variance w(k,T) and implied vol across moneyness and expiries |
| `total_variance_surface` | `moneyness` | Log-moneyness grid: −0.5 to +0.5 in 0.025 steps (41 points) |
| `total_variance_surface` | `tenors` | Time to expiry in years for each expiry |
| `total_variance_surface` | `total_variance` | w(k,T) values — rows are expiries, columns are moneyness |
| `total_variance_surface` | `implied_vol` | IV (%) derived from total variance: σ = √(w/T) × 100 |
| **Arbitrage Flags** | | Detected no-arbitrage violations in the fitted surface |
| `arbitrage_flags[]` | `type` | `butterfly` (d²w/dk² < 0) or `calendar` (w decreasing in T) |
| `arbitrage_flags[]` | `strike_or_k` | Log-moneyness where violation occurs |
| **Variance Swap** | | Fair variance swap values per expiry via numerical SVI integration |
| `variance_swap_fair_values[]` | `fair_variance` | Integrated fair variance over [−15%, +15%] moneyness |
| `variance_swap_fair_values[]` | `fair_vol` | √(fair_variance / T) × 100 |
| `variance_swap_fair_values[]` | `convexity_adjustment` | fair_vol − atm_iv — positive = convexity premium from wings |
| **Greeks Surfaces** | | 2D grids of higher-order greeks across strikes (±15% of spot) and expiries |
| `greeks_surfaces.vanna` | | ∂²V/∂S∂σ — delta sensitivity to vol changes |
| `greeks_surfaces.charm` | | ∂²V/∂S∂t — delta decay over time (call options) |
| `greeks_surfaces.volga` | | ∂²V/∂σ² — vega convexity |
| `greeks_surfaces.speed` | | ∂³V/∂S³ — gamma sensitivity to spot |

### Errors

| Status | Description |
|--------|-------------|
| `403` | Requires Alpha plan or higher |
| `404` | Symbol not found or no data |

### Notes

- SVI fitting uses the raw parameterization of Gatheral (2004). Fits are filtered — slices with poor ATM IV or too few data points are rejected.
- Arbitrage detection uses a tolerance of 0.01 for butterfly and 0.001 for calendar to filter numerical noise.
- Greeks surfaces are computed via BSM formulas from stored BSM IV per contract (not from SVI). Strike range is ±15% of spot.
- Variance swap fair value uses trapezoidal integration over ±15% moneyness range (500 steps). Wing extrapolation beyond this range is excluded to avoid SVI noise.

---

## `GET /v1/vrp/{symbol}`

Full Volatility Risk Premium dashboard. Combines live IV/RV/GEX data with historical percentiles, regime classification, strategy suitability scores, and macro context.

**Requires Alpha plan or higher.**

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `symbol` | path | Stock/ETF ticker (e.g., `SPY`, `QQQ`, `TSLA`) |

### Response

| Field | Type | Description |
|-------|------|-------------|
| **Core VRP** | | |
| `vrp.atm_iv` | `number` | ATM implied volatility (%, from BSM on live options via Thetadata) |
| `vrp.rv_5d` ... `rv_30d` | `number` | Realized volatility windows (annualized %, from Yahoo Finance closes) |
| `vrp.vrp_5d` ... `vrp_30d` | `number` | VRP spread = ATM_IV - RV for each window |
| `vrp.z_score` | `number?` | Z-score of current VRP vs 60-day history (null if < 5 days history) |
| `vrp.percentile` | `number?` | Percentile rank of current VRP (0-100, null if insufficient history) |
| **Variance Premium** | | |
| `variance_risk_premium` | `number` | VRP in variance space (IV^2 - RV^2), per Carr & Wu (2009) |
| `convexity_premium` | `number` | Fair vol (OI-weighted) minus ATM IV — positive = wings are rich |
| `fair_vol` | `number` | OI-weighted average IV across ±20% moneyness |
| **Directional VRP** | | |
| `directional.put_wing_iv_25d` | `number` | 25-delta put IV (%) |
| `directional.call_wing_iv_25d` | `number` | 25-delta call IV (%) |
| `directional.downside_rv_20d` | `number` | RV from negative returns only (downside semivariance) |
| `directional.upside_rv_20d` | `number` | RV from positive returns only |
| `directional.downside_vrp` | `number` | Put-wing IV minus downside RV |
| `directional.upside_vrp` | `number` | Call-wing IV minus upside RV |
| **Term VRP Curve** | | |
| `term_vrp[]` | `array` | VRP by expiry bucket (7, 14, 30, 60 DTE) |
| `term_vrp[].dte` | `number` | Days to expiry |
| `term_vrp[].iv` | `number` | ATM IV for this tenor |
| `term_vrp[].rv` | `number` | Term-matched realized vol |
| `term_vrp[].vrp` | `number` | VRP spread for this tenor |
| **GEX-Conditioned** | | |
| `gex_conditioned.regime` | `string` | `positive_gamma` or `negative_gamma` |
| `gex_conditioned.harvest_score` | `number` | 0-1 harvestability score (higher = safer to sell premium) |
| `gex_conditioned.interpretation` | `string` | Human-readable regime interpretation |
| **Vanna-Conditioned** | | |
| `vanna_conditioned.outlook` | `string` | Vol compression/expansion outlook |
| `vanna_conditioned.interpretation` | `string` | How vanna flows affect premium selling |
| **Regime** | | |
| `regime.gamma` | `string` | `positive_gamma` or `negative_gamma` |
| `regime.vrp_regime` | `string?` | `harvestable`, `event_only`, `toxic_short_vol`, `cheap_convexity`, or `surface_distorted` |
| `regime.net_gex` | `number` | Net gamma exposure ($) |
| `regime.gamma_flip` | `number` | Gamma flip strike |
| **Strategy Scores** (0-100) | | |
| `strategy_scores.short_put_spread` | `number` | Short put spread suitability |
| `strategy_scores.short_strangle` | `number` | Short strangle suitability |
| `strategy_scores.iron_condor` | `number` | Iron condor suitability |
| `strategy_scores.calendar_spread` | `number` | Calendar spread suitability |
| **Composite** | | |
| `net_harvest_score` | `number` | 0-100 composite: is premium selling viable right now? |
| `dealer_flow_risk` | `number` | 0-100 dealer hedging amplification risk |
| `warnings` | `string[]` | Active warning flags: `event_risk`, `negative_gamma`, `poor_wing_liquidity`, `term_inversion`, `credit_stress`, `extreme_vrp` |
| **Macro** | | |
| `macro.vix` | `number` | VIX spot |
| `macro.vix_3m` | `number` | VIX3M (3-month VIX) |
| `macro.vix_term_slope` | `number` | VIX3M/VIX ratio (>1 = contango, <1 = backwardation) |
| `macro.dgs10` | `number` | 10-Year Treasury yield |
| `macro.hy_spread` | `number` | ICE BofA High Yield OAS (credit stress indicator) |
| `macro.fed_funds` | `number` | Federal Funds rate |

### Errors

| Status | Description |
|--------|-------------|
| `403` | Requires Alpha plan or higher |
| `404` | Symbol not found or no data |

---

## `GET /v1/vrp/{symbol}/history`

Daily VRP time series for charting and backtesting. Populated by nightly data service after market close.

**Requires Alpha plan or higher.**

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `symbol` | path | | Stock/ETF ticker |
| `days` | query | `30` | Lookback days (1-365) |

### Response

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | `string` | Ticker symbol |
| `days` | `number` | Requested lookback |
| `data_points` | `number` | Number of data points returned |
| `history[].date` | `date` | Snapshot date |
| `history[].spot` | `number` | Close price |
| `history[].atm_iv` | `number?` | ATM IV (%) |
| `history[].rv_5d` ... `rv_30d` | `number?` | Realized vol windows |
| `history[].vrp_20d` | `number?` | VRP spread (ATM_IV - RV20d) |
| `history[].straddle` | `number?` | ATM straddle price ($) |
| `history[].expected_move_1d` | `number?` | 1-day expected move ($) |

### Notes

- History accumulates daily after market close (4:35 PM ET). Z-score and percentile become available after 5+ data points.
- ATM IV is computed via BSM from Thetadata option snapshots (standalone, not dependent on real-time pollers).
- Realized vol is computed from Yahoo Finance historical closes using log returns and sample standard deviation.
- Data sources: spot (Thetadata/Yahoo), RV (Yahoo), IV (Thetadata + BSM), macro (FRED + Yahoo VIX).

---

## `GET /v1/account`

Returns account details, plan, and usage quota for the authenticated user.

### Example

```bash
curl -H "X-Api-Key: YOUR_API_KEY" https://lab.flashalpha.com/v1/account
```

### Response `200`

```json
{
  "user_id": "d621e6ab-b4fc-4d62-86fc-08e489477e11",
  "email": "user@example.com",
  "plan": "growth",
  "daily_limit": "1000",
  "usage_today": 42,
  "remaining": "958",
  "resets_at": "2026-03-09T00:00:00Z"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | string | User's unique identifier (GUID) |
| `email` | string | User's email address |
| `plan` | string | Plan name: `free`, `basic`, `growth`, `alpha`, `enterprise` |
| `daily_limit` | string | Daily request limit, or `"unlimited"` for Business/Institutional tiers |
| `usage_today` | integer | Number of API requests made today (always `0` for unlimited plans) |
| `remaining` | string | Requests remaining today, or `"unlimited"` |
| `resets_at` | string | ISO 8601 timestamp when the daily quota resets (midnight UTC) |

---

## `GET /health`

Returns system health status. **Public endpoint — no authentication required. Not rate limited.**

### Example

```bash
curl https://lab.flashalpha.com/health
```

### Response `200`

```json
{
  "status": "Healthy"
}
```

---

## Errors

All endpoints return consistent error responses.

### `401 Unauthorized`

```json
{
  "title": "Unauthorized",
  "status": 401,
  "detail": "Invalid API key."
}
```

### `403 Tier Restricted`

```json
{
  "status": "ERROR",
  "error": "tier_restricted",
  "message": "This endpoint requires the Growth plan or higher.",
  "current_plan": "Basic",
  "required_plan": "Growth"
}
```

### `404 Not Found`

```json
{
  "error": "symbol_not_found",
  "message": "No data for XYZ."
}
```

### `429 Too Many Requests`

```json
{
  "status": "ERROR",
  "error": "Quota exceeded",
  "message": "You have exceeded your daily API quota of 10 requests on the Free plan. Please upgrade to Basic for a higher limit.",
  "current_plan": "Free",
  "limit": 10,
  "upgrade_to": "Basic",
  "reset_at": "2026-03-01T00:00:00Z"
}
```

---

## Conventions

- All timestamps are **UTC** in ISO 8601 format
- All exposure values are in **USD notional**
- Dates use `yyyy-MM-dd` format
- GEX formula: `gamma * OI * 100 * spot^2 * 0.01` (per 1% move, SpotGamma convention)
- Greeks are calculated via **Black-Scholes-Merton** (not sourced from vendor)
- Implied volatility is smoothed via **SVI** (Stochastic Volatility Inspired) parameterization
- Dealer position is the **opposite** of net exposure (dealers are counterparty)
- OI changes are **day-over-day** deltas (when prior-day snapshot is available)
- Any US equity or ETF symbol is supported — data is fetched on-demand and cached for 15 seconds
