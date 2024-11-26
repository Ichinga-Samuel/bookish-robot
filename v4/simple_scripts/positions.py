import asyncio
from datetime import datetime
from pytz import timezone
from aiomql import ForexSymbol, Positions, History, Order, OrderType, RAM, TradeAction, MetaTrader


async def main():
    async with MetaTrader() as mt5:
        pos = Positions()

        # close all open positions
        await pos.close_all()

        open_pos = await pos.get_positions()
        print(f'Number of open positions: {len(open_pos)}') # 0

        # get start time using local timezone
        tz = timezone('UTC')
        start = datetime.now(tz=tz)
        start = start.replace(minute=start.minute - 1)

        # create two symbols and initialize them
        sym1 = ForexSymbol(name="BTCUSD")
        sym2 = ForexSymbol(name="ETHUSD")
        await sym1.initialize()
        await sym2.initialize()


        # create first order
        order_type = OrderType.BUY
        volume = sym1.volume_min
        tick = await sym1.info_tick()
        sl = sym1.trade_stops_level + sym1.spread * 2 * sym1.point
        tp = sl * 2
        price = tick.ask
        sl = price - sl
        tp = price + tp
        order = Order(symbol=sym1.name, type=order_type, volume=volume, price=price, sl=sl, tp=tp)
        await order.send()

        # create second order
        order_type = OrderType.SELL
        volume = sym2.volume_min
        tick = await sym2.info_tick()
        price = tick.bid
        order2 = Order(symbol=sym2.name, type=order_type, volume=volume, price=price)
        await order2.send()

        # get the number of open positions
        open_pos = await pos.get_positions()
        total = len(open_pos)
        print(f'{total} Open positions')  # 2
        await asyncio.sleep(10)

        # close all open positions
        await pos.close_all()
        # get the number of open positions
        open_pos = await pos.get_positions()
        total = len(open_pos)
        print(f'{total} Open positions') # 0


asyncio.run(main())
