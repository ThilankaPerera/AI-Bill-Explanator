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
    
    