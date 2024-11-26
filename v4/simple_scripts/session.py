from datetime import time

from aiomql import Session, Sessions, Chaos, ForexSymbol

# Create individual sessions
# time is in 24-hour format and in UTC
session1 = Session(start=time(8),
                   end=time(16),
                   on_start="close_all",
                   on_end="close_all",
                   name="London")

session2 = Session(start=time(13), end=time(22, 0), name="New York")

# Combine sessions into a Sessions object
sessions = Sessions(sessions=[session1, session2])

# Create a Chaos Strategy
eur = ForexSymbol(name="EURUSD")
chaos = Chaos(sessions=sessions, symbol=eur)
