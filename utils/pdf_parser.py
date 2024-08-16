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
    
    def _ocr_page(self, page) -> str:
        """Perform OCR on a page image"""
        try:
            # Convert page to image
            img = page.to_image(resolution=300)
            pil_img = img.original
            
            # Perform OCR
            text = pytesseract.image_to_string(pil_img)
            return text
        except Exception as e:
            logger.error(f"OCR failed: {str(e)}")
            return ""
    
    def _extract_structured_data(self) -> Dict:
        """Extract structured data like amounts, dates, account numbers"""
        data = {
            'amounts': [],
            'dates': [],
            'account_numbers': [],
            'bill_type': None
        }
        
        # Extract amounts (LKR)
        amount_patterns = [
            r'(?:Rs\.?|LKR)\s*([0-9,]+\.?\d*)',
            r'([0-9,]+\.?\d*)\s*(?:Rs\.?|LKR)',
            r':\s*([0-9,]+\.?\d*)\s*$'
        ]
        
        for pattern in amount_patterns:
            matches = re.findall(pattern, self.text_content, re.MULTILINE)
            for match in matches:
                try:
                    amount = float(match.replace(',', ''))
                    data['amounts'].append(amount)
                except:
                    pass
        
        # Extract dates
        date_patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, self.text_content)
            data['dates'].extend(matches)
        
        # Extract account/reference numbers
        account_patterns = [
            r'Account\s*(?:No\.?|Number)?\s*:?\s*([A-Z0-9-]+)',
            r'Reference\s*(?:No\.?|Number)?\s*:?\s*([A-Z0-9-]+)',
            r'Bill\s*(?:No\.?|Number)?\s*:?\s*([A-Z0-9-]+)'
        ]
        
        for pattern in account_patterns:
            matches = re.findall(pattern, self.text_content, re.IGNORECASE)
            data['account_numbers'].extend(matches)
        
        # Detect bill type
        from config import BILL_TYPES
        text_lower = self.text_content.lower()
        
        for bill_type, keywords in BILL_TYPES.items():
            if any(keyword.lower() in text_lower for keyword in keywords):
                data['bill_type'] = bill_type
                break
        
        return data