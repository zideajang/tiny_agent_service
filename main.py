import asyncio
from multiagent.clients.openai_api import OpenAIGPTAPI

async def main():
    openAIGPTAPI = OpenAIGPTAPI()

    # 测试异步方法
    # answer = await openAIGPTAPI.aask("hello world")
    # print(answer)

    # 测试 ask
    # answer = openAIGPTAPI.ask("牛奶是如何进行脱脂的，脱脂牛奶适合哪些人群饮用")
    # print(answer)

    # 测试 ask_code
    # answer = openAIGPTAPI.ask_code(['请扮演一个 Google Python 专家工程师，如果理解，回复明白','写一个hello world'])
    # print(answer)

    answer = await openAIGPTAPI.aask_code(['请扮演一个Google Python专家工程师，如果理解，回复明白', '写一个hello world'])
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())
  