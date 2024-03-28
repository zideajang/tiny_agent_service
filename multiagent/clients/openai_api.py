import time
from functools import wraps
import asyncio
from azentengine.config import Config
from azentengine.logs import logger


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
class OpenAIGPTAPI(RateLimiter):

    def __init__(self, rpm) -> None:
        self.config = Config()
        RateLimiter.__init__(self,rpm)

# 打开并读取 YAML 文件



if __name__ == "__main__":
    batch = [f"sequence_{i}" for i in  range(20)]

    rate_limiter = RateLimiter(5)
    # [[1,2,3,4,5],[1,2,3,4,5]]
    res = rate_limiter.split_batches(batch)
    print(res)
    # print(batch)