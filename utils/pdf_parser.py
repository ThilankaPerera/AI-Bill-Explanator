import pdfplumber
import pytesseract
from PIL import Image
import io
import re
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFParser:
    """Parse PDF bills and extract text content"""
    
    def __init__(self):
        self.text_content = ""
        self.tables = []
        self.metadata = {}
    
    def parse_pdf(self, pdf_file) -> Dict:
        """
        Parse PDF file and extract text and tables
        
        Args:
            pdf_file: Uploaded PDF file object
            
        Returns:
            Dictionary with extracted text, tables, and metadata
        """
        try:
            with pdfplumber.open(pdf_file) as pdf:
                # Extract metadata
                self.metadata = {
                    'num_pages': len(pdf.pages),
                    'metadata': pdf.metadata
                }
                
                all_text = []
                all_tables = []
                
                