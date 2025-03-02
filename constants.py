"""
Constants for the RAG Marketing Strategist System.
"""

# File paths
WORKING_DIRECTORY = "."
NLTK_DATA_DIR = f"{WORKING_DIRECTORY}/nltk_data"
DEFAULT_PDF_PATH = "./Marketing_Strategies.pdf"

# NLTK downloads
NLTK_DOWNLOADS = ["punkt_tab"]

# Cache settings
STRATEGY_CACHE_SIZE = 32

# PDF settings
PDF_FONT = "Arial"
PDF_TITLE_SIZE = 12
PDF_BODY_SIZE = 12

# Section titles for generated PDFs
STRATEGY_SECTIONS = [
    "Campaign Objectives",
    "Target Audience Analysis",
    "Channel Selection",
    "Content Strategy",
    "Budget Allocation",
    "Measurement and KPIs"
]