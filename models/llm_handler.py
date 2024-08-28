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
            
            
            
            self.llm = HuggingFacePipeline(pipeline=pipe)
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            logger.info("Falling back to simplified mode...")
            self.llm = None
    
   