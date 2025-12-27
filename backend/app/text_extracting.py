import pdfplumber
from docx import Document


def extract_text(file, filename):
    """Extract text from uploaded files based on file extension."""

    filename = filename.lower()

    if filename.endswith(".pdf"):
        text = extract_pdf(file)

    elif filename.endswith(".docx"):
        text = extract_docx(file)

    elif filename.endswith(".txt"):
        text = extract_txt(file)

    else:
        raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")

    if not text or not text.strip():
        raise ValueError("No readable text found in file.")

    return text


def extract_pdf(file):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_docx(file):
    """Extract text from a DOCX file."""
    doc = Document(file)
    return "\n".join(para.text for para in doc.paragraphs if para.text)


def extract_txt(file):
    """Extract text from a TXT file."""
    file.seek(0)
    return file.read().decode("utf-8", errors="ignore")
