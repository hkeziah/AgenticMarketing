"""
Main entry point for the RAG Marketing Strategist System.

This system uses Retrieval-Augmented Generation (RAG) to create marketing campaign strategies.
It combines a vector database for storing and retrieving relevant marketing information
with a language model for generating comprehensive and effective strategies.
"""

import os
import argparse
from config import load_config, load_environment_variables
from utils import setup_nltk, extract_text_from_pdf, save_strategy_as_pdf
from vector_db import VectorDatabase
from generator import GroqGenerator
from strategist import RAGMarketingStrategist


def parse_arguments():
    """
    Parse command-line arguments

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='RAG Marketing Strategist System')
    parser.add_argument(
        '--config',
        type=str,
        default='settings.yaml',
        help='Path to the configuration file'
    )
    parser.add_argument(
        '--query',
        type=str,
        help='Marketing campaign description to generate a strategy for'
    )
    parser.add_argument(
        '--add-pdf',
        type=str,
        help='Path to a PDF file to add to the vector database'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save the generated strategy as a PDF'
    )
    return parser.parse_args()


def initialize_system(config):
    """
    Initialize the RAG Marketing Strategist System

    Args:
        config (dict): Configuration dictionary

    Returns:
        tuple: (VectorDatabase, GroqGenerator, RAGMarketingStrategist) instances
    """
    # Initialize the vector database
    vector_db = VectorDatabase(config)

    # Initialize the strategy generator
    generator = GroqGenerator(config)

    # Initialize the RAG Marketing Strategist
    strategist = RAGMarketingStrategist(vector_db, generator)

    return vector_db, generator, strategist


def add_pdf_to_vector_db(vector_db, pdf_path, config):
    """
    Add content from a PDF file to the vector database

    Args:
        vector_db (VectorDatabase): Vector database instance
        pdf_path (str): Path to the PDF file
        config (dict): Configuration dictionary
    """
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Add the text to the vector database
    if pdf_text:
        chunk_size = config['vector_db'].get('chunk_size', 5)
        vector_db.add_text(pdf_text, chunk_size)
        print(f"Content from {pdf_path} added to the vector database")
    else:
        print(f"Failed to extract text from {pdf_path}")


def main():
    """Main function to run the RAG Marketing Strategist System"""
    # Parse command-line arguments
    args = parse_arguments()

    # Load environment variables
    load_environment_variables()

    # Set up NLTK
    setup_nltk()

    # Load configuration
    config = load_config(args.config)

    # Initialize the system
    vector_db, generator, strategist = initialize_system(config)

    # Add a PDF to the vector database if specified
    if args.add_pdf:
        add_pdf_to_vector_db(vector_db, args.add_pdf, config)
    elif config.get('resources', {}).get('pdf_source'):
        # Use default PDF from configuration
        default_pdf = config['resources']['pdf_source']
        if os.path.exists(default_pdf):
            add_pdf_to_vector_db(vector_db, default_pdf, config)

    # Generate a strategy if a query is specified
    if args.query:
        # Generate the strategy
        strategy = strategist.create_strategy(args.query)

        # Print the strategy
        print(f"\nMarketing Strategy for '{args.query}':\n")
        print(strategy)

        # Save the strategy as a PDF if specified
        if args.save:
            output_dir = config.get('output', {}).get('pdf_output_dir', 'strategies')
            filename = save_strategy_as_pdf(args.query, strategy, output_dir)
            print(f"\nStrategy saved as PDF: {filename}")
    elif config.get('example_queries'):
        # Use default query from configuration
        query = config['example_queries'][0]

        # Generate the strategy
        strategy = strategist.create_strategy(query)

        # Print the strategy
        print(f"\nMarketing Strategy for '{query}':\n")
        print(strategy)

        # Save the strategy as a PDF
        output_dir = config.get('output', {}).get('pdf_output_dir', 'strategies')
        filename = save_strategy_as_pdf(query, strategy, output_dir)
        print(f"\nStrategy saved as PDF: {filename}")


if __name__ == "__main__":
    main()