from src.services.generation.llm_factory import LLMFactory
from src.utils.logger import logger

class GenerationService:
    """
    Service to handle response generation using ChatBedrock LLM.
    """
    
    def __init__(self):
        logger.info("Initializing GenerationService")
        
        self.llm = LLMFactory.create_llm()
        
        logger.info("GenerationService initialized successfully.")
    
    def get_llm(self):
        """Return the LLM instance."""
        return self.llm
