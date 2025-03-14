from langchain_postgres.vectorstores import PGVector
from src.services.retrieval.embedding_factory import EmbeddingFactory
from src.utils.logger import logger
from src.utils.environment import COLLECTION_NAME, COLLECTIONS_TABLE, CONNECTION_URL, EMBEDDINGS_TABLE

class RetrievalService:
    """
    Service to handle retrieval of relevant documents using PGVector.
    """
    
    def __init__(self):
        logger.info("Initializing RetrievalService")
        
        self.embeddings = EmbeddingFactory.create_embeddings()

        self.vector_db = PGVector(
            embeddings=self.embeddings,
            collection_name=COLLECTION_NAME,
            collection_store_table=COLLECTIONS_TABLE,
            embedding_store_table=EMBEDDINGS_TABLE,
            connection=CONNECTION_URL,
            use_jsonb=True,
        )
        
        self.retriever = self.vector_db.as_retriever()
        logger.info("RetrievalService initialized successfully")
    
    def get_retriever(self):
        """Return the retriever instance."""
        return self.retriever
