from aiomql import Trader, ForexSymbol, RAM


class SimpleTrader(Trader):

   def __init__(self, *, symbol, ram: RAM = None)
       ram = ram or Ram(risk_to_reward=2, loss_limit=4)              #1
       super().__init__(symbol=symbol ram=ram) 

   async def create_order(self, order_type: OrderType, sl: float):
        pos = await self.ram.check_losing_positions()
        if pos:
            raise RuntimeError(f"More than {self.ram.loss_limit} losing positions")
        amount = await self.ram.get_amount()
        await self.symbol.info() 
        tick = await self.symbol.info_tick()
        points = (tick.ask - sl) / self.symbol.point if order_type == OrderType.BUY else (abs(tick.bid - sl) /
                                                                                          self.symbol.point)
        self.order.type = order_type
        volume, points = await self.symbol.compute_volume_points(amount=amount, points=points)
        self.order.volume = volume
        self.order.comment = self.parameters.get('name', self.__class__.__name__) 
        tick = await self.symbol.info_tick() 
        self.set_trade_stop_levels(points=points, tick=tick)

async def place_trade(self, *, order_type: OrderType, sl,  parameters: dict = None):
        try:
            self.parameters |= parameters or {}
            await self.create_order(order_type=order_type, sl=sl)
            if not await self.check_order():
                return
            await self.send_order()
        except Exception as err:
            logger.error(f"{err}. Symbol: {self.order.symbol}\n {self.__class__.__name__}.place_trade")


