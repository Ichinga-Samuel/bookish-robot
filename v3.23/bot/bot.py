import logging
from aiomql import ForexSymbol, Bot, Sessions

from finger_trap import FingerTrap

logging.basicConfig(level=logging.WARNING)


def run_bot():
    bot = Bot()
    symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'USDCAD', 'AUDUSD', 'NZDUSD', 'EURGBP', 'EURJPY', 'GBPJPY']
    strategies = [FingerTrap(symbol=ForexSymbol(name=symbol)) for symbol in symbols]
    bot.add_strategies(strategies)
    bot.execute()


run_bot()
