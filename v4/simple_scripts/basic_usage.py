import asyncio
import os
from aiomql import MetaTrader, Config
from setuptools.command.setopt import config_file

config = Config(config_file='backtesting/trade_records/New folder/aiomql.json')
# config.load_config()
print(config.login)

# async def start():
#     mt5 = MetaTrader()
#     init = await mt5.initialize()
#     print(init)
#     login = await mt5.login(login=40311691, password="Aiomql-Demo1", server="Deriv-Demo")
#     print(login)
#     acc_info = await mt5.account_info()
#     print(acc_info)
#
#
#
# def start_sync():
#     mt5 = MetaTrader()
#     init = mt5._initialize()
#     print(init)
#     login = mt5._login(login=40311691, password="Aiomql-Demo1", server="Deriv-Demo")
#     print(login)
#     acc_info = mt5._account_info()
#     print(acc_info)
#
#
# # start_sync()
# asyncio.run(start())
