#!/usr/bin/env python3
"""
Sentiment Analysis Tool - Simple Working Version
"""

import os
import sys
import pandas as pd
from typing import List, Dict, Any

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def analyze_single_text(text: str) -> Dict[str, Any]:
    """Analyze sentiment of a single text"""
    try:
        from textblob import TextBlob
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        
        # TextBlob analysis
        blob = TextBlob(text)
        tb_polarity = blob.sentiment.polarity
        
        # VADER analysis
        vader = SentimentIntensityAnalyzer()
        vader_scores = vader.polarity_scores(text)
        vader_compound = vader_scores['compound']
        
        # Determine sentiment
        if tb_polarity > 0.1 and vader_compound > 0.05:
            sentiment = "Positive"
            confidence = (abs(tb_polarity) + abs(vader_compound)) / 2
        elif tb_polarity < -0.1 and vader_compound < -0.05:
            sentiment = "Negative"
            confidence = (abs(tb_polarity) + abs(vader_compound)) / 2
        else:
            sentiment = "Neutral"
            confidence = 1 - abs(tb_polarity + vader_compound) / 2
        
        return {
            'text': text,
            'sentiment': sentiment,
            'confidence': round(confidence, 3),
            'textblob_score': round(tb_polarity, 3),
            'vader_score': round(vader_compound, 3)
        }
    
    except ImportError as e:
        return {'error': f'Missing package: {str(e)}'}
    except Exception as e:
        return {'error': f'Analysis error: {str(e)}'}

def create_sample_data():
    """Create sample data for testing"""
    sample_texts = [
        "I love this product! It's amazing!",
        "This is the worst service ever. Terrible experience.",
        "The weather is okay today.",
        "I'm so excited about the new update!",
        "Not sure how I feel about this.",
        "Absolutely fantastic work!",
        "I hate waiting in long queues.",
        "The movie was decent, nothing special.",
        "Best purchase I've made this year!",
        "Customer service was disappointing."
    ]
    return sample_texts

def analyze_csv_file(file_path: str, text_column: str = 'text'):
    """Analyze sentiment from CSV file"""
    try:
        # Load CSV file
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return []
        
        df = pd.read_csv(file_path)
        print(f"✅ Loaded {len(df)} rows from CSV")
        
        # Check if column exists
        if text_column not in df.columns:
            print(f"❌ Column '{text_column}' not found")
            print(f"Available columns: {list(df.columns)}")
            return []
        
        # Analyze each text
        results = []
        texts = df[text_column].astype(str).tolist()
        
        print(f"🔄 Analyzing {len(texts)} texts...")
        for i, text in enumerate(texts, 1):
            result = analyze_single_text(text)
            results.append(result)
            print(f"Progress: {i}/{len(texts)}", end='\r')
        
        print(f"\n✅ Analysis complete!")
        return results
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []

def display_results(results):
    """Display analysis results"""
    if not results:
        print("No results to display")
        return
    
    print("\n" + "="*80)
    print("SENTIMENT ANALYSIS RESULTS")
    print("="*80)
    
    for i, result in enumerate(results, 1):
        if 'error' in result:
            print(f"{i:2d}. ERROR: {result['error']}")
            continue
        
        text = result['text'][:60] + '...' if len(result['text']) > 60 else result['text']
        sentiment = result['sentiment']
        confidence = result['confidence']
        
        print(f"{i:2d}. Text: {text}")
        print(f"    Sentiment: {sentiment} (Confidence: {confidence})")
        print("-" * 80)

def show_statistics(results):
    """Show statistics"""
    if not results:
        return
    
    # Count sentiments
    sentiments = [r.get('sentiment', 'Unknown') for r in results if 'error' not in r]
    if not sentiments:
        return
    
    positive = sentiments.count('Positive')
    negative = sentiments.count('Negative')
    neutral = sentiments.count('Neutral')
    total = len(sentiments)
    
    print("\n" + "="*50)
    print("STATISTICS")
    print("="*50)
    print(f"Total Texts: {total}")
    print(f"Positive: {positive} ({positive/total*100:.1f}%)")
    print(f"Negative: {negative} ({negative/total*100:.1f}%)")
    print(f"Neutral: {neutral} ({neutral/total*100:.1f}%)")
    print("="*50)

def save_results_to_csv(results, output_file='results.csv'):
    """Save results to CSV"""
    try:
        # Filter out errors
        clean_results = [r for r in results if 'error' not in r]
        if not clean_results:
            print("❌ No valid results to save")
            return False
        
        df = pd.DataFrame(clean_results)
        df.to_csv(output_file, index=False)
        print(f"✅ Results saved to: {output_file}")
        return True
    
    except Exception as e:
        print(f"❌ Error saving results: {str(e)}")
        return False

def main():
    """Main function"""
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
            # Single text analysis
            print("\n📝 SINGLE TEXT ANALYSIS")
            print("-" * 30)
            
            text = input("Enter text to analyze: ").strip()
            if not text:
                print("❌ Empty text entered")
                continue
            
            print(f"\n🔄 Analyzing...")
            result = analyze_single_text(text)
            
            if 'error' in result:
                print(f"❌ {result['error']}")
                continue
            
            print(f"\n✅ RESULT:")
            print(f"Text: {result['text']}")
            print(f"Sentiment: {result['sentiment']}")
            print(f"Confidence: {result['confidence']}")
            print(f"TextBlob Score: {result['textblob_score']}")
            print(f"VADER Score: {result['vader_score']}")
        
        elif choice == '2':
            # CSV file analysis
            print("\n📊 CSV FILE ANALYSIS")
            print("-" * 25)
            
            file_path = input("Enter CSV file path: ").strip()
            if not file_path:
                print("❌ No file path entered")
                continue
            
            text_column = input("Enter text column name (default: 'text'): ").strip()
            if not text_column:
                text_column = 'text'
            
            results = analyze_csv_file(file_path, text_column)
            if results:
                display_results(results)
                show_statistics(results)
                
                save_choice = input("\nSave results to CSV? (y/n): ").strip().lower()
                if save_choice == 'y':
                    output_file = input("Enter output filename (default: 'results.csv'): ").strip()
                    if not output_file:
                        output_file = 'results.csv'
                    save_results_to_csv(results, output_file)
        
        elif choice == '3':
            # Sample data testing
            print("\n🧪 SAMPLE DATA TESTING")
            print("-" * 25)
            
            sample_texts = create_sample_data()
            print(f"Testing with {len(sample_texts)} sample texts...")
            
            results = []
            for text in sample_texts:
                result = analyze_single_text(text)
                results.append(result)
            
            display_results(results)
            show_statistics(results)
        
        elif choice == '4':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exited by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()