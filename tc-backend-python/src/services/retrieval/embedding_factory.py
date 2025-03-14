from langchain_aws import BedrockEmbeddings
from langchain_openai import OpenAIEmbeddings
from src.utils.environment import AMAZON_REGION, EMBEDDINGS_MODEL_ID, EMBEDDINGS_PROVIDER

class EmbeddingFactory:
    """
    Factory to create embeddings based on the specified provider (Bedrock or OpenAI).
    """
    
    @staticmethod
    def create_embeddings():
        if EMBEDDINGS_PROVIDER == "bedrock":
            return BedrockEmbeddings(
                region_name=AMAZON_REGION,
                model_id=EMBEDDINGS_MODEL_ID,
            )
        elif EMBEDDINGS_PROVIDER == "openai":
            return OpenAIEmbeddings(model=EMBEDDINGS_MODEL_ID)
        else:
            raise ValueError(f"Unsupported embedding provider: {EMBEDDINGS_PROVIDER}")
