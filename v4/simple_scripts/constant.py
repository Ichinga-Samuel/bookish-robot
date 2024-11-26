from aiomql import OrderFilling, TimeFrame, OrderType

# Accessing an enum value
fok = OrderFilling.FOK
print(fok)  # Output: ORDER_FILLING_FOK

# Accessing properties or methods
hourly = TimeFrame.H1
print(hourly.seconds)  # Output: 3600
secs = hourly.seconds
print(TimeFrame.get_timeframe(secs))  # Output: TimeFrame.H1

buy = OrderType.BUY
print(buy) # OrderType.BUY

# get the opposite
sell = buy.opposite
print(sell) # OrderType.SELL
