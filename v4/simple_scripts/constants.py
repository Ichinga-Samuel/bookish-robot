from aiomql import OrderType, TimeFrame

buy = OrderType.BUY

print(buy) # OrderType.BUY

# get the opposite
sell = buy.opposite
print(sell) # OrderType.SELL
