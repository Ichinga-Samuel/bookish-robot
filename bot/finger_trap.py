import asyncio
import logging

from aiomql import Tracker, ForexSymbol, TimeFrame, OrderType, Sessions, Strategy, Candles, Trader
from aiomql.utils import find_bearish_fractal, find_bullish_fractal

from trader import SimpleTrader

logger = logging.getLogger(__name__)


class FingerTrap(Strategy):
    ttf: TimeFrame
    etf: TimeFrame
    fast_ema: int
    slow_ema: int
    entry_ema: int
    ecc: int
    tcc: int
    trader: Trader
    tracker: Tracker

    parameters = {"fast_ema": 8, "slow_ema": 20, "etf": TimeFrame.M5,
                  "ttf": TimeFrame.H1, "entry_ema": 5, "tcc": 672, "ecc": 3360}  # 1

    def __init__(self, *, symbol: ForexSymbol, params: dict | None = None, trader: Trader = None,
                 sessions: Sessions = None, name: str = 'FingerTrap'):
        super().__init__(symbol=symbol, params=params, sessions=sessions, name=name)
        self.trader = trader or SimpleTrader(symbol=self.symbol)
        self.tracker: Tracker = Tracker(snooze=self.ttf.time)  # 2

    async def check_trend(self):
        try:
            candles: Candles = await self.symbol.copy_rates_from_pos(timeframe=self.ttf, count=self.tcc)  # 3
            if not ((current := candles[-1].time) >= self.tracker.trend_time):  # 4
                self.tracker.update(new=False, order_type=None)
                return
            self.tracker.update(new=True, trend_time=current)
            candles.ta.ema(length=self.slow_ema, append=True, fillna=0)
            candles.ta.ema(length=self.fast_ema, append=True, fillna=0)
            candles.rename(inplace=True, **{f"EMA_{self.fast_ema}": "fast", f"EMA_{self.slow_ema}": "slow"})  # 5

            candles['fas'] = candles.ta_lib.above(candles.fast, candles.slow)
            candles['fbs'] = candles.ta_lib.below(candles.fast, candles.slow)
            candles['caf'] = candles.ta_lib.above(candles.close, candles.fast)
            candles['cbf'] = candles.ta_lib.below(candles.close, candles.fast)  # 6
            current = candles[-1]
            if current.fas and current.caf:
                self.tracker.update(trend="bullish")
            elif current.fbs and current.cbf:
                self.tracker.update(trend="bearish")  # 7
            else:
                self.tracker.update(trend="ranging", snooze=self.ttf.time, order_type=None) # 8
        except Exception as err:
            logger.error(f"{err} for {self.symbol} in {self.__class__.__name__}.check_trend")
            self.tracker.update(snooze=self.ttf.time, order_type=None)

    async def confirm_trend(self):
        try:
            candles = await self.symbol.copy_rates_from_pos(timeframe=self.etf, count=self.ecc)
            if not ((current := candles[-1].time) >= self.tracker.entry_time):
                self.tracker.update(new=False, order_type=None)  # 9
                return
            self.tracker.update(new=True, entry_time=current)
            candles.ta.ema(length=self.entry_ema, append=True)
            candles.rename(**{f"EMA_{self.entry_ema}": "ema"})
            candles['cae'] = candles.ta_lib.cross(candles.close, candles.ema)
            candles['cbe'] = candles.ta_lib.cross(candles.close, candles.ema, above=False)  # 10
            current = candles[-1]
            if self.tracker.bullish and current.cae:
                sl = find_bullish_fractal(candles).low
                self.tracker.update(snooze=self.ttf.time, order_type=OrderType.BUY, sl=sl)
            elif self.tracker.bearish and current.cbe:
                sl = find_bearish_fractal(candles).high
                self.tracker.update(snooze=self.ttf.time, order_type=OrderType.SELL, sl=sl)  # 11
            else:
                self.tracker.update(snooze=self.etf.time, order_type=None)
        except Exception as err:
            logger.error(f"{err} for {self.symbol} in {self.__class__.__name__}.confirm_trend")
            self.tracker.update(snooze=self.etf.time, order_type=None)

    async def watch_market(self):
        await self.check_trend()
        if not self.tracker.ranging:
            await self.confirm_trend()  # 12

    async def trade(self):
        print(f"Trading {self.symbol}")
        async with self.sessions as sess:
            await self.sleep(self.ttf.time)
            while True:
                await sess.check()
                try:
                    await self.watch_market()
                    if not self.tracker.new:
                        await asyncio.sleep(2)
                        continue
                    if self.tracker.order_type is None:
                        await self.sleep(self.tracker.snooze)
                        continue
                    await self.trader.place_trade(order_type=self.tracker.order_type, parameters=self.parameters,
                                                  sl=self.tracker.sl)  # 13
                    await self.sleep(self.tracker.snooze)
                except Exception as err:
                    logger.error(f"{err} For {self.symbol} in {self.__class__.__name__}.trade")
                    await self.sleep(self.ttf.time)
