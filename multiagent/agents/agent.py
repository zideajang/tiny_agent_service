from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Type, Iterable

from multiagent.logs import logger
from multiagent.clients.openai_api import OpenAIGPTAPI


class RoleSetting:
    name: str
    profile: str
    goal: str
    constraints: str
    desc: str
    skills:list[str]

    def __str__(self):
        return f"{self.name}({self.profile})"

    def __repr__(self):
        return self.__str__()

@dataclass
class AgentContext:
    """Agent 运行时上下文"""
    env:  = field(default=None)
    memory: Memory = field(default_factory=Memory)
    state: int = field(default=0)
    todo: Action = field(default=None)
    watch: set[Type[Action]] = field(default_factory=set)

    @property
    def important_memory(self) -> list[Message]:
        """获得关注动作对应的信息"""
        return self.memory.get_by_actions(self.watch)

    @property
    def history(self) -> list[Message]:
        return self.memory.get()


class Agent:

    def __init__(self,name="",profile="",goal="",constraints="",desc=""):
        self._llm = OpenAIGPTAPI()

