import time
from typing import Union, NamedTuple
from functools import wraps

import asyncio
import aiohttp

import requests

from multiagent.config import Config
from multiagent.logs import logger

from multiagent.utils.singleton import Singleton
from multiagent.utils.token_counter import TOKEN_COSTS

from multiagent.provider.base_gpt_api import BaseGPTAPI

def retry(max_retries):
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return await f(*args, **kwargs)
                except Exception as e:
                    if i == max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** i)
        return wrapper
    return decorator

class RateLimiter:
    """控制访问的速度频率"""
    def __init__(self,rpm) -> None:
        self.last_call_time = 0
        self.interval = 1.1 * 60 / rpm
        self.rpm = rpm

    def split_batches(self, batch):
        return [batch[i:i + self.rpm] for i in range(0, len(batch), self.rpm)]
    
    async def wait_if_needed(self,num_requests):
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time

        if elapsed_time < self.interval * num_requests:
            remaining_time = self.interval * num_requests - elapsed_time
            logger.info(f"sleep {remaining_time}")
            await asyncio.sleep(remaining_time)
            
        self.last_call_time = time.time()

class Costs(NamedTuple):
    total_prompt_tokens: int
    total_completion_tokens: int
    total_cost: float
    total_budget: float


# 计算开销
class CostManager(metaclass=Singleton):
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0
        self.total_budget = 0

        self.config = Config()

    def update_cost(self, prompt_tokens, completion_tokens, model): 
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens

        cost = (
            prompt_tokens * TOKEN_COSTS[model]["prompt"]
            + completion_tokens * TOKEN_COSTS[model]["completion"]
        ) / 1000


        self.total_cost += cost

        logger.info(f"Total running cost: ${self.total_cost:.3f} | Max budget: ${self.config.max_budget:.3f} | "
                    f"Current cost: ${cost:.3f}, {prompt_tokens=}, {completion_tokens=}")
        self.config.total_cost = self.total_cost

    def get_total_prompt_tokens(self):
        return self.total_prompt_tokens
    
    def get_total_completion_tokens(self):
        return self.total_completion_tokens
    
    def get_total_cost(self):
        return self.total_cost
    
    def get_costs(self) -> Costs:
        return Costs(self.total_prompt_tokens, self.total_completion_tokens, self.total_cost, self.total_budget)



class OpenAIGPTAPI(BaseGPTAPI,RateLimiter):

    def __init__(self) -> None:
        self.config = Config()
        self.__init_openai(self.config)
        self._cost_manager = CostManager()
        self.model = self.config.openai_api_model
        RateLimiter.__init__(self,rpm=self.rpm)
        
    def __init_openai(self, config):
        self.base_url = self.config.get("BASE_API_URL")
        self.rpm = int(config.get("RPM", 10))
    
    
    async def _achat_completion(self, messages: list[dict]) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, json={
                "messages":messages
            }) as response:
                rsp = await response.json()
                self._update_costs(rsp)
                return rsp

    def _chat_completion(self, messages: list[dict]) -> dict:
        rsp = requests.post(self.base_url, json={
            "messages":messages
        })
        print(rsp)
        print(type(rsp))
        rsp = rsp.json()
        self._update_costs(rsp)
        return rsp
    
    def completion(self, messages: list[dict]) -> dict:
        return self._chat_completion(messages)
    
    @retry(max_retries=1)
    async def acompletion(self, messages: list[dict]) -> dict:
        return await self._achat_completion(messages)
    
    async def acompletion_text(self, messages: list[dict]) -> str:
        rsp = await self._achat_completion(messages)
        return self.get_choice_text(rsp)
    

    async def acompletion_batch(self, batch: list[list[dict]]) -> list[dict]:
        """返回完整JSON"""
        split_batches = self.split_batches(batch)
        all_results = []

        for small_batch in split_batches:
            logger.info(small_batch)
            await self.wait_if_needed(len(small_batch))

            future = [self.acompletion(prompt) for prompt in small_batch]
            results = await asyncio.gather(*future)
            logger.info(results)
            all_results.extend(results)

        return all_results
    
    async def acompletion_batch_text(self, batch: list[list[dict]]) -> list[str]:
        """仅返回纯文本"""
        raw_results = await self.acompletion_batch(batch)
        results = []
        for idx, raw_result in enumerate(raw_results, start=1):
            result = self.get_choice_text(raw_result)
            results.append(result)
            logger.info(f"Result of task {idx}: {result}")
        return results
    
    def _update_costs(self, response: dict):
        usage = response.get('usage')
        prompt_tokens = int(usage['prompt_tokens'])
        completion_tokens = int(usage['completion_tokens'])
        self._cost_manager.update_cost(prompt_tokens, completion_tokens, self.model)

        
    def get_costs(self) -> Costs:
        return self._cost_manager.get_costs()


# 打开并读取 YAML 文件



if __name__ == "__main__":

    openAIGPTAPI = OpenAIGPTAPI()
    rsp = openAIGPTAPI.aask("hello world")
    print(rsp)


    exit(0)
    batch = [f"sequence_{i}" for i in  range(20)]

    rate_limiter = RateLimiter(5)
    # [[1,2,3,4,5],[1,2,3,4,5]]
    res = rate_limiter.split_batches(batch)
    # print(res)
    # print(batch)