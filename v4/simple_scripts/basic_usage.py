import asyncio

from aiomql import MetaTrader


async def basic():
    mt5 = MetaTrader()
    init = await mt5.initialize()
    print(init)
    login = await mt5.login(login=40311691, password="Aiomql-Demo1", server="Deriv-Demo")
    print(login)
    acc_info = await mt5.account_info()
    print(acc_info)


def basic_sync():
    mt5 = MetaTrader()
    init = mt5._initialize()
    print(init)
    login = mt5._login(login=40311691, password="Aiomql-Demo1", server="Deriv-Demo")
    print(login)
    acc_info = mt5._account_info()
    print(acc_info)


# basic_sync()

async def main():
    await basic()

asyncio.run(main())
