import asyncio

from aiomql import MetaTrader, Candle, Candles, TimeFrame


async def main():
    async with MetaTrader() as mt5:
        # get price bars from the terminal for the last 200 bars
        bars = await mt5.copy_rates_from_pos("EURUSD", TimeFrame.M1, 0, 200)

        # bar
        candles = Candles(data=bars)

        # get the latest candle by accessing the last one.
        # Explore the candle object
        last = candles[-1]  # A Candle object
        print(last)
        # print only ohlc
        print(last.dict(include={'open', 'high', 'low', 'close'}))

        # get the last five hours
        last_five = candles[-5:]  # A Candles object.

        # confirm that slicing returns a Candles object
        print(type(last_five))
        print(last_five)

        # get the close price of all the candles
        close = candles['close']  # close price of all the candles as a pandas series
        print(type(close))
        print(close)

        # compute ema using pandas ta
        candles.ta.ema(length=34, append=True, fillna=0)
        # rename the column to ema
        candles.rename(EMA_34='ema')

        # use talib to compute crossover. This returns a series object that is not part of the candles object.
        closeXema = candles.ta_lib.cross(candles.close, candles.ema)
        candles.ta.above
        # add to the candles
        candles['closeXema'] = closeXema
        print(candles)

        # iterate over the first 5 candles
        for candle in candles[:5]:
            print(candle.open, candle.Index)


asyncio.run(main())
