# API Keys for different models
API_KEYS = {
    "google_gemini": "your_google_gemini_api_key_here",
    "chatgpt": "your_openai_chatgpt_api_key_here"
}

# API Endpoints for different models
API_ENDPOINTS = {
    "google_gemini": "https://gemini-api.google.com/query",  # Adjust URL if needed
    "chatgpt": "https://api.openai.com/v1/completions"
}

# Model-specific parameters (to be used in LangChain configuration)
MODEL_PARAMS = {
    "google_gemini": {
        "context": "UPSC",  # The context in which the model will generate questions
        "type": "questions"  # The type of output expected from the model (e.g., questions)
    },
    "chatgpt": {
        "model": "gpt-4",  # You can adjust the model version
        "max_tokens": 1500,  # Maximum number of tokens the model should generate
        "temperature": 0.7  # Adjust temperature for creativity (0 = deterministic, 1 = more creative)
    }
}