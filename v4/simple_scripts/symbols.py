import asyncio
from datetime import datetime
from aiomql import Symbol, TimeFrame, Account


async def main():
    # Assume account details are in the config file
    async with Account():
        # symbol object must be created with a name
        sym = Symbol(name="BTCUSD")
        print(sym, 'name is the only available property')


        # initialize the symbol to get properties
        await sym.initialize()
        # all the properties are now available
        print(sym.dict)


        # get the last 1000 rates.
        # data is returned as a Candles object
        candles = await sym.copy_rates_from_pos(timeframe=TimeFrame.H1, count=1000, start_position=0)
        print(len(candles))  # 1000

        # get candles of the last 24 hours
        today = datetime.now()
        yesterday = today.replace(day=today.day - 1)
        rates = await sym.copy_rates_range(timeframe=TimeFrame.H1, date_from=yesterday, date_to=today)
        print(len(rates))  # 24

        # get price ticks for the last 24 hours
        # data is returned as a Ticks object
        ticks = await sym.copy_ticks_range(date_from=yesterday, date_to=today)
        print(len(ticks))

        # get the current price tick
        tick = await sym.info_tick()
        # ask and bid price
        ask, bid = tick.ask, tick.bid
        print(ask, bid)


asyncio.run(main())
