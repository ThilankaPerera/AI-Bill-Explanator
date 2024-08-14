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
                
                # Process each page
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    text = page.extract_text()
                    if text:
                        all_text.append(text)
                    else:
                        # If no text, try OCR
                        logger.info(f"No text found on page {page_num}, attempting OCR...")
                        text = self._ocr_page(page)
                        if text:
                            all_text.append(text)
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        all_tables.extend(tables)
                
                self.text_content = "\n\n".join(all_text)
                self.tables = all_tables
                
                # Extract structured data
                structured_data = self._extract_structured_data()
                
                return {
                    'text': self.text_content,
                    'tables': self.tables,
                    'metadata': self.metadata,
                    'structured_data': structured_data
                }
                
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise
    
    