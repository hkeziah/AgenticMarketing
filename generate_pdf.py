from fpdf import FPDF


def generate_placeholder_text(section_title):
    """
    Generates placeholder text for a given marketing strategy section.

    Args:
        section_title (str): The title of the section.

    Returns:
        str: Placeholder text describing the section.
    """
    return (f"This section provides an overview of {section_title.lower()}. "
            f"It covers key concepts and best practices. "
            f"Understanding these principles is crucial for developing effective marketing strategies. "
            f"In the following paragraphs, we will explore various aspects of {section_title.lower()}, "
            f"including its importance, common challenges, and practical tips for implementation.\n\n"
            f"Additionally, we will discuss how {section_title.lower()} integrates with other components "
            f"of a marketing campaign. By the end of this section, you will have a solid foundation "
            f"to apply these concepts to your own marketing efforts.")


# List of marketing strategy sections
sections = [
    "Introduction to Marketing Strategies",
    "Defining Campaign Objectives",
    "Understanding Your Target Audience",
    "Selecting the Right Marketing Channels",
    "Crafting Engaging Content",
    "Budget Allocation for Maximum Impact",
    "Measuring Campaign Success with KPIs"
]

# Initialize FPDF object
pdf = FPDF()
pdf.add_page()

# Set font for the document title
pdf.set_font("Arial", size=16, style='B')
pdf.cell(200, 10, txt="Sample Marketing Strategies Document", ln=1, align="C")

# Set default font size for body text
pdf.set_font("Arial", size=12)

# Add each section with its placeholder text
for section in sections:
    # Section title (bold and slightly larger font)
    pdf.set_font("Arial", size=14, style='B')
    pdf.multi_cell(0, 10, txt=section)

    # Section content (normal font)
    pdf.set_font("Arial", size=12)
    text = generate_placeholder_text(section)
    pdf.multi_cell(0, 10, txt=text)

    # Add spacing after each section
    pdf.ln(10)

# Save the PDF to the current directory
pdf.output("Marketing_Strategies.pdf")

print("Sample 'Marketing_Strategies.pdf' has been generated successfully.")