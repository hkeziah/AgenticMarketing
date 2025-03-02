"""
Vector database implementation for the RAG Marketing Strategist System.
"""

import uuid
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize


class VectorDatabase:
    """
    A class to handle vector database operations for marketing content using Chroma DB.
    """

    def __init__(self, config):
        """
        Initialize the Vector Database

        Args:
            config (dict): Configuration dictionary from settings
        """
        self.config = config['vector_db']
        self.db_path = self.config.get('db_path', './chroma_db')
        self.collection_name = self.config.get('collection_name', 'marketing_strategist_collection')
        self.model_name = self.config.get('model_name', 'all-MiniLM-L6-v2')

        # Initialize the Chroma DB client
        self.client = chromadb.PersistentClient(path=self.db_path)

        # Initialize the sentence transformer
        self.encoder = SentenceTransformer(self.model_name)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.model_name
        )

        # Get or create the collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function
        )

        print(f"Vector Database initialized with collection: {self.collection_name}")

    def add_text(self, text, chunk_size=None):
        """
        Add text to the vector database

        Args:
            text (str): Text to add to the database
            chunk_size (int, optional): Number of sentences per chunk
        """
        if chunk_size is None:
            chunk_size = self.config.get('chunk_size', 5)

        # Tokenize the text into sentences
        sentences = sent_tokenize(text, language="english")

        # Create chunks of text
        chunks = self._create_chunks(sentences, chunk_size)

        # Generate unique IDs for each chunk
        ids = [str(uuid.uuid4()) for _ in chunks]

        # Add chunks to the collection
        self.collection.add(
            documents=chunks,
            ids=ids
        )

        print(f"Added {len(chunks)} chunks to the vector database")

    def _create_chunks(self, sentences, chunk_size):
        """
        Create chunks of sentences

        Args:
            sentences (list): List of sentences
            chunk_size (int): Number of sentences per chunk

        Returns:
            list: List of text chunks
        """
        chunks = []
        for i in range(0, len(sentences), chunk_size):
            chunk = ' '.join(sentences[i:i + chunk_size])
            chunks.append(chunk)
        return chunks

    def retrieve(self, query, k=3):
        """
        Retrieve relevant chunks for a query

        Args:
            query (str): Query to search for
            k (int): Number of results to return

        Returns:
            list: List of relevant text chunks
        """
        results = self.collection.query(query_texts=[query], n_results=k)
        return results['documents'][0]