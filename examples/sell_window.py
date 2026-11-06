"""Should you sell options today? Print the sell-window answer for one symbol.

Run:  FLASHALPHA_API_KEY=... python examples/sell_window.py SPY
Docs: https://flashalpha.com/docs/lab-api-strategies-sell-window
"""

import os
import sys

from flashalpha import FlashAlpha

symbol = sys.argv[1] if len(sys.argv) > 1 else "SPY"
fa = FlashAlpha(os.environ["FLASHALPHA_API_KEY"])
answer = fa.sell_window(symbol)

print(f"{answer['symbol']} session {answer['session']}")
if answer.get("legs_indicative"):
    print("Quotes are from before the 09:35 ET entry. Call again at or after 09:35 ET for the strikes to trade.")

for window in answer["windows"]:
    print(f"{window.get('expiry', 'no listed expiry')}: {window['action']}")
    for trade in window.get("candidates", []):
        legs = ", ".join(
            f"{leg['side']} {leg['quantity']} {leg['strike']:g} {leg['type']}" for leg in trade.get("legs", [])
        )
        credit = trade.get("mid_credit")
        credit_text = f"${credit * 100:,.2f} credit at mid" if credit is not None else "no quote"
        print(f"  {trade['structure']} ({legs}), {credit_text}, exit: {trade['exit']}")
