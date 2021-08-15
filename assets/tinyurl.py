import aiohttp


async def get_tinyurl(link: str):
    url = f"http://tinyurl.com/api-create.php?url={link}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = (await response.content.read()).decode('utf-8')
    return response
