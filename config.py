"""
Configuration loader for the RAG Marketing Strategist System.
"""

import os
import yaml
from dotenv import load_dotenv


def load_config(config_path="settings.yaml"):
    """
    Load configuration from YAML file

    Args:
        config_path (str): Path to the configuration file

    Returns:
        dict: Configuration dictionary
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return get_default_config()


def load_environment_variables():
    """Load environment variables from .env file"""
    load_dotenv()

    # Check if GROQ_API_KEY is in environment variables
    if not os.getenv("GROQ_API_KEY"):
        print("WARNING: GROQ_API_KEY not found in environment variables.")
        print("Please set your GROQ API key or extract it from https://console.groq.com/keys")


def get_default_config():
    """
    Return default configuration if config file cannot be loaded

    Returns:
        dict: Default configuration dictionary
    """
    return {
        "vector_db": {
            "collection_name": "marketing_strategist_collection",
            "model_name": "all-MiniLM-L6-v2",
            "db_path": "./chroma_db",
            "chunk_size": 10
        },
        "generator": {
            "model_name": "mixtral-8x7b-32768",
            "max_tokens": 1000,
            "temperature": 0.7
        },
        "output": {
            "pdf_output_dir": "strategies"
        },
        "resources": {
            "pdf_source": "./Marketing_Strategies.pdf"
        },
        "prompts": {
            "system_prompt": "You are an AI marketing strategist designed to create comprehensive and effective marketing campaign plans..."
        }
    }