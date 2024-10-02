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
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Upload Your Bill")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload your utility bill in PDF format"
        )
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.markdown("""
        **BillBuster** helps Sri Lankan citizens understand their bills by:
        - Extracting text from PDF bills (even scanned ones)
        - Breaking down charges into categories
        - Explaining jargon in simple terms
        - Detecting anomalies and overcharges
        
        **Supported Bill Types:**
        - Electricity (CEB, LECO)
        - Water (NWSDB)
        - Telecom (Dialog, Mobitel, SLT, etc.)
        - Hospital/Medical bills
        """)
        
        st.markdown("---")
        st.markdown("**Built with:**")
        st.markdown("🤖 Mistral-7B AI Model")
        st.markdown("📄 PDF Processing")
        st.markdown("📊 Interactive Visualizations")
    
    # Main content
    if uploaded_file is not None:
        process_bill(uploaded_file)
    else:
        show_demo_info()


def show_demo_info():
    """Show information when no file is uploaded"""
    st.info("👆 Upload a bill PDF to get started!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 Clear Breakdowns
        See exactly where your money goes with visual charts and detailed tables.
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 AI Explanations
        Get plain English explanations of complex billing terms and charges.
        """)
    
    with col3:
        st.markdown("""
        ### 🔍 Anomaly Detection
        Automatically detect unusual charges, penalties, or billing errors.
        """)
    
    st.markdown("---")
    st.subheader("💡 How It Works")
    
    steps_col1, steps_col2, steps_col3, steps_col4 = st.columns(4)
    
    with steps_col1:
        st.markdown("#### 1️⃣ Upload")
        st.markdown("Upload your bill PDF")
    
    with steps_col2:
        st.markdown("#### 2️⃣ Extract")
        st.markdown("AI extracts text & data")
    
    with steps_col3:
        st.markdown("#### 3️⃣ Analyze")
        st.markdown("Categorize & analyze charges")
    
    with steps_col4:
        st.markdown("#### 4️⃣ Explain")
        st.markdown("Get clear explanations")


def process_bill(uploaded_file):
    """Process uploaded bill file"""
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🤖 AI Explanation", 
        "📈 Visualizations", 
        "⚠️ Alerts & Insights"
    ])
    
    # Parse PDF
    if st.session_state.parsed_data is None:
        with st.spinner("📄 Extracting text from PDF..."):
            try:
                parser = PDFParser()
                st.session_state.parsed_data = parser.parse_pdf(uploaded_file)
                st.success("✅ PDF parsed successfully!")
            except Exception as e:
                st.error(f"❌ Error parsing PDF: {str(e)}")
                return
    
    parsed_data = st.session_state.parsed_data
    
    # Analyze charges
    if st.session_state.analyzed_data is None:
        with st.spinner("🔍 Analyzing charges..."):
            try:
                analyzer = TextAnalyzer()
                charges = analyzer.analyze_charges(
                    parsed_data['text'],
                    parsed_data['structured_data']
                )
                anomalies = analyzer.detect_anomalies(charges)
                insights = analyzer.generate_insights(
                    charges,
                    parsed_data['structured_data'].get('bill_type')
                )
                
                st.session_state.analyzed_data = {
                    'charges': charges,
                    'anomalies': anomalies,
                    'insights': insights
                }
                st.success("✅ Analysis complete!")
            except Exception as e:
                st.error(f"❌ Error analyzing bill: {str(e)}")
                return
    
    analyzed_data = st.session_state.analyzed_data
    charges = analyzed_data['charges']
    anomalies = analyzed_data['anomalies']
    insights = analyzed_data['insights']
    
    # TAB 1: Overview
    with tab1:
        show_overview(parsed_data, charges)
    
    # TAB 2: AI Explanation
    with tab2:
        show_ai_explanation(parsed_data, charges)
    
    # TAB 3: Visualizations
    with tab3:
        show_visualizations(charges)
    
    # TAB 4: Alerts & Insights
    with tab4:
        show_alerts_insights(anomalies, insights)


def show_overview(parsed_data, charges):
    """Display overview tab content"""
    st.header("📊 Bill Overview")
    
    