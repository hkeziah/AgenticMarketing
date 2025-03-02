"""
RAG Marketing Strategist implementation that combines vector database and LLM generator.
"""

from functools import lru_cache
from constants import STRATEGY_CACHE_SIZE


class RAGMarketingStrategist:
    """
    A class that combines the VectorDatabase and GroqGenerator to create an AI marketing strategist.
    """

    def __init__(self, vector_db, generator, cache_size=None):
        """
        Initialize the RAG Marketing Strategist

        Args:
            vector_db (VectorDatabase): Vector database instance
            generator (GroqGenerator): Strategy generator instance
            cache_size (int, optional): Size of the strategy cache
        """
        self.vector_db = vector_db
        self.generator = generator
        self.cache_size = cache_size if cache_size is not None else STRATEGY_CACHE_SIZE

        # Initialize the create_strategy method with LRU cache
        self.create_strategy = lru_cache(maxsize=self.cache_size)(self._create_strategy)

        print(f"RAG Marketing Strategist initialized with cache size: {self.cache_size}")

    def _create_strategy(self, input_description):
        """
        Create a marketing strategy for the given input description

        Args:
            input_description (str): Description of the marketing campaign

        Returns:
            str: Generated marketing strategy
        """
        # Retrieve relevant content from the vector database
        relevant_content = self.vector_db.retrieve(input_description)

        # Generate the strategy using the retrieved content
        strategy = self.generator.generate_strategy(input_description, relevant_content)

        return strategy

    def clear_cache(self):
        """Clear the strategy cache"""
        self.create_strategy.cache_clear()
        print("Strategy cache cleared")