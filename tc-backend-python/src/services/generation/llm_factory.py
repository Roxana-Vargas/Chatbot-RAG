from langchain_aws import ChatBedrock
from langchain_openai import ChatOpenAI
from src.utils.environment import LLM_PROVIDER, LLM_MODEL_ID
from src.utils.logger import logger

class LLMFactory:
    """
    Factory to create LLM models based on the specified provider (Bedrock or OpenAI).
    """

    @staticmethod
    def create_llm():
        if LLM_PROVIDER == "bedrock":
            logger.info("Using Bedrock LLM")
            return ChatBedrock(model_id=LLM_MODEL_ID)

        elif LLM_PROVIDER == "openai":
            logger.info("Using OpenAI LLM")
            return ChatOpenAI(model=LLM_MODEL_ID, logprobs=True)

        else:
            raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
