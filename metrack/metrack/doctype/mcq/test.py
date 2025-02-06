import requests

def clean_mcq_format(mcq):
    url = "http://ollama:11434"

    prompt = f"""
    Please clean and format the following MCQ text. Remove any unnecessary spaces, extra lines, and ensure proper alignment. Do not change the content, meaning, or language of the text.  Format the output like this:

    Question: What is the capital of France?
    A: Paris
    B: London
    C: Berlin
    D: Rome
    Explanation: Paris is the capital of France.

    Input:
    Question: {mcq['question']}
    A: {mcq['a']}
    B: {mcq['b']}
    C: {mcq['c']}
    D: {mcq['d']}
    Explanation: {mcq['explanation']}
    """

    try:
        response = requests.post(url, json={"model": "mistral", "prompt": prompt}, timeout=10)
        response.raise_for_status()  # Check for HTTP errors

        response_json = response.json()
        if "response" in response_json:
            return response_json["response"]
        elif "error" in response_json:
            print(f"Ollama Error: {response_json['error']}")
            return None
        else:
            print("Unexpected response from Ollama:", response_json)
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None

# Sample MCQ data
mcq_data = {
    "question": "What is the capital of France? ",
    "a": " Paris ",
    "b": " London ",
    "c": " Berlin ",
    "d": " Rome ",
    "explanation": "Paris is the capital of France.  "
}

cleaned_mcq = clean_mcq_format(mcq_data)
if cleaned_mcq:
    print("Cleaned and Formatted MCQ:", cleaned_mcq)