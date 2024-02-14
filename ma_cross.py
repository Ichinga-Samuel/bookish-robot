from aiomql import Strategy, Symbol, Trader, Candle, Candles, Tracker, TimeFrame, OrderType, find_bearish_fractal, find_bullish_fractal

class MACross(Strategy):
    ttf: TimeFrame
    first_ema: int
    second_ema: int
    parameters = {'first_ema': 13, 'second_ema': 34, 'ttf': TimeFrame.H4}
    def __init__(self, *, symbol: Symbol, params: dict = None, trader: Trader = None):
         self.tracker = Tracker(snooze=self.etf)
         self.name = 'MACross'

    async def find_trend():
        candles = await self.symbol.copy_rates_from_pos(count=self.cc, timeframe=self.ttf)  #1
        candles.ta.ema(length=self.first_ema, append=True)
        candles.ta.ema(length=self.second_ema, append=True)                                 #2
        candles.rename({f'EMA_self.{first_ema}': 'fast', f'EMA_self.{fast_ema}': 'slow')    #3
        candles['caf'] = candles.ta_lib.above(candles.close, candles.fast)
        candles['cbs'] = candles.ta_lib.below(candles.close, candles.fast)                   #4
        candles['fxs'] = candles.ta_lib.cross(candles.fast, candles.slow)
        candles['sxf'] = candles.ta_lib.cross(candles.fast, candles.slow, above=False)       #5
        current = candles[-1]                                                                #6 
        if current.fxs and current.caf:                                                      #7
           sl = find_bullish_fractal(candles)
           self.tracker.update(order_type=OrderType.BUY, sl=sl)                              #8
        elif current.sxf and current.cbs:                                                    #9 
            sl = find_bearish_fractal(candles)
            self.tracker.update(order_type=OrderType.SELL, sl=sl)                            #10
        else:
             self.tracker.update(order_type=None)

      async def trade():
          print(f"Trading {self.symbol} with {self.name}")
          while True:
             await self.sess.check()                                                         #11      
             await self.find_trend()
             if not self.tracker.order_type is None:
                await self.trader.place_trade(order_type=self.tracker.order_type, sl=sl, parameters=self.parameters)  #12
             await self.sleep(self.etf.time)                                                                          #13   
            continue
          
           
