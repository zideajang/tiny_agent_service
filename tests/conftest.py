from unittest.mock import Mock
import pytest
from multiagent.logs import logger
from multiagent.clients.openai_api import OpenAIGPTAPI

class Context:
    def __init__(self):
        self._llm_api = OpenAIGPTAPI()

    @property
    def llm_api(self):
        return self._llm_api
    
@pytest.fixture(scope="package")
def llm_api():
    logger.info("Setting up the test")
    _context = Context()

    yield _context.llm_api

    logger.info("Tearing down the test")


@pytest.fixture(scope="function")
def mock_llm():
    # Create a mock LLM for testing
    return Mock()