from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load a real AI detector model (it will download ~400MB the first time you run the server)
print("Loading HuggingFace AI Model... (this takes a minute on startup)")
detector = pipeline("text-classification", model="roberta-base-openai-detector")
print("Model loaded and ready!")

class Review(BaseModel):
    text: str

@app.post("/analyze")
def analyze_review(review: Review):
    print(f"Analyzing: {review.text[:50]}...")
    
    # Models crash if you feed them a whole novel, so we cap it at 500 characters for safety
    safe_text = review.text[:500]
    
    try:
        # The model outputs a dictionary like: [{'label': 'Fake', 'score': 0.98}]
        result = detector(safe_text)[0]
        
        # Convert the model's confidence into our 0-100% AI probability score
        if result['label'] == 'Fake':
            probability = result['score'] * 100
        else:
            # If it thinks it's Real, the AI probability is the inverse
            probability = (1 - result['score']) * 100
            
        final_score = round(probability, 1)
        
    except Exception as e:
        print("Model error:", e)
        final_score = 50.0 # Neutral fallback if something breaks

    return {"score": final_score}