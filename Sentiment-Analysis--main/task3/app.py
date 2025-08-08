import streamlit as st
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import re
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="Sentiment Analysis Tool",
    page_icon="📊",
    menu_items={}
)

# Hide Streamlit elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
div[data-testid="stToolbar"] {visibility: hidden;}
div[data-testid="stDecoration"] {visibility: hidden;}
div[data-testid="stStatusWidget"] {visibility: hidden;}
#MainMenu {visibility: hidden;}
.stActionButton {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Enhanced sentiment analysis class
class EnhancedSentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        # Context-aware phrases that are often misclassified
        self.negative_contexts = [
            r"could be better", r"needs improvement", r"not great", r"okay but",
            r"disappointed", r"expected more", r"falls short", r"lacks",
            r"missing", r"wish it was", r"hope for better", r"not satisfied"
        ]
        self.positive_contexts = [
            r"much better than", r"way better", r"so much better",
            r"absolutely amazing", r"highly recommend", r"love it",
            r"perfect", r"excellent", r"outstanding"
        ]
        
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        if pd.isna(text):
            return ""
        text = str(text).lower().strip()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def context_aware_adjustment(self, text, base_score):
        """Adjust sentiment based on context patterns"""
        text_lower = text.lower()
        
        # Check for negative contexts
        for pattern in self.negative_contexts:
            if re.search(pattern, text_lower):
                # Adjust score to be more negative
                if base_score > 0:
                    return max(-0.1, base_score - 0.6)  # Make positive scores negative
                else:
                    return min(-0.5, base_score - 0.2)  # Make negative scores more negative
        
        # Check for positive contexts
        for pattern in self.positive_contexts:
            if re.search(pattern, text_lower):
                # Boost positive sentiment
                if base_score < 0:
                    return min(0.1, base_score + 0.4)  # Reduce negative impact
                else:
                    return min(1.0, base_score + 0.3)  # Boost positive
        
        return base_score
    
    def analyze_sentiment(self, text):
        """Enhanced sentiment analysis with context awareness"""
        if not text or pd.isna(text):
            return {
                'textblob_sentiment': 'Neutral',
                'textblob_score': 0.0,
                'vader_sentiment': 'Neutral',
                'vader_score': 0.0,
                'enhanced_sentiment': 'Neutral',
                'enhanced_score': 0.0,
                'confidence': 'Low'
            }
        
        # Convert to string and handle numeric ratings
        text_str = str(text).strip()
        
        # Handle numeric ratings (1-5 scale)
        if text_str.replace('.', '').replace('-', '').isdigit():
            try:
                rating = float(text_str)
                if 1 <= rating <= 2:
                    return {
                        'textblob_sentiment': 'Negative',
                        'textblob_score': -0.5,
                        'vader_sentiment': 'Negative',
                        'vader_score': -0.5,
                        'enhanced_sentiment': 'Negative',
                        'enhanced_score': -0.5,
                        'confidence': 'High'
                    }
                elif rating == 3:
                    return {
                        'textblob_sentiment': 'Neutral',
                        'textblob_score': 0.0,
                        'vader_sentiment': 'Neutral',
                        'vader_score': 0.0,
                        'enhanced_sentiment': 'Neutral',
                        'enhanced_score': 0.0,
                        'confidence': 'High'
                    }
                elif 4 <= rating <= 5:
                    return {
                        'textblob_sentiment': 'Positive',
                        'textblob_score': 0.5,
                        'vader_sentiment': 'Positive',
                        'vader_score': 0.5,
                        'enhanced_sentiment': 'Positive',
                        'enhanced_score': 0.5,
                        'confidence': 'High'
                    }
            except:
                pass
        
        processed_text = self.preprocess_text(text_str)
        
        # TextBlob analysis
        blob = TextBlob(processed_text)
        tb_score = blob.sentiment.polarity
        
        # VADER analysis
        vader_scores = self.vader.polarity_scores(processed_text)
        vader_score = vader_scores['compound']
        
        # Enhanced analysis with context awareness
        enhanced_score = (tb_score + vader_score) / 2  # Average of both
        enhanced_score = self.context_aware_adjustment(processed_text, enhanced_score)
        
        # Determine sentiment labels with adjusted thresholds
        def get_sentiment_label(score):
            if score >= 0.1:
                return 'Positive'
            elif score <= -0.1:
                return 'Negative'
            else:
                return 'Neutral'
        
        # Calculate confidence based on agreement between methods
        agreement = abs(tb_score - vader_score)
        if agreement < 0.2:
            confidence = 'High'
        elif agreement < 0.5:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        return {
            'textblob_sentiment': get_sentiment_label(tb_score),
            'textblob_score': round(tb_score, 3),
            'vader_sentiment': get_sentiment_label(vader_score),
            'vader_score': round(vader_score, 3),
            'enhanced_sentiment': get_sentiment_label(enhanced_score),
            'enhanced_score': round(enhanced_score, 3),
            'confidence': confidence
        }

# Initialize analyzer
analyzer = EnhancedSentimentAnalyzer()

# App title
st.title("🎯 Sentiment Analysis Tool")
st.markdown("Enhanced accuracy with context-aware analysis")

# Create tabs
tab1, tab2 = st.tabs(["📝 Single Text Analysis", "📊 CSV File Analysis"])

# Tab 1: Single Text Analysis
with tab1:
    st.subheader("Analyze Single Text")
    
    user_input = st.text_area("Enter text to analyze:", height=100, 
                             placeholder="e.g., 'This product could be better' or 'I absolutely love this!'")
    
    if st.button("Analyze Sentiment", type="primary"):
        if user_input:
            result = analyzer.analyze_sentiment(user_input)
            
            st.markdown("### 📊 Analysis Results")
            
            # Create results table
            results_table = pd.DataFrame({
                'Algorithm': ['TextBlob', 'VADER', 'Enhanced'],
                'Sentiment': [result['textblob_sentiment'], result['vader_sentiment'], result['enhanced_sentiment']],
                'Score': [result['textblob_score'], result['vader_score'], result['enhanced_score']],
                'Confidence': [result['confidence'], result['confidence'], result['confidence']]
            })
            
            st.dataframe(results_table, use_container_width=True, hide_index=True)
            
            # Show explanation for enhanced results
            if "could be better" in user_input.lower():
                st.info("🧠 **Context Detection**: Detected phrase 'could be better' - adjusted to reflect the critical nature of this feedback.")
            
            st.markdown("---")
            st.markdown("**📋 Score Guide:** Positive: > 0.1 | Neutral: -0.1 to 0.1 | Negative: < -0.1")
        else:
            st.warning("Please enter some text to analyze.")

# Tab 2: CSV Analysis
with tab2:
    st.subheader("Analyze CSV File")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("### 📄 File Preview")
            st.dataframe(df.head())
            
            # Column selection - Allow ALL columns to be analyzed
            all_columns = df.columns.tolist()
            selected_column = st.selectbox("Select column to analyze:", all_columns)
            
            if st.button("🚀 Analyze All Rows", type="primary"):
                if selected_column:
                    with st.spinner("Analyzing... This may take a moment for large files."):
                        # Apply enhanced analysis to all rows
                        results = []
                        for idx, text in enumerate(df[selected_column]):
                            result = analyzer.analyze_sentiment(text)
                            results.append(result)
                        
                        # Create results DataFrame
                        results_df = pd.DataFrame(results)
                        final_df = pd.concat([df, results_df], axis=1)
                        
                        st.success(f"✅ Analysis complete! Processed {len(df)} rows.")
                        
                        # Show results summary
                        st.write("### 📊 Results Summary")
                        
                        # Use enhanced sentiment for visualization (most accurate)
                        enhanced_counts = final_df['enhanced_sentiment'].value_counts()
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Pie chart
                            fig = px.pie(values=enhanced_counts.values, 
                                       names=enhanced_counts.index,
                                       title="Enhanced Sentiment Distribution",
                                       color_discrete_map={
                                           'Positive': '#2E8B57',
                                           'Negative': '#DC143C', 
                                           'Neutral': '#696969'
                                       })
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Summary statistics
                            st.write("**Enhanced Analysis Results:**")
                            for sentiment, count in enhanced_counts.items():
                                percentage = (count/len(df)*100)
                                st.write(f"• {sentiment}: {count} ({percentage:.1f}%)")
                            
                            avg_score = final_df['enhanced_score'].mean()
                            st.write(f"• Average Score: {avg_score:.3f}")
                            
                            high_confidence = (final_df['confidence'] == 'High').sum()
                            confidence_pct = (high_confidence/len(df)*100)
                            st.write(f"• High Confidence: {high_confidence} ({confidence_pct:.1f}%)")
                        
                        # Show detailed results
                        st.write("### 📋 Detailed Results")
                        st.dataframe(final_df)
                        
                        # Download results
                        csv = final_df.to_csv(index=False)
                        st.download_button(
                            label="💾 Download Enhanced Results as CSV",
                            data=csv,
                            file_name='enhanced_sentiment_analysis_results.csv',
                            mime='text/csv'
                        )
                        
                else:
                    st.warning("Please select a column to analyze.")
                    
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# Footer
st.markdown("---")
st.markdown("🎯 **Enhanced Features**: Context-aware analysis, confidence scoring, and improved accuracy for complex phrases.")