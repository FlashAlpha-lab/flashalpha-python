# sell-window: should you sell options today?

`GET https://lab.flashalpha.com/v1/strategies/sell-window/{symbol}`

Option sellers get wiped out on a few bad days. sell-window tells you which days to stay out, and on the days it says sell, it hands you the trades: which expiry, which strikes and how to exit. Every session, for SPY, QQQ and IWM. More than 5 million backtests led to this one endpoint.

## Two ways to use it

- **Experienced traders: avoid the bad sessions.** Keep your own strategy and use sell or skip per expiry as a risk switch: trade that expiry when it says sell, stand aside when it says skip.
- **Newer traders: follow the concrete picks.** On a sell, the response lists the expiry, the structure, the exact strikes and how to exit. How much you trade is your decision.

## Call it

```python
from flashalpha import FlashAlpha

fa = FlashAlpha("YOUR_API_KEY")
answer = fa.sell_window("SPY")

for window in answer["windows"]:
    print(window.get("expiry"), window["action"])  # sell, skip or unavailable
    for trade in window.get("candidates", []):
        print(" ", trade["structure"], trade.get("mid_credit"), trade["exit"])
```

Runnable example: [`examples/sell_window.py`](https://github.com/FlashAlpha-lab/flashalpha-python/blob/main/examples/sell_window.py)

```bash
FLASHALPHA_API_KEY=... python examples/sell_window.py SPY
```

The answer is set from the previous session's close and stays fixed for the session. It switches at the close (16:00 ET, 13:00 ET on early-close days): before the close it is for the current session, after the close and on closed days it is for the next session.

Without an SDK:

```bash
curl "https://lab.flashalpha.com/v1/strategies/sell-window/SPY" \
  -H "X-Api-Key: YOUR_API_KEY"
```

## Read the answer

A skip day:

```json
{
  "symbol": "SPY",
  "session": "2026-11-05",
  "windows": [
    { "expiry": "2026-11-05", "days_to_expiry": 0, "action": "skip" },
    { "expiry": "2026-11-12", "days_to_expiry": 7, "action": "skip" },
    { "expiry": "2026-11-18", "days_to_expiry": 13, "action": "skip" },
    { "expiry": "2026-12-04", "days_to_expiry": 29, "action": "skip" }
  ]
}
```

A sell day (one window and one trade shown):

```json
{
  "symbol": "SPY",
  "session": "2026-10-16",
  "spot": 772.255,
  "quoted_at": "2026-10-16T13:35:00Z",
  "legs_indicative": false,
  "windows": [
    { "expiry": "2026-10-16", "days_to_expiry": 0, "action": "sell",
      "candidates": [
        { "structure": "short_put", "exit": "expiry",
          "legs": [ { "side": "sell", "quantity": 1, "type": "put", "strike": 769, "delta": -0.19, "bid": 0.39, "ask": 0.4 } ],
          "mid_credit": 0.395 }
      ] }
  ]
}
```

| Field | Meaning |
|---|---|
| `symbol`, `session` | The symbol and the trading session the answer applies to (`yyyy-MM-dd`). |
| `spot`, `quoted_at`, `legs_indicative` | Present when a window sells and an option chain could be loaded. `legs_indicative: true` means the quotes are from before that session's 09:35 ET entry: call again at or after 09:35 ET for the strikes to trade. |
| `windows[]` | Always four entries: the same-day expiry, then the expiries closest to one week, two weeks and one month out. |
| `windows[].expiry`, `days_to_expiry` | The listed expiry this window trades. Absent when no listed expiry falls in the range. |
| `windows[].action` | `sell`, `skip` or `unavailable`. Treat `unavailable` like a skip. |
| `windows[].candidates[]` | Present only on `sell`. Can be empty: a trade whose legs cannot all be found in the chain is left out. |
| `candidates[].structure` | `short_put`, `short_call`, `short_strangle`, `short_straddle`, `tail_hedged_put`, `put_credit_spread` or `put_bwb`. |
| `candidates[].exit` | `expiry`: hold to expiration. `tp50`: close once the position can be bought back for half of the credit or less, otherwise hold to expiration. |
| `candidates[].legs[]` | `side`, `quantity`, `type`, `strike`, `delta`, `bid`, `ask` for one unit of the trade. Absent when no chain could be loaded. |
| `candidates[].mid_credit` | Net credit per share at mid. Multiply by 100 for one unit in dollars. |

## How strikes are picked

Only out-of-the-money contracts with a bid above zero, a bid/ask spread of at most 20% of the mid and open interest of at least 250. Among those, the contract whose delta is closest to the trade's target and within 0.05 of it; ties go to the tighter spread, then the higher open interest. A trade whose legs cannot all be found in the chain is left out, because the backtest could not have filled it either.

## The backtest

| Backtest, 2018 to 2026 | Following sell-window | Selling the same trades every day |
|---|---|---|
| Max drawdown at the same trade size | $255k | $959k |
| Worst month at the same trade size | -$171k | -$307k |
| Sharpe ratio | 0.76 | 0.61 |
| Total P&L at the same max drawdown | $3.55M | $2.32M |
| Worst day at the same max drawdown | -$258k | -$385k |

Cut the risk or earn more. Keep your trade size and the deepest drawdown falls 73%. Or size up about 3.8 times, until the deepest drawdown matches, and you earn 53% more. These are two separate choices, not one result.

Backtest on SPY, QQQ and IWM, January 2018 to October 2026, at halfway fills and $1 per contract. At one contract set per signal, following it made $945,541 on 20,883 trades; selling every day made $2,321,150 on 56,975. At 3.76 times the contracts, both fell $958,924 at their deepest, and the worst month was -$642,135 against -$307,241. Past results do not guarantee future returns, and short options can lose more than the premium collected. The skip call applies to new trades, so it cannot protect open positions from a sudden shock. This is data, not investment advice.

See [every backtested trade](https://flashalpha.com/articles/sell-window-backtest-every-trade-2018-2026).

## Why you can trust this backtest

- **More than 5 million backtests.** Strategies, deltas, expiries, exits and entry rules, on real quotes from 2018 to 2026. Most rules did not survive.
- **Tested against luck.** Trading less cuts drawdown on its own, so the rule was compared with 1,000 random schedules that skip the same number of days. Across SPY, QQQ and IWM from 2018 to 2026, it beat 90% of them on Sharpe ratio and 83% on drawdown.
- **The bar came first.** For each test, what would count as a pass was written down before running it. Rules built on the VIX curve and on price trend failed, so they were thrown out.
- **What it did not win is reported.** In 2017, a calm year with no selloff to avoid, its Sharpe ratio was 1.55 against 1.70 for selling every day.
- **No hindsight.** Each answer uses only the previous session's close. Trades enter at 09:35 ET at that day's quotes, fill halfway to the bid or ask, pay $1 a contract and are valued every day.
- **Check it yourself.** On Alpha, replay any session since 2018 through the historical API and get the answer it gives, strikes included.

## Forward test

A backtest shows the past, so the forward test runs in public. A paper bot follows the sell-window endpoint every session and posts the day's call and P&L on [Discord](https://discord.gg/UtH22J8df2).

## Plans

Live answers need Basic or higher through November 2026, and Growth or higher from December 1, 2026. Backtesting any past session needs Alpha or higher. See [plans](https://flashalpha.com/pricing).

## FAQ

### Should I sell options today?

Call the endpoint. For SPY, QQQ and IWM it says `sell`, `skip` or `unavailable` for four listed expiries in the current session. On a skip there is nothing to do. It gives data, not investment advice, and how much you trade is your decision.

### When should I not sell options?

When sell-window says `skip` for that expiry. The research behind it is in [When not to sell options](https://flashalpha.com/articles/when-not-to-sell-options-negative-gamma-spy-qqq-short-premium-backtest).

### Which strikes should I sell?

On a sell, `candidates` lists the trades with concrete strikes from the option chain, each contract's delta and quote, the credit at mid and the exit rule. The contract rules are in [How strikes are picked](#how-strikes-are-picked).

### Does it predict selloffs or market direction?

No. It tells you which sessions to stay out of. It does not forecast direction, and the skip call applies to new trades, so it cannot protect open positions from a sudden shock.

### Does following it make more money than selling every day?

Compare the two at the same risk. Sized to the same max drawdown (about 3.8 times the contracts), following it made $3.55M against $2.32M, with a smaller worst day and a deeper worst month. At the same trade size it trades about a third as often, so total P&L is lower ($945,541 against $2,321,150), and the deepest drawdown falls 73%.

### How was it tested?

More than 5 million backtests, then against 1,000 random schedules that skip the same number of days. See [Why you can trust this backtest](#why-you-can-trust-this-backtest).

### Can I check the results myself?

Yes. On Alpha, replay any session since 2018 with [flashalpha-historical-python](https://github.com/FlashAlpha-lab/flashalpha-historical-python) or the [historical API](https://flashalpha.com/docs/historical-sell-window).

### I already have a strategy. How do I use it?

Use sell or skip per expiry as a risk switch: trade that expiry when it says sell and stand aside when it says skip. The tests cover the candidate trades, not your strategy, so replay it on your own trades through the historical API first.

### Which symbols does it cover?

SPY, QQQ and IWM. Any other symbol returns HTTP 200 with every window `unavailable`.

### Which plan do I need?

Live answers need Basic or higher through November 2026, and Growth or higher from December 1, 2026. Backtesting any past session needs Alpha or higher.

### How do I follow it going forward?

A paper bot follows the endpoint every session and posts the day's call and P&L on [Discord](https://discord.gg/UtH22J8df2), so the forward test runs in public.

### How is it different from the other strategy endpoints?

The other `/v1/strategies/*` endpoints score one trade idea in a shared decision envelope. sell-window answers one question per expiry and has its own response shape, with no score.

## Links

- [API docs](https://flashalpha.com/docs/lab-api-strategies-sell-window)
- [Historical API docs](https://flashalpha.com/docs/historical-sell-window)
- [Trading guide: how to follow sell-window](https://flashalpha.com/articles/complete-guide-trading-sell-window-spy-qqq-iwm)
- [The backtest: every trade, 2018 to 2026](https://flashalpha.com/articles/sell-window-backtest-every-trade-2018-2026)
- [When not to sell options: the study that started this research](https://flashalpha.com/articles/when-not-to-sell-options-negative-gamma-spy-qqq-short-premium-backtest)
- [Plans](https://flashalpha.com/pricing)
- [Discord: the live forward test](https://discord.gg/UtH22J8df2)

## Other languages

- JavaScript / TypeScript: [flashalpha-js](https://github.com/FlashAlpha-lab/flashalpha-js)
- Go: [flashalpha-go](https://github.com/FlashAlpha-lab/flashalpha-go)
- Java: [flashalpha-java](https://github.com/FlashAlpha-lab/flashalpha-java)
- .NET: [flashalpha-dotnet](https://github.com/FlashAlpha-lab/flashalpha-dotnet)
- Backtesting (Python): [flashalpha-historical-python](https://github.com/FlashAlpha-lab/flashalpha-historical-python)

Keywords: should I sell options today, when not to sell options, sell or skip, option selling API, short premium risk filter, when to sell puts, which strikes to sell, 0DTE sell or skip, credit spread entry timing, SPY QQQ IWM option selling.
