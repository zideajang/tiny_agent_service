
from azentengine.schema import Message

PREFIX_TEMPLATE = """You are a {profile}, named {name}, your goal is {goal}, and the constraint is {constraints}. """


class Role:


    async def _react(self) -> Message:
        pass


    async def run(self,message=None):
        if message:
            if isinstance(message, str):
                