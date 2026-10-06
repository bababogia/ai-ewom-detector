from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import nltk
import statistics

# Download required NLTK data for sentence parsing
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True) # Add this line
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading HuggingFace AI Model...")
detector = pipeline("text-classification", model="roberta-base-openai-detector")
print("Model loaded!")

class Review(BaseModel):
    text: str

def calculate_burstiness(text: str) -> float:
    """Measures variance in sentence length. Low variance = highly uniform (likely AI)."""
    sentences = nltk.sent_tokenize(text)
    if len(sentences) < 2:
        return 0.0 # Too short to measure variance
        
    lengths = [len(nltk.word_tokenize(s)) for s in sentences]
    variance = statistics.variance(lengths)
    return round(variance, 2)

@app.post("/analyze")
def analyze_review(review: Review):
    safe_text = review.text[:300]
    
    # 1. Linguistic Pattern Analysis
    burstiness_score = calculate_burstiness(safe_text)
    
    # 2. Transformer Inference
    try:
        result = detector(safe_text)[0]
        probability = result['score'] * 100 if result['label'] == 'Fake' else (1 - result['score']) * 100
        final_score = round(probability, 1)
    except Exception as e:
        print("Model error:", e)
        final_score = 50.0 

    return {
        "score": final_score,
        "burstiness": burstiness_score
    }