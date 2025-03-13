"""
Main entry point for the RAG Marketing Strategist System.

This system uses Retrieval-Augmented Generation (RAG) to create marketing campaign strategies.
It combines a vector database for storing and retrieving relevant marketing information
with a language model for generating comprehensive and effective strategies.
"""

import os
import streamlit as st
from config import load_config, load_environment_variables
from utils import setup_nltk, extract_text_from_pdf, save_strategy_as_pdf
from vector_db import VectorDatabase
from generator import GroqGenerator
from strategist import RAGMarketingStrategist


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
    st.set_page_config(page_title="Marketing Campaign Strategist", layout="wide")
    
    st.title("🎯 AI Marketing Campaign Strategist")
    st.markdown("""
    Generate comprehensive marketing strategies using AI. This tool combines marketing expertise 
    with advanced AI to create customized campaign strategies for your business.
    """)

    # Load environment variables and setup
    load_environment_variables()
    setup_nltk()
    
    # Load configuration
    config = load_config('settings.yaml')
    
    # Initialize the system
    vector_db, generator, strategist = initialize_system(config)
    
    # Sidebar for PDF upload
    with st.sidebar:
        st.header("📚 Knowledge Base")
        st.markdown("Upload marketing documents to enhance the AI's knowledge")
        
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        if uploaded_file:
            with st.spinner("Processing PDF..."):
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Add to vector database
                add_pdf_to_vector_db(vector_db, temp_path, config)
                os.remove(temp_path)  # Clean up
                st.success("PDF processed and added to knowledge base!")
    
    # Main content area
    st.header("💡 Generate Marketing Strategy")
    
    # Input for marketing campaign description
    campaign_description = st.text_area(
        "Describe your marketing campaign",
        placeholder="Example: a new eco-friendly water bottle targeting millennials with a budget of $50,000",
        height=100
    )
    
    # Generate button
    if st.button("Generate Strategy", type="primary"):
        if not campaign_description:
            st.warning("Please provide a campaign description")
        else:
            with st.spinner("Generating your marketing strategy..."):
                try:
                    strategy = strategist.create_strategy(campaign_description)
                    
                    # Display strategy
                    st.markdown("### 📊 Your Marketing Strategy")
                    st.markdown(strategy)
                    
                    # Save as PDF
                    output_dir = config.get('output', {}).get('pdf_output_dir', 'strategies')
                    filename = save_strategy_as_pdf(campaign_description, strategy, output_dir)
                    
                    # Provide download link
                    with open(filename, 'rb') as f:
                        st.download_button(
                            label="Download Strategy as PDF",
                            data=f,
                            file_name=os.path.basename(filename),
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"Error generating strategy: {str(e)}")


if __name__ == "__main__":
    main()