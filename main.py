from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# Allow Chrome to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    text: str

@app.post("/analyze")
def analyze_review(review: Review):
    print(f"Received review: {review.text[:50]}...")
    # Fake AI detection score for testing the connection
    fake_score = round(random.uniform(10, 99), 1)
    return {"score": fake_score}