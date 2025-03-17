import os
import asyncio
from pathlib import Path

from utils import utils, checker

BASE_DIR = Path(__file__).resolve().parent
addresses = utils.read_file(os.path.join(BASE_DIR, "addresses.txt"))
proxies = utils.read_file(os.path.join(BASE_DIR, "proxies.txt"))


async def main():
    if len(addresses) != len(proxies):
        raise Exception('Приватные ключи не соответствуют количеству прокси')
    elif len(addresses) == 0 or len(proxies) == 0:
        raise Exception('Нет прокси и приватников')

    tasks = []
    for address, proxy in zip(addresses, proxies):
        tasks.append(checker.checker(address=address, proxy=proxy))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())