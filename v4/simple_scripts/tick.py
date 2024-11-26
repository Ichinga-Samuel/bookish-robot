import asyncio
from datetime import datetime

from aiomql import MetaTrader, Tick, Ticks


async def main():
    start = datetime(2024, 11,20)
    async with MetaTrader() as mt5:
        # get the latest 100 ticks
        ticks = await mt5.copy_ticks_from("BTCUSD", start, 100, mt5.COPY_TICKS_ALL)
        ticks = Ticks(data=ticks)
        print(ticks)
        print(type(ticks[-1]))

        # get the last 10 ticks
        last_10 = ticks[-10:]

        # get the ask and bid price of the last tick
        last_tick = ticks[-1]
        ask, bid = last_tick.ask, last_tick.bid
        print(ask, bid)

        # get the ema of the bid price
        ticks.ta.ema(close='bid', length=8, append=True, fillna=0)
        ticks.rename(EMA_8='ema')

        # get the series of the ema
        ema = ticks['ema']
        print(ema)

asyncio.run(main())
