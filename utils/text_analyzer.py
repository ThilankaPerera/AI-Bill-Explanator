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
        
        # Calculate totals per category
        for category, items in charges['categories'].items():
            charges['summary'][category] = sum(item['amount'] for item in items)
        
        # Find total amount
        total_patterns = [
            r'(?:total|amount\s+due|payable)\s*:?\s*(?:Rs\.?|LKR)?\s*([0-9,]+\.?\d*)',
            r'(?:Rs\.?|LKR)?\s*([0-9,]+\.?\d*)\s*(?:total|amount\s+due|payable)'
        ]
        
        for pattern in total_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                charges['total_amount'] = float(match.group(1).replace(',', ''))
                break
        
        # If total not found, sum all amounts
        if charges['total_amount'] == 0 and structured_data.get('amounts'):
            charges['total_amount'] = max(structured_data['amounts'])
        
        return charges
    
    def _categorize_charge(self, description: str) -> str:
        """Categorize a charge based on its description"""
        desc_lower = description.lower()
        
        for category, keywords in self.charge_keywords.items():
            if any(keyword in desc_lower for keyword in keywords):
                return category.replace('_', ' ').title()
        
        return 'Other Charges'
    
    def detect_anomalies(self, current_charges: Dict, 
                        historical_data: List[Dict] = None) -> List[Dict]:
        """
        Detect unusual charges or patterns
        
        Args:
            current_charges: Current bill charges
            historical_data: Previous bills data (if available)
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        # Check for unusually high amounts
        if current_charges.get('total_amount', 0) > 50000:  # LKR
            anomalies.append({
                'type': 'high_total',
                'severity': 'warning',
                'message': f"Bill amount (Rs. {current_charges['total_amount']:,.2f}) is unusually high",
                'suggestion': 'Please verify your consumption and check for any penalties or arrears'
            })
        
        # Check for penalty charges
        for item in current_charges.get('line_items', []):
            if any(word in item['description'].lower() 
                   for word in ['penalty', 'late fee', 'interest', 'arrears']):
                anomalies.append({
                    'type': 'penalty_charge',
                    'severity': 'alert',
                    'message': f"Penalty charge detected: {item['description']} - Rs. {item['amount']:,.2f}",
                    'suggestion': 'Consider paying bills on time to avoid penalty charges'
                })
        
        # Check VAT percentage (should be 15% in Sri Lanka)
        taxes = current_charges.get('summary', {}).get('Taxes', 0)
        if taxes > 0:
            other_charges = current_charges.get('total_amount', 0) - taxes
            if other_charges > 0:
                vat_percentage = (taxes / other_charges) * 100
                if vat_percentage > 18 or vat_percentage < 12:
                    anomalies.append({
                        'type': 'unusual_tax',
                        'severity': 'info',
                        'message': f"Tax percentage ({vat_percentage:.1f}%) seems unusual",
                        'suggestion': 'Standard VAT in Sri Lanka is 15%'
                    })
        
        