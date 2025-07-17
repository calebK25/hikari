import duckdb, os
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def chat(messages, model="moonshotai/kimi-dev-72b:free"):
    # Try different models if one fails
    models_to_try = [
        "moonshotai/kimi-dev-72b:free",  # Kimi
        "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",  # Dolphin Mistral 24B Venice
        "google/gemma-3n-e2b-it:free",  # Google Gemma 3n 2B
        "mistralai/mistral-small-3.2-24b-instruct:free",  # Mistral Small 3.2 24B
        "deepseek/deepseek-r1-0528-qwen3-8b:free"  # DeepSeek R1 0528 Qwen3 8B
    ]
    
    for model_name in models_to_try:
        try:
            resp = client.chat.completions.create(model=model_name, messages=messages)
            return resp
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            continue
    
    # If all models fail, raise the last error
    raise Exception("All available models are currently unavailable")