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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .insight-box {
        background-color: #E8F4F8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1rem 0;
    }
    .anomaly-warning {
        background-color: #FFF3CD;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FFC107;
        margin: 1rem 0;
    }
    .anomaly-alert {
        background-color: #F8D7DA;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #DC3545;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'parsed_data' not in st.session_state:
        st.session_state.parsed_data = None
    if 'analyzed_data' not in st.session_state:
        st.session_state.analyzed_data = None
    if 'llm_handler' not in st.session_state:
        st.session_state.llm_handler = None


def load_llm():
    """Load LLM model with caching"""
    if st.session_state.llm_handler is None:
        with st.spinner("Loading AI model... This may take a minute on first run."):
            st.session_state.llm_handler = LLMHandler()
    return st.session_state.llm_handler


def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">💰 BillBuster</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">AI-Powered Bill Explainer for Sri Lanka 🇱🇰</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("""
    Upload your electricity, water, hospital, or telecom bill and get:
    - 📊 Clear breakdown of all charges
    - 🤖 AI explanation in plain English
    - 🔍 Detection of unusual charges
    - 💡 Money-saving tips
    """)
    
    


