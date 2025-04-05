from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import re

app = FastAPI(title="BGL Log Classification API")

# Determine the project root by moving up two levels from this file's location (since this file is in /src/api/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_dir = os.path.join(project_root, 'model')

# Load the trained model and TF-IDF vectorizer
model_path = os.path.join(model_dir, 'log_classification_model.pkl')
vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
except Exception as e:
    raise RuntimeError(f"Error loading model or vectorizer: {e}")

def clean_text(text: str) -> str:
    """
    Clean the input text by converting to lowercase, 
    removing numbers, punctuation, and extra spaces.
    """
    text = text.lower()
    text = re.sub(r'\d+', '', text)             # Remove numbers
    text = re.sub(r'[^\w\s]', '', text)          # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()     # Remove extra spaces
    return text

class LogRequest(BaseModel):
    log_message: str

@app.post("/predict")
def predict_log(request: LogRequest):
    """
    Accept a log message, preprocess it, transform it using the TF-IDF vectorizer,
    and predict whether it's an alert (1) or non-alert (0).
    """
    if not request.log_message:
        raise HTTPException(status_code=400, detail="Log message is required.")
    
    cleaned = clean_text(request.log_message)
    features = vectorizer.transform([cleaned])
    prediction = model.predict(features)
    
    return {"predicted_label": int(prediction[0])}

@app.get("/")
def read_root():
    return {"message": "Welcome to the BGL Log Classification API. Use the /predict endpoint to classify a log message."}
