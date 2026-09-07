"""
PDF generator utilities.
"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate


class PDFGenerator:
    """Base PDF generator."""

    def __init__(self, filename: str):
        self.filename = Path(filename)

    def document(self):
        return SimpleDocTemplate(
            str(self.filename),
            pagesize=A4,
        )