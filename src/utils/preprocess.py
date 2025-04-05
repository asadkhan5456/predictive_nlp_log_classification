import re
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

# Bypass SSL verification for downloading stopwords if needed
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Clean the log message text:
      - Convert to lowercase
      - Remove numbers (if desired)
      - Remove punctuation
      - Remove extra whitespace
    """
    text = text.lower()
    text = re.sub(r'\d+', '', text)             # Remove numbers; comment this line if numbers are needed
    text = re.sub(r'[^\w\s]', '', text)          # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()     # Remove extra spaces
    return text

def tokenize_text(text):
    """
    Tokenize the cleaned text and remove stopwords.
    """
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def preprocess_bgl_logs(df):
    """
    Preprocess the BGL log DataFrame:
      - Clean the 'log_message' column
      - Tokenize the cleaned text
    """
    # Check if 'log_message' exists; if not, handle accordingly
    if 'log_message' not in df.columns:
        raise ValueError("Column 'log_message' not found in DataFrame.")
        
    df['cleaned_text'] = df['log_message'].apply(clean_text)
    df['tokens'] = df['cleaned_text'].apply(tokenize_text)
    return df

def extract_tfidf_features(df, text_column='cleaned_text'):
    """
    Convert text data into TF-IDF features.
    Returns the feature matrix and the fitted vectorizer.
    """
    vectorizer = TfidfVectorizer(max_features=5000)
    features = vectorizer.fit_transform(df[text_column])
    return features, vectorizer

if __name__ == '__main__':
    # Determine the project root by moving up three directories from this file's location
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(project_root, 'data', 'processed', 'parsed_bgl_logs.csv')
    
    # Load the parsed BGL log dataset
    df = pd.read_csv(data_path)
    
    # Preprocess the logs: clean the log_message and tokenize
    df = preprocess_bgl_logs(df)
    
    print("Preprocessing completed. Sample log messages, cleaned text, and tokens:")
    print(df[['log_message', 'cleaned_text', 'tokens']].head())
    
    # Extract TF-IDF features for further modeling
    tfidf_features, vectorizer = extract_tfidf_features(df)
    print("TF-IDF feature matrix shape:", tfidf_features.shape)
