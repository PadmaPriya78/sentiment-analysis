"""
Text preprocessing module for sentiment analysis
"""
import re
import string
from typing import List, Optional
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class TextPreprocessor:
    """Text preprocessing class for sentiment analysis"""
    
    def __init__(self):
        """Initialize the text preprocessor"""
        self.stop_words = None
        self._download_nltk_data()
        self._load_stopwords()
    
    def _download_nltk_data(self):
        """Download required NLTK data if not present"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("Downloading NLTK stopwords...")
            nltk.download('stopwords', quiet=True)
    
    def _load_stopwords(self):
        """Load English stopwords"""
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            print(f"Warning: Could not load stopwords: {e}")
            self.stop_words = set()
    
    def remove_urls(self, text: str) -> str:
        """
        Remove URLs from text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with URLs removed
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    def remove_mentions(self, text: str) -> str:
        """
        Remove @mentions from text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with mentions removed
        """
        return re.sub(r'@\w+', '', text)
    
    def remove_hashtags(self, text: str) -> str:
        """
        Remove hashtags from text (keeps the text, removes #)
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with hashtags removed
        """
        return re.sub(r'#(\w+)', r'\1', text)
    
    def remove_extra_whitespace(self, text: str) -> str:
        """
        Remove extra whitespace and normalize spaces
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        return text.strip()
    
    def remove_punctuation(self, text: str, keep_sentence_ending: bool = True) -> str:
        """
        Remove punctuation from text
        
        Args:
            text (str): Input text
            keep_sentence_ending (bool): Keep sentence ending punctuation
            
        Returns:
            str: Text with punctuation removed
        """
        if keep_sentence_ending:
            # Keep sentence ending punctuation
            translator = str.maketrans('', '', string.punctuation.replace('.', '').replace('!', '').replace('?', ''))
        else:
            # Remove all punctuation
            translator = str.maketrans('', '', string.punctuation)
        
        return text.translate(translator)
    
    def remove_numbers(self, text: str) -> str:
        """
        Remove numbers from text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with numbers removed
        """
        return re.sub(r'\d+', '', text)
    
    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords from text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with stopwords removed
        """
        if not self.stop_words:
            return text
        
        try:
            tokens = word_tokenize(text.lower())
            filtered_tokens = [token for token in tokens if token.lower() not in self.stop_words]
            return ' '.join(filtered_tokens)
        except Exception as e:
            print(f"Warning: Could not remove stopwords: {e}")
            return text
    
    def expand_contractions(self, text: str) -> str:
        """
        Expand common contractions
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with contractions expanded
        """
        contractions = {
            "ain't": "am not",
            "aren't": "are not",
            "can't": "cannot",
            "couldn't": "could not",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he would",
            "he'll": "he will",
            "he's": "he is",
            "i'd": "i would",
            "i'll": "i will",
            "i'm": "i am",
            "i've": "i have",
            "isn't": "is not",
            "it'd": "it would",
            "it'll": "it will",
            "it's": "it is",
            "let's": "let us",
            "shouldn't": "should not",
            "that's": "that is",
            "there's": "there is",
            "they'd": "they would",
            "they'll": "they will",
            "they're": "they are",
            "they've": "they have",
            "we'd": "we would",
            "we'll": "we will",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what's": "what is",
            "where's": "where is",
            "who's": "who is",
            "won't": "will not",
            "wouldn't": "would not",
            "you'd": "you would",
            "you'll": "you will",
            "you're": "you are",
            "you've": "you have"
        }
        
        for contraction, expansion in contractions.items():
            text = re.sub(re.escape(contraction), expansion, text, flags=re.IGNORECASE)
        
        return text
    
    def clean_text(self, text: str, 
                  remove_urls: bool = True,
                  remove_mentions: bool = True,
                  remove_hashtags: bool = True,
                  remove_punctuation: bool = True,
                  remove_numbers: bool = False,
                  remove_stopwords: bool = True,
                  expand_contractions: bool = True,
                  convert_lowercase: bool = True) -> str:
        """
        Clean text using specified preprocessing steps
        
        Args:
            text (str): Input text
            remove_urls (bool): Remove URLs
            remove_mentions (bool): Remove @mentions
            remove_hashtags (bool): Remove hashtags
            remove_punctuation (bool): Remove punctuation
            remove_numbers (bool): Remove numbers
            remove_stopwords (bool): Remove stopwords
            expand_contractions (bool): Expand contractions
            convert_lowercase (bool): Convert to lowercase
            
        Returns:
            str: Cleaned text
        """
        if not isinstance(text, str):
            return ""
        
        # Basic cleaning
        cleaned_text = text
        
        # Remove URLs
        if remove_urls:
            cleaned_text = self.remove_urls(cleaned_text)
        
        # Remove mentions
        if remove_mentions:
            cleaned_text = self.remove_mentions(cleaned_text)
        
        # Remove hashtags
        if remove_hashtags:
            cleaned_text = self.remove_hashtags(cleaned_text)
        
        # Expand contractions
        if expand_contractions:
            cleaned_text = self.expand_contractions(cleaned_text)
        
        # Convert to lowercase
        if convert_lowercase:
            cleaned_text = cleaned_text.lower()
        
        # Remove punctuation
        if remove_punctuation:
            cleaned_text = self.remove_punctuation(cleaned_text)
        
        # Remove numbers
        if remove_numbers:
            cleaned_text = self.remove_numbers(cleaned_text)
        
        # Remove stopwords
        if remove_stopwords:
            cleaned_text = self.remove_stopwords(cleaned_text)
        
        # Final cleanup
        cleaned_text = self.remove_extra_whitespace(cleaned_text)
        
        return cleaned_text
    
    def preprocess_batch(self, texts: List[str], **kwargs) -> List[str]:
        """
        Preprocess a batch of texts
        
        Args:
            texts (List[str]): List of input texts
            **kwargs: Preprocessing options
            
        Returns:
            List[str]: List of cleaned texts
        """
        return [self.clean_text(text, **kwargs) for text in texts]