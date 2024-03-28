
import asyncio
from azentengine.roles import Role

class Environment:

    def __init__(self) -> None:
        self.roles: dict[str,Role] = {}


    def add_role(self,role:Role):