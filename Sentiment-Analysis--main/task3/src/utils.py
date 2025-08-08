#!/usr/bin/env python3
"""
Sentiment Analysis Tool - Main Application
Complete sentiment analysis solution with CLI interface
"""

import os
import sys
from typing import List, Dict, Any
import pandas as pd

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import project modules
try:
    from src.config import Config
    from src.utils import load_data, save_results, create_sample_data, display_results, get_statistics, print_statistics, validate_text_input
    from src.preprocessing import TextPreprocessor
    from src.analyzer import SentimentAnalyzer
except ImportError as e:
    print(f"❌ Import Error: {str(e)}")
    print("Make sure all files are in the correct src/ folder")
    sys.exit(1)

class SentimentAnalysisApp:
    """Main application class for sentiment analysis"""
    
    def __init__(self):
        """Initialize the application"""
        self.config = Config()
        self.preprocessor = TextPreprocessor()
        self.analyzer = SentimentAnalyzer()
        
    def analyze_single_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a single text
        
        Args:
            text (str): Input text
            
        Returns:
            Dict: Analysis result
        """
        if not validate_text_input(text):
            return {'error': 'Invalid text input'}
        
        # Preprocess text
        cleaned_text = self.preprocessor.clean_text(text)
        
        # Analyze sentiment
        result = self.analyzer.analyze_sentiment(cleaned_text)
        result['original_text'] = text
        result['cleaned_text'] = cleaned_text
        
        return result
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment of multiple texts
        
        Args:
            texts (List[str]): List of input texts
            
        Returns:
            List[Dict]: Analysis results
        """
        results = []
        
        print(f"🔄 Analyzing {len(texts)} texts...")
        
        for i, text in enumerate(texts, 1):
            print(f"Processing {i}/{len(texts)}", end='\r')
            result = self.analyze_single_text(text)
            results.append(result)
        
        print(f"\n✅ Analysis complete!")
        return results
    
    def analyze_csv_file(self, file_path: str, text_column: str = 'text') -> List[Dict[str, Any]]:
        """
        Analyze sentiment from CSV file
        
        Args:
            file_path (str): Path to CSV file
            text_column (str): Column name containing text
            
        Returns:
            List[Dict]: Analysis results
        """
        # Load data
        df = load_data(file_path)
        
        if df.empty:
            print("❌ No data loaded")
            return []
        
        # Check if text column exists
        if text_column not in df.columns:
            print(f"❌ Column '{text_column}' not found in CSV")
            print(f"Available columns: {list(df.columns)}")
            return []
        
        # Extract texts
        texts = df[text_column].astype(str).tolist()
        
        # Analyze
        results = self.analyze_batch(texts)
        
        return results
    
    def run_interactive_mode(self):
        """Run interactive CLI mode"""
        print("🚀 SENTIMENT ANALYSIS TOOL")
        print("=" * 40)
        
        while True:
            print("\nChoose an option:")
            print("1. Analyze single text")
            print("2. Analyze CSV file")
            print("3. Test with sample data")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                self.handle_single_text()
            elif choice == '2':
                self.handle_csv_file()
            elif choice == '3':
                self.handle_sample_data()
            elif choice == '4':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
    
    def handle_single_text(self):
        """Handle single text analysis"""
        print("\n📝 SINGLE TEXT ANALYSIS")
        print("-" * 30)
        
        text = input("Enter text to analyze: ").strip()
        
        if not text:
            print("❌ Empty text entered")
            return
        
        print(f"\n🔄 Analyzing text...")
        result = self.analyze_single_text(text)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        # Display result
        print(f"\n✅ ANALYSIS RESULT:")
        print(f"Original Text: {result.get('original_text', '')}")
        print(f"Sentiment: {result.get('sentiment', 'Unknown')}")
        print(f"Confidence: {result.get('confidence', 0):.2f}")
        
        if 'scores' in result:
            scores = result['scores']
            print(f"Detailed Scores:")
            for key, value in scores.items():
                print(f"  {key}: {value:.3f}")
    
    def handle_csv_file(self):
        """Handle CSV file analysis"""
        print("\n📊 CSV FILE ANALYSIS")
        print("-" * 25)
        
        file_path = input("Enter CSV file path: ").strip()
        
        if not file_path:
            print("❌ No file path entered")
            return
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        text_column = input("Enter text column name (default: 'text'): ").strip()
        if not text_column:
            text_column = 'text'
        
        # Analyze
        results = self.analyze_csv_file(file_path, text_column)
        
        if not results:
            return
        
        # Display results
        display_results(results)
        
        # Show statistics
        stats = get_statistics(results)
        print_statistics(stats)
        
        # Ask to save results
        save_choice = input("\nSave results to CSV? (y/n): ").strip().lower()
        if save_choice == 'y':
            output_path = input("Enter output file path (default: 'results.csv'): ").strip()
            if not output_path:
                output_path = 'results.csv'
            
            save_results(results, output_path)
    
    def handle_sample_data(self):
        """Handle sample data testing"""
        print("\n🧪 SAMPLE DATA TESTING")
        print("-" * 25)
        
        # Create sample data
        sample_df = create_sample_data()
        texts = sample_df['text'].tolist()
        
        print(f"Testing with {len(texts)} sample texts...")
        
        # Analyze
        results = self.analyze_batch(texts)
        
        # Display results
        display_results(results)
        
        # Show statistics
        stats = get_statistics(results)
        print_statistics(stats)

def main():
    """Main function"""
    try:
        app = SentimentAnalysisApp()
        app.run_interactive_mode()
    
    except KeyboardInterrupt:
        print("\n\n👋 Exited by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()