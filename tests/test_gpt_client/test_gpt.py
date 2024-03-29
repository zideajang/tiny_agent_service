import pytest
from multiagent.logs import logger

@pytest.mark.usefixtures("llm_api")
class TestGPT:
    def test_llm_api_ask(self, llm_api):
        answer = llm_api.ask('hello chatgpt')
        print(answer)
        assert len(answer) > 0