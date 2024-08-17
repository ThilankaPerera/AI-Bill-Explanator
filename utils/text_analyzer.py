import re
from typing import Dict, List, Tuple
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextAnalyzer:
    """Analyze bill text to extract charges, categories, and insights"""
    
    def __init__(self):
        self.charge_keywords = {
            'fixed_charges': ['fixed charge', 'rental', 'basic charge', 'standing charge'],
            'usage_charges': ['usage', 'consumption', 'units', 'kwh', 'mb', 'gb'],
            'taxes': ['vat', 'tax', 'levy', 'nbt', 'cess'],
            'additional_charges': ['surcharge', 'penalty', 'late fee', 'reconnection', 'interest'],
            'discounts': ['discount', 'concession', 'rebate', 'waiver']
        }
    
    