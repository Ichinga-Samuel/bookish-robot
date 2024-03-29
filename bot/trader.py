from logging import getLogger

from aiomql import Trader, ForexSymbol, RAM, OrderType

logger = getLogger(__name__)


class SimpleTrader(Trader):

    def __init__(self, *, symbol: ForexSymbol, ram: RAM = None):
        ram = ram or RAM(risk_to_reward=2, loss_limit=4)  # 1
        super().__init__(symbol=symbol, ram=ram)

    async def create_order(self, order_type: OrderType, sl: float):
        pos = await self.ram.check_losing_positions()  # 2
        if pos:
            raise RuntimeError(f"More than {self.ram.loss_limit} losing positions")
        amount = await self.ram.get_amount()
        await self.symbol.info()
        tick = await self.symbol.info_tick()
        points = (tick.ask - sl) / self.symbol.point if order_type == OrderType.BUY else (abs(tick.bid - sl) /
                                                                                          self.symbol.point)  # 3
        self.order.type = order_type
        volume, points = await self.symbol.compute_volume_points(amount=amount, points=points)  # 4
        self.order.volume = volume
        self.order.comment = self.parameters.get('name', self.__class__.__name__)
        tick = await self.symbol.info_tick()
        self.set_trade_stop_levels(points=points, tick=tick)  # 5

    async def place_trade(self, *, order_type: OrderType, sl, parameters: dict = None):
        try:
            self.parameters |= parameters or {}
            await self.create_order(order_type=order_type, sl=sl)
            if not await self.check_order():
                return
            await self.send_order()
        except Exception as err:
            logger.error(f"{err} for {self.order.symbol} in {self.__class__.__name__}.place_trade")
