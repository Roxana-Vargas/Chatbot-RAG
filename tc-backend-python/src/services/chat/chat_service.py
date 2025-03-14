import math
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough, RunnableLambda
from src.services.chat.prompt_templates import PROMPT_TEMPLATES
from src.utils.logger import logger
from src.services.retrieval.retrieval_service import RetrievalService
from src.services.generation.generations_service import GenerationService
from src.utils.environment import PROMPT_TEMPLATE
from langchain.schema import AIMessage
from src.utils.response_helpers import convert_documents_to_dict

class ChatService:
    """
    Chat service for performance using retrieval from PGVector and LLM response.
    """
    
    def __init__(self):
        logger.info("Initializing ChatService")

        self.retrieval_service = RetrievalService()
        self.generation_service = GenerationService()
        self.prompt_template = PROMPT_TEMPLATES[PROMPT_TEMPLATE]

        #  Create runnable chain
        self.chain = RunnableParallel({
            "context": self.retrieval_service.get_retriever(),
            "user_message": RunnablePassthrough(),
        }) | {
            "response": self.prompt_template | self.generation_service.get_llm() | RunnableLambda(self._calculate_confidence),
            "documents": lambda x: x["context"]
        }
        
        logger.info("ChatService initialized successfully")


    def process_message(self, user_message: str) -> dict:
        """
        Process user message using LangChain's Runnable Chain.
        Returns a dictionary containing the AI response and the retrieved documents.
        """
        try:
            logger.info(f"Processing user message: {user_message}")
            result = self.chain.invoke(user_message)
            
            # Extract the response and documents
            response_content = result["response"].content if hasattr(result["response"], 'content') else result["response"]
            documents = result["documents"]
            serializable_documents = convert_documents_to_dict(documents=documents)
            
            logger.info(f"AI response: {response_content}")
            return {
                "response": response_content,
                "documents": serializable_documents
            }
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "response": "Sorry, an error occurred while processing your request.",
                "documents": []
            }
    
    def _calculate_confidence(self, model_output: AIMessage) -> dict:
        """
        Calculate the confidence of the model output based on the logprobs.
        """
        logprobs = model_output.response_metadata.get("logprobs", None)
        
        if not logprobs or not logprobs.get("content"):
            logger.info("No logprobs found. Using default confidence.")
            confidence = 1.0

        else:
            # Calculate the confidence as the average of the token logprobs
            total_confidence = 0.0
            for token_data in logprobs["content"]:
                logprob = token_data["logprob"]
                total_confidence += math.exp(logprob)
            
            confidence = total_confidence / len(logprobs["content"])
            rounded_confidence = round(confidence, 2)
            logger.info(f"Confidence: {confidence}")

        return {
            "content": model_output.content, 
            "confidence": rounded_confidence
        }
