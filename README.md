eWOM AI Review Detector by Bogiatzis Alexandros
A real-time ecosystem designed to detect AI-generated electronic word-of-mouth (eWOM) reviews on e-commerce platforms. This project bridges theoretical research on market integrity with a practical, local-first detection tool.

By combining a fine-tuned Transformer model (RoBERTa) with hard linguistic pattern analysis (NLTK), this tool seamlessly injects color-coded trust signals directly into the Amazon review interface.

 Features
Real-Time DOM Injection: Uses a MutationObserver to instantly scan and attach visual badges to reviews the moment they load on the page.
Dual-Engine Analysis:

Neural Pattern Recognition: Utilizes roberta-base-openai-detector to identify semantic LLM fingerprints and vocabulary loops.

Linguistic Math (Burstiness): Uses NLTK to calculate sentence length variance. (Humans write chaotically; AI writes with uniform structure).

Native UI Integration: Replaces clunky buttons with sleek, color-coded badges (Green = Human, Yellow = Moderate Risk, Red = AI) that blend into the e-commerce layout.

Local-First Processing: Runs the machine learning inference entirely locally via a FastAPI backend, ensuring zero data privacy leaks.

 Architecture & Tech Stack
Backend: Python, FastAPI, Uvicorn
Machine Learning: HuggingFace Transformers, PyTorch
Linguistic Analysis: NLTK (Natural Language Toolkit)
Frontend: Chrome Extension (Manifest V3, Vanilla JavaScript, CSS)

 Installation & Setup
1. Start the Backend API (Python)
Ensure you have Python 3.8+ installed.

Bash
# Clone the repository
git clone https://github.com/yourusername/ewom-ai-detector.git
cd ewom-ai-detector/backend

# Install the required dependencies
pip install fastapi uvicorn transformers torch nltk

# Start the local server
uvicorn main:app --reload
Note: On the first run, the server will download the RoBERTa model weights (~400MB) and NLTK sentence tokenizers.

2. Install the Browser Extension (Chrome)
Open Google Chrome and navigate to chrome://extensions/.
Enable Developer mode using the toggle in the top right corner.
Click the Load unpacked button in the top left.
Select the extension folder located inside the cloned repository.

Usage
Ensure the Python backend is running in your terminal in by adding it in the code files
Navigate to any product page on Amazon (supports .com, .de, .co.uk, etc.).

Scroll down to the reviews section.

The extension will automatically scrape the review text, send it to your local API, and append a color-coded risk badge to every review.

How the Algorithm Works:
The backend processes eWOM text through a two-part security pipeline:

The Neural Network: The RoBERTa model tokenizes the text and analyzes it through self-attention layers. It looks for mathematical predictability (perplexity) and statistical matches to known AI training data, outputting a probability score.

The Linguistic Math: The NLTK pipeline tokenizes the text into sentences and calculates the variance in word count per sentence (burstiness). High variance suggests human writing, while mathematically uniform sentence structures heavily indicate LLM generation.
