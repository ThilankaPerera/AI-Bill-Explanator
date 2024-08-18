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
    
    def analyze_charges(self, text: str, structured_data: Dict) -> Dict:
        """
        Analyze and categorize charges from bill text
        
        Args:
            text: Extracted bill text
            structured_data: Structured data from PDF parser
            
        Returns:
            Dictionary with categorized charges
        """
        charges = {
            'total_amount': 0,
            'categories': defaultdict(list),
            'line_items': [],
            'taxes': [],
            'summary': {}
        }
        
        # Extract line items with amounts
        lines = text.split('\n')
        for line in lines:
            # Look for patterns like "Description ... Amount"
            amount_match = re.search(r'([0-9,]+\.?\d*)\s*$', line.strip())
            if amount_match:
                amount = float(amount_match.group(1).replace(',', ''))
                description = line[:amount_match.start()].strip()
                
                if description and len(description) > 3:
                    item = {
                        'description': description,
                        'amount': amount,
                        'category': self._categorize_charge(description)
                    }
                    charges['line_items'].append(item)
                    charges['categories'][item['category']].append(item)
        
        