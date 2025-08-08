# Sentiment Analysis Project

## Overview
This project analyzes text data to determine sentiment (positive, negative, neutral), helping businesses assess customer feedback and make informed decisions.

## Features
- Text preprocessing and cleaning
- Multiple sentiment analysis approaches
- VADER sentiment analysis
- TextBlob sentiment analysis
- Sample data analysis
- Interactive text input analysis

## Project Structure
```
sentiment_analysis/
├── data/                    # Data storage (created automatically)
├── src/                     # Source code modules
│   ├── __init__.py         # Package initialization
│   ├── config.py           # Configuration settings
│   ├── preprocessing.py    # Text preprocessing functions
│   ├── analyzer.py         # Core sentiment analysis
│   └── utils.py           # Utility functions
├── requirements.txt        # Python dependencies
├── main.py                # Main execution script
└── README.md              # This file
```

## Installation
1. Navigate to project directory:
```bash
cd "C:\path\to\your\sentiment_analysis"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the main script:
```bash
python main.py
```

Choose from:
- Option 1: Analyze sample data
- Option 2: Enter custom text for analysis

## Dependencies
- pandas: Data manipulation
- numpy: Numerical operations
- textblob: Text processing and sentiment analysis
- vaderSentiment: VADER sentiment analyzer
- scikit-learn: Machine learning utilities
- nltk: Natural language processing
- matplotlib & seaborn: Data visualization
- tqdm: Progress bars

## Output
The system provides:
- Sentiment classification (Positive/Negative/Neutral)
- Confidence scores
- Visual analysis charts
- Detailed sentiment breakdown

## Requirements Met
✅ Analyzes text data for sentiment classification
✅ Helps businesses assess customer feedback
✅ Simple, optimal, and modularized code structure
✅ Includes only necessary components