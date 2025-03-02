"""
LLM-based strategy generator for the RAG Marketing Strategist System.
"""

from groq import Groq
import os


class GroqGenerator:
    """
    A class to handle marketing strategy generation using the Groq API.
    """

    def __init__(self, config):
        """
        Initialize the Groq Generator

        Args:
            config (dict): Configuration dictionary from settings
        """
        self.config = config['generator']
        self.model_name = self.config.get('model_name', 'mixtral-8x7b-32768')
        self.max_tokens = self.config.get('max_tokens', 1000)
        self.temperature = self.config.get('temperature', 0.7)
        self.system_prompt = config.get('prompts', {}).get('system_prompt', '')

        # Initialize the Groq client
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        print(f"GroqGenerator initialized with model: {self.model_name}")

    def generate_strategy(self, input_description, retrieved_content):
        """
        Generate a marketing strategy using the Groq API

        Args:
            input_description (str): Description of the marketing campaign
            retrieved_content (list): Retrieved content from the vector database

        Returns:
            str: Generated marketing strategy
        """
        # Create the prompt
        prompt = f"Create a marketing campaign strategy for {input_description}. Use the following information:\n"
        prompt += "\n\n".join(retrieved_content)
        prompt += "\n\nStrategy:"

        try:
            # Generate the strategy
            chat_completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            # Return the generated strategy
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error generating strategy: {str(e)}")
            return f"Failed to generate strategy: {str(e)}"