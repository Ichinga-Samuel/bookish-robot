import asyncio

from aiomql import Account


async def manage_account():
    print(Account().config.account_info())
    async with Account() as account:
        print("Account successfully connected!")
        print(account.dict)

async def check_account():
    res = await Account().mt5.initialize()
    les = await Account().mt5.login()
    print(res, les)


asyncio.run(check_account())
