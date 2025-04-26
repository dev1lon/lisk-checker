import asyncio

import aiohttp
from aiohttp import ContentTypeError
from aiohttp_proxy import ProxyConnector
from fake_useragent import UserAgent

from utils import logger, semaphore


logger = logger.get_logger()


async def checker(address, proxy):
    async with semaphore.semaphore:

        headers = {'user-agent': UserAgent().random}
        json = {'wallet_address': address}

        connector = ProxyConnector.from_url(f'http://{proxy}')

        for i in range(0,3):
            try:
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.post(url='https://lisk.com/wp-json/bornfight/v1/eligibility-check', headers=headers, json=json) as response:
                        if response.status == 502:
                            raise ContentTypeError
                        data = await response.json()
                        logger.success(f"{address} | {data['message']}")
                        return
            except ContentTypeError:
                logger.warning(f'{address} | Failed request. Retry')
                await asyncio.sleep(30)
            logger.error(f'{address} | Failed request. Attempts finished')