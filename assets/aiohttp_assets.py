import aiohttp


async def aiohttp_get(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_list = (await response.content.read()).decode('utf-8')
            return response_list
