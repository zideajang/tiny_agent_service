from __future__ import annotations

from dataclasses import dataclass,field
from typing import TypedDict

from azentengine.logs import logger


class RawMessage(TypedDict):
    content:str
    role:str 


class Message:

    content:str
    role: str = field(default='user')

    def __str__(self) -> str:
        return f"{self.role}: {self.content}"
    

    def __repr__(self) -> str:
        return self.__str__
    
    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content
        }