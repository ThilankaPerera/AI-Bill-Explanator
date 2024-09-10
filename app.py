import streamlit as st
import sys
from pathlib import Path
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import PDFParser, TextAnalyzer, Visualizer
from models import LLMHandler
from config import UPLOAD_DIR, CURRENCY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="BillBuster - AI Bill Explainer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

