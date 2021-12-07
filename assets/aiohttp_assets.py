import aiohttp


async def aiohttp_get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = (await response.content.read()).decode('utf-8')
            return response


async def aiohttp_get_binary(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = (await response.content.read())
            return response


async def aiohttp_post(url: str, data: dict = None, params: dict = None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, params=params) as response:
            response = (await response.content.read()).decode('utf-8')
            return response


async def aiohttp_post_binary(url: str, data: dict = None, params: dict = None):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, params=params) as response:
            response = (await response.content.read())
            return response
