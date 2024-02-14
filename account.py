import asyncio

from aiomql import Account

# use the account class to login

async def main():
    async with Account(login=123456, password='password', server='server') as acc:
        print(acc.balance)
        # perform some transactions refresh and check the balance 
        await acc.refresh()
        # get only margin, equity, balance
        acc_details = acc.get_dict(include=set('margin', 'equity', 'balance'))
        print(acc_details)
        
