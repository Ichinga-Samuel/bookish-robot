import asyncio

from aiomql import Order, Account, Symbol, OrderType


async def main():
    async with Account() as _:
        sym = Symbol(name="BTCUSD")
        await sym.initialize()
        volume = sym.volume_min
        sl = (sym.trade_stops_level + sym.spread) * 2 * sym.point
        # risk to reward ratio of 1:2
        tp = (sym.trade_stops_level + sym.spread) * 2 * sym.point * 2
        price = sym.ask
        sl = price - sl
        tp = price + tp
        req = {
            "symbol": sym.name,
            "price": price,
            "sl": sl,
            "tp": tp,
            "volume": volume,
            "type": OrderType.BUY,
            "comment": "aiomql"
        }
        order = Order(**req)
        margin = await order.calc_margin()
        print(margin, 'margin')
        ocr = await order.check()
        print(ocr, 'order check result')
        profit = await order.calc_profit()
        print(profit, 'profit')
        loss = await order.calc_loss()
        print(loss, 'loss')
        print('the profit is twice the loss')
        osr = await order.send()
        print(osr, 'order send result')


asyncio.run(main())
