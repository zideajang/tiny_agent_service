from typing import Optional

from abc import abstractmethod
from multiagent.clients.base_chatbot import BaseChatbot
from multiagent.logs import logger


class BaseGPTAPI(BaseChatbot):

    system_prompt = 'You are a helpful assistant.'

    def _user_msg(self, msg: str) -> dict[str, str]:
        return {"role": "user", "content": msg}
    
    def _assistant_msg(self, msg: str) -> dict[str, str]:
        return {"role": "assistant", "content": msg}
    
    def _system_msg(self, msg: str) -> dict[str, str]:
        return {"role": "system", "content": msg}
    
    def _system_msgs(self, msgs: list[str]) -> list[dict[str, str]]:
        return [self._system_msg(msg) for msg in msgs]
    
    def _default_system_msg(self):
        return self._system_msg(self.system_prompt)
    

    def ask(self, msg: str) -> str:
        message = [self._default_system_msg(), self._user_msg(msg)]
        rsp = self.completion(message)
        return self.get_choice_text(rsp)
    
    async def aask(self, msg: str, system_msgs: Optional[list[str]] = None) -> str:
        if system_msgs:
            message = self._system_msgs(system_msgs) + [self._user_msg(msg)]
        else:
            message = [self._default_system_msg(), self._user_msg(msg)]
        rsp = await self.acompletion(message)
        logger.debug(message)
        # logger.debug(rsp)
        return self.get_choice_text(rsp)
    
    def _extract_assistant_rsp(self, context):
        return "\n".join([i["content"] for i in context if i["role"] == "assistant"])
    

