# 💰 BillBuster - AI Bill Explainer for Sri Lanka

An AI-powered application that helps Sri Lankan citizens understand their utility bills by breaking down complex charges, explaining jargon, and detecting anomalies.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

- **📄 PDF Processing**: Extracts text from PDF bills using OCR and text parsing
- **🤖 AI Explanations**: Uses Mistral-7B open-source LLM to explain bills in plain English
- **📊 Visual Breakdowns**: Interactive charts showing charge distributions
- **🔍 Anomaly Detection**: Identifies unusual charges, penalties, and billing errors
- **💡 Smart Insights**: Provides money-saving tips and usage recommendations
- **🇱🇰 Sri Lanka Focused**: Tailored for CEB, LECO, Dialog, Mobitel, SLT, and other local providers

## 🚀 Supported Bill Types

- ⚡ **Electricity**: CEB, LECO
- 💧 **Water**: National Water Supply & Drainage Board
- 📱 **Telecom**: Dialog, Mobitel, Hutch, Airtel, SLT
- 🏥 **Hospital**: Medical and healthcare bills

## 📋 Prerequisites

- Python 3.8 or higher
- 4GB+ RAM (8GB recommended for LLM)
- GPU (optional, but recommended for faster AI processing)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/billbuster.git
cd billbuster
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Add to PATH

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

## 🎯 Usage

### Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using BillBuster

1. **Upload Bill**: Click "Choose a PDF file" in the sidebar
2. **View Overview**: See key metrics and charge breakdown
3. **Get AI Explanation**: Click "Generate AI Explanation" for plain English summary
4. **Explore Visuals**: Check interactive charts and graphs
5. **Review Alerts**: See detected anomalies and money-saving tips

## 📁 Project Structure
```
billbuster/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore rules
├── utils/               # Utility modules
│   ├── __init__.py
│   ├── pdf_parser.py    # PDF extraction logic
│   ├── text_analyzer.py # Charge analysis
│   └── visualization.py # Chart creation
├── models/              # AI model handling
│   ├── __init__.py
│   └── llm_handler.py   # LLM integration
└── data/               # Data directory
    └── uploaded_bills/  # Temporary file storage
```

## 🔧 Configuration

Edit `config.py` to customize:

- **LLM Model**: Change `LLM_MODEL` to use different models
- **Bill Types**: Add more utility providers
- **Taxes**: Update tax rates (VAT, NBT)
- **Thresholds**: Adjust anomaly detection sensitivity

## 🤖 AI Model

BillBuster uses **Mistral-7B-Instruct-v0.2**, a powerful open-source LLM:

- **Model**: mistralai/Mistral-7B-Instruct-v0.2
- **Size**: ~7 billion parameters
- **License**: Apache 2.0
- **Performance**: Excellent instruction following

### Using Different Models

You can swap to other open-source models by editing `config.py`:
```python
LLM_MODEL = "meta-llama/Llama-2-7b-chat-hf"  # Llama 2
LLM_MODEL = "tiiuae/falcon-7b-instruct"       # Falcon
```

## 📊 Features in Detail

### PDF Parsing
- Extracts text from native PDFs
- OCR for scanned documents
- Table extraction for structured data
- Handles multi-page bills

### Charge Analysis
- Categorizes charges automatically
- Identifies fixed vs. usage-based charges
- Separates taxes and additional fees
- Calculates percentages and totals

### Anomaly Detection
- Compares against historical averages
- Flags unusually high bills
- Detects penalty charges
- Validates tax percentages

### Visualizations
- Pie charts for distribution
- Bar charts for comparison
- Interactive tables
- Trend analysis (with historical data)

## 🐛 Troubleshooting

### Model Loading Issues

If the AI model fails to load:
```python
# The app will automatically fall back to rule-based explanations
# No action needed - functionality continues without AI
```

### OCR Not Working

Ensure Tesseract is installed and in PATH:
```bash
# Test Tesseract
tesseract --version
```

### Memory Issues

For low-RAM systems, use a smaller model:
```python
# In config.py
LLM_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **Mistral AI** for the open-source LLM
- **Streamlit** for the amazing framework
- **pdfplumber** for PDF processing
- **Tesseract** for OCR capabilities

## 📧 Contact

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: support@billbuster.lk (example)

## 🗺️ Roadmap

- [ ] Historical bill tracking
- [ ] Email bill import
- [ ] Multi-language support (Sinhala, Tamil)
- [ ] Mobile app version
- [ ] Bill payment reminders
- [ ] Usage prediction
- [ ] Budget recommendations

---

**Made with ❤️ for Sri Lanka 🇱🇰**

*Helping citizens understand their bills, one PDF at a time.*
```