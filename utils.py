"""
Utility functions for the RAG Marketing Strategist System.
"""

import os
import nltk
import PyPDF2
from fpdf import FPDF
from constants import NLTK_DATA_DIR, PDF_FONT, PDF_TITLE_SIZE, PDF_BODY_SIZE


def setup_nltk():
    """
    Set up NLTK data directory and download necessary datasets
    """
    # Create NLTK data directory if it doesn't exist
    if not os.path.exists(NLTK_DATA_DIR):
        os.makedirs(NLTK_DATA_DIR)

    # Add this directory to the nltk data path
    nltk.data.path.append(NLTK_DATA_DIR)

    # Download 'punkt' to the specified path
    nltk.download('punkt_tab', download_dir=NLTK_DATA_DIR)

    print(f"NLTK setup complete in {NLTK_DATA_DIR}")


def extract_text_from_pdf(pdf_file_path):
    """
    Extract text from a PDF file

    Args:
        pdf_file_path (str): Path to the PDF file

    Returns:
        str or None: Extracted text or None if extraction fails
    """
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return None


def save_strategy_as_pdf(input_description, strategy, output_dir='strategies'):
    """
    Save a generated marketing strategy as a PDF file

    Args:
        input_description (str): Description of the marketing campaign
        strategy (str): Generated marketing strategy text
        output_dir (str): Directory to save the PDF file

    Returns:
        str: Path to the saved PDF file
    """
    # Create PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(PDF_FONT, size=PDF_TITLE_SIZE)
    pdf.cell(200, 10, txt=f"Marketing Strategy for {input_description}", ln=1, align="C")
    pdf.set_font(PDF_FONT, size=PDF_BODY_SIZE)
    pdf.multi_cell(0, 10, txt=strategy)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save PDF file
    filename = f"{output_dir}/strategy_{input_description.replace(' ', '_')[:50]}.pdf"
    pdf.output(filename)
    return filename