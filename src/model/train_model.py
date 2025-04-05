import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def load_data():
    # Determine the project root by moving up three directories from this file's location
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(project_root, 'data', 'processed', 'parsed_bgl_logs.csv')
    df = pd.read_csv(data_path)
    return df

def prepare_data(df):
    # Convert 'alert' column to binary labels: '-' means non-alert (0), otherwise alert (1)
    df['label'] = df['alert'].apply(lambda x: 0 if x.strip() == '-' else 1)
    
    # Use 'cleaned_text' if it exists; otherwise, fallback to 'log_message'
    if 'cleaned_text' in df.columns:
        text_data = df['cleaned_text']
    else:
        text_data = df['log_message'].str.lower()  # minimal cleaning
    return text_data, df['label']

def train_model(X_train, y_train):
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    return clf

if __name__ == '__main__':
    # Load the dataset
    df = load_data()
    print("Data loaded. Shape:", df.shape)
    
    # Prepare the text and labels
    X_text, y = prepare_data(df)
    
    # Split into training and testing sets
    X_train_text, X_test_text, y_train, y_test = train_test_split(X_text, y, test_size=0.2, random_state=42)
    
    # Create TF-IDF features
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)
    
    print("TF-IDF features created. Training model...")
    
    # Train the model
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save the model and vectorizer
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_dir = os.path.join(project_root, 'model')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    joblib.dump(model, os.path.join(model_dir, 'log_classification_model.pkl'))
    joblib.dump(vectorizer, os.path.join(model_dir, 'tfidf_vectorizer.pkl'))
    print("Model and vectorizer saved.")
