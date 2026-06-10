"""Strategy signals, earnings analytics, and multi-leg structures (1.1.0).

Exercises three of the new endpoint families:
  - a strategy-signal decision envelope (vol carry),
  - earnings analytics (expected move into the next event),
  - a pure-math multi-leg structure P&L (a call vertical).

Reads the API key from the FLASHALPHA_API_KEY environment variable.
"""

import os

from flashalpha import FlashAlpha

fa = FlashAlpha(os.environ["FLASHALPHA_API_KEY"])

# 1. Strategy signal: volatility risk-premium carry (Alpha+).
#    Every strategy endpoint returns the same StrategyDecisionResponse shape.
carry = fa.strategy_vol_carry("SPY", target_short_delta=0.20, max_width=10)
print(f"vol-carry decision: {carry['decision']} (score {carry['score']}, regime {carry.get('regime')})")
for s in carry.get("best_structures", []):
    print(f"  #{s['rank']} {s['structure']} {s['expiry']} credit={s.get('credit')} edge={s.get('edge_score')}")
print()

# 2. Earnings: implied-move decomposition for the next event (Growth+).
em = fa.earnings_expected_move("AAPL")
print(f"AAPL earnings {em.get('earnings_date')}: implied move {em.get('implied_move_pct')}%")
print()

# 3. Structure: at-expiry P&L for a 100/110 call debit spread (Basic+, pure math).
pnl = fa.structure_pnl(
    legs=[
        {"action": "buy", "type": "call", "strike": 100, "premium": 3.20, "quantity": 1},
        {"action": "sell", "type": "call", "strike": 110, "premium": 1.10, "quantity": 1},
    ],
    min_underlying=80,
    max_underlying=130,
    points=81,
)
print(f"Call vertical: max_profit={pnl['max_profit']} max_loss={pnl['max_loss']} breakevens={pnl['breakevens']}")
