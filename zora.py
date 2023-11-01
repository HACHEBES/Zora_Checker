import requests
from datetime import datetime
from aiohttp import ClientSession
import asyncio
from aiohttp import ContentTypeError


async def trans_and_time(session: ClientSession,address):

    try:
        async with session.get(f'https://zora.superscan.network/api/blockchain/7777777/address/{address}') as response:
            response_json = await response.json()
            balance = float(response_json['balance']['value']) / 10 ** 16
            txs = response_json['txs']
            date = response_json['activity']['last']['date']
            return balance, txs, date
    except Exception as e:
        print('Произошла ошибка:', str(e))
        return 0, 0, 0
async def cheker(session: ClientSession, address):

    balances = await trans_and_time(session, address=address)
    return f'{balances[1]}:{balances[0]}:{balances[2]}'

async def main():

    addresses = []
    with open('wallet.txt', 'r') as file:
        for line in file:
            addresses.append(line.strip())
    async with ClientSession() as session:
        tasks = [cheker(session, address) for address in addresses]
        results = await asyncio.gather(*tasks)
        with open('output.txt', 'w') as file:
            file.write('')
        for i in range(len(addresses)):
            with open('output.txt', 'a') as file:
                data = f'{addresses[i]}:{results[i]}'
                file.write(data + '\n')
        return results

asyncio.run(main())