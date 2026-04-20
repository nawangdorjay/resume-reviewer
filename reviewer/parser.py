"""
Resume Parser — Extract text from PDF, DOCX, or plain text files.
"""

from pathlib import Path


def parse_resume(file_path: Path) -> str:
    """Extract text from a resume file. Supports PDF, DOCX, and TXT."""
    
    suffix = file_path.suffix.lower()
    
    if suffix == ".pdf":
        return _parse_pdf(file_path)
    elif suffix in (".docx", ".doc"):
        return _parse_docx(file_path)
    elif suffix == ".txt":
        return _parse_txt(file_path)
    else:
        # Try reading as plain text
        return _parse_txt(file_path)


def _parse_pdf(file_path: Path) -> str:
    """Extract text from PDF using pdfplumber."""
    try:
        import pdfplumber
        
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        return "\n".join(text_parts)
    except ImportError:
        raise ImportError(
            "pdfplumber is required for PDF parsing. "
            "Install it with: pip install pdfplumber"
        )


def _parse_docx(file_path: Path) -> str:
    """Extract text from DOCX using python-docx."""
    try:
        from docx import Document
        
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)
    except ImportError:
        raise ImportError(
            "python-docx is required for DOCX parsing. "
            "Install it with: pip install python-docx"
        )


def _parse_txt(file_path: Path) -> str:
    """Read plain text file."""
    return file_path.read_text(encoding="utf-8", errors="replace")
