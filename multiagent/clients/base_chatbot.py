from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class BaseChatbot(ABC):

    mode: str = "API"

    @abstractmethod
    def ask(self, msg: str) -> str:
        """Ask LLM a question and get an answer"""

    @abstractmethod
    def ask_batch(self,msgs:list) -> str:
        """ask LLM a series of questions and get a series of answers"""

    @abstractmethod
    def ask_code(self, msgs: list) -> str:
        """Ask GPT multiple questions and get a piece of code"""