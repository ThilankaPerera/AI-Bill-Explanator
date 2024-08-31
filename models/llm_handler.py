import os
from typing import Dict, List
import logging
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMHandler:
    """Handle LLM operations for bill explanation"""
    
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.model_name = model_name
        self.llm = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the LLM model"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {device}")
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            # Create pipeline
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=1000,
                temperature=0.3,
                top_p=0.95,
                repetition_penalty=1.15
            )
            
            self.llm = HuggingFacePipeline(pipeline=pipe)
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            logger.info("Falling back to simplified mode...")
            self.llm = None
    
    def explain_bill(self, bill_data: Dict) -> str:
        """
        Generate a plain English explanation of the bill
        
        Args:
            bill_data: Dictionary containing bill information
            
        Returns:
            Plain English explanation
        """
        if self.llm is None:
            return self._fallback_explanation(bill_data)
        
        try:
            prompt_template = """You are a helpful assistant explaining utility bills to people in Sri Lanka. 
Explain this bill in simple, clear language that anyone can understand.

Bill Information:
Bill Type: {bill_type}
Total Amount: Rs. {total_amount}
Charges Breakdown:
{charges_summary}

Line Items:
{line_items}

Provide a clear, friendly explanation in 3-4 paragraphs:
1. What this bill is for and the total amount
2. Break down the main charges in simple terms
3. Explain any taxes or additional fees
4. Give practical advice if relevant

Use simple Sinhala/English terms that Sri Lankan people understand. Be concise and helpful.

Explanation:"""

            # Prepare data
            charges_summary = "\n".join([
                f"- {category}: Rs. {amount:,.2f}"
                for category, amount in bill_data.get('charges', {}).get('summary', {}).items()
            ])
            
            line_items = "\n".join([
                f"- {item['description']}: Rs. {item['amount']:,.2f}"
                for item in bill_data.get('charges', {}).get('line_items', [])[:10]
            ])
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["bill_type", "total_amount", "charges_summary", "line_items"]
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            response = chain.run(
                bill_type=bill_data.get('structured_data', {}).get('bill_type', 'utility').title(),
                total_amount=f"{bill_data.get('charges', {}).get('total_amount', 0):,.2f}",
                charges_summary=charges_summary,
                line_items=line_items
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return self._fallback_explanation(bill_data)
    
    def _fallback_explanation(self, bill_data: Dict) -> str:
        """Generate explanation without LLM (fallback mode)"""
        bill_type = bill_data.get('structured_data', {}).get('bill_type', 'utility').title()
        total = bill_data.get('charges', {}).get('total_amount', 0)
        summary = bill_data.get('charges', {}).get('summary', {})
        
        explanation = f"""## Your {bill_type} Bill Explained

