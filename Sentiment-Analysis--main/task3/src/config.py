"""
Configuration settings for sentiment analysis project
"""
import os
from pathlib import Path

class Config:
    """Configuration class for sentiment analysis application"""
    
    def __init__(self):
        """Initialize configuration settings"""
        
        # Project paths
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / "data"
        self.models_dir = self.project_root / "models"
        self.output_dir = self.project_root / "output"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Text preprocessing settings
        self.remove_stopwords = True
        self.remove_punctuation = True
        self.convert_to_lowercase = True
        self.remove_numbers = False
        self.min_text_length = 3
        self.max_text_length = 10000
        
        # Sentiment analysis settings
        self.use_textblob = True
        self.use_vader = True
        self.confidence_threshold = 0.1
        
        # TextBlob settings
        self.textblob_neutral_threshold = 0.1
        
        # VADER settings
        self.vader_positive_threshold = 0.05
        self.vader_negative_threshold = -0.05
        
        # Output settings
        self.save_detailed_results = True
        self.include_confidence_scores = True
        self.output_format = "csv"  # csv, json, xlsx
        
        # Display settings
        self.max_display_length = 100
        self.show_statistics = True
        self.show_progress = True
        
        # Performance settings
        self.batch_size = 1000
        self.enable_multiprocessing = False
        self.max_workers = 4
        
        # Logging settings
        self.log_level = "INFO"
        self.log_to_file = False
        self.log_file = "sentiment_analysis.log"