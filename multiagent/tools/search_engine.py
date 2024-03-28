import asyncio
from azentengine.logs import logger
from duckduckgo_search import AsyncDDGS
async def aget_results(word):
    results = await AsyncDDGS(proxies=None).text(word, max_results=100)
    return results

# TODO 这部分代码还需要解决

async def main():
    words = ["sun", "earth", "moon"]
    tasks = [aget_results(w) for w in words]
    results = await asyncio.gather(*tasks)
    print(results)

if __name__ == "__main__":
    
    asyncio.run(main())
    