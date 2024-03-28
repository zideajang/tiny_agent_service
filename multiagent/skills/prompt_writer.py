from abc import ABC
from typing import Union


class GPTPromptGenerator:
    
    def __init__(self) -> None:
        self._generators = {i:getattr(self, f"gen_{i}_style") for i in ['instruction', 'chatbot', 'query']}



if __name__ == "__main__":
    gpt_prompt_generator = GPTPromptGenerator()
    